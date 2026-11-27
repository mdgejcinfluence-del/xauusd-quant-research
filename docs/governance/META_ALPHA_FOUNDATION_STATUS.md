# META ALPHA — RAPPORT DE FONDATION (état réel au seq478)

## Où nous en sommes

Un cas de découverte complet (Colorful), un corpus de marché certifié
(685 M de ticks, 2010-2026), deux moteurs candidats gelés et rejetés
économiquement, et désormais une constitution qui recentre le projet
sur les modèles économiques.

## Découvert / cru / inconnu

- **Découvert (démontré)** : chez Colorful, un comportement
  d'accumulation d'inventaire avec récupération au voisinage du prix
  moyen (ME-001, mécanique et trajectoires) ; l'échec économique de
  nos implémentations V1/V2-F2 et sa cause principale (accumulation
  sélectionnée par l'adversité × coûts, sortie plafonnée, aucun stop).
- **Cru (fortement étayé, non validé)** : que ME-001 soit la source du
  revenu de Colorful ; ses statistiques publiques (+6,01 ¥/transaction
  affichés) sont UNVERIFIED et sa rentabilité réelle inconnue.
- **Inconnu** : le déclencheur exact de ses clôtures, sa formule de
  volume, son stop éventuel, son comportement vendeur, son risque de
  queue — et si ME-001, exploité avec nos propres règles, dégage un
  edge net positif dans notre corpus. C'est la question ouverte centrale.

## Reclassification des travaux antérieurs

- **Directement utiles** : DIRR-003 (trajectoires/récupération),
  AESR-002 (mécanisme), LMD-008 (cause des pertes), BACKTEST-2026-001
  (économie des candidats), EIDR-005/EMI-006 (frontière de la sortie).
- **Secondaires mais conservés** : RE-ENTRY-001→007 et FILTER-001/002
  (fidélité d'entrée), CDME-004, DEEP-REVERSE-001 (contexte).
- **Suffisants / clos** : reconstruction ponctuelle de l'EA Colorful —
  non identifiable sur 5 paniers, ne pas relancer sans observations
  nouvelles répondant à une question d'identification précise.

## Trois prochaines recherches prioritaires (autonomie, doctrine §13)

1. **Détection de la signature ME-001 dans le corpus** (VERT) :
   mesurer fréquence et rendement net disponible des fenêtres de
   récupération (retour au prix moyen après excursion bornée) sur
   2010-2026, avant tout moteur. Valeur : décide si ME-001 mérite un
   moteur propre. Coût faible, test discriminant direct.
2. **Gestion de l'échec de récupération** (VERT) : quantifier dans le
   corpus la queue des excursions qui ne reviennent jamais (durées,
   profondeurs, coûts de portage) — c'est le risque qui a tué V1/V2 et
   la variable qui déterminera toute règle de sortie propre.
3. **ME-002 (déséquilibre temporaire)** (VERT) : première détection de
   signature (écarts/résorption) comme source de rendement
   potentiellement indépendante de ME-001 pour le futur portefeuille.

Aucune V3 n'est créée ; aucun moteur gelé n'est modifié.
