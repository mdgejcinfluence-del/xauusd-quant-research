# PHASE 3 — AUDIT FINAL ET ATTEINTE RÉELLE DE L'OBJECTIF

- **Étape** : audit final de la Phase 3 (`PHASE3_FINAL_OBJECTIVE_AUDIT.md`) — déterminer, sans illusion ni forçage, si l'objectif « **cartographier les régimes comportementaux de XAUUSD sur 2010–2026** » a réellement été atteint.
- **Sources** : uniquement les rapports Phase 3 V2 existants — `PHASE3_V2_REGIME_MAP_CANDIDATES.md` (3.6F), `PHASE3_V2_REGIME_MAP_CONSOLIDATION.md` (3.6G), `PHASE3_V2_G_E2_PROFILE.md` (3.6H), `PHASE3_V2_G_E2_VALIDATION.md` (3.6I), `PHASE3_V2_FINAL_REGIME_MAP.md` (3.6J/3.8), `PHASE3_V2_FINAL_REGIME_VALIDATION.md` (3.7), `PHASE3_V2_SCIENTIFIC_EVIDENCE_REPORT.md` (3.9).
- **Méthode** : audit **par les preuves uniquement** ; aucune nouvelle recherche, aucun modèle, aucun K, aucune feature, aucune stratégie, aucun backtest, aucun classifieur ; **aucune classification modifiée** ; littérature non utilisée comme preuve.
- **Aucun commit, aucun push.**

---

## 1. OBJECTIF EXACT DE LA PHASE 3

L'objectif, tel qu'énoncé selon les étapes 3.6F–3.9, est double :

1. **Descriptif** : identifier les **états comportementaux distincts et récurrents** de XAUUSD sur 2010–2026, et les caractériser (définition, apparition, durée, transitions) ;
2. **Taxonomique** : séparer correctement **régime** (récurrent + persistant + reproductible + distinct), **candidat**, **événement/anomalie**, **indéterminé** et **exclu**.

Critère de réussite implicite de la Phase 3 (et non pas simplement de chaque étape) : produire une **cartographie suffisamment démontrée** — c'est-à-dire : des régimes **réellement légitimés par les données**, des événements **réellement séparés**, des incertitudes **réellement conservées**, sans forçage.

**Point de vigilance central de cet audit** : une Phase 3 qui conclut « il existe principalement un comportement de référence et **aucun second régime nettement démontré** » peut être une **réponse scientifique valide** — même si elle est moins riche qu'espéré. L'objectif n'est pas de produire plusieurs régimes, mais de produire une cartographie **vraie** (cf. consigne 3.6J : « ne pas chercher à obtenir plusieurs régimes à tout prix »).

---

## 2. PREUVES DISPONIBLES (synthèse factuelle, aucun recalcul)

### 2.1 Données et features
- Grille M3 validée : **1 963 826 barres** (2010-01-01 → 2026-08-30) ; 1 888 789 lignes multivariées complètes (**96,179 %**) utilisées en 3.6F ; 25 features V2 conservées ; `VOLUME` exclu ; fenêtres positionnelles `[i−W+1, i]` ; estimateurs épinglés ; H1 aligné « bucket fermé » (AMEND 1.0/1.1, PIT) ; standardisation robuste médiane/MAD (fallback std si MAD ≈ 0).
- Documenté : `PHASE3_V2_DATA_CONTRACT.md`, `PHASE3_V2_FEATURE_SPEC.md`, rapports 3.6F–3.9.
- **Absent du workspace** : `PHASE3_V2_FEATURE_AUDIT.md`, rapports 3.6A–3.6D, artefacts bruts `/tmp/xauusd_pilot36f*.json` (perdus après réinitialisation).

