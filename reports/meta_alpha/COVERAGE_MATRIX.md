# MATRICE DE COUVERTURE v2 — 134 ENTRÉES (seq 1→134) MONTÉES EN PREUVE

**Version 2 — Ordre P0-V2 du propriétaire/coach, 2026-11-18 (complément de l'auditeur
externe). Documentaire strict : 0 essai, 0 budget consommé, 0 réouverture de piste
morte, Phase 11 non démarrée, aucun capital engagé.** Cette v2 remplace la v1
(seq 136). Elle démontre la couverture réelle cellule par cellule ; elle ne défend
aucune conclusion et ne fabrique aucune expérience.

**Budgets figés (rappel obligatoire, tête de document) :** tick **148/150** · panel
**28/60** · exogène **6/60** · Phase 7 **0/24** · NR Phase 8 **0/24** · Phase 9 **10/12**
(By(12)). Phase 10 et P0/P0-V2 : simulation/documentaire hors budget. Holdouts anciens
et HOLDOUT_NR (2025+, lake seul) : jamais ouverts ni téléchargés.

---

## 1. Niveau de preuve — règle de lecture de la v2

Aucune cellule n'est déclarée couverte sans ses cinq pièces, portées **dans** la
cellule ou dans la ligne de preuve qui la suit immédiatement :

1. **seq maîtresse(s)** de la chaîne d'audit ;
2. **hypothèse littéralement testée** (ou, pour les gates, littéralement bloquée) ;
3. **résolution des données** effectivement utilisées (tick, minute, heure, jour, 8 h…) ;
4. **résultat chiffré** tel que chaîné ;
5. **budget consommé** par le test (0 si rejet au gate).

Si une pièce manque dans les sources, la cellule ne peut pas porter la classe R :
elle descend en P, I ou J selon la cause. Aucune affirmation de couverture sans pièce.

## 2. Taxonomie à quatre classes (remplace « non falsifiable » partout)

| Classe | Définition | Exemples du programme |
|---|---|---|
| **R — Réfutée** | Testée et rejetée dans le périmètre précis, cinq pièces présentes | F1–F6, F10, F11, F15, B1, atlas M6 |
| **P — Sous-puissante** | MDE > effet plausible au N disponible ; le temps seul ne le lèvera pas, ou pas à échelle humaine | F13 (n_eff < 200), F14 (MDE 43,2 > 16,7), F16 (MDE 57,6 ≫ 9,4), F9 |
| **I — Inaccessible** | Données payantes/non certifiables gratuitement, ou venue absente | flux ETF, surprise vs consensus, maker, options, tick COMEX |
| **J — Jamais testée** | Aucune entrée des 134 seq ne couvre la cellule | C-2 et les cellules J listées §8 |

