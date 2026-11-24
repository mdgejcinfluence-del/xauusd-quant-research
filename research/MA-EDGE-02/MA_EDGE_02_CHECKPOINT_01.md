# MA-EDGE-02 — CHECKPOINT 01 (seq409 → seq410)

## Ce qui a changé depuis la clôture MA-EDGE-01

Le blocage « aucun flux Bid/Ask » est **résolu pour l'observation** : le flux historique public
Dukascopy (fichiers horaires `.bi5`, Bid/Ask au tick, UTC ms, sans compte ni clé) est vérifié en
conditions réelles depuis le runner CI : heures échantillons de 42 899 à 49 642 ticks, **zéro
violation Bid < Ask**, horodatages strictement croissants, spread médian 0,40–0,45 USD
(≈ 1 bp au prix courant), écart inter-tick maximal < 3 s. Classement complet de 8 sources
(niveaux A/B/C, motifs de rejet) : `FEED_RESEARCH_REPORT.md`. Limite mesurée : publication des
fichiers horaires par lots avec plusieurs heures de retard (l'heure close 15:00 était disponible
à 17:45 ; l'heure 17:00 ne l'était pas encore à 18:50) — compatible avec une collecte
quotidienne, incompatible avec une exécution temps réel, ce que SHADOW n'exige pas.

## Travaux livrés

- `ci_tools/edge02_dukascopy.py` : connecteur (probe/collect), manifeste d'heures idempotent,
  les heures en échec transitoire (503) sont toujours réessayées, seuls les vides > 48 h figent.
- `ci_tools/edge02_shadow.py` : pipeline complet ticks → barres M15 Mid → détection 24-B
  reproduite → score gelé M15_TIME_ONLY → règle 120 min vs référence 8 h. **Auto-test synthétique
  passé en CI** (détection, entrée ≤ 60 s, sortie deadline, déduplication).
- Workflow : job `edge02` (input dédié, limite des 25 respectée) + **cron quotidien 03:30 UTC**
  qui collectera chaque jour les heures postérieures au préenregistrement et commitera les données.
- `CONTRACT_120MIN_AUDIT.md` : audit des 10 points d'ambiguïté ; règle inchangée, clarifications
  strictes. Correction majeure : **le départ prospectif réel est l'horodatage public du
  préenregistrement, 2026-11-24T17:12:57Z** — les événements 2026-10-01 → 2026-11-24 sont exclus
  de toute évaluation de la règle.
- EXP-07 (`EXP07_*.csv`, EXPLORATORY_POST_HOC) : anatomie des pertes prolongées — classe
  dominante **dérive après MFE** (265/405 FP, −39,0 bp), MAE médian atteint à 225 min (après
  l'échéance de 120 min : cohérent avec le mécanisme visé) ; échecs rapides quasi indolores.
- Hypothèses H17–H20 consignées (`NEW_HYPOTHESES.md`), aucune promue sans préenregistrement.

## État SHADOW

Collecte armée, population encore vide (premières heures post-préenregistrement en attente de
publication Dukascopy ; le cron les récupérera). Aucun ordre, aucun capital, aucun événement
fabriqué. Seuil de description à 25 événements sélectionnés (fréquences/qualité seulement) ;
conclusion économique uniquement à la taille préenregistrée (≈ 350 événements / 140 grappes).

## Prochain travail (déjà engagé, sans arbitrage requis)

1. Laisser le cron accumuler ; vérifier la première journée complète collectée et lancer la
   détection d'événements sur données réelles postérieures au départ prospectif.
2. Préparer le connecteur MT5 démo (branchement interchangeable niveau A−) — seul point exigeant
   un jour l'identité du fondateur ; aucune donnée inventée.
3. Si la taxonomie EXP-07 se confirme sur les premiers événements prospectifs *descriptifs*,
   rédiger le préenregistrement séparé H18 (sortie sur retour sous l'entrée après MFE) — jamais
   de comparaison opportuniste avec la deadline sur la même population.
4. Réévaluer trimestres : fréquence réelle des événements, qualité des cotations aux échéances,
   taux de NON_EXECUTION/EXIT_NONEXECUTABLE.
