"""L6 — extraction de la matrice, par partition, avec checkpoints durables.

C'est le barreau coûteux de l'échelle. Trois règles le rendent sûr :

1. **Une partition à la fois.** Jamais le corpus entier en mémoire. DuckDB
   écrit le résultat d'une partition, on passe à la suivante.
2. **Checkpoint avant / après.** Une partition terminée est enregistrée avec
   le hash de sa sortie. Relancer ne refait que ce qui manque. Un arrêt de 12 h
   ou une coupure de session ne coûte que la partition en cours.
3. **Aucune variable sans définition.** On n'extrait que les variables
   présentes dans le Variable Registry. Une variable bloquée n'entre pas dans
   la matrice — sinon la matrice contiendrait un paramètre inventé.

Le résultat n'est pas un « résultat scientifique » : c'est une matière première
tracée. Aucune conclusion d'edge ne peut être tirée ici.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Iterable

from .fs import Storage
from . import registry

MATRIX_DIR = "11_EXTRACTION/MATRIX"
CHECKPOINT_REL = "11_EXTRACTION/EXTRACTION_CHECKPOINTS_V1.json"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


# Paramètre attendu par variable, tel qu'écrit par decisions.py.
# Table explicite : si le nom change d'un côté, on veut une erreur bruyante,
# pas un None silencieux.
PARAM_NAME = {
    "ROLL_STD_MID": "N",
    "ROLL_RANGE_MID": "N",
    "MAD_NORM_DEV": "N",
}


def _expr_for(variable_id: str, params: dict[str, Any]) -> str | None:
    """Traduit une variable du Registry en expression SQL.

    Seules les variables dont la sémantique est SANS AMBIGUÏTÉ sont traduites ici.
    Tout le reste lève : on préfère ne pas extraire plutôt qu'extraire faux.
    """
    v = variable_id.upper()

    if v == "MID":
        return "((ask + bid) / 2.0)"
    if v == "SPREAD_ABS":
        return "(ask - bid)"
    if v == "SPREAD_REL":
        return "CASE WHEN (ask + bid) <> 0 THEN (ask - bid) / ((ask + bid) / 2.0) END"
    if v == "RET_TICK":
        return ("((ask + bid) / 2.0) / NULLIF(lag((ask + bid) / 2.0) OVER (ORDER BY t), 0) - 1")

    # --- variables paramétrées : uniquement si le paramètre est EXPLICITE ---
    if v == "ROLL_STD_MID":
        w = params.get(PARAM_NAME["ROLL_STD_MID"])
        n = _as_int(w)
        if n is None:
            raise _MissingParameter(f"ROLL_STD_MID : fenêtre absente ou non entière ({w!r})")
        return (f"stddev_samp((ask + bid) / 2.0) OVER (ORDER BY t "
                f"ROWS BETWEEN {n - 1} PRECEDING AND CURRENT ROW)")

    if v == "ROLL_RANGE_MID":
        w = params.get(PARAM_NAME["ROLL_RANGE_MID"])
        n = _as_int(w)
        if n is None:
            raise _MissingParameter(f"ROLL_RANGE_MID : fenêtre absente ou non entière ({w!r})")
        return (f"(max((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN {n - 1} PRECEDING AND CURRENT ROW)"
                f" - min((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN {n - 1} PRECEDING AND CURRENT ROW))")

    raise _NotTranslatable(f"{variable_id} : pas de traduction SQL certifiée à ce stade")


class _MissingParameter(RuntimeError):
    """Le registre contient la variable mais pas son paramètre : incohérence."""


class _NotTranslatable(RuntimeError):
    """La variable existe mais sa formule n'est pas encore figée : on n'invente pas."""


def _as_int(x: Any) -> int | None:
    try:
        n = int(str(x).strip())
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def plan_extraction(storage: Storage) -> dict[str, Any]:
    """Décide QUOI extraire, sans rien exécuter.

    Rend la liste des variables extractibles et, séparément, celles qui sont
    refusées avec la raison exacte. C'est la partie qui répond à « l'ingénierie
    fera quoi, concrètement ».
    """
    if not storage.exists(registry.VARIABLE_REGISTRY_REL):
        return {"status": "NO_REGISTRY", "extractible": [], "refused": []}

    reg = storage.read_json(registry.VARIABLE_REGISTRY_REL)
    extractible: list[dict[str, Any]] = []
    refused: list[dict[str, Any]] = []

    for key, var in reg.get("variables", {}).items():
        vid = var.get("variable_id") or key.split("@")[0]
        params = var.get("parameters") or {}
        try:
            expr = _expr_for(vid, params)
        except _MissingParameter as exc:
            refused.append({"variable_id": vid, "reason": str(exc), "cause": "PARAMETRE_MANQUANT"})
            continue
        except _NotTranslatable as exc:
            refused.append({"variable_id": vid, "reason": str(exc), "cause": "FORMULE_NON_CERTIFIEE"})
            continue
        extractible.append({"variable_id": vid, "sql": expr, "parameters": params})

    return {
        "status": "PLANNED",
        "extractible_total": len(extractible),
        "refused_total": len(refused),
        "extractible": extractible,
        "refused": refused,
    }


def extract_partition(
    parquet_path: str | Path,
    plan: dict[str, Any],
    *,
    out_path: str | Path,
    ts_col: str = "timestamp",
    bid_col: str = "bid",
    ask_col: str = "ask",
    memory_limit: str = "4GB",
    threads: int = 2,
) -> dict[str, Any]:
    """Écrit la matrice d'UNE partition. Retourne les métriques + le hash."""
    from .duck import connect
    from .config import sha256_file

    feats = plan.get("extractible") or []
    if not feats:
        return {"status": "NOTHING_TO_EXTRACT", "reason": "aucune variable extractible"}

    select_list = ",\n        ".join(f"{f['sql']} AS {f['variable_id']}" for f in feats)
    src = Path(parquet_path).as_posix()
    dst = Path(out_path)
    dst.parent.mkdir(parents=True, exist_ok=True)

    q = f"""
    COPY (
        WITH base AS (
            SELECT "{ts_col}" AS t, "{bid_col}" AS bid, "{ask_col}" AS ask
            FROM read_parquet('{src}')
            ORDER BY "{ts_col}"
        )
        SELECT t, bid, ask,
        {select_list}
        FROM base
    ) TO '{dst.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """

    with connect(memory_limit=memory_limit, threads=threads) as con:
        con.execute(q)
        rows = con.execute(f"SELECT count(*) FROM read_parquet('{dst.as_posix()}')").fetchone()[0]

    return {
        "status": "EXTRACTED",
        "source": str(parquet_path),
        "output": str(dst),
        "rows": int(rows),
        "columns": [f["variable_id"] for f in feats],
        "sha256": sha256_file(dst),
        "size_bytes": dst.stat().st_size,
    }


