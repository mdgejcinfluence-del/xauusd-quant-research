"""Démonstration exécutable de bout en bout — DONNÉES SYNTHÉTIQUES.

Ce script ne prouve RIEN sur le marché. Il prouve que la chaîne
d'ingénierie fonctionne : préflight -> préparation -> exécution des unités
-> checkpoints -> reprise -> benchmark -> rapport.

Usage :
    python scripts/demo_end_to_end.py --workspace /tmp/metaalpha_demo
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from metaalpha.bench import bench_partition, extrapolate
from metaalpha.config import Config
from metaalpha.fs import Storage
from metaalpha.governance import approve_phase
from metaalpha.orchestrator import Orchestrator
from metaalpha.preflight import run_preflight

ROOT = Path(__file__).resolve().parent.parent


def build_fake_repo(root: Path, n_parts: int = 12, rows: int = 20_000) -> None:
    parts = root / "01_PARQUET" / "XAUUSD_DGP_CHRONOLOGICAL_V5R10" / "PARTITIONS"
    parts.mkdir(parents=True, exist_ok=True)
    (root / "04_CHECKPOINTS").mkdir(parents=True, exist_ok=True)

    (root / "04_CHECKPOINTS" / "PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json").write_text(json.dumps({
        "status": "CERTIFIED", "symbol": "XAUUSD", "raw_files": 11136, "parquet_files": 11136,
        "total_ticks_validated": 685118625, "validated_raw_errors": 0,
        "synthetic_data": False, "interpolation": False,
        "ohlc_substitution": False, "source_substitution": False}))
    (root / "04_CHECKPOINTS" / "PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json").write_text(json.dumps({
        "status": "CERTIFIED", "phase": "PHASE_02", "artifact": "DGP_BASE",
        "output_partitions": 348, "output_rows": 685118625,
        "observation_unit": "NATIVE_XAUUSD_TICK_EVENT", "chronological_order": True,
        "mid_validation": "PASS", "spread_validation": "PASS", "out_of_core": True,
        "formula_registry_status": "PARTIAL", "scientific_families_undefined": 19,
        "phase_3_started": False}))

    for i in range(1, n_parts + 1):
        ts = pa.array([1_600_000_000_000 + j * 137 for j in range(rows)], type=pa.timestamp("ms", tz="UTC"))
        base = 1900.0 + i
        bid = pa.array([base + (j % 211) * 0.01 for j in range(rows)], type=pa.float64())
        ask = pa.array([base + 0.2 + (j % 211) * 0.01 for j in range(rows)], type=pa.float64())
        pq.write_table(pa.table({"timestamp": ts, "bid": bid, "ask": ask}),
                       parts / f"part_{i:06d}.parquet")


def unit_fn(phase: str):
    """Unité de travail de démonstration : agrégat causal par partition.

    Aucune formule scientifique : uniquement des comptages et le spread
    observé, strictement causal (aucun accès au futur).
    """
    def _fn(uid: str, storage: Storage) -> tuple[int, str, str]:
        from metaalpha.duck import connect

        parts = storage.root / "01_PARQUET" / "XAUUSD_DGP_CHRONOLOGICAL_V5R10" / "PARTITIONS"
        src = parts / f"{uid}.parquet"
        out_rel = f"20_DERIVED/{phase}/{uid}.parquet"
        out_path = storage.root / storage.writable_subdir / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with connect(memory_limit="2GB", threads=2, temp_dir="/tmp/duckdb_demo") as con:
            con.execute(
                f"""
                COPY (
                    SELECT
                        date_trunc('day', timestamp) AS day,
                        count(*)                     AS n_ticks,
                        avg(ask - bid)               AS spread_mean_observed,
                        min(timestamp)               AS t_min,
                        max(timestamp)               AS t_max
                    FROM read_parquet('{src.as_posix()}')
                    GROUP BY 1 ORDER BY 1
                ) TO '{out_path.as_posix()}' (FORMAT PARQUET);
                """
            )
            n = con.execute(
                f"SELECT count(*) FROM read_parquet('{out_path.as_posix()}')"
            ).fetchone()[0]

        from metaalpha.config import sha256_file

        rel_norm = str(out_path.relative_to(storage.root / storage.writable_subdir))
        return int(n), rel_norm, sha256_file(out_path)

    return _fn


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default="/tmp/metaalpha_demo")
    ap.add_argument("--parts", type=int, default=12)
    ap.add_argument("--rows", type=int, default=20000)
    args = ap.parse_args()

    ws = Path(args.workspace)
    if ws.exists():
        shutil.rmtree(ws)
    root = ws / "META_ALPHA_XAUUSD_DGP"
    build_fake_repo(root, args.parts, args.rows)

    print("=" * 74)
    print("META ALPHA — DÉMONSTRATION DE BOUT EN BOUT (données SYNTHÉTIQUES)")
    print("=" * 74)

    # 1) préflight (lecture seule)
    rep = run_preflight(str(root), sample="part_000001.parquet")
    print(f"\n[1] PRÉFLIGHT : {rep['status']}")
    print(f"    partitions : {rep['partitions']['count']}   tailles : {rep['partitions']['total_gb']} Go")
    for a in rep["assertions"]:
        print(f"    {a['certificate']:<9} {a['field']:<24} {a['classification']}")
    print(f"    schéma observé : {[c['name'] for c in rep['observations'][0]['sample_schema']['columns']]}")
    if rep["blocking"]:
        print("    ⚠ BLOCAGE ATTENDU :", ", ".join(rep["blocking"]))
        print("      -> Le préflight refuse une base dont le nombre de partitions ne")
        print("         correspond pas au certificat. C'est exactement le garde-fou")
        print("         'BASELINE_PATH_CONFLICT / PARTITION_COUNT' exigé au §5.1.")

    # 2) approbation (simule le geste du propriétaire)
    storage = Storage.open(root)
    approve_phase(storage, "PHASE_2_ANALYTICAL", "demonstration-locale-non-valide",
                  "démo de la machine à états")
    print("\n[2] APPROBATION PHASE_2_ANALYTICAL enregistrée (trace dans 00_GOVERNANCE/approvals)")

    # 3) exécution des unités
    cfg = Config.load(ROOT / "config" / "execution_config.json")
    parts = sorted(p.name for p in (root / "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS").glob("*.parquet"))
    units = [p.replace(".parquet", "") for p in parts]

    orch = Orchestrator(storage, cfg, phase="PHASE_2_ANALYTICAL",
                        unit_fn=unit_fn("PHASE_2_ANALYTICAL"), runtime="demo-runtime")
    out1 = orch.run(units, input_hash_for=lambda u: rep["certificates"]["PHASE_02"]["sha256"] + "#" + u)
    print(f"\n[3] PREMIER PASSAGE : {out1.status}")
    print(f"    exécutées={out1.units_executed} sautées={out1.units_skipped} échecs={out1.units_failed}")

    # 4) idempotence
    out2 = orch.run(units, input_hash_for=lambda u: rep["certificates"]["PHASE_02"]["sha256"] + "#" + u)
    print(f"\n[4] DEUXIÈME PASSAGE (idempotence) : {out2.status}")
    print(f"    exécutées={out2.units_executed} sautées={out2.units_skipped} "
          f"-> {out2.units_skipped}/{len(units)} unités reconnues par checkpoint")

    # 5) benchmark réel sur les partitions (synthétiques) du workspace
    parts_dir = root / "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS"
    files = sorted(parts_dir.glob("*.parquet"))[:3]
    runs = [bench_partition(f, memory_limit="2GB", threads=2) for f in files]
    ext = extrapolate(runs, n_partitions_total=348, parallelism=1)
    print("\n[5] BENCHMARK (mesuré sur 3 partitions SYNTHÉTIQUES, 20k lignes)")
    for r in runs:
        print(f"    {r['partition']}: {r['num_rows']:>7} lignes  {r['elapsed_s']:.3f}s  "
              f"{r['rows_per_s']:>9} lignes/s  RSS {r['peak_rss_mb']} Mo")
    print(f"    extrapolation 348 partitions : {ext['eta_hours_low']}h – {ext['eta_hours_high']}h")
    print("    ⚠ étiquette :", ext["label"])
    print("    ⚠ Ces chiffres ne mesurent PAS le corpus réel : les partitions de démonstration")
    print("      font 20 000 lignes, les vraies en comptent ~2 M. Le débit dominant sera l'I/O.")

    # 6) rapport final
    state = storage.read_json("00_GOVERNANCE/state.json")
    print("\n[6] ÉTAT FINAL")
    print(f"    phase_active      : {state['active_phase']}")
    print(f"    statut            : {state['phase_status']}")
    print(f"    phases terminées  : {state['completed_phases']}")
    print(f"    holdout scellé    : {state['holdout_sealed']}")
    derived = list((root / "RESEARCH_V1_XAUUSD_TICK_ONLY" / "20_DERIVED").rglob("*.parquet"))
    print(f"    dérivés produits  : {len(derived)} fichiers Parquet")
    print("\n   Chemin de démonstration :", ws)
    return 0


if __name__ == "__main__":
    sys.exit(main())
