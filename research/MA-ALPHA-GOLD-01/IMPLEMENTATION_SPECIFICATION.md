# SPÉCIFICATION D'IMPLÉMENTATION (simulation uniquement — aucun ordre réel autorisé)

Chaîne : flux Bid/Ask (Dukascopy niveau B aujourd'hui) → barres M15 Mid (chauffe 250 barres) →
détection d'événements 24-B reproduite → score M15_TIME_ONLY gelé (seuil 0,560955) → entrée au
premier tick exécutable ≤ 60 s → deadline 120 min / référence 8 h (bras H17 séparé) →
comptabilité S0/S1/S2, grappes = fenêtres [t0, t0+8h) connexes, bootstrap graine 2129 →
évaluation uniquement à ≈ 350 événements sélectionnés / 140 grappes. Implémenté et auto-testé :
`ci_tools/edge02_dukascopy.py`, `ci_tools/edge02_shadow.py` (selftest CI vert). Déclenchement de
collecte : dispatch manuel par session (le cron GitHub ne vit que sur la branche par défaut).
Aucun capital, aucun compte, aucun ordre : toute activation réelle exigerait une décision
fondateur distincte, hors de ce dossier.
