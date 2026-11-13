"""Configuration : chargement, validation, hash déterministe.

Le config_hash entre dans la clé de checkpoint : toute modification de
configuration invalide légitimement les checkpoints dépendants.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "execution_config.json"


class ConfigError(RuntimeError):
    pass


def canonical_json(obj: Any) -> str:
    """Sérialisation canonique : indispensable pour un hash stable."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | os.PathLike[str], chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return "sha256:" + h.hexdigest()


def code_hash(root: str | os.PathLike[str] | None = None) -> str:
    """Hash de l'arbre de code (hors tests/docs/caches).

    Utilisé dans la clé de checkpoint : si le code change, les unités
    doivent être rejouées.
    """
    root = Path(root or Path(__file__).resolve().parent)
    h = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        h.update(path.name.encode())
        h.update(path.read_bytes())
    return "sha256:" + h.hexdigest()


@dataclass(frozen=True)
class Config:
    raw: dict = field(default_factory=dict)
    sha: str = ""

    @classmethod
    def load(cls, path: str | os.PathLike[str] | None = None) -> "Config":
        p = Path(path or DEFAULT_CONFIG_PATH)
        if not p.exists():
            raise ConfigError(f"configuration absente : {p}")
        with open(p, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        cls._validate(raw)
        return cls(raw=raw, sha=sha256_text(canonical_json(raw)))

    @staticmethod
    def _validate(raw: dict) -> None:
        required = [
            "engine", "budget", "orchestrator", "duckdb", "paths", "governance",
        ]
        missing = [k for k in required if k not in raw]
        if missing:
            raise ConfigError(f"clés de configuration manquantes : {missing}")
        if raw["budget"]["cap_usd"] <= 0:
            raise ConfigError("budget.cap_usd doit être > 0 (un plafond nul doit être explicite : no_llm=true)")
        allowed_status = set(raw["governance"]["terminal_statuses"])
        expected = {
            "PHASE_COMPLETE_AWAITING_OWNER_REVIEW",
            "BLOCKED_WITH_RESUME",
            "FAILED_TECHNICAL",
            "INCOMPLETE",
            "NO_EDGE",
        }
        if allowed_status != expected:
            raise ConfigError(
                "governance.terminal_statuses doit être exactement l'ensemble du kit V1.1 §15.2"
            )

    def get(self, *keys: str, default: Any = None) -> Any:
        node: Any = self.raw
        for k in keys:
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return node

    @property
    def cap_usd(self) -> float:
        return float(self.get("budget", "cap_usd", default=0.0))

    @property
    def no_llm(self) -> bool:
        return bool(self.get("budget", "no_llm", default=True))
