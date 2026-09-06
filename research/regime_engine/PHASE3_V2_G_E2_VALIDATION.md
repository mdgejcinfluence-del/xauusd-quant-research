# PHASE 3 V2 — STEP 3.6I : VALIDATION DU RÉGIME CANDIDAT G-E2

- **Étape** : 3.6I — déterminer si **G-E2** peut être retenu comme régime comportemental de la cartographie finale.
- **Sources UNIQUES** : `PHASE3_V2_REGIME_MAP_CANDIDATES.md` (3.6F), `PHASE3_V2_REGIME_MAP_CONSOLIDATION.md` (3.6G), `PHASE3_V2_G_E2_PROFILE.md` (3.6H). **Aucune autre donnée, aucun calcul, aucun modèle, aucun K, aucun backtest, aucune stratégie, aucune modification de features.**
- **Objet évalué** : G-E2 = « queue droite modérée, extrêmes moins agrégés » — KM K4 s1 (84 750 ; 4,49 %), KM K5 s0 (80 117 ; 4,24 %), HMM K5 s3 (90 099 ; 4,77 %, « approchant/atténué »).
- **Règle de verdict (définie ici, appliquée systématiquement)** :
  - **ACCEPT** si : (a) stabilité KM K4/K5 **établie**, (b) concordance HMM **établie** (pas seulement approchante), (c) récurrence multi-années **établie**, (d) persistance **suffisante** ;
  - **REJECT** si : échec d'un critère **structurant** (concordance inter-familles, récurrence, persistance) sans possibilité de résolution par les données disponibles ;
  - **UNCERTAIN** sinon : candidat **plausible mais non établi** — statut intermédiaire explicite, sans acceptation ni rejet.

---

## 1. Stabilité entre KM K4 / KM K5 — PASS (fort)

| Critère | KM K4 s1 | KM K5 s0 |
|---|---|---|
| Taille | 84 750 (4,49 %) | 80 117 (4,24 %) |
| Écart tailles | — | **5,5 %** |
| Profil résumé | skew +4,7σ ; kurt +6,2σ ; spacing +1,1σ ; clust −0,85σ ; ext_rate −0,5σ | identiques (3.6F §8) |
| Années | 2013 26,7 ; 2014 18,4 ; 2016 35,5 ; 2017 15,8 ; 2026 2,9 ; 2024 0,7 | 2013 28,2 ; 2014 19,0 ; 2016 35,1 ; 2017 14,6 ; 2026 3,1 ; 2024 0 |
| Épisodes | 102 | 219 |
| Médiane épisode | 1 (fragmentation) | 1 (fragmentation) |
| Moyenne/Max | 368–832 / ≈ 22 600 | identiques (bloc 2013–2017) |
| Persistance (diag) | 0.9987 | 0.9973 |
| ARI seeds (partition) | 0.885 / 0.885 / 0.9999 | 0.988 / 0.978 / 0.974 |

**Lecture** : tailles à 5,5 % ; profils résumés (les 5 features discriminantes) **identiques** ; répartitions annuelles quasi superposées (écarts ≤ 1,5 point) ; persistance du même ordre (0.9987 vs 0.9973) ; épisodes K5 plus nombreux avec un seul noyau continu (max/moyenne identiques — le « 219 vs 102 » reflète la fragmentation de frontière, pas une structure différente). La différence K4/K5 est donc **paramétrique, pas structurelle**. La seule baisse notable (ARI seeds K4 0.885) concerne la **permutation de deux états entre seeds** (identifiée 3.6F §7.2) ; la partition K4 reste correcte à 88,5 % minimum, et le profil G-E2 est stable entre K4 et K5.

**Verdict partiel : STABLE.** L'écart de tailles (5,5 %), l'écart d'épisodes (facteur 2) et l'ARI K4 0.885 introduisent une **incertitude de frontière**, mais pas une instabilité de la structure.

---

## 2. Concordance avec HMM K5 — PARTIEL (décisif, insuffisant)

| Dimension | KM K4/K5 (G-E2 canonique) | HMM K5 s3 (E2′) |
|---|---|---|
| Taille | 80 117–84 750 | 90 099 |
| skew | **+4,72σ** (+2,43) | **+0,72σ** — 6,6× plus faible |
| kurtosis | **+6,22σ** (101,1) | **+1,0σ** — 6,2× plus faible |
| storm_clust | **−0,85σ** (0,297) | **−0,87σ** (≈ identique) |
| ext_spacing | +1,12σ (18) | **+0,90σ** (3.6H §6 ; « approchant ») |
| ext_rate | −0,52σ | **−0,47σ** (3.6H §4/§7) |
| run | −0,46σ | +0,03σ (pas le trait −0,46σ) |
| vr2 | −0,00σ | **−0,22σ** (pas le trait −0,00σ) |
| Années | 2013/2014/2016/2017 | **non disponible dans les données de E2′** (3.6G §7.3.5 : stats par état HMM non calculées) |
| Persistance (diag) | 0.9987 / 0.9973 | **0.9957** |
| Épisodes | 102–219 (méd. 1) | **non disponibles** |