Le terme « non falsifiable » disparaît du vocabulaire du programme. Les seuls murs
arithmétiques permanents sont classés **P avec mention « structurel »** (le N requis
excède l'histoire disponible de l'actif, pas seulement la patience de l'observateur).

## 3. Les huit dimensions et les horizons (trame inchangée)

Dimensions : **D1** Direction/signe · **D2** Volatilité & risque prévisible ·
**D3** Microstructure & exécution · **D4** Calendrier & saisonnalité ·
**D5** Événements & annonces · **D6** Exogène & cross-asset ·
**D7** Paiements structurels · **D8** Structure du jeu/challenge.
Horizons : **H1** tick–minutes · **H2** intraday/heures · **H3** journalier ·
**H4** hebdo–mensuel · **H5** ères. Régimes : calme/moyen/nerveux (terciles F3),
news, corpus ancien 2010–2020, régime NR 2020→.

---

## 4. Matrice montée en preuve, par dimension

### D1 — Direction / signe

| Cellule | Classe | Preuve (seq · hypothèse littérale · résolution · résultat chiffré · budget) |
|---|---|---|
| D1×H1 réversion conditionnelle | **R** | seq 69–72 · « retour exécutable contre-choc après choc tick, cellules heure×spread serré » · tick, entrées exécutables H=20/50/200 ticks · cellules négatives/nettes sous les ancres (artefact `F1_SYNTHESIS.json`) · **4 essais** (tick 148/150 cumulé) |
| D1×H1 imbalance ORI | **R** | seq 71–73 · « ORI50 prédit le retour Mid à 20/50 ticks » · tick, déciles par ère · corrélations sans capturabilité nette (`F2_SYNTHESIS.json`) · **12 essais** déclarés |
| D1×H1 post-saut / gap week-end × F7 | **P** | seq 93–97 · F13-A fade du gap, F13-B suivi, F13-C ORI pré-saut en fenêtre F7, F13-D continuation post-saut · tick · **n_eff = 135 / 135 / 38 / 153 < 200 au gate R1, aucune performance lue** · **0 essai** consommé (4 déclarés non exécutés) |
| D1×H2 réversion horaire | **R** | seq 66–68 · « retour horaire i+1 contre le retour de l'heure i » · barres 60 s agrégées heure, 60 024 heures par ère · v2 honnête (bug v1 consigné seq 67) : −2,7 / −2,6 / −2,1 bp par ère ≈ −spread · **4 essais** |
| D1×H2–H5 atlas directionnel ancien corpus | **R** | seq 115–116 · crible M6, cellules fenêtre×régime×horizon (30) sur atlas M1–M5 · horaire · meilleur effet descriptif **2,8 bp vs plancher 9,4 bp**, MDE cellulaires 0,7–5,8 bp → 0/30 survivantes, aucun candidat né · **0/24** |
| D1×H2–H5 atlas régime NR | **R** | seq 118–120 · même crible sur corpus NR · GC=F journalier + S3 horaire 2020 (3 768 h) · daily 0/6 (0,3–6,1 vs 10,8–48,4 bp), intraday 0/30 (meilleur 7,4 vs 22,2) · **0/24** |
| D1×H3 TSMOM or seul | **P** | seq 80–81 · F9 arrêté **avant** test · journalier, 2 572 j / 10,2 ans · **MDE Sharpe 0,93 > 0,5 visé** · **0 essai** |
| D1×H4–H5 momentum panel | **R** | seq 86–91 · F10 XSMOM « le momentum cross-sectionnel 43 actifs paie » et F11 TSMOM panel · journalier panel ≤2014 · F10 : meilleur Sharpe **0,56 < 0,8**, DSR 0,878 < 0,95, PBO 0,557 · F11 : **0,28**, DSR 0,586, PBO 0,821 · **16 + 12 = 28/60** |
| D1×H1–H2 post-annonce | **R** | F15, voir annexe F15 (§6) : 6/6 variantes réfutées, **6/60** exogène |
| D1×H1–H2 pré-annonce | **R** | B1, seq 125–128 : voir D5 ci-dessous |

### D2 — Volatilité & risque prévisible (certifiée en service, jamais en direction)

| Cellule | Classe | Preuve |
|---|---|---|
| D2×H3 prévision de vol lendemain (F3) | **Certifiée (service)** | seq 61–64 (L1) et 82 (L2) · « HAR sur RV/BPV/J bat le naïf en QLIKE » · journalier tick-agrégé · **QLIKE 0,0191 vs 0,0266, R² MZ médian 0,200, 5/5 blocs, walk-forward annuel** · 1 essai déclaré seq 61 |
| D2×H2 anticipation de sauts (F7) | **Certifiée (service)** | seq 75–77 (L1) et 83 (L2) · « probabilité de saut dans l'heure, logistique gelée » · horaire · **AUC OOF 0,684, lift 2,85× à 5 % d'alerte ; forward 2017/18/19 : 0,684/0,696/0,687** · 2 essais déclarés seq 75 |
| D2×H1 anatomie des sauts/queues | **R (descriptif clos)** | seq 30–45 (MARKET_DIMENSIONS, POST_EVENT, VOL_HOURLY, SPREAD_EPISODES, 282/282) · caractérisation post-mouvements extrêmes et couplage RV/spread au tick et à l'heure, **descriptif par ordre, aucun PnL** · 0 essai en propre (missions descriptives chaînées) |
| D2×H4 modèle de vol hebdomadaire dédié | **J** | Aucune seq ne préenregistre un HAR hebdomadaire ; le F3 journalier agrégé n'est pas un test de la cellule. Mécanisme : persistance de vol (même que F3) — mais cellule déjà couverte en esprit par F3 ; classée J sans éligibilité propre (§8) |
| D2×H5 stabilité inter-ères de F3/F7 | **Partielle → J pour le test de rupture** | L2 annuel 3/3 (seq 82–83) couvre 2017–2019 ; aucun test préenregistré de dégradation de calibration F3/F7 sur le régime NR n'existe dans les 134 seq. Risque de maintenance documenté, pas une hypothèse |

### D3 — Microstructure & exécution

| Cellule | Classe | Preuve |
|---|---|---|
| D3×H1 mécanismes de cotation, lead-lag bid/ask | **R** | seq 11–16 (GLOBAL_DISCOVERY, DEEP_AXES préenregistrés seq 12/15) · tick, IS 282 partitions · axes A/B/C caractérisés, aucun mécanisme capturable net du spread · budgets de la génération pré-panel (inclus dans le cumul tick) |
| D3×H1 modèle de spread (F4) | **R** | seq 65 · « AR(2) log-spread horaire bat EWMA de ≥10 % » · horaire, n = 22 928 · **gain RMSE 1,53 % < 10 %** → non qualifié · inclus Phase 2 |
| D3×H2 borne adverse selection du maker | **I (venue)** | seq 122–123 · mesure descriptive 0 essai : heures à spread haut (méd. 4,6 bp) → mouvement absolu heure suivante 8,4 bp vs 7,5 bp ailleurs — adverse selection de l'ordre du spread capté, **tranchable au tick seulement** ; venues du périmètre 100 % taker → la cellule maker elle-même est **I**, pas testée |
| D3×H3–H5 exécution longue / maker patient | **I (venue)** | Aucune venue maker accessible dans le périmètre (CFD retail, challenge prop) ; aucune seq ne peut porter la preuve |
| Ancres de coût (mesures, pas hypothèses) | — | C1_BG = **4,7 bp** (seq 108, `OWNER_CONFIG_V2.json`) ; régime NR : S2 ≈ **1,35 bp**, spread médian S3 ≈ **2,2 bp** (seq 119–120) ; E4 seq 60–62 : long inconditionnel ≈ −spread de clôture par ère (vérité de référence) |

### D4 — Calendrier & saisonnalité

| Cellule | Classe | Preuve |
|---|---|---|
| D4×H2 cellules heure×jour (F5) | **R** | seq 74–76 · « rendement moyen par cellule tod×jour » · horaire · meilleure cellule mer. 12 h **−3,07 bp (n = 206) avec retournement de signe au 3ᵉ tiers (+0,79)** → non qualifiée · **120 cellules déclarées au budget** |
| D4×H1–H5 calendriers descriptifs | **R (descriptif clos)** | seq 30–33 (282/282 : pic 14 h UTC 8,35 % des ticks, spread 2,20 bp ; creux 21 h ; spread max 22 h 3,33 bp), seq 116/120 atlas M1/M5 fenêtre×régime contre C1_BG · descriptif sans statistique de gain, par ordre · 0 essai |
| D4×H4 fin de mois / roll futures | **J** | Aucune seq ne la couvre ; mécanisme spot non articulé (le roll est un flux futures, canal spot indirect non démontré) → J **sans** éligibilité (§8) |

### D5 — Événements & annonces

| Cellule | Classe | Preuve |
|---|---|---|
| D5×H1–H2 **post**-annonce (dérive/retournement après publication) | **R** | F15 seq 109–113, **6/6 réfutées** ; détail complet et replay documentaire en **annexe F15, §6** |
| D5×H1 **pré**-annonce (dérive T−240→T−5 min) | **R** | seq 125–128 (B1, Phase 9) · « long inconditionnel (v1) et continuation du signe T−24 h→T−240 (v2) dans la fenêtre pré-annonce » · tick poolé FOMC+NFP+CPI, **n = 326 événements** (gate seq 126 : pool 375, MDE 5,55 < 6,7/9,4 → TESTABLE) · **v1 −1,2 bp net hist, IC95 [−5,9 ; +3,5] ; v2 −3,0 bp, IC [−7,6 ; +1,6] ; ECR ≪ 2 ; placebos ±7 j du même ordre** · **2/12** Phase 9 ; confirmation NR conditionnelle pré-déclarée **non déclenchée** (seq 128) |
| D5×H3 réaction signée par la **surprise** (vs consensus) | **I (données)** | Aucune seq ne teste un écart à un consensus point-in-time : le consensus historique horodaté n'est pas certifiable gratuitement (pack exogène seq 101–105 : « aucune variable surprise, consensus manquant documenté, aucune imputation », F15_PREREG). Voir aussi la distinction F14/F15 §6.3 |
| D5×H5 pré/post-annonce en régime NR | **Partielle → J conditionnelle** | B1 n'a été exécuté que sur l'ancien corpus ; le volet NR était conditionnel à un succès primaire qui n'a pas eu lieu (seq 125/128). La cellule NR n'est ni testée ni réfutée : elle est **J héritée d'une condition éteinte** — la rouvrir serait re-tester B1, interdit sans nouvel ordre et nouvelle hypothèse |

### D6 — Exogène & cross-asset

| Cellule | Classe | Preuve |
|---|---|---|
| D6×H3 équilibre macro journalier (F14) | **P** | seq 106–107 · « écart d'équilibre or vs drivers (DFII10, dollar, COT, GVZ, volume) se résorbe » · journalier PIT `available_at_utc` · arrêté au gate : **MDE 43,2 bp > effet minimal 16,7 bp ; portes drivers 0/5** (DFII10 signe conforme 4/4 mais pic au lag 0, \|t\| = 2,92 < 3) · **0 essai** (5 déclarés non exécutés) |
| D6×H4 positionnement COT (F16) | **P (structurel)** | seq 110–111 · « z COT hebdo, contrarian/momentum, horizon 2 sem » · hebdomadaire, 524 sem., 262 paris indépendants · **MDE 57,6 bp ≫ 9,4/6,7 bp aux deux ancres** — N requis ≈ (57,6/9,4)² ≈ 37× l'histoire disponible (≈ 19 000 semaines) : le temps ne le lèvera pas · **0 essai** |
| D6×H5 corrélations panel & stabilité | **R (descriptif clos)** | seq 116 M4 : GC corrélé PL 0,59 / SI 0,58 / PA 0,38 ; stabilité des corrélations moitiés 0,84 · descriptif, alimentant le crible — pas une hypothèse de gain |
| D6 flux ETF GLD/IAU | **I (données)** | seq 104, clos définitivement : flux non certifiables gratuitement ; volume daily ≠ flux, substitut interdit « dans toute hypothèse future » |
| D6 inter-marchés par résolution | voir **§5 dédié** | quatre résolutions, statuts distincts, jambes précisées |

### D7 — Paiements structurels

| Cellule | Classe | Preuve |
|---|---|---|
| D7×H3 portage funding perpétuels, niveau (BTC, ETH) | **Certifiée** | seq 127 (préreg : sélection par **profondeur seule** sur 913 symboles, coûts déclarés 40 bp AR amorti 1 an) et seq 129 · « short perp + long spot delta-neutre récolte le funding » · funding 8 h Binance Vision depuis 2020, ~7 488 événements/patte · **BTC net +11,2 %/an, IC95 [10,8 ; 12,5], jours+ 88 %, série nég. max 11 j ; ETH +13,3 %/an, IC [12,7 ; 14,8] ; stabilité 3/3 ères ; BY passée** · **8/12 Phase 9** (avec B1 : 10/12). Érosion chaînée : BTC 17,4/9,9/4,2 %/an par ère ; corr BTC/ETH 0,87 |
| D7×H3 portage ZEC, SOL | **R** | seq 129 · mêmes gates · ZEC ère 2025-26 **−10,5 %/an** (instabilité) ; SOL moyenne −12,5 %/an tirée par outliers (médiane +9,1) · inclus dans les 8 essais |
| D7×H5 portage perpétuels récents (XAU, SOXL, SNDK, SKHYNIX) | **P (structurel, par le temps)** | seq 129 · historique **1 seule ère** (nés 2025-12→2026-06) ; le gate préenregistré exige ≥3 ères : insatisfiable aujourd'hui quelle que soit la volonté — le N requis est du temps calendaire (≈ 4–5 ans par actif), pas un budget |
| D7 prime de variance GVZ−RV | **I (venue)** pour la monétisation ; mesure **R-descriptive** | seq 123 (ancien IS : +5,6 pts de vol, positive 94,9 %, n = 2 490 j ; ères +7,1/+6,0/+3,1) et seq 130 (NR : +2,2/+1,5/+0,4, positive 69–77 %) — la **mesure** est couverte, la **monétisation** exige des options → venue absente du périmètre |
| D7×H2/H3 **dynamique** du funding (timing sur niveau extrême) | **J** | Le portage certifié (seq 129) teste le **niveau moyen** en portage permanent ; aucune seq ne teste une règle d'entrée/sortie conditionnelle au niveau du funding. Mécanisme et éligibilité discutés sans plaidoyer au §8 |

### D8 — Structure du jeu / challenge (simulation, hors budget, aucun test de marché)

| Cellule | Classe | Preuve |
|---|---|---|
| D8×H3 politiques de passage 2-Step | **Simulée (hors classes R/P/I/J)** | seq 132–134 · 4 000 trajectoires/politique, règles V2 exactes, bruit calibré sur vol prédite F3, **μ imposée −2/0/+2 bp (jamais mesurée)** · à μ = −2 bp : F3-asservi P1 = 0,323 / P2 = 0,609 (produit 0,197), fixe 0,185, jeu hardi borné 0,023 (écrasé par limite journalière × trailing), Kelly μ ≤ 0 → taille 0 · **0 essai** |
| D8×H2 filtres fenêtres M1/M5 + embargo F7 | **Simulée** | seq 133 : filtres neutres à légèrement négatifs sur P(passage), effet seulement sur la queue · 0 essai |
| D8 panier contrôlé à stop dur | **Simulée — réfutée en simulation** | seq 133 E2 : distribution déclarée (92 % +0,10 % / 7 % −0,8 % / 1 % −4,5 %) → P(passage P1) = 0, ruine ≈ 100 % (gains < seuil qualifiant +0,5 % ; jour −4,5 % > limite journalière) |
| D8 arithmétique du ticket | **Simulée** | seq 133 E3 : P(passage total) max ≈ 0,197 ≪ 0,75 (règle de cohérence 25 %) ; EV positive seulement sous hypothèses de gain financé qui supposent le μ manquant |

---

## 5. Inter-marchés par résolution (exigence 4)

Remarque de l'auditeur, retenue et appliquée ci-dessous : **l'impossibilité
d'exécuter deux jambes n'interdit pas un signal à une jambe.** Chaque ligne précise
donc si l'hypothèse naturelle exige une jambe (signal → trade sur le spot) ou deux
(exécution relative futures/spot, hors périmètre challenge).

| Résolution | Données en dépôt ? | Statut honnête | Ce que la résolution peut et ne peut pas prouver |
|---|---|---|---|
| **Seconde** (tick COMEX GC vs spot) | **Non** — tick futures synchronisé = flux payant (CME) ; aucune seq ne le contient | **I (données)** | Seule résolution où un lead-lag futures→spot de quelques secondes serait visible. Hypothèse naturelle : **une jambe** (signal futures, exécution spot) — mais sans les données, rien n'est testable ; deux jambes seraient de toute façon hors périmètre |
| **Minute** (GC=F 1-min roulant ~30 j vs spot) | **Partiel** — GC=F 1-min collectable par fenêtres roulantes de 7 j (seq 119 : « 30 j refusé, roulant 7 j actif ») ; pas d'archive minute constituée en dépôt | **J bornée → P si constituée** | 30 jours ≈ 43 000 minutes mais quelques centaines d'épisodes indépendants au mieux : peut prouver un décalage de découverte de prix grossier (≥1–2 min), **ne peut pas** prouver un effet capturable net du spread spot (le MDE minute sur 30 j excède tout lead-lag plausible, et l'échantillon couvre un seul régime). Hypothèse : une jambe |
| **Heure** (GC=F ~730 j vs spot Dukascopy S3) | **Oui en partie** — GC=F horaire 2024+ (Yahoo) et S3 horaire 2020 (3 768 h, seq 119–120) ; les deux fenêtres **ne se recouvrent pas** en dépôt | **J (défaut de recouvrement)** | À cette échelle, futures et spot d'un même sous-jacent sont arbitrés quasi à l'identique : tout écart horaire persistant serait un artefact de base/staleness, pas un paiement. La cellule est testable en principe (une jambe) dès qu'une fenêtre commune GC=F×S3 existe — le backfill S3 2021–2023 non collecté (throttling) et l'horaire Yahoo 2024+ ne se touchent pas encore |
| **Jour** (GC=F daily vs spot daily) | **Oui** — GC=F IS_NR 1 007 j + VALID 252 j (seq 119), spot daily ancien corpus | **R (par le crible)** | Le crible M6 NR (seq 120, 0/6 cellules daily) couvre la relation journalière or/futures comme cellule de l'atlas ; au-delà, futures et spot journaliers sont le même prix à la base près — aucune hypothèse directionnelle distincte n'a été préenregistrée ni n'a survécu |

## 6. Annexe F15 — replay documentaire (exigence 3, aucun test nouveau)

### 6.1 Fenêtres effectivement testées (sources : `F15_PREREG.json`, `F15_RESULTS.json`, seq 109–113)

- **Univers** : FOMC (81 événements IS), NFP/PAYEMS (129–143), CPI (127–151), timestamps = `available_at_utc` du pack exogène PIT (seq 105). **Aucune variable surprise** (consensus absent, documenté au préreg).
- **Entrée** : premier tick **≥ T+5 min** après `available_at_utc`. (La v1 — entrée T+60 s avec premier mouvement mesuré T+60 s→T+5 min, donc signal connaissant sa fenêtre de définition — a été **rejetée avant verdict, seq 112**, résultats non consignés. La v2 corrige : premier mouvement mesuré T→T+5 min, entrée au premier tick ≥ T+5 min.)
- **Sorties mesurées** : 15 / 60 / 240 min rapportées pour toutes les variantes ; **verdict sur H = 60 min uniquement** (gelé a priori au préreg).
- **Variantes (N = 6, toutes exécutées)** : FOMC dérive **−0,4 bp** / FOMC retournement **−7,4** ; NFP dérive **−6,7** / NFP retournement **−0,5** ; CPI dérive **−1,3** / CPI retournement **−5,3** (nets, ancre historique ; ancre BG pire ; rappels 15 min et 240 min également négatifs à quasi-égalité). Tous les IC95 franchissent 0 sauf CPI-retournement, négatif. ECR < 2 partout ; placebos ±30 j silencieux. **Verdict : ÉCHEC 0/6, budget exogène 6/60** (seq 113), confirmé à la clôture du programme exogène (seq 114).
- Gate préalable (seq 109, `F15_F16_GATES.json`) : TESTABLE aux trois familles (MDE 6,0/4,5/4,4 bp < effets minimaux 9,4 BG / 6,7 hist ; σ 60 min = 19,4 bp ; spread médian IS 2,33 bp). La réfutation est donc un résultat, pas un défaut de puissance.

### 6.2 Exclusion de la fenêtre T+1→T+5 min — justification strictement documentaire

Ce qui a **effectivement été mesuré** et qui fonde l'exclusion :

1. **Atlas M2 (seq 116, `ATLAS_DATA.json`)** : amplitude médiane du premier mouvement |T→T+5 min| = **11,4 bp (FOMC), 12,3 bp (NFP), 6,8 bp (CPI)** ; amplitudes médianes |ret| à 15/60/240 min = 14,3/29,3/41,9 bp (FOMC) — la volatilité d'événement ne retombe pas sous son niveau de 15 min dans la fenêtre de 240 min. Spreads médians **à l'entrée** : 2,64/2,51/2,28 bp (FOMC/NFP/CPI).
2. **E4 (seq 60–62)** : vérité de référence du corpus — le long inconditionnel exécutable ≈ −spread de clôture par ère ; l'ajustement de prix d'événement est porté par le spread et le premier saut, pas par une dérive lente.
3. **Prérequis d'entrée** : toute entrée avant `available_at_utc` + latence d'exécution est une fuite par construction (doctrine zéro-fuite du programme) ; la première minute contient l'ajustement discontinu lui-même (saut), déjà caractérisé par POST_EVENT (seq 37–39) et D2×H1.

Ce qui n'a **jamais été mesuré** — écrit noir sur blanc, conformément à l'ordre :

- Le **profil de spread minute par minute de T−5 à T+30** autour des publications n'existe pas comme artefact : M2 donne des spreads d'entrée et des amplitudes médianes, pas la trajectoire T+1→T+5 du spread. **Non mesuré.**
- La **capturabilité exécutable à l'intérieur de T+1→T+5** (prix réellement offerts tick par tick pendant l'élargissement) n'a jamais été extraite comme hypothèse : la fenêtre est exclue par le préreg (entrée ≥ T+5 min) en raison de (1)+(2)+(3), non par un test de la fenêtre elle-même. **La cellule T+1→T+5 est donc J-interdite** : jamais testée, et non ouvrable sans nouvel ordre, nouveau préreg et budget neuf — elle n'est pas « réfutée » et la v2 ne la classe pas R.

### 6.3 Distinction F14 / F15 (noir sur blanc)

**F14** = intégration des **niveaux** macro à l'échelle du **jour** : l'hypothèse était
qu'un écart d'équilibre journalier entre l'or et ses drivers (taux réels, dollar, COT,
GVZ, volume) se résorbe en jours/semaines. Verdict : **P** (seq 107) — portes drivers
0/5 et MDE 43,2 > 16,7 bp ; le seul driver au signe conforme (DFII10) avait son pic
d'information au **lag 0**, c'est-à-dire intégré le jour même.

