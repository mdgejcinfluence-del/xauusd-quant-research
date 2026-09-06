# PHASE 3 V2 — STEP 3.8 : FINALISATION DE LA CARTOGRAPHIE DES RÉGIMES XAUUSD 2010–2026

- **Étape** : 3.8 — finalisation (`PHASE3_V2_FINAL_REGIME_MAP.md`). **Ce document remplace la version provisoire 3.6J du même fichier** et consolide, sans changement factuel, les classifications arrêtées en 3.7.
- **Source de vérité** : uniquement les rapports Phase 3 V2 déjà produits (3.6F `REGIME_MAP_CANDIDATES`, 3.6G `REGIME_MAP_CONSOLIDATION`, 3.6H `G_E2_PROFILE`, 3.6I `G_E2_VALIDATION`, 3.6J `FINAL_REGIME_MAP` (v. provisoire), 3.7 `FINAL_REGIME_VALIDATION`). **Aucun calcul, aucun modèle, aucun K, aucun clustering, aucune feature, aucun classifieur, aucun backtest, aucune stratégie, aucune optimisation.**
- **Question centrale** : la cartographie actuelle permet-elle de définir une **carte finale** des régimes comportementaux de XAUUSD 2010–2026, avec les états correctement classés RÉGIME / CANDIDAT / EVENT-ANOMALIE / INDETERMINATE / EXCLUDED ? → **OUI**, la classification est stable depuis 3.7 et demeure intacte après vérification ; elle est finalisée ci-dessous.
- **Aucun commit, aucun push.**

---

## 1. Objective

