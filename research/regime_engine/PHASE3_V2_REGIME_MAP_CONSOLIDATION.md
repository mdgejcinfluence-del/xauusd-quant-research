# PHASE 3 V2 — STEP 3.6G : CONSOLIDATION DE LA CARTE CANDIDATE DES RÉGIMES

- **Étape** : 3.6G — consolidation de la carte candidate issue de 3.6F (`PHASE3_V2_REGIME_MAP_CONSOLIDATION.md`)
- **Statut** : consolidation **descriptive** — aucun nouveau modèle, aucun K recalculé, aucun classifieur, aucun backtest, aucune stratégie, aucune modification de features.
- **Date** : 2026-09-06
- **Source primaire** : `PHASE3_V2_REGIME_MAP_CANDIDATES.md` (3.6F — run complet K-means/HMM K=2..5 sur 1 888 789 × 25 lignes, 1 963 826 × 27 au total, 96,179 %).
- **Note d'accessibilité des sources** : `/tmp/xauusd_pilot36f.json`, `/tmp/xauusd_pilot36f_episodes.json` et les rapports nominaux 3.6B–3.6F ne sont **pas présents dans le workspace courant** (réinitialisation de l'environnement après les runs). Le rapport 3.6F a été restauré à l'identique depuis les résultats de session ; **toutes les valeurs ci-dessous en sont extraites textuellement. AUCUN calcul n'a été relancé, AUCUNE valeur n'a été recalculée.**
- **Définitions de confiance utilisées (uniques pour ce rapport)** :
  - **HIGH** : structure distincte reproduite dans **les deux familles** (≥ 2 configurations chacune) **ou** identité exacte inter-méthodes (ARI = 1.0000) ;
  - **MEDIUM** : reproduite dans **une famille sur ≥ 2 K** (ou 2–3 configurations au total), avec récurrence multi-années **partielle** ;
  - **LOW** : **une seule configuration**, ou poids **instable en K**, ou dépendance à une **feature fragile** (MAD ≈ 0 / fallback std).

---

## 0. Synthèse — les 8 critères par candidat

