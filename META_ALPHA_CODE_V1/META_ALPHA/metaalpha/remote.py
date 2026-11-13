"""Accès distant au corpus : abstraction entre Drive réel et un backend local.

C'est la pièce qui rend une session temporaire SANS CONSÉQUENCE :

    télécharger 1 partition  ->  calculer 1 unité  ->  publier 1 artefact  ->  sortir

Aucune session ne « dure ». Chaque session ne fait qu'une unité, puis meurt
proprement. Le runtime suivant reprend l'unité suivante. La durée de session
devient un détail sans effet sur le résultat.

Deux implémentations :
  LocalRemote  : système de fichiers (tests, dry-run) — aucune dépendance.
  DriveRemote  : API Google Drive v3 avec compte de service — utilisé sur
                 Kaggle/Actions où Drive ne peut PAS être monté.
"""
from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol

from .config import sha256_file


class Remote(Protocol):
    def download(self, rel: str, dest: Path) -> Path: ...
    def upload(self, local: Path, rel: str) -> str: ...
    def exists(self, rel: str) -> bool: ...
    def listdir(self, rel: str) -> list[str]: ...
    def read_json(self, rel: str) -> dict: ...
    def write_json(self, rel: str, obj: dict) -> str: ...


# ---------------------------------------------------------------------------
@dataclass
class LocalRemote:
    """Backend local : même sémantique, zéro dépendance. Sert aux tests."""

    root: Path

    def _p(self, rel: str) -> Path:
        return self.root / rel

    def download(self, rel: str, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self._p(rel), dest)
        return dest

    def upload(self, local: Path, rel: str) -> str:
        target = self._p(rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".part")
        shutil.copyfile(local, tmp)
        os.replace(tmp, target)          # publication atomique
        return sha256_file(target)

    def exists(self, rel: str) -> bool:
        return self._p(rel).exists()

    def listdir(self, rel: str) -> list[str]:
        p = self._p(rel)
        return sorted(x.name for x in p.iterdir()) if p.exists() else []

    def read_json(self, rel: str) -> dict:
        return json.loads(self._p(rel).read_text(encoding="utf-8"))

    def write_json(self, rel: str, obj: dict) -> str:
        target = self._p(rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()
        target.write_bytes(data)
        return sha256_file(target)


# ---------------------------------------------------------------------------
@dataclass
class DriveRemote:
    """Google Drive via compte de service (API v3).

    Sur Kaggle, Drive ne peut pas être monté : on passe donc par l'API.
    Le JSON du compte de service est lu depuis Kaggle Secrets, JAMAIS écrit
    dans le dépôt ni dans le notebook.

    Prérequis : partager le dossier Drive avec l'e-mail du compte de service
    (Lecteur sur le corpus, Éditeur sur RESEARCH_V1_*).
    """

    sa_info: dict
    root_folder_id: str
    _svc: object | None = None
    _folders: dict | None = None

    def _service(self):
        if self._svc is None:
            from google.oauth2 import service_account  # import paresseux
            from googleapiclient.discovery import build

            creds = service_account.Credentials.from_service_account_info(
                self.sa_info, scopes=["https://www.googleapis.com/auth/drive"]
            )
            self._svc = build("drive", "v3", credentials=creds, cache_discovery=False)
        return self._svc

    def _find(self, name: str, parent: str | None = None) -> str | None:
        q = f"name = '{name}' and trashed = false"
        if parent:
            q += f" and '{parent}' in parents"
        res = (
            self._service()
            .files()
            .list(q=q, spaces="drive", fields="files(id,name)", supportsAllDrives=True,
                  includeItemsFromAllDrives=True)
            .execute()
        )
        files = res.get("files", [])
        return files[0]["id"] if files else None

    def _resolve_id(self, rel: str, create: bool = False) -> str | None:
        parts = [p for p in rel.strip("/").split("/") if p]
        parent = self.root_folder_id
        for i, part in enumerate(parts):
            last = i == len(parts) - 1
            found = self._find(part, parent)
            if found:
                parent = found
                continue
            if not create:
                return None
            meta = {
                "name": part,
                "parents": [parent],
                **({"mimeType": "application/vnd.google-apps.folder"} if not last else {}),
            }
            parent = (
                self._service().files().create(body=meta, fields="id", supportsAllDrives=True)
                .execute()["id"]
            )
        return parent

    def download(self, rel: str, dest: Path) -> Path:
        from googleapiclient.http import MediaIoBaseDownload

        fid = self._resolve_id(rel)
        if not fid:
            raise FileNotFoundError(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = self._service().files().get_media(fileId=fid, supportsAllDrives=True)
        with open(dest, "wb") as fh:
            dl = MediaIoBaseDownload(fh, req, chunksize=8 * 1024 * 1024)
            done = False
            while not done:
                _, done = dl.next_chunk()
        return dest

    def upload(self, local: Path, rel: str) -> str:
        from googleapiclient.http import MediaFileUpload

        name = Path(rel).name
        parent_rel = str(Path(rel).parent)
        parent_id = self._resolve_id(parent_rel, create=True) if parent_rel != "." else self.root_folder_id
        existing = self._find(name, parent_id)
        media = MediaFileUpload(str(local), resumable=True, chunksize=8 * 1024 * 1024)
        if existing:
            self._service().files().update(
                fileId=existing, media_body=media, supportsAllDrives=True
            ).execute()
        else:
            self._service().files().create(
                body={"name": name, "parents": [parent_id]},
                media_body=media, fields="id", supportsAllDrives=True,
            ).execute()
        return sha256_file(local)

    def exists(self, rel: str) -> bool:
        return self._resolve_id(rel) is not None

    def listdir(self, rel: str) -> list[str]:
        fid = self._resolve_id(rel)
        if not fid:
            return []
        res = (
            self._service().files()
            .list(q=f"'{fid}' in parents and trashed = false", fields="files(name)",
                  pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True)
            .execute()
        )
        return sorted(f["name"] for f in res.get("files", []))

    def read_json(self, rel: str) -> dict:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            p = self.download(rel, Path(td) / "x.json")
            return json.loads(p.read_text(encoding="utf-8"))

    def write_json(self, rel: str, obj: dict) -> str:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / Path(rel).name
            p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return self.upload(p, rel)


def remote_from_env(local_root: str | None = None) -> Remote:
    """Sélectionne le backend : local si METAALPHA_LOCAL_ROOT, sinon Drive."""
    if local_root or os.environ.get("METAALPHA_LOCAL_ROOT"):
        return LocalRemote(Path(local_root or os.environ["METAALPHA_LOCAL_ROOT"]))
    sa = os.environ.get("GDRIVE_SA_JSON")
    folder = os.environ.get("GDRIVE_ROOT_FOLDER_ID")
    if not sa or not folder:
        raise RuntimeError(
            "aucun backend distant configuré : définir GDRIVE_SA_JSON + GDRIVE_ROOT_FOLDER_ID, "
            "ou METAALPHA_LOCAL_ROOT pour un test local"
        )
    return DriveRemote(json.loads(sa), folder)
