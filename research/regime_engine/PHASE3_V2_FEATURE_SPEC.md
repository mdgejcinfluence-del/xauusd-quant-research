# PHASE 3 V2 — STEP 3.2 : FEATURE SPECIFICATION (CANDIDATE SET, FROZEN)

**Date :** 2026-09-06 (UTC) · **Référence :** `PHASE3_V2_DATA_CONTRACT.md` (DATA_CONTRACT = FROZEN)
**Portée :** spécification uniquement — aucun dataset, aucune segmentation, aucun backtest, aucune optimisation.
**Statut :** `FEATURE SPECIFICATION — FROZEN CANDIDATE SET` (candidat : pré-sélection, pas de sélection finale).
**Rupture V1 :** l'ancien moteur 31-features est abandonné ; aucun nom, aucune formule, aucune fenêtre, aucun MIN_OBS, aucune constante de la V1 n'est réutilisé ou référencé. Toute ressemblance avec des descripteurs classiques (ACF, variance ratio, kurtosis) est une redéfinition V2 autonome.

---

## 0. CONVENTIONS PARTAGÉES (partie intégrante de chaque formule)

### 0.1 Grilles et alignement
- Grilles : M1 (maître, 5 874 003 lignes), M3 (1 963 826 barres), H1 (98 412 barres) — uniquement les grilles validées Phase-2B (contrat §2).
- **Ancre de ligne :** toute feature est définie **sur une barre M3 `t`** (contrat A1). M1 et H1 sont des **entrées** alignées sur `t`.
- `T(t)` = heure de début (bord de bucket) de la barre M3 `t`, en minutes UTC entières, multiple de 3.
- `endM1(t)` = dernière minute M1 ≤ `T(t)+2` (existe toujours : une barre M3 existe ssi ≥ 1 M1 réel).
- `h(t)` = `floor((T(t)+2)/60)` = barre H1 dont le bucket contient la minute `T(t)+2` ; les valeurs H1 utilisées sont celles des barres H1 d'indice ≤ `h(t)` (bucket fermé — **jamais** une barre H1 se terminant après `T(t)+2`).
- Indices : `i` position de barre dans la grille (ordre `bar_id` croissant) ; `s` indice interne de fenêtre.