**F15** = dynamique **d'événement** à l'échelle **minute** : l'hypothèse était qu'après
le saut de publication, le prix dérive ou retourne de façon capturable entre T+5 min et
T+60 min. Verdict : **R** (seq 113) — 6/6 variantes exécutées et réfutées au tick.

Ni confusion ni héritage : F14 n'a jamais rien dit des minutes (sa mesure de lag 0 est
journalière et porte sur des niveaux), F15 n'a jamais rien dit des niveaux
journaliers (ses fenêtres s'arrêtent à 240 min et son signal est le premier
mouvement). Leurs verdicts (P et R) sont de classes différentes et ne se renforcent ni
ne s'annulent. La cellule « surprise vs consensus » (D5×H3, classe I) est une troisième
question, distincte des deux : elle exigerait le chiffre attendu, qu'aucun des deux
programmes n'a jamais possédé.

## 7. Audit B7 — grille F3 × F7 × momentum × régime × coût (exigence 5, documentaire uniquement)

**Aucun calcul nouveau, aucune expérience.** Pour chaque combinaison de la grille
non-linéaire F3 (vol prédite) × F7 (probabilité de saut) × signal de momentum × régime
× ancre de coût, on a cherché une entrée équivalente dans les 134 seq. « Absente »
signifie : aucune seq ne la couvre, même partiellement.

