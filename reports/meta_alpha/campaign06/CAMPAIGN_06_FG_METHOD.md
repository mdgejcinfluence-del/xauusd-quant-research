# CAMPAGNE 6 — MÉTHODE F-G, COUVERTURE, BIAIS (préparation, pré-gel)

**Statut : PRÉPARATION — aucun calcul effectué.**

## 1. Méthode statistique (livrable 7)

- **Unités et grappes** : unité = journée utilisable ; bootstrap par
  grappes-journées pour C6-02..05 ; pour C6-01 (paires de journées
  successives, recouvrement structurel), grappe proposée = semaine
  civile afin de ne pas traiter des paires partageant un jour comme
  indépendantes (à confirmer au gel).
- **Bootstrap** : 2 000 réplicats, rééchantillonnage des grappes,
  graine fixée au protocole (convention des campagnes précédentes :
  graine datée, publiée). Effets : différences de médianes (ER, τ),
  intervalles percentile 95 %, p bootstrap bilatérales.
- **Multiplicité** : correction **Benjamini–Yekutieli séparée pour la
  famille F-G de cinq** (m = 5, H₅ = 2,2833), appliquée aux p-values
  calculables ; toute comparaison structurellement non testable serait
  publiée avec q = NaN, sans imputation, et une sensibilité au
  décompte de famille pourrait être exigée au gel (leçon seq223).
- **Éligibilité pré-déclarée** : ≥ 200 journées et ≥ 100 grappes par
  bras (convention campagnes 4–5) ; en dessous, la comparaison est
  déclarée NON ÉLIGIBLE avec effectifs publiés, sans assouplissement.
- **Lectures fermées** : CANDIDATE_J1 (q BY < 0,05 **et** matérialité
  atteinte) ; SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL ;
  NÉGATIF ; NON_ÉLIGIBLE ; STRUCTURELLEMENT_NON_ÉVALUABLE si le critère
  d'une variable ne peut être satisfait par aucune observation.
  Publication systématique : effectifs initiaux/éligibles/censurés,
  couvertures, effets, IC, p brutes, q BY, matérialités, et toutes les
  lectures, y compris négatives.

## 2. Matrice de couverture historique (livrable 9)

Corpus déjà constitué (campagnes précédentes, aucune nouvelle
extraction pour cette préparation) : 282 partitions mensuelles
Kaggle vérifiées, janvier 2010 – décembre 2020, 3 540 993 barres M1,
3 097 journées présentes, 2 572 journées utilisables pour C4/C5.

| Ère (convention campagnes précédentes) | Journées à usage F-F OK publiées en C5 | Rôle en F-G |
|---|---|---|
| 2010–2013 | 1 034 | bras A de C6-05 |
| 2014–2016 | 774 | publiée, hors contraste C6-05 |
| 2017–2020 | 763 | bras B de C6-05 |

La population F-G définitive différera par ses propres règles de
couverture (dictionnaire §5 : trou maximal et taux minimal propres aux
grandeurs de forme) ; les effectifs éligibles par comparaison seront
recalculés **uniquement après gel**, et toute ère ou classe tombant
sous les seuils d'éligibilité sera publiée comme telle. Le holdout
2020–2026 reste scellé et hors matrice.

## 3. Registre des biais, dépendances et limites de mesure (livrable 10)

| # | Biais / dépendance | Traitement pré-déclaré |
|---|---|---|
| B1 | Effet de fréquence (« règle ») : L dépend de la granularité d'observation | convention unique clôtures M1 ; aucune comparaison inter-fréquences ; limite publiée |
| B2 | Trous de cotation : L sous-estimé, ER gonflé après fusion de mouvements | censure des journées à trou > seuil (à geler), sauts de reprise marqués et comptés, statuts publiés |
| B3 | Halt quotidien du marché : la journée de cotation n'a pas 1 440 minutes actives | couverture mesurée en minutes observées/attendues du corpus, jamais d'exigence 1 440/1 440 (leçon C5-10) |
| B4 | Redondances algébriques ER ↔ S ↔ |Δ|/A ; PD ↔ signe de Δ | une variable primaire par comparaison ; secondaires étiquetés non indépendants (dictionnaire §3) |
| B5 | Déplacement net faible : signe et PD instables | classe DÉPLACEMENT FAIBLE exclue des comparaisons par signe, effectifs publiés |
| B6 | Persistance de volatilité confondue avec persistance de forme (C6-01) | ventilation par amplitude du jour j ; lecture limitée à l'association |
| B7 | Terciles d'amplitude contemporains (C6-02) rétrospectifs | étiquetage rétrospectif explicite ; audit mécanique dédié ; aucun usage « à T0 » |
| B8 | Évolution de la microstructure et de la couverture sur dix ans (C6-05) | statistiques de couverture publiées par ère ; aucune correction a posteriori |
| B9 | Distribution bornée et possiblement bimodale d'ER | médianes + bootstrap percentile ; aucune hypothèse gaussienne |
| B10 | Grandeurs de journée complète rétrospectives | étiquette « disponible à la clôture » ; aucune lecture intraday ni temps réel |
| B11 | Classes directionnelle/oscillante aux constantes arbitraires (C6-01) | constantes fixées a priori au gel, jamais ajustées ; analyses continues primaires, classes secondaires |

## 4. Suspension et échec

Tout échec d'extraction, toute incohérence de chaîne ou de couverture
suspend le calcul concerné ; les comparaisons non exécutées restent
consignées comme non exécutées (doctrine campagnes précédentes). Aucun
budget expérimental n'est consommé par la préparation ni, sauf ordre
contraire au gel, par l'exécution descriptive.
