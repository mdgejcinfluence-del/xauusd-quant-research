"""Audit de calibration de la baseline de volatilité (EXPANSION-001, axe 1).

Couverture globale ET conditionnelle (par tercile de volatilité passée),
largeur moyenne des intervalles, comparaison à une référence
inconditionnelle (quantiles de toute la fenêtre d'apprentissage, sans
glissement). Couverture != précision != utilité économique.
"""
from __future__ import annotations

from .forecast import quantile


def _intervals(absr, window, mode):
    out = []
    for t in range(window, len(absr)):
        past = sorted(absr[:t]) if mode == "inconditionnel" else sorted(absr[t - window:t])
        out.append((quantile(past, 0.1), quantile(past, 0.9), absr[t], past[len(past) // 2]))
    return out


def audit(returns, window: int = 200) -> dict:
    absr = [abs(x) for x in returns]
    res = {}
    for mode in ("glissant", "inconditionnel"):
        iv = _intervals(absr, window, mode)
        hits = sum(1 for lo, hi, y, _ in iv if lo <= y <= hi)
        widths = [hi - lo for lo, hi, _, _ in iv]
        # couverture conditionnelle par tercile de la médiane passée (régime)
        meds = sorted(m for *_, m in iv)
        t1, t2 = meds[len(meds) // 3], meds[2 * len(meds) // 3]
        cond = {}
        for name, pred in (("calme", lambda m: m <= t1), ("moyen", lambda m: t1 < m <= t2), ("agite", lambda m: m > t2)):
            sub = [(lo, hi, y) for lo, hi, y, m in iv if pred(m)]
            cond[name] = round(100 * sum(1 for lo, hi, y in sub if lo <= y <= hi) / len(sub), 1) if sub else None
        res[mode] = {"n": len(iv), "couverture_pct": round(100 * hits / len(iv), 1),
                     "largeur_moyenne": round(sum(widths) / len(widths), 2), "couverture_par_regime": cond}
    return res
