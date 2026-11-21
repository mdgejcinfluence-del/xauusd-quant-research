# CAMPAGNE 2.4 — PROTOCOLE DE CONFIRMATION J2 (PROPOSITION, NON EXÉCUTÉ)

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DOCUMENT DE PROTOCOLE — AUCUN CALCUL EXÉCUTÉ DANS CETTE CAMPAGNE.** Aucune
promotion J2 n'est prononcée ni préparée comme acquise ; ce document définit les
conditions auxquelles une confirmation *pourrait* être demandée, et il attend une
autorisation distincte du propriétaire. Budgets expérimentaux intacts (tick
148/150 · panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 · P9 10/12), holdout
2020–2026 non accédé, FRED suspendue, anciennes fiches ANO inchangées.

## 1. Statut de la découverte à confirmer

La relation entre la profondeur atteinte à T0 (barre de franchissement d'un niveau
Asie/veille, à partir de 08:00 UTC) et la réintégration ultérieure sous 60 minutes
est classée **J1 — association comportementale candidate à confirmation
prédictive**. Valeurs descriptives sur le corpus consulté (réplication décennale
seq 179) : contraste entre terciles extrêmes de profondeur atteinte à T0 de
+13,3 points [12,2 ; 14,2], stable en valeur centrale sur les trois ères
(+12,4 / +13,7 / +15,6). Ces chiffres décrivent le passé consulté ; ils ne
constituent ni une probabilité exploitable, ni une rentabilité, ni un échantillon
de confirmation.

## 2. Hypothèse principale (unique, prédéfinie)

