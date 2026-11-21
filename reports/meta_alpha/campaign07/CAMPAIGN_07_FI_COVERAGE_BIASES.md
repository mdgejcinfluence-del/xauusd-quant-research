# CAMPAGNE 7 — F-I : COUVERTURE HISTORIQUE, BIAIS ET LIMITES

**Statut : PRÉPARATION — aucun calcul F-I.** La matrice réutilise
uniquement les diagnostics déjà publiés des campagnes précédentes.

## 1. Matrice de couverture historique (livrable 7)

Corpus constitué : 282 partitions mensuelles vérifiées (janvier 2010 –
janvier 2020 pour l'IS), 3 540 993 barres M1, 3 097 journées présentes,
2 572 journées utilisables au sens C4/C5. Fourchettes de prix
historiques approximatives (contexte public, à confirmer mécaniquement
à l'extraction comme simple diagnostic, jamais comme résultat F-I) :

| Ère | Prix approx. (USD) | Pas de 50 USD en bp (approx.) | Conséquence de conception |
|---|---|---|---|
| 2010–2013 | ~1 000–1 900 (pic 2011) | ~260–500 | grille absolue « lâche » en relatif |
| 2014–2016 | ~1 050–1 400 | ~360–480 | régime de prix bas |
| 2017–2020 (IS) | ~1 150–1 650 | ~300–430 | grille intermédiaire |

Le holdout 2020–2026 (prix au-delà de 2 000 USD) reste scellé et hors
matrice. Les effectifs d'épisodes par grille et par ère sont inconnus
à ce stade (calculs interdits) ; toute grille ou ère sous les seuils
d'éligibilité sera publiée NON_ELIGIBLE, sans fusion après coup.

## 2. Registre des biais et limites (livrable 8)

| # | Biais / limite | Traitement pré-déclaré |
|---|---|---|
| C1 | Choix des niveaux après coup (« data snooping » de grille) | grilles fixées a priori (50/10 USD, anneaux disjoints), placebo décalé d'un demi-pas, famille fermée de cinq |
| C2 | Effet général de parcours confondu avec la rondité | référence placebo identique en tout point ; seul l'écart rond − placebo est interprété |
| C3 | Volatilité/session/amplitude confondues avec la rondité | ventilations publiées par session et tercile d'amplitude contemporain ; règle de déclassement à fermer au consolidé |
| C4 | Échelle absolue vs relative : 50 USD ne vaut pas les mêmes bp selon l'ère | double publication USD/bp ; I-05 teste l'évolution de l'écart ; aucune redéfinition de grille en cours de campagne |
| C5 | Touche confondue avec franchissement | franchissement strict par clôture au-delà ; touches publiées à part (convention C5) |
| C6 | Ordre temporel intra-barre inconnu en M1 | franchissement par saut et épisodes SIMULTANÉS classés, exclus du primaire, publiés |
| C7 | Niveaux multiples traversés en une journée agitée | épisodes indépendants par niveau mais grappes-journées au bootstrap ; chevauchements d'épisodes d'un même niveau interdits par la fenêtre de washout |
| C8 | Suivi +60 min incomplet (trous, fin de journée) | censures publiées, aucun observable silencieux sur fenêtre incomplète (statuts hérités C5/C6) |
| C9 | Prix nominal qui traverse les grilles différemment (dérive haussière décennale) | approches par les deux côtés publiées séparément en ventilation ; côté d'approche figé à l'ouverture de l'épisode |
| C10 | Effet « chiffre rond » indistinguable d'un effet de liquidité ordinaire aux prix entiers | limite assumée : la famille décrit un comportement, elle ne démontre aucun mécanisme psychologique ; toute candidate J1 l'énoncera ainsi |

## 3. Comparaison explicite avec les campagnes précédentes (livrable 10)

Reprise et extension de l'audit du blueprint : les campagnes 0–2 ont
étudié des niveaux **endogènes** (extrêmes formés par le prix) sans
référence placebo ; C5 F-F a daté les atteintes de ces mêmes extrêmes
de la veille. F-I change les trois dimensions à la fois : niveaux
**exogènes** (grille arithmétique), question de **contact** (approche,
touche, rejet, maintien) plutôt que de dépassement-réintégration, et
**placebo décalé** intégré au dessein. F-G (Campagne 6) ne contient ni
niveau ni événement de contact. La famille ne peut donc pas
« reproduire simplement » les anciennes analyses : si l'écart
rond − placebo est nul partout, la conclusion sera précisément que
les nombres ronds ne forment pas une famille distincte dans ce corpus
— résultat négatif publiable et utile à la cartographie.

## 4. Décision demandée

Validation de l'orientation (grilles 50/10 et anneaux, placebo
décalé, famille de cinq I-01..I-05), puis autorisation de rédiger le
protocole consolidé (constantes à geler : bande d'approche 25 bp,
washout 60 min, seuil de rejet 25 bp, suivi 60 min, règle de
déclassement de composition) — préparation uniquement, calculs
toujours interdits jusqu'à l'ordre d'exécution.
