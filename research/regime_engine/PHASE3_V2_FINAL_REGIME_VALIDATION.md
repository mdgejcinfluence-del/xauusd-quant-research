# PHASE 3 V2 — STEP 3.7 : VALIDATION DE LA CARTE FINALE DES RÉGIMES

- **Étape** : 3.7 — validation/invalidation de la carte provisoire issue de 3.6J (`PHASE3_V2_FINAL_REGIME_VALIDATION.md`).
- **Sources EXCLUSIVES (vérifiées présentes)** : `PHASE3_V2_FINAL_REGIME_MAP.md` (3.6J), `PHASE3_V2_G_E2_VALIDATION.md` (3.6I), `PHASE3_V2_G_E2_PROFILE.md` (3.6H), `PHASE3_V2_REGIME_MAP_CONSOLIDATION.md` (3.6G), `PHASE3_V2_REGIME_MAP_CANDIDATES.md` (3.6F).
- **Aucun nouveau modèle, aucun K, aucun clustering, aucun backtest, aucune stratégie, aucune optimisation, aucun recalcul, aucune modification de features, aucun classifieur.**
- **Question unique traitée** : *« Avons-nous maintenant suffisamment de preuves pour appeler la carte des régimes XAUUSD 2010–2026 une cartographie finale, ou doit-elle rester provisoire ? »*

---

## §1. Méthode de validation

1. **Aucune donnée nouvelle** : la validation s'appuie strictement sur l'ensemble de preuves déjà produit (3.6F → 3.6J). Le verdict 3.7 ne peut donc **ni créer** de preuve nouvelle, **ni changer** les faits établis ; il peut seulement **statuer définitivement** sur chaque état à partir de l'existant.
2. **Sept axes par état** : statut final ; preuve de récurrence ; preuve de persistance ; preuve de distinction comportementale ; reproductibilité ; dépendance éventuelle à un artefact/anomalie ; niveau de confiance.
3. **Règles impératives appliquées** :
   - G-E0 → régime **uniquement si** récurrence démontrée ;
   - G-E1 → régime **uniquement si** sa structure dépasse le confinement 2010 ;
   - G-E3 → régime **uniquement si** preuve indépendante supplémentaire déjà disponible ;
   - G-E4 → **EXCLUDED** si instabilité K + quasi-constance non résolues ;
   - G-E2 → verdict **définitif** à partir des preuves disponibles (3.6I : UNCERTAIN) ;
   - G-B → distinguer explicitement d'un simple « cluster résiduel ».
4. **Verbalisation** : chaque axe est marqué **ÉTABLI** (preuve dans l'existant), **NON ÉTABLI** (preuve absente de l'existant) ou **PARTIEL** (preuve partielle/existante mais limitée).

---

## §2. Tableau de décision — les 6 états

