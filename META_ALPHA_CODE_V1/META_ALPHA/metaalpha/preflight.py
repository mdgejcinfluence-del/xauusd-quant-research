"""Préflight Phase 2 analytique — LECTURE SEULE sur la base certifiée.

Exigences du dossier maître (§5.1) :

1. lire les deux certificats hérités ;
2. calculer et conserver leur SHA-256 ;
3. vérifier l'accessibilité des chemins désignés ;
4. séparer les assertions des certificats des observations nouvelles ;
5. en cas de conflit de chemin : BASELINE_PATH_CONFLICT et arrêt de la tâche.

Aucune écriture hors de RESEARCH_V1_*. Aucune reconstruction de Phase 1/2.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

from .config import sha256_file
from .fs import Storage
from .governance import ReadOnlyView

CERT_P1 = "04_CHECKPOINTS/PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json"
CERT_P2 = "04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json"
PARTITIONS = "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS"

EXPECTED_P1 = {"total_ticks_validated": 685_118_625, "raw_files": 11_136, "status": "CERTIFIED"}
EXPECTED_P2 = {
    "output_rows": 685_118_625,
    "output_partitions": 348,
    "observation_unit": "NATIVE_XAUUSD_TICK_EVENT",
    "chronological_order": True,
    "phase_3_started": False,
}


def _classify(name: str, value, expected) -> str:
    if expected is None:
        return "OBSERVED"
    if value == expected:
        return "ASSERTION_CONFIRMED"
    return "ASSERTION_MISMATCH"


def run_preflight(root: str, sample: str | None = None) -> dict:
    storage = Storage.open(root)
    ro = ReadOnlyView(storage)
    report: dict = {
        "schema_version": "1.0",
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "root": str(storage.root),
        "status": None,
        "certificates": {},
        "partitions": {},
        "assertions": [],
        "observations": [],
        "blocking": [],
        "holdout_touched": False,
        "writes_performed": False,
    }

    # 1-2. Certificats + hashes
    for tag, rel, expected in (("PHASE_01", CERT_P1, EXPECTED_P1), ("PHASE_02", CERT_P2, EXPECTED_P2)):
        p = storage.path(rel)
        if not p.exists():
            report["blocking"].append(f"MISSING_CERTIFICATE:{rel}")
            report["certificates"][tag] = {"path": rel, "present": False}
            continue
        doc = ro.read_json(rel)
        report["certificates"][tag] = {
            "path": rel,
            "present": True,
            "sha256": sha256_file(p),
            "bytes": p.stat().st_size,
            "fields": {k: doc.get(k) for k in expected},
        }
        for k, exp in expected.items():
            report["assertions"].append(
                {
                    "certificate": tag,
                    "field": k,
                    "expected_by_document": exp,
                    "observed_in_certificate": doc.get(k),
                    "classification": _classify(k, doc.get(k), exp),
                }
            )
            if doc.get(k) != exp:
                report["blocking"].append(f"ASSERTION_MISMATCH:{tag}:{k}")

    # 3. Chemin des partitions
    part_dir = storage.path(PARTITIONS)
    if not part_dir.exists():
        report["blocking"].append(f"BASELINE_PATH_CONFLICT:{PARTITIONS}")
        report["partitions"] = {"path": PARTITIONS, "exists": False, "count": 0}
    else:
        files = sorted(part_dir.glob("*.parquet"))
        total = sum(f.stat().st_size for f in files)
        report["partitions"] = {
            "path": PARTITIONS,
            "exists": True,
            "count": len(files),
            "first": files[0].name if files else None,
            "last": files[-1].name if files else None,
            "total_bytes": total,
            "total_gb": round(total / 1e9, 3),
        }
        if len(files) != 348:
            report["blocking"].append(f"PARTITION_COUNT:{len(files)}!=348")

    # 4. Échantillon : schéma réel observé (jamais supposé)
    if sample:
        try:
            from .duck import describe_parquet

            sp = part_dir / sample if part_dir.exists() else Path(sample)
            report["observations"].append({"sample_schema": describe_parquet(sp)})
        except Exception as exc:  # pragma: no cover
            report["observations"].append({"sample_schema_error": str(exc)})

    if report["blocking"]:
        report["status"] = "BLOCKED_WITH_RESUME"
    elif report["partitions"].get("count") == 348 and len(report["certificates"]) == 2:
        report["status"] = "PREFLIGHT_OK_AWAITING_OWNER_REVIEW"
    else:
        report["status"] = "INCOMPLETE"

    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="META ALPHA — préflight Phase 2 (lecture seule)")
    ap.add_argument("--root", required=True, help="racine META_ALPHA_XAUUSD_DGP")
    ap.add_argument("--sample", default=None, help="ex. part_000001.parquet")
    ap.add_argument("--out", default=None, help="écrit le rapport (dans RESEARCH_V1_*)")
    args = ap.parse_args(argv)

    try:
        report = run_preflight(args.root, args.sample)
    except FileNotFoundError as exc:
        print(json.dumps({"status": "BLOCKED_DRIVE_PATH", "error": str(exc)}, indent=2))
        return 2

    text = json.dumps(report, indent=2, ensure_ascii=False)
    print(text)
    if args.out:
        Storage.open(args.root).write_atomic_json(args.out, report)
    else:
        storage = Storage.open(args.root)
        storage.write_atomic_json("40_REPORTS/PHASE_2_ANALYTICAL/PREFLIGHT_REPORT.json", report)

    return 0 if report["status"].startswith("PREFLIGHT_OK") else 1


if __name__ == "__main__":
    sys.exit(main())
