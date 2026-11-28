"""Prévision probabiliste — baseline calibrée (Phase 6).

Objet: distribution du |rendement| de la prochaine barre, par quantiles
empiriques d'une fenêtre passée uniquement. Évaluation: couverture des
intervalles sur une période postérieure jamais utilisée pour calibrer.
Aucune fuite: la prévision pour t n'utilise que les données < t.
"""
from __future__ import annotations

import math


def quantile(sorted_vals, q: float) -> float:
    if not sorted_vals:
        raise ValueError("quantile: série vide")
    i = min(len(sorted_vals) - 1, max(0, int(q * len(sorted_vals))))
    return sorted_vals[i]


def evaluate_coverage(returns, window: int = 200, quantiles=(0.1, 0.5, 0.9)) -> dict:
    """Couverture hors échantillon glissante: pour chaque t >= window,
    l'intervalle [q10, q90] passé doit contenir |r_t| ~80% du temps."""
    absr = [abs(x) for x in returns]
    hits, total, med_err = 0, 0, []
    for t in range(window, len(absr)):
        past = sorted(absr[t - window:t])
        lo, hi = quantile(past, quantiles[0]), quantile(past, quantiles[2])
        med = quantile(past, quantiles[1])
        if lo <= absr[t] <= hi:
            hits += 1
        med_err.append(abs(absr[t] - med))
        total += 1
    if not total:
        raise ValueError("pas assez de données pour évaluer la couverture")
    return {"n_previsions": total, "couverture_q10_q90_pct": round(100 * hits / total, 1),
            "cible_nominale_pct": 80.0, "erreur_mediane_abs": round(sum(med_err) / len(med_err), 3)}
