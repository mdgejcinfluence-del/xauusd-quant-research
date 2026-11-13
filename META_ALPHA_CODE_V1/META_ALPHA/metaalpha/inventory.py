"""Inventaire du corpus — le système découvre, il ne suppose rien.

Contrainte structurante : on ne connaît pas le schéma réel du corpus, on ne
connaît pas sa taille, on n'a pas le droit de le re-télécharger. Donc
l'ingénierie ne peut pas commencer par « voici les colonnes ». Elle commence
par « voici comment on découvre les colonnes ».

Ce module fait exactement trois choses :

1. ÉNUMÉRER les fichiers Parquet d'une racine, sans hypothèse de nommage.
2. LIRE le schéma de chaque fichier (Parquet footer uniquement : aucun octet
   de données n'est lu). Le coût est négligeable même sur des milliers de
   fichiers.
3. GROUPER les fichiers par signature de schéma. Une déviation de schéma est
   un signal fort : elle est enregistrée, jamais corrigée d'office.

Aucune science ici : uniquement de la topologie de stockage.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable

from .contracts_engine import detect_fields
from .config import sha256_text

PARQUET_SUFFIXES = (".parquet", ".pq")


def iter_parquet_files(root: str | os.PathLike[str], *, max_files: int = 100_000) -> list[Path]:
    """Énumère les Parquet sous `root`, triés, bornés. Aucune lecture de données."""
    base = Path(root)
    if not base.exists():
        return []
    out: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for name in filenames:
            if name.lower().endswith(PARQUET_SUFFIXES):
                out.append(Path(dirpath) / name)
                if len(out) >= max_files:
                    out.sort()
                    return out
    out.sort()
    return out


def read_schema_signature(path: str | os.PathLike[str]) -> dict[str, Any]:
    """Lit le schéma d'un Parquet (footer seul). Ne lit AUCUNE ligne."""
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(path)
    md = pf.metadata
    cols = list(pf.schema_arrow.names)
    sig = sha256_text("|".join(cols))
    return {
        "columns": cols,
        "signature": sig[:16],
        "num_rows": int(md.num_rows) if md is not None else None,
        "num_row_groups": int(md.num_row_groups) if md is not None else None,
        "size_bytes": Path(path).stat().st_size,
    }


def build_inventory(
    root: str | os.PathLike[str],
    *,
    max_files: int = 100_000,
) -> dict[str, Any]:
    """Recense le corpus et regroupe par signature de schéma.

    Le résultat est la carte d'entrée de l'extraction : chaque partition y est
    décrite par ce qu'elle EST réellement, pas par ce qu'on croyait qu'elle
    serait.
    """
    files = iter_parquet_files(root, max_files=max_files)
    partitions: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for p in files:
        try:
            meta = read_schema_signature(p)
        except Exception as exc:  # fichier tronqué, corrompu, export partiel
            errors.append({"path": str(p), "error": f"{type(exc).__name__}: {exc}"})
            continue
        det = detect_fields(meta["columns"])
        partitions.append({
            "path": str(p),
            "partition_id": sha256_text(str(p))[:16],
            "schema_signature": meta["signature"],
            "num_rows": meta["num_rows"],
            "size_bytes": meta["size_bytes"],
            "columns": meta["columns"],
            "field_mapping": det["canonical"],
            "has_core_quote_triplet": det["has_core_quote_triplet"],
            "forbidden_fields_present": det["forbidden_fields_present"],
            "unmapped_columns": det["unmapped_columns"],
        })

    by_sig: dict[str, list[str]] = {}
    for part in partitions:
        by_sig.setdefault(part["schema_signature"], []).append(part["partition_id"])

    total_rows = sum(p["num_rows"] or 0 for p in partitions)
    total_bytes = sum(p["size_bytes"] for p in partitions)

    return {
        "root": str(root),
        "schema_version": "1.0",
        "files_found": len(files),
        "partitions_ok": len(partitions),
        "partitions_unreadable": len(errors),
        "unreadable": errors[:50],
        "total_rows": total_rows,
        "total_bytes": total_bytes,
        "schema_signatures": {
            sig: {"count": len(ids), "partition_ids": ids[:20]} for sig, ids in by_sig.items()
        },
        "schema_heterogeneous": len(by_sig) > 1,
        "partitions": partitions,
        # Le système dit lui-même ce qu'il ne sait pas encore.
        "unknowns": [] if partitions else [
            "aucun fichier Parquet sous cette racine : corpus non monté ou chemin incorrect",
        ],
    }
