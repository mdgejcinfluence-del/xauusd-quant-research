# PHASE 3 V2 — STEP 3.9 : RAPPORT SCIENTIFIQUE ET AUDIT DES PREUVES
# CARTOGRAPHIE DES RÉGIMES XAUUSD 2010–2026

- **Étape** : 3.9 — audit scientifique et traçabilité des preuves (`PHASE3_V2_SCIENTIFIC_EVIDENCE_REPORT.md`).
- **Objet** : défendre, de façon traçable et réfutable, la cartographie finale (3.8) ; **auditer** les preuves ; **relier chaque conclusion à une preuve quantitative précise** ; **documenter le fondement scientifique des méthodes** ; **séparer preuve empirique et justification méthodologique** ; **identifier honnêtement les limites**.
- **Interdits respectés** : aucun clustering, aucun K, aucun HMM, aucune feature, aucun backtest, aucune stratégie, aucun classifieur, aucune optimisation, aucune exploration nouvelle ; **la carte finale n'est pas modifiée** ; G-E2 n'est pas promu ; la littérature n'est **jamais** utilisée comme preuve d'existence d'un régime XAUUSD.
- **Aucun calcul** : les résultats sont repris tels quels ; seuls des constats arithmétiques élémentaires (déjà publiés) sont cités.

### Source de vérité — inventaire exact du workspace

| Document cité (consigne) | Présent dans le workspace | Note |
|---|---|---|
| `PHASE3_V2_DATA_CONTRACT.md` | ✅ | Contrat données Phase 3 V2 |
| `PHASE3_V2_FEATURE_SPEC.md` | ✅ | Spec 25 features, familles, fenêtres |
| `PHASE3_V2_FEATURE_AUDIT.md` | ❌ **absent** | Le rapport d'audit comportemental (3.4/3.6A) n'est pas dans le workspace après réinitialisation ; ses conclusions ne sont utilisables qu'à travers 3.6F–3.8 |
| `PHASE3_V2_FINAL_REGIME_MAP.md` | ✅ | Carte finale (3.8) |
| `PHASE3_V2_FINAL_REGIME_VALIDATION.md` | ✅ | Validation (3.7) |
| Résultats 3.6F | ✅ via `PHASE3_V2_REGIME_MAP_CANDIDATES.md` | Chiffres bruts publiés |
| Résultats 3.6G | ✅ via `PHASE3_V2_REGIME_MAP_CONSOLIDATION.md` | Consolidation |
| Résultats 3.6H / 3.6I | ✅ `PHASE3_V2_G_E2_PROFILE.md` / `PHASE3_V2_G_E2_VALIDATION.md` | Profil + verdict UNCERTAIN |
| Résultats 3.7 / 3.8 | ✅ (ci-dessus) | PROVISIONAL → VALIDATED |
| Artefacts bruts `/tmp/xauusd_pilot36f*.json` | ❌ **absents** (reset) | Limitation majeure (§12) |

---

## 1. OBJET SCIENTIFIQUE

**Définition opérationnelle retenue (unique)** : un **régime comportemental** est un état du marché caractérisé par une **combinaison suffisamment stable de propriétés observables** — volatilité, persistance/série, excursions, structure des bougies, queues de distribution, clustering des événements extrêmes — qui (i) **persiste** au-delà de l'échelle d'une observation isolée, (ii) **réapparaît** sur plusieurs périodes temporelles distinctes, (iii) est **reproductible** par des méthodes indépendantes, et (iv) est **distinct** des autres états.

**Ce qu'un régime N'EST PAS** :
- il n'est **pas** défini par une performance de stratégie (aucun rendement, Sharpe, drawdown n'entre dans la définition) ;
- il n'est **pas** un artefact de partition (un état ne devient pas régime parce qu'un clustering le produit) ;
- il n'est **pas** un événement ponctuel (une poche historique ou une anomalie de source ne devient pas un régime par facilité de séparation) ;
- il n'est **pas** une propriété économique interprétée (aucune étiquette « hausse/panique/etc. » n'est attribuée) — les noms sont purement comportementaux (3.6F §8, 3.8 §6).

**Statut de la cartographie audité** : carte finale de 3.8 = `FINAL_REGIME_MAP = VALIDATED` (critère de classification correcte, non forcée, incertitudes conservées) ; le présent audit **ne modifie pas** cette carte et évalue la **force scientifique** des preuves qui la sous-tendent.

---

## 2. CHAÎNE DE PREUVE

> Pour chaque maillon : **preuve existante ; métrique support ; ce que cela démontre ; ce que cela NE démontre PAS.**

### 2.1 DONNÉES
- **Preuve** : `PHASE3_V2_DATA_CONTRACT.md` — grille M3 validée : **1 963 826 barres**, 2010-01-01T00:00:00Z → 2026-08-30T23:57:00Z ; compteurs d'intégrité (`n_m1`, `internal_missing`, `internal_breaks` = 0, `contig_next`) ; lignes par année (2010 364 242 … 2025 354 415 ; **2026 233 755 année partielle**) ; `VOLUME_POLICY = EXCLUDED` (jamais chargé, jamais utilisé, jamais dérivé) ; vérifications A9 (grilles reproduisent les cibles ; sinon STOP).
- **Métrique** : décompte 1 963 826 ; complétude multivariée **1 888 789 lignes** (96,179 % des barres) utilisées par 3.6F ; ~75 037 lignes exclues par masque NaN (nettoyage NON destructif, aucun NaN supprimé du parquet — 3.6A).
- **Démontre** : domaine 2010–2026 **complet en couverture** (hors 2026 partielle), intégrité d'horodatage/contiguïté contrôlée par compteurs, **exclusion explicite du volume**.
- **Ne démontre PAS** : la justesse de la convention de source (règle de pause week-end/session), ni l'absence de tout biais d'enregistrement non couvert par les compteurs ; aucune contre-vérité externe.

### 2.2 FEATURES
- **Preuve** : `PHASE3_V2_FEATURE_SPEC.md` — 25 features, fenêtres **positionnelles** `[i−W+1, i]` ; estimateurs **épinglés** (std/var ddof=1, quantiles linéaires, moments population ddof=0, Pearson pairwise) ; MIN_OBS ; familles (volatilité, série/persistance, excursions, structure bougies, queues E, extrêmes E) ; NaN gérés par masque d'exhaustivité.
- **Métriques** : 25 features consommées par 3.6F (aucune supprimée) ; reproductibilité des formules.
- **Démontre** : définitions **univoques et reproductibles** ; fenêtres à information passée ; politiques de gestion des NaN.
- **Ne démontre PAS** : que ces 25 features **suffisent** à caractériser le comportement de marché ; la **dépendance de la carte au choix des features** reste ouverte (§12) ; aucune justification d'exhaustivité.