**H1** : sur un échantillon chronologiquement postérieur au gel du présent
protocole et jamais consulté pour la découverte, les dépassements dont la
profondeur atteinte à T0 appartient au tercile supérieur des seuils causaux (§4)
présentent un taux de réintégration sous 60 minutes inférieur à ceux du tercile
inférieur, avec un contraste (BAS − HAUT) **≥ +5 points** (borne de matérialité,
moitié basse de l'intervalle descriptif) et un intervalle de confiance à 95 %
excluant zéro.

- **Variable observable à T0** : `prof_max_jusqua_bp` à l'instantané 0 —
  excursion maximale au-delà du niveau sur la seule barre de franchissement,
  connue à la clôture de cette barre. (Variable secondaire préenregistrée, sans
  rang de décision : profondeur initiale de clôture.)
- **Issue future** : réintégration = première clôture M1 revenue du bon côté du
  niveau, strictement après T0, sous 60 minutes (définition du dictionnaire gelé
  seq 157, inchangée).
- **Horizons** : principal 60 minutes ; secondaires descriptifs 15 et 30 minutes
  (positions par rapport au niveau), sans valeur de décision.
- **Censure** : absence de réintégration à T0+60 = censuré à droite, compté comme
  non-réintégration dans le taux principal (convention déjà utilisée), avec
  analyse de sensibilité préenregistrée excluant les épisodes tronqués par la fin
  de journée (< 60 barres disponibles).
- **Unité d'indépendance** : grappe jour×niveau ; intervalles par bootstrap par
  grappes (2 000 répétitions, graine à figer dans l'ordre d'exécution).

## 3. Seuils — exclusivement à partir du passé

Les seuils historiques rétrospectifs (fragment : 1,4853/3,4476 bp ; décennie :
1,2499/2,9694 bp) sont **conservés pour les descriptions historiques et
interdits** pour la confirmation. Procédure proposée, à figer dans l'ordre
d'exécution avant tout accès aux données de confirmation :

- **Expanding window** : seuils = quantiles 1/3 et 2/3 de la profondeur atteinte
  à T0 calculés sur tous les épisodes strictement antérieurs à la date de
  l'événement classé, avec une période d'amorçage (burn-in) dont la durée est
  fixée ex ante et pendant laquelle aucun épisode n'est classé.
- Mise à jour des seuils à fréquence fixe (proposition : mensuelle, premier jour
  ouvré), figée entre deux mises à jour ; journal des valeurs successives
  publié avec les résultats.
- Alternative rolling window (fenêtre glissante de longueur fixe) admise
  seulement si elle est choisie **avant** l'exécution ; un seul des deux
  schémas aura valeur de décision, l'autre relèvera de la sensibilité.

## 4. Échantillon de confirmation — existe-t-il ?

**Non, pas dans le périmètre actuellement autorisé.** Le corpus IS 2010–2020 a
été intégralement consulté pour la découverte et la réplication descriptive
(campagnes 0 à 2.3) : le découper à nouveau, même chronologiquement, ne créerait
pas un échantillon indépendant — toute statistique calculée dessus resterait une
re-description du matériau de découverte. Le seul matériau temporellement
disjoint existant (données postérieures à 2020) appartient à des périmètres
scellés dont l'accès exige une autorisation distincte, non accordée par le
présent document. Il reste deux voies, détaillées dans
`CAMPAIGN_2_4_TEMPORAL_SPLIT_PLAN.md` : (a) **confirmation prospective** sur des
données générées après le gel du protocole, collectées au fil de l'eau, sans
aucune lecture avant l'atteinte de l'effectif requis ; (b) lecture unique d'une
réserve scellée, uniquement sur autorisation écrite distincte précisant
périmètre, date de gel des données et compteur d'essais. **Aucune période
disponible n'est inventée** : à la date du présent protocole, la voie (a) démarre
avec zéro épisode.

## 5. Hétérogénéité entre époques (méthode proposée)

Ne jamais conclure à la stabilité sur le seul recouvrement des intervalles. Sur
l'échantillon de confirmation, découpé en blocs temporels prédéfinis :

1. **Contraste** : interaction ère×groupe testée par bootstrap par grappes de la
   différence des contrastes ; synthèse méta-analytique des contrastes par bloc
   (Q de Cochran, I²) à titre descriptif structuré.
2. **Taux de base** : taux de réintégration global par bloc, publié séparément du
   contraste (une dérive du taux de base ne doit pas être lue comme une dérive
   de l'association).
3. **Seuils** : trajectoire des seuils causaux (§3) publiée bloc par bloc ; une
   dérive des seuils signale un changement d'échelle du marché, pas
   nécessairement de l'association.
4. **Distribution des événements** : quantiles de la profondeur atteinte et de la
   profondeur initiale par bloc, comparés graphiquement et par écarts de
   quantiles (pas de test de distribution à valeur de décision).

## 6. Critère de confirmation ou de rejet (à figer dans l'ordre d'exécution)

- **Confirmation (passage en J2 discutable, décision propriétaire séparée)** :
  contraste principal ≥ +5 points, IC 95 % par bootstrap par grappes excluant
  zéro, effectif et grappes au moins égaux aux requis du document de puissance,
  signe du contraste homogène dans au moins la moitié des blocs temporels
  prédéfinis.
- **Rejet** : borne supérieure de l'IC < +5 points à effectif requis atteint, ou
  inversion de signe significative.
- **Non concluant** : tout autre cas, notamment effectif non atteint — aucune
  lecture anticipée des résultats intermédiaires (pas d'arrêts opportunistes :
  l'effectif cible et la règle d'arrêt sont fixés avant la collecte).

Aucun de ces critères n'attribue de direction de trading, de point d'entrée ou de
rentabilité : même confirmée, l'association resterait un fait comportemental
(J2) dont l'exploitabilité (J3) exigerait une preuve séparée de capturabilité
nette de coûts, hors du présent périmètre.

## 7. Ce que ce document n'autorise pas

Aucun calcul sur de nouvelles données, aucun backtest, aucun `challenge_sim`,
aucune optimisation, aucune lecture du holdout 2020–2026, aucune consommation de
budget expérimental, aucune modification des fiches ANO existantes ni des seuils
historiques. L'exécution éventuelle fera l'objet d'un ordre distinct, d'un gel
chaîné de ses paramètres restants (graine, burn-in, schéma de seuils, blocs), et
d'un compteur d'essais propre.

**STATUT : PROTOCOLE DE CONFIRMATION PROPOSÉ — VALIDATION DU PROPRIÉTAIRE EN
ATTENTE.**

*Compagnons : `CAMPAIGN_2_4_TEMPORAL_SPLIT_PLAN.md`,
`CAMPAIGN_2_4_POWER_REQUIREMENTS.md`, `CAMPAIGN_2_4_ANOMALY_STATUS.md`.*
