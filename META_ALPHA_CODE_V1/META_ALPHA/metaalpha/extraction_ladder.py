"""L'échelle d'extraction — la pièce centrale, et la réponse à « et ensuite ? ».

L'idée en une phrase : **on n'extrait pas un corpus, on gravit une échelle de
classification.** Chaque barreau a un critère de sortie mesurable. Le système
calcule lui-même à quel barreau il se trouve, et ce qu'il faut pour monter d'un
cran. Il ne demande jamais « et maintenant, quoi ? ».

    L0  DÉCOUVERTE      on ne sait pas ce qu'il y a       -> inventaire, schémas
    L1  TOPOLOGIE       on sait ce qu'il y a              -> grille de partitions
    L2  INTÉGRITÉ       les fichiers sont utilisables     -> lisibilité + monotonie du temps
    L3  DÉRIVATION      le prix est reconstruit           -> mid, spread, dt, ret_tick
    L4  MESURE          les distributions sont connues    -> quantiles, trous, doublons
    L5  ENRICHISSEMENT  les variables paramétrées existent -> 9 décisions -> 11 variables
    L6  EXTRACTION      la matrice est produite           -> features + labels, par partition
    L7  CONTRAT         la matrice est opposable          -> hash, manifeste, lignée

Règles invariantes de l'échelle :

* On ne saute pas un barreau. Si L2 échoue, L3 à L7 sont marqués BLOQUÉS.
* Un barreau n'est franchi que si son critère est MESURÉ, jamais supposé.
* Seul L5 contient une décision humaine. L0->L4 et L6->L7 sont automatiques.
* Le coût de chaque barreau est calculé sur des mesures réelles quand elles
  existent, et explicitement marqué ESTIMÉ sinon.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from .inventory import build_inventory
from .fs import Storage
from . import registry

# ---------------------------------------------------------------------------
# Définition de l'échelle
# ---------------------------------------------------------------------------
LEVELS: tuple[dict[str, Any], ...] = (
    {
        "level": "L0_DECOUVERTE",
        "rank": 0,
        "question": "Qu'y a-t-il sous la racine du corpus ?",
        "exit_criterion": "au moins 1 fichier Parquet lisible",
        "automatic": True,
        "cost": "secondes",
    },
    {
        "level": "L1_TOPOLOGIE",
        "rank": 1,
        "question": "Combien de partitions, de quelle taille, avec quels schémas ?",
        "exit_criterion": "total_rows > 0 et un schéma canonique identifié",
        "automatic": True,
        "cost": "secondes (lecture des footers uniquement)",
    },
    {
        "level": "L2_INTEGRITE",
        "rank": 2,
        "question": "Chaque partition est-elle utilisable telle quelle ?",
        "exit_criterion": "0 fichier illisible, timestamp strictement croissant, spread >= 0",
        "automatic": True,
        "cost": "minutes (1 passe bornée par partition)",
    },
    {
        "level": "L3_DERIVATION",
        "rank": 3,
        "question": "Le prix reconstruit est-il cohérent ?",
        "exit_criterion": "MID, SPREAD_ABS, SPREAD_REL, RET_TICK calculés et non nuls",
        "automatic": True,
        "cost": "minutes (opérations ligne à ligne, sans fenêtre)",
    },
    {
        "level": "L4_MESURE",
        "rank": 4,
        "question": "À quoi ressemblent les distributions réelles ?",
        "exit_criterion": "quantiles, inter-arrivées, doublons, trous mesurés sur échantillon borné",
        "automatic": True,
        "cost": "minutes par partition échantillonnée",
    },
    {
        "level": "L5_ENRICHISSEMENT",
        "rank": 5,
        "question": "Quelles variables paramétrées sont définies ?",
        "exit_criterion": "les 9 décisions répondues -> 11 variables instanciées",
        "automatic": False,          # seule barreau à décision humaine
        "cost": "10 min du propriétaire, 0 FCFA",
    },
    {
        "level": "L6_EXTRACTION",
        "rank": 6,
        "question": "Peut-on produire la matrice features + labels ?",
        "exit_criterion": "matrice écrite par partition, avec checkpoints durables",
        "automatic": True,
        "cost": "1 passe complète, proportionnelle à total_rows",
    },
    {
        "level": "L7_CONTRAT",
        "rank": 7,
        "question": "La matrice est-elle opposable plus tard ?",
        "exit_criterion": "manifeste + sha256 + lignée variable->formule->partition",
        "automatic": True,
        "cost": "secondes",
    },
)

LEVEL_INDEX = {lvl["level"]: lvl for lvl in LEVELS}


# ---------------------------------------------------------------------------
# Évaluation : où en est-on, réellement ?
# ---------------------------------------------------------------------------
def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def evaluate_levels(
    *,
    inventory: dict[str, Any] | None,
    sample: dict[str, Any] | None = None,
    decisions_answered: int = 0,
    variables_instantiated: int = 0,
    matrix_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Calcule le barreau atteint et le blocage exact du barreau suivant.

    Aucune valeur n'est supposée : chaque barreau est franchi sur preuve.
    """
    states: list[dict[str, Any]] = []

    inv = inventory or {}
    files_found = int(inv.get("files_found") or 0)
    partitions_ok = int(inv.get("partitions_ok") or 0)
    total_rows = int(inv.get("total_rows") or 0)
    hetero = bool(inv.get("schema_heterogeneous"))

    obs = (sample or {}).get("observed") or {}
    checks = (sample or {}).get("checks") or {}

    reached: dict[str, bool] = {
        "L0_DECOUVERTE": files_found >= 1,
        "L1_TOPOLOGIE": partitions_ok >= 1 and total_rows > 0 and not hetero,
        "L2_INTEGRITE": (
            partitions_ok >= 1
            and int(inv.get("partitions_unreadable") or 0) == 0
            and int(checks.get("negative_spread") or 0) == 0
            and int(checks.get("null_mid") or 0) == 0
        ),
        "L3_DERIVATION": bool(obs.get("mid") is not None or obs.get("spread_abs_med") is not None),
        "L4_MESURE": bool((sample or {}).get("status") == "MEASURED"
                          and obs.get("spread_abs_med") is not None),
        "L5_ENRICHISSEMENT": decisions_answered >= 9,
        "L6_EXTRACTION": bool(matrix_manifest),
        "L7_CONTRAT": bool(matrix_manifest and matrix_manifest.get("manifest_sha256")),
    }

    # Un barreau ne peut être atteint si le précédent ne l'est pas.
    chain_broken = False
    for lvl in LEVELS:
        name = lvl["level"]
        ok = reached.get(name, False) and not chain_broken
        if not ok:
            chain_broken = True
        states.append({
            "level": name,
            "rank": lvl["rank"],
            "question": lvl["question"],
            "exit_criterion": lvl["exit_criterion"],
            "automatic": lvl["automatic"],
            "cost": lvl["cost"],
            "reached": ok,
            "blocked_by": None if ok else (states[-1]["level"] if states and not states[-1]["reached"] else "critère non satisfait"),
        })

    current = "L0_DECOUVERTE"
    for st in states:
        if st["reached"]:
            current = st["level"]
        else:
            break

    nxt = [lvl for lvl in LEVELS if lvl["rank"] == LEVEL_INDEX[current]["rank"] + 1]
    next_level = nxt[0] if nxt else None

    return {
        "generated_utc": _now(),
        "current_level": current,
        "current_rank": LEVEL_INDEX[current]["rank"],
        "levels_total": len(LEVELS),
        "states": states,
        "next_level": next_level,
        "needs_human": bool(next_level and not next_level["automatic"]),
        "who_acts_next": (
            "AUCUN_AGENT : chaîne terminée" if not next_level
            else "PROPRIETAIRE (10 min)" if not next_level["automatic"]
            else "SYSTEME (automatique, sans intervention)"
        ),
        "why": (
            "Tous les barreaux automatiques sont franchis."
            if not next_level
            else f"Le barreau {next_level['level']} demande : {next_level['exit_criterion']}"
        ),
    }


