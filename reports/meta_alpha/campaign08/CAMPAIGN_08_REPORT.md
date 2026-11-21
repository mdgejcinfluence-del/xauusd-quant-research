# CAMPAGNE 8 — RAPPORT SCIENTIFIQUE F-J « CHOCS MINUTE EXTRÊMES ET LEUR SILLAGE »

**Protocole gelé V2 (seq266). Exécution autorisée par le propriétaire
(seq267), confirmation de gel seq268. Run CI 44911859012 vert du premier
coup.** Corpus IS XAU/USD uniquement ; holdout scellé ; aucun backtest ;
aucune promotion automatique.

## 1. Exécution et couverture

Extraction : 282/282 partitions, 3 540 993 barres M1, 3 097 journées
présentes. Détection causale : **3 087 journées éligibles, 10 journées
inéligibles** (amorçage : moins de 10 journées antérieures ou de
10 000 variations — publiées, aucun seuil rétroactif). Seuil journalier
T_D : min 10,0 bp (plancher actif), médiane 10,04 bp, max 27,68 bp.

**14 735 chocs** détectés (7 337 positifs, 7 398 négatifs), regroupés en
**7 905 épisodes** : POSITIFS 3 344, NÉGATIFS 3 239, **MIXTES 1 322**
(publiés séparément, exclus des comparaisons). Statuts : **7 833 CLOS,
72 CLÔTURE_INDÉTERMINÉE** (silence de 15 minutes non intégralement
observé — censurés, aucune disponibilité fabriquée, exclus des
comparaisons). Parmi les épisodes clos non mixtes, 43 CENSURE_FENÊTRE à
+60 minutes. Épisodes isolés 5 423, regroupés 2 482.

## 2. Résultats FJ-01 à FJ-05 (R₆₀, différence de médianes, matérialité 10 bp, BY m = 5 fixe)

| ID | Effet (bp) | IC 95 % | p | q BY | n (A/B) | Grappes (A/B) | Lecture |
|---|---|---|---|---|---|---|---|
| FJ-01 signe (isolés + vs −) | +0,17 | [−0,81 ; +1,61] | 0,641 | 1,000 | 2 736 / 2 596 | 1 517 / 1 499 | **NÉGATIF** |
| FJ-02 regroupés vs isolés | −3,74 | [−5,38 ; −1,78] | 0,0005 | 0,0057 | 1 156 / 5 332 | 852 / 2 075 | **SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL** |
| FJ-03 majeurs vs modérés (isolés) | −2,52 | [−4,23 ; +0,16] | 0,082 | 0,312 | 304 / 5 028 | 277 / 2 030 | **NÉGATIF** |
| FJ-04 2010–13 vs 2017–20 (isolés) | −1,47 | [−3,24 ; −0,17] | 0,029 | 0,166 | 2 525 / 1 061 | 876 / 528 | **NÉGATIF** |
| FJ-05 isolés appariés vs pseudo-événements | −4,28 | [−11,10 ; +13,95] | 0,259 | 0,739 | 5 126 / 5 126 | 12 / 12 | **NON ÉVALUABLE** |

**Aucune candidate J1. Catalogue ANO-C8 vide.**

## 3. Lectures

- **FJ-01 NÉGATIF** : à une heure, le sillage médian des chocs isolés
  haussiers (−4,50 bp orientés) et baissiers (−4,67 bp) ne diffère pas.
  Le retour partiel après un choc isolé est symétrique en signe.
- **FJ-02 SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL** : après un épisode
  regroupé, la continuation signée médiane est plus négative de 3,74 bp
  qu'après un choc isolé (regroupés −8,34 bp contre isolés −4,60 bp) :
  le retracement post-épisode est plus prononcé, mais l'écart est très
  inférieur au seuil matériel de 10 bp. Aucune candidature.
- **FJ-03 NÉGATIF** : l'intensité primaire I_ép (majeurs −7,04 bp,
  modérés −4,52 bp) ne produit pas de différence établie après
  correction BY.
- **FJ-04 NÉGATIF** : la différence brute entre ères (−5,06 bp en
  2010–13, −3,59 bp en 2017–20) ne survit pas à la correction BY.
- **FJ-05 NON ÉVALUABLE** : l'appariement a réussi (5 191 paires, aucun
  épisode non apparié, 5 126 paires aux deux R₆₀ définis), mais le
  graphe de dépendance gelé — journées communes, sillages chevauchants,
  arêtes d'appariement — fusionne la quasi-totalité des unités en
  **12 grappes** (plus grande grappe : 99,8 % des unités) : le seuil
  gelé de 100 grappes par bras n'est pas atteint et GRAPPE_DOMINANTE est
  active, avec COMPOSITION_SENSIBLE (parts d'ère : épisodes
  47/33/20 % contre pseudo-événements 66/22/12 %). Conformément au
  protocole, la comparaison est publiée comme **non évaluable** : les
  chiffres descriptifs (épisodes appariés ≈ −4,3 bp sous les
  pseudo-événements en médiane brute) ne fondent aucune lecture.

## 4. Faits descriptifs (publiés sans test)

Médiane de R₆₀ des épisodes clos non mixtes : **−5,07 bp** (retracement
médian d'environ un tiers de l'amplitude maximale : part retracée
médiane 0,335 ; retournement complet dans 1 969 cas sur 6 488).
Nouveau choc dans l'heure : 29,6 % des épisodes contre 10,5 % du bassin
de pseudo-événements (descriptif). Stabilisation médiane post/pré :
1,076. Épisodes mixtes clos : R₆₀ médian −0,53 bp (n = 1 302).
Ventilation par session (épisodes clos non mixtes, médianes R₆₀) :
S1 −3,75 (n 709), S2 −5,33 (1 754), S3 −5,36 (3 825), S4 −4,67 (200) —
publiée sans test, comme gelé.

## 5. Multiplicité et contrôles

Famille fermée de cinq, **BY à m = 5 fixe** (H₅ = 2,283333) appliquée
aux cinq p brutes [0,641 ; 0,0005 ; 0,082 ; 0,029 ; 0,259] ; q obtenues
[1,000 ; 0,0057 ; 0,312 ; 0,166 ; 0,739]. Bootstrap 2 000 réplicats par
composantes connexes, graine 20261113. Aucune p-value créée par les
contrôles de composition ou de grappe. GRAPPE_DOMINANTE inactive sur
FJ-01…FJ-04 (plus grandes parts 0,3–1,0 %), active sur FJ-05.

## 6. Conclusion

L'anatomie qui émerge est celle d'un **retracement partiel symétrique**
dans l'heure suivant un choc minute extrême daté causalement, un peu
plus marqué après les épisodes regroupés, sans différence établie selon
le signe, l'intensité ou l'ère, et sans que la référence
pseudo-événements — non évaluable en l'état du graphe gelé — permette
de conclure au-delà des épisodes eux-mêmes. Aucune fiche ANO n'est
ouverte ; les campagnes F-G et F-I restent closes ; aucune fiche
historique n'est modifiée.
