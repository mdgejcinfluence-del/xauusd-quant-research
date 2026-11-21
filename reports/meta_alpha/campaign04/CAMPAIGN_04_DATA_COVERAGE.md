# CAMPAGNE 4 — COUVERTURE DES DONNÉES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Source | Périmètre | Usage campagne 4 | État |
|---|---|---|---|
| Corpus tick IS (282 partitions, Kaggle `shalom5123`, accès HTTPS direct) | 2010-01-04 → 2019-12-16 ; 3 540 993 barres M1 reconstituées (campagnes 2.3/3) | RV journalière et de session, rendements M1, extrêmes, asymétries | Accessible ; intégrité vérifiée (282/282, seq 179 et seq 191) |
| F3 gelé (`reports/meta_alpha/phase2/f3_har/F3_DAILY_PRED.csv`) | Prédiction HAR journalière, 2 572 jours (2 071 évalués) | État-passé de référence (terciles gelés seq 75), matrice de discordance | Commité, consulté, **non modifié** |
| Bruts campagnes 1–3 (épisodes gelés) | Même corpus IS | Fréquences conditionnelles d'événements déjà catalogués (impulsions IMP-M5 seq 191, dépassements seq 179) selon les états | Commités, consultés ; définitions historiques inchangées |
| Flux prospectif de confirmation T0 | Postérieur au gel 2.4 | **Interdit à cette campagne** (chantier A réservé) | Non collecté, non utilisé |
| Holdout / périmètres post-2020 | Scellés | Aucun | Non accédé |
| FRED / exogène (calendriers macro) | Suspendu | Aucun : les « événements structurels » traités sont internes (sessions, frontières de journées, événements catalogués) | Non utilisé |

## Exigences d'exécution (rappel)

- Garde d'intégrité : partitions chargées = attendues (282) ; journées
  recoupées avec les comptes des campagnes précédentes (2 515 journées
  pleines historiques ; 3 097 dates UTC présentes au sens de la campagne 3)
  et tout écart expliqué avant synthèse.
- Amorçages causaux : les états exigent 40 à 60 journées d'historique (et
  20 000 barres M1 pour les seuils d'extrêmes) ; les zones sans état
  attribuable sont comptées et publiées par famille, jamais comblées.
- Validation temporelle avant calcul : tests sur données synthétiques
  (patron campagne 3) — seuils excluant le jour courant, confirmation non
  antidatée, fenêtres de conséquences strictement postérieures à la date
  de confirmation.
- Reproductibilité : moteur versionné, workflow séquentiel à commit unique,
  bruts gzip (correctif campagne 3), journaux CI commités y compris en cas
  d'échec ; en cas d'échec de récupération, suspension documentée plutôt
  que publication partielle non étiquetée.
- Aucune donnée fabriquée ou imputée ; les journées/sessions sous les
  minimums de barres sont exclues des mesures concernées et comptées.