### 2.3 VALIDATION PIT
- **Preuve** : correction d'alignement H1 « AMENDMENT 1.0/1.1 » documentée dans le moteur (`engine_version V2_STEP3.3_2_H1_AMEND1.1`) — h(t) = **dernier bucket H1 entièrement fermé** à endM1(t) = T(t)+2 ; `h_idx = searchsorted(t_h1, hb, 'right') − 1` ; w arm-up h_idx<0 → NaN ; asserts de non-violation (h1_bucket_end ≤ endM1).
- **Métrique** : asserts d'alignement ; 2 features impactées (A-3, B-6) ; les 23 autres non concernées (3.6A).
- **Démontre** : par construction, **aucune information H1 future** dans les features H1 alignées ; nécessité de l'amendement documentée par l'audit PIT (FAIL/H1 → STOP → AMEND).
- **Ne démontre PAS** : une validation PIT ré-exécutable dans ce workspace (le rapport `PHASE3_V2_H1_PIT_VALIDATION.md` est **absent** après reset) ; ni que les features soient causales au sens prédictif (elles sont descriptives ici).

### 2.4 DÉCOUVERTE DES STRUCTURES
- **Preuve** : 3.6F — K-means (K=2..5, n_init=10, max_iter=300) et HMM Gaussian **diag** (K=2..5, n_iter=50, tol=1e-4, init `stmc`), 3 seeds (0,1,2), sur X standardisé robustement (médiane/MAD, fallback std si MAD ≈ 0 sur `m3_storm_p90_run_month`) ; sanity HMM full-cov K=2.
- **Métriques** : taille des états ; silhouette (K-means) ; ARI inter-seeds.
- **Démontre** : l'existence de **partitions** (K-means) et de **modèles séquentiels** (HMM) à K fixés — rien de plus.
- **Ne démontre PAS** : le **nombre** de régimes (aucun K sélectionné, interdit) ; la « vérité » d'une partition ; aucune inférence sur la dimension latente.