| # | Combinaison | Entrée équivalente | Seq / citation |
|---|---|---|---|
| B7-1 | Momentum seul (sans F3 ni F7) | Testée | F9 (P, seq 80–81), F10/F11 (R, seq 90–91), F15-dérive (R, seq 113), atlas M6 momentum implicite (R, seq 116/120) |
| B7-2 | F3 seul en sizing (pas de signal) | Simulée | Phase 7 axe 2 (seq 116 : −0,1/+1,5/+1,4 pt selon μ imposé) ; Phase 10 E1 politique « f3_asservi » (seq 133) |
| B7-3 | F7 seul en embargo (pas de signal) | Simulée | Phase 10 E1 filtres on/off (seq 133) ; F7 comme « coût évité par exécution reportée » (seq 116) |
| B7-4 | F7 × condition de spread (gate d'exécution) | Bloquée au gate | F13-C (ORI×F7, n_eff 38) et F13-D (post-saut×F7, n_eff 153) — **P**, seq 93–97 |
| B7-5 | ORI × F7 (signe pré-saut conditionné au risque de saut) | Bloquée au gate | F13-C, identique à B7-4 — **P**, seq 96 |
| B7-6 | Momentum × F7 (suivi de saut quand F7 alerte) | Bloquée au gate | F13-D — **P**, seq 97 |
| B7-7 | Momentum × F3 (signal dimensionné par vol prédite) | **Absente comme test** ; présente seulement en simulation | Phase 10 « f3_asservi » applique le sizing à un bruit à μ imposée, pas à un signal de momentum mesuré (seq 133) |
| B7-8 | Momentum × régime (calme/nerveux) | Testée | Crible M6 : 30 cellules fenêtre×régime×horizon, régime nerveux inclus (meilleur effet 2,8 bp, R, seq 116) ; atlas NR 0/30 (seq 120) |
| B7-9 | Momentum × régime news | Testée | F15 dérives FOMC/NFP/CPI (R, seq 113) ; B1 continuation pré-annonce (R, seq 128) |
| B7-10 | Momentum × ancre de coût double | Testée partout | Doctrine deux ancres appliquée (C1_hist/C1_BG) dans F15, B1, M6 — aucune variante n'est positive aux deux ancres |
| B7-11 | F3 × F7 simultanés sur un signal (meta-labelling complet) | **Absente** | F8 méta-labelling déclaré **« sans objet : aucun primaire directionnel candidat »** (seq 78) — la combinaison n'a jamais eu de primaire à filtrer |
| B7-12 | F3 × F7 × régime × coût, grille complète déclarée | **Absente** | Aucune seq ne préenregistre la grille combinatoire complète ; seules ses projections (B7-2, 3, 4, 8) existent. La grille pleine est donc **J** — et son préalable (un primaire B7-11) est R-absent : un filtre ne crée pas le signal qu'il filtre (Phase 7, seq 116–117) |

Conclusion de l'audit B7 : la grille est couverte **par projections** (1, 2, 3, 4, 5, 6,
8, 9, 10 testées/bloquées/simulées) et **absente en produit complet** (7 comme test,
11, 12). Cette absence n'est pas un angle mort prometteur au sens de l'ordre : ses
composantes directionnelles sont R ou P, et F3/F7 sont certifiés comme services dont
la valeur est conditionnelle à un μ qu'aucune composante n'a fourni. Elle est reportée
au §8 en J non éligible, pour traçabilité.

