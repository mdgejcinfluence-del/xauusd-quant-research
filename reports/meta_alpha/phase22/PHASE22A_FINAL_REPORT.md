# PHASE 22-A — RAPPORT FINAL : SWEEP & RECLAIM (A) ET IMPULSE–PULLBACK–RESUMPTION (B)

Statut : `EXPLORATORY_POST_HOC`. Familles étudiées séparément, jamais fusionnées. Holdout interdit.
Résultats nets nommés `HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION`
(spread intégré une fois sur prix Bid/Ask réels, slippage S2 = 1 bp/côté principal, commissions exclues).
Verdicts au registre seq381.

## Famille A — Sweep & Reclaim (3 073 événements primaires confirmés ; 1 281 breakouts sans réintégration)

Après réintégration d'un niveau balayé (Overnight High/Low, Previous Day High/Low), le déplacement
contrariant existe en Mid mais est faible et symétrique (à 1 h : MFE médian ~11–13 bp, MAE médian
~11–15 bp, terminal Mid ≈ 0 ; 65 % des événements Overnight touchent le centre de la boîte avant la
clôture, 38 % l'extrémité opposée). Une fois le spread et le slippage S2 appliqués, le rendement
directionnel contrariant est **significativement négatif** sur presque tous les niveaux et horizons :
−3,7 à −8,2 bp en moyenne (q BH ≤ 0,047 pour 10 des 12 tests ; seuls A3/A4 à EOD sont non
significatifs), taux positif 39–51 %, négatif dans les deux sous-périodes (−6,1 bp en 2010-2015,
−3,4 bp en 2016-2019 à EOD). Queues lourdes : MAE médian EOD ~37 bp, P5 du net −119 bp, pire −545 bp,
20 % de pertes > 50 bp sans stop (aucune politique de stop optimisée, conformément au contrat).

**Verdict A : `SWEEP_RECLAIM_NO_ASYMMETRY`** — la réintégration ne produit pas d'asymétrie contrariante
exploitable ; après coûts hypothétiques, le mécanisme est perdant. Inverser le sens après coup pour
prétendre un edge de continuation est interdit et n'est pas revendiqué (le terminal Mid est ~nul ;
l'écart vient des coûts).

## Famille B — Impulse–Pullback–Resumption H4 (905 épisodes : 505 reprises, 300 invalidations complètes, 97 sans reprise, 3 sans pullback)

Après confirmation de reprise, le rendement aligné net S2 est de −1,2 bp (2 barres), −2,1 bp
(4 barres), −6,7 bp (8 barres), **aucun significatif** (q 0,35–0,72), médianes négatives (−5 à −10 bp),
MAE médian croissant (21 → 65 bp), 33 % de pertes > 50 bp à 8 barres, signe instable entre
sous-périodes à H8 (−13,6 bp en 2010-2015, +4,0 bp en 2016-2019).

**Verdict B : `H4_IMPULSE_WITHOUT_RESUMPTION_ADVANTAGE`** (et `NO_ECONOMIC_ASYMMETRY_SUPPORTED`).

## Réponses aux questions de clôture

1. Non : pas de déplacement contrariant mesurable après coûts après sweep & reclaim.
2. Les retours au centre sont fréquents (65 %) mais d'amplitude symétrique à l'adverse — insuffisants.
3. Non : aucune asymétrie favorable après reprise d'impulsion H4.
4. Non : rien ne persiste après spread + S2 (S0 déjà négatif ou nul presque partout).
5. Non : queues adverses (P5 −119/−176 bp) incompatibles avec une exploitation sans gestion du risque
   qui, elle, n'était pas autorisée à être optimisée.

**Aucune des deux familles n'est inscrite `ECONOMIC_CANDIDATE_EXPLORATORY`.** Aucune stratégie
combinée, aucun entraînement, aucun ordre. Trois défauts ont été corrigés avant interprétation
(identifiants d'événements par lot fusionnés à tort, prix d'entrée indexé sur la fenêtre au lieu de
la journée, téléversement d'artefacts incluant les fragments des autres lots) ; seuls les chiffres
de la version corrigée, reproduite en CI verte, sont rapportés ici.
