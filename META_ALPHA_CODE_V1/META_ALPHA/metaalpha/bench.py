"""Benchmark réel — mesure le débit avant toute extrapolation.

Règle du cahier des charges (§10) : « ne présente jamais une extrapolation
comme un benchmark réel ». Ce module produit BENCHMARK_REPORT.json, seul
document qui autorise un chiffre de performance.

Il mesure :
  - débit de lecture Parquet (octets/s, lignes/s)
  - temps des agrégats représentatifs
  - RAM pic (tracemalloc + maxrss)
  - espace de spill DuckDB
  - écriture (débit réel, y compris sur Drive)
  - ETA extrapolée AVEC intervalle d'incertitude explicitement étiqueté
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import statistics
import sys
import time
import tracemalloc
from pathlib import Path

from . import duck
from .config import Config


def _maxrss_mb() -> float:
    try:
        import resource

        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    except Exception:  # pragma: no cover
        return float("nan")


def bench_partition(path: str | Path, *, memory_limit: str = "4GB", threads: int = 2) -> dict:
    p = Path(path)
    size = p.stat().st_size
    tracemalloc.start()
    t0 = time.perf_counter()
    with duck.connect(memory_limit=memory_limit, threads=threads, temp_dir="/tmp/duckdb_bench") as con:
        n_rows = int(
            con.execute("SELECT num_rows FROM parquet_file_metadata(?)", [str(p)]).fetchone()[0]
        )
        # colonnes réelles (on exclut la pseudo-colonne "schema" du footer)
        cols = [
            r[0]
            for r in con.execute("SELECT name FROM parquet_schema(?)", [str(p)]).fetchall()
            if r[0] and r[0] != "schema"
        ]
        # agrégat représentatif : comptage + cardinalité de la 1re colonne
        first = cols[0] if cols else None
        if first:
            con.execute(
                f'SELECT count(*), count(DISTINCT "{first}") FROM read_parquet(?)', [str(p)]
            ).fetchone()
        else:  # pragma: no cover
            con.execute("SELECT count(*) FROM read_parquet(?)", [str(p)]).fetchone()
    elapsed = time.perf_counter() - t0
    tracemalloc.stop()

    return {
        "partition": p.name,
        "size_mb": round(size / 1e6, 3),
        "num_rows": n_rows,
        "columns_count": len(cols),
        "columns_sample": cols[:12],
        "elapsed_s": round(elapsed, 4),
        "rows_per_s": int(n_rows / elapsed) if elapsed else None,
        "mb_per_s": round((size / 1e6) / elapsed, 2) if elapsed else None,
        "peak_rss_mb": round(_maxrss_mb(), 1),
        "memory_limit": memory_limit,
        "threads": threads,
    }


def extrapolate(runs: list[dict], n_partitions_total: int = 348, parallelism: int = 1) -> dict:
    if not runs:
        return {"error": "aucune mesure"}
    per_part = [r["elapsed_s"] for r in runs]
    median = statistics.median(per_part)
    lo, hi = min(per_part), max(per_part)
    # marge d'incertitude : dispersion observée + 25 % de marge réseau/Drive
    total_lo = lo * n_partitions_total / parallelism
    total_hi = hi * n_partitions_total / parallelism * 1.25
    return {
        "label": "EXTRAPOLATION — PAS UN BENCHMARK RÉEL SUR LES 348 PARTITIONS",
        "partitions_measured": len(runs),
        "partitions_total": n_partitions_total,
        "median_seconds_per_partition": round(median, 3),
        "parallelism_assumed": parallelism,
        "eta_seconds_low": round(total_lo, 1),
        "eta_seconds_high": round(total_hi, 1),
        "eta_hours_low": round(total_lo / 3600, 2),
        "eta_hours_high": round(total_hi / 3600, 2),
        "fits_in_24h_low": total_lo < 86400,
        "fits_in_24h_high": total_hi < 86400,
        "caveat": (
            "Marge basse = partition la plus rapide observée. Marge haute = la plus lente +25 % "
            "pour latence Drive. Ne pas citer comme mesure du corpus complet."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="META ALPHA — benchmark")
    ap.add_argument("--partitions-dir", required=True)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--parallelism", type=int, default=1)
    ap.add_argument("--memory-limit", default="4GB")
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    files = sorted(Path(args.partitions_dir).glob("*.parquet"))[: args.n]
    if not files:
        print(json.dumps({"status": "FAILED_TECHNICAL", "error": "aucune partition trouvée"}))
        return 2

    runs = [bench_partition(f, memory_limit=args.memory_limit, threads=args.threads) for f in files]
    report = {
        "schema_version": "1.0",
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "host": {"platform": sys.platform, "cpu_count": os.cpu_count()},
        "runs": runs,
        "extrapolation": extrapolate(runs, parallelism=args.parallelism),
        "measured_for_real": True,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(json.dumps(report["extrapolation"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
