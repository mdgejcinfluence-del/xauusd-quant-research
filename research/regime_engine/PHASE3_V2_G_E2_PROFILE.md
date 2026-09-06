# PHASE 3 V2 — STEP 3.6H : PROFIL COMPORTEMENTAL FINAL — G-E2

- **Étape** : 3.6H — caractérisation finale du candidat de régime **G-E2** (identifié en 3.6G, « queue droite modérée, extrêmes moins agrégés », = R-E2 de 3.6F).
- **Sources UNIQUES** : `PHASE3_V2_REGIME_MAP_CANDIDATES.md` (3.6F) et `PHASE3_V2_REGIME_MAP_CONSOLIDATION.md` (3.6G). **Aucune autre donnée, aucun calcul.**
- **Ce rapport est descriptif** : aucune nouvelle exécution (pas de modèle, pas de clustering, pas de K, pas de parquet, pas de backtest, pas de stratégie, aucune modification de features).
- **Définition de G-E2 (rappel 3.6G)** : état récurrent candidat hors référence — « queue droite modérée, extrêmes moins agrégés » ; éléments factuels : KM K4 s1 (84 750 ; 4,49 %), KM K5 s0 (80 117 ; 4,24 %) et approchant HMM K5 s3 (90 099 ; 4,77 %) ; années 2013/2014/2016/2017 (~93–97 % de l'état).
- **Base de profil utilisée** : la signature canonique est celle de **KM K5 s0** (seule colonne E2 complète en §3.1/§3.2 de 3.6F) ; KM K4 s1 est qualifié « très proche » (6.3 de 3.6F) et les valeurs résumées de R-E2 (§8 de 3.6F) s'appliquent aux deux ; HMM K5 s3 est « approchant » (profil atténué, non identique) — il n'est **pas** fusionné dans la signature.

---

## 1. Signature des 25 features

Écarts robustes (z, unités MAD vs médiane globale) — signature **KM K5 s0** (3.6F §3.2) ; valeurs brutes entre parenthèses (3.6F §3.1).

| Feature | G-E2 (z) | Valeur brute | Lecture |
|---|---|---:|---|
| m3_skew_month | **+4.72** | **+2.43** | queue **droite** modérée |
| m3_kurtosis_month | **+6.22** | **101.1** | aplatissement **élevé** (mais ≈ 4× plus faible que G-E0 : 420.9) |
| m3_ext_spacing_month | **+1.12** | **18** | extrêmes **plus espacés** (vs 12 en médiane) |
| m3_storm_clust_month | **−0.85** | 0.297 | agrégats d'extrêmes **moins nombreux** |
| m3_ext_rate_month | −0.52 | 0.0148 | taux d'extrêmes M3 **plus faible** |
| m3_run_month | −0.46 | 1.909 | rafales directionnelles **plus courtes** |
| m3_range_sigma_day | −0.31 | 1.025 | dispersion jour **légèrement basse** |
| m3_tr_sigma_day | −0.31 | 1.029 | dispersion true-range **légèrement basse** |
| h1_vol_ratio_day_month | −0.23 | 0.821 | H1 vs mois **légèrement sous la normale** |
| m3_vol_ratio_day_month | −0.17 | 0.881 | M3 vs mois **légèrement sous la normale** |
| m3_acf1_day | −0.17 | −0.0365 | autocorrélation jour **légèrement plus négative** |
| m3_low_wick_day | −0.18 | 0.200 | mèche basse **légèrement plus courte** |
| m3_tr_expansion_day | −0.14 | −203.6 (bps) | expansion true-range **légèrement plus basse** |
| m3_close_pos_day | −0.12 | 0.498 | position de clôture **légèrement plus basse** |
| m3_ext_rate_day (m1_ext_rate_day) | −0.10 | 0.0139 | extrêmes M1 **légèrement plus rares** |
| h1_acf1_month | −0.09 | −0.0188 | autocorrélation H1 mois **faiblement négative** |
| m3_m1_noise_ratio | −0.03 | 1.014 | ratio bruit ≈ médiane |
| m3_dir_month | −0.03 | −0.0006 | direction mensuelle ≈ médiane |
| m3_vr2_month | −0.00 | 0.986 | variance ratio ≈ médiane |
| m3_body_range_day | +0.06 | 0.495 | corps ≈ médiane |
| m3_body_dir_day | +0.00 | 0 | direction du corps ≈ médiane |
| m3_scf_day | +0.16 | 0.518 | corrélation de série jour **légèrement haute** |
| m3_up_wick_day | +0.03 | 0.202 | mèche haute ≈ médiane |
| m3_ext_sign_month | +0.10 | 0.491 | signe des extrêmes ≈ médiane |
| m3_storm_p90_run_month | +0.00† | 2 | niveau 2 (≈ médiane ; pas de signal) |

† `m3_storm_p90_run_month` : quasi-constante (niveaux discrets, MAD ≈ 0 → fallback std) — z non interprétable ; niveau brut = **2**, identique à la médiane. **Le signal de G-E2 ne repose pas sur cette feature** (contrairement à G-E4).

**En résumé** : G-E2 est un état dont le profil est proche de la référence sur 20 features / 25 (|z| ≤ 0,52), et **différencié sur 4 features** : skew +4,72σ, kurtosis +6,22σ, ext_spacing +1,12σ, storm_clust −0,85σ (et, secondairement, ext_rate −0,52σ). La signature est donc **étroite et concentrée sur la famille des extrêmes** — elle ne touche ni la volatilité de dispersion (|z| ≤ 0,31), ni la structure des bougies (|z| ≤ 0,18), ni la directionnalité (|z| ≤ 0,46).

---

## 2. Familles comportementales dominantes

Classement par amplitude moyenne des z (signature KM K5 s0 ; familles définies dans la spec, lecture comportementale) :

1. **Famille EXTREMBES / aplatissement (DOMINANTE)** — |z| moyen ≈ 2,4-3,3 : `m3_skew_month` +4,72σ, `m3_kurtosis_month` +6,22σ, `m3_ext_spacing_month` +1,12σ, `m3_storm_clust_month` −0,85σ, `m3_ext_rate_month` −0,52σ, `m3_ext_sign_month` +0,10σ, `m1_ext_rate_day` −0,10σ, `m3_storm_p90_run_month` 0. **C'est la seule famille réellement séparatrice.**
2. **Famille VOLATILITÉ / dispersion** — modérée et **en retrait** : `m3_range_sigma_day` −0,31σ, `m3_tr_sigma_day` −0,31σ, `m3_tr_expansion_day` −0,14σ, `m3_vol_ratio_day_month` −0,17σ, `h1_vol_ratio_day_month` −0,23σ, `m3_m1_noise_ratio` −0,03σ, `m3_vr2_month` −0,00σ. Tendance : **dispersion jour et ratios de volume légèrement SOUS la norme** — G-E2 n'est pas un état de volatilité élevée.
3. **Famille PERSISTANCE / série** — secondaire : `m3_acf1_day` −0,17σ, `m3_scf_day` +0,16σ, `h1_acf1_month` −0,09σ, `m3_run_month` −0,46σ (le plus déviant de cette famille : **rafales plus courtes**).
4. **Famille STRUCTURE DES BOUGIES** — **quasi neutre** (|z| ≤ 0,18) : body_range +0,06σ, up_wick +0,03σ, low_wick −0,18σ, close_pos −0,12σ, body_dir +0,00σ.
5. **Famille DIRECTIONNALITÉ** — **neutre** : `m3_dir_month` −0,03σ, `m3_body_dir_day` +0,00σ.

> Conclusion famille : **G-E2 est un état de distribution (forme des queues et répartition temporelle des extrêmes), pas un état d'amplitude ni de direction.**

---

## 3. Volatilité

- **Niveau général** : **sous la référence** mais faiblement — `m3_range_sigma_day` 1,025 (−0,31σ), `m3_tr_sigma_day` 1,029 (−0,31σ), `m3_tr_expansion_day` −203,6 bps (−0,14σ).
- **Ratios d'échelle** : `m3_vol_ratio_day_month` 0,881 (−0,17σ), `h1_vol_ratio_day_month` 0,821 (−0,23σ) → la volatilité intra-jour (M3 et H1) est **légèrement en dessous** de la référence mensuelle ; `m3_vr2_month` 0,986 (≈ médiane).
- **Contraste explicite** (3.6F §1/§3, §8) : G-E2 **n'est pas** G-E3 — G-E3 est défini par `vol_ratio_day_month` **+3,08σ**, `h1_vol_ratio` **+2,46σ** ; G-E2 est dans la direction **opposée** (−0,17σ / −0,23σ).
- **Conclusion** : la volatilité ne définit pas G-E2 ; elle est **légèrement basse**, et surtout **aucune composante de volatilité n'atteint |z| ≥ 0,5** — G-E2 ne doit être ni utilisé ni lu comme un régime « haute volatilité ».

---

## 4. Persistance / directionnalité

**Persistance (auto-transition, matrices de 3.6F §4.3/§5) :**
- **KM K4 (E2)** : diag **0.9987** (empirique).
- **KM K5 (E2)** : diag **0.9973** (empirique) — la plus faible des lignes du modèle avec X.
- **HMM K5 (E2′)** : diag **0.9957** — **la plus faible de toutes les lignes HMM** (B 0.9997, E1 0.9997, E3 0.9960, E4′ 0.9994) ; c'est le candidat **le moins auto-persistant** de la carte.
- **HMM K4 (état « S1 » ≈ E2-ish)**: diag **0.9990** — cohérent, mais HMM K4 est instable (3.6F §7.2) → indicatif uniquement.

**Directionnalité :** `m3_dir_month` −0,03σ (médiane −0,0006), `m3_body_dir_day` +0,00σ, `m3_ext_sign_month` +0,10σ → **aucune asymétrie directionnelle** ; `m3_run_month` 1,909 (−0,46σ) indique des **rafales directionnelles plus courtes** que la référence, mais sans biais de signe. `m3_acf1_day` −0,0365 (vs −0,0251 en B) : autocorrélation journalière **un peu plus négative** (mémoire un peu plus courte), secondaire.

**Conclusion** : G-E2 est **persistant mais moins que tous les autres candidats** (0.9957–0.9987) et **directionnellement neutre** ; c'est cohérent avec un état de « forme de distribution » plutôt que de tendance.

---

## 5. Structure des bougies

| Caractéristique | G-E2 | B (référence) | E1 (contraste) |
|---|---:|---:|---:|
| body_range_day | 0,495 (+0,06σ) | 0,495 | 0,366 (−4,22σ) |
| low_wick_day | 0,200 (−0,18σ) | 0,203 | 0,378 (+7,62σ) |
| up_wick_day | 0,202 (+0,03σ) | 0,202 | 0,187 (−0,64σ) |
| close_pos_day | 0,498 (−0,12σ) | 0,500 | 0,618 (+4,29σ) |
| body_dir_day | 0 (+0,00σ) | 0 | +0,0064 (+0,20σ) |

- **Corps ≈ référence** ; **mèches ≈ référence** (mèche basse légèrement raccourcie, −0,18σ) ; position de clôture ≈ centre (0,498) ; corps directionnel ≈ neutre.
- **Contraste net avec G-E1** : G-E1 est la structure « mèche basse dominante » (low_wick +7,62σ, body_range −4,22σ, close_pos +4,29σ) ; **G-E2 n'a rien de cette signature** (|z| ≤ 0,18 sur tout le bloc bougies).
- **Conclusion** : la structure des bougies de G-E2 est **indiscernable de la référence** — ce n'est pas un critère de définition de G-E2, et c'est un point fort de distinction avec G-E1.

---

## 6. Comportement des extrêmes

**C'est le cœur de G-E2.** Les 4 features dominantes sont toutes de la famille des extrêmes, avec un sens opposé sur l'agrégation :

| Feature | G-E2 | B | G-E0 (contraste) | Sens |
|---|---:|---:|---:|---|
| m3_skew_month | **+2,43** (+4,72σ) | −0,100 | **−9,39** (−17,5σ) | queue **droite modérée** (G-E0 : queue gauche extrême) |
| m3_kurtosis_month | **101,1** (+6,22σ) | 21,6 | **420,9** (+30,5σ) | aplatissement élevé (G-E0 : extrême, ~4× plus) |
| m3_storm_clust_month | **0,297** (−0,85σ) | 0,356 | **0,389** (+0,95σ) | **moins** d'agrégats (G-E0 : plus) |
| m3_ext_spacing_month | **18** (+1,12σ) | 12 | 10 (−0,67σ) | extrêmes **plus espacés** (G-E0 : plus rapprochés) |
| m3_ext_rate_month | 0,0148 (−0,52σ) | 0,0156 | 0,0156 (+0,05σ) | extrêmes M3 un peu **plus rares** |
| m1_ext_rate_day | 0,0139 (−0,10σ) | 0,0146 | 0,0146 (+0,00σ) | extrêmes M1 ≈ norme |
| m3_ext_sign_month | 0,491 (+0,10σ) | 0,484 | 0,473 (−0,31σ) | signe ≈ neutre |
| m3_storm_p90_run_month | **2** | 2 | 2 | niveau médian (pas de signal) |

**Lecture comportementale** : un mois type de G-E2 = **distribution à queue droite modérée et aplatissement élevé, mais avec des extrêmes moins fréquents et surtout plus espacés / moins regroupés** que la normale — la queue droite est « épaisse mais dispersée ». C'est exactement l'opposé de G-E0 (queue gauche extrême + agrégats forts) sur l'axe agrégation, et un ordre de grandeur plus doux sur l'axe queues.

---

## 7. Stabilité temporelle

- **Concentré 2013–2017** (~93–97 % des lignes de l'état ; 3.6F §6.3/§6.6, 3.6G §4) ;
- **Structure épisodique** : KM K4 = 102 épisodes, KM K5 = 219 épisodes ; **médiane d'épisode = 1 bar** (basculements de frontière K-means K≥3 — limitation connue, 3.6F §7.2.6), **moyenne 368–832**, **max ≈ 22 600 bars** (bloc continu principal) — il existe donc un **noyau continu** malgré la fragmentation de frontière ;
- **Stabilité inter-K** : tailles KM K4 84 750 / KM K5 80 117 (écart 5,5 %), profils résumés identiques (§8 3.6F : skew +4,7σ, kurt +6,2σ, spacing +1,1σ, storm_clust −0,85σ, ext_rate −0,5σ pour K4 et K5) ; **HMM K5 s3 est « approchant » mais atténué** (skew +0,72σ, kurt +1,0σ, storm_clust −0,87σ) — **ni fusionné ni ignoré** ; coexistence signalée en 3.6G §7.3.3 comme non tranchée ;
- **Stabilité des étiquettes K-means** : KM K4 ARI seeds 0.885/0.885/0.9999 (une permutation entre deux états), KM K5 ARI 0.988/0.978/0.974 → la **partition** est stable à ~1–2 %, l'identité fine de l'état l'est aussi à ce titre ;
- **Pas d'occurrence en 2010-2012, 2015, 2018-2025** (0 % ; seul 2024 à 0,7 % pour KM K4 et 2026 à 2,9–3,1 %) → **présence par blocs, pas continue**.

---

## 8. Années de présence

| Année | KM K5 s0 (%) | KM K4 s1 (%) |
|---|---:|---:|
| 2010–2012 | 0 | 0 |
| 2013 | **28.2** | **26.7** |
| 2014 | **19.0** | **18.4** |
| 2015 | 0 | 0 |
| 2016 | **35.1** | **35.5** |
| 2017 | **14.6** | **15.8** |
| 2018–2023 | 0 | 0 |
| 2024 | 0 | 0.7 |
| 2025 | 0 | 0 |
| 2026 | **3.1** | **2.9** |

(3.6F §6.3 ; totaux des lignes de l'état par année — l'état est confiné à un sous-ensemble de la série, pas de répartition sur toute la période.)

**Lecture** : 4 années dominantes (**2013, 2014, 2016, 2017**, ≈ 93–97 % cumulés) avec une **coupure 2015** ; apparition résiduelle **2026** (≈ 3 %) et 2024 (0,7 % seulement en K4) ; **absence totale 2018–2023**. La présence est donc **récurrente sur plusieurs années disjointes** — c'est le seul candidat non-référence avec cette propriété (G-E0 = 2 fenêtres ; G-E1 = 2010 ; G-E3 = mono-configuration ; G-E4 = définition instable), d'où son statut MEDIUM/HIGH de candidat en 3.6G.

---

## 9. Transitions typiques

**KM K4** (ordre B, E2, E1, E0 ; empirique — 3.6F §5.1) :
```
B  → B 0.9998  E2 0.0001  E1 0.0002  E0 0.0000
E2 → B 0.0013  E2 0.9987  E1 0.0000  E0 0.0000
```

**KM K5** (ordre E2, E0, X, E1, B ; empirique — 3.6F §5.1) :
```
E2 → E2 0.9973  E0 0.0000  X 0.0018  E1 0.0000  B 0.0010
B  → E2 0.0001  E0 0.0000  X 0.0173  E1 0.0001  B 0.9825
```

**HMM K5** (ordre E4′, E1, B, E2′, E3 ; paramètres du modèle — 3.6F §5.2) :
```
B   → E2′ 0.0001
E2′ → E4′ 0.0020  B 0.0020  E2′ 0.9957  E3 0.0003
E3  → E2′ 0.0005
```

**Synthèse des trajectoires typiques :**
- **séjour prolongé** : diag 0.9957–0.9987 (mais la **plus faible** de tous les candidats) ;
- **sortie dominante → G-B (référence)** : E2→B 0.0010–0.0020 (KM K5 → B ; HMM K5 → B) ; vers B 0.0013 (KM K4) ;
- **échanges secondaires** : K-means K5 E2↔X (0.0018 / 0.0002 — l'état-fragment X étant un artefact de frontière, cette transition est peu interprétable) ; HMM K5 E2′↔E4′ (0.0020 / 0.0004) et E3→E2′ (0.0005) — très faibles ;
- **entrée dominante depuis B** : 0.0001 (K-means K4/K5, HMM K5).

En pratique, G-E2 est un état **atteint rarement depuis la référence et quitté principalement vers la référence**, avec un séjour plus court que B/E0/E1/E4 mais non trivial (séjour HMM ~ 1/0.0057 ≈ du même ordre que les autres candidats ; aucune transition « charnière » n'émerge — 3.6F §5).

---

## 10. Distinction avec G-B, G-E0 et G-E1

| Dimension | **G-E2** | **G-B (référence)** | **G-E0 (queue extrême)** | **G-E1 (mèche basse/2010)** |
|---|---|---|---|---|
| Fréquence | 4,2–4,8 % (80–90 k) | 58–99 % (1,10–1,86 M) | 1,48 % (27 901) | 4,5–4,7 % (85–88 k) |
| Features dominantes | skew **+4,7σ**, kurt **+6,2σ**, spacing **+1,1σ**, clust **−0,85σ** | ≈ médiane (|z| ≤ 0,3) | skew **−17,5σ**, kurt **+30,5σ**, vr2 −2,9σ, clust **+0,95σ** | low_wick **+7,6σ**, body_range **−4,2σ**, close_pos **+4,3σ**, sigma +1,5σ, vr2 +1,7σ |
| Queue | **droite modérée** | ≈ nul | **gauche extrême** | ≈ nul |
| Agrégation des extrêmes | **moins** d'agrégats (clust −0,85σ ; spacing +1,1σ) | neutre (0,356 ; 12) | **plus** d'agrégats (clust +0,95σ ; spacing −0,67σ) | neutre (0,340 ; 12) |
| Volatilité jour | **légèrement basse** (−0,17/−0,23σ ; sigma −0,31σ) | ≈ médiane (sigma 1,061 / +0,08σ-état) | sigma −0,38/−0,39σ | sigma **+1,55/+1,65σ** |
| Structure bougies | **≈ référence** (|z| ≤ 0,18) | ≈ médiane | ≈ référence (body_range −0,26σ) | **contrastée** (low_wick ↑↑, body ↓↓, close ↑↑) |
| Directionnalité | **neutre**, run −0,46σ | neutre | vr2 −2,9σ, signe −0,31σ | neutre (run −0,91σ) |
| Années | **2013, 2014, 2016, 2017** (+2026 ≈ 3 %) | toutes | **2015 + 2021 seulement** | **2010 (98 %)** + traces |
| Épisodes | 102–219 ; méd. 1 ; **max ~22 600** ; moy. 368–832 | K2 : 3 ép. (566 628) ; K≥3 fragmenté | **exactement 2** (13 952 / 13 950) | 258–266 ; méd. 1 ; max ~27 100 |
| Persistance | **0.9957–0.9987** (la plus faible) | 0.9825–1.0 | **0.9999** (absorbant) | 0.9969–0.9997 |
| Configurations | KM K4 + KM K5 (+ HMM K5 s3 approchant) | 8/8 | KM K2–K5 + HMM full (ARI 1.0) | 6/6 K≥3 |
| Statut 3.6G | **récurrent (MEDIUM)** | référence (HIGH) | **événement/anomalie F3** | **localisé 2010** |

**Distinctions clés en une phrase :**
- vs **G-B** : mêmes bougies/volatilité, mais G-E2 est **différencié sur la forme des queues** (skew/kurtosis) et l'agrégation des extrêmes — G-B est le profil médian, G-E2 en est un écart circonscrit ;
- vs **G-E0** : **signe opposé de la queue** (droite vs gauche) et **sens opposé de l'agrégation** (moins vs plus) ; G-E0 est ~4× plus extrême en kurtosis et strictement événementiel (2 fenêtres), G-E2 est multi-années ;
- vs **G-E1** : G-E1 est un état de **structure des bougies** (mèches/corps/clôture) avec volatilité **élevée** ; G-E2 est un état de **distribution des extrêmes** avec bougies ≈ référence et volatilité **légèrement basse** — leur seul point commun est la taille (~4,5 %) et la faible persistance relative.

---

## Conclusion

### Pourquoi G-E2 peut être considéré comme **régime candidat**
1. **Récurrence temporelle multi-années** : présent en 4 années distinctes (2013, 2014, 2016, 2017, ≈ 93–97 % de l'état) — seule structure (hors référence) avec cette propriété ; présence résiduelle 2026 (~3 %).
2. **Reproduction inter-paramétrisation** : retrouvé dans 2 configurations K-means indépendantes (K4 s1, K5 s0) avec tailles (84 750 / 80 117) et profils résumés identiques (skew +4,7σ, kurt +6,2σ, spacing +1,1σ, clust −0,85σ, ext_rate −0,5σ) ; **concordance inter-familles approchée** via HMM K5 s3 (même sens sur clust −0,87σ, même famille d'extrêmes, mais atténué) — sans s'y limiter.
3. **Signature comportementale cohérente et interprétable** : un seul axe dominant (forme de distribution : queue droite modérée + aplatissement élevé + extrêmes moins fréquents et plus espacés), toutes les autres familles ≈ référence → le signal est **sélectif**, pas un artefact de proportion.
4. **Structure épisodique avec noyau continu** : max ≈ 22 600 bars et moyenne 368–832 → des **blocs prolongés** existent malgré la fragmentation de frontière K-means (limitation documentée).
5. **Non confondu avec les anomalies connues** : G-E2 n'est pas G-E0 (pas de skew −17σ/30σ, pas de coïncidence avec les règles F3), n'est pas confiné à 2010 — il est donc **distinct des deux signaux de qualité de données** identifiés en 3.6F/3.6G.

### Ce qui manque encore pour le considérer comme **régime final**
1. **Confirmation inter-famille exacte** : le correspondant HMM (K5 s3) est « approchant » et **atténué** (skew +0,72σ vs +4,72σ) ; la relation G-E2 ↔ HMM K5 s3 est **non tranchée** (3.6G §7.3.3). Sans elle, la concordance est 2 configurations + 1 approchante, pas 2 familles fermes.
2. **Statistiques d'épisodes côté HMM** : non disponibles (seules médianes globales 193–268 bars) — la durée de séjour HMM de G-E2 est **inconnue** ; le caractère « régime » (épisodes longs vs basculements) n'est pas établi côté modèle séquentiel.
3. **Diagnostic de la fragmentation K-means** : médiane d'épisode = 1 bar (mosaïques de frontière, 3.6F §7.2.6) — la définition opérationnelle de G-E2 (seuil de séjour) reste à fixer ; les moyennes/max indiquent un noyau, mais sa borne temporelle précise n'est pas établie.
4. **Stabilité en full-covariance** : l'effet du modèle de covariance sur G-E2 n'a pas été évalué (3.6G §7.3.6) ; or le sanity K2 a montré que la structure dépend fortement de la diagonale vs full (ARI −0.0154). La robustesse de G-E2 à cette hypothèse est un point ouvert majeur.
5. **Robustesse au traitement des features quasi-constantes / données 2010-2023** : skew/kurtosis mensuels sont des fenêtres longues et sensibles aux anomalies de queues (F3) ; la stabilité de G-E2 si les anomalies sont exclues **n'a pas été testée** (aucune suppression/altération autorisée à ce stade).
6. **Critères de sélection non financiers non fournis** : pas de test de significativité, pas de hold-out, pas de critère de stabilité bootstrappé — conformément aux interdits, **aucun de ces contrôles n'a été exécuté** et ils sont nécessaires avant toute qualification de « régime final ».

### Observations qui ne doivent **surtout pas** être confondues avec G-E2
1. **G-E0** (queue gauche extrême, +30,5σ, agrégats ↑, 2 fenêtres 2015/2021) : même famille « extrêmes » mais **signe opposé** (skew gauche) et **agrégation opposée** (clust ↑, spacing ↓) ; jamais considérer la queue extrême comme « version forte de G-E2 ».
2. **G-E1** (mèche basse, corps réduit, clôture haute, sigma ↑, 2010) : taille similaire (~4,5 %) mais **structure des bougies et volatilité opposées** — une confusion G-E2/G-E1 mélangerait distribution et microstructure.
3. **G-E3** (volatilité jour/mois +3,1σ/+2,5σ, m1_ext_rate +1,7σ) : amplement **au-dessus** de la norme de volatilité ; G-E2 est **en dessous** (−0,17/−0,23σ). Ne pas lire G-E2 comme « volatilité élevée ».
4. **G-E4** (storm_p90_run = 1, 12,8–30,7 %, HMM-only) : repose sur `m3_storm_p90_run_month` (quasi-constante, MAD ≈ 0) ; **G-E2 est au niveau 2 et ne dépend pas de cette feature**.
5. **Fragment « X » KM K5** (593 894 lignes, vol_ratio +1,03σ) : artefact de fragmentation K5, à ne pas assimiler à G-E2 (taille ~7× et profil différent).
6. **État « S1 » du HMM K4** : seulement « E2-ish » et issu du HMM K=4 **instable** (seed 1 effondré, seed 0 à ligne nulle) — ne pas utiliser comme preuve de G-E2.
7. **Toute interprétation économique ou financière** : explicitement **hors périmètre** à toutes les étapes (3.6F §8.2, 3.6G §8) — G-E2 est décrit en termes comportementaux uniquement.

---

*Fin du rapport — Step 3.6H. Aucun modèle, aucun clustering, aucun K, aucun calcul, aucun parquet, aucun backtest, aucune modification de features ; sources exclusives 3.6F + 3.6G ; aucun commit, aucun push.*