---

## 8. ANGLES MORTS RÉSIDUELS ET HYPOTHÈSES ÉLIGIBLES À UNE FUTURE PHASE 11

*Section finale exigée par l'ordre P0-V2. Elle liste sans plaidoyer. Le verdict
d'exhaustivité ou non appartient au propriétaire après lecture, pas à ce document.*

### 8.1 Ce qui est J (jamais testé) — et son statut d'éligibilité

| Cellule | Mécanisme économique articulé ? | Données dans le périmètre 0 FCFA ? | Éligibilité au sens de la règle P0 |
|---|---|---|---|
| **C-2 — D7×H2/H3 : dynamique du funding** (règles d'exposition conditionnelles au niveau extrême du funding, par distinction avec le portage permanent certifié seq 129) | Oui : le funding extrême rémunère la fourniture de liquidité au camp encombré ; payeur identifié (camp à levier contraint) ; persistance par contraintes de marge | Oui : séries `FUNDING_*.csv` en dépôt (collecte seq 127) | **Seule cellule J remplissant les deux critères.** N'est pas ouverte par ce document ; exigerait ordre explicite + préreg chaîné + micro-budget neuf, gates inchangés |
| Fenêtre événementielle T+1→T+5 min (D5×H1) | Le mécanisme (ajustement incomplet) est contredit indirectement par M2/E4 mais la fenêtre n'a jamais été testée en propre (§6.2) | Oui (tick en dépôt) | J-interdite : non ouvrable sans nouvel ordre ; la v2 ne la classe ni R ni éligible « propre » — l'exclusion repose sur des mesures voisines et un prérequis d'entrée, pas sur un test |
| B7-7 / B7-11 / B7-12 : grilles combinées F3×F7×momentum | Non en propre : un produit de filtres sans primaire ; les primaires sont R/P (B7-1, 4, 5, 6) | Oui | **Non éligible** — mécanisme non articulé indépendamment de ses composantes réfutées |
| D2×H4 vol hebdomadaire ; D2×H5 rupture de calibration NR | Mécanisme = celui de F3 (déjà certifié) ; pas d'hypothèse distincte | Oui | **Non éligible en propre** — maintenance de service, pas hypothèse de Phase 11 |
| D4×H4 fin de mois / roll spot | Canal spot non démontré | Oui | **Non éligible** — mécanisme non articulé jusqu'au spot |
| Inter-marchés minute (30 j) et heure (fenêtre commune à constituer) — signal **une jambe** | Oui (découverte de prix futures) mais borné par l'arbitrage quasi-identique à l'heure et par le MDE à 30 j | Partiel (§5) | **Non éligible en l'état** — la cellule heure est J par défaut de recouvrement, la minute est J-bornée→P ; aucune ne satisfait « données dans le périmètre » aujourd'hui |

### 8.2 Ce qui est I (inaccessible) — avec le prix de l'accès

| Cellule | Mur | Prix de l'accès (état des connaissances du dépôt) |
|---|---|---|
| Maker / microstructure d'exécution (D3) | Venue 100 % taker dans tout le périmètre (CFD retail, challenge) | Accès à une venue maker (compte exchange, KYC, capital) — coût monétaire non consigné dans le dépôt ; décision d'exploitation déjà réservée au propriétaire par seq 131 |
| Prime de variance monétisée (D7) | Pas d'infrastructure options | Compte options + données de chaîne d'options historiques — non chiffrés dans le dépôt, hors 0 FCFA |
| Drift signé par la surprise (D5×H3) | Consensus macro point-in-time horodaté | Abonnement données consensus (type fournisseur d'estimations horodatées) — non chiffré dans le dépôt, hors 0 FCFA |
| Flux ETF GLD/IAU (D6) | Flux non certifiables gratuitement (seq 104, clos définitivement) | Source de flux certifiée payante — substitut par le volume interdit |
| Tick COMEX seconde (inter-marchés) | Flux tick futures synchronisé | Licence données CME — non chiffrée dans le dépôt, hors 0 FCFA |

*Aucun prix n'est inventé : quand le dépôt ne contient pas de devis, la case dit
« non chiffré dans le dépôt ». Ordre de grandeur commun aux cinq lignes : toutes
exigent de sortir du budget 0 FCFA, ce qui est une décision propriétaire, pas une
conclusion du document.*

### 8.3 Ce qui est P (sous-puissant) — avec le N qu'il faudrait

| Cellule | État actuel (pièces) | N requis (arithmétique sur les chiffres chaînés) | Le temps le lèvera-t-il ? |
|---|---|---|---|
| F13-A/B gap week-end (D1×H1) | n_eff 135 < 200 (seq 94–95) | ≥ 200 événements de gap qualifiés effectifs (+48 %) | Lentement : les gaps qualifiés s'accumulent au rythme des week-ends à fort écart — années supplémentaires d'IS nouveau corpus |
| F13-C ORI×F7 (D1×H1) | n_eff 38 < 200 (seq 96) | ≥ 200, soit ~5× les alertes F7 qualifiées | Très lentement (fenêtre 2017+ seulement par construction du modèle gelé) |
| F13-D post-saut×F7 (D1×H1) | n_eff 153 < 200 (seq 97) | ≥ 200 (+31 %) | Lentement, même contrainte |
| F9 TSMOM or (D1×H3) | MDE Sharpe 0,93 > 0,5 visé, 10,2 ans (seq 80) | MDE ∝ 1/√temps → (0,93/0,5)² ≈ 3,5× la durée, ≈ **35 ans** d'historique comparable | Non à échelle de programme |
| F14 équilibre exo (D6×H3) | MDE 43,2 > 16,7 bp (seq 107) | (43,2/16,7)² ≈ 6,7× les observations journalières (≈ 60+ ans au rythme actuel) — ou un effet plausible plus grand, qu'aucune mesure ne suggère | Non à échelle humaine utile |
| F16 COT (D6×H4) | MDE 57,6 ≫ 9,4 bp ; 262 paris indépendants (seq 111) | (57,6/9,4)² ≈ 37×, ≈ **19 000 semaines** | Non — **P structurel** |
| Carry perpétuels récents (D7×H5) | 1 ère disponible, gate ≥ 3 ères (seq 129) | ≈ 4–5 ans calendaires par actif | **Oui, par le seul temps** — sans budget ni test : la donnée mûrit seule, la question se reposera avec un ordre |
| Inter-marchés minute 30 j | Quelques centaines d'épisodes indépendants au mieux (§5) | Un MDE ≤ effet plausible exigerait des années d'archive minute GC=F constituée | Seulement par accumulation d'archive (ingénierie lente, pas d'essai) |

### 8.4 Ce que ce document ne fait pas

Il ne déclare pas la couverture exhaustive — ce verdict appartient au propriétaire.
Il ne recommande l'ouverture d'aucune cellule, y compris C-2. Il ne préenregistre
rien. Il constate, avec pièces : les cellules R sont réfutées dans leur périmètre
exact ; les cellules P ont un prix en N écrit ci-dessus ; les cellules I ont un mur
nommé ; les cellules J sont au nombre de six familles, dont une seule satisfait les
deux critères de la règle de suite. Tout le reste de l'espace {8 dimensions ×
5 horizons × régimes} est couvert par au moins une des preuves du §4.

