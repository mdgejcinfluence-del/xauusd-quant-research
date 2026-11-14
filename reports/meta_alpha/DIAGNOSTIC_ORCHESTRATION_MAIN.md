# Diagnostic — pourquoi le chaînage automatique inter-workflows est bloqué

## Fait vérifié (run P3-001, 13 nov. 2026)
À la fin du run P3-001 (succès), l'étape « déclencher l'orchestrateur » a exécuté
`gh workflow run orchestrateur.yml --ref arena/...` sans erreur visible (masquée par
`|| true`), mais **aucun run orchestrateur n'apparaît** dans l'historique GitHub.

## Cause précise (règles GitHub Actions)
1. `workflow_run` ne se déclenche que pour les workflows présents sur la **branche
   par défaut** du dépôt (ici `main`).
2. `workflow_dispatch` exige aussi que le fichier workflow existe sur la branche
   par défaut pour être « enregistré »; un dispatch vers un workflow qui n'existe
   que sur une branche secondaire échoue silencieusement/côté API.
3. Les push effectués avec le `GITHUB_TOKEN` ne déclenchent pas de nouveaux runs
   (sauf `workflow_dispatch`/`repository_dispatch`, eux-mêmes soumis au point 2).
Nos workflows vivent uniquement sur `arena/afe12737-xauusd-quant-research`
=> le chaînage inter-workflows est structurellement inactif. Les chaînages
INTRA-workflow (étapes, checkpoints, commits, reprise) fonctionnent et sont prouvés.

## Correction proposée (branche contrôlée, NON fusionnée)
- Fusionner vers `main` les seuls fichiers d'orchestration:
  `.github/workflows/p3-001.yml`, `p4-001.yml`, `orchestrateur.yml`,
  `phase2-autonomous.yml` (+ futurs workflows de phase), en conservant les
  déclencheurs `push` restreints à la branche de session et `workflow_dispatch`.
- Conséquences: (a) les workflows deviennent « enregistrés » -> dispatch et
  workflow_run fonctionnent; (b) tout push sur `main` touchant ces fichiers peut
  activer les déclencheurs `push` (ils filtrent `branches: [arena/...]`, donc
  aucun déclenchement accidentel depuis main); (c) `main` reçoit du code
  d'orchestration avant le code scientifique complet — risque faible, périmètre
  limité aux workflows; (d) action irréversible au sens « main avance » mais
  sans aucun effet sur le corpus ni sur les gates sensibles.
- Alternative sans fusion: un planificateur externe (cron GitHub sur main avec
  un workflow minimal qui lit les checkpoints et dispatche) — exige quand même
  un fichier sur main.

## Décision requise du propriétaire
Fusion ciblée des workflows vers `main`: OUI/NON. En attendant: mécanisme actuel
(checkpoints + lancement par session) — aucune perte, continuité manuelle assumée.
