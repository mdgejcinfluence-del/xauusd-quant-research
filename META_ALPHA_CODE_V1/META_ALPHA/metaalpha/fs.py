"""Abstraction de stockage : local ou Google Drive monté.

Trois garanties, et c'est tout ce que ce module doit garantir :

1. ALLOWLIST D'ÉCRITURE — impossible d'écrire hors des racines autorisées.
   La base certifiée (00_RAW, 01_PARQUET, 04_CHECKPOINTS) est protégée
   structurellement, pas par convention.
2. ÉCRITURE ATOMIQUE — write .tmp -> validate -> rename. Un fichier au nom
   final existe donc toujours complet et valide.
3. HASH — chaque artefact publié est accompagné de son sha256.

Aucune science ici.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

from .config import canonical_json, sha256_file, sha256_text


class WriteDenied(RuntimeError):
    """Tentative d'écriture hors allowlist. Toujours fatale."""


class ValidationFailed(RuntimeError):
    """Le fichier temporaire n'a pas passé la validation : rien n'est publié."""


PROTECTED_DIRS = ("00_RAW", "01_PARQUET", "04_CHECKPOINTS", "02_", "03_")
RESEARCH_DIR = "RESEARCH_V1_XAUUSD_TICK_ONLY"


@dataclass
class Storage:
    root: Path
    writable_subdir: str = RESEARCH_DIR
    _writable_roots: tuple[Path, ...] = ()

    @classmethod
    def open(cls, root: str | os.PathLike[str], writable_subdir: str = RESEARCH_DIR) -> "Storage":
        r = Path(root).resolve()
        if not r.exists():
            # zone de recherche locale (kernel jetable) : on la crée.
            # En production la racine Drive existe déjà ; si elle manque, le
            # préflight lève BASELINE_PATH_CONFLICT avant toute écriture.
            r.mkdir(parents=True, exist_ok=True)
        writable = (r / writable_subdir).resolve()
        writable.mkdir(parents=True, exist_ok=True)
        return cls(root=r, writable_subdir=writable_subdir, _writable_roots=(writable,))

    # ---------- résolution des chemins ----------
    # Convention : un chemin relatif de recherche ("10_REGISTRIES/x.json") est
    # résolu DANS la zone de recherche. Un chemin explicitement préfixé par la
    # racine du projet ("04_CHECKPOINTS/...", "01_PARQUET/...") est résolu à la
    # racine du projet (lecture seule).
    def path(self, rel: str) -> Path:
        return self.root / rel

    def _resolve_read(self, rel: str) -> Path:
        direct = self.root / rel
        if direct.exists():
            return direct
        alt = self.root / self.writable_subdir / rel
        return alt if alt.exists() else direct

    def _resolve_write(self, rel: str) -> Path:
        first = Path(rel).parts[0] if Path(rel).parts else ""
        if first in PROTECTED_DIRS:
            # la base certifiée n'est jamais une cible d'écriture, même via un
            # chemin relatif : on renvoie le chemin réel pour que le refus soit explicite
            return self.root / rel
        direct = self.root / rel
        if str(direct.resolve()).startswith(str((self.root / self.writable_subdir).resolve())):
            return direct
        return self.root / self.writable_subdir / rel

    # ---------- lecture ----------
    def read_json(self, rel: str) -> dict:
        with open(self._resolve_read(rel), "r", encoding="utf-8") as fh:
            return json.load(fh)

    def exists(self, rel: str) -> bool:
        return self._resolve_read(rel).exists()

    # ---------- écriture ----------
    def _assert_writable(self, target: Path) -> None:
        t = target.resolve()
        # 1) la base certifiée est protégée nommément (message explicite)
        if any(str(t) == str(d) or str(t).startswith(str(d) + os.sep)
               for d in PROTECTED_DIRS_FULL(self.root)):
            raise WriteDenied(f"écriture interdite sur la base certifiée : {t}")
        # 2) hors de la zone de recherche => refus, quelle que soit la raison
        if not any(t == w or str(t).startswith(str(w) + os.sep) for w in self._writable_roots):
            raise WriteDenied(
                f"écriture hors espace de recherche autorisé ({self.writable_subdir}) : {t}"
            )

    def write_atomic_bytes(
        self,
        rel: str,
        data: bytes,
        validator: Callable[[Path], None] | None = None,
    ) -> str:
        """Écrit rel de façon atomique. Retourne le sha256 du contenu publié."""
        target = self._resolve_write(rel)
        self._assert_writable(target)
        target.parent.mkdir(parents=True, exist_ok=True)

        tmp = target.parent / f".{target.name}.{uuid.uuid4().hex[:8]}.tmp"
        try:
            with open(tmp, "wb") as fh:
                fh.write(data)
                fh.flush()
                os.fsync(fh.fileno())
            if validator is not None:
                validator(tmp)          # lève ValidationFailed
            os.replace(tmp, target)      # atomique sur le même système de fichiers
        except Exception:
            tmp.unlink(missing_ok=True)
            raise
        return sha256_file(target)

    def write_atomic_json(self, rel: str, obj: Any) -> str:
        payload = (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")

        def _validate(p: Path) -> None:
            with open(p, "r", encoding="utf-8") as fh:
                reloaded = json.load(fh)
            if canonical_json(reloaded) != canonical_json(obj):
                raise ValidationFailed(f"JSON relu != JSON écrit pour {rel}")

        return self.write_atomic_bytes(rel, payload, validator=_validate)

    def append_csv_line(self, rel: str, row: dict, header: Iterable[str]) -> None:
        """Append-only pour le Trial Ledger : jamais de réécriture."""
        target = self._resolve_write(rel)
        self._assert_writable(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        cols = list(header)
        new_file = not target.exists()
        with open(target, "a", encoding="utf-8", newline="") as fh:
            if new_file:
                fh.write(",".join(cols) + "\n")
            fh.write(",".join(_csv_cell(row.get(c, "")) for c in cols) + "\n")

    def try_create_exclusive(self, rel: str, obj: Any) -> bool:
        """Crée le fichier SEULEMENT s'il n'existe pas. Sert de base au lease."""
        target = self._resolve_write(rel)
        self._assert_writable(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return False
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(obj, indent=2, sort_keys=True))
        return True

    # ---------- utilitaires ----------
    def check_free_space(self, min_gb: float) -> None:
        free_gb = shutil.disk_usage(self.root).free / 1e9
        if free_gb < min_gb:
            raise RuntimeError(
                f"espace disque insuffisant : {free_gb:.2f} Go libres < {min_gb} Go requis"
            )

    def cleanup_orphan_tmp(self, max_age_seconds: int = 6 * 3600) -> list[str]:
        """Marque/nettoye les .tmp abandonnés par un runtime mort."""
        removed: list[str] = []
        now = time.time()
        for p in (self.root / self.writable_subdir).rglob("*.tmp"):
            if now - p.stat().st_mtime > max_age_seconds:
                p.unlink(missing_ok=True)
                removed.append(str(p))
        return removed


def PROTECTED_DIRS_FULL(root: Path) -> tuple[Path, ...]:
    return tuple((root / d).resolve() for d in PROTECTED_DIRS)


def _csv_cell(value: Any) -> str:
    s = str(value)
    if any(c in s for c in [",", '"', "\n"]):
        return '"' + s.replace('"', '""') + '"'
    return s


def content_hash(obj: Any) -> str:
    return sha256_text(canonical_json(obj))