**Lecture** : l'accord est **réel mais partiel** — même direction sur le bloc critique (skew/kurtosis positifs, storm_clust nettement négatif, ext_rate légèrement bas, ext_spacing élevé) ; **désaccord quantitatif net** sur l'intensité (skew/kurtosis ≈ 6× plus faibles) et **désaccord sur deux traits secondaires** (run et vr2, de sens opposés). La taille est proche (4,77 % vs 4,24–4,49 %). **Ce n'est pas une concordance établie** : c'est une **concordance de famille** (distribution à queue droite + extrêmes moins agrégés) **non confirmée en intensité**, et **non vérifiée sur la récurrence temporelle** (stats par état HMM indisponibles).

**Verdict partiel : PARTIEL — non établi.** Sans ça, aucun candidat de la carte minimale 3.6G ne peut être accepté par la règle définie ici, puisque la concordance inter-familles est **structurante** (c'est le critère qui a séparé les candidats 3.6G).

---

## 3. Récurrence multi-années — PASS (le point fort)

- Années dominantes (KM K5 s0 / KM K4 s1) : **2013 (28,2 / 26,7 %) · 2014 (19,0 / 18,4 %) · 2016 (35,1 / 35,5 %) · 2017 (14,6 / 15,8 %)**, cumul ≈ 93–97 % ; présence résiduelle **2026 (3,1 / 2,9 %)** et 2024 (0,7 % en K4 uniquement) ; **absence 2018–2025** (sauf 2024 K4) ; **coupure 2015**.
- La conformité 3.6G a retenu G-E2 comme seul candidat non-référence avec cette propriété (G-E0 : 2 fenêtres 2015/2021 ; G-E1 : 2010 à 98 % ; G-E3 : 1 configuration ; G-E4 : poids instable en K).
- **Nature de la récurrence** : **par blocs** (2013–2014, 2016–2017) — non continue, mais **disjointe sur 4 années calendaires** → récurrence temporelle **réelle**, distincte d'un événement ponctuel.

**Verdict partiel : RÉCURRENT** (multi-années). Caveat : les années montrent la **distribution de l'état**, pas la durée des épisodes (stats HMM par état indisponibles ; media K-means = 1 bar).

---

## 4. Persistance des épisodes — PARTIEL (décisif, insuffisant)

- **K-means** : diag **0.9987 (K4)** et **0.9973 (K5)** — fortes, mais **empiriques sur étiquettes dures**, biaisées par la fragmentation de frontière (3.6F §4.3).
- **HMM K5 E2′** : diag **0.9957** — la **plus faible de toutes les lignes HMM** (B 0.9997, E1 0.9997, E3 0.9960, E4′ 0.9994).
- **Durées** : médiane d'épisode **= 1 bar** (K-means K4/K5) ; **moyenne 368–832** ; **max ≈ 22 600 bars** (un noyau continu) ; **HMM par état indisponible** (seule la médiane globale 193–268 bars est publiée).

**Lecture** : il existe **un noyau continu** (max 22 600 bars ≈ 47 jours à 3 min), ce qui écarte l'hypothèse « artefact pur de frontière » ; mais la **durée de séjour typique** n'est pas établie : la médiane d'un bar signifie que la majorité des excursions est courte (basculements), et la persistance HMM (0.9957) étant la plus faible de la carte, G-E2 est **le candidat le moins « collant »** — ce qui est compatible avec un régime épisodique, mais n'est **pas** une démonstration de régime soutenu.
- **Sensibilité** : l'écart diag K4/K5 (0.9987 vs 0.9973) et K-means/HMM (0.9973–0.9987 vs 0.9957) est **petit mais systématique** ; le caractère « régime » repose sur le noyau (22 600) et la moyenne (368–832), **pas sur la persistance**.

**Verdict partiel : PARTIEL — non établi.** Persistance intrinsèque plus faible que tous les autres candidats ; épisodes par état HMM inconnus.

---

## 5. Cohérence de la signature comportementale — PASS (fort)

- **Un seul axe dominant** : famille **extrêmes/aplatissement** — skew +4,72σ, kurtosis +6,22σ, ext_spacing +1,12σ, storm_clust −0,85σ (+ ext_rate −0,52σ). **Toutes les autres familles ≈ référence** (volatilité |z| ≤ 0,31 ; bougies |z| ≤ 0,18 ; directionnalité |z| ≤ 0,46 ; persistance/série |z| ≤ 0,46).
- **Sens cohérent** : queue droite + aplatissement élevé + extrêmes **moins fréquents** et **plus espacés** = « queue épaisse mais dispersée ». La co-signature clust ↓ / spacing ↑ est **mutuellement cohérente** (moins d'agrégats ↔ plus d'espacement).
- **Indépendance** : le signal ne repose **pas** sur `m3_storm_p90_run_month` (niveau 2, ≈ médiane) — contrairement à G-E4 ; **pas** de dépendance à la structure des bougies (|z| ≤ 0,18) — contrairement à G-E1 ; **pas** de dépendance à la volatilité (|z| ≤ 0,31) — contrairement à G-E3.
- **Cohérence interne** : la même signature (5 features) apparaît **identique** dans KM K4 s1 et KM K5 s0 (3.6F §8, 3.6H §7) ; le HMM K5 s3 est dans la même famille avec la même direction sur les traits critiques (voir §2).

**Verdict partiel : COHÉRENT** — la signature est **sélective, interprétable, sans redondance avec les autres candidats**.

---

## 6. Distinction avec G-B, G-E0 et G-E1 — PASS (fort)

| Dimension | G-E2 | G-B | G-E0 | G-E1 |
|---|---|---|---|---|
| Famille dominante | extrêmes/aplatissement (queue droite) | ≈ médiane | extrêmes/aplatissement (queue gauche) | microstructure (bougies + sigma) |
| Queues | skew +2,43 ; kurt 101,1 | skew −0,100 ; kurt 21,6 | skew **−9,39** ; kurt **420,9** | skew −0,088 ; kurt 10,6 |
| Agrégation | **clust −0,85σ ; spacing +1,12σ** | neutre (0,356 ; 12) | **clust +0,95σ ; spacing −0,67σ** | neutre (0,340 ; 12) |
| Volatilité | sigma −0,31σ ; ratios −0,17/−0,23σ | ≈ médiane | sigma −0,38/−0,39σ | sigma **+1,55/+1,65σ** |
| Bougies | **≈ réf** (|z| ≤ 0,18) | ≈ médiane | ≈ réf | **low_wick +7,62σ ; body −4,22σ ; close +4,29σ** |
| Direction | neutre ; run −0,46σ | neutre | vr2 −2,91σ ; signe −0,31σ | run −0,91σ |
| Années | 2013/2014/2016/2017 (+2026 3 %) | toutes | 2015 + 2021 | 2010 (98 %) |
| Persistance | 0.9957–0.9987 | 0.9825–1.0 | 0.9999 | 0.9969–0.9997 |

- **vs G-B** : même structure de bougies/volatilité, mais G-E2 est différencié sur la **forme des queues** et l'agrégation des extrêmes — il n'est pas un simple repli de la référence.
- **vs G-E0** : **signe opposé de la queue** (droite vs gauche) et **sens opposé de l'agrégation** (moins vs plus) ; G-E0 est **événementiel** (2 fenêtres, 2015/2021), G-E2 est **multi-années**. G-E2 n'est pas « une version faible de G-E0 ».
- **vs G-E1** : familles **disjointes** — G-E1 = microstructure mèches/corps/clôture + sigma élevé ; G-E2 = forme de distribution, bougies ≈ réf, sigma bas. Leur ressemblance se limite à la taille (~4,5 %) et à la faible persistance relative.

**Verdict partiel : DISTINCT** (aucun chevauchement conceptuel ou temporel avec les autres candidats de la carte).

---

## 7. Sensibilité aux deux configurations voisines E2 / E2′

Deux sensibilités distinctes :

**a) Entre KM K4 (E2) et KM K5 (E2′)** — sensibilité **faible** : tailles 84 750 vs 80 117 (5,5 %), profils des 5 features discriminantes identiques, répartitions annuelles ≈ superposées, persistance 0.9987 vs 0.9973. La structure G-E2 est **stable** à travers le changement K.

