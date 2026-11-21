# CAMPAGNE 5 — DIAGNOSTICS QUALITÉ ET COUVERTURE

- Extraction : 282/282 partitions décennales, 3 540 993 barres M1,
  3 097 journées présentes, 2 572 journées utilisables.
- Contrôle de couverture par fenêtre F-E (V2.2 : attendu, observé,
  taux, trous, statut COMPLETE/PARTIELLE/CENSUREE publiés) :
  fichier `CAMPAIGN_05_WINDOW_COVERAGE.csv` (10 288 × 4 fenêtres) ;
  résumé au registre des censures. Statut COMPLETE pour la journée
  (critère général) : première barre ≤00:10, dernière ≥23:50, aucun
  trou >30 min et couverture ≥95 % — 395 journées ; ce statut n'est
  jamais utilisé comme preuve d'absence d'atteinte.
- Validation temporelle synthétique avant calcul
  (`ci_tools/campaign05_temporal_tests.py`, verte en CI avant
  extraction) : frontières de disponibilité « avant B », distinction
  début de barre / disponibilité, atteinte réelle vs observée, fenêtres
  censurées, retards, mouvement nul, écart des 5 points.
- Vérification de chaîne du registre (219 entrées + seq220/221) par le
  workflow avant tout calcul ; extraction refusée si chaîne KO.
- Reproductibilité : bootstrap 2 000 réplicats, graine 20261113 ;
  moteur `ci_tools/campaign05_engine.py` sha256 `c364dfec…48d9b`,
  synthèse `ci_tools/campaign05_synthesize.py` sha256 `71021545…5887a`.
- Correction post-run 1 : voir incidents. Les sorties régénérées du
  run 44892455679 remplacent intégralement celles du run 44892050419
  pour tout ce qui touche aux atteintes journalières.
