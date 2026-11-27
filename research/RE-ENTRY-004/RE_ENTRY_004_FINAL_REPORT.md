# RE-ENTRY-004 — TEST DE L'HYPOTHÈSE DES DEUX PHASES (amorçage / renforcement martingale)

Hypothèse testée telle que préenregistrée (seq438), sans aucune modification après résultats.
Données : 5 paniers reconstruits (A–E, cotations Dukascopy comparatives, UTC+2 fortement étayé) ;
un 3e instantané public archivé ce cycle n'a apporté **aucune transaction nouvelle** (la page et
le compteur du profil, 49 595, sont inchangés — période calme ou affichage figé, non tranché).

## Test central — les ajouts n°2 et n°3 n'obéissent pas à la même règle (tableau TWOPHASE_TABLE.csv)
**Ajout n°2 (4 paniers : A, B, C, E)** : délais **16, 20, 29, 40 secondes** — toujours immédiats ;
déplacements depuis la 1re entrée : −4,11 / −2,96 / **−0,09 (neutre)** / **+2,11 bp (favorable)**.
La phase 1 « entrée en deux temps » est reproductible dans sa dimension temporelle et
indifférente au signe du mouvement.
**Ajout n°3 (3 paniers : A, B, C)** : délais 180 / 194 / 598 s ; déplacements depuis la 1re
entrée : **−6,56 / −5,58 / −4,68 bp** — toujours défavorables, dans une zone étroite reproduite
sur 3 paniers indépendants malgré des délais très variables. Le déclencheur de la 3e position
est donc compatible avec un **recul minimal depuis la première entrée (≈ −4,5 à −6,5 bp)**,
pas avec un délai (180 à 598 s) ni avec le recul depuis la 2e position (−1,7 à −5,5 bp, dispersé).

## Verdict sur l'hypothèse préenregistrée
**FORTEMENT ÉTAYÉE** — pas CONFIRMÉE : 4 et 3 paniers indépendants seulement. Forme précise :
entrée initiale directionnelle ; deuxième entrée quasi immédiate (16–40 s) à règle distincte
(confirmation/pairing temporel, condition exacte NON DÉTERMINABLE) ; renforcement martingale à
partir de la 3e position sur recul défavorable. Les volumes de la 3e position (0,02 / 0,02 / 0,03)
ne suivent toujours aucune formule identifiable à ce stade.

## Phases E et F — limites nettes
- **Positions 4 et suivantes : NON DÉTERMINABLE.** Aucun panier collecté n'en comporte ; rien
  n'est extrapolé (progression, exposition maximale, plafond de positions inconnus).
- **Clôture nette (panier C approfondi)** : clôture au prix moyen pondéré à 0,04 USD près, avec
  des profits individuels de −4/−3/+1 ¥ (les deux premières positions perdent, la 3e gagne) —
  le brut de panier est ≈ 0 au point de sortie, le net de −6 ¥ s'explique par spreads/coûts.
  A et B, en revanche, ferment à +5,7 et +8,0 bp **au-dessus** de leur prix moyen (nets +11/+13 ¥).
  Il n'existe donc pas de distance fixe au-dessus du prix moyen : la sortie ressemble à
  « premier retour au voisinage du point mort ou au-delà, saisi quand il se présente » — avec,
  chez C, une acceptation du point mort (perte nette). Seuil financier net exact, rôle éventuel
  d'une durée maximale ou d'une condition de sécurité : **NON DÉTERMINABLE**.

## Risque du mécanisme à deux phases (évaluation)
La structure confirmée dans ses grandes lignes est asymétrique : phase 1 rapide et peu risquée
(0,02 lot engagé en < 1 min), phase 2 qui engage 0,02–0,03 lot supplémentaires **contre** la
tendance à −5 bp, sans stop observé, avec une sortie qui accepte le point mort. Le risque se
concentre entièrement dans les paniers qui ne reviennent pas : inconnus à ce jour (aucun panier
à 4+ positions, aucune perte flottante maximale observée). Le drawdown affiché de 31,81 % et le
gain moyen inférieur à la perte moyenne restent les seuls témoins de cette queue.

## Tableau de classement final
| Conclusion | Statut | Paniers |
|---|---|---|
| Entrée n°2 quasi immédiate (16–40 s), signe indifférent | FORTEMENT ÉTAYÉE | 4 |
| Entrée n°3 sur recul −4,7 à −6,6 bp depuis la 1re | FORTEMENT ÉTAYÉE | 3 |
| Délai comme déclencheur de la 3e position | RÉFUTÉE (180–598 s dispersés) | 3 |
| Recul depuis la 2e position comme déclencheur | NON DÉTERMINABLE (dispersé) | 3 |
| Formule des lots | NON DÉTERMINABLE | 3 |
| Positions 4+ | NON DÉTERMINABLE | 0 |
| Distance fixe de clôture au-dessus du prix moyen | RÉFUTÉE (C au point mort) | 3 |
| Clôture au premier retour au voisinage du point mort | HYPOTHÈSE À TESTER | 3 |

## Prochaine étape
Continuer les instantanés (15 min en session active) jusqu'aux premiers paniers à 4+ positions
et à longue durée : ce sont eux, et eux seuls, qui trancheront la phase 2 profonde (plafond,
progression réelle des lots, perte flottante maximale) et la règle de coupe en perte.
