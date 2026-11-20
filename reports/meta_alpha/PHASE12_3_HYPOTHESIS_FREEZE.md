# PHASE 12.3 — GEL DES 36 HYPOTHÈSES S12-01 / S12-02

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**Statut : GEL DOCUMENTAIRE — le budget BY(36) n'est pas autorisé (décision
propriétaire Phase 12.3).** Aucune cellule ne peut être modifiée après consultation
de ses résultats ; aucune cellule ne peut être ajoutée ; une fusion (réduction) ne
peut être décidée que sur la faisabilité (§ inventaire), avant toute performance,
et documentée. Budgets inchangés : tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 ·
NR 0/24 · P9 10/12.

## 1. Formule de coûts gelée (correction Phase 12.3)

Formule générale retenue par le propriétaire :

**`D_TP ≥ 2 × D_SL + C_gain + 2 × C_perte`**

où `C_gain` = coût total supporté sur un trade gagnant (commissions + slippage de
sortie gagnante + autres frais) et `C_perte` = coût total supporté sur un trade
perdant, **hors spread déjà contenu dans les distances sur prix exécutables**
(audit seq 148 : entrée Ask / sortie Bid pour un long, symétrique pour un court).
La forme `3C` de Phase 12.1 n'est qu'un cas particulier, licite uniquement si
l'égalité `C_gain = C_perte = C` est explicitement justifiée au préreg (mêmes
commissions, slippage supposé symétrique — hypothèse à écrire, jamais implicite).
Distinction maintenue (seq 148) : volatilité prévue (échelle σ) ≠ mouvement absolu
attendu (E|Δ|) ≠ probabilité d'atteinte de la cible (**non calibrable** avec les
données du programme ; aucune cellule ne peut invoquer une telle probabilité).

## 2. Règles communes gelées (toutes cellules)

Conventions seq 144/146/148 telles que corrigées : journée UTC ; blocs de session
UTC (Asie [00:00, 08:00), entrée Londres [08:00, 13:00) et New York [13:00, 21:00),
hors 15 premières minutes — paramètre de conception non mesuré) ; exclusion news
FOMC/NFP/CPI [T−5, T+5] avec liquidation T−5 (calendrier `available_at_utc`) ;
niveaux : extrêmes de la session Asie du jour et de la veille UTC (plus haut sur Ask,
plus bas sur Bid — convention exécutable) ; entrée à la première cotation exécutable
après confirmation (jamais le Mid, jamais une clôture indisponible) ; stop dur posé
dès l'entrée, jamais dégradé ; sortie à la cible structurelle, au stop, à
l'invalidation ou à l'horizon maximal (fin de session d'entrée pour S12-01 ; ≤ 2
sessions pour S12-02) ; filtres à chaque entrée : **F3/Q** avec
`Q_required(t) = 2·D_SL(t)/C(t) + 3` évalué par décision au scénario central (plus de
seuil universel, seq 148), **F7 conditionnel** (blocage si décile d'alerte 10 ET Q
insuffisant ; sinon réduction de risque de moitié — paramètre proposé non calibré),
**S2** spread observé ≤ 4,0 bp (paramètre proposé) ; géométrie admise seulement si
`D_TP ≥ 2·D_SL + C_gain + 2·C_perte` au scénario central ; sizing abstrait (spec MT5
absente) ; budgets de protection 3 %/jour et 7 % DD = paramètres proposés, non des
garanties. Métrique primaire de chaque cellule : **moyenne du PnL net par trade
(Bid/Ask, scénario central)** avec IC95 % ; métriques secondaires pré-déclarées :
PnL net aux scénarios favorable/défavorable, signe par tiers chronologique, ECR,
fréquence hebdomadaire, drawdown de la variante. Critère de rejet d'une cellule
(gates conjonctifs, seq 146/148) : n_eff < 200 grappes jour×niveau ⟹ NON TESTABLE
(0 essai) ; MDE au n_eff > effet minimal ⟹ NON TESTABLE ; sinon rejet si IC95 % net
inclut 0 à C1_NR ou C1_BG, ou signe non stable 3/3, ou ECR < 2, ou p non survivant à
BY(36).

## 3. Les 36 cellules (gelées)

Hypothèse économique commune S12-01 : les exécutions forcées au-delà d'un niveau de
référence (stops, suiveurs tardifs) s'épuisent si le prix est rejeté ; la réintégration
confirmée signale ce rejet. S12-02 : la cassure engage suiveurs et rachats de stops ;
le retest réussi trie les vraies cassures. Paramètres figés par cellule ci-dessous
(inventaire machine : `PHASE12_3_CELL_INVENTORY.csv`).

**S12-01 « SWEEP » (12)** — déclencheur : bougie 1 min clôture au-delà du niveau,
bougie suivante clôture réintégrée ; entrée à la confirmation ; stop = extrême du
balayage − buffer_stop ; cible = niveau structurel opposé gelé (extrême opposé de la
même source de niveau), admise seulement si la formule §1 tient.

| ID | Dir. | Niveau | Buffer stop (bp) | Cellules partageant les mêmes événements |
|---|---|---|---|---|
| S12-01-L-A2 / L-A5 / L-A10 | LONG | Bas Asie | 2 / 5 / 10 | même grappe (le buffer ne change pas le déclencheur) |
| S12-01-L-V2 / L-V5 / L-V10 | LONG | Bas veille | 2 / 5 / 10 | idem |
| S12-01-C-A2 / C-A5 / C-A10 | COURT | Haut Asie | 2 / 5 / 10 | idem |
| S12-01-C-V2 / C-V5 / C-V10 | COURT | Haut veille | 2 / 5 / 10 | idem |

**S12-02 « BREAKOUT-RETEST » (24)** — déclencheur : clôture 1 min complète au-delà
du niveau + buffer_cassure, retest du niveau (±0,05 %) sous 60 min avec clôture du
bon côté ; entrée à la confirmation de retest ; stop = extrême du retest − buffer_stop ;
cible = prochain niveau structurel, condition §1.

| ID (motif ×12 par direction) | Dir. | Niveau | Buffer cassure (bp) | Buffer stop (bp) |
|---|---|---|---|---|
| S12-02-L-A-b2-s2 … L-A-b5-s10 | LONG | Haut Asie | 2 / 5 | 2 / 5 / 10 |
| S12-02-L-V-b2-s2 … L-V-b5-s10 | LONG | Haut veille | 2 / 5 | 2 / 5 / 10 |
| S12-02-C-A-b2-s2 … C-A-b5-s10 | COURT | Bas Asie | 2 / 5 | 2 / 5 / 10 |
| S12-02-C-V-b2-s2 … C-V-b5-s10 | COURT | Bas veille | 2 / 5 | 2 / 5 / 10 |

(Les 24 identifiants complets, un par combinaison, sont dans l'inventaire CSV, qui
fait foi en cas de divergence avec cette notation compacte.)

## 4. Famille BY(36)

Famille = ces 36 hypothèses, métrique primaire unique par cellule (§2). BY au niveau
q = 0,05 contrôle le FDR sous dépendance (H₃₆ ≈ 4,25) ; le FWER n'est pas contrôlé
(écrit, seq 148). Aucune addition après préreg ; aucune suppression après résultats ;
les réductions pour faisabilité sont décidées **maintenant**, sur l'inventaire de
puissance, et listées dans `PHASE12_3_BUDGET_PROPOSAL.md`.

*Gel produit sans consulter aucun rendement : les définitions ci-dessus précèdent
l'inventaire de faisabilité et ne dépendent pas de ses résultats chiffrés de
performance (il n'en contient aucun).*