---

## Annexes techniques (7 pièces, mises à jour v2)

**A1 — Registre seq → cellules.** seq 1–5 générations P3/P4 (D1) · 6–25 découvertes
descriptives (D1/D3/D4) · 26–49 volatilité/microstructure 282/282 (D2/D3) ·
50–52 config (D8) · 53–68 fondations E1–E5, F3/F4/F6 (D1/D2/D3) · 69–79 F1/F2/F5/F7,
clôture IS 144/150 · 80–85 F9 (P), F3/F7 L2, châssis · 86–92 panel F10/F11 (R, 28/60) ·
93–98 F13 (P, 0 consommé), clôture directionnelle 148/150 · 99–100 voie B ·
101–105 pack exogène PIT, ETF clos (I) · 106–107 F14 (P) · 108 config V2, C1_BG ·
109–114 F15 (R, 6/60), F16 (P), clôture exogène · 115–117 atlas M6 0/30 (R, 0/24) ·
118–121 NR 0/6+0/30 (R, 0/24), HOLDOUT scellé · 122–123 audit, B2/B3 descriptifs ·
124–131 Phase 9 : B1 (R, 2/12), carry (certifié, 8 essais), clôture 10/12 ·
132–134 Phase 10 simulation (D8) · 135–136 matrice v1 · 137+ présente v2.

