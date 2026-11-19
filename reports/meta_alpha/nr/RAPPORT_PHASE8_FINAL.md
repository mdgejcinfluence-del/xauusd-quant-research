# RAPPORT PHASE 8 FINAL — CORPUS « NOUVEAU RÉGIME »

## Issue (au sens du §6 de l'ordre)
**Atlas NR sans cellule survivante → clôture définitive du corpus NR.** Budget NR : **0/24 essais consommés** (aucun candidat légal n'est né des cribles). Renaissance uniquement par donnée payante + ordre explicite du propriétaire.

## Collecte et qualification des sources (seq 119)
| Source | Verdict |
|---|---|
| S1 Yahoo GC=F daily | ✅ colonne vertébrale : IS_NR 1 007 j (2020–2023), VALID 252 j, HOLDOUT au lake (upload seul) |
| S1 Yahoo XAUUSD=X | ❌ 404 query1 **et** query2 depuis CI — abandonné, consigné (GC=F suffit) |
| S1 Yahoo horaire | ⚠️ 2024+ seulement → intraday IS_NR impossible par S1 (constat, pas contournement) |
| S1 Yahoo 1 min | ✅ roulant 7 j actif au lake (30 j refusé par Yahoo, consigné) |
| S2 Swissquote | ✅ enregistreur actif (cron 14h10/22h10 UTC lun–ven) ; snapshot : spread min 50,4 ¢ à 3 725 $ ≈ **1,35 bp** |
| S3 Dukascopy | ✅ **QUALIFIÉ** (ticks .bi5 vérifiés ; bougies 1 min : t = secondes depuis minuit UTC, sonde versionnée) |

Lake Kaggle privé `shalom5123/xauusd-nr-corpus` créé et vérifié. Coût du nouveau régime, mesuré et non importé : le spread en bp a chuté (prix ×2,5, spread en cents stable) — C1_NR ≈ 1,4–2,5 bp contre ~3–4,5 bp dans l'ancien corpus. L'avantage annoncé par le coach existe ; il n'a pas suffi.

## Backfill intraday S3 — couverture honnête
12 fichiers mensuels (2020, à trous : throttling progressif de Dukascopy sur IP de CI ; un premier lot corrompu par un mauvais décodage d'horodatage a été **jeté et consigné**, format sondé puis corrigé). 3 768 heures IS_NR exploitables. Les mois 2021–2023 restent téléchargeables par reprise (le collecteur saute les mois présents) — chantier de collecte, pas de recherche ; il ne change pas le verdict ci-dessous, le crible étant dominé par le plancher de coût autant que par le MDE.

## ATLAS_NR (0 essai, descriptif)
Daily complet (`ATLAS_NR.md`) + intraday 2020 (`ATLAS_NR_INTRADAY.json` : M1/M5 mesurés sur spreads Dukascopy réels, spread médian ≈ 2,2 bp).
- **Crible daily : 0/6** (effets 0,3–6,1 bp ; seuils 10,8–48,4 bp).
- **Crible intraday : 0/30** (meilleur effet 7,4 bp — fenêtre 17–21 UTC, régime nerveux, 4 h — contre seuil 22,2 bp ; le plancher ECR≥2 à C1_BG = 9,4 bp élimine à lui seul presque tout, comme en Phase 7).

## Moteur méta-portefeuille (§5, livré avant tout edge, comme ordonné)
`ci_tools/meta_portfolio.py`, testé sur synthétique uniquement : allocation ∝ IR² pénalisée par corrélation (borne basse d'IR par patte — une patte à borne ≤ 0 pèse zéro), Kelly de crise multi-stratégies, CUSUM kill-switch par patte (k=0,5σ, h=4σ), interface `challenge_sim`. Il attend des pattes certifiées ; il n'en a reçu aucune.

## Registre des 24 essais NR
Aucun né. BY(24) sans objet. HOLDOUT_NR (2025+) jamais ouvert ni téléchargé par un moteur.

## Conclusion
La doctrine a été satisfaite de bout en bout : source nouvelle réelle, régime nouveau mesuré (or à 3 700 $, spread en bp divisé par ~2,5), préenregistrements, gates avant tests. Le nouveau régime a changé les coûts ; il n'a pas changé la structure : le contenu directionnel descriptif reste sous le plancher de capturabilité, aux deux ancres. Le programme de recherche directionnelle — ancien corpus (seq 117) et corpus NR — est clos. Renaissance : donnée payante + ordre du propriétaire, hors budget 0 FCFA. Les actifs permanents demeurent : F3/F7 (service), châssis durci + méta-portefeuille prêt, simulateur ancré, packs et lake scellés, enregistreur de spread S2 en marche (il continuera d'accumuler la vérité des coûts, gratuitement), et 121 entrées d'audit.