| ID | Fréquence globale | Années de présence | Durée des épisodes | Transitions (diag. ; principales) | Caractéristiques comportementales (z robustes) | Configurations | Récurrent / événementiel | Confiance |
|---|---|---|---|---|---|---|---|---|
| **R-B** | 58,3 – 98,5 % (1 101 824–1 860 888) | continue 2010–2026 | KM K2 : 3 ép., médiane 566 628 ; KM K≥3 : fragmentation (médiane 1) ; HMM : méd. 193–268 | diag 0.9825–1.0000 | ∼ médiane globale (|z| ≤ 0.3 partout) | 8/8 (KM K2–K5, HMM K2–K5) | **Récurrent** (état dominant/référence) | **HIGH** |
| **R-E0** | 27 901 (1,48 %) — identique à tous K | **seulement 2015 (50 %) et 2021 (50 %)** | **exactement 2 épisodes** : 13 952 et 13 950 bars | 0.9999 (quasi-absorbant) ; entrées/sorties ≈ 0.0001 | skew −9,39 (−17,5σ), kurt 420,9 (+30,5σ), vr2 −2,91σ, storm_clust +0,95σ, spacing −0,67σ | KM K2/K3/K4/K5 (ensemble identique) + HMM **full** K2 (ARI 1.0000) ; **absent** du HMM diag | **Événementiel** (2 fenêtres ; anomalie de queues F3) | **HIGH** (structure) — **événement, pas régime** |
| **R-E1** | 85 053–88 196 (4,50–4,67 %) | 2010 (97,9–98,5 %), 2011 (1,1–1,2 %), 2020 (0,4–0,5 %), 2025 (0,3–0,4 %) | KM : 258–266 ép., médiane 1 (frontières), **moyenne 330–332**, max ≈ 27 100 ; HMM : méd. 193–252 (global) | diag 0.9969–0.9997 ; exit principal E1→B 0.0017–0.0030 | low_wick +7,62σ, body_range −4,22σ, close_pos +4,29σ, sigma +1,55/+1,65σ, vr2 +1,70σ, run −0,91σ, acf1 +0,56σ | **6/6 configurations K≥3** (KM K3/K4/K5 + HMM K3/K4/K5) | **Événementiel / localisé 2010** (98 %) — pas de récurrence multi-années | **MEDIUM** (régime) — structure distincte HIGH |
| **R-E2** | 80 117–90 099 (4,24–4,77 %) | 2013 (26,7–28,2 %), 2014 (18,4–19,0 %), 2016 (35,1–35,5 %), 2017 (14,6–15,8 %), 2026 (2,9–3,1 %) | KM : 102–219 ép., médiane 1, moyenne 368–832, max ≈ 22 600 | diag 0.9957–0.9987 | skew +2,43 (+4,72σ), kurt 101,1 (+6,22σ), spacing +1,12σ, storm_clust −0,85σ, ext_rate −0,52σ, run −0,46σ | KM K4 s1, KM K5 s0 (+ HMM K5 s3 approchant) — **2/8 + 1 approchant** | **Récurrent en germe** (4 années) mais **épisodique** | **MEDIUM** |
| **R-E3** | 79 258 (4,20 %) | **toutes les années** ; pics 2011 (21,2 %) et 2020 (17,3 %) | par état : **non calculé (indéterminé)** ; HMM K5 global : 1 365 ép., médiane 193 | diag 0.9960 ; sorties : →B 0.0027, →E4′ 0.0007, →E2′ 0.0005 | vol_ratio_day **+3,08σ**, h1_vol_ratio **+2,46σ**, m1_ext_rate_day **+1,73σ**, ext_rate +1,25σ, noise −0,75σ | **HMM K5 s4 uniquement (1/8)** | présent toutes années mais **une seule configuration** | **LOW** |
| **R-E4** | **varie avec K** : 241 497 (12,79 %) – 579 765 (30,70 %) | toutes les années (2010 : 15,0 % ; pics 2011/2012/2017) | par état : **indéterminé** ; HMM global : méd. 193–268 | diag 0.9987–0.9995 | storm_p90_run_month **= 1** (vs 2), storm_clust −0,73/−0,89σ, kurt −0,46σ, spacing +0,45/+0,67σ | HMM K2/K3/K4/K5 (fragmenté en K4/K5) ; **jamais** retrouvé par K-means | présent toutes années mais **définition instable en K** | **LOW** |

---

## 1. R-B — État de référence

1. **Fréquence globale** : 58,33 % (KM K5, 1 101 824) ; 66,71–69,30 % (HMM) ; 89,51–93,99 % (KM K4/K3) ; 98,52 % (KM K2, 1 860 888).
2. **Années de présence** : **continue 2010–2026** — seul état présent sur toute la période.
3. **Durée des épisodes** : KM K2 = 3 épisodes, médiane 566 628 bars ; KM K≥3 = fragmentation de frontière (médiane 1 ; K3 : 520 ép. globaux, K4 : 748, K5 : 39 106) ; HMM = 551 (K2), 569 (K3), 845 (K4), 1 365 (K5) épisodes globaux, médianes 193–268. Statistiques par état HMM : **non calculées (indéterminé)**.
4. **Transitions** : diag 1.0000 (KM K2), 0.9999 (KM K3), 0.9998 (KM K4), **0.9825 (KM K5, avec X→B 0.0173)**, 0.9997–0.9998 (HMM K2–K5). La baisse à K=5 est un artefact de fragmentation.
5. **Caractéristiques comportementales** : profil = **médiane globale** de toutes les features (|z| ≤ 0,3) ; storm_p90_run_month = 2 (HMM K2) ; toutes les dimensions ≈ normales.
6. **Méthodes/configurations** : 8/8 (KM K2–K5 × HMM K2–K5).
7. **Récurrent ou événementiel** : **récurrent par construction** — c'est le corps principal de la distribution ; à traiter comme **référence**, pas comme « régime » actif.
8. **Niveau de confiance** : **HIGH** (existence et rôle de référence).

---

## 2. R-E0 — Queue skew/kurtosis extrême (candidat anomalie de données)

