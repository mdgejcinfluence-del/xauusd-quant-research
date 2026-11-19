# RAPPORT PHASE 9 FINAL — « DERNIÈRES PORTES »

## Résultat de phase : **deux pattes certifiées** (carry BTC et ETH). Budget consommé : **10/12** (B1 : 2, CARRY : 8). BY(12) respectée au niveau de la phase. La Phase 9 ne se referme donc pas sur un néant : elle transmet au propriétaire une décision d'exploitation, qui n'est pas prise ici.

## Bloc B1 — Dérive pré-annonce : ÉCHEC 0/2 (seq 128)
Fenêtre T−240→T−5 min, 326 événements poolés : long inconditionnel −1,2 bp, continuation −3,0 bp, IC franchissant zéro, placebos ±7 j du même ordre. La dérive pré-FOMC des actions ne vit pas sur l'or — ou pas à nos coûts. Confirmation NR non déclenchée (pré-déclarée). B1 enterré.

## Bloc CARRY — la carte des paiements (seq 127, `CARRY_MAP.md`)
Première mesure du programme qui n'est pas une prédiction : le funding des perpétuels, un flux que les longs paient aux shorts, delta-neutre.

| Patte | Funding net %/an | Jours+ | Série nég. max | Ères (21-22/23-24/25-26) | Statut |
|---|---|---|---|---|---|
| **BTCUSDT** | **+11,2** | 88 % | 11 j | +17,4 / +9,9 / +4,2 | **CERTIFIÉE** |
| **ETHUSDT** | **+13,3** | 88 % | 13 j | +19,2 / +10,6 / +3,6 | **CERTIFIÉE** |
| ZECUSDT | +10,7 | 87 % | 19 j | +21,2 / +12,7 / **−10,5** | enterrée (ère récente négative) |
| SOLUSDT | −12,9 | 71 % | 28 j | mixte | enterrée |
| SOXL / XAU / SNDK / SKHYNIX (perpétuels d'actions et or) | +9,9 à +26,4 mesurés | ~60 % | 2–6 j | **1 seule ère** (nés fin 2025–2026) | **non certifiables** : historique trop court — en observation, pas enterrés comme faux |

Le paiement est réel, mesuré sur 6,5 ans et 7 488 événements par patte, net de coûts déclarés prudents (40 bp), IC95 loin de zéro, séries négatives courtes. Il est aussi **en compression franche** (BTC : 17,4 → 9,9 → 4,2 %/an) : le coach avait raison sur la direction, et quiconque le récolte récolte un flux qui s'érode. Corrélation BTC/ETH des funding journaliers : 0,87 — le « portefeuille » de deux pattes est presque une seule patte ; poids indiciels du méta-portefeuille (IR² pénalisé) : 57/43, enregistrés dans `META_PORTFOLIO_LEGS.json`.

Incidents consignés : sélection par profondeur refaite deux fois avant toute mesure de funding (OI en unités de coin non comparable ; tranche alphabétique [:60] qui excluait BTC/ETH) — la liste finale est par volume USD sur les 913 symboles.

## Bloc B2-extension — prime de variance ère NR (0 essai)
L'érosion continue, sans s'inverser : **+2,2 (2020-22) → +1,5 (2023-24) → +0,4 (2025-26)** points de vol, positive ~70–77 % du temps (contre +7,1/+6,0/+3,1 et ~95 % dans l'ancien IS). La prime existe toujours ; elle s'amincit vers zéro. Actif dormant : pas d'infrastructure options, pas de trade, aucune certification — comme ordonné.

## Bloc B3 — étagère confirmée (0 essai)
Non rouvert : borné en Phase 8/9 (adverse selection ≈ spread capté) et inapplicable sur terrains 100 % taker.

## Ce qui est transmis au propriétaire
Deux pattes de carry certifiées, enregistrées dans `meta_portfolio.py`, avec leurs chiffres d'érosion écrits en première ligne. Toute exploitation réelle (compte exchange, KYC, capital, levier ≤ 3× et collatéral ≥ 50 % selon les maths de liquidation du prereg) est une **décision séparée du propriétaire**, hors de cette phase et hors budget 0 FCFA actuel — la recherche, elle, est terminée et chaînée (seq 124→131).

## État final des budgets
Phase 9 : 10/12 consommés, 2 non dépensés (la confirmation NR de B1, jamais déclenchée, et la marge). Tous les budgets historiques restent figés. Le programme directionnel sur l'or reste clos (seq 117/121 inchangés) ; ce qui s'est ouvert en Phase 9 n'est pas de la direction — c'est un paiement, et il est certifié comme tel, avec son érosion en face.
