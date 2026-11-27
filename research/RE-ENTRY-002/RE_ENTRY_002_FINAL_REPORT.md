# RE-ENTRY-002 — ÉLARGISSEMENT DE L'ÉCHANTILLON « COLORFUL DROPS » (99001292)

## 1. Ce qui a été obtenu de manière autonome (et ce qui ne l'est pas)
La page publique HFM `strategy-view?account=99001292` est accessible sans compte et affiche les
statistiques du fournisseur ainsi que ses **6 dernières transactions réelles** (« Trading
Activity »). Limites établies par test : le paramètre `page=2` ne change rien (aucune pagination
publique trouvée) ; depuis les runners CI, HFM répond **403** (protection anti-robot, journal
`PROBE_LOG.txt`) — la consultation passe par une lecture web ordinaire, pas par un contournement.
L'historique complet (49 595 transactions clôturées affichées) **n'est pas accessible** par les
mécanismes publics : seuls des instantanés successifs des dernières lignes peuvent l'échantillonner.
Chaque instantané est archivé avec provenance (`PUBLIC_PAGE_SNAPSHOT_2026-11-27.csv`).

## 2. Base de paniers — 5 paniers réels, 12 transactions (ne pas confondre)
| Panier | Date (affichée) | Positions | Volumes | Durée | Résultat affiché |
|---|---|---|---|---|---|
| A | 2026-11-26 | 3 Buy | 0,01 / 0,01 / 0,02 | 19 min 12 s | +11 ¥ |
| B | 2026-11-26 | 3 Buy | 0,01 / 0,01 / 0,02 | 11 min 55 s | +13 ¥ |
| C | 2026-11-27 | 3 Buy | 0,01 / 0,01 / **0,03** | 10 min 48 s | **−6 ¥ (perdant)** |
| D | 2026-11-27 | 1 Buy | 0,01 | **17 s** | +1 ¥ |
| E | 2026-11-27 | 2 Buy | 0,01 / 0,01 | 1 min 27 s | +3 ¥ |
Paniers entièrement reconstructibles sur cotations : A et B (RE-ENTRY-001, Dukascopy comparatif).
C, D, E : transactions réelles certaines (page publique), mais reconstruction prix
**NON DÉTERMINABLE à cette heure** — les ticks Dukascopy du 2026-11-27 08:00 UTC ne sont pas
encore publiés par le flux (publication par lots constatée ; heures présentes : 0-7 et 9).
Aucun prix n'a été inventé pour compléter.

## 3. Ce que le nouvel échantillon change
- **Premier cas perdant observé (C)** : 3 positions fermées groupées pour −4/−3/+1 ¥, net −6 ¥.
  L'existence de clôtures groupées perdantes contredit l'idée d'un take-profit de panier
  systématiquement gagnant : le panier peut aussi être coupé en perte (ou arriver à échéance
  d'une autre règle). La règle « retour au-dessus du prix moyen » reste étayée pour A/B, mais
  n'est **pas suffisante** comme explication universelle — statut ramené à FORTEMENT ÉTAYÉE
  (condition fréquente, pas démontrée nécessaire ni suffisante).
- **Progression des volumes non uniforme** : la 3e position vaut 0,02 (A, B) mais **0,03 (C)**.
  La formule des lots n'est donc pas un simple « ×2 à la 3e » ; dépendance possible à la
  distance, à la perte flottante ou au nombre de cycles — **NON DÉTERMINABLE** avec 3 paniers
  à 3 positions. Toute extrapolation de martingale classique reste interdite.
- **Paniers très courts** : D dure 17 secondes (+1 ¥), E 87 secondes. La durée moyenne affichée
  du profil (20 min 14 s par transaction) masque une dispersion extrême ; des sorties quasi
  immédiates existent (objectif minuscule atteint, ou clôture opportuniste) — mécanisme exact
  NON DÉTERMINABLE sans prix.
- **Premières entrées à secondes :00 sur C/D/E** (10:30:00, 10:45:00, 11:00:00 — frontières
  M15) contre :20/:34 pour A/B : indice faible d'un déclenchement parfois lié à la clôture de
  bougie, contredit par A/B ; **HYPOTHÈSE À TESTER**, pas une règle.

## 4. Tableau des règles (observations indépendantes = paniers)
| Règle | Statut | Paniers |
|---|---|---|
| Entrée initiale après impulsion haussière, haut de range 15 m | FORTEMENT ÉTAYÉE | 2 (A, B) |
| Renforcements contre le mouvement (−3 à −6,6 bp) | FORTEMENT ÉTAYÉE | 2 (A, B) |
| Intervalles d'ajout irréguliers (29–598 s), non périodiques | FORTEMENT ÉTAYÉE | 2 |
| Clôture groupée d'un panier (à la seconde près) | FORTEMENT ÉTAYÉE | 5 (A–E) |
| Clôture au retour au-dessus du prix moyen pondéré | FORTEMENT ÉTAYÉE pour A/B ; insuffisante seule (C perdant) | 2 + 1 contraire partiel |
| Doublement du lot à la 3e position | CONTREDITE comme règle fixe (0,03 chez C) | 3 |
| Fuseau d'affichage UTC+2 | FORTEMENT ÉTAYÉ | 2 |
| Seuils exacts, formule des lots, objectif chiffré, règle de coupe en perte | NON DÉTERMINABLE | — |

## 5. Risque de queue — toujours non mesuré, mais mieux borné
C prouve que des paniers se ferment en perte ; le profil (49 595 transactions, gain moyen
¥22,37 < perte moyenne ¥27,82, drawdown 31,81 %) reste la seule vue d'ensemble, et ce sont des
valeurs affichées par la plateforme, pas des résultats audités. Ni le nombre maximal de
positions, ni la perte flottante maximale, ni les paniers longs ne sont observables dans les
instantanés publics à ce jour.

## 6. Prochaine étape précise
Mettre en place une **collecte d'instantanés programmée** de la page publique (toutes les
heures, via un environnement non filtré) : en quelques jours, des dizaines de paniers réels —
dont des perdants et des longs — deviendraient analysables, et les prix Dukascopy correspondants
seraient publiés entre-temps par le flux. C'est le seul élargissement autonome licite identifié ;
l'alternative (historique complet) suppose l'accès du compte suiveur, hors périmètre actuel.