### 2.2 Découverte (3.6F) — chiffres publiés
| K | K-means (sizes seed 0 · silhouette · ARI seeds · méd. épisode) | HMM diag (sizes seed 0 · ARI seeds · méd. épisode) |
|---|---|---|
| 2 | [1 860 888 ; 27 901] · **0,7911** · 1,000/1,000/1,000 · 566 628 | [579 765 ; 1 309 024] · 1,000/1,000/1,000 · 252 |
| 3 | [1 775 205 ; 27 901 ; 85 683] · 0,4009 · 0,99998 × 2 / 0,99999 · 1 | [491 756 ; 1 308 837 ; 88 196] · 1,000/1,000/1,000 · 252 |
| 4 | [1 690 577 ; 84 750 ; 85 561 ; 27 901] · 0,3215 · 0,885/0,885/0,9999 · 1 | [241 497 ; 251 389 ; 87 435 ; 1 308 468] · **≈0 / 0,99989 / ≈0** · 268 (seed 1 = état unique) |
| 5 | [80 117 ; 27 901 ; 593 894 ; 85 053 ; 1 101 824] · 0,1224 · 0,988/0,978/0,974 · 1 | [374 323 ; 85 126 ; 1 259 983 ; 90 099 ; 79 258] · ≈1/≈1/1,000 · 193 |

- Sanity K2 : HMM **full** = partition K-means (ARI **1,0000**, [1 860 888 ; 27 901]) ; HMM diag vs full ARI **−0,0154** → la structure K=2 dépend du modèle de covariance.
- K-means K≥3 : médiane d'épisode = **1 bar** (mosaïques de frontière — limitation documentée 3.6F §7.2.6, 3.9 §12).
- HMM K4 : instable (seed 1 effondré ; seed 0 état à ligne nulle) — documenté 3.6F §7.2, 3.9 §8.

### 2.3 États candidats (3.6F → 3.6I)
| État | Taille | Signature (z robustes) | Récurrence | Persistance (diag) | Reproductibilité | Verdicts |
|---|---|---|---|---|---|---|
| **G-B** (référence) | 58,3–98,5 % (KM) ; 66,7–69,3 % (HMM) | |z| ≤ 0,3 sur 25 features | continue 2010–2026 | 0,9997–0,9998 (HMM) ; KM K2 1,0000 ; épisodes longs (566 628) | 8/8 configs ; ARI seeds ≥ 0,974 | FINAL_REGIME (3.7/3.8) |
| **G-E2** | 80 117–90 099 (4,24–4,77 %) | skew +4,72σ ; kurt +6,22σ ; spacing +1,12σ ; clust −0,85σ | 2013/2014/2016/2017 (≈93–97 %), 2026 ~3 %, coupure 2015 | 0,9987 (K4) / 0,9973 (K5) / **0,9957 (HMM — plus faible)** ; méd. ép. = 1 bar ; noyau ≈ 22 600 ; **durées HMM par état inconnues** | 2 configs KM identiques (écart 5,5 %) + 1 HMM « approchante » **6× atténuée** (skew +0,72σ) ; ARI seeds 0,885–0,9999 | 3.6I **UNCERTAIN** → 3.7/3.8 **CANDIDATE_REGIME** |
| **G-E0** | 27 901 (1,48 %) | skew −17,5σ ; kurt +30,5σ ; vr2 −2,91σ | **2 fenêtres** : 2015-07-20→09-01 (13 952 bars) ; 2021-08-08→09-21 (13 950 bars) ; 0 % ailleurs | 0,9999 (artefact 2 fenêtres) | identité exacte KM K2–K5 + HMM full (ARI 1,0000) ; **absent du HMM diag** | **EVENT** (anomalie F3, ≥ 30 extrêmes) |
| **G-E1** | 85 053–88 196 (4,50–4,67 %) | low_wick +7,62σ ; body −4,22σ ; close +4,29σ ; sigma +1,55/+1,65σ | **2010 : 97,9–98,5 %** ; traces 2011/2020/2025 ; 0 % ailleurs | 0,9969–0,9997 ; noyau ≈ 27 100 | 6/6 configs K≥3 (profils quasi identiques) | **EVENT** (bord de période, anomalies 3.6D) |
| **G-E3** | 79 258 (4,20 %) | vol_ratio_day +3,08σ ; h1_vol +2,46σ ; m1_ext +1,73σ | toutes années (pics 2011/2020) | 0,9960 ; épisodes par état inconnus | **1/8 configurations** (HMM K5 s4) | **INDETERMINATE** |
| **G-E4** | 241 497–579 765 (**12,79–30,70 % selon K**) | storm_p90_run = 1 ; clust −0,73/−0,89σ | toutes années | 0,9987–0,9995 (définition change avec K) | 4/4 HMM, **0/4 K-means** | **EXCLUDED** (instabilité K + MAD ≈ 0) |

