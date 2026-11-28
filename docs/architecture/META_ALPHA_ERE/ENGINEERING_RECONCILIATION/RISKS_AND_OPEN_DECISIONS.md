# RÉCONCILIATION — RISQUES ET DÉCISIONS OUVERTES

## Faits vérifiés / propositions / non-vérifiés (rappel)

- **[DÉPÔT]** : HEAD, registre 498 entrées, CI Actions comme calcul,
  Kaggle = stockage migré et vérifié, moteurs gelés intacts, aucun des
  neuf moteurs n'existe comme logiciel.
- **[EXT]** : tout le dossier externe est une conception non déployée ;
  ses tests sont synthétiques ; ses limites Kaggle sont documentaires.
- **[NV]** : quotas et matériel réels de notre compte Kaggle en mode
  kernels ; existence d'une quelconque API ARENA (réponse : aucune
  connue) ; coûts d'un éventuel stockage objet externe.

## Incompatibilités découvertes (consolidées)

1. Plan de calcul : Kaggle-kernels [EXT] vs CI Actions prouvée [DÉPÔT].
2. Échelle de preuve : E5 externe plus faible que N7 interne.
3. Environnement : Python 3.12/wheelhouse [EXT] vs runner CI/venv réel.
4. Orchestration : « adaptateur ARENA » [EXT] sans substrat réel.
5. Le dossier externe ignore nos actifs de gouvernance (registre
   chaîné, Drift Guard, checkpoints) — réconciliés ici sans rien
   remplacer.

## Risques non résolus

- **R1.** La taxonomie N0–N7 et les corrections d'ERE-REVIEW-002
  attendent toujours la validation du fondateur ; construire dessus
  avant serait bâtir sur du non-décidé.
- **R2.** Dépendance Drive comme source des partitions (la migration
  Kaggle la réduit, sans l'achever comme source de vérité).
- **R3.** Pas de lock d'environnement : la reproductibilité repose sur
  la stabilité des runners — risque réel, traité à l'étape 4.
- **R4.** Un seul agent supervise : la reprise dépend de la qualité
  des objets committés (`DossierState` reste à créer).
- **R5.** Phénomènes de marché périssables : ME-001 attend son épreuve
  prospective ; aucun calendrier ne peut être promis.

## Décisions demandées au fondateur

1. Approuver le verdict d'architecture (monolithe modulaire, calcul CI,
   Kaggle = stockage, kernels en option à qualifier).
2. Trancher les décisions encore ouvertes d'ERE-REVIEW-002 (taxonomie
   N0–N7 officielle, corrections 1–7, séparation I-A/I-B, Visuel 1
   proposé).
3. Autoriser ou non une mission de qualification Kaggle-kernels sur
   synthétique (aucun coût engagé ici).
4. Choisir le prochain dossier trader ou donner la priorité aux
   étapes socles 1–2 de la feuille de route.
5. Confirmer qu'aucune implémentation ne commence avant ces réponses.

**Critère d'arrêt de la mission : atteint.** Dossier complet, vérifiable,
sans implémentation. Verdict : `READY_FOR_FOUNDER_REVIEW`.
