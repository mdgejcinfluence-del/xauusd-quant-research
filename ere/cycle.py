"""Cycle autonome de recherche (Phase 3): OBSERVE -> ... -> SELECT_NEXT.

Chaque transition est un comportement vérifiable, journalisé par le
noyau. Le cycle génère au moins deux hypothèses concurrentes à partir
des structures observées, gèle son protocole (hash), exécute, évalue
selon des critères déclarés AVANT l'exécution, met à jour la mémoire
et sélectionne la prochaine recherche. Il sait s'abstenir (NOT_IDENTIFIED)
et continuer sur les propriétés identifiables.
"""
from __future__ import annotations

import math

from .uncertainty import prioritize_experiments

# Critères déclarés avant exécution (protocole du cycle, non optimisés).
SEUIL_VOL_CLUSTERING = 0.15
SEUIL_SIGN_PERSISTENCE = 0.53


def _acf1_abs(returns) -> float:
    a = [abs(x) for x in returns]
    if len(a) < 12:
        return 0.0
    m = sum(a) / len(a)
    num = sum((a[i] - m) * (a[i - 1] - m) for i in range(1, len(a)))
    den = sum((x - m) ** 2 for x in a)
    return num / den if den else 0.0


def _sign_persistence(returns) -> float:
    if len(returns) < 12:
        return 0.5
    same = sum(1 for i in range(1, len(returns)) if (returns[i] > 0) == (returns[i - 1] > 0))
    return same / (len(returns) - 1)


def run_cycle(kernel, returns, context: str = "synthetique") -> dict:
    """Un tour complet du cycle sur une série de rendements (barres)."""
    tid = kernel.create_task("cycle_recherche", {"context": context, "n": len(returns),
                                                 "seuils": [SEUIL_VOL_CLUSTERING, SEUIL_SIGN_PERSISTENCE]})
    kernel.transition(tid, "RUNNING")
    # OBSERVE
    vol_acf = _acf1_abs(returns); sign_p = _sign_persistence(returns)
    observed = {"vol_clustering_acf1": round(vol_acf, 3), "sign_persistence": round(sign_p, 3), "n": len(returns)}
    # GENERATE_HYPOTHESES (>=2 concurrentes, toujours)
    hyps = [
        {"id": "H-REGIME-VOL", "enonce": "la volatilité persiste (régimes calme/agité)", "prediction": f"acf1 > {SEUIL_VOL_CLUSTERING}"},
        {"id": "H-DIRECTION", "enonce": "les mouvements persistent en signe", "prediction": f"persistance > {SEUIL_SIGN_PERSISTENCE}"},
        {"id": "H-NULLE", "enonce": "aucune structure (marche sans mémoire)", "prediction": "acf1 et persistance proches du hasard"},
    ]
    # DESIGN + FREEZE (le hash du plan est l'identifiant de tâche)
    plan_hash = tid
    # EXECUTE + EVALUATE selon les critères gelés
    verdicts = {}
    verdicts["H-REGIME-VOL"] = "RETENUE" if vol_acf > SEUIL_VOL_CLUSTERING else "REFUTEE"
    verdicts["H-DIRECTION"] = "RETENUE" if sign_p > SEUIL_SIGN_PERSISTENCE else "REFUTEE"
    verdicts["H-NULLE"] = "REFUTEE" if "RETENUE" in verdicts.values() else "RETENUE"
    retenues = [h for h, v in verdicts.items() if v == "RETENUE"]
    qualification = "STRUCTURE_DETECTEE" if retenues and retenues != ["H-NULLE"] else "NOT_IDENTIFIED"
    # UPDATE_KNOWLEDGE
    kernel.put_knowledge(f"cycle:{context}", {"observed": observed, "verdicts": verdicts, "qualification": qualification})
    # SELECT_NEXT_RESEARCH (priorisation: départager ce qui reste, coût faible d'abord)
    candidats = [
        {"nom": "etendre_aux_partitions_par_annee", "hypotheses_departagees": 2, "cout_relatif": 2.0, "segment_disponible": True},
        {"nom": "repliquer_sur_autre_periode", "hypotheses_departagees": 1, "cout_relatif": 1.0, "segment_disponible": True},
        {"nom": "ouvrir_segment_protege", "hypotheses_departagees": 3, "cout_relatif": 0.5, "segment_disponible": False},
    ]
    next_research = prioritize_experiments(candidats)[0]["nom"]
    result = {"observed": observed, "hypotheses": [h["id"] for h in hyps], "plan_hash": plan_hash,
              "verdicts": verdicts, "qualification": qualification, "prochaine_recherche": next_research}
    kernel.transition(tid, "COMPLETED", result)
    return result