| État | (1) Statut final | (2) Récurrence | (3) Persistance | (4) Distinction comportementale | (5) Reproductibilité | (6) Dépendance artefact/anomalie | (7) Confiance |
|---|---|---|---|---|---|---|---|
| **G-B** | **FINAL_REGIME** | **ÉTABLIE** (continue 2010–2026) | **ÉTABLIE** (diag HMM 0.9997–0.9998 ; épisodes longs en K2) | **ÉTABLIE** (unique par sa neutralité — voir §3.1) | **ÉTABLIE** (8/8 configurations) | **AUCUNE** détectée | **HIGH** |
| **G-E2** | **CANDIDATE_REGIME** | **ÉTABLIE** (4 années disjointes) | **NON ÉTABLIE** (médiane ép. = 1 bar ; diag 0.9957 = plus faible ; épisodes HMM par état inconnus) | **ÉTABLIE** (signature sélective queue droite/extrêmes désagrégés) | **PARTIELLE** (2 configs KM identiques + 1 HMM « approchante » 6× atténuée) | **NON résolue** (fragmentation K-means ; sensibilité au modèle de covariance) | **MEDIUM** |
| **G-E0** | **EVENT** | **NON ÉTABLIE** (2 fenêtres : 2015, 2021) | **NON PERTINENTE** (0.9999 = artefact d'un état à 2 fenêtres) | **ÉTABLIE** (queue extrême −17,5σ/+30,5σ) | **ÉTABLIE** (identité exacte KM K2–K5 + HMM full, ARI 1.0) | **OUI — anomalie de source connue** (règle F3 « ≥ 30 extrêmes », 3.6A) | **HIGH** (comme événement/anomalie) |
| **G-E1** | **EVENT** | **NON ÉTABLIE** (98 % concentrés en 2010) | **PARTIELLE** (diag 0.9969–0.9997 ; noyau ≈ 27 100 bars) | **ÉTABLIE** (signature mèche basse/corps réduit/clôture haute — unique) | **ÉTABLIE** (6/6 configurations K≥3, profils quasi identiques) | **OUI — bord de période** (2010 : début du domaine, lieu des anomalies résiduelles 3.6D) | **HIGH** (structure) ; **MEDIUM** (récurrence) |
| **G-E3** | **INDETERMINATE** | **NON DÉMONTRABLE** (présence toutes années mais détection mono-configuration) | **PARTIELLE** (diag 0.9960 ; épisodes par état non calculés) | **ÉTABLIE** (volatilité jour/mois +3,08σ/+2,46σ — unique) | **NON ÉTABLIE** (1 seule configuration : HMM K5 s4) | **NON résolue** (aucune preuve indépendante dans l'existant) | **LOW** |
| **G-E4** | **EXCLUDED** | **NON ÉTABLIE** (poids instable en K) | **NON PERTINENTE** (définition change avec K) | **PARTIELLE** (storm_p90_run = 1) | **NON ÉTABLIE** (jamais retrouvé par K-means) | **OUI — artefact technique** (feature quasi-constante, MAD ≈ 0 → fallback std ; z non interprétable) | **LOW** |

---

## §3. Dossiers par état

### §3.1 G-B — « comportement de référence » → **FINAL_REGIME** (confiance HIGH)

- **Récurrence** : **ÉTABLIE** — seul état présent **en continu 2010–2026** ; part de ses lignes par année : 2010 1,4 ; 2011 4,9 ; 2012 3,4 ; 2013 8,3 ; 2014 6,1 ; 2015 7,4 ; 2016 5,9 ; 2017 3,9 ; 2018 5,8 ; 2019 5,9 ; 2020 5,0 ; 2021 8,3 ; 2022 7,0 ; 2023 8,4 ; 2024 8,6 ; 2025 6,2 ; 2026 3,6 (%) (HMM K2) — **aucune année à zéro**.
- **Persistance** : **ÉTABLIE** — diag HMM 0.9997–0.9998 ; KM K2 : 3 épisodes, médiane 566 628 bars (pas une mosaïque) ; KM K3 0.9999, KM K4 0.9998 (K5 0.9825 = fragmentation documentée, non une propriété de l'état). HMM : médianes d'épisodes 193–268 bars.
- **Distinction comportementale** : **ÉTABLIE** — profil ≈ médiane globale (|z| ≤ 0,3 sur les 25 features) ; tous les autres états sont des **écarts circonscrits** à ce profil (queue extrême, microstructure, forme de distribution, volatilité, extrêmes cumulés). G-B est l'unique état **sans** écart discriminant.
- **Reproductibilité** : **ÉTABLIE** — 8/8 configurations (KM K2–K5 + HMM K2–K5) ; tailles 58,33–98,52 % (KM), 66,71–69,30 % (HMM) ; silhouette K2 0.7911 (séparation avec l'état rare) ; ARI seeds ≥ 0.974 sur toutes les configurations.
- **Dépendance artefact** : **AUCUNE** — pas de dépendance à une feature quasi-constante, pas de coïncidence avec les anomalies F3/3.6D, pas de confinement temporel.
- **G-B n'est PAS un « cluster résiduel »** — justification explicite :
  1. Un cluster résiduel est un **réceptacle d'éléments hétérogènes** mal attribués. G-B est à l'inverse un **mode central homogène** : profil stable = médianes globales, |z| ≤ 0,3 sur les 25 features, aucune queue de distribution mélangée ;
  2. G-B est **séparé et non « le reste »** : en K2, la silhouette 0.7911 mesure une **vraie séparation** entre G-B et l'état rare ; la partition n'est pas « tout sauf les anomalies » ;
  3. G-B est **reproduit** par deux familles de modèles indépendants (K-means **et** HMM), en 8/8 configurations — un cluster résiduel serait instable entre modèles ;
  4. G-B a une **persistance temporelle propre** (diag 0.9997–0.9998, épisodes longs en K2) — un résidu n'a pas de dynamique propre ;
  5. Les anomalies G-E0/G-E1 sont **séparées explicitement** de G-B (et non absorbées par lui) — comportement inverse d'un fourre-tout. Le seul « résidu » du pipeline serait l'absence d'autre régime validé, ce qui ne fait pas de G-B un résidu ;
  6. **Limite honnête** : G-B est le mode dominant, donc sa médiane est structurellement proche de la médiane globale ; sa « distinction » est une distinction **par défaut** (neutralité) et non par excès. G-B est le **régime de référence** de la carte — il décrit le comportement modal, pas un comportement exceptionnel.

---

### §3.2 G-E2 — « queue droite modérée, extrêmes moins agrégés » → **CANDIDATE_REGIME** (confiance MEDIUM) — verdict **définitif**

- **Récurrence** : **ÉTABLIE** — 2013 (26,7–28,2 %), 2014 (18,4–19,0 %), 2016 (35,1–35,5 %), 2017 (14,6–15,8 %) = 4 années disjointes sur 2 blocs (2013–2014, 2016–2017), + résiduel 2026 (2,9–3,1 %) et 2024 (0,7 % en K4 seulement) ; absent 2010–2012, 2015, 2018–2023, 2025.
- **Persistance** : **NON ÉTABLIE** — diag KM K4 0.9987 / KM K5 0.9973 (empirique, étiquettes dures) ; **diag HMM 0.9957 = la plus faible de toute la carte** ; médiane d'épisode = **1 bar** (mosaïques de frontière K-means, limitation connue) ; moyenne 368–832 ; noyau max ≈ 22 600 bars ; **épisodes HMM par état : non disponibles**.
- **Distinction comportementale** : **ÉTABLIE** — signature exclusive et sélective : skew +4,72σ, kurtosis +6,22σ, ext_spacing +1,12σ, storm_clust −0,85σ (+ ext_rate −0,52σ, run −0,46σ) ; 20 autres features |z| ≤ 0,52 ; bougies ≈ référence (|z| ≤ 0,18) ; volatilité légèrement basse (|z| ≤ 0,31) ; directionnalité neutre — **aucun autre candidat ne partage cette combinaison**.
- **Reproductibilité** : **PARTIELLE** — identique entre KM K4 s1 (84 750 ; 4,49 %) et KM K5 s0 (80 117 ; 4,24 %) (tailles 5,5 % d'écart, profils résumés identiques, répartitions annuelles ≈ superposées) ; **HMM K5 s3 « approchante » mais atténuée** : skew +0,72σ vs +4,72σ, kurt +1,0σ vs +6,22σ (≈ 6× plus faibles), run/vr2 de sens opposés, répartition annuelle **non disponible**. ARI seeds : KM K4 0.885/0.885/0.9999, KM K5 0.988/0.978/0.974.
- **Dépendance artefact/anomalie** : **NON résolue mais non identifiée comme anomalie de source** — pas de coïncidence avec F3 ni avec les anomalies 2010 ; en revanche **sensibilité non testée** à la fragmentation K-means (médiane = 1 bar) et au **modèle de covariance** (le sanity K2 a montré une dépendance totale diag vs full, ARI −0.0154) — ces points restent limitrophes mais ne constituent pas une preuve d'artefact.
- **Verdict définitif (règle)** : les preuves disponibles sont **suffisantes pour classer** G-E2 **CANDIDATE_REGIME** — récurrence et distinction établies, reproductibilité partielle, persistance non établie → **ni FINAL_REGIME, ni REJECT** (rien de réfutatoire ; l'absence de preuve de persistance et de concordance exacte HMM n'est pas une preuve d'absence de structure). Le verdict 3.6I **UNCERTAIN** est ainsi **confirmé et clos** : G-E2 n'est pas un régime final, mais il reste le seul candidat récurrent hors référence.

---

### §3.3 G-E0 — « queue d'aplatissement extrême » → **EVENT** (confiance HIGH comme événement)

- **Récurrence** : **NON ÉTABLIE** — **exactement 2 fenêtres** : 2015-07-20 01:36 → 2015-09-01 08:51 (13 952 bars) et 2021-08-08 23:03 → 2021-09-21 09:57 (13 950 bars) ; 0 % toutes les autres années ; 27 901 lignes (1,48 %).
- **Persistance** : NON PERTINENTE pour un régime — diag 0.9999 est un artefact d'un état quasi absorbant à 2 fenêtres ; les deux épisodes durent ~6 semaines chacun.
- **Distinction comportementale** : **ÉTABLIE** — skew −9,39 (−17,5σ), kurtosis 420,9 (+30,5σ), vr2 −2,91σ, storm_clust +0,95σ — état défini **exclusivement** par des queues extrêmes.
- **Reproductibilité** : **ÉTABLIE** — ensemble **identique** à travers KM K2/K3/K4/K5 et partition identique du HMM full-cov K2 (ARI 1.0000) ; **absent du HMM diag** (la détection dépend du modèle de covariance).
- **Dépendance artefact/anomalie** : **OUI — anomalie de source connue** — coïncide avec la règle F3 « ≥ 30 extrêmes » (3.6A) ; drapeau qualité de données.
- **Application de la règle** : la récurrence **n'est pas démontrée** (2 fenêtres) → **ne peut pas devenir un régime**. Elle reste **EVENT** malgré sa reproductibilité parfaite — la facilité de séparation statistique ne suffit pas.

---

### §3.4 G-E1 — « structure mèche basse / début de période » → **EVENT** (confiance HIGH structure / MEDIUM récurrence)

- **Récurrence** : **NON ÉTABLIE** — 2010 : **97,9–98,5 %** ; 2011 : 1,1–1,2 % ; 2020 : 0,4–0,5 % ; 2025 : 0,3–0,4 % ; 0 % ailleurs. Structure **confinée à 2010** (départ 2010-02-12 11:57 ; dernier épisode 2025-12-01).
- **Persistance** : PARTIELLE — diag 0.9969–0.9997 (KM 0.9970–0.9973 ; HMM 0.9997) ; 258–266 épisodes (médiane 1, moyenne 330–332, noyau ≈ 27 100 bars) — cohérente **à l'intérieur** de 2010.
- **Distinction comportementale** : **ÉTABLIE** — low_wick +7,62σ, body_range −4,22σ, close_pos +4,29σ, range/tr_sigma +1,55/+1,65σ, vr2 +1,70σ, run −0,91σ — combinaison unique, aucun autre candidat ne l'approche.
- **Reproductibilité** : **ÉTABLIE** — 6/6 configurations K≥3 (KM K3/K4/K5 + HMM K3/K4/K5), profils z quasi identiques (low_wick +7,62 vs +7,56 vs +7,63 ; body −4,22 vs −4,17 vs −4,22 ; close +4,29 vs +4,27 vs +4,29).
- **Dépendance artefact/anomalie** : **OUI — bord de période** — 98 % en 2010, début du domaine ; 2010 est aussi le lieu des anomalies résiduelles (3.6D) → **validation source requise** (non exécutée).
- **Application de la règle** : sa structure **ne dépasse pas son confinement 2010** → **ne peut pas devenir un régime**. Elle reste **EVENT** — la reproductibilité inter-méthodes est réelle mais ne remplace pas la récurrence temporelle.

---

### §3.5 G-E3 — « volatilité jour/mois élevée » → **INDETERMINATE** (confiance LOW)

- **Récurrence** : NON DÉMONTRABLE — présent toutes années (pics 2011 21,2 % ; 2020 17,3 %) **mais** détecté dans **1 seule configuration** (HMM K5 s4) ; sans seconde détection, l'étalement temporel n'est pas une preuve de récurrence de la **même** structure.
- **Persistance** : PARTIELLE — diag 0.9960 ; **épisodes par état non calculés** ; seule la médiane globale HMM K5 (193 bars) est disponible.
- **Distinction comportementale** : **ÉTABLIE** — vol_ratio_day +3,08σ, h1_vol_ratio +2,46σ, m1_ext_rate +1,73σ, ext_rate +1,25σ, noise −0,75σ — signature unique (volatilité intra-jour nettement au-dessus de la normale mensuelle).
- **Reproductibilité** : **NON ÉTABLIE** — 1/8 configurations.
- **Dépendance artefact/anomalie** : NON résolue — aucune preuve indépendante supplémentaire disponible dans les résultats existants.
- **Application de la règle** : **aucune preuve indépendante supplémentaire** n'est disponible → **ne peut pas devenir un régime**. Statut **INDETERMINATE** (ni candidat, ni exclu : la distinction est établie mais la structure n'est pas vérifiée).

---

### §3.6 G-E4 — « mois sans extrêmes cumulés » → **EXCLUDED** (confiance LOW)

- **Récurrence** : NON ÉTABLIE — poids **instable en K** : 30,70 % (K2) → 26,04 % (K3) → 12,79 % (K4) → 19,82 % (K5) ; la « même » structure change de taille d'un facteur ~2,4 selon K.
- **Persistance** : NON PERTINENTE — diag 0.9987–0.9995, mais la définition de l'état change avec K ; épisodes par état non calculés.
- **Distinction comportementale** : PARTIELLE — `m3_storm_p90_run_month` = 1 (vs 2 partout ailleurs), storm_clust −0,73/−0,89σ, kurtosis −0,46σ — mais le signal repose sur une **feature quasi-constante** (MAD ≈ 0 → fallback std, z-score non interprétable ; seul le niveau discret 1 vs 2 est fiable).
- **Reproductibilité** : NON ÉTABLIE — 4 configurations HMM (K2–K5) mais **jamais retrouvé par K-means** ; cohérence inter-familles absente.
- **Dépendance artefact/anomalie** : **OUI — artefact technique** — feature quasi-constante + instabilité de K **non résolues**.
- **Application de la règle** : instabilité K + quasi-constance **non résolues** → **EXCLUDED** (confirmé tel quel). Nota : le signal brut « niveau 1 vs 2 » reste une observation réelle, à réévaluer uniquement dans le cadre d'une revue de features (hors périmètre 3.7).

---

## §4. Test de suffisance — réponse à la question unique

### Ce qui est **établi** (preuves existantes)
1. **G-B** est un **régime** au sens strict : présence continue 2010–2026, signature identifiable (neutralité), persistance réelle (diag 0.9997–0.9998, épisodes longs), reproductibilité 8/8, distinction claire, aucune dépendance à un artefact ; **et ce n'est pas un cluster résiduel** (§3.1).
2. **G-E0 et G-E1** sont **définitivement écartés** du statut de régime : pas de récurrence (2 fenêtres / 98 % en 2010) + dépendance à anomalies connues (F3 / bord de période 3.6D). Leur statut **EVENT** est définitif.
3. **G-E2** est **définitivement classé CANDIDATE_REGIME** (verdict 3.6I confirmé et clos) : récurrence et distinction établies ; persistance et concordance HMM non établies.
4. **G-E3 INDETERMINATE**, **G-E4 EXCLUDED**, de façon définitive au vu de l'existant.

### Ce qui **manque** pour appeler la carte « finale » (aucune de ces preuves n'est dans l'existant)
1. **Persistance de G-E2** : statistiques d'épisodes HMM par état (durées médianes/moyennes/max) — seule la médiane globale (193–268) existe ;
2. **Concordance exacte KM/HMM de G-E2** : comparaison directe des partitions (le HMM « approchant » est 6× atténué ; sa répartition annuelle est absente) ;
3. **Robustesse au modèle de covariance** : aucun test full-cov pour G-E2 (le sanity K2 a montré une dépendance totale diag vs full) ;
4. **Validation de source** des fenêtres G-E0 (2015, 2021) et de la période G-E1 (2010) — jamais exécutée ;
5. **Contrôles statistiques** : significativité, stabilité bootstrappée, ARI vs permutation — jamais exécutés (interdits/hors périmètre) ;
6. **Couverture temporelle quantitative** : aucune proportion annuelle « part de chaque année occupée par chaque état » n'a été calculée (seule P(année|état) existe).

### Arbitrage VALIDATED / PROVISIONAL / INSUFFICIENT

- **NON VALIDATED** : la règle exige que les régimes retenus satisfassent ensemble cohérence, persistance, reproductibilité et non-redondance. C'est vrai pour **G-B seul** ; **G-E2**, seul autre candidat, ne satisfait pas la persistance (et seulement partiellement la reproductibilité). Une carte « finale » avec 1 régime validé + 1 candidat incertain ne remplit pas le critère.
- **NON INSUFFICIENT** : une cartographie **robuste et sobre émerge bien** — un régime de référence documenté et validé (G-B, non résiduel), un candidat récurrent bien caractérisé (G-E2), deux événements/anomalies clairement séparés (G-E0, G-E1), un indéterminé (G-E3) et un exclu (G-E4). Ce n'est pas « aucune structure exploitable ».
- **DONC PROVISIONAL** : la structure est **convaincante dans sa sobriété** (1 régime + candidat + événements) mais **complète seulement à ~2/6 des critères de validation d'un second régime** ; plusieurs éléments critiques restent non établis (liste ci-dessus). La carte doit **rester provisoire** — et c'est la conclusion correcte : le corpus de preuves actuel n'a pas changé depuis 3.6J, et il ne permet aucun passage à VALIDATED.

---

## §5. Verdict final

# FINAL_REGIME_MAP = PROVISIONAL

**Réponse à la question unique** : non, nous n'avons **pas** suffisamment de preuves pour appeler la carte des régimes XAUUSD 2010–2026 une **cartographie finale** ; elle doit **rester provisoire**.
- Nous **avons** suffisamment de preuves pour **valider un régime** (G-B) et pour **statuer définitivement** sur les 5 autres états (G-E2 candidat ; G-E0/G-E1 événements ; G-E3 indéterminé ; G-E4 exclu) ;
- Nous **n'avons pas** suffisamment de preuves pour valider un **second régime** récurrent — c'est le point qui bloque le passage à VALIDATED ;
- La carte est **robuste** (cohérence, non-redondance, persistance et couverture **pour le régime retenu** et pour la séparation anomalies/régimes) et donc **pas insuffisante**.

### Résultat consolidé

| ID | STATUT | SIGNATURE | ANNÉES | PERSISTANCE | REPRODUCTIBILITÉ | CONFIANCE | JUSTIFICATION |
|---|---|---|---|---|---|---|---|
| **G-B** | **FINAL_REGIME** | ≈ médiane (|z| ≤ 0,3) | 2010–2026 continu | diag HMM 0.9997–0.9998 ; épisodes longs (K2 : méd. 566 628) | 8/8 configs ; silhouette 0.7911 | **HIGH** | Seul état satisfaisant les 6 critères cumulatifs ; **pas un cluster résiduel** (§3.1) |
| **G-E2** | **CANDIDATE_REGIME** | skew +4,72σ ; kurt +6,22σ ; spacing +1,12σ ; clust −0,85σ | 2013, 2014, 2016, 2017 (+2026 ~3 %) | diag 0.9957–0.9987 (plus faible) ; méd. ép. = 1 bar ; noyau ~22 600 ; épisodes HMM inconnus | 2 configs KM identiques + 1 HMM « approchante » (6× atténuée) | **MEDIUM** | Verdict 3.6I UNCERTAIN confirmé et clos ; récurrence + distinction établies, persistance + concordance non établies |
| **G-E0** | **EVENT** | skew −17,5σ ; kurt +30,5σ ; vr2 −2,9σ | 2015 (50 %), 2021 (50 %) | 2 épisodes ~6 sem. ; diag 0.9999 (artefact) | Identité exacte KM K2–K5 + HMM full (ARI 1.0) | **HIGH** (événement) | Récurrence non démontrée ; anomalie F3 — **ne peut pas être un régime** (règle) |
| **G-E1** | **EVENT** | low_wick +7,62σ ; body −4,22σ ; close +4,29σ ; sigma +1,5/1,6σ | 2010 (98 %), traces | diag 0.9969–0.9997 ; noyau ~27 100 | 6/6 configs K≥3, profils ~identiques | **HIGH** (structure) / MEDIUM (récurrence) | Confinement 2010 non dépassé ; bord de période + anomalies 3.6D — **ne peut pas être un régime** (règle) |
| **G-E3** | **INDETERMINATE** | vol_ratio_day +3,08σ ; h1_vol +2,46σ ; m1_ext +1,73σ | toutes années (pics 2011/2020) | diag 0.9960 ; épisodes par état inconnus | 1 seule config (HMM K5 s4) | **LOW** | Aucune preuve indépendante supplémentaire disponible (règle) |
| **G-E4** | **EXCLUDED** | storm_p90_run = 1 ; clust −0,73/−0,89σ | toutes années | 0.9987–0.9995 | 4 configs HMM, jamais K-means | **LOW** | Instabilité K (12,8–30,7 %) + quasi-constance non résolues (règle) |

---

## §6. Limites de cette validation (et ce qui n'a PAS été fait)

1. **Aucun calcul** : la validation repose intégralement sur des chiffres déjà publiés ; aucun contrôle (bootstrap, permutation, significativité, épisodes HMM par état, full-cov, validation source) n'a été exécuté — ces éléments sont explicitement hors périmètre 3.7 et **non remplacés** par une intuition.
2. **Sources incomplètes depuis la réinitialisation** : les rapports 3.6A–3.6D et les JSON bruts (`/tmp/xauusd_pilot36f*.json`) ne sont pas présents dans le workspace ; seuls 3.6F–3.6J sont exploitables. Les conclusions 3.6A–3.6D citées ici proviennent de ce qu'en rapportent 3.6F–3.6J.
3. **Incertitude résiduelle sur G-B** : sa « distinction » est une neutralité (définition par défaut) ; si la question exigeait un second comportement **actif**, la carte ne contient qu'un seul régime et doit rester sobre — c'est le sens du PROVISIONAL.
4. **Pas de classifieur, pas de stratégie** : aucun modèle de classification n'est construit ; aucune performance, aucun backtest, aucune optimisation — conformément aux interdits à toutes les étapes 3.6F–3.7.

**Conditions de sortie du PROVISIONAL (non exécutées, nécessitant explicitement de nouvelles étapes dédiées) :**
- calcul des **durées d'épisodes HMM par état** (K2–K5) ;
- **comparaison directe de partitions** KM K4/K5 vs HMM K5 (concordance G-E2) ;
- **test full-covariance** de G-E2 (robustesse) ;
- **validation source** des fenêtres G-E0 (2015/2021) et de la période G-E1 (2010) ;
- contrôles de stabilité (multi-seeds, bootstrap) et couverture annuelle quantitative ;
- puis **révision de la carte** — seule issue possible vers VALIDATED ou, si les tests réfutent G-E2, vers une carte à régime unique.

---

*Fin du rapport — Step 3.7. FINAL_REGIME_MAP = PROVISIONAL. Aucun modèle, aucun K, aucun clustering, aucun backtest, aucune stratégie, aucune optimisation, aucun calcul ; sources exclusives 3.6F–3.6J ; aucun commit, aucun push.*