**b) Entre KM K5 (E2) et HMM K5 (E2′)** — sensibilité **élevée** (le point décisif) :
- **Très sensible** : intensity skew/kurtosis (4,72σ/6,22σ → 0,72σ/1,0σ, facteur ≈ 6) et les traits `run` (−0,46σ → +0,03σ) et `vr2` (−0,00σ → −0,22σ) — **inversion de direction** sur deux traits secondaires, et un **écart de 6× sur le cœur de la signature**.
- **Insensible** : storm_clust (−0,85σ vs −0,87σ), ext_rate (−0,52σ vs −0,47σ), ext_spacing (+1,12σ vs +0,90σ), taille (4,24–4,49 % vs 4,77 %).
- **Non testable** : récurrence temporelle et épisodes de E2′ (stats par état HMM absentes).

**Lecture de la sensibilité** : la structure « extrêmes moins agrégés » est **robuste à l'approximation** (4-5 traits stables), mais l'état **exact** — « queue droite modérée » au sens de skew +4,72σ / kurt +6,22σ — **est spécifique au K-means** : le HMM K5 voit la même famille avec une intensité ≈ 6× plus faible. La carte doit donc être **sobre** : G-E2 (K-means) et E2′ (HMM) partagent une **famille comportementale**, pas un état quantifié identique.