def run_extraction(
    storage: Storage,
    partitions: Iterable[dict[str, Any]],
    *,
    limit: int | None = None,
) -> dict[str, Any]:
    """Extrait les partitions manquantes, une par une, avec checkpoint durable."""
    plan = plan_extraction(storage)
    if plan["status"] != "PLANNED" or not plan.get("extractible"):
        return {"status": "BLOCKED", "plan": plan,
                "reason": "aucune variable extractible : répondre aux décisions d'abord"}

    ckpt = storage.read_json(CHECKPOINT_REL) if storage.exists(CHECKPOINT_REL) else {
        "schema_version": "1.0", "partitions": {}
    }

    done: list[dict[str, Any]] = []
    skipped: list[str] = []
    errors: list[dict[str, str]] = []

    targets = list(partitions)
    if limit is not None:
        targets = targets[:limit]

    for part in targets:
        pid = part["partition_id"]
        prev = ckpt["partitions"].get(pid)
        if prev and prev.get("status") == "EXTRACTED" and Path(prev["output"]).exists():
            skipped.append(pid)
            continue

        out = storage.root / storage.writable_subdir / MATRIX_DIR / f"{pid}.parquet"
        try:
            res = extract_partition(part["path"], plan, out_path=out)
        except Exception as exc:
            errors.append({"partition_id": pid, "error": f"{type(exc).__name__}: {exc}"})
            ckpt["partitions"][pid] = {"status": "FAILED", "error": str(exc), "utc": _now()}
            storage.write_atomic_json(CHECKPOINT_REL, ckpt)   # checkpoint même en échec
            continue

        ckpt["partitions"][pid] = {**res, "utc": _now()}
        storage.write_atomic_json(CHECKPOINT_REL, ckpt)       # durable, partition par partition
        done.append(res)

    report = {
        "schema_version": "1.0",
        "generated_utc": _now(),
        "plan": plan,
        "extracted_now": len(done),
        "skipped_already_done": len(skipped),
        "failed": len(errors),
        "errors": errors,
        "partitions_done_total": sum(
            1 for v in ckpt["partitions"].values() if v.get("status") == "EXTRACTED"
        ),
        "results": done,
    }
    storage.write_atomic_json("11_EXTRACTION/EXTRACTION_RUN_V1.json", report)
    return report


# ---------------------------------------------------------------------------
# L7 — le contrat : rendre la matrice opposable
# ---------------------------------------------------------------------------
def build_manifest(storage: Storage) -> dict[str, Any]:
    """Scelle la matrice : hash global, lignée, et ce qui reste bloqué.

    Un manifeste n'est pas une décoration : c'est ce qui permet, six mois plus
    tard, de prouver quelle matrice exacte a produit quel résultat — et de
    refuser de comparer deux choses différentes.
    """
    from .config import sha256_text

    if not storage.exists(CHECKPOINT_REL):
        return {"status": "NO_EXTRACTION", "reason": "aucune extraction enregistrée"}

    ckpt = storage.read_json(CHECKPOINT_REL)
    parts = {k: v for k, v in ckpt.get("partitions", {}).items() if v.get("status") == "EXTRACTED"}

    entries = []
    for pid, meta in sorted(parts.items()):
        entries.append({
            "partition_id": pid,
            "source": meta.get("source"),
            "output": meta.get("output"),
            "rows": meta.get("rows"),
            "columns": meta.get("columns"),
            "sha256": meta.get("sha256"),
        })

    var_reg = storage.read_json(registry.VARIABLE_REGISTRY_REL) \
        if storage.exists(registry.VARIABLE_REGISTRY_REL) else {"variables": {}}
    plan = plan_extraction(storage)

    lineage = {
        "variables_used": sorted({c for e in entries for c in (e.get("columns") or [])}),
        "variables_refused": [r["variable_id"] for r in plan.get("refused", [])],
        "registry_sha256": sha256_text(
            str(sorted(var_reg.get("variables", {}).keys()))
        )[:32],
    }

    body = {
        "partitions": entries,
        "lineage": lineage,
        "total_rows": sum(e["rows"] or 0 for e in entries),
    }
    manifest_sha = sha256_text(str(body))[:64]

    manifest = {
        "schema_version": "1.0",
        "generated_utc": _now(),
        **body,
        "manifest_sha256": manifest_sha,
        "honesty": {
            "is_scientific_result": False,
            "note": (
                "Ce manifeste prouve l'intégrité de la matière première, pas "
                "l'existence d'un edge. Le Holdout n'est pas ouvert ici."
            ),
        },
    }
    storage.write_atomic_json("11_EXTRACTION/MANIFEST_V1.json", manifest)
    return manifest