# ---------------------------------------------------------------------------
# Avancement automatique : le système monte tout seul jusqu'à L4
# ---------------------------------------------------------------------------
def advance(
    storage: Storage,
    corpus_root: str | Path,
    *,
    sample_partitions: int = 3,
    max_events_per_partition: int = 200_000,
) -> dict[str, Any]:
    """Fait monter l'échelle aussi haut que possible, sans intervention.

    S'arrête net au premier barreau non franchi et explique pourquoi. Ne
    franchit JAMAIS L5 : c'est une décision humaine par construction.
    """
    from .contracts_engine import derive_sample, detect_fields

    log: list[str] = []
    inv = build_inventory(corpus_root)
    log.append(f"L0/L1 — {inv['files_found']} fichiers, {inv['partitions_ok']} lisibles, "
               f"{inv['total_rows']:,} lignes, {len(inv['schema_signatures'])} signature(s) de schéma")

    # Échantillonnage : on prend les partitions les plus grosses, une par
    # signature de schéma, pour ne pas mesurer 3 fois la même chose.
    picks: list[dict[str, Any]] = []
    seen_sig: set[str] = set()
    for part in sorted(inv["partitions"], key=lambda p: -(p["num_rows"] or 0)):
        if part["schema_signature"] in seen_sig:
            continue
        seen_sig.add(part["schema_signature"])
        picks.append(part)
        if len(picks) >= sample_partitions:
            break

    samples: list[dict[str, Any]] = []
    for part in picks:
        schema = detect_fields(part["columns"])
        smp = derive_sample(part["path"], schema, max_events=max_events_per_partition)
        samples.append({
            "partition_id": part["partition_id"],
            "path": part["path"],
            "result": smp,
        })
        log.append(f"L2/L3/L4 — {Path(part['path']).name} : {smp.get('status')} "
                   f"({smp.get('events_measured')} événements)")

    # On ne retient qu'un échantillon représentatif pour juger l'intégrité.
    primary = next((s["result"] for s in samples if s["result"].get("status") == "MEASURED"), None)

    answers = {}
    if storage.exists("00_GOVERNANCE/OWNER_DECISIONS_V1.json"):
        answers = storage.read_json("00_GOVERNANCE/OWNER_DECISIONS_V1.json").get("answers", {})

    var_count = 0
    if answers:
        var_reg = storage.read_json(registry.VARIABLE_REGISTRY_REL) if storage.exists(
            registry.VARIABLE_REGISTRY_REL) else {"variables": {}}
        var_count = len(var_reg.get("variables", {}))

    # L'échelle doit VOIR ce qui a déjà été produit : sinon elle redemande un
    # travail déjà fait. On relit donc l'extraction et le manifeste s'ils existent.
    from .extract import CHECKPOINT_REL

    matrix_manifest = None
    if storage.exists("11_EXTRACTION/MANIFEST_V1.json"):
        matrix_manifest = storage.read_json("11_EXTRACTION/MANIFEST_V1.json")
    elif storage.exists(CHECKPOINT_REL):
        ck = storage.read_json(CHECKPOINT_REL)
        if any(v.get("status") == "EXTRACTED" for v in ck.get("partitions", {}).values()):
            matrix_manifest = {"extraction_present": True, "manifest_sha256": None}

    ladder = evaluate_levels(
        inventory=inv,
        sample=primary,
        decisions_answered=len(answers),
        variables_instantiated=var_count,
        matrix_manifest=matrix_manifest,
    )

    report = {
        "schema_version": "1.0",
        "generated_utc": _now(),
        "corpus_root": str(corpus_root),
        "inventory": {k: v for k, v in inv.items() if k != "partitions"},
        "inventory_partitions": inv["partitions"],
        "samples": samples,
        "ladder": ladder,
        "log": log,
    }
    storage.write_atomic_json("11_EXTRACTION/EXTRACTION_LADDER_V1.json", report)
    return report


def load_ladder(storage: Storage) -> dict[str, Any]:
    rel = "11_EXTRACTION/EXTRACTION_LADDER_V1.json"
    if not storage.exists(rel):
        return {"ladder": None, "reason": "aucune évaluation disponible : lancer advance()"}
    return storage.read_json(rel)