1. **Fréquence globale** : **27 901 lignes — 1,48 %**, ensemble **identique** dans KM K2/K3/K4/K5 et dans HMM **full** K2.
2. **Années de présence** : **aucune en dehors de deux fenêtres** — 2015 (50 % des lignes de l'état) et 2021 (50 %) ; 0 % toutes les autres années.
3. **Durée des épisodes** : **exactement 2 épisodes** — 2015-07-20 01:36 → 2015-09-01 08:51 (**13 952 bars**) et 2021-08-08 23:03 → 2021-09-21 09:57 (**13 950 bars**) ; durées quasi symétriques (~6 semaines calendaires).
4. **Transitions** : quasi-absorbant (diag **0.9999**) ; B→E0 0.0000, E0→B 0.0001 (KM K2) ; aucun autre échange notable.
5. **Caractéristiques comportementales principales** : skew **−9,39** (z **−17,5σ**), kurtosis **420,9** (z **+30,5σ**), vr2 0,896 (**−2,91σ**), storm_clust **+0,95σ**, ext_spacing 10 (**−0,67σ**), noise +0,36σ, dir_month −0,61σ, run −0,63σ, acf1 +0,19σ, h1_acf1 +0,31σ — toutes les autres features |z| < 0,7. **État défini exclusivement par les queues d'asymétrie/aplatissement mensuels.**
6. **Méthodes/configurations** : KM K2 s1, K3 s1, K4 s3, K5 s2 (ensemble identique) + **HMM full K2** (ARI 1.0000) — **absent du HMM diag** (les corrélations avec les autres features sont faibles).
7. **Récurrent ou événementiel** : **strictement ÉVÉNEMENTIEL** — 2 fenêtres. Coïncide avec les anomalies de queues du dataset (règle F3 « ≥ 30 extrêmes », 3.6A) → **à traiter comme drapeau de qualité de données**.
8. **Niveau de confiance** : **HIGH** (reproductibilité inter-méthodes ARI=1.0, profil extrême) **en tant que structure** ; **confiance nulle en tant que régime récurrent**.

---

## 3. R-E1 — Structure « mèche basse / 2010 »

1. **Fréquence globale** : 85 053–88 196 lignes — **4,50–4,67 %** ; écarts entre configurations ≤ 3,7 %.
2. **Années de présence** : 2010 **97,9–98,5 %** ; 2011 **1,1–1,2 %** ; 2020 **0,4–0,5 %** ; 2025 **0,3–0,4 %** ; 0 % ailleurs. Début à la première ligne exploitable (2010-02-12 11:57) ; dernier épisode 2025-12-01.
3. **Durée des épisodes** : KM — 258–266 épisodes, **médiane 1** (basculements aux frontières), **moyenne 330–332**, **max ≈ 27 100 bars** (bloc principal 2010) ; HMM — médiane 193–252 (globale K5/K3 ; par état non calculé).
4. **Transitions** : diag **0.9969–0.9997** ; sortie principale **E1→B 0.0017–0.0030** (KM) / 0.0001–0.0002 (HMM) ; entrées B→E1 0.0001–0.0002.
5. **Caractéristiques comportementales principales** : low_wick **0,378 vs 0,204** (**+7,62σ**), body_range **0,366** (**−4,22σ**), close_pos **0,618** (**+4,29σ**), m3_range/tr_sigma **+1,55/+1,65σ**, vr2 **+1,70σ**, run **−0,91σ**, acf1 **+0,56σ**, scf +0,38σ, up_wick −0,64σ, ext_rate +0,93σ, ext_sign +0,70σ, kurt −0,65σ. **Combinaison unique** — aucun autre candidat ne l'approche.
6. **Méthodes/configurations** : **6/6 configurations K≥3** — KM K3/K4/K5 + HMM K3/K4/K5 — profils z quasi identiques (ex. low_wick +7,62 vs +7,56 vs +7,63 ; body_range −4,22 vs −4,17 vs −4,22 ; close_pos +4,29 vs +4,27 vs +4,29).
7. **Récurrent ou événementiel** : **LOCALISÉ / ÉVÉNEMENTIEL** — 98 % en 2010 ; structure cohérente **à l'intérieur** de 2010 (noyau ≈ 27 100 bars) mais **pas de récurrence multi-années**. Ne pas classer comme « régime récurrent ».
8. **Niveau de confiance** : **HIGH** en tant que structure distincte (6/6) ; **MEDIUM** en tant que régime (recurrence insuffisante) → **retenu MEDIUM** pour la carte minimale.

---

## 4. R-E2 — Skew/kurtosis modérés, extrêmes moins agrégés

1. **Fréquence globale** : KM K4 s1 84 750 (4,49 %) ; KM K5 s0 80 117 (4,24 %) ; HMM K5 s3 90 099 (4,77 %, approchant).
2. **Années de présence** : 2013 **26,7–28,2 %** ; 2014 **18,4–19,0 %** ; 2016 **35,1–35,5 %** ; 2017 **14,6–15,8 %** ; 2026 **2,9–3,1 %** ; 2024 0,7 % (KM K4) ; 0 % ailleurs.
3. **Durée des épisodes** : KM — 102 (K4) à 219 (K5) épisodes, **médiane 1**, **moyenne 368–832**, **max ≈ 22 600 bars** (bloc 2013–2017) ; HMM par état non calculé.
4. **Transitions** : diag **0.9987** (KM K4), **0.9973** (KM K5, →X 0.0018), **0.9957** (HMM K5, →E4′ 0.0020, →B 0.0020) — persistance la plus faible des candidats.
5. **Caractéristiques comportementales principales** : skew **+2,43** (**+4,72σ**), kurtosis **101,1** (**+6,22σ**), ext_spacing **18** (**+1,12σ**), storm_clust 0,297 (**−0,85σ**), ext_rate 0,0148 (**−0,52σ**), run **−0,46σ**, vol_ratio −0,17σ, h1_vol_ratio −0,23σ, sigma −0,31σ, acf1 −0,17σ. **Opposé à R-E0** sur la queue (droite vs gauche) et sur l'agrégation des extrêmes (clust ↓ / spacing ↑ vs clust ↑).
6. **Méthodes/configurations** : KM K4 s1, KM K5 s0 + HMM K5 s3 « approchant » (skew +0,72σ, kurt +1,0σ, storm_clust −0,87σ, profil atténué) — **2/8 + 1 approchant**.
7. **Récurrent ou événementiel** : **récurrent en germe** (4 années calendaires distinctes : 2013, 2014, 2016, 2017) mais **épisodique** (médiane épisode 1 ; noyau continu ~22 600 bars). C'est le seul candidat hors R-B avec une fenêtre multi-années > 1 configuration.
8. **Niveau de confiance** : **MEDIUM**.

---

## 5. R-E3 — Volatilité jour/mois élevée

1. **Fréquence globale** : 79 258 lignes — **4,20 %** (HMM K5 s4 uniquement).
2. **Années de présence** : **toutes les années** — 2010 7,0 ; 2011 **21,2** ; 2012 9,4 ; 2013 5,2 ; 2014 5,0 ; 2015 1,1 ; 2016 2,7 ; 2017 1,2 ; 2018 2,9 ; 2019 5,0 ; 2020 **17,3** ; 2021 2,4 ; 2022 1,9 ; 2023 1,9 ; 2024 3,4 ; 2025 7,3 ; 2026 5,0 (%). Pics 2011 et 2020.
3. **Durée des épisodes** : **par état : non calculée (indéterminé)** — seules les statistiques HMM K5 globales sont disponibles (1 365 épisodes, médiane 193 bars).
4. **Transitions** : diag **0.9960** ; sorties →B 0.0027, →E4′ 0.0007, →E2′ 0.0005.
5. **Caractéristiques comportementales principales** : vol_ratio_day_month **1,572** (**+3,08σ**), h1_vol_ratio **1,572** (**+2,46σ**), m1_ext_rate_day **0,0271** (**+1,73σ**), ext_rate_month **+1,25σ**, noise **−0,75σ**, up_wick −0,49σ, scf −0,43σ, tr_expansion −0,34σ, body_range +0,53σ, dir_month +0,52σ, acf1 +0,50σ. Signature : volatilité intra-jour M3/H1 nettement au-dessus de la normale mensuelle, répartition moins gaussienne, extrêmes M1 plus fréquents.
6. **Méthodes/configurations** : **HMM K5 s4 uniquement** — **1/8**.
7. **Récurrent ou événementiel** : présence étalée sur toutes les années (au contraire de R-E0/R-E1) **mais détection mono-configuration** → l'étalement temporel ne peut pas être confirmé comme récurrence de la même structure.
8. **Niveau de confiance** : **LOW**.

---

## 6. R-E4 — Mois sans extrêmes cumulés (storm_p90_run = 1)

1. **Fréquence globale** : **instable en K** — HMM K2 579 765 (**30,70 %**) ; K3 491 756 (26,04 %) ; K4 241 497 (12,79 %) ; K5 374 323 (19,82 %).
2. **Années de présence** : toutes les années (HMM K2) — 2010 **15,0** ; 2011 9,3 ; 2012 **12,1** ; 2013 0,1 ; 2014 5,0 ; 2015 2,7 ; 2016 6,4 ; 2017 **10,9** ; 2018 6,7 ; 2019 6,4 ; 2020 8,4 ; 2021 0,9 ; 2022 4,1 ; 2023 0,8 ; 2024 0,4 ; 2025 5,8 ; 2026 4,9 (%).
3. **Durée des épisodes** : **par état : non calculée (indéterminé)** ; HMM global méd. 193–268 ; émission non calculée.
4. **Transitions** : diag **0.9995** (K2), **0.9995** (K3), **0.9987** (K4 S0), **0.9994** (K5 E4′) ; échanges avec B 0.0002–0.0007.
5. **Caractéristiques comportementales principales** : **storm_p90_run_month = 1** (vs 2 partout ailleurs — seul état avec le niveau 1), storm_clust **−0,73 à −0,89σ**, kurtosis **−0,46σ**, ext_spacing +0,45/+0,67σ, h1_acf1 −0,04/−0,17σ, noise −0,01/−0,26σ ; reste ≈ médiane.
6. **Méthodes/configurations** : HMM K2/K3/K4/K5 (fragmenté en K4/K5) ; **jamais retrouvé par K-means** (ni par HMM full-cov K2, qui retrouve R-E0).
7. **Récurrent ou événementiel** : présent toutes années mais **définition non stable** (poids 12,8–30,7 % selon K) et **signal porté par une feature quasi-constante** (MAD ≈ 0 → fallback std, z-score non interprétable ; seul le niveau discret 1 vs 2 est fiable).
8. **Niveau de confiance** : **LOW**.

---

## 7. Carte minimale proposée (3.6G)

> La carte minimale est **post-analytique, descriptive** ; elle ne retient **aucun K**, ne construit **aucun classifieur**, n'évalue **aucune performance**. Les noms sont des étiquettes de travail, issus des profils §3.3 de 3.6F.

### 7.1 États **récurrents** (à conserver comme hypothèses de travail structurantes)

| ID consolidé | Nom de travail | Base factuelle | Statut |
|---|---|---|---|
| **G-B** | État de référence | 58–99 %, continu 2010–2026, profil ≈ médiane, 8/8 configurations | Référence **obligatoire** — HIGH |
| **G-E2** | « queue droite modérée, extrêmes moins agrégés » | 4,2–4,8 %, 2013/2014/2016/2017 (≈ 93–97 %), KM K4+K5 + HMM K5 approchant, max épisode ≈ 22 600 | **Seul candidat multi-années hors référence** — MEDIUM (provisoire) |

**Ce que cela signifie** : la carte minimale comporte **deux éléments** — un état de référence dominant (G-B) et **un unique candidat récurrent** (G-E2), encore à confirmer (voir §7.3). **Aucun autre candidat ne satisfait** simultanément : ≥ 2 configurations, ≥ 2 années de présence, cohérence épisodique.

### 7.2 États **événementiels** — à ne **pas confondre** avec des régimes

| ID consolidé | Nom de travail | Base factuelle | Traitement recommandé |
|---|---|---|---|
| **G-E0** | « queue d'aplatissement extrême » (candidat anomalie de données) | 1,48 %, 2 fenêtres (2015-07-20→09-01 ; 2021-08-08→09-21), identique KM K2–K5 + HMM full K2 (ARI 1.0), profil −17,5σ/+30,5σ | **Hors carte de régimes** ; drapeau qualité de données (règle F3) ; validation source obligatoire avant tout usage |
| **G-E1** | « structure mèche-basse / début de période » | 4,5–4,7 %, 98 % en 2010, 6/6 configurations K≥3, noyau ≈ 27 100 bars | **Hors carte de régimes** en l'état : structure réelle mais **localisée 2010** ; possible artefact de bord de domaine (à valider avec l'audit 2010 / 3.6D) |

