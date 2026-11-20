# PHASE 12.1 — VALIDATION MATHÉMATIQUE ET TECHNIQUE DU BLUEPRINT

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**Statut : PHASE 12.1 TERMINÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**
Validation documentaire et mathématique du blueprint seq 144, accepté comme
*architecture* (ni backtest, ni budget, ni validation des paramètres). Statistiques
produites sous la dérogation cadrée §0 de l'ordre : **IS uniquement**, chaque tableau
marqué « DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE ». Aucun calcul de
P&L, taux de réussite, espérance ou probabilité de passage. Budgets inchangés
(tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 · P9 10/12) ; enveloppe
Phase 12 proposée, non consommée. **Suspension FRED appliquée** (§9 ci-dessous).

---

## 1. Annexe de conformité V3 ↔ blueprint seq 144 → corrections 12.1

| Exigence V3 | Réponse seq 144 (section) | 12.1 |
|---|---|---|
| §0 Préambule verbatim | Tête du blueprint, reproduit | **Inchangé**, reproduit ci-dessus |
| §1 Cibles challenge (+8/+10, +5, 4 %, 8/10 %, RR 2:1, 3–10/sem) | §F.2 tableau | **Précisé** §6 : configurations séparées maintenues, modèle générique étiqueté |
| §2 Périmètre des connaissances + cimetière | §B, §C, rappel cimetière | **Inchangé** |
| §3 Couche 1 (niveaux S3, langage, sessions, opens) | §D.0, §A.5 | **Précisé/corrigé** §4 : table DST exacte ; opens mesurés en descriptif IS (ci-dessous), règle 15 min maintenue comme paramètre de conception |
| §3 Couche 2 (F3 Q_t, F7, S2, arbitrage coûts) | §D.1 | **Corrigé** §2 (conversion saisonnière, Q_min dérivé), §3 (filtre F7 conditionnel), §5 (3 scénarios alignés V3) |
| §3 Couche 3 (formules, 2R, interdictions) | §D.1 Couche 3 | **Corrigé** §2.3 : condition algébrique exacte du 2R **net** (TP ≥ 2·SL + 3·coût) |
| §3 Couche 4 (sizing, budgets, CUSUM) | §D.1 Couche 4 | **Précisé** §6 (perte flottante, transition P1→P2, contrat générique) |
| §4 Gabarits scénarios + comptage + non-collision | §D.2–D.5 | **Précisé** §7 (36 cellules documentées une à une par famille paramétrique) |
| §4 S12-03 double admission | §D.4 : écarté, double justification | **Inchangé** |
| §5 Exclusion news [−5,+5], liquidation T−5 | §D.0, §F.1 | **Inchangé** |
| §6 Contrat mathématique challenge | §F.2 | **Précisé** §6 |
| §7 Protocole statistique futur | §G, §H | **Précisé** §7 (BY = FDR, articulation des gates, n/MDE par cellule) |
| §8 Livrable A–J | Blueprint §A–§J | **Inchangé** ; la présente validation met à jour §J (§8 ci-dessous) |
| §9 Interdictions | Tête + §I du blueprint | **Inchangé**, appliquées à la présente mission |
| §10 Chaîne + ligne COVERAGE_MATRIX | seq 143–144, matrice 1 ligne | **Inchangé** ; aucune modification de la matrice à ce stade (ordre 12.1 §10) |

Aucune exigence V3 n'est « MANQUANT » dans seq 144 ; les corrections 12.1 portent sur la
dérivation (Q_min), une condition algébrique (2R net), le mode d'action F7, et les
précisions opérationnelles (sessions, coûts, contrat, cellules).

## 2. F3 — conversion temporelle, unités, dérivation de Q_min

### 2.1 Conversion imposée (remplace √(h/24))

DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE. Le profil saisonnier horaire
mesuré sur la série horaire IS certifiée (60 025 h ; `HOURLY_SEASONAL_PROFILE.csv`)
donne la part de variance par heure UTC : creux 03–05 h (1,7–1,8 %/h), montée 12–15 h
(7,7–10,2 %/h, pic 13 h = 10,17 %), retombée 20–21 h (1,0–1,8 %). L'hypothèse iid
sous-jacente à √(h/24) est donc réfutée par nos propres mesures (facteur ~6 entre
l'heure la plus calme et l'heure la plus active).

