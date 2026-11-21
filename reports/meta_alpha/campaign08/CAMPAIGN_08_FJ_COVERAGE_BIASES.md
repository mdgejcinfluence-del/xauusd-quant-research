# CAMPAGNE 8 — F-J : COUVERTURE, BIAIS, LIMITES, NOUVEAUTÉ

**Statut : PRÉPARATION — aucun calcul F-J.** Matrice issue des seuls
diagnostics déjà publiés (campagnes 4–7).

## 1. Matrice de couverture historique (livrable 9)

Corpus IS constitué : 282 partitions, 3 540 993 barres M1, 3 097
journées présentes (2010–2013 : 1 245 ; 2014–2016 : 932 ; 2017–2020 :
920, au sens des journées présentes C6). La période d'amorçage causal
(≥10 journées et ≥10 000 variations antérieures) rendra inéligibles
les toutes premières journées de 2010 — effectif exact inconnu avant
extraction et publié alors. Le nombre de chocs dépendra des seuils
causaux (quantile 99,5 % glissant proposé) : par construction, de
l'ordre de 0,5 % des minutes actives au-dessus du seuil relatif avant
plancher, soit un ordre de grandeur de quelques milliers d'épisodes
potentiels sur la décennie — estimation de conception, pas un
résultat. Tout bras sous les seuils d'éligibilité sera NON_ELIGIBLE.

## 2. Registre des biais et limites (livrable 10)

| # | Biais / limite | Traitement pré-déclaré |
|---|---|---|
| D1 | Seuil poolé rétrospectif présenté comme causal | **interdit** : fenêtre causale de 20 journées antérieures, fixe par journée ; référence poolée seulement en descriptif étiqueté |
| D2 | Amorçage : début de corpus sans historique | inéligibilité publiée (≥10 journées, ≥10 000 variations) ; aucun seuil rétroactif |
| D3 | Chocs groupés comptés comme indépendants | unité = épisode (regroupement 15 min) ; grappes-journées au bootstrap ; chocs intra-épisode hors tests |
| D4 | Sillages qui se chevauchent entre épisodes proches | épisodes d'une même journée dans la même grappe ; sillages postérieurs au dernier choc ; chevauchements publiés |
| D5 | Saut après trou pris pour un choc | aucune variation calculée à travers un trou ; reprises publiées comme discontinuités |
| D6 | « Extrême » relatif au calme ambiant (plancher) | plancher absolu 10 bp ; intensité ρ relative publiée avec les amplitudes en bp |
| D7 | Contexte de volatilité confondu avec l'effet du choc | tercile causal d'activité pré-événement en ventilation ; pseudo-événements appariés (J-05) sur session et activité pré-événement |
| D8 | Fenêtres de sillage incomplètes (trous, fin de journée) | statuts de censure publiés ; ordre indéterminé déclaré, jamais reconstruit |
| D9 | Interprétation prédictive ou « opportunité » d'un choc | interdite par la doctrine : anatomie descriptive ; toute candidate J1 l'énoncera |
| D10 | Dérive décennale de la microstructure (seuils, fréquences) | fréquences/intensités par ère publiées ; J-04 dédiée, sans ajustement après coup |
| D11 | Épisodes à signes mixtes | classe par premier choc, drapeau MIXTE publié, ventilation séparée |

## 3. Nouveauté par rapport aux campagnes précédentes (livrable 12)

F-J est la première famille dont l'événement est une **variation
statistiquement extrême datée causalement**, et non un niveau
(campagnes 0–2, 5, 7), un état agrégé (4), un épisode d'extension (3),
une ouverture (5) ou une forme de journée (6). Par rapport à F3/HAR et
F7 : aucun modèle, aucune prévision, aucune classification — le seuil
causal est un instrument de datation, pas un régime exploitable, et
l'étude porte sur l'après-événement descriptif (sillage), dimension
absente de toutes les campagnes closes. Le risque de glisser vers une
« étude des régimes de volatilité » est traité par D1/D6/D9 et par le
choix d'unités événementielles (épisodes) plutôt que d'états.

## 4. Décision demandée

Validation de l'orientation (seuil causal 99,5 % sur 20 journées,
plancher 10 bp, regroupement 15 minutes, famille J-01..J-05 avec
session en ventilation fermée), puis autorisation du protocole
consolidé — préparation uniquement, calculs interdits jusqu'à l'ordre
d'exécution.