**Règle de non-confusion** : la concordance inter-méthodes (G-E1 = 6/6) **ne suffit pas** à faire un régime — le critère décisif est la **récurrence temporelle multi-années**, absente pour G-E0 (2 fenêtres) et pour G-E1 (2010 à 98 %).

### 7.3 Éléments **encore indéterminés**

1. **G-E3** (« volatilité jour/mois élevée ») : présente toutes années (pics 2011/2020) mais **1 seule configuration (HMM K5)** ; épisodes par état non calculés → **indéterminé**, à confirmer par reproduction (hors périmètre actuel).
2. **G-E4** (« mois sans extrêmes cumulés ») : poids **instable en K** (12,8–30,7 %), HMM-only, dépendance à une feature quasi-constante (`m3_storm_p90_run_month`, MAD ≈ 0) → **indéterminé**, à traiter comme structure faible ; la question du traitement de cette feature (sans suppression définitive) reste ouverte.
3. **Relation G-E2 ↔ HMM K5 s3** : profils proches mais atténués (skew +0,72σ vs +4,72σ) — **non tranchée** ; ne pas fusionner sans preuve supplémentaire.
4. **Fragment « X » de KM K5** (593 894, vol_ratio +1,03σ) : sans équivalent ailleurs, médiane d'épisode 1 → **fragmentation de frontière**, écarté.
5. **Statistiques d'épisodes par état pour le HMM** : non calculées dans les données disponibles (seules les médianes globales 193–268 existent) → **trou d'information** pour E3/E4/G-E2 côté HMM.
6. **Stabilité de G-E2 en full-covariance** : la structure K=2 de R-E0 n'apparaît qu'en full-cov ; l'effet du modèle de covariance sur G-E2 n'a pas été évalué.

