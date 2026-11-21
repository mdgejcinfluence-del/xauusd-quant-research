# CAMPAGNE 6 — PROPOSITION DE FAMILLE D'EXPLORATION (sans calcul)

**Statut : PROPOSITION SOUMISE AU FONDATEUR — aucun calcul lancé, aucune
définition gelée.** La Campagne 5 est définitivement close au descriptif
(validation fondateur chaînée seq224). La présente proposition ne
privilégie ni ANO-C5-001, ni ANO-C5-002, ni ANO-C5-003 : ces candidates
restent au catalogue commun, sans priorité, et toute confirmation
éventuelle exigerait un ordre distinct, un mécanisme explicatif et un
protocole indépendant.

## Famille proposée — F-G « Forme des trajectoires journalières »

### Pourquoi cette famille

Les campagnes précédentes ont cartographié les dépassements de niveaux
et leur réintégration (C0–C2), des candidates d'épisodes (C3), les états
relatifs de volatilité réalisée et leurs transitions (C4), puis les
ouvertures de session et les extrêmes datés de la veille (C5). Aucune
n'a décrit **la forme géométrique de la trajectoire intraday elle-même** :
dans quelle mesure une journée XAU/USD ressemble-t-elle à une tendance
(directionnelle, chemin quasi rectiligne), à un range (allers-retours
sans déplacement net) ou à un parcours mixte ? C'est une dimension
comportementale indépendante des niveaux franchis, des sessions et des
états de volatilité, mesurable en grandeurs sans dimension (donc
comparables entre ères malgré le changement d'échelle du prix de
l'or), et purement descriptive.

### Grandeurs candidates (à définir dans un dictionnaire, non gelées ici)

Par journée utilisable (barres M1, clôtures) :

- **Efficience de trajectoire** : |clôture − ouverture| / somme des
  |variations minute à minute| (ratio dans [0,1] ; proche de 1 =
  tendance rectiligne, proche de 0 = range sinueux).
- **Sinuosité** : longueur totale du chemin / amplitude journalière
  (haut − bas).
- **Part directionnelle** : fraction des minutes dont la variation va
  dans le sens du déplacement net de la journée.
- **Localisation du point médian de parcours** : heure à laquelle la
  moitié de la longueur de chemin journalière est accomplie.
- **Asymétrie de forme** : efficience de la première moitié de journée
  moins efficience de la seconde moitié.

### Comparaisons envisageables (ébauche, 5 par famille)

1. L'efficience médiane diffère entre journées de forte et de faible
   amplitude journalière (terciles descriptifs contemporains, jamais
   présentés comme un conditionnement temps réel).
2. L'efficience présente une persistance d'un jour au suivant
   (P(journée « tendance » après journée « tendance ») vs taux de base).
3. La forme diffère entre jours de semaine (lundi/vendredi vs milieu
   de semaine), à amplitude comparable publiée.
4. La localisation du point médian de parcours diffère selon le signe
   du déplacement net (journées haussières vs baissières).
5. L'asymétrie de forme (première vs seconde moitié de journée) diffère
   entre ères 2010–13 et 2017–20.

Chaque comparaison suivrait la discipline habituelle : dictionnaire
d'événements rédigé et soumis avant gel, protocole consolidé,
validation temporelle synthétique, éligibilité pré-déclarée (effectifs
et grappes minimaux), bootstrap par grappes-journées, correction BY par
famille de cinq, seuils de matérialité pré-enregistrés, publication des
négatifs, des non éligibles et des registres de censure, candidates
éventuelles au catalogue J1 sans promotion automatique.

### Garde-fous spécifiques à cette famille

- Grandeurs **sans dimension** uniquement (ratios), pour éviter toute
  confusion d'échelle entre ères ; aucune grandeur en prix brut.
- Aucun conditionnement par les terciles poolés rétrospectifs de F3
  (audit seq196/199) ; tout découpage par amplitude serait contemporain,
  descriptif, et étiqueté comme tel.
- Les journées à couverture partielle feraient l'objet de statuts de
  fenêtre publiés, comme en C5 (aucun observable silencieux sur fenêtre
  incomplète) ; la sensibilité de l'efficience aux minutes manquantes
  serait traitée dans le dictionnaire avant gel.
- Aucun lien imposé avec les candidates C5 : si une recoupement
  descriptif apparaissait, il serait publié comme tel, sans priorité.

## Familles alternatives (non retenues comme proposition principale)

- **F-H « Localisation temporelle des extrêmes du jour courant »** :
  distribution de l'heure du plus haut / plus bas du jour même.
  Cartographie simple et robuste, mais partiellement adjacente à F-F
  (C5) ; gardée en réserve.
- **F-I « Comportement autour des nombres ronds »** : fréquence et
  devenir des approches des multiples de 10/50 USD. Spécifique au
  XAU/USD, mais sensible au changement d'échelle du prix (1 100 → 2 600
  USD sur la décennie) et plus proche d'une hypothèse de micro-structure
  que d'une cartographie générale ; gardée en réserve.

## Ce que cette proposition ne demande pas

Aucune extraction, aucun calcul, aucun budget expérimental. Aucun
backtest stratégique ni `challenge_sim`. Holdout 2020–2026 scellé ;
T0 séparé et inactif ; FRED suspendue ; 36 cellules S12 gelées ; fiches
historiques inchangées.

## Décision demandée

1. Approbation du principe de la famille F-G (forme des trajectoires
   journalières) comme prochaine famille d'exploration — ou choix de
   F-H / F-I en réserve.
2. Autorisation de rédiger le dictionnaire d'événements et le protocole
   consolidé (préparation uniquement, sans calcul), soumis ensuite à
   validation avant tout gel.