### 0.2 Séries primitives
- `C_R(i)`, `O_R(i)`, `H_R(i)`, `L_R(i)` : OHLC réels de la grille R (aucune modification).
- `r_R(i) = ln C_R(i) − ln C_R(i−1)` pour `i > 1` ; `r_R(1) = NaN`.
- `R_bps(i) = 10000·(H_R(i) − L_R(i)) / C_R(i)` (range en points de base).
- `TR_R(i) = max(H−L, |H − C_R(i−1)|, |L − C_R(i−1)|)` ; `TR_bps(i) = 10000·TR_R(i)/C_R(i−1)` ; `i=1` → NaN. Si `C_R(i−1) ≤ 0` (impossible en pratique mais épinglé) → NaN.
- `sign_R(i) = +1/−1/0` selon `r_R(i) > 0 / < 0 / = 0` ; `sign( NaN ) = 0`.
- **Pas propre :** `clean_R(i) = 1` ssi `contig_next_R(i) = 1` (compteur d'intégrité des grilles ; pour M1, minutes consécutives). Si `r_R(i)` est NaN → `clean = 0`.

### 0.3 Fenêtres (positions, pas d'horloge murale — contrat GAP_POLICY)
| Nom | Valeur | Positions | Nominal wall-clock |
|---|---|---|---|
| `W3_D` | 480 | M3 | ≈ 1 440 min (1 jour) |
| `W3_M` | 14 400 | M3 | ≈ 43 200 min (30 jours) |
| `W1_D` | 1 440 | M1 | ≈ 1 440 min (1 jour) |
| `W1_D` (M1 → M3) | 1 440 | M1, dernières positions ≤ `endM1(t)` | ≈ 1 jour |
| `WH_D` | 24 | H1 | ≈ 1 440 min |
| `WH_M` | 336 | H1 | ≈ 20 160 min (14 jours) |

- Fenêtre de positions `[i−W+1, i]` **incluse en i** ; si `i < W` → feature NaN (règle de disponibilité générale).
- Fenêtre M1 alignée sur `t` : les **W1_D dernières barres M1** de minute ≤ `endM1(t)`.

### 0.4 Estimateurs épinglés (déterminisme)
- `var_S(x)` = variance d'échantillon **ddof=1** ; `std_S(x) = sqrt(var_S(x))`.
- `mean(x)` = moyenne arithmétique ; `med(x)` = percentile 50 **interpolation linéaire** (convention numpy).
- `p90(x)` = percentile 90, interpolation linéaire.
- `ACF1(x)` = coefficient de corrélation de Pearson (pairwise-complete) entre `x_s` et `x_{s−1}` sur les paires où les deux existent.
- `skew(x)` = `m3/m2^{3/2}`, moments **population (ddof=0)** : `mk = mean((x−mean)^k)`.
- `kurt_excess(x)` = `m4/m2² − 3` (ddof=0).
- `VR(x, q)` = `Var(Σ_{j=1..q} x_{b·q+j}) / (q · Var(x))` sur blocs **non chevauchants** de `q` pas consécutifs **tous propres**, calculés dans l'ordre des positions, avec `Var` ddof=1 sur chacun des deux termes ; les blocs invalides sont ignorés.
- Aucun nombre aléatoire, aucune donnée externe, aucune interpolation temporelle.

### 0.5 Règles globales (gaps / NaN / disponibilité)
- **Gaps :** les fenêtres portent sur la séquence de positions ; un gap ne décale rien, ne comble rien. Les pas non propres (`clean=0`) sont exclus des statistiques de retours ; les barres de type « stub » de rollover sont des barres réelles : elles **restent** dans les statistiques de forme (C/D) et leur effet est une propriété documentée (extrêmes conservés, contrat EXTREME_POLICY) — jamais supprimées.
- **NaN général :** NaN ssi (a) `i < W`, ou (b) nombre d'observations valides `< MIN_OBS` de la feature, ou (c) dénominateur non fini ou nul (règle feature), ou (d) entrée non finie. **Aucun remplissage** (ni forward ni backward) : NaN reste NaN.
- **Début d'échantillon :** warm-up = `W` positions (global max = 14 400 positions M3 ≈ 30 jours) ; pas de backfill ; les NaNs de warm-up sont attendus et documentés.
- **Zéros vs NaN :** un taux nul (0 extrême, 0 saturation) est une valeur VALIDE ; NaN est réservé aux cas indéfinis (0 extrême classables pour les ratios conditionnels, dénominateurs nuls).
- **Seuils de classification (E/F) :** pour une barre dont `σ_prev` est indéfini → **flag = 0** (non classable ≠ extrême), le dénominateur de comptage est alors `n_eval` = nombre de barres classables ; NaN ssi `n_eval < MIN_OBS`.

---

## FEATURE SPECIFICATION — FROZEN CANDIDATE SET

### FAMILLE A — VOLATILITÉ RELATIVE

---
#### `m3_vol_ratio_day_month`
- **Famille :** A · **Niveau :** M3 (calcul) — entrées M3 (ligne M3 `t`)
- **Formule :** `V = σ_M3(t; 480) / σ_M3(t; 14400)` où `σ_R(i;W) = std_S({ r_R(s) : s ∈ [i−W+1, i], clean_R(s)=1 })`
- **Horizon :** court 480 positions / long 14 400 positions (M3)
- **MIN_OBS :** 120 (court) et 3 600 (long), sinon NaN
- **Unités :** sans dimension (ratio de volatilités)
- **Justification comportementale :** compare l'énergie du jour au mois : >1 = accélération (régime de tension), <1 = compression (régime calme) — premier signal de régime de volatilité.
- **PIT :** les deux fenêtres se terminent en `t` (fermeture du bar `t`) ; aucun indice > t.
- **Gaps :** statistiques sur pas propres uniquement ; un grand gap ne décale pas la fenêtre, il réduit `n_eval` (NaN si < MIN_OBS).
- **NaN :** (a) `i < 480` ou `i < 14400`, (b) `n_eval < MIN_OBS` sur l'une des deux fenêtres, (c) `σ = 0` → NaN (ratio non défini).
- **Disponibilité :** première valeur finie après 14 400 barres M3 (≈ 30 jours), puis continue ; jamais rempli.

---
#### `m3_m1_noise_ratio`
- **Famille :** A · **Niveau :** M3 (ligne) — entrées M3 + **M1 substrate**
- **Formule :** `N = √3 · σ_M1^(t; 1440) / σ_M3^(t; 480)`, avec `σ_M1^(t;1440)` calculé sur les 1 440 dernières barres M1 de minute ≤ `endM1(t)` (pas 1-min propres) et `σ_M3^(t;480)` comme A-1.
- **Horizon :** 1 440 positions M1 / 480 positions M3
- **MIN_OBS :** 360 (M1) / 120 (M3)
- **Unités :** sans dimension ; ≈1 sous marche aléatoire, >1 = micro-bruit M1 excédentaire, <1 = M1 « lisse » relatif (efficience d'échelle).
- **Justification comportementale :** mesure la proportion de bruit microstructurel vs mouvement porteur (facteur √3 = correction d'échelle de diffusion) — propriété comportementale d'échelle.
- **PIT :** fenêtres se terminant en `t` / `endM1(t)` ; `endM1(t)` est la dernière minute du bucket M3 fermé.
- **Gaps :** pas propres M1 uniquement ; les fenêtres ne sont pas ré-échantillonnées.
- **NaN :** (a) fenêtre incomplète, (b) `n_eval < MIN_OBS`, (c) `σ_M3 = 0`.
- **Disponibilité :** after 1 440 positions M1 et 480 M3 → depuis ~1 jour M3.

---
#### `h1_vol_ratio_day_month`
- **Famille :** A · **Niveau :** M3 (ligne) — entrées **H1 context** (barres ≤ `h(t)`)
- **Formule :** `Vh = σ_H1(h(t); 24) / σ_H1(h(t); 336)`
- **Horizon :** 24 / 336 positions H1
- **MIN_OBS :** 12 / 84
- **Unités :** sans dimension
- **Justification comportementale :** même signal de tension/compression que A-1 mais au niveau contexte horaire — complémentaire (H1 absorbe complètement les chocs M1, Phase-2B §9.1e).
- **PIT :** barre H1 `h(t)` fermée (bucket contenant `T(t)+2`, dernière minute M3 du bar `t`) ; fenêtres se terminant en `h(t)`.
- **Gaps :** pas propres H1 (contig_next H1) ; taux de discontinuité H1 4,30 % → `n_eval` réduit, NaN si < MIN_OBS.
- **NaN :** idem A-1 + dénominateur nul.
- **Disponibilité :** après 336 barres H1 (≈ 14 jours).

### FAMILLE B — PERSISTANCE / DÉPENDANCE DIRECTIONNELLE

---
#### `m3_acf1_day`
- **Famille :** B · **Niveau :** M3
- **Formule :** `ACF1 = corr_Pearson({r(s)}, {r(s−1)})` sur `s ∈ [t−479, t]`, paires avec `clean(s)=clean(s−1)=1`
- **Horizon :** 480 positions
- **MIN_OBS :** 120 paires valides
- **Unités :** sans dimension ([−1, 1])
- **Justification comportementale :** dépendance à court terme des retours M3 (tendance ou reversion) — propriété de persistance.
- **PIT :** paires `(s−1, s)` avec s ≤ t ; aucun futur.
- **Gaps :** seules les paires proprement consécutives comptent (les paires traversant une fermeture sont exclues).
- **NaN :** fenêtre incomplète ou < 120 paires ; `std=0` → NaN.
- **Disponibilité :** après 480 positions M3.

---
#### `m3_vr2_month`
- **Famille :** B · **Niveau :** M3
- **Formule :** `VR2 = Var(blocs de 2 pas propres consécutifs) / (2 · Var(1 pas propre))` sur `[t−14399, t]`, estimateur §0.4
- **Horizon :** 14 400 positions, q=2, blocs non chevauchants
- **MIN_OBS :** 3 600 blocs valides
- **Unités :** sans dimension ; 1 = marche aléatoire, >1 = continuation, <1 = reversion (à horizon 2)
- **Justification comportementale :** second estimateur (non chevauchant) de la persistance — complémentaire de l'ACF (estimateur chevauchant) ; les deux sont conservés car leurs sous-échantillonnages diffèrent (leçon Phase-2B §3.2b, non-additivité documentée).
- **PIT :** blocs entièrement dans `[t−14399, t]` ; aucun bloc ne déborde en `t+1`.
- **Gaps :** un bloc est valide ssi ses 2 pas sont `clean` ; les blocs invalides sont ignorés.
- **NaN :** fenêtre incomplète ou < 3 600 blocs.
- **Disponibilité :** après 14 400 positions M3.

---
#### `m3_scf_day`
- **Famille :** B · **Niveau :** M3
- **Formule :** `SCF = #{ s : sign(s) ≠ sign(s−1), tous deux non nuls } / #{ s : les deux signes non nuls }`, `s ∈ [t−479, t]`, pas propres
- **Horizon :** 480 positions
- **MIN_OBS :** 120 paires à signes non nuls
- **Unités :** [0, 1] ; 0,5 = alternance neutre, >0,5 = alternance élevée (reversion), <0,5 = sérialité
- **Justification comportementale :** fréquence de retournement signe — descripteur de persistance complémentaire à l'ACF, robuste aux queues.
- **PIT :** paires `(s−1, s)` ≤ t.
- **Gaps :** paires propres uniquement ; `r=0` exclu de la paire (ni changement ni continuation) et `sign=0` brise les courses (B-4).
- **NaN :** fenêtre incomplète ou < 120 paires.
- **Disponibilité :** après 480 positions.

---
#### `m3_run_month`
- **Famille :** B · **Niveau :** M3
- **Formule :** `RUN = N_runs_nonzero / N_bars_nonzero` sur `[t−14399, t]` (signes non nuls ; `sign=0` casse la course), pas propres, les `r=NaN` non comptés
- **Horizon :** 14 400 positions
- **MIN_OBS :** 3 600 signes non nuls
- **Unités :** barres (longueur moyenne de course)
- **Justification comportementale :** longueur moyenne des séquences directionnelles — persistance à l'échelle mensuelle.
- **PIT :** fenêtre ≤ t.
- **Gaps :** une fermeture casse une course (pas non propre exclu) — comportement documenté : les courses ne traversent pas les marchés fermés.
- **NaN :** fenêtre incomplète, < 3 600 signes, ou `N_runs = 0`.
- **Disponibilité :** après 14 400 positions.

---
#### `m3_dir_month`
- **Famille :** B · **Niveau :** M3
- **Formule :** `DIR = mean({r(s) propre, s ∈ [t−14399, t]}) / std_S(même ensemble)`
- **Horizon :** 14 400 positions
- **MIN_OBS :** 3 600 retours propres
- **Unités :** sans dimension (dérive par unité de volatilité)
- **Justification comportementale :** force directionnelle nette du mois — distingue un marché en dérive d'un marché en retournement neutre.
- **PIT :** fenêtre ≤ t.
- **Gaps :** pas propres uniquement.
- **NaN :** fenêtre incomplète, < 3 600, ou `std = 0`.
- **Disponibilité :** après 14 400 positions.

---
#### `h1_acf1_month`
- **Famille :** B · **Niveau :** M3 (ligne) — entrées H1 ≤ `h(t)`
- **Formule :** `ACF1_h = corr_Pearson({r_H1(s)}, {r_H1(s−1)})`, `s ∈ [h(t)−335, h(t)]`, paires propres H1
- **Horizon :** 336 positions H1
- **MIN_OBS :** 84 paires
- **Unités :** sans dimension
- **Justification comportementale :** persistance du contexte horaire — qualité de contexte indépendante du niveau M3.
- **PIT :** `h(t)` fermé ; paires ≤ `h(t)`.
- **Gaps :** paires propres H1 (contig_next H1) ; contiguïté H1 95,7 % → n_eval réduit.
- **NaN :** fenêtre incomplète (< 336 barres H1 depuis le début), < 84 paires, std nul.
- **Disponibilité :** après 336 barres H1 (≈ 14 jours).

### FAMILLE C — AMPLITUDE / EXCURSIONS

---
#### `m3_range_sigma_day`
- **Famille :** C · **Niveau :** M3
- **Formule :** `M = med({ R_bps(s) / (10000·σ_prev(s; 480)) : s ∈ [t−479, t], R_bps fini, σ_prev fini non nul })`, `σ_prev(s;480) = std_S` sur positions `[s−480, s−1]` (retours propres)
- **Horizon :** 480 positions (ratio évalué en `s`, référence σ en `s−1`)
- **MIN_OBS :** 120 barres valides
- **Unités :** sans dimension (range en unités de σ)
- **Justification comportementale :** excursion typique du bar par rapport à la volatilité passée — « amplitude relative du bar » (référence Phase-2B : ~1,07 médian M3).
- **PIT :** `s ≤ t` ; σ de la fenêtre `[s−480, s−1]` strictement antérieure.
- **Gaps :** barres de rollover (range gonflé par la fermeture) incluses — propriété réelle, non retirée.
- **NaN :** fenêtre incomplète, < 120, σ_prev nul (ratio non défini → barre exclue).
- **Disponibilité :** après 480 positions + 480 précédentes → en pratique ~960 positions.

---
#### `m3_tr_sigma_day`
- **Famille :** C · **Niveau :** M3
- **Formule :** `MT = med({ TR_bps(s) / (10000·σ_prev(s; 480)) : s ∈ [t−479, t] })` (mêmes conventions)
- **Horizon :** 480 positions
- **MIN_OBS :** 120 barres
- **Unités :** sans dimension
- **Justification comportementale :** comme C-1 mais avec le **true range** (capte les trous inter-barres) — l'écart C-1/C-2 mesure la part d'« excitation » des gaps dans l'amplitude.
- **PIT :** identique C-1 (TR_bps utilise `C_R(s−1)`, passé).
- **Gaps :** TR intègre explicitement les sauts de fermeture — c'est l'objet de la feature.
- **NaN :** idem C-1 ; `TR` non fini → barre exclue.
- **Disponibilité :** idem C-1.

---
#### `m3_tr_expansion_day`
- **Famille :** C · **Niveau :** M3
- **Formule :** `E = mean({ 10000·ln(TR_bps(s) / TR_bps(s−1)) : s ∈ [t−479, t], les deux finis et > 0 })`
- **Horizon :** 480 positions (deltas à pas 1)
- **MIN_OBS :** 120 deltas valides
- **Unités :** bps (log-delta de TR par barre)
- **Justification comportementale :** tendance d'expansion/décompression de l'amplitude — signal d'évolution du régime (le retard d'expansion suit la volatilité de manière propre).
- **PIT :** deltas entre `s−1` et `s`, `s ≤ t`.
- **Gaps :** un delta traversant une fermeture reste calculé sur les barres réelles (TR des deux barres), pas de ré-échantillonnage — le pas de temps physique varie ; documenté.
- **NaN :** fenêtre incomplète, < 120 deltas, l'un des deux TR = 0 ou non fini (delta exclu).
- **Disponibilité :** après 480 positions.

### FAMILLE D — STRUCTURE DES BOUGIES / COMPACITÉ

*Tous : médiane (interpolation linéaire) sur `[t−479, t]`, barres M3 avec `H−L > 0` ; MIN_OBS 120 barres non dégénérées ; unités [0,1] (D-5 : [−1,1]) ; PIT : `s ≤ t`, OHLC du bar `s` fermé ; gaps : les stubs de rollover sont inclus (propriété réelle) ; NaN : fenêtre incomplète, < 120 barres valides, ou dénominateur nul ; disponibilité : après 480 positions + 1 (les valeurs de forme exigent le bar fermé).*

---
**`m3_body_range_day`** — D · M3
- Formule : `med({ |C(s)−O(s)| / (H(s)−L(s)) })`
- Justification comportementale : compacité du corps vs amplitude totale — barres « pleines » (impulsion) vs « doji » (indécision).
- PIT : OHLC de `s` ; fenêtre ≤ t.

**`m3_up_wick_day`** — D · M3
- Formule : `med({ (H(s) − max(O(s), C(s))) / (H(s)−L(s)) })`
- Justification comportementale : part de la mèche haute — rejet de hauts / pression vendeuse en fin de barre ; propriété de structure.

**`m3_low_wick_day`** — D · M3
- Formule : `med({ (min(O(s), C(s)) − L(s)) / (H(s)−L(s)) })`
- Justification comportementale : part de la mèche basse — rejet de bas / pression acheteuse.

**`m3_close_pos_day`** — D · M3
- Formule : `med({ (C(s) − L(s)) / (H(s)−L(s)) })`
- Justification comportementale : position de clôture dans le range — déséquilibre fin de barre (0 = clôture au plus bas, 1 = au plus haut).

**`m3_body_dir_day`** — D · M3
- Formule : `med({ (C(s) − O(s)) / (H(s)−L(s)) })`
- Justification comportementale : corps directionnel signé — intensité de la direction du bar relative à son amplitude (borne [−1, 1]).
- Note : distinct de D-4 (clôture vs étendue totale) ; les quatre captures d'ombre/corps/position sont complémentaires et non dérivées linéairement (D-5 = D-4 − D-1·signe... en fait non : indépendants par construction, documenté).

*(Commentaire de non-redondance : D-2 + D-3 + D-1 = 1 par barre ; D-4 et D-5 partagent des entrées mais mesurent des quantités différentes ; aucun n'est une combinaison linéaire d'un autre.)*

### FAMILLE E — QUEUE / ÉVÉNEMENTS EXTRÊMES

*Flag de base (épinglé V2) : `ext(s) = 1` ssi `|r_M3(s)| > 3 · σ_prev(s; 480)` (σ_prev défini, non nul, n_eval ≥ 120 sinon flag 0). Forme algébrique identique à la règle descriptive Phase-2B, mais **redéfinie ici** comme règle V2 autonome (aucun flag Phase-2B hérité).*

---
#### `m3_ext_rate_month`
- **Famille :** E · **Niveau :** M3 · **Formule :** `n_ext / n_eval` sur `[t−14399, t]` (bars classables) · **Horizon :** 14 400 · **MIN_OBS :** 3 600 classables · **Unités :** [0,1]
- **Justification comportementale :** fréquence d'événements extrêmes relative à la volatilité courante — intensité du régime de queues.
- **PIT :** `ext(s)` n'utilise que `[s−480, s−1]` + `r(s)` ; `s ≤ t`.
- **Gaps :** `σ_prev` sur pas propres ; un bar à σ indéfini → flag 0 (non classable, compté au dénominateur uniquement via n_eval).
- **NaN :** fenêtre incomplète ou < 3 600 classables · **Disponibilité :** après 14 400 + 480 positions.

---
#### `m3_kurtosis_month`
- **Famille :** E · **Niveau :** M3 · **Formule :** `kurt_excess({r propre, [t−14399, t]})` · **MIN_OBS :** 3 600 · **Unités :** sans dimension (0 = gaussien)
- **Justification comportementale :** épaisseur de queue — les marchés de régime « choc » ont des queues plus lourdes (Phase-2B : kurtosis M3 ×2,72 après 2013).
- **PIT :** fenêtre ≤ t · **Gaps :** pas propres · **NaN :** fenêtre incomplète, < 3 600, `var = 0` · **Disponibilité :** après 14 400 positions.

---
#### `m3_skew_month`
- **Famille :** E · **Niveau :** M3 · **Formule :** `skew({r propre, [t−14399, t]})` · **MIN_OBS :** 3 600 · **Unités :** sans dimension
- **Justification comportementale :** asymétrie de la distribution des rendements — direction des grosses excursions.
- **PIT :** idem · **Gaps :** idem · **NaN :** idem + `var = 0` · **Disponibilité :** idem.

---
#### `m1_ext_rate_day`
- **Famille :** E · **Niveau :** M3 (ligne) — **entrées M1** · **Formule :** `n_ext1 / n_eval1` sur les 1 440 dernières barres M1 ≤ `endM1(t)`, avec `ext1(s) = 1` ssi `|r_M1(s)| > 3·σ1_prev(s; 1440)` (σ1_prev sur `[s−1440, s−1]`, pas 1-min propres, MIN_OBS 360 sinon flag 0) · **Horizon :** 1 440 positions M1 · **MIN_OBS :** 360 classables · **Unités :** [0,1]
- **Justification comportementale :** taux d'événements microstructurels M1 (chocs de 1 minute) — contextualisation des extrêmes M1 dans le bar M3 (contrat : extrêmes M1 contextualisés, jamais supprimés).
- **PIT :** `endM1(t)` = dernière minute du bucket M3 fermé ; fenêtres ≤ `endM1(t)`.
- **Gaps :** pas propres 1-min ; 3 708 fermetures ≥ 50 min → n_eval réduit mais ≥ 1 400 la plupart du temps.
- **NaN :** fenêtre incomplète (barres M1 couvertes < 1 440) ou < 360 classables · **Disponibilité :** après ~1 jour de M1 (les 1 440 premières positions) — plus tôt que les features M3 longues.

---
#### `m3_ext_sign_month`
- **Famille :** E · **Niveau :** M3 · **Formule :** `#{ext & r>0} / n_ext` sur `[t−14399, t]` · **Horizon :** 14 400 · **MIN_OBS :** 30 extrêmes (sinon NaN) · **Unités :** [0,1] (>0,5 = surreprésentation positive)
- **Justification comportementale :** asymétrie directionnelle des événements extrêmes — « qui » porte les queues.
- **PIT :** `ext` passif (E-1), signe de `r(s)`, `s ≤ t` · **Gaps :** idem E-1 · **NaN :** fenêtre incomplète ou `n_ext < 30` · **Disponibilité :** après 14 400 positions + événements suffisants.

### FAMILLE F — STRUCTURE TEMPORELLE / CLUSTERING (mesurable sans ambiguïté, sans volume)

*Base : flag `ext` de E-1 sur M3. Aucune donnée de volume, aucun horaire de session (voir exclusions).*

---
#### `m3_storm_clust_month`
- **Famille :** F · **Niveau :** M3
- **Formule :** `C = mean({ hit(s) : s extreme, s ∈ [t−14399, t−5] })`, `hit(s) = 1` ssi au moins un des `ext(s+1..s+5) = 1`
- **Horizon :** 14 400 positions (paires à distance ≤ 5 barres)
- **MIN_OBS :** 30 extrêmes éligibles (s+5 ≤ t), sinon NaN
- **Unités :** [0,1] — part des extrêmes suivis d'un extrême dans les 5 barres
- **Justification comportementale :** regroupement temporel des chocs (clustering) — propriété de structure temporelle mesurable sur les retours seuls. Référence Phase-2B : probabilité intra-5 ≈ 0,34 vs 0,076 attendu (M3) — l'objet est re-mesuré ici, aucune valeur héritée.
- **PIT :** `s+5 ≤ t` — la fenêtre de co-occurrence reste ≤ t ; aucun `t+1`.
- **Gaps :** les distances sont en POSITIONS (pas en minutes) ; une fermeture entre `s` et `s+5` ne casse pas la fenêtre (documenté : la « proximité temporelle » est en barres de marché, pas en minutes d'horloge).
- **NaN :** fenêtre incomplète ou < 30 extrêmes éligibles · **Disponibilité :** après 14 400 positions + 5.

---
#### `m3_storm_p90_run_month`
- **Famille :** F · **Niveau :** M3
- **Formule :** `P90` (interpolation linéaire) des longueurs de courses consécutives `ext=1` dans `[t−14399, t]`
- **Horizon :** 14 400 positions
- **MIN_OBS :** 30 extrêmes au total, sinon NaN
- **Unités :** barres
- **Justification comportementale :** longueur typique des épisodes de chocs consécutifs — persistance des tempêtes.
- **PIT :** courses entièrement ≤ t.
- **Gaps :** une course se poursuit à travers une fermeture si les barres voisines sont extrêmes (positionnel) — documenté.
- **NaN :** fenêtre incomplète ou < 30 extrêmes · **Disponibilité :** idem F-1.

---
#### `m3_ext_spacing_month`
- **Famille :** F · **Niveau :** M3
- **Formule :** `med({ positions(s_{j+1}) − positions(s_j) : extrêmes conjoints dans [t−14399, t] })`
- **Horizon :** 14 400 positions
- **MIN_OBS :** 30 extrêmes (donc ≥ 29 écarts), sinon NaN
- **Unités :** barres
- **Justification comportementale :** espacement médian entre événements extrêmes — échelle de retour des tempêtes.
- **PIT :** écarts entre positions ≤ t.
- **Gaps :** mêmes conventions positionnelles.
- **NaN :** fenêtre incomplète ou < 30 extrêmes · **Disponibilité :** idem.

---

## TABLEAU RÉCAPITULATIF (25 candidats)

| # | Nom canonique | Famille | Niveau (ligne M3 ; entrées) | Fenêtre | MIN_OBS | Unités |
|---|---|---|---|---|---|---|
| 1 | `m3_vol_ratio_day_month` | A | M3 | 480 / 14 400 | 120 / 3 600 | — |
| 2 | `m3_m1_noise_ratio` | A | M3 + M1 | 1 440 M1 / 480 M3 | 360 / 120 | — |
| 3 | `h1_vol_ratio_day_month` | A | M3 + H1 | 24 / 336 H1 | 12 / 84 | — |
| 4 | `m3_acf1_day` | B | M3 | 480 | 120 paires | — |
| 5 | `m3_vr2_month` | B | M3 | 14 400 | 3 600 blocs | — |
| 6 | `m3_scf_day` | B | M3 | 480 | 120 paires | — |
| 7 | `m3_run_month` | B | M3 | 14 400 | 3 600 signes | barres |
| 8 | `m3_dir_month` | B | M3 | 14 400 | 3 600 | — |
| 9 | `h1_acf1_month` | B | M3 + H1 | 336 H1 | 84 paires | — |
| 10 | `m3_range_sigma_day` | C | M3 | 480 | 120 | — |
| 11 | `m3_tr_sigma_day` | C | M3 | 480 | 120 | — |
| 12 | `m3_tr_expansion_day` | C | M3 | 480 | 120 deltas | bps |
| 13 | `m3_body_range_day` | D | M3 | 480 | 120 barres | — |
| 14 | `m3_up_wick_day` | D | M3 | 480 | 120 barres | — |
| 15 | `m3_low_wick_day` | D | M3 | 480 | 120 barres | — |
| 16 | `m3_close_pos_day` | D | M3 | 480 | 120 barres | — |
| 17 | `m3_body_dir_day` | D | M3 | 480 | 120 barres | — |
| 18 | `m3_ext_rate_month` | E | M3 | 14 400 | 3 600 | [0,1] |
| 19 | `m3_kurtosis_month` | E | M3 | 14 400 | 3 600 | — |
| 20 | `m3_skew_month` | E | M3 | 14 400 | 3 600 | — |
| 21 | `m1_ext_rate_day` | E | M3 + M1 | 1 440 M1 | 360 | [0,1] |
| 22 | `m3_ext_sign_month` | E | M3 | 14 400 | 30 extrêmes | [0,1] |
| 23 | `m3_storm_clust_month` | F | M3 | 14 400 (+5) | 30 extrêmes | [0,1] |
| 24 | `m3_storm_p90_run_month` | F | M3 | 14 400 | 30 extrêmes | barres |
| 25 | `m3_ext_spacing_month` | F | M3 | 14 400 | 30 extrêmes | barres |

## VÉRIFICATIONS (avant implémentation)

**Déterminisme :** toute formule est une fonction pure des OHLC committées (grilles validées) ; estimateurs épinglés au §0.4 (ddof, interpolation de quantiles, moments population, blocs VR) ; aucune source aléatoire, aucune heure locale, aucune donnée externe, aucune interpolation temporelle, aucun ré-échantillonnage ; l'alignement M3→M1/H1 utilise des minutes UTC entières via `floor`/`endM1` (données réelles).

**PIT (aucune information future) :** audit ligne par ligne — chaque fenêtre est `[i−W+1, i]` (ou `≤ endM1(t)` / `≤ h(t)`) ; aucune formule ne contient `t+k` (k ≥ 1), aucun `rolling(center=True)`, aucun `shift(-k)`, aucune normalisation globale ; `m3_storm_clust_month` restreint explicitement les événements éligibles à `s+5 ≤ t` ; `σ_prev` n'utilise que `[s−W, s−1]` ; `h(t)` est le bucket H1 **fermé** contenant la dernière minute du bar M3 `t`. Toute implémentation future devra prouver ces points par audit de troncature dynamique (écart exactement nul) avant usage.

---

## FEATURES REJECTED BEFORE IMPLEMENTATION

| Candidat rejeté | Raison précise |
|---|---|
| Toute feature dérivée du **volume** (volume ratio, volume-weighted return, turnover proxy, barres à volume nul) | `VOLUME_POLICY = EXCLUDED` (unité inconnue, L1, contrat §1) — jamais chargé, jamais dérivé |
| **Niveaux de prix absolus** et moyennes mobiles USD (close − MA, price position absolue) | Non stationnaire ; nécessiterait des ancres/paramètres exogènes ; ne décrit pas une propriété comportementale intrinsèque ; contrat « behavioral only » |
| **Signaux de stratégie** (crossovers MA, momentum lags optimisés, stops/résistances) | Hors périmètre pré-stratégie ; introduirait des paramètres non justifiés et un risque de surapprentissage avant toute analyse de régimes |
| **Timeframes non validées** (M2, M5, M10, M15, M20, M30, H2, H4) | Contrat §2 : seules les grilles M1/M3/H1 validées Phase-2B sont autorisées |
| **Horaires de session / jour de semaine** (heure UTC, harmoniques du jour, indicateur week-end) | Ambigu : les minutes manquantes rendent la position calendaire ≠ position de marché ; propriété comportementale non mesurable sans ambiguïté ; les 5 fenêtres UTC Phase-2B sont descriptives, non héritées (contrat §5) ; équivalent retiré même en version « part des extrêmes 16–21 UTC » |
| **Order-flow / spread / depth / tick / bid-ask** | Aucune donnée externe disponible (contrainte 5) ; données indisponibles et non reproductibles |
| **Normalisation globale** (z-score full-sample, min-max plein échantillon, quantiles globaux) | Look-ahead indirect (contrainte 6) — toute normalisation future devra être **causale** et spécifiée séparément ; aucune feature de ce spec n'en dépend |
| **Fenêtres centrées** (moyennes centrées, convolutions `center=True`) | Contrainte 2 — interdit ; aucune feature de ce spec n'en utilise |
| **Tout `t+k`** (rendement suivant, ratio volatilité future, issue à `t+5`) | PIT_POLICY — interdit ; c'était la structure de défauts de la V1 (C3/D5), définitivement abandonnée |
| **`m1_path_day_raw_bps`** (somme des |retours M1| du jour, bps bruts) | Redondant avec `m3_m1_noise_ratio` (même source d'information) ; variante « niveau d'activité » non normalisée → ce serait une feature de niveaux, rejetée pour la même raison que les niveaux de prix |
| **Feature « 2013 break flag »** (indicateur de changement de convention) | Split calendaire non PIT-safe en tant que feature comportementale ; la rupture 2013 reste documentée pour les analyses de stabilité (contrat §5), pas un input de feature |
| **Flags hérités Phase-2B** (`m1_ext`, `r3_ext` comme colonnes de classification) | Aucune valeur héritée : les règles d'extrêmes V2 sont redéfinies autonomes dans ce spec (§E) ; les colonnes Phase-2B ne sont pas des productions contractuelles |
| **Features de gap / qualité de données** (taux de trous internes, nb de ruptures) | Propriétés d'intégrité, pas comportementales ; déjà portées par les compteurs de grille — hors famille A–F ; leur inclusion biaiserait les régimes par des artefacts de collecte |

---

```
FEATURE SPECIFICATION — FROZEN CANDIDATE SET
N_CANDIDATES = 25
FAMILIES = A:3  B:6  C:3  D:5  E:5  F:3
PIT = VERIFIED BY CONSTRUCTION (all windows past-only, indices <= t, closed-bucket alignment)
DETERMINISM = VERIFIED (frozen estimators, no RNG, no external data, no interpolation)
NORMALIZATION = NONE IN THIS SPEC (any future normalization must be causal and separately specified)
HEIRARCHY = M3 anchor row / M1 substrate inputs / H1 context inputs
SELECTION / K / CLUSTERING = NOT DONE (next steps only after this freeze)
```