### 2.4 Verdicts successifs
- 3.6I : G-E2 = **REGIME_CANDIDATE_UNCERTAIN** (clos) ;
- 3.6J, 3.7 : **FINAL_REGIME_MAP = PROVISIONAL** (critère strict : chaque régime doit satisfaire seul tous les critères) ;
- 3.8 : **FINAL_REGIME_MAP = VALIDATED** (critère de **classification** : régime démontré identifié, événements séparés, indéterminés conservés, rien de forcé) ;
- 3.9 : **SCIENTIFIC_STATUS = SUPPORTED_WITH_LIMITATIONS**.

---

## 3. ÉVALUATION DE LA CARTE ACTUELLE (sans la forcer)

### 3.1 Point critique imposé : stabilité d'algorithme ≠ stabilité de partition ≠ existence d'un régime

Cet audit vérifie explicitement la distinction, car c'est le point où une cartographie peut être **surestimée** :

| Niveau | Ce qui a été mesuré | Ce que cela **démontre** | Ce que cela **NE démontre PAS** |
|---|---|---|---|
| **Stabilité d'algorithme** | ARI inter-seeds élevé (KM K2–K3 : ≥ 0,99998 ; HMM K2/K3/K5 : ≥ 0,99999) ; n_init=10 ; 3 seeds | L'algorithme **reproduit sa propre solution** sur ce jeu de données | L'existence d'un régime ; la récurrence ; la persistance |
| **Stabilité de partition** | ARI inter-familles (KM vs HMM full K2 = 1,0000) ; tailles répétées (G-E2 K4/K5 écart 5,5 %) ; 8/8 (G-B) ; 6/6 (G-E1) | Les **partitions** sont reproductibles entre paramétrisations/modèles | L'existence d'un régime ; la temporalité ; la non-circularité (mêmes données, mêmes features) |
| **Existence d'un régime comportemental** | Récurrence **temporelle** (P(année\|état), fenêtres) + **persistance mesurée** (transitions, durées d'épisodes réelles) + signature distincte + non-dépendance à un artefact | Un **état comportemental** distinct et récurrent **dans le temps** | Rien d'autre — c'est le seul niveau qui légitime le mot « régime » |

**Conclusion de la distinction** : dans la carte finale, **seul G-B** satisfait le troisième niveau (récurrence continue + persistance mesurée + signature + reproductibilité + non-artefact). **G-E2** satisfait la récurrence et la distinction (niveau 3 partiel) mais **pas** la persistance mesurée (médiane 1 bar côté K-means ; durées HMM inconnues) ni la concordance inter-familles (niveau 2 partiel : 1 HMM atténué 6×). G-E0/G-E1 satisfont brillamment le niveau 2 (reproductibilité) mais **pas** le niveau 3 (récurrence absente). G-E3 (niveau 2 = 1/8, niveau 3 non vérifiable) ; G-E4 (niveau 2 = 4/4 HMM mais 0/4 KM ; niveau 3 = instable).

### 3.2 Évaluation état par état (preuves existantes uniquement)