### 7.4 Périmètre explicite de la carte minimale

- **Retenus (hypothèses)** : G-B (HIGH), G-E2 (MEDIUM).
- **Événements hors régimes** : G-E0 (anomalie F3), G-E1 (localisé 2010).
- **Indéterminés** : G-E3, G-E4, relation G-E2/HMM s3.
- **Écartés** : fragment X (KM K5), HMM K4 seed 1 (effondrement), HMM K4 seed 0 (état à ligne nulle) — solutions dégénérées/limites.
- **Non réalisé par conception** : choix définitif de K, classifieur, backtest, stratégie, modification de features.

---

## 8. Rappel des interdits respectés

- Aucun modèle lancé, aucun K recalculé, aucun K-means/HMM relancé — **aucune exécution de calcul** dans cette étape ;
- Aucune sélection définitive de K ; aucune sélection sur performance financière ;
- Aucun classifieur, aucun backtest, aucune stratégie, aucune modification de features ;
- **Un seul fichier créé** : `research/regime_engine/PHASE3_V2_REGIME_MAP_CONSOLIDATION.md` ;
- **Aucun commit, aucun push** ; STOP complet.

---

*Fin du rapport — Step 3.6G. Cartographie minimale provisoire (G-B, G-E2) ; G-E0/G-E1 événementiels ; G-E3/G-E4 indéterminés ; pas de K définitif, aucun classifieur, aucun backtest.*
