"""Installe le garde-fou secrets comme hook pre-commit.

    python scripts/install_hooks.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    hook = root / ".githooks" / "pre-commit"
    if not hook.exists():
        print(f"hook introuvable : {hook}")
        return 1
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=root, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"échec : {exc}")
        return 1
    hook.chmod(0o755)
    print("hook installé : core.hooksPath = .githooks")
    print("test : créer un fichier contenant un faux secret, puis git commit — il doit être refusé.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