| État | Récurrence | Persistance | Distinction | Reproductibilité | Stabilité | Transitions | Temporalité | Séparation régime/événement/artefact | Statut d'audit |
|---|---|---|---|---|---|---|---|---|---|
| **G-B** | ✅ continue 2010–2026 | ✅ mesurée (0,9997–0,9998 ; épisodes longs) | ✅ neutralité (mais distinction **par défaut**) | ✅ 8/8 | ✅ seeds ≥ 0,974 | ✅ diag forte ; sorties faibles vers E2/E1/E3 | ✅ toute la période | ✅ aucun artefact identifié | **Régime démontré** |
| **G-E2** | ✅ 4 années disjointes + 2 blocs | ❌ **non démontrée** (méd. 1 bar ; HMM inconnu ; diag 0,9957 = plus faible) | ✅ signature unique | ⚠️ 2 KM identiques + 1 HMM 6× atténué | ⚠️ K4 : permutation seeds (0,885) ; K5 : ≥ 0,974 | ⚠️ sortie → B (0,0010–0,0020) ; entrée depuis B 0,0001 | ✅ 2013–2017 ; absent 2018–2025 ; résiduel 2026 | ⚠️ sensibilité covariance **non testée** ; fragmentation | **Régime candidat** |
| **G-E0** | ❌ **2 fenêtres** | ❌ non pertinente (artefact) | ✅ extrême et unique | ✅ identité exacte (K2–K5 + HMM full) | ✅ (mais dépendant du modèle de covariance) | ⚠️ 0,9999 — état absorbant à 2 fenêtres | ❌ 2015 + 2021 uniquement | ✅ **anomalie F3** | **Événement/anomalie** |
| **G-E1** | ❌ **98 % en 2010** | ⚠️ noyau 27 100 (intra-2010) | ✅ unique (mèche basse) | ✅ 6/6 | ✅ | ⚠️ sortie → B 0,0017–0,0030 | ❌ confinement 2010 + traces | ✅ bord de période / anomalies 3.6D | **Événement/anomalie** |
| **G-E3** | ⚠️ toutes années mais mono-détection | ⚠️ 0,9960 ; épisodes inconnus | ✅ signature unique | ❌ 1/8 | ❌ non testée (1 seule) | ⚠️ → B 0,0027 ; → E2′ 0,0005 | ⚠️ étalé, pics 2011/2020 | ⚠️ aucune preuve indépendante | **Indéterminé** |
| **G-E4** | ⚠️ toutes années mais définition instable | ⚠️ 0,9987–0,9995 (change avec K) | ⚠️ partielle (feature quasi-constante) | ❌ 0/4 K-means | ❌ instable en K (12,79–30,70 %) | ⚠️ diag élevée mais définition mouvante | ⚠️ partout, incohérent | ✅ **artefact technico-définitionnel** (MAD ≈ 0) | **Exclu** |

### 3.3 Évaluation de la carte dans son ensemble

- **Cohérence interne** : ✅ — chaque état a une classification justifiée par ses preuves ; aucune catégorie ne contredit une mesure.
- **Séparation régime/événement** : ✅ — G-E0/G-E1 exclus malgré une séparabilité/reproductibilité très élevée (le critère discriminant est la **persistance**, conforme à 3.9 §8) .
- **Non-redondance** : ✅ — G-B ≠ G-E2 ≠ G-E0 ≠ G-E1 ≠ G-E3 ≠ G-E4 sur les signatures.
- **Couverture** : ⚠️ — G-B représente 58,3–98,5 % (selon K) ; la majorité du comportement est couverte, mais la métrique « proportion de chaque année occupée » n'existe pas (seule P(année|état)).
- **Persistance des états retenus comme régimes** : ✅ pour G-B ; ❌ pour G-E2 (candidat ; « tenant » du critère mais non démontrée).
- **Neutralité de G-B** : ⚠️ — sa « distinction » est la **neutralité** (profil = médiane) ; c'est un régime de **référence**, pas un comportement exceptionnel. La silhouette K2 (0,7911) est en outre **partiellement portée par l'outlier G-E0** (caveat standard — 3.9 §8).

**Verdict d'évaluation** : la carte est **cohérente et honnête** ; elle est néanmoins **pauvre en régimes nets** : **un seul régime démontré (G-B, de type référence) et un seul candidat distinct non démontré (G-E2)**. Les autres états sont des événements, un indéterminé et un exclu.

---

## 4. FAIBLESSES ÉVENTUELLES (transparence obligatoire — aucune masquée)