---

## VERDICT FINAL

# REGIME_CANDIDATE_UNCERTAIN

### Justification (une ligne)
G-E2 **passe** 4 critères sur 7 (stabilité inter-K, récurrence multi-années, cohérence de signature, distinction avec les autres candidats) mais **échoue à établir** les 2 critères structurants restants — **concordance exacte avec le HMM K5** (même famille, intensité 6× plus faible, traits secondaires inversés, aucune info temporelle) et **persistance des épisodes** (médiane = 1 bar côté K-means, diag 0.9957 = plus faible de la carte, épisodes HMM par état inconnus) — et est **sensible** à la configuration E2/E2′.

### Détail des 7 critères

| # | Critère | Verdict partiel | Poids | Justification |
|---|---|---|---|---|
| 1 | Stabilité KM K4/K5 | ✅ **PASS** | haut | tailles 5,5 % ; profils identiques ; années ≈ superposées ; persistance 0.9987/0.9973 |
| 2 | Concordance HMM K5 | ⚠️ **PARTIEL — non établi** | **structurant** | même famille ; skew/kurt **6× plus faibles** ; run/vr2 inversés ; récurrence E2′ non vérifiée |
| 3 | Récurrence multi-années | ✅ **PASS** | haut | 2013 (28,2 %), 2014 (19,0 %), 2016 (35,1 %), 2017 (14,6 %) ; 2026 ~3 % ; absence 2018–2025 |
| 4 | Persistance des épisodes | ⚠️ **PARTIEL — non établi** | **structurant** | diag HMM 0.9957 (plus faible) ; médiane ép. = 1 bar (K-means) ; noyau 22 600 ; stats HMM inconnues |
| 5 | Cohérence de la signature | ✅ **PASS** | haut | axe unique (extrêmes) ; co-signature clust ↓ / spacing ↑ ; indépendance storm_p90/bougies/volatilité |
| 6 | Distinction G-B/G-E0/G-E1 | ✅ **PASS** | haut | familles disjointes : queues (signe/agrégation) vs microstructure vs référence |
| 7 | Sensibilité E2 / E2′ | ⚠️ **SENSIBLE (partiel)** | moyen | robuste sur 5 traits ; divergence 6× sur cœur (skew/kurt) ; 2 inversions secondaires |

### Ce que l'UNCERTAIN permet (et ne permet pas)
- **Permet** : conserver G-E2 dans la cartographie finale **comme candidat en attente** — distinct, récurrent, cohérent ; c'est le **seul candidat non-référence** avec récurrence multi-années et profil sélectif.
- **Ne permet pas** : qualifier G-E2 de régime **final** ni de régime **établi** — la concordance inter-familles et la persistance ne sont pas démontrées ; la carte finale doit le présenter **avec le statut UNCERTAIN** (et non comme régime confirmé).

### Conditions de levée (pour ACCEPT ou REJECT — non exécutées ici)
1. **Concordance HMM** : comparaison directe de partition/états KM K4/K5 vs HMM K5 (nécessaire : réutilisation des labels/échantillons, stats par état HMM — sans nouveau modèle) ; si ARI/mesure de chevauchement ≥ 0,7 et intensités cohérentes → **ACCEPT** ; si structures disjointes → **REJECT**.
2. **Persistance** : statistiques d'épisodes HMM par état (durées médianes/moyennes/max et nombre de séjours de E2′) ; si durée typique ≥ seuil d'un régime (ex. hors battements de frontière) → **ACCEPT** ; si épisodes tous courts → **REJECT**.
3. **Récurrence de E2′** : répartition annuelle du HMM K5 s3 (non disponible dans les données courantes) — élément nécessaire pour confirmer (ou infirmer) la récurrence 2013/2014/2016/2017.
4. **Robustesse au modèle de covariance** (3.6H §Conclusion) : G-E2 en full-cov — si la concordance dégrade → **REJECT** ; sinon renforce l'ACCEPT.
5. **Sensibilité au traitement des features** (anomalies F3, features quasi-constantes) : non testée — élément de précaution avant décision finale.

> **Aucune de ces conditions n'a été exécutée** (aucun calcul, aucune donnée, aucun modèle) — elles sont listées comme **prérequis d'une décision future**, hors périmètre 3.6I.

---

*Fin du rapport — Step 3.6I. Verdict : REGIME_CANDIDATE_UNCERTAIN. Aucun modèle, aucun K, aucun calcul, aucun backtest, aucune stratégie, aucune modification de features ; sources exclusives 3.6F–3.6H ; aucun commit, aucun push.*
