# CAMPAGNE 3 — MÉTHODE ET MULTIPLICITÉ (GEL DE PRINCIPE)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** À figer par le
hash du dictionnaire avant extraction ; aucun paramètre modifié après
consultation des résultats.

## 1. Statistiques descriptives (le cœur de la campagne)

Pour chaque famille (IMP-M5, IMP-M15 séparée, CONS) et chaque instantané :
effectifs d'épisodes, journées distinctes, distributions (médiane, P25/P75,
P90) des variables d'instantané et des issues, taux de censure, taux de
chevauchement. Conditionnements publiés : session (Asie/Londres/New York/nuit),
ère (3), régime F3 (BAS/MOYEN/HAUT, NON_CLASSE publié à part) — en tableaux
prédéfinis, sans recherche de la « meilleure » cellule.

## 2. Famille fermée de comparaisons (détection descriptive)

Douze comparaisons maximum, énumérées avant calcul dans le document
d'exécution ; règle de lecture identique à la campagne 2 : bootstrap par
grappes-journées (2 000 répétitions, graine figée à l'exécution), correction
**BY** interne à la famille, seuil matériel (5 points pour une proportion,
ratio 1,15 pour une médiane), suffisance ≥ 200 épisodes et ≥ 100 journées par
bras, cohérence de signe dans ≥ 2 ères sur 3 quand la dimension n'est pas l'ère.
En deçà : queue de distribution ou non concluant, **conservés et publiés** dans
les résultats négatifs.

Exemples de comparaisons admissibles (à arrêter définitivement avant calcul) :
retracement atteint à +12 barres selon le tercile **causal** d'amplitude
initiale ; issues de consolidation selon la durée déjà écoulée à l'instantané ;
contrastes de session et de régime sur les variables d'instantané — jamais sur
des classeurs futurs.

## 3. Garde-fous

- Aucun test directionnel confirmatoire, aucun PnL, aucun coût appliqué à un
  gain (il n'y a pas de gain) ; le spread est un contexte.
- Les familles IMP-M15 et CONS ont leurs propres familles statistiques ; aucun
  pooling inter-familles pour « gagner » de la significativité.
- Les épisodes chevauchants sont signalés ; les analyses de sensibilité
  (exclusion des chevauchements) sont préenregistrées ou ne sont pas faites.
- Nouvelles fiches éventuelles : J1 candidates uniquement, au catalogue commun,
  avec la même structure de fiche que les campagnes 1–2 ; aucune ressemblance
  avec ANO-C1/C2 n'est requise ni favorisée.
- Arrêt propre : si l'extraction ne couvre pas le corpus (garde d'intégrité),
  la campagne se suspend et le documente au lieu de publier du partiel non
  étiqueté.