**A2 — Budgets et gates.** Voir tête de document. Gates constants : préreg chaîné
avant calcul · n ≥ 200 · R3/MDE avant toute performance · BY (jamais BH) sur le
budget de phase · IC95 % net > 0 aux deux ancres · signe 3/3 · ECR ≥ 2 · rejet au
gate = 0 essai (F9, F13, F14, F16).

**A3 — Données et holdouts.** Tick ancien 282/282 (Kaggle vérifié) ; panel 43 actifs
≤2014 ; exogène PIT (`available_at_utc`, DST date par date, seq 105) ; NR GC=F daily
1 007+252 j, S3 horaire 2020 (3 768 h), S2 spread en cron ; funding 913 symboles
(sélection profondeur). Backfill S3 2021–2023 non collecté (throttling). Holdouts :
jamais ouverts. google_drive désactivé pour la conversation (à réactiver par
l'utilisateur avant usage).

**A4 — Ancres de coût.** C1_BG 4,7 bp (seq 108) ; NR mesuré 1,35–2,2 bp (seq 119–120) ;
E4 : long inconditionnel ≈ −spread/ère (seq 62) ; carry : 40 bp AR/1 an (seq 127).
Inconnues courtier jamais estimées : slippage, contrat, min/pas, tick size/value,
digits (seq 55) — sizing définitif conditionnel.

**A5 — Actifs certifiés.** F3 HAR-RV L2 (service vol) ; F7 sauts L2 (service) ;
carry BTC +11,2 %/an et ETH +13,3 %/an nets (seq 129, compression par ère chaînée,
corr 0,87, poids méta-portefeuille 57/43) ; châssis + `meta_portfolio.py` prêts.
Aucune exploitation engagée — décision propriétaire séparée (seq 131).

**A6 — Incidents consignés.** Alignement signal/fenêtre sanctionné deux fois
(F6 v1 seq 67 ; F15 v1 seq 112) ; sélection carry corrigée deux fois avant mesure
(seq 127–129) ; `challenge_sim.simuler()` P=0 mécanique (seq 116) ; format S3
(t = secondes depuis minuit UTC, prix ×1000) ; fuite clé FRED run2 purgée —
**révocation propriétaire toujours pendante** (seq 105) ; logs CI inaccessibles
depuis le sandbox (les workflows committent leurs résultats).

**A7 — Règle de suite.** Une Phase 11 ne peut naître que d'une cellule J à mécanisme
articulé + données en périmètre (§8.1 : une seule), par ordre explicite créant un
micro-budget neuf (aucun ancien budget rechargeable), préreg chaîné avant calcul,
gates inchangés. Les cellules I exigent d'abord l'achat de l'accès ; les cellules P,
le N du §8.3 ; les cellules R ne se rouvrent pas. Ce document n'autorise rien.

*Fin de la v2. Chaîne : seq 137 (MISSION P0-V2) → livraison ci-dessus. Budgets
inchangés. Holdouts intacts. Phase 11 non démarrée.*