**Règle de conversion adoptée (paramètre de conception, à geler au préreg)** :
`σ²(t0, h) = RV_prévue_F3(jour) × Σ_{u ∈ [t0, t0+h]} w_u`, où `w_u` = part de variance
de l'heure u dans le profil saisonnier IS (Σ journalière des w = 1 par construction),
la fenêtre étant prise sur le calendrier horaire réel (traversée de minuit incluse).
L'intégrale journalière redonne exactement la prévision F3 : la renormalisation exigée
par l'ordre est satisfaite par construction.

### 2.2 Unités communes

F3 prévoit une variance journalière de rendements ; `σ(t0,h)` est en rendement, converti
en **bp de prix** : `Mouvement_σ_bp = 10 000 × σ(t0,h)`. Convention distributive écrite :
sous hypothèse gaussienne de travail, `E|Δ| = σ × √(2/π) ≈ 0,798 × σ` ; le blueprint
retient `Mouvement_prévu = E|Δ|_bp` (et non σ) comme numérateur de Q — convention
déclarée, la queue réelle des rendements d'or étant plus épaisse, ce choix est
conservateur en fréquence mais non en amplitude extrême (déclaré, §I du blueprint).
Coût S2 en bp : `Coût_total = spread_observé + commissions + slippage_hypothèse`,
mêmes unités. Q_t est donc un ratio de bp/bp, sans dimension.

### 2.3 Dérivation de Q_min (remplace la proposition « 4 » de seq 144)

Deux conditions algébriques, issues de la doctrine et non des résultats :

1. **2R net exact.** Pour un long : gain net à la cible = `TP − C`, perte nette au stop
   = `SL + C` (C = coût aller-retour total en bp, entrée+sortie). Le ratio net ≥ 2
   exige `TP − C ≥ 2(SL + C)`, soit **`Distance_TP ≥ 2 × Distance_SL + 3 × C`**.
   (La formulation seq 144 « cible ≥ 2R net » était imprécise ; la présente condition
   la remplace.) À C = 4,7 bp (C1_BG) et SL = 20 bp : TP ≥ 54,1 bp.
2. **Capacité de mouvement.** Pour que la cible soit atteignable dans l'horizon sans
   invoquer la queue : `E|Δ_h| ≥ Distance_TP`. Donc
   `Q_t = E|Δ_h| / C ≥ Distance_TP / C ≥ (2·SL + 3C)/C = 2·SL/C + 3`.
   Avec la géométrie de référence du blueprint (SL de référence 20 bp, ancre haute
   C = C1_BG = 4,7 bp) : `Q_min ≥ 2×20/4,7 + 3 ≈ 11,5`.

**Q_min = 11 (paramètre de conception dérivé, non optimisé, figé avant tout essai ;
arrondi à l'entier inférieur de la borne dérivée 11,5 — écart déclaré).** La condition
opérationnelle complète au préreg sera la conjonction : `Q_t ≥ 11` **et**
`Distance_TP ≥ 2·Distance_SL + 3·C_scénario` évaluée au scénario de coût central (§5).
Q_min = 4 (seq 144) est retiré : il ne dérivait de rien.

## 3. F7 — définition du filtre de sauts

### 3.1 Faits et limites documentaires

F7 (gelé, seq 75–83) : probabilité de saut sur **l'heure suivante**, AUC 0,684, lift
2,85× au taux d'alerte 5 % (décile supérieur ≈ zone d'alerte validée). Ses features
incluent l'état de volatilité courant : **par construction, les hauts déciles F7
co-occurrent avec les régimes de forte volatilité** — c'est-à-dire précisément les
régimes où Q_t est élevé et où S12-02 (continuation) cherche ses configurations.

DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE. La table de co-occurrence
exacte F3×F7 exigerait la série horaire des probabilités F7, **qui n'est pas versionnée
dans le dépôt** (seuls les résultats agrégés seq 77/83 le sont). Produite à la place,
et étiquetée comme telle : la co-occurrence régime F3 (déciles de la vol prédite
journalière, 2 071 jours) × déciles de volatilité horaire réalisée
(`F3_REGIME_X_HOURLY_VOL.csv`, 47 311 heures jointes) montre la concentration attendue
des régimes hauts. La table F3×F7 exacte est classée **NON PRODUISIBLE depuis les
artefacts versionnés sans ré-exécuter l'inférence du modèle gelé** — ce qui n'a pas été
fait (aucune modification/exécution de code de stratégie ; et ce serait une étape de
préreg, pas de la validation).

