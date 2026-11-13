"""Garde-fou anti-fuite — un dépôt public ne pardonne pas l'erreur.

Le projet a été explicitement décidé public. Cela impose une règle absolue :
aucun secret ne doit pouvoir entrer dans l'arbre git, même par accident, même
dans un fichier de test, même dans un commentaire.

Ce module fait deux choses :

1. `scan_tree()` — parcourt les fichiers suivis par git et détecte les motifs
   de secret connus (clés Kaggle, clés de service Google, tokens GitHub,
   clés cloud). Utilisable en pre-commit et en CI.
2. `assert_no_secret()` — lève si un motif est trouvé, avec le fichier et la
   ligne, jamais avec la valeur.

Il est volontairement bruyant : un faux positif coûte trente secondes, une
clé publiée coûte le projet.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

# Motifs à haute confiance. Un motif trop large produit des faux positifs qui
# poussent à désactiver le garde-fou — donc on reste précis.
PATTERNS: tuple[tuple[str, str], ...] = (
    ("kaggle_token", r"KGAT_[A-Za-z0-9]{20,}"),
    ("google_api_key", r"AIza[0-9A-Za-z_\-]{35}"),
    ("google_oauth_client_secret", r"GOCSPX-[A-Za-z0-9_\-]{28,}"),
    ("github_pat", r"gh[pousr]_[A-Za-z0-9]{36,}"),
    ("aws_access_key", r"AKIA[0-9A-Z]{16}"),
    ("private_key_block", r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    ("slack_token", r"xox[baprs]-[0-9A-Za-z\-]{10,}"),
    ("generic_bearer", r"Bearer\s+eyJ[A-Za-z0-9_\-]{20,}"),
)

# Un fichier de compte de service Google se reconnaît à sa forme, pas à son nom.
SA_JSON_KEYS = ("private_key_id", "client_email", "service_account")

# Fichiers jamais scannés : binaires, caches, et ce module lui-même (il contient
# les motifs, donc il se déclencherait tout seul).
SKIP_SUFFIXES = (".parquet", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".pyc", ".html")
SKIP_PATHS = {"metaalpha/secrets_guard.py", "tests/test_secrets_guard.py"}
# Répertoires jamais suivis : caches, builds (le nom du test contient le faux secret)
SKIP_DIR_PARTS = {".pytest_cache", "__pycache__", ".git", "node_modules", ".ruff_cache"}



def tracked_files(root: Path) -> list[Path]:
    """Fichiers suivis par git. Repli sur un parcours disque hors dépôt git."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=root, capture_output=True, text=True, timeout=30
        )
        if out.returncode == 0 and out.stdout.strip():
            return [root / p for p in out.stdout.splitlines() if p.strip()]
    except (OSError, subprocess.SubprocessError):
        pass
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts:
            files.append(p)
    return files


def _rel(root: Path, p: Path) -> str:
    try:
        return p.relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def scan_text(text: str) -> list[dict[str, Any]]:
    """Détecte les motifs de secret dans une chaîne. Ne renvoie jamais la valeur."""
    hits: list[dict[str, Any]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in PATTERNS:
            m = re.search(pattern, line)
            if m:
                hits.append({
                    "kind": name,
                    "line": lineno,
                    # 6 caractères seulement : assez pour identifier, pas pour exploiter
                    "preview": m.group(0)[:6] + "…",
                })
        if all(k in line for k in ("client_email", "private_key")):
            hits.append({"kind": "google_service_account_json", "line": lineno, "preview": "…"})
    return hits


def scan_file(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    if len(text) > 4_000_000:      # fichier énorme : on ne bloque pas la CI
        return []
    return scan_text(text)


def scan_tree(root: str | Path, *, skip_paths: Iterable[str] = ()) -> dict[str, Any]:
    base = Path(root)
    skip = set(SKIP_PATHS) | set(skip_paths)
    findings: list[dict[str, Any]] = []
    for p in tracked_files(base):
        rel = _rel(base, p)
        if rel in skip or (set(Path(rel).parts) & SKIP_DIR_PARTS):
            continue
        for hit in scan_file(p):
            findings.append({"file": rel, **hit})
    return {
        "files_scanned": len(tracked_files(base)),
        "findings": findings,
        "clean": not findings,
        "rules": [name for name, _ in PATTERNS] + ["google_service_account_json"],
    }


class SecretLeak(RuntimeError):
    """Un secret a été trouvé dans l'arbre. La publication doit s'arrêter."""


def assert_no_secret(root: str | Path) -> None:
    rep = scan_tree(root)
    if not rep["clean"]:
        detail = "; ".join(f"{f['file']}:{f['line']} ({f['kind']})" for f in rep["findings"][:10])
        raise SecretLeak(
            f"{len(rep['findings'])} secret(s) détecté(s) dans l'arbre — publication interdite. "
            f"Détail : {detail}"
        )


def main() -> int:
    import json
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    rep = scan_tree(root)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