Finaliser la cartographie comportementale XAUUSD 2010–2026 **à partir de la carte déjà construite et validée provisoirement** (3.6J → 3.7). Objectifs opérationnels :
1. reprendre et **confirmer** la classification de 3.7 (aucune révision factuelle : les preuves n'ont pas changé) ;
2. vérifier la **cohérence globale** de cette cartographie (récurrence, persistance, distinction, reproductibilité, séparation régime/événement/artefact, couverture, cohérence inter-familles) ;
3. **ne pas sauver G-E2** : statuer son rôle uniquement sur les preuves disponibles ;
4. vérifier que G-E0/G-E1 restent hors RÉGIME et que G-E3/G-E4 ne complètent pas artificiellement la carte ;
5. produire la **cartographie finale explicite**, la synthèse chronologique et le **verdict global unique**.

Rappel du critère de validation applicable (énoncé 3.8) : VALIDATED ne signifie pas que chaque observation soit parfaitement classifiée ; il suffit que **le(s) régime(s) réellement démontré(s) soient clairement identifiés**, que les **événements/anomalies soient séparés explicitement**, que les **états indéterminés soient conservés comme tels**, et que **aucune catégorie ne soit artificiellement forcée**. Une incertitude subsistante sur G-E2 doit être **conservée dans la carte**, non résolue par une nouvelle campagne.

---

## 2. Final regime map

| ID | STATUT FINAL | RÉSUMÉ COMPORTEMENTAL | PÉRIODE(S) | RÔLE DANS LA CARTE 2010–2026 |
|---|---|---|---|---|
| **G-B** | **FINAL_REGIME** | Comportement de référence : profil ≈ médiane globale (|z| ≤ 0,3 sur les 25 features) | continue 2010–2026 | **Fond de la carte** — mode dominant et continu ; tous les autres états sont des écarts circonscrits à ce mode |
| **G-E2** | **CANDIDATE_REGIME** | « Queue droite modérée, extrêmes moins agrégés » : skew +4,72σ, kurt +6,22σ, spacing +1,12σ, storm_clust −0,85σ | blocs 2013–2014 et 2016–2017 (+ résiduel 2026 ~3 %) | **Seul candidat récurrent hors référence** — incertitude conservée : persistance et concordance KM/HMM non établies |
| **G-E0** | **EVENT** | « Queue d'aplatissement extrême » : skew −17,5σ, kurt +30,5σ, vr2 −2,91σ | **2 fenêtres uniquement** : 2015-07-20→09-01 ; 2021-08-08→09-21 | **Événement / anomalie de source (règle F3)** — séparé de la carte des régimes |
| **G-E1** | **EVENT** | « Structure mèche basse / début de période » : low_wick +7,62σ, body_range −4,22σ, close_pos +4,29σ, sigma +1,55/+1,65σ | **2010 (98 %)** + traces 2011/2020/2025 | **Événement de bord de période** — structure hautement reproductible mais confinée au début du domaine |
| **G-E3** | **INDETERMINATE** | « Volatilité jour/mois élevée » : vol_ratio_day +3,08σ, h1_vol +2,46σ, m1_ext_rate +1,73σ | toutes années (pics 2011, 2020) | **Conservé indéterminé** — une seule configuration de détection, aucune preuve indépendante supplémentaire |
| **G-E4** | **EXCLUDED** | « Mois sans extrêmes cumulés » : storm_p90_run_month = 1 | toutes années (définition instable) | **Exclu** — poids instable en K (12,8–30,7 %) et dépendance à une feature quasi-constante (MAD ≈ 0) |

**Classification finale = celle de 3.7, confirmée sans révision.** La carte n'est pas enrichie artificiellement : **un seul régime démontré (G-B)** ; G-E2 candidat (incertitude conservée) ; G-E0/G-E1 événements séparés ; G-E3 indéterminé ; G-E4 exclu.

---

## 3. State-by-state classification

### 3.1 G-B → FINAL_REGIME
- **Statut / raison** : seul état satisfaisant **simultanément** présence continue 2010–2026, signature identifiable, persistance réelle, reproductibilité 8/8, distinction claire, absence d'artefact. **Ce n'est pas un cluster résiduel** : mode central homogène (|z| ≤ 0,3), vraie séparation en K=2 (silhouette 0,7911), reproduction par deux familles indépendantes (K-means **et** HMM), persistance propre (diag HMM 0,9997–0,9998), anomalies explicitement séparées (et non absorbées).
- **Période(s)** : 2010–2026, continu (seul état sans année à zéro).
- **Confiance** : **HIGH**.
- **Rôle** : fond/référence ; définit le cadre par rapport auquel tout comportement déviant est mesuré.
- **Faits clés** : 58,33–98,52 % selon K (K-means), 66,71–69,30 % (HMM) ; HMM K2 69,30 % (1 309 024 lignes) ; KM K2 98,52 % ; diag HMM 0,9997–0,9998 ; KM K2 : 3 épisodes, médiane 566 628 bars ; HMM : médianes 193–268 bars.

### 3.2 G-E2 → CANDIDATE_REGIME (rôle déterminé sur preuves disponibles, non « sauvé »)
- **Statut / raison** : **candidat conservé**, verdict 3.6I (UNCERTAIN) confirmé et clos en 3.7. Récurrence **établie** (4 années disjointes : 2013, 2014, 2016, 2017) et distinction comportementale **établie** (signature sélective sur la famille des extrêmes) ; **mais** persistance **non établie** (médiane d'épisode = 1 bar côté K-means ; diag HMM 0,9957 = plus faible de la carte ; durées HMM par état inconnues) et concordance avec HMM **non établie** (état « approchant » 6× atténué : +0,72σ vs +4,72σ ; répartition annuelle E2′ absente). Rien de réfutatoire n'existe → **ni régime confirmé, ni rejet**.
- **Période(s)** : blocs 2013–2014 (27–28 % / 18–19 % de l'état par année) et 2016–2017 (35 % / 15 %) ; résiduel 2026 (2,9–3,1 %) ; 2024 (0,7 % en K4 seulement) ; absent 2010–2012, 2015, 2018–2023, 2025.
- **Confiance** : **MEDIUM**.
- **Rôle** : seul candidat récurrent hors référence ; **ne joue pas le rôle d'un régime final** tant que persistance/concordance ne sont pas établies ; l'incertitude est une propriété **assumée** de la carte finale.
- **Faits clés** : 80 117 (KM K5, 4,24 %), 84 750 (KM K4, 4,49 %), 90 099 (HMM K5 s3 « approchant », 4,77 %) ; profils résumés KM K4/K5 identiques ; tailles à 5,5 % ; diag 0,9987 / 0,9973 / 0,9957 ; 102–219 épisodes, médiane 1, moyenne 368–832, noyau max ≈ 22 600 bars ; ARI seeds KM K4 0,885/0,885/0,9999, KM K5 0,988/0,978/0,974.

### 3.3 G-E0 → EVENT
- **Statut / raison** : **événement/anomalie**, en application de la règle (récurrence non démontrée). Le fait qu'il soit **extrêmement séparable** (ensemble identique KM K2–K5, ARI 1,0000 avec HMM full-cov K2) ne le rend pas régime : sa récurrence temporelle est **absente** (2 fenêtres seulement).
- **Période(s)** : 2015-07-20 01:36 → 2015-09-01 08:51 (13 952 bars) ; 2021-08-08 23:03 → 2021-09-21 09:57 (13 950 bars) ; 0 % ailleurs ; 27 901 lignes (1,48 %).
- **Confiance** : **HIGH** (en tant qu'événement identifié).
- **Rôle** : drapeau qualité de source (coïncide avec la règle F3 « ≥ 30 extrêmes », 3.6A) ; **hors carte des régimes** ; validation source requise avant tout usage.
- **Faits clés** : skew −9,39 (−17,5σ) ; kurtosis 420,9 (+30,5σ) ; vr2 0,896 (−2,91σ) ; storm_clust +0,95σ ; diag 0,9999 (artefact d'un état à 2 fenêtres) ; absent du HMM diag (dépend du modèle de covariance).

### 3.4 G-E1 → EVENT
- **Statut / raison** : **événement de bord de période**, en application de la règle (structure non dépassée au-delà de 2010). Très haute reproductibilité (6/6 configurations K≥3, profils quasi identiques) mais récurrence multi-années **absente**.
- **Période(s)** : 2010 **97,9–98,5 %** (début 2010-02-12 11:57) ; 2011 1,1–1,2 % ; 2020 0,4–0,5 % ; 2025 0,3–0,4 % ; 0 % ailleurs ; 85 053–88 196 lignes (4,50–4,67 %).
- **Confiance** : HIGH (structure) / MEDIUM (récurrence) → **statut EVENT**.
- **Rôle** : événement de début de domaine ; 2010 est également le lieu d'anomalies résiduelles (3.6D) → validation source requise ; **hors carte des régimes**.
- **Faits clés** : low_wick 0,378 (+7,62σ) ; body_range 0,366 (−4,22σ) ; close_pos 0,618 (+4,29σ) ; sigma +1,55/+1,65σ ; vr2 +1,70σ ; run −0,91σ ; diag 0,9969–0,9997 ; 258–266 épisodes (médiane 1, moyenne 330–332, noyau ≈ 27 100 bars).

### 3.5 G-E3 → INDETERMINATE
- **Statut / raison** : **indéterminé** — aucune preuve indépendante supplémentaire disponible dans l'existant (règle). Signature comportementale unique, mais **1 seule configuration** de détection (HMM K5 s4) ; l'étalement sur toutes les années sans seconde détection ne prouve pas la récurrence de la même structure.
- **Période(s)** : toutes années (pics 2011 21,2 % ; 2020 17,3 %) ; 79 258 lignes (4,20 %).
- **Confiance** : **LOW**.
- **Rôle** : **ne complète pas la carte** ; conservé tel quel, en attente de preuves indépendantes (hors périmètre).
- **Faits clés** : vol_ratio_day_month 1,572 (+3,08σ) ; h1_vol_ratio 1,572 (+2,46σ) ; m1_ext_rate_day 0,0271 (+1,73σ) ; ext_rate +1,25σ ; noise −0,75σ ; diag 0,9960 ; épisodes par état non calculés.

### 3.6 G-E4 → EXCLUDED
- **Statut / raison** : **exclu** — instabilité en K (30,70 % → 26,04 % → 12,79 % → 19,82 % pour K=2..5) **non résolue** et dépendance à une feature **quasi-constante** (`m3_storm_p90_run_month`, MAD ≈ 0 → fallback std, z-score non interprétable) — les deux conditions de la règle restent inchangées.
- **Période(s)** : toutes années (définition instable) ; 241 497–579 765 lignes (12,8–30,7 %).
- **Confiance** : **LOW**.
- **Rôle** : **ne complète pas la carte** ; le signal brut « niveau 1 vs 2 » reste une observation réelle, à réévaluer uniquement dans le cadre d'une revue de features (sans suppression définitive) et hors périmètre 3.8.
- **Faits clés** : storm_p90_run = 1 (vs 2) ; storm_clust −0,73/−0,89σ ; kurtosis −0,46σ ; diag 0,9987–0,9995 ; détecté HMM K2–K5 uniquement (jamais K-means).

---

## 4. Chronological map 2010–2026

> **Métrique** : les % par année sont les **répartitions des lignes de chaque état** P(année|état) publiées en 3.6F (aucun recalcul ; la proportion « part de l'année occupée par l'état » n'existe pas dans les résultats et n'est pas dérivée). La présence/absence par année est directement lisible ; G-B (référence) est présent toutes les années.

| Année | G-B (réf.) | G-E2 (cand.) | G-E1 (év.) | G-E0 (év.) | G-E3 (indét.) | G-E4 (exclu) | Lecture chronologique |
|---|---|---|---|---|---|---|---|
| **2010** | présent (1,4 % de ses lignes) | **absent** | **98 %** (début 02-12) | absent | 7,0 % | 15,0 % | **Événement G-E1** : structure mèche-basse, bord de période ; fond = G-B |
| **2011** | présent (4,9) | absent | 1,1–1,2 % | absent | **21,2 % (pic)** | 9,3 % | Pic G-E3 (volatilité jour/mois) — indéterminé, une seule détection |
| **2012** | présent (3,4) | absent | 0 | absent | 9,4 % | 12,1 % | Année dominée par G-B (état de référence) |
| **2013** | présent (8,3) | **26,7–28,2 %** | 0 | absent | 5,2 % | 0,1 % | **Ouverture du bloc G-E2 #1** (2013–2014) |
| **2014** | présent (6,1) | **18,4–19,0 %** | 0 | absent | 5,0 % | 5,0 % | Fin du bloc G-E2 #1 |
| **2015** | présent (7,4) | **absent (coupure)** | 0 | **50 %** (07-20→09-01) | 1,1 % | 2,7 % | **Événement G-E0 #1** (queue extrême, ≈ 6 semaines) ; G-E2 coupé |
| **2016** | présent (5,9) | **35,1–35,5 %** | 0 | absent | 2,7 % | 6,4 % | **Ouverture du bloc G-E2 #2** (2016–2017) |
| **2017** | présent (3,9) | **14,6–15,8 %** | 0 | absent | 1,2 % | 10,9 % | Fin du bloc G-E2 #2 |
| **2018** | présent (5,8) | absent | 0 | absent | 2,9 % | 6,7 % | Retour au fond G-B ; G-E2 absent (2018–2025) |
| **2019** | présent (5,9) | absent | 0 | absent | 5,0 % | 6,4 % | Année de référence |
| **2020** | présent (5,0) | absent | 0,4–0,5 % | absent | **17,3 % (pic)** | 8,4 % | Pic G-E3 ; trace G-E1 |
| **2021** | présent (8,3) | absent | 0 | **50 %** (08-08→09-21) | 2,4 % | 0,9 % | **Événement G-E0 #2** (queue extrême, ≈ 6 semaines) |
| **2022** | présent (7,0) | absent | 0 | absent | 1,9 % | 4,1 % | Année de référence |
| **2023** | présent (8,4) | absent | 0 | absent | 1,9 % | 0,8 % | Année de référence |
| **2024** | présent (8,6) | **0,7 % (K4 seul)** | 0 | absent | 3,4 % | 0,4 % | Première trace marginale G-E2 depuis 2017 |
| **2025** | présent (6,2) | absent | 0,3–0,4 % | absent | 7,3 % | 5,8 % | Dernière trace G-E1 (2025-12-01) ; G-E2 absent |
| **2026** | présent (3,6) | **2,9–3,1 %** | 0 | absent | 5,0 % | 4,9 % | Réapparition résiduelle G-E2 (~3 % de l'état) |

**Lecture d'ensemble** : 2010–2026 = **un fond comportemental continu (G-B)** ponctué d'**incursions épisodiques** — deux blocs candidats (G-E2 : 2013–2014, 2016–2017), deux événements-anomalies (G-E0 : 2015, 2021), un événement de début de période (G-E1 : 2010), des pics indéterminés (G-E3 : 2011, 2020). **Aucune alternance rapide ni cycle de régimes** : pas de preuve d'une séquence régulière multi-états sur la période.

---

## 5. Regime vs Event vs Indeterminate vs Excluded

### 5.1 Séparation vérifiée (aucune catégorie forcée)

| Frontière | Vérification |
|---|---|
| **RÉGIME ↔ ÉVÉNEMENT** | G-B : continu + persistant + reproductible → RÉGIME. G-E0 : séparation statistique parfaite mais **2 fenêtres** → EVENT. G-E1 : reproductibilité 6/6 mais **98 % en 2010** → EVENT. La facilité de séparation ne confère pas le statut de régime (règle 3.6J §2). |
| **CANDIDAT ↔ RÉGIME** | G-E2 : récurrence + distinction établies ; persistance + concordance KM/HMM **non établies** → CANDIDAT (incertitude conservée, rien n'a été « sauvé »). |
| **INDETERMINATE ↔ RÉGIME** | G-E3 : signature identifiable mais **1 seule configuration**, aucune preuve indépendante → INDETERMINATE (conservé tel quel, non utilisé pour enrichir la carte). |
| **EXCLUDED ↔ RÉGIME** | G-E4 : instabilité K + feature quasi-constante **non résolues** → EXCLUDED (non utilisé pour enrichir la carte). |

### 5.2 Cohérence globale avec les résultats 2010–2026

| Axe | Vérification (résultats existants) |
|---|---|
| **Récurrence temporelle** | G-B : continue (seul état sans année à 0) ✅ ; G-E2 : 4 années disjointes ✅ ; G-E0 : 2 fenêtres ❌ ; G-E1 : 1 poche (2010) ❌ ; G-E3 : étalé mais non vérifiable ❌ ; G-E4 : toutes années mais définition instable ⚠️ |
| **Persistance** | G-B : diag 0,9997–0,9998, épisodes longs ✅ ; G-E2 : 0,9957–0,9987 mais médiane épisode = 1 bar, HMM inconnu ⚠️ ; G-E0/G-E1 : diag élevé mais confinement ↔ non pertinent pour un régime ; G-E3 : 0,9960 sans épisodes ; G-E4 : 0,9987–0,9995 mais définition change avec K |
| **Distinction comportementale** | Établie pour G-B (neutralité), G-E2 (queue droite/désagrégation), G-E0 (queue gauche/agrégation), G-E1 (microstructure), G-E3 (volatilité) | G-E4 (feature discrète quasi-constante, unique mais fragile) |
| **Reproductibilité** | G-B 8/8 ✅ ; G-E1 6/6 ✅ ; G-E0 4/4 KM + 1/1 HMM full (ARI 1,0) ✅ ; G-E2 2/2 KM + 1/1 HMM approchante (6× atténuée) ⚠️ ; G-E3 1/8 ❌ ; G-E4 4/4 HMM mais 0/4 K-means ❌ |
| **Séparation régime / événement / artefact** | G-B régime ; G-E0/G-E1 événements (anomalies connues F3 / bord 2010) ; G-E4 artefact technique ; G-E3 non tranché — **aucune anomalie transformée en régime** ✅ |
| **Couverture temporelle** | G-B couvre 58,3–98,5 % (K-means) / 66,7–69,3 % (HMM) → majorité du comportement ; anomalies séparées et non forcées dans des régimes ✅ (couverture quantitative annuelle non calculée — limite §7) |
| **Cohérence entre familles de découverte** | G-B : K-means + HMM (8/8) ✅ ; G-E2 : K-means (2) + HMM approchante (1) ⚠️ ; G-E0 : K-means + HMM full (identité, ARI 1,0) mais absent du HMM diag (dépendance covariance, documentée) ; G-E1 : K-means + HMM (6/6) ✅ ; G-E3 : HMM seul ; G-E4 : HMM seul |

**Conclusion du §5** : la cartographie est **cohérente** avec l'ensemble des résultats ; la seule incertitude quantitative ouverte (G-E2) est **conservée explicitement** dans la classification, conformément à la consigne.

---

## 6. Evidence and confidence

| ID | Preuve de récurrence | Preuve de persistance | Preuve de distinction | Reproductibilité | Artefact/anomalie | Confiance |
|---|---|---|---|---|---|---|
| **G-B** | continue 2010–2026 | diag HMM 0,9997–0,9998 ; KM K2 : 3 ép., médiane 566 628 ; HMM : méd. 193–268 | ≈ médiane, |z| ≤ 0,3 — unique par neutralité ; silhouette 0,7911 (K2) | 8/8 configurations (KM + HMM) | aucune | **HIGH** |
| **G-E2** | 2013, 2014, 2016, 2017 (+2026 ~3 %) | diag 0,9987/0,9973/0,9957 ; méd. ép. 1 bar ; moyenne 368–832 ; noyau ≈ 22 600 ; HMM par état inconnu | skew +4,72σ ; kurt +6,22σ ; spacing +1,12σ ; clust −0,85σ — combinaison unique | KM K4/K5 identiques (tailles 5,5 %) ; HMM « approchante » 6× atténuée ; ARI seeds 0,885–0,9999 | non résolue (fragmentation K-means, sensibilité covariance) — **aucun artefact identifié** | **MEDIUM** |
| **G-E0** | absent (2 fenêtres) | 2 épisodes ~6 sem. ; diag 0,9999 (artefact) | skew −17,5σ ; kurt +30,5σ — exclusivement queues | identité exacte KM K2–K5 + HMM full (ARI 1,0) ; absent HMM diag | **OUI** : anomalie F3 (≥ 30 extrêmes, 3.6A) | **HIGH** (événement) |
| **G-E1** | absent (98 % 2010) | diag 0,9969–0,9997 ; noyau ≈ 27 100 bars | low_wick +7,62σ ; body −4,22σ ; close +4,29σ ; sigma +1,5/1,6σ — unique | 6/6 configurations K≥3, profils quasi identiques | **OUI** : bord de période (2010, anomalies 3.6D) | HIGH (structure) / MEDIUM (récurrence) |
| **G-E3** | non vérifiable (étalé, mono-détection) | diag 0,9960 ; épisodes par état inconnus | vol_ratio_day +3,08σ ; h1_vol +2,46σ ; m1_ext +1,73σ — unique | 1/8 configurations | aucune preuve indépendante | **LOW** |
| **G-E4** | non établie (poids 12,8–30,7 % selon K) | diag 0,9987–0,9995 (définition change avec K) | storm_p90_run = 1 ; clust −0,73/−0,89σ — partielle | 4/4 HMM, 0/4 K-means | **OUI** : feature quasi-constante (MAD ≈ 0 → fallback std) | **LOW** |

**Niveaux de confiance inchangés par rapport à 3.7** — aucune preuve nouvelle ne justifie une révision.

---

## 7. Remaining limitations

1. **G-E2 — persistance non établie** : durées d'épisodes HMM par état indisponibles (seules médianes globales 193–268 bars publiées) ; médiane K-means = 1 bar (mosaïques de frontière, limitation documentée 3.6F §7.2.6) ; noyau max ≈ 22 600 bars. → l'incertitude est **conservée** dans la carte (consigne 3.8), non résolue.
2. **G-E2 — concordance inter-familles non établie** : HMM K5 s3 « approchant » (skew +0,72σ, kurt +1,0σ vs +4,72σ/+6,22σ) ; répartition annuelle de E2′ absente ; comparaison directe de partitions non exécutée.
3. **Sensibilité au modèle de covariance** : sanity K=2 montre un changement total diag ↔ full (ARI −0,0154) ; robustesse de G-E2 au full-cov non évaluée.
4. **Validation source non faite** : fenêtres G-E0 (2015/2021, règle F3) et période G-E1 (2010, anomalies 3.6D) — audit amont requis avant tout usage (hors périmètre 3.8).
5. **Couverture temporelle quantitative absente** : seules les répartitions P(année|état) existent ; la part de chaque année occupée par chaque état n'a pas été calculée (aucun recalcul).
6. **Contrôles statistiques non exécutés** : significativité, bootstrap, ARI vs permutations — aucun n'est disponible (et aucun n'a été lancé ici).
7. **Sources brutes indisponibles** : depuis la réinitialisation de l'environnement, `/tmp/xauusd_pilot36f*.json` et rapports 3.6A–3.6D ne sont pas présents ; toutes les valeurs proviennent des rapports 3.6F–3.7 (restaurés/créés en session). Toute reproduction nécessiterait une reconstruction explicite — non effectuée.
8. **Distinction « par défaut » de G-B** : G-B est le mode dominant ; sa distinction est une neutralité (profil médian), pas un écart exceptionnel. Cette limite est assumée : G-B est le **régime de référence** de la carte, non un comportement anormal.

---

## 8. Final verdict

**Décision appliquée (critère 3.8)** : VALIDATED ne requiert pas que chaque observation soit parfaitement classifiée ; il suffit que (i) le ou les régimes réellement démontrés soient clairement identifiés, (ii) les événements/anomalies soient séparés explicitement, (iii) les états indéterminés soient conservés comme tels, (iv) aucune catégorie ne soit artificiellement forcée — et que toute incertitude subsistante (G-E2) soit **conservée dans la carte**.

| Critère 3.8 | Évaluation |
|---|---|
| Régime(s) démontré(s) clairement identifié(s) | ✅ **G-B** — seul régime démontré (continu, persistant, reproductible 8/8, non résiduel) |
| Événements/anomalies séparés explicitement | ✅ **G-E0** (anomalie F3, 2 fenêtres), **G-E1** (bord de période 2010) — hors catégorie RÉGIME |
| États indéterminés conservés comme tels | ✅ **G-E3** (INDETERMINATE), **G-E4** (EXCLUDED) — non utilisés pour enrichir la carte |
| Aucune catégorie artificiellement forcée | ✅ — aucun second régime créé ; G-E2 **CANDIDATE_REGIME** avec incertitude conservée (3.6I clos : récurrence + distinction établies, persistance + concordance non établies) |
| Aucun nouveau travail | ✅ — aucune exploration, aucun calcul, aucune donnée nouvelle ; uniquement consolidation de 3.6F–3.7 |

**Réponse à la question centrale** : oui, la cartographie actuelle permet de définir une **carte finale** avec les états correctement classés. La carte est sobre par construction : **un régime démontré, un candidat explicite, deux événements séparés, un indéterminé, un exclu**. L'incertitude sur G-E2 est une **propriété de la carte** (statut candidat), pas une lacune de la classification — elle ne requiert pas de nouvelle campagne.

**Note de cohérence avec 3.7** : 3.7 a statué PROVISIONAL en appliquant le critère plus strict de 3.6J (chaque régime retenu doit satisfaire seul tous les critères) ; 3.8 fournit explicitement le critère de validation **de la cartographie** (classification correcte, non-forcée, incertitudes conservées), qui est satisfait. Le verdict ci-dessous est donc la **décision finale** de la Phase 3 selon le critère énoncé à cette étape.

# FINAL_REGIME_MAP = VALIDATED

**Résumé de la carte finale (XAUUSD 2010–2026)** :
- **G-B** — FINAL_REGIME (référence continue, HIGH) ;
- **G-E2** — CANDIDATE_REGIME (queue droite modérée / extrêmes moins agrégés ; blocs 2013–2014, 2016–2017 ; incertitude conservée, MEDIUM) ;
- **G-E0** — EVENT (queue extrême ; 2015 et 2021 ; anomalie F3) ;
- **G-E1** — EVENT (structure mèche basse ; 2010 ; bord de période) ;
- **G-E3** — INDETERMINATE (volatilité jour/mois élevée ; pics 2011/2020 ; 1 seule détection) ;
- **G-E4** — EXCLUDED (mois sans extrêmes cumulés ; instable K + feature quasi-constante).

*Fin du rapport — Step 3.8. Aucun modèle, aucun K, aucun clustering, aucune feature, aucun classifieur, aucun backtest, aucune stratégie, aucune optimisation, aucun calcul ; sources exclusives Phase 3 V2 (3.6F–3.7) ; aucun commit, aucun push.*