### 3.2 Règle de décision écrite (tranchée comme l'ordre l'exige)

Un blocage dur au décile supérieur F7 éliminerait matériellement les configurations
d'expansion visées par S12-02 (recouvrement par construction, §3.1). **Décision
(paramètre de conception)** : le filtre F7 est **conditionnel, non bloquant seul** —
entrée interdite si et seulement si `décile F7 = 10` (zone d'alerte) **ET**
`Q_t < Q_min + marge`, la marge étant fixée à +50 % de Q_min (proposé non calibré) ;
si `Q_t` dépasse ce seuil majoré, l'entrée reste autorisée mais le **risque par
transaction est réduit de moitié** (réduction de risque, seconde branche permise par
l'ordre). Horizon aligné : la prédiction F7 (heure suivante) doit couvrir l'heure
d'entrée ; pour une détention multi-heures, le filtre s'évalue à l'entrée uniquement
(déclaré : F7 ne prédit pas à h > 1 h, aucune extrapolation n'est inventée). F7 ne
reçoit jamais de signe directionnel.

## 4. Sessions — conventions opérationnelles exactes

Conventions retenues (paramètres de conception ; le programme n'en contenait aucune) :

| Session | Heure locale de marché | Équivalent UTC (hiver) | Équivalent UTC (été) | Règle DST |
|---|---|---|---|---|
| Asie (Tokyo) | 09:00–18:00 JST (pas de DST) | 00:00–09:00 | 00:00–09:00 | Aucune |
| Londres | 08:00–16:30 London | 08:00–16:30 | **07:00–15:30** | BST du dernier dimanche de mars au dernier dimanche d'octobre |
| New York (COMEX) | 08:20–13:30 ET | 13:20–18:30 | **12:20–17:30** | EDT du 2ᵉ dimanche de mars au 1ᵉʳ dimanche de novembre |

**Convention opérationnelle gelée pour les scénarios** : par cohérence avec les
timestamps UTC natifs de S3 et pour éviter toute ambiguïté de conversion dans le code
futur, les niveaux et fenêtres sont calculés sur les **blocs UTC de seq 144**
(Asie [00:00, 08:00), Londres [08:00, 13:00), New York [13:00, 21:00) UTC), la table
ci-dessus servant de correspondance documentaire avec les heures locales — les deux
conventions divergent aux marges en été (déclaré ; le préreg devra en élire une,
recommandation : blocs UTC). Journée de référence des extrêmes de la veille : journée
calendaire UTC précédente [00:00, 24:00). Extrêmes : max/min des bougies 1 min S3 de la
session, cotations Mid exclues (niveaux sur Bid pour un plus bas, Ask pour un plus haut
— convention exécutable, à geler). Règle des 15 minutes post-ouverture :
**paramètre de conception, non mesuré** (étiquette maintenue).

DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE. Spread par bloc de session
(série horaire IS) : médiane Asie 2,34 / Londres 2,20 / New York 2,27 / nuit 21–24 h
3,16 bp ; P90 : 3,88 / 3,13 / 3,63 / 5,03 bp (`SPREAD_BY_SESSION.csv`, n = 6 186–20 570 h
par bloc). Autour des ouvertures retenues : le spread médian horaire est plat
(2,19–2,22 bp de 07 h à 11 h UTC) et la part de variance monte de 4,4 % (07 h) à
8,9–10,2 % (12–13 h) — **aucun élargissement de spread d'ouverture n'est mesuré dans
la série horaire** ; la résolution horaire ne voit pas les premières minutes : le
spread des 15 premières minutes d'open reste **NON MESURÉ** (résolution tick
requise), et la règle conservatrice de 15 min demeure donc en vigueur, non calibrée.
Jours fériés/semaines raccourcies/données manquantes : règle proposée — session sans
cotations pendant > 60 min = session inexistante (niveaux reportés à la dernière
session complète) ; semaine < 3 sessions complètes = niveaux de veille hebdomadaire
interdits. Jamais d'imputation de cotations absentes.

## 5. S2 — modèle de coût

### 5.1 Traçabilité (ne pas confondre les fenêtres)

La mesure P11-A1 (seq 142) certifie les **fenêtres d'annonces** (T−5→T+30), pas les
sessions de trading. Pour S12-01/S12-02, la traçabilité IS est la distribution horaire
du corpus (§4) : médianes par session 2,20–2,34 bp, P75 2,57–2,77, P90 3,13–3,88
(hors nuit). Le flux S2 (NR, ~1,35 bp) est un régime différent, plus récent : les deux
ne se mélangent pas ; C1_NR sert d'ancre basse de certification, pas de description IS.

### 5.2 Trois scénarios (alignés arbitrage V3 ; slippage = hypothèses étiquetées)

| Scénario | Spread | Slippage (hypothèse, jamais observation) | Coût total RT indicatif |
|---|---|---|---|
| Favorable | P50 mesuré de la session (≈2,2–2,3 bp) | +0,3 bp/côté (hypothèse basse déclarée) | spread + commission 1,0 + 0,6 ≈ **3,8–3,9 bp** |
| Central | P75 mesuré (≈2,6–2,8 bp) | +0,6 bp/côté (hypothèse centrale déclarée) | ≈ **4,8–5,0 bp** |
| Défavorable | max(C1_BG 4,7 ; P90 mesuré ≈3,9) = **4,7 bp** | +1,5 bp/côté (stress déclaré) | ≈ **8,7 bp** |

Commission : 0,5 bp/côté (config V2). Aucun de ces slippages n'est une mesure ;
ils bornent.

### 5.3 Slippage maximal supportable (algébrique — borne de viabilité, pas une mesure)

De la condition 2R net `TP ≥ 2·SL + 3C` avec `C = spread + commissions + 2·s`
(s = slippage par côté) : **`s_max = (TP − 2·SL − 3×(spread + commissions)) / 6`**.
Si `s_max < 0`, la géométrie est non viable avant même tout slippage. Exemple de
lecture (géométrie de référence SL = 20, TP = 54,1, spread+commissions = 3,3) :
s_max = (54,1 − 40 − 9,9)/6 ≈ **0,7 bp/côté** — toute exécution dégradée au-delà tue le
2R net de cette géométrie ; c'est un critère d'ignorance du trade, pas une prévision.

## 6. Challenge — protection du capital (spécification complète)

- **Risque par transaction** : `r ∈ {0,25 % ; 0,50 %}` de l'equity courante (grille
  proposée, 2 valeurs max) ; `Risque_monétaire = Equity × r` ;
  `Taille = Risque_monétaire / (Distance_SL_bp × valeur_bp_par_lot + coûts_par_lot)`.
- **Contrat générique explicite (hypothèse générique — à remplacer par le règlement
  exact de la firme)** : 1 lot = 100 onces ; 1 bp de prix (0,01 $) par lot = 1 $ ;
  devise USD. Aucune conformité à un fournisseur particulier n'est affirmée.
- **Risque cumulé** : somme des risques ouverts (stops) ≤ budget journalier restant ;
  **positions simultanées ≤ 2** (paramètre proposé) et une seule par scénario.
- **Perte flottante comptée** : le mur journalier interne se calcule sur l'equity
  (flottant inclus), pas sur la balance — déclarée au §F.2 seq 144, confirmée.
- **Stop journalier interne 3 %** (paramètre proposé) vs mur officiel 4 % : à −3 %
  equity du jour, entrées bloquées et positions fermées au marché ; marge = 1 pt pour
  latence/pointes (minute 0 news : > 20 bp mesurés, seq 142).
- **Drawdown** : plafond interne 7 % (trailing equity) vs référence 8 % (sensibilité
  10 %) ; à −7 %, arrêt de la phase en cours.
- **Transition P1 → P2** : equity réinitialisée à la base de phase ; le risque r est
  **inchangé** (toute réduction serait un paramètre nouveau à préenregistrer) ; le
  CUSUM et les budgets journaliers repartent de zéro à l'entrée en P2 ; P1 +8 % et
  +10 % restent deux configurations **séparées**, chacune simulée séquentiellement
  P(P1 puis P2), jamais en produit de marginales.
- **Sorties d'urgence** : stop dur par position toujours actif, liquidation pré-news
  T−5, fermeture journalière à −3 % : aucune n'est désactivable.

## 7. Les 36 cellules — documentation et discipline BY

### 7.1 Inventaire exact (aucune cellule supplémentaire après préreg ; fusions permises et documentées, additions interdites)

**S12-01 (12)** = direction {long, court} × niveau {bas/haut Asie, bas/haut veille
selon direction} — comptées : par direction, niveau ∈ {session, veille} (2) × buffer
stop ∈ {2, 5, 10} bp (3) = 6/direction. Variable principale : PnL net par trade (bp,
Bid/Ask). Métrique : moyenne nette + IC95 %. Critère : gates §7.2.

**S12-02 (24)** = direction {long, court} × niveau {session, veille} (2) × buffer de
cassure ∈ {2, 5} bp (2) × buffer stop ∈ {2, 5, 10} bp (3) = 12/direction.
Mêmes variable/métrique/critère.

Pour chaque cellule : **n effectif requis ≥ 200 trades** (gate du programme) ;
**MDE (gate R3)** = `2,8 × σ_trade / √n` pré-calculée au σ descriptif de la géométrie
avant tout test — si MDE > effet minimal (2R net à l'ancre haute), la cellule est
NON TESTABLE à 0 essai, comme F9/F13/F14/F16. Budget attribué : 1 essai par cellule,
plafond 36, **non consommé**.

### 7.2 Discipline de famille — ce que BY contrôle, exactement

La correction de **Benjamini-Yekutieli** contrôle le **FDR** : la proportion attendue
de fausses découvertes **parmi les cellules rejetées** (déclarées positives), sous
dépendance arbitraire entre tests — propriété qui motive son choix ici (les cellules
partagent niveaux, jours et filtres : dépendance forte et inconnue). Elle ne contrôle
**pas** le FWER (probabilité d'au moins un faux positif dans la famille), qui exigerait
Bonferroni/Holm — plus conservateur et non retenu par la doctrine du programme.
Articulation : BY(36) discipline la famille des 36 tests primaires ; les gates par
cellule (n ≥ 200, R3/MDE en amont à 0 essai, IC95 % net > 0 aux ancres C1_NR **et**
C1_BG, signe 3/3, ECR ≥ 2) sont des conditions **supplémentaires conjonctives** — une
cellule ne « passe » que si elle survit à BY **et** à chaque gate ; les scénarios de
coût ne multiplient pas la famille (évaluations de certification d'une même hypothèse,
convention du blueprint soumise à validation).

## 8. Section J mise à jour (décisions réservées au propriétaire)

1. Acter les corrections 12.1 : Q_min = 11 dérivé (retrait du 4), condition
   `TP ≥ 2·SL + 3C`, filtre F7 conditionnel avec réduction de risque, convention de
   sessions (blocs UTC recommandés) ?
2. Admettre S12-01/S12-02 au préenregistrement (S12-03 reste écarté) et valider le
   plafond 36 cellules/BY(36) avec la convention « coûts = certification » ?
3. Identifier une prop firm + règlement exact + spec MT5 (pour sortir du modèle et du
   contrat génériques) ?
4. **Rotation FRED** : bloquante pour toute réactivation des workflows suspendus (§9).
5. Autoriser ou non l'étape suivante (préreg + extraction descriptive de fréquence) —
   le lancement des expériences exigera dans tous les cas une autorisation distincte,
   après contrôle coach du présent livrable.

## 9. Sécurité FRED — suspension appliquée (ordre §9)

Dès la présente livraison (seq 145) : le workflow **`.github/workflows/exogenous_pack_v2.yml`**
— seul workflow du dépôt appelant FRED (`ci_tools/exogenous_complete.py` via
`${{ secrets.FRED_API_KEY }}`) — est **suspendu** : déclencheur push retiré, job marqué
`if: ${{ false }}` (ne peut tourner même en dispatch manuel), en-tête documentaire
citant seq 145. Aucun autre workflow ne référence FRED (vérifié par recherche sur
`.github/workflows/`). La mission 12.1 n'a pas utilisé FRED (calendrier déjà dans le
programme). Réactivation uniquement après confirmation de rotation par le propriétaire.
Rappel : la clé historiquement exposée (seq 105, confirmée seq 140 dans les commits
`cfd3df5/833f13b/b144080`, purgée à HEAD par `7c0ebec`) reste lisible dans l'historique ;
la purge future réécrira les SHA et exigera le mapping ancien→nouveau des 144+
checkpoints. La clé n'a été ni affichée, ni copiée, ni réutilisée ici.

*Fin de la validation. Comparaison seq 144 → 12.1 : §1 (tableau exigence par
exigence). Aucune expérience n'est lancée par ce document.*