### 2.5 STABILITÉ
- **Preuve** : ARI entre seeds et tailles par seed. KM K2 : ARI 1,000/1,000/1,000 ; KM K3 : 0,99998/0,99998/0,99999 ; KM K4 : 0,8854/0,8854/0,9999 ; KM K5 : 0,9881/0,9775/0,9735. HMM K2/K3/K5 : ≥ 0,99999 ; **HMM K4 : ≈0/0,99989/≈0** (seed 1 = [0;0;1;1 888 788] état unique ; seed 0 = état 3 à ligne de transition nulle).
- **Métriques** : ARI (chance-corrected), `sizes_seeds`, états dégénérés.
- **Démontre** : stabilité forte KM K2–K3 et HMM K2/K3/K5 ; **instabilité documentée de HMM K4** (solution dégénérée) et permutation partielle de seeds KM K4.
- **Ne démontre PAS** : la stabilité **au-delà** des 3 seeds testés (pas de test de significativité d'ARI — Steinley 2004 fournit la méthode, non exécutée ici) ; pas de bootstrap.

### 2.6 RÉCURRENCE
- **Preuve** : `per_year_share` (P(année | état)) et fenêtres d'épisodes (3.6F §4, §6) ; fenêtres précises E0 (2 épisodes 13 952 / 13 950 bars) ; E1 98 % 2010 ; E2 4 années ; E3 toutes années (1 configuration) ; E4 toutes années (poids instable).
- **Métriques** : répartitions annuelles par état ; nombres d'épisodes ; fenêtres temporelles.
- **Démontre** : la **présence/absence** annuelle de chaque état et la localisation des épisodes.
- **Ne démontre PAS** : la **proportion de chaque année occupée** par chaque état (P(année|état) ≠ P(état|année) ; cette métrique inverse n'a jamais été calculée — signalé en 3.6J §5/§7).

### 2.7 DISTINCTION
- **Preuve** : profils médians robustes par état (médianes brutes + z robustes = (méd_état − méd_globale)/(1,4826·MAD_globale)) ; silhouette K2 0,7911.
- **Métriques** : z robustes par feature (ex. G-E2 : skew +4,72σ, kurt +6,22σ ; G-E0 : −17,5σ/+30,5σ ; G-E1 : low_wick +7,62σ) ; silhouette.
- **Démontre** : des **signatures distinctes** dans l'espace des 25 features.
- **Ne démontre PAS** : l'**universalité** du repère (médiane/MAD globale, dépendante de l'échantillon 2010–2026) ; la **séparabilité** hors repère ; une distance statistique testée (aucun test de différence inter-états exécuté).

### 2.8 REPRODUCTIBILITÉ
- **Preuve** : répétition inter-configurations (KM K2–K5, HMM K2–K5, sanity full-cov) ; ARI inter-modèles K2 : KM vs HMM full = **1,0000** ; KM vs HMM diag = **−0,0154** ; diag vs full = **−0,0154** ; G-E2 HMM « approchant » (+0,72σ vs +4,72σ).
- **Métriques** : comptage des configurations ; ARI inter-modèles ; comparaison de profils.
- **Démontre** : G-B (8/8), G-E0 (identité KM K2–K5 + HMM full), G-E1 (6/6 K≥3) fortement reproductibles ; G-E2 (2 KM + 1 HMM atténué) partiellement.
- **Ne démontre PAS** : l'identité multi-familles de G-E2 (concordance exacte non établie) ; la **réplication indépendante** (voir §12 — résultats restaurés, pas une ré-exécution).

### 2.9 SÉPARATION ÉVÉNEMENT / RÉGIME
- **Preuve** : critère de **persistance** comme discriminant (littérature §8 ; convention interne 3.6J §2) ; anomalies documentées : règle F3 « ≥ 30 extrêmes » (E0) ; bord de période 2010 + anomalies résiduelles 3.6D (E1).
- **Métriques** : nombre de fenêtres (E0 = 2), concentration annuelle (E1 98 % 2010), localisation d'anomalie.
- **Démontre** : la classification E0/E1 = événements est **argumentée par absence de récurrence**, pas par défaut.
- **Ne démontre PAS** : que **toutes** les anomalies soient identifiées (E3 non tranché, E4 fragile) ; l'**origine exacte** des anomalies (aucune validation de source exécutée).

### 2.10 CARTOGRAPHIE FINALE
- **Preuve** : 3.7 (dossiers par état) + 3.8 (classification définitive, chronologie, matrice) : G-B FINAL_REGIME ; G-E2 CANDIDATE_REGIME ; G-E0/G-E1 EVENT ; G-E3 INDETERMINATE ; G-E4 EXCLUDED.
- **Métriques** : tableau final 3.8 §4 ; verdict critère 3.8.
- **Démontre** : une carte **classée et non forcée**, avec incertitude G-E2 **conservée**.
- **Ne démontre PAS** : qu'un **classifieur** opérationnel existe (non construit, interdit) ; qu'aucune autre structure latente non observée n'existe.

---

## 3. PREUVES EMPIRIQUES DES ÉTATS

> Dossier standard par état (A–I). Tous les nombres proviennent de 3.6F (§1–§8) / 3.6H (profil G-E2) / 3.6I (verdict) / 3.7 (dossiers) / 3.8 (classement final). Aucun recalcul.

### 3.1 G-B — comportement de référence
| Rubrique | Éléments |
|---|---|
| A. Identité | Mode central ; profil ≈ médiane globale ; identifié dans KM K2 s0, K3 s0, K4 s2, K5 s4 et HMM K2 s1, K3 s1, K4 s3, K5 s2 |
| B. Signature | Médianes ≈ médianes globales (|z| ≤ 0,3 sur les 25 features) ; ex. m3_vol_ratio_day_month 0,924 ; m3_range_sigma_day 1,061 ; m3_body_range_day 0,495 ; m3_close_pos_day 0,500 ; m3_skew_month −0,100 ; m3_kurtosis_month 21,6 ; m3_storm_p90_run_month = 2 ; m3_ext_spacing_month = 12 |
| C. Récurrence | **Continue 2010–2026** ; P(année|état) jamais nulle : 2010 1,4 ; 2011 4,9 ; 2012 3,4 ; 2013 8,3 ; 2014 6,1 ; 2015 7,4 ; 2016 5,9 ; 2017 3,9 ; 2018 5,8 ; 2019 5,9 ; 2020 5,0 ; 2021 8,3 ; 2022 7,0 ; 2023 8,4 ; 2024 8,6 ; 2025 6,2 ; 2026 3,6 (%) |
| D. Persistance | diag HMM 0,9997–0,9998 ; KM K2 : 3 épisodes, médiane 566 628 bars ; HMM : médianes globales 193–268 bars ; diag KM 1,0000 (K2) / 0,9999 (K3) / 0,9998 (K4) / 0,9825 (K5, fragmentation) |
| E. Distinction | **Neutralité unique** : seule signature sans écart discriminant ; tous les autres états sont des écarts circonscrits |
| F. Reproductibilité | **8/8 configurations** (KM K2–K5 + HMM K2–K5) ; ARI seeds ≥ 0,974 ; silhouette K2 0,7911 (avec E0) |
| G. Régime/événement/artefact | **Régime** — aucune dépendance à un artefact identifié ; non confondu avec un cluster résiduel (3.7 §3.1, 6 arguments) |
| H. Confiance | **HIGH** |
| I. Limites | Distinction **par défaut** (centralité) ; silhouette 0,7911 partiellement portée par l'outlier E0 (caveat Rousseeuw, §8) ; la métrique P(année|état) ne mesure pas l'occupation annuelle |

### 3.2 G-E2 — queue droite modérée, extrêmes moins agrégés
| Rubrique | Éléments |
|---|---|
| A. Identité | KM K4 s1 (84 750 ; 4,49 %), KM K5 s0 (80 117 ; 4,24 %), HMM K5 s3 « approchant » (90 099 ; 4,77 %) |
| B. Signature | skew **+4,72σ** (+2,43) ; kurt **+6,22σ** (101,1) ; ext_spacing **+1,12σ** (18) ; storm_clust **−0,85σ** (0,297) ; ext_rate −0,52σ (0,0148) ; run −0,46σ (1,909) ; sigma −0,31σ ; 20/25 features |z| ≤ 0,52 |
| C. Récurrence | 2013 26,7–28,2 % ; 2014 18,4–19,0 % ; 2016 35,1–35,5 % ; 2017 14,6–15,8 % ; 2026 2,9–3,1 % ; 2024 0–0,7 % ; absent 2010–2012, 2015, 2018–2023, 2025 |
| D. Persistance | diag KM K4 **0,9987** / KM K5 **0,9973** / HMM K5 **0,9957** (la plus faible de la carte) ; 102–219 épisodes, **médiane 1**, moyenne 368–832, max ≈ 22 600 bars (noyau) ; **durées HMM par état inconnues** |
| E. Distinction | Combinaison unique (queues droites modérées + désagrégation des extrêmes) ; différente de E0 (gauche extrême, agrégation ↑), E1 (bougies/sigma ↑), E3 (volatilité ↑), E4 (feature quasi-constante) |
| F. Reproducibilité | KM K4/K5 : profils résumés identiques, tailles à 5,5 % ; ARI seeds 0,885/0,885/0,9999 (K4), 0,988/0,978/0,974 (K5) ; **HMM : approchant mais 6× atténué** (skew +0,72σ, kurt +1,0σ) et répartition annuelle E2′ **indisponible** |
| G. Régime/événement/artefact | Ni événement (récurrence), ni artefact identifié — mais **sensibilité non testée** à la fragmentation (médiane épisode = 1) et au modèle de covariance |
| H. Confiance | **MEDIUM** (3.6I : UNCERTAIN → 3.7 : CANDIDATE_REGIME) |
| I. Limites | Persistance non établie ; concordance inter-familles non établie (6× atténué) ; fragmentation K-means ; aucun full-cov testé |

### 3.3 G-E0 — queue d'aplatissement extrême
| Rubrique | Éléments |
|---|---|
| A. Identité | KM K2 s1 / K3 s1 / K4 s3 / K5 s2 (même ensemble) ; HMM full K2 (ARI 1,0000) ; absent du HMM diag |
| B. Signature | skew −9,39 (**−17,5σ**) ; kurt 420,9 (**+30,5σ**) ; vr2 0,896 (−2,91σ) ; storm_clust 0,389 (+0,95σ) ; ext_spacing 10 (−0,67σ) ; autres |z| < 0,7 |
| C. Récurrence | **2 fenêtres seulement** : 2015-07-20 01:36→09-01 08:51 (13 952 bars) ; 2021-08-08 23:03→09-21 09:57 (13 950 bars) ; 0 % ailleurs |
| D. Persistance | diag 0,9999 (artefact d'un état quasi absorbant à 2 fenêtres) ; durées ~6 semaines chacune |
| E. Distinction | Définie exclusivement par des queues extrêmes ; signature la plus extrême de l'étude |
| F. Reproducibilité | **Parfaite** : ensemble identique à travers 4 configurations KM + identité exacte HMM full (ARI 1,0000) ; mais **dépendante du modèle de covariance** (absent du diag) |
| G. Régime/événement/artefact | **Événement/anomalie** : coïncide avec règle F3 « ≥ 30 extrêmes » (3.6A) ; absence de récurrence |
| H. Confiance | **HIGH en tant qu'événement** (ZÉRO en tant que régime) |
| I. Limites | 2 occurrences → aucune inférence de récurrence possible ; origine exacte non validée (validation source jamais exécutée) |

### 3.4 G-E1 — structure mèche basse / début de période
| Rubrique | Éléments |
|---|---|
| A. Identité | KM K3 s2, K4 s2, K5 s1 ; HMM K3 s2, K4 s2, K5 s1 |
| B. Signature | low_wick 0,378 (**+7,62σ**) ; body_range 0,366 (**−4,22σ**) ; close_pos 0,618 (**+4,29σ**) ; range/tr_sigma **+1,55/+1,65σ** ; vr2 1,038 (+1,70σ) ; run −0,91σ ; acf1 +0,56σ |
| C. Récurrence | **2010 : 97,9–98,5 %** ; 2011 1,1–1,2 % ; 2020 0,4–0,5 % ; 2025 0,3–0,4 % ; 0 % ailleurs ; départ 2010-02-12 11:57 ; dernier épisode 2025-12-01 |
| D. Persistance | diag 0,9969–0,9997 ; 258–266 épisodes (médiane 1, moyenne 330–332, noyau ≈ 27 100 bars) |
| E. Distinction | Combinaison microstructure unique (mèche basse, corps réduit, clôture haute, sigma élevé) |
| F. Reproducibilité | **6/6 configurations K≥3** ; profils quasi identiques (low_wick +7,62 vs +7,56 vs +7,63 ; body −4,22 vs −4,17 vs −4,22 ; close +4,29 vs +4,27 vs +4,29) |
| G. Régime/événement/artefact | **Événement de bord de période** : confinement 2010 + anomalies résiduelles 3.6D sur 2010 ; pas de récurrence multi-années |
| H. Confiance | **HIGH (structure) / MEDIUM (récurrence)** → EVENT |
| I. Limites | La reproductibilité 6/6 ne compense pas l'absence de récurrence ; validation source 2010 non exécutée |

### 3.5 G-E3 — volatilité jour/mois élevée
| Rubrique | Éléments |
|---|---|
| A. Identité | HMM K5 s4 uniquement (79 258 ; 4,20 %) |
| B. Signature | vol_ratio_day_month 1,572 (**+3,08σ**) ; h1_vol_ratio 1,572 (**+2,46σ**) ; m1_ext_rate_day 0,0271 (**+1,73σ**) ; ext_rate +1,25σ ; noise −0,75σ ; up_wick −0,49σ |
| C. Récurrence | Toutes années (pics 2011 21,2 % ; 2020 17,3 %) — mais **une seule configuration** : la récurrence n'est pas vérifiable |
| D. Persistance | diag 0,9960 ; épisodes par état **non calculés** |
| E. Distinction | Signature unique (volatilité intra-jour nettement au-dessus de la normale mensuelle) |
| F. Reproducibilité | **1/8 configurations** — non établie |
| G. Régime/événement/artefact | Indéterminé (pas de preuve indépendante, pas d'artefact identifié) |
| H. Confiance | **LOW** |
| I. Limites | Mono-configuration ; aucune preuve indépendante supplémentaire disponible dans l'existant |

### 3.6 G-E4 — mois sans extrêmes cumulés
| Rubrique | Éléments |
|---|---|
| A. Identité | HMM K2 s0, K3 s0, K4 s0 (fragmenté), K5 s0 (fragmenté) ; jamais retrouvé par K-means |
| B. Signature | storm_p90_run_month **= 1** (vs 2 partout ailleurs) ; storm_clust −0,73/−0,89σ ; kurt −0,46σ ; spacing +0,45/+0,67σ |
| C. Récurrence | Toutes années (2010 15,0 %) — mais **poids instable en K** |
| D. Persistance | diag 0,9987–0,9995 (définition change avec K) ; épisodes par état non calculés |
| E. Distinction | Partielle — portée par une **feature quasi-constante** (MAD ≈ 0 → fallback std ; z interprétation invalide) |
| F. Reproducibilité | 4 configurations HMM mais **0/4 K-means** — non établie inter-familles |
| G. Régime/événement/artefact | **Artefact technico-définitionnel** : instabilité K (12,79–30,70 % selon K) + quasi-constance non résolues |
| H. Confiance | **LOW** |
| I. Limites | Signal brut « niveau 1 vs 2 » réel mais non exploitables en régime sans traitement de la feature (interdit) ; le statut EXCLUDED est conservé |

---

## 4. CAS G-B

**Pourquoi G-B peut être considéré comme régime de référence :**

| Preuve | Valeur | Ce qu'elle apporte |
|---|---|---|
| Silhouette K-means K2 | **0,7911** | Mesure de séparation globale de la partition 2 états (avec E0) — voir caveat §8 (outlier) |
| Reproduction inter-seed | ARI 1,000/1,000/1,000 (KM K2) ; ≥ 0,974 toutes configurations | Partition identique quel que soit le seed |
| Reproduction inter-familles | **8/8 configurations** (K-means + HMM, K2–K5) | La structure ne dépend pas d'une famille de modèles |
| Transition diagonale | **0,9997–0,9998** (HMM K2–K5) ; 1,0000 (KM K2) | Forte auto-persistance |
| Présence continue | 2010–2026, P(année|état) jamais nulle | Récurrence maximale (par construction) |
| Distinction | |z| ≤ 0,3 ; profil = médiane | Neutralité centrale — distinction par défaut |
| Épisodes | KM K2 : 3 épisodes, médiane 566 628 ; HMM : 193–268 | Pas une mosaïque d'un bar |

**Limite conceptuelle (explicitée, non exagérée)** : G-B est le **régime de référence dominant** ; sa distinction repose **en partie** sur son caractère **central/neutre** (profil ≈ médiane de l'échantillon). Il s'agit d'une neutralité **par construction**, pas d'une signature positive. De plus, la silhouette K2 = 0,7911 est **en partie portée par l'outlier E0** (voir §8, caveat Rousseeuw : « une structure forte peut venir d'un unique outlier ») ; elle ne prouve pas que G-B soit séparé de G-E2/G-E3/G-E4 (non testé en K2). **Conclusion : la preuve de G-B = récurrence continue + persistance + reproductibilité 8/8 + non-artefact — suffisante pour le statut FINAL_REGIME, insuffisante pour affirmer une « structure de séparation interne » riche.**

---

## 5. CAS G-E2

**Présentation exacte selon le dossier de preuve :**

1. **Récurrence multi-années — ÉTABLIE** : 2013 (26,7–28,2 %), 2014 (18,4–19,0 %), 2016 (35,1–35,5 %), 2017 (14,6–15,8 %) ; 2 blocs disjoints 2013–2014 et 2016–2017 ; résiduel 2026 (2,9–3,1 %).
2. **Signature — principalement liée aux queues de distribution** : skew +4,72σ, kurtosis +6,22σ (famille E), avec accompagnement désagrégation des extrêmes (clust −0,85σ, spacing +1,12σ, ext_rate −0,52σ). Volatilité (|z| ≤ 0,31), bougies (|z| ≤ 0,18), directionnalité (|z| ≤ 0,46) ≈ référence.
3. **Reproduction dans plusieurs configurations K-means — OUI** : KM K4 s1 (84 750) et KM K5 s0 (80 117), profils résumés identiques, tailles à 5,5 %, répartitions annuelles superposées ; ARI seeds K5 0,988/0,978/0,974 (K4 0,885 — permutation de seeds, documentée).
4. **Configuration HMM approchante — OUI mais atténuée** : HMM K5 s3 (90 099 ; 4,77 %) avec storm_clust −0,87σ (même sens) mais skew +0,72σ / kurt +1,0σ (**≈ 6× plus faibles**) et traits `run` / `vr2` de sens opposés ; répartition annuelle E2′ **indisponible**.
5. **Limites sur la persistance** : médiane d'épisode K-means = **1 bar** (mosaïques de frontière) ; diag HMM 0,9957 = **la plus faible de la carte** ; durées HMM par état **inconnues** ; seul noyau max ≈ 22 600 bars et moyenne 368–832 attestent une continuité partielle.
6. **Limites sur la concordance inter-familles** : la concordance est **de famille** (direction des queues + désagrégation) mais **pas identitaire** (intensité 6× plus faible) ; aucune mesure de chevauchement de labels KM/HMM n'existe.
7. **Limites liées à la fragmentation** : médiane 1 bar → impossible de distinguer « régime entrecoupé » de « frontière de partition » sans statistiques d'épisodes HMM.
8. **Limites liées à la covariance** : sanity K2 montre que la structure peut changer **totalement** entre diag et full (ARI −0,0154) ; aucune évaluation full-cov de G-E2 n'a été faite.

**Conclusion obligatoire (conservée) : G-E2 reste CANDIDATE_REGIME.** Il n'est **pas** promu FINAL_REGIME : récurrence et distinction sont établies, mais persistance et concordance inter-familles **ne sont pas établies** — exactement le verdict 3.6I (UNCERTAIN) confirmé en 3.7.

---

## 6. CAS G-E0 ET G-E1

**Leur séparation en événements/anomalies est scientifiquement plus défendable qu'une conversion artificielle en régimes** — pour trois raisons formelles :

**(a) Le critère de régime est la persistance, pas la séparation.** La littérature méthodologique distingue explicitement « structural outlier » (observation isolée ou courte séquence violant les patterns stables) et « regime change » (transition persistante affectant un segment soutenu) — la **persistance est le discriminant formel** [1](https://doi.org/10.3390/e28070724). G-E0 : 2 fenêtres de ~6 semaines → séquence courte, pas un segment soutenu récurrent. G-E1 : 98 % concentrés sur une seule année → pas de récurrence.

**(b) La facilité de séparation n'implique pas la récurrence.** G-E0 est le candidat le plus **séparable** de l'étude (identité exacte KM K2–K5 + HMM full-cov, ARI 1,0000 ; silhouette K2 0,7911) ; G-E1 est le plus **reproductible** (6/6 configurations, profils quasi identiques). Or, précisément, Rousseeuw (1987) avertit qu'une **structure de clustering forte peut être produite par un seul point/objet extrême** — la silhouette mesure la qualité d'adéquation à une partition, pas la récurrence temporelle [3](https://wis.kuleuven.be/stat/robust/papers/publications-1987/rousseeuw-silhouettes-jcam-sciencedirectopenarchiv.pdf). Un événement « parfaitement séparable » est un **cas d'école d'événement**, pas un régime.

**(c) Les deux candidats sont associés à des anomalies documentées.**
- **G-E0** : deux fenêtres (2015-07-20→09-01 ; 2021-08-08→09-21) ; concentration extrême (50 % de l'état par fenêtre, 27 901 lignes = 1,48 %) ; anomalie **F3 « ≥ 30 extrêmes »** documentée en 3.6A (mentionnée dans 3.6F §6.6/§8.2) ; profil −17,5σ/+30,5σ (queue extrême unique). → **EVENT / ANOMALY**.
- **G-E1** : 98 % en 2010 ; localisation temporelle au **début du domaine** (2010-02-12 11:57) ; lien avec les anomalies résiduelles de bord de période (3.6D, mentionné 3.6F §8.2) ; cela n'exclut pas un comportement réel, mais **le confine** — sans récurrence, il ne passe pas le critère de régime. → **EVENT / ANOMALY**.

**Conclusion : les deux statuts EVENT sont ceux qui maximisent la défendabilité scientifique** — ils reconnaissent la force de la structure (reproductibilité) sans la sur-interpréter (récurrence absente).

---

## 7. G-E3 ET G-E4

**G-E3 (INDETERMINATE) — pourquoi ne pas le promouvoir :**
- **Faible reproductibilité** : 1 seule configuration sur 8 (HMM K5 s4) ; aucun équivalent K-means.
- **Absence de preuve indépendante** : aucune seconde détection n'existe dans les résultats ; la présence toutes années est **non vérifiable** comme récurrence de la *même* structure (une seule réalisation).
- **Sans preuve indépendante supplémentaire disponible** (règle de la consigne), le statut INDETERMINATE est la seule position honnête ; la signature (volatilité +3,08σ/+2,46σ) est réelle et distingue l'état, mais ne suffit pas.

**G-E4 (EXCLUDED) — pourquoi ne pas le promouvoir :**
- **Instabilité selon K** : 30,70 % (K2) → 26,04 % (K3) → 12,79 % (K4) → 19,82 % (K5) — le « même » état change de taille d'un facteur ≈ 2,4 ; la partition n'est pas stable en K (et **aucun K n'est sélectionné** par principe).
- **Jamais retrouvé par K-means** : la reproductibilité inter-familles est nulle (0/4).
- **Feature quasi-constante / MAD ≈ 0** : `m3_storm_p90_run_month` a un MAD global ≈ 0 → fallback std ; le z-score publié (−2,35σ) est **non interprétable** ; seule la valeur discrète (1 vs 2) est fiable — une feature quasi-constante ne peut pas porter seule la définition d'un régime.
- **Faible fiabilité** : statut EXCLUDED conservé (règle : reste EXCLUDED tant que l'instabilité K et la quasi-constance ne sont pas résolues — aucune résolution n'a été tentée, et toute tentative nécessiterait un traitement de features interdit).

**Conclusion : INDETERMINATE / EXCLUDED — aucun des deux ne doit compléter artificiellement la carte.**

---

## 8. FONDEMENT SCIENTIFIQUE DES MÉTHODES

> **Recherche bibliographique STRICTEMENT méthodologique.** La littérature est utilisée pour justifier **des méthodes**, jamais pour prouver l'existence d'un régime XAUUSD. Chaque source est notée par type (peer-reviewed / preprint / documentation / secondaire).

### 8.1 Table MÉTHODE → MESURE → PERTINENCE → LIMITATION → NON-CONCLUSION

| Méthode | Ce qu'elle mesure | Pourquoi pertinente | Limitation | Ce qu'elle ne permet pas de conclure |
|---|---|---|---|---|
| **HMM Gaussian (diag/full)** | Distribution conjointe des observations conditionnée à un état latent + dynamique markovienne | Modélise des états latents séquentiels et leur persistance — cadre standard des régimes financiers [2](https://doi.org/10.3390/jrfm13120311) | EM converge vers un optimum local ; sensibilité à l'initialisation ; covariance diag = indépendance conditionnelle forte ; K non choisi | Que les états HMM soient des « régimes » au sens économique ou que K soit correct |
| **K-means** | Partition par centroïdes minimisant la variance intra-cluster (espace euclidien) | Découverte non séquentielle, complémentaire au HMM ; point de départ standard | Lloyd converge vers un minimum local ; pas de notion de temps ; dépend de l'échelle | Que la partition soit une structure temporelle persistante ; que K soit vrai |
| **Standardisation robuste (médiane/MAD)** | Localisation/dispersion robustes aux queues | Les 25 features ont des queues extrêmes (skew/kurt) ; la moyenne/σ seraient dominées par E0 | MAD ≈ 0 pour features quasi-constantes → fallback std (utilisé, documenté) | Que le z robuste soit interprétable lorsque MAD ≈ 0 (non : G-E4) |
| **Silhouette** | Adéquation moyenne d'un point à son cluster vs à son voisin le plus proche | Évalue la **qualité de séparation** d'une partition donnée [3](https://wis.kuleuven.be/stat/robust/papers/publications-1987/rousseeuw-silhouettes-jcam-sciencedirectopenarchiv.pdf) | Une structure forte peut venir d'**un seul outlier** ; ne mesure pas la récurrence ; dépend de K (décroît avec K) | Que la silhouette désigne un « bon » nombre de clusters ou des régimes ; aucun K retenu par score |
| **Adjusted Rand Index** | Accord de partitions corrigé du hasard (≥ 0 = chance ; 1 = identité) | Quantifie la **stabilité inter-seeds** et la **concordance inter-modèles** [1](https://www.semanticscholar.org/paper/Properties-of-the-Hubert-Arabie-adjusted-Rand-Steinley/b318a6411a9ec5a44ab982659b6344a549945021) | Ne renseigne que l'accord d'étiquettes ; la significativité exige un test (méthode Steinley 2004, non exécutée) ; sensible aux tailles déséquilibrées | Que deux partitions ARI=1 soient « vraies » ; que ARI=0 soit « pas de structure » |
| **Matrice de transition (diag.)** | Probabilité de rester dans l'état (persistance) | Interprétation directe des régimes persistants (cadre Hamilton/Markov-switching) [2](https://researchdatabase.minneapolisfed.org/downloads/6t053g06m?locale=es) | Hypothèse **d'indépendance de durée** (probabilité constante, pas de dépendance à l'âge de l'épisode) ; diag K-means = labels durs biaisés par fragmentation | Que la persistance soit stable dans le temps ou indépendante de la durée |
| **Longueurs d'épisodes (médiane/max)** | Durée des séjours contigus | Distingue « état persistant » de « mosaïque de frontières » | Médiane K-means = **1 bar** (fragmentation) ; les durées HMM par état sont **absentes** | Que G-E2 soit un régime soutenu (non établi) |
| **Répartition annuelle par état** | P(année | état) | Lisible pour la **présence/absence** et la localisation | P(année|état) ≠ P(état|année) : ne donne pas l'occupation de chaque année | Des proportions d'occupation annuelle (jamais calculées) |
| **Fenêtres positionnelles [i−W+1, i] + PIT** | Information passée uniquement | Évite le look-ahead (nécessaire pour des features causales) [1](https://arxiv.org/html/2512.12924v1) ; purged CV comme cadre plus large [3](https://en.wikipedia.org/wiki/Purged_cross-validation) | La discipline d'information ne garantit pas la pertinence prédictive ; aucune validation PIT reproductible ici (rapport absent) | Que les features soient causales au sens économétrique |
| **Critère persistance vs événement** | Structure soutenue vs séquence courte | Discriminant formel entre changement de régime et outlier structurel [1](https://doi.org/10.3390/e28070724) ; événements uniques (visités une fois) [2](https://www.nature.com/articles/s41598-021-03526-y) | Décision dépend du seuil interprété (2 fenêtres / 98 % 2010) ; subjectivité du seuil | Que tous les événements soient détectés (E3/E4 non tranchés) |

### 8.2 Sources utilisées et leur portée exacte

| Source | Type | Utilisation | **Ce qu'elle ne prouve PAS** |
|---|---|---|---|
| Rousseeuw, P.J. (1987), *Silhouettes*, J. Comput. Appl. Math. 20:53–65 [3](https://wis.kuleuven.be/stat/robust/papers/publications-1987/rousseeuw-silhouettes-jcam-sciencedirectopenarchiv.pdf) | Peer-reviewed (méthode primaire) | Justifie l'interprétation de la silhouette et le caveat « single far outlier » | Rien sur XAUUSD ; n'implique pas que K2 soit le vrai nombre |
| Hubert & Arabie (1985) ; Steinley (2004), *Properties of the Hubert–Arabie ARI*, Psychological Methods 9(3):386–396 [1](https://www.semanticscholar.org/paper/Properties-of-the-Hubert-Arabie-adjusted-Rand-Steinley/b318a6411a9ec5a44ab982659b6344a549945021) | Peer-reviewed (méthode primaire) | Justifie l'ARI comme mesure d'accord corrigée du hasard ; note l'existence d'un test de significativité | Que nos ARI soient significatifs (test non exécuté) |
| Hamilton (1989), *A New Approach to the Economic Analysis of Nonstationary Time Series*, via Durland & McCurdy (1994) [2](https://researchdatabase.minneapolisfed.org/downloads/6t053g06m?locale=es) | Peer-reviewed (méthode primaire) | Cadre Markov-switching, persistance via transition probabilities ; rappelle l'hypothèse de durée indépendante | Que nos matrices s'appliquent à des inconnues de durée |
| *Regime-Switching Factor Investing with HMM*, J. Risk Financial Manag. 13(12):311 [2](https://doi.org/10.3390/jrfm13120311) | Peer-reviewed (application) | Montre l'usage standard de HMM pour régimes de marché — **méthodologique uniquement** | **N'établit aucun régime XAUUSD** (porte sur S&P 500, avec stratégie — hors périmètre) |
| *Rule-Based Detection of Structural Outliers…*, Entropy 28(7):724 [1](https://doi.org/10.3390/e28070724) | Peer-reviewed | Distinction formelle outlier structural vs changement de régime (persistance) | Rien sur XAUUSD |
| *Model-free detection of unique events in time series*, Sci. Rep. 11 [2](https://www.nature.com/articles/s41598-021-03526-y) | Peer-reviewed | Notion d'événement unique / état visité une fois | Rien sur XAUUSD |
| Walk-forward / information set discipline [1](https://arxiv.org/html/2512.12924v1) ; Purged CV (López de Prado) [3](https://en.wikipedia.org/wiki/Purged_cross-validation) | Préprint / documentation | Justifie la discipline PIT de la chaîne (information passée) | Que la description PIT soit reproductible ici (rapport absent) |
| Notes EM / k-means multi-restarts [1](https://medium.com/@gurupatil327/introduction-to-em-algorithm-in-ml-dfe2f1ea079c) [2](https://www.numberanalytics.com/blog/7-key-tips-em-algorithm-mixture-models) [3](https://medium.com/@jimcanary/mastering-mixture-models-a-detailed-exploration-of-gaussian-mixture-models-39cf3a3a0fe3) | **Secondaires (blogs)** — utilisées uniquement pour rappeler des propriétés standard (EM → optimum local, multi-starts recommandés) | Justifie le protocole multi-seeds | Aucune ; pas une autorité méthodologique primaire |
| Documentation primaire de bibliothèques (n_init=10 par défaut dans scikit-learn ; hmmlearn EM) | Documentation | Justifie le réglage standard multi-restarts utilisé | Aucune |

**Note de transparence** : les sources secondaires (blogs, stackoverflow-type) ne sont citées que comme rappel de propriétés standards, **jamais** comme preuve ; les conclusions empiriques de ce rapport ne dépendent que des résultats 3.6F–3.8.

---

## 9. MATRICE « PREUVE / CONCLUSION »

> **Aucune conclusion sans preuve correspondante.** Niveau = force (voir §11).

| Conclusion | Preuve XAUUSD | Mesure | Niveau | Limitation |
|---|---|---|---|---|
| G-B est récurrent | P(année|état) jamais nulle 2010–2026 | répartition annuelle | **HIGH** | P(année|état) ≠ occupation ; 2026 partielle |
| G-B est distinct | profil |z| ≤ 0,3 ; nette différence avec signatures E0/E1/E2/E3 | z-robustes, profils | **MEDIUM** | Distinction par neutralité (défaut), pas par excès |
| G-B est reproductible | 8/8 configurations ; ARI seeds ≥ 0,974 | comptage configs, ARI | **HIGH** | 3 seeds seulement |
| G-B persiste | diag HMM 0,9997–0,9998 ; KM K2 3 épisodes méd. 566 628 | matrice de transition, épisodes | **HIGH** | Durée-indépendance (Hamilton) |
| G-E2 est récurrent mais non confirmé | 4 années disjointes (2013/2014/2016/2017) ; 2 blocs | répartition annuelle | **HIGH** (récurrence) / **NOT ESTABLISHED** (persistance, concordance) | épisodes HMM absents ; E2′ atténué 6× |
| G-E0 est événementiel | 2 fenêtres exactes ; 0 % ailleurs ; anomalie F3 | fenêtres, répartition, ancrage anomalie | **HIGH** | validation source non faite |
| G-E1 est événementiel | 98 % 2010 ; traces < 1,5 % ; 6/6 reproduction | répartition annuelle | **HIGH** (confinement) | 2010 = bord de domaine, cause non isolée |
| G-E3 est indéterminé | 1/8 configurations ; aucune preuve indépendante | comptage configs | **HIGH** (statut) — preuve de structure **LOW** | absence de donnée, pas preuve négative |
| G-E4 est exclu | poids 12,79–30,70 % selon K ; 0/4 K-means ; MAD ≈ 0 | tailles multi-K, comptage, MAD | **HIGH** (statut) | signal « 1 vs 2 » réel, inexploitable en régime |
| K=4 HMM est instable | seed 1 → [0;0;1;1 888 788] ; seed 0 → état ligne nulle | sizes_seeds, états dégénérés | **HIGH** | pas d'explication de la cause (init/EM) |

---

## 10. MATRICE « PREUVE EMPIRIQUE » vs « JUSTIFICATION MÉTHODOLOGIQUE »

> Deux colonnes conceptuellement séparées. **Aucune ligne ne peut être lue comme « la littérature prouve le régime ».**

| # | PREUVE EMPIRIQUE XAUUSD (résultats 3.6F–3.8) | JUSTIFICATION SCIENTIFIQUE DE LA MÉTHODE (littérature — indépendante de XAUUSD) |
|---|---|---|
| 1 | 1 888 789 lignes × 25 features ; K-means + HMM K=2..5 ; silhouette 0,7911 (K2) ; ARI inter-seeds ; profils z ; transitions ; épisodes ; P(année|état) | Silhouette : mesure d'adéquation/séparation d'une partition [3](https://wis.kuleuven.be/stat/robust/papers/publications-1987/rousseeuw-silhouettes-jcam-sciencedirectopenarchiv.pdf) ; ARI : accord corrigé du hasard [1](https://www.semanticscholar.org/paper/Properties-of-the-Hubert-Arabie-adjusted-Rand-Steinley/b318a6411a9ec5a44ab982659b6344a549945021) |
| 2 | G-B : 8/8 configurations, diag 0,9997–0,9998, continu 2010–2026 | Markov-switching : la persistance se lit dans les probabilités de transition, avec hypothèse de durée indépendante [2](https://researchdatabase.minneapolisfed.org/downloads/6t053g06m?locale=es) ; HMM = cadre standard d'états latents de marché [2](https://doi.org/10.3390/jrfm13120311) |
| 3 | G-E0 : 2 fenêtres ; G-E1 : 98 % 2010 → EVENT | Outlier structural vs changement de régime : le discriminant est la **persistance** [1](https://doi.org/10.3390/e28070724) ; l'unicité temporelle définit l'événement [2](https://www.nature.com/articles/s41598-021-03526-y) |
| 4 | G-E2 : récurrence 4 années, signature queues, concordance HMM 6× atténuée → CANDIDATE | La reproduction inter-modèles est mesurée par ARI [1](https://www.semanticscholar.org/paper/Properties-of-the-Hubert-Arabie-adjusted-Rand-Steinley/b318a6411a9ec5a44ab982659b6344a549945021) ; l'accord ne vaut pas validation de persistance (Hamilton) [2](https://researchdatabase.minneapolisfed.org/downloads/6t053g06m?locale=es) |
| 5 | Fenêtres positionnelles [i−W+1, i], H1 fermé (AMEND 1.1) ; volume exclu | Discipline d'information (pas de look-ahead) [1](https://arxiv.org/html/2512.12924v1) ; purged CV comme cadre de validation temporelle [3](https://en.wikipedia.org/wiki/Purged_cross-validation) |
| 6 | Multi-seeds (0,1,2) ; n_init=10 ; sanity full-cov | Multi-init standard contre les optima locaux (EM/k-means) [1](https://medium.com/@gurupatil327/introduction-to-em-algorithm-in-ml-dfe2f1ea079c) [2](https://www.numberanalytics.com/blog/7-key-tips-em-algorithm-mixture-models) (sources secondaires) |

**Règle de lecture** : colonne gauche = faits XAUUSD (seuls invoqués pour la carte) ; colonne droite = pourquoi les outils utilisés sont légitimes en général (aucune assertion d'existence d'un régime).

---

## 11. NIVEAU DE FORCE DES PREUVES — ÉCHELLE ET CRITÈRES

| Niveau | Critères d'attribution | Exemples |
|---|---|---|
| **HIGH** | Preuve quantitative directe + répétition ≥ 2 familles/conjectures + absence d'artefact connu + critère (récurrence ou persistance) mesuré | G-B récurrent/persistant/reproductible ; G-E0 événementiel ; G-E1 confiné 2010 |
| **MEDIUM** | Preuve quantitative directe + répétition partielle + un critère essentiel non mesuré | G-E2 récurrent + distinct, mais persistance et concordance inter-familles non établies ; G-B distinct (neutralité) |
| **LOW** | Preuve de structure existante mais mono-configuration, ou dépendance à une mesure fragile | G-E3 (1/8) ; G-E4 (instabilité K + MAD≈0) |
| **NOT ESTABLISHED** | Le critère demandé n'est pas mesuré par les résultats existants | Persistance de G-E2 (durées HMM par état) ; récurrence de G-E3 ; distinction G-E2 vs E2′ en identité |

**Application aux 6 états** : G-B HIGH ; G-E2 MEDIUM (avec sous-critères NOT ESTABLISHED) ; G-E0 HIGH (événement) ; G-E1 HIGH (confinement) / MEDIUM (récurrence) ; G-E3 LOW ; G-E4 LOW.

---

## 12. LIMITES SCIENTIFIQUES

1. **Absence de validation statistique indépendante** : aucun test de significativité d'ARI (méthode Steinley 2004 disponible, non exécutée), aucun bootstrap, aucun test de différence entre profils d'états, aucune validation croisée spatio-temporelle. Les preuves sont **descriptives** et **reproductibles**, pas **inférées**.
2. **Nombre de périodes comparables** : la récurrence est évaluée sur 7 années utiles pour G-E2 (2010–2026 avec fenêtres de 1 an) ; G-E0 = 2 occurrences ; G-E1 = 1 poche ; les « périodes » sont donc **en petit nombre** — aucune inférence fréquentiste de récurrence possible.
3. **Changements de convention/session** : le contrat DATA indique une grille M3 avec contiguïté et 2 248 barres manquantes (0,1145 %) ; les conventions de pause/week-end/session ne sont pas auditées ici (aucun calcul, rapport d'audit N/S absent du workspace) ; une rupture de convention pourrait affecter les fenêtres mensuelles.
4. **Couverture incomplète** : 2026 est **partielle** (233 755 lignes vs ~355 k) ; 75 037 lignes à NaN exclus du masque de 3.6F (96,179 % utilisés) ; la couverture des états en 2026 est donc **fragile** (déjà visible : G-E2 2,9–3,1 %).
5. **Dépendance aux features choisies** : la cartographie est définie dans l'espace des 25 features V2 ; aucune analyse de sensibilité au choix des features (familles, fenêtres) n'existe ; le remplacement/ajout d'une feature pourrait déplacer la frontière G-E2 (documenté dans 3.6J §9.6).
6. **Validation full-cov incomplète** : seule la configuration K=2 full-cov existe (ARI diag vs full −0,0154) ; **aucun full-cov pour G-E2/G-E1** — la dépendance à la covariance (diag = indépendance conditionnelle) reste un problème non résolu pour les candidats.
7. **Perte des artefacts bruts après reset** : `/tmp/xauusd_pilot36f*.json`, `/tmp/xauusd_pilot36f_episodes.json`, baseline robuste et scripts sont **absents** ; les valeurs ne sont disponibles que via les rapports. **Traçabilité partielle** : les métriques sont citées, les calculs sous-jacents ne sont pas re-exécutables dans le workspace.
8. **Résultats restaurés ≠ réplication indépendante** : les chiffres de 3.6F–3.7 proviennent des runs antérieurs au reset, rapportés en session ; leur restauration dans les rapports **n'est pas** une ré-exécution ; aucune indépendance des runs ne peut être revendiquée.
9. **G-E2 non démontré comme régime final** : la persistance et la concordance inter-familles restent non établies ; son statut CANDIDATE_REGIME est **conservé**, ce qui limite la carte à un seul régime final.
10. **Biais de confirmation possible** : la validation 3.7/3.8 réutilise les mêmes résultats qui ont produit la carte (pas de partition de données train/test) ; le critère 3.8 est un critère de **classement**, pas d'**inférence** — la distinction 3.6J (PROVISIONAL selon critère strict) vs 3.8 (VALIDATED selon critère de cartographie) doit rester visible.

---

## 13. VERDICT SCIENTIFIQUE

### A. Existe-t-il une preuve solide d'au moins un régime comportemental ?
**OUI.** G-B : récurrence continue 2010–2026 (P(année|état) jamais nulle), persistance mesurée (diag HMM 0,9997–0,9998 ; KM K2 3 épisodes médiane 566 628), reproductibilité 8/8 configurations (KM + HMM, K2–K5), ARI seeds ≥ 0,974, aucune dépendance à un artefact, non confondu avec un cluster résiduel (3.7). Force : **HIGH**.

### B. La carte distingue-t-elle correctement régime et événement/anomalie ?
**OUI, avec une réserve.** Le discriminant appliqué est la **persistance** (conforme à la distinction formelle outlier/régime [1](https://doi.org/10.3390/e28070724)) : G-E0 (2 fenêtres, anomalie F3) et G-E1 (98 % 2010, bord de période) sont séparés explicitement et ne sont **pas** promus malgré une séparabilité/reproductibilité très élevée. Réserve : ce discriminant est appliqué **par jugement encadré par les chiffres** (2 fenêtres, 98 %), non par un test automatisé de récurrence ; E3/E4 restent hors régime pour d'autres raisons (mono-configuration / instabilité K + MAD≈0).

### C. Quels états sont réellement démontrés ?
- **Démontré comme régime** : G-B (récurrence + persistance + reproductibilité + non-artefact).
- **Démontrés comme événements** : G-E0 (2 fenêtres, anomalie F3, séparation extrême) ; G-E1 (structure reproductible 6/6 mais confinement 2010).
- **Démontrés comme structures distinctes** : G-E2 (signature et récurrence) — mais **pas** comme régime (persistance/concordance non établies).

### D. Quels états restent seulement candidats ou indéterminés ?
- **CANDIDATE** : G-E2 (récurrence + distinction établis ; persistance, concordance inter-familles, fragmentation, covariance non résolues — verdict 3.6I clos).
- **INDETERMINATE** : G-E3 (signature identifiée, 1 seule configuration, aucune preuve indépendante).
- **EXCLUDED** : G-E4 (instabilité K 12,79–30,70 %, 0/4 K-means, MAD ≈ 0).

### VERDICT

# SCIENTIFIC_STATUS = SUPPORTED_WITH_LIMITATIONS

**Justification** :
- **Pas STRONGLY_SUPPORTED** : les limites sont substantielles — absence de validation statistique indépendante (significativité, bootstrap), absence de ré-exécution (artefacts perdus, résultats restaurés non indépendants), G-E2 non démontré comme régime, dépendance covariance non testée pour les candidats, nombre très faible de « périodes » comparables (2 fenêtres G-E0, 1 poche G-E1). Ces limitations **empêchent** la conclusion la plus forte.
- **Pas INSUFFICIENT_EVIDENCE** : un régime est solidement établi (G-B) avec des métriques quantitatives et une reproductibilité multi-familles ; la séparation régime/événement est argumentée et conforme à un critère formel ; les états incertains sont classés explicitement (G-E2 candidat, G-E3 indéterminé, G-E4 exclu) sans forçage.
- **Donc SUPPORTED_WITH_LIMITATIONS** : la cartographie est **scientifiquement défendable et réfutable** — chaque conclusion est reliée à une métrique (silhouette, ARI, transitions, épisodes, répartitions annuelles, z-robustes), chaque méthode est justifiée par la littérature méthodologique, et chaque limites est documentée.

---

## 14. CONCLUSION

La cartographie finale des régimes comportementaux XAUUSD 2010–2026 (3.8 : G-B FINAL_REGIME ; G-E2 CANDIDATE_REGIME ; G-E0/G-E1 EVENT ; G-E3 INDETERMINATE ; G-E4 EXCLUDED) est **défendable, traçable et réfutable** au niveau **SUPPORTED_WITH_LIMITATIONS** :

1. **Un régime est établi** (G-B, référence continue et persistante) — la question « existe-t-il au moins un régime ? » a une réponse empirique positive.
2. **La distinction régime/événement est argumentée** (persistance comme discriminant ; G-E0 et G-E1 exclus malgré leur séparabilité/reproductibilité élevées).
3. **Les incertitudes sont explicites** : G-E2 demeure CANDIDATE_REGIME (récurrence et distinction établies ; persistance, concordance inter-familles, covariance non établies), G-E3 INDETERMINATE, G-E4 EXCLUDED.
4. **La preuve est limitée mais honnête** : aucune inférence statistique indépendante, aucune ré-exécution, artefacts bruts perdus, dépendance aux features choisies — ces limites sont documentées et doivent être levées avant tout usage inférentiel.

**Limite de portée** : ce rapport **ne change pas** la carte (VALIDATED selon le critère de classification de 3.8) et **ne la réévalue pas** selon un critère d'inférence (qui donnerait PROVISIONAL, cf. 3.7) — il audite la force des preuves. **Aucune transition** vers stratégie, trading, backtest, portefeuille, exécution ou classifieur n'est faite ni suggérée comme étape suivante de cette phase.

---

*Fin du rapport — Step 3.9. Aucun clustering, aucun K, aucun HMM, aucune feature, aucun backtest, aucune stratégie, aucun classifieur, aucune optimisation, aucun calcul ; littérature utilisée uniquement comme justification méthodologique ; preuve empirique exclusivement issue des résultats 3.6F–3.8 ; aucun commit, aucun push.*