1. **Faiblesse centrale — un seul régime « net »** : la carte ne démontre qu'un régime de **référence** (G-B, défini par neutralité). Le seul état distinct récurrent (G-E2) reste **candidat** : persistance non démontrée (médiane d'épisode 1 bar), concordance inter-familles non démontrée (HMM 6× atténué), covariance non testée. **La réponse « il existe principalement un mode de référence, et pas de second régime nettement établi » est une réponse scientifique, mais elle est moins riche que l'objectif formulé (« cartographier les régimes »).**
2. **Distinction clé (niveau) — algorithmique vs partitionnaire vs comportemental** : les ARI inter-seeds (très élevés) prouvent la **stabilité d'algorithme**, pas l'existence de régimes ; les ARI inter-familles (1,0000 pour E0, 8/8 pour G-B) prouvent la **stabilité de partition**, pas la récurrence ; seuls G-B et (partiellement) G-E2 ont un niveau **comportemental** vérifié. Ce point est bien documenté mais la lecture de la carte finale peut le faire oublier.
3. **Manque de validation statistique indépendante** : aucun test de significativité (ARI vs hasard — méthode Steinley 2004 disponible, non exécutée), aucun bootstrap, aucun test de différence inter-états, aucune CV temporelle ; les preuves sont **descriptives et reproductibles**, pas **inférées**.
4. **Reproductibilité compromise par la réinitialisation** : artefacts bruts (`/tmp/*.json`, `episodes.json`, baseline) **perdus** ; rapports 3.6A–3.6D et `PHASE3_V2_FEATURE_AUDIT.md` **absents** ; les chiffres proviennent du rapport 3.6F restauré en session → **aucune ré-exécution indépendante** possible ni réalisée. Une **réplication indépendante** ne peut pas être revendiquée.
5. **Dépendance au choix des features** : la carte est définie dans l'espace des 25 features V2 ; aucune analyse de sensibilité au choix des features/fenêtres ; G-E2 repose sur des features de queues (sensibles aux anomalies F3).
6. **Dépendance au modèle de covariance** : sanity K2 = changement **total** diag ↔ full (ARI −0,0154) ; aucun full-cov pour G-E2/G-E1 → incertitude structurelle.
7. **Temporalité limitée** : petits nombres d'occurrences comparables (G-E0 : 2 ; G-E1 : 1 poche ; G-E2 : 2 blocs + 2 années isolées) → aucune inférence fréquentiste de récurrence ; 2026 partielle (233 755 lignes) ; changements de convention/session non audités dans le workspace.
8. **HMM K4 instable** et **permutation de seeds KM K4** : les identifications fines à K=4 sont indicatives ; le sanity HMM K4 (seed 0, état à ligne nulle) est une **solution limite** non interprétable.
9. **Biais de confirmation** : la validation (3.7/3.8) réutilise les mêmes données/features que la découverte ; convergence possible des verdicts par construction.
10. **Divergence de verdicts entre étapes** : 3.6J/3.7 = PROVISIONAL (critère strict) ; 3.8 = VALIDATED (critère de classification). Cette **différence de critère** doit rester visible : la carte est validée **comme classification**, pas comme **carte inférentiellement établie** (3.9 l'a explicitement dit).

---

## 5. DÉCISION FINALE

# PHASE3_OBJECTIVE = ACHIEVED_WITH_LIMITATIONS

---

## 6. JUSTIFICATION DE LA DÉCISION

### 6.1 Pourquoi pas ACHIEVED
Une **faiblesse importante** empêche de considérer l'objectif comme **pleinement établi** :
1. **Un seul régime « net » démontré** — et il s'agit du **mode de référence** (G-B), dont la distinction repose en partie sur la **neutralité** ; le seul état **distinct** et récurrent hors référence (G-E2) est **candidat, non démontré** (persistance et concordance inter-familles non établies).
2. **Aucune validation statistique indépendante** (significativité, bootstrap, tests inter-états) : les preuves sont descriptives et reproductibles, mais **pas inférées**.
3. **Reproductibilité non indépendante** : artefacts bruts perdus, résultats restaurés en session, aucune ré-exécution → impossible de parler de **réplication**.
4. **Dépendance non résolue** au choix des features et au **modèle de covariance** (diag vs full), avec G-E2/G-E1 non testés en full-cov.
5. La carte est donc **utile et défendable** (3.9 : SUPPORTED_WITH_LIMITATIONS), mais **pas pleinement établie** — exactement la définition d'ACHIEVED_WITH_LIMITATIONS.

### 6.2 Pourquoi pas NOT_ACHIEVED
1. **Un régime est réellement démontré** (G-B) : récurrence continue 2010–2026 (P(année|état) jamais nulle), persistance mesurée (diag HMM 0,9997–0,9998 ; épisodes longs en K2), reproductibilité 8/8 (K-means + HMM, K2–K5), non-artefact — le « niveau 3 » (existence comportementale) est atteint pour G-B.
2. **La séparation régime/événement est scientifiquement fondée** : G-E0 (2 fenêtres, anomalie F3) et G-E1 (98 % 2010, bord de période) sont exclus **malgré** leur séparabilité/reproductibilité très élevée — le critère discriminant (persistance) est correct et appliqué sans forçage.
3. **Une taxonomie complète et honnête a été produite** : un régime démontré, un candidat explicite (incertitude conservée, verdict 3.6I clos), deux événements, un indéterminé, un exclu ; aucune catégorie artificiellement forcée (aucun second régime inventé, G-E2 non promu).
4. **La réponse scientifique est claire** : sur 2010–2026, le comportement de XAUUSD est **dominé par un état de référence continu** (G-B), ponctué d'**incursions** — 2 blocs du candidat G-E2 (2013–2014, 2016–2017), 2 événements G-E0 (2015, 2021), 1 événement G-E1 (2010), pics G-E3 (2011, 2020), G-E4 instable → **aucune alternance rapide de régimes n'est observée**. C'est une **conclusion de fond**, pas un échec de l'exploration.
5. **Les méthodes sont scientifiquement appropriées** (3.9 §8) : silhouette, ARI (Hubert-Arabie/Steinley), HMM (Hamilton), persistance par transitions, séparation événement/structure — tout en rappelant que la littérature ne **prouve** aucun régime XAUUSD.

### 6.3 Résumé de la décision
| Dimension | État |
|---|---|
| Objectif descriptif (identifier des états) | ✅ **atteint** (taxonomie complète, chiffrée) |
| Objectif « cartographier des régimes » | ✅ **atteint de façon sobre** : 1 régime de référence démontré (G-B) + 1 candidat (G-E2) + événements séparés |
| Niveau de démonstration | ⚠️ **inférentiel non atteint** : pas de test statistique indépendant, pas de réplication, dépendances non résolues |
| Honnêteté de la carte | ✅ **maximale** : aucune catégorie forcée, aucune faiblesse masquée |
| Conclusion de fond | ⚠️ **éclairante mais limitée** : « pas de second régime nettement démontré » |

**Conclusion finale** : la Phase 3 a **atteint son objectif au niveau de la cartographie descriptive et taxonomique** — la carte est cohérente, sobre, chiffrée et honnête. Elle **ne l'a pas atteint au niveau de la démonstration inférentielle** : le seul régime distingué de la référence reste un candidat ; la validation statistique indépendante, la réplication et le test de sensibilité (features/covariance) font défaut. La cartographie est donc **scientifiquement utile et défendable, mais pas pleinement établie** → **ACHIEVED_WITH_LIMITATIONS**.

---

## 7. CONDITIONS DE SORTIE VERS ACHIEVED (non exécutées — hors périmètre de cet audit)

Pour passer à ACHIEVED, il faudrait (étapes futures dédiées, non lancées ici) :
1. statistiques d'épisodes **HMM par état** (K2–K5) — pour statuer sur la persistance de G-E2 ;
2. comparaison directe de partitions KM/HMM (concordance G-E2) ;
3. test **full-covariance** de G-E2/G-E1 ;
4. tests de significativité (ARI vs hasard, bootstrap, tests inter-états) ;
5. validation source des fenêtres G-E0 (2015/2021) et de la période G-E1 (2010) ;
6. ré-exécution indépendante (artefacts régénérés) — seule façon de lever la limite de reproductibilité.

Ces éléments **ne sont pas présents** dans les preuves actuelles ; leur absence est la raison du statut **ACHIEVED_WITH_LIMITATIONS** et non ACHIEVED.

---

*Fin du rapport — Audit final Phase 3. Aucun nouveau modèle, aucun K, aucune feature, aucune stratégie, aucun backtest, aucun classifieur ; littérature non utilisée comme preuve ; seule conclusion : PHASE3_OBJECTIVE = ACHIEVED_WITH_LIMITATIONS ; aucun commit, aucun push.*
