# MATRICE DE COUVERTURE — 134 ENTRÉES (seq 1→134) × 8 DIMENSIONS × HORIZONS × RÉGIMES

**Ordre P0 du propriétaire, 2026-11-18 — 0 FCFA, 0 essai consommé.** Document de fouille
déductive (chaîné seq 135–136, marqué hors budget de recherche). Il ne teste rien, ne
rouvre rien, ne certifie rien. Il cartographie ce que la base de connaissances a
effectivement couvert, ce qu'elle n'a couvert qu'en partie, ce qu'elle n'a jamais
touché, et ce qu'elle ne peut pas falsifier dans le périmètre actuel.

**Règle de la suite (ordre P0, inchangée) :** seule une cellule **« jamais testé »**
dotée d'un **mécanisme économique articulé** peut devenir une hypothèse de Phase 11 —
préenregistrée, micro-budget créé par ordre explicite du propriétaire, gates inchangés
(préreg seq avant calcul → n ≥ 200 → R3/MDE → test → BY globale → IC95 % net > 0 aux
deux ancres → signe 3/3 → ECR ≥ 2 ; rejet au gate = 0 essai). Rien d'autre ne rouvre
quoi que ce soit.

---

## 0. Conventions

### 0.1 Les huit dimensions (trame reprise de l'ordre)

| # | Dimension | Question qu'elle pose |
|---|---|---|
| D1 | **Direction / signe** | Le signe du prochain mouvement est-il prévisible au-delà des coûts ? |
| D2 | **Volatilité & risque prévisible** | L'amplitude (pas le signe) de demain est-elle prévisible et monétisable en service ? |
| D3 | **Microstructure & exécution** | Le carnet/la cotation (spread, bid-ask, lead-lag, maker/taker) contient-il un paiement capturable ? |
| D4 | **Calendrier & saisonnalité** | L'heure, le jour, la session portent-ils un effet exploitable ? |
| D5 | **Événements & annonces** | Autour des publications (avant/après), un flux prévisible existe-t-il ? |
| D6 | **Exogène & cross-asset** | Taux, dollar, COT, panel multi-actifs, équilibres externes prédisent-ils l'or ? |
| D7 | **Paiements structurels** | Un flux payé par la structure (funding, prime de variance, basis) existe-t-il sans prédire le prix ? |
| D8 | **Structure du jeu / challenge** | Les règles (barrières, limites, jours qualifiants) créent-elles une valeur par le contrôle, sans edge ? |

### 0.2 Horizons

**H1** tick→minutes · **H2** intraday (heures) · **H3** journalier · **H4** hebdo→mensuel ·
**H5** long / ères (multi-années, stabilité inter-ères).

### 0.3 Régimes

**R-calme / R-moyen / R-nerveux** (terciles de vol prédite F3), **R-news** (fenêtres de
publication et sauts), **R-ancien** (corpus IS tick 2010–2020), **R-NR** (régime nouveau
2020→, corpus Phase 8). La couverture « régime » d'une cellule est précisée dans le
détail (§3) : un test mené sur le seul R-ancien ne couvre pas le R-NR, et réciproquement.

### 0.4 Statuts

- **TESTÉ** — hypothèse préenregistrée, gate passé ou verdict rendu, budget consommé ou gate à 0 essai. La cellule est fermée au verdict indiqué.
- **PARTIELLEMENT TESTÉ** — une partie de la cellule est couverte (un régime, un horizon voisin, une mesure descriptive sans test, un gate sans exécution). Ce qui manque est nommé.
- **JAMAIS TESTÉ** — aucune entrée de la chaîne ne touche la cellule. Éligible Phase 11 **uniquement** si un mécanisme économique est articulé (§5).
- **NON FALSIFIABLE** — la cellule ne peut pas être tranchée dans le périmètre actuel. Cause nommée à chaque fois : **(P)** puissance statistique insuffisante (n ou MDE), **(D)** données payantes ou non certifiables gratuitement, **(V)** accès venue/exécution absent (maker, options, futures synchronisés).

---

## 1. Matrice synthétique (dimension × horizon)

Lecture : statut dominant de la cellule ; le détail et les seq sont au §3. Quand une
cellule mélange plusieurs statuts selon le régime, le statut le plus faible est affiché
et le §3 tranche régime par régime.

| Dim | H1 tick–min | H2 intraday | H3 journalier | H4 hebdo–mensuel | H5 ères |
|---|---|---|---|---|---|
| **D1 Direction** | TESTÉ — échec (seq 67–73, 94–97, 113) | TESTÉ — échec (seq 66–68, 116, 120) | TESTÉ — échec / non testable (seq 80–81, 90–91, 107) | TESTÉ — échec (seq 90–91) ; NON TESTABLE COT (seq 111) | TESTÉ — échec (atlas 0/30 + 0/30, seq 116/120) |
| **D2 Volatilité** | PARTIEL (sauts F7 seq 75–77 ; tick descriptif seq 30–45) | TESTÉ — **F7 certifié service** (seq 77, 83) | TESTÉ — **F3 certifié service** (seq 61–64, 82) | PARTIEL (HAR journalier seul ; pas de modèle hebdo dédié) | PARTIEL (stabilité 3/3 L2 seq 82–83 ; érosion vol documentée, pas de test de rupture préenregistré) |
| **D3 Microstructure** | TESTÉ — échec directionnel (seq 11–16, 70–73) ; maker NON FALSIFIABLE (V) (seq 123) | PARTIEL (borne adverse-selection horaire seq 123 ; tick seul tranche) | PARTIEL (spread F4 faible seq 65 ; pas de test d'exécution journalier) | JAMAIS (pas de mécanisme articulé → non éligible) | PARTIEL (spread par ère seq 54/59 ; régime NR ÷~2,5 seq 119–120) |
| **D4 Calendrier** | PARTIEL (calendrier tick descriptif seq 30–33 ; jamais testé en hypothèse tick) | TESTÉ — échec (seq 74–76 ; atlas M1 seq 116/120) | PARTIEL (jour de semaine dans F5 seq 74–76 ; jamais en hypothèse dédiée journalière) | JAMAIS (effet fin de mois / roulement : mécanisme faible, voir §5) | PARTIEL (calendriers par ère descriptifs seq 17–19, 32) |
| **D5 Événements** | TESTÉ — échec post-annonce (seq 109–113) ; pré-annonce TESTÉ — échec (seq 125–128) | TESTÉ — échec (seq 113, 128) | PARTIEL (F14 lag 0 : intégré le jour même, seq 106–107 ; surprise signée jamais testée, §5) | JAMAIS (pas d'événement hebdo récurrent identifié) | PARTIEL (F15/B1 sur R-ancien seulement ; confirmation NR de B1 non déclenchée seq 128) |
| **D6 Exogène** | JAMAIS (pas de flux exogène tick gratuit synchronisé — tend vers NON FALSIFIABLE (D)) | PARTIEL (co-variation descriptive M3 seq 116 ; aucun test intraday exogène) | TESTÉ — non testable au gate (seq 106–107) | TESTÉ — non testable COT (seq 110–111) ; flux ETF NON FALSIFIABLE (D) (seq 104) | TESTÉ — échec panel (seq 86–92) |
| **D7 Paiements structurels** | JAMAIS (funding échantillonné 8 h ; pas de cellule tick) | JAMAIS (idem ; funding intraday = dynamique, §5 cellule C-2) | TESTÉ — **BTC/ETH certifiés** (seq 127–129) ; ZEC/SOL enterrés | PARTIEL (carry = flux continu ; pas de variante hebdo distincte à tester) | PARTIEL (≥3 ères exigées : perpétuels récents 1 ère — non certifiables, seq 129) ; prime de variance descriptive érodée (seq 123/130), monétisation NON FALSIFIABLE (V) |
| **D8 Challenge** | n/a (pas de cellule marché) | PARTIEL (filtres fenêtres M1/M5+F7 simulés seq 133) | TESTÉ en simulation (seq 132–134, hors budget) | PARTIEL (horizon 1 000 j simulé ; pas de politique multi-phase optimisée au-delà de P1×P2) | PARTIEL (simulation μ imposée ; jamais de validation sur trajectoire réelle — par construction, pas un test de marché) |

---

## 2. Couverture par régime (lecture transversale)

| Régime | Couverture | Seq maîtresses | Angle mort résiduel |
|---|---|---|---|
| R-calme / R-moyen | Dense : atlas fenêtre×régime, F5, M5/M6, coûts par régime | 74–76, 116, 120 | Aucun effet directionnel n'y dépasse le plancher (2,8 bp max vs 9,4 requis, seq 116) |
| R-nerveux | Dense : F7 (sauts), atlas régime nerveux = meilleur effet descriptif, toujours sous le plancher | 75–77, 83, 116 | Queue de saut monétisable seulement en maker/options → (V) |
| R-news | Post-annonce testé (F15), pré-annonce testé (B1), embargo simulé | 109–113, 125–128, 133 | Réaction signée par la **surprise** (vs consensus) : données consensus PIT payantes → (D), voir §5 C-3 |
| R-ancien (2010–2020) | Corpus principal : 282 partitions tick, panel ≤2014, exogène IS ≤2020-01-20 | 1–114 | Holdouts anciens scellés, jamais ouverts — couverture volontairement asymétrique |
| R-NR (2020→) | GC=F daily + S3 horaire 2020 partiel, spread S2 en cron, B2-extension, carry 2020→ | 118–121, 129–130 | Backfill S3 2021–2023 horaire **non collecté** (throttling) : l'intraday NR hors 2020 reste descriptif mince — cellule partielle, pas un angle mort d'hypothèse |
| Crise (2008, COVID, 2022) | Hors corpus (IS démarre 2010 ; NR démarre 2020, COVID inclus en daily seulement) | 119 | NON FALSIFIABLE en l'état (D) : aucune source tick crise qualifiée à 0 FCFA |

---

## 3. Détail par dimension — seq, verdict, budget

### D1 — Direction / signe
- **H1** : F1 réversion conditionnelle (seq 69–72, 4 essais), F2 ORI (seq 71–73, 12 essais), F6 v1 rejetée pour bug d'alignement puis v2 honnête négative (seq 66–68, 4 essais), F13-A/B/C/D **non testables** au gate R1 n_eff < 200 (seq 93–97, 0 essai consommé sur 4). Verdict : échec gelé, coût ≈ −spread structurel (E4 seq 60–62 : long inconditionnel ≈ −spread de clôture par ère).
- **H2** : F6 réversion horaire (seq 66–68), crible M6 Phase 7 **0/30** (meilleur 2,8 bp vs 9,4 ; MDE 0,7–5,8 bp — ce n'est pas la puissance, c'est le plancher de coût, seq 116), atlas NR intraday **0/30** (7,4 vs 22,2, seq 120).
- **H3** : F9 TSMOM **non testable** MDE Sharpe 0,93 > 0,5 visé (seq 80–81, 0 essai) ; F14 équilibre exogène non testable (seq 107).
- **H4–H5** : F10 XSMOM panel échec (Sharpe 0,56 < 0,8, DSR 0,878, PBO 0,557 ; seq 88–90, 16 essais), F11 TSMOM panel échec (0,28 ; seq 89–91, 12 essais). Budgets figés : tick 148/150, panel 28/60.
- **Régimes** : testé en R-calme/nerveux (M6), R-news (D5), R-ancien et R-NR. Aucune poche de régime n'a survécu au plancher ECR ≥ 2.

### D2 — Volatilité & risque prévisible (seule dimension directionnellement « positive », en service)
- **F3 HAR-RV certifié L1+L2** (seq 61–64, 82 : QLIKE 0,0191 vs 0,0266 naïf, R² MZ médian 0,200, 5/5 blocs, walk-forward 3/3). **F7 anticipation de sauts certifié L1+L2** (seq 75–77, 83 : AUC OOF 0,684, forward annuel 0,684/0,696/0,687).
- Usage certifié : **service uniquement** (sizing, filtre, embargo) — Phase 7 seq 116 : le sizing F3 déplace P(passage) de −0,1/+1,5 pt selon μ imposé ; Phase 10 seq 133 : meilleure politique simulée à μ = −2 bp (P1×P2 ≈ 0,197).
- **Partiel** : pas de modèle de vol hebdomadaire dédié (H4) ; pas de test préenregistré de rupture de qualité F3/F7 par ère (H5) — la dérive de calibration en R-NR est un risque de service documenté, pas une hypothèse testée.

### D3 — Microstructure & exécution
- Testé directionnellement au tick : lead-lag bid/ask et mécanismes de cotation (seq 11–16, GLOBAL/DEEP_AXES), réversion vs spread (F1/F2). Échec : le spread est le coût, pas la poche.
- F4 modèle de spread : gain 1,5 % < seuil 10 % (seq 65) — non qualifié.
- **Maker : NON FALSIFIABLE (V).** Borne descriptive seq 123 : adverse selection horaire ≈ spread capté ; tranchable au tick seulement, et les venues du périmètre (CFD retail, challenge) sont 100 % taker. Aucune cellule maker ne peut naître à 0 FCFA sans accès venue — ce n'est pas un « jamais testé » éligible, c'est un mur d'accès.
- Mesures d'exécution : C1_BG = 4,7 bp (ancre challenge, seq 108), S2 NR ≈ 1,35 bp, spread médian intraday S3 ≈ 2,2 bp (seq 119–120) — le régime NR divise le spread par ~2,5 sans changer la structure des verdicts D1.

### D4 — Calendrier & saisonnalité
- F5 : 120 cellules déclarées au budget, meilleure cellule (mer. 12 h) −3,07 bp avec retournement de signe au 3ᵉ tiers (seq 74–76) — non qualifiée.
- Atlas M1/M5 (seq 116, 120) : calendriers réels et marqués (pic d'activité 14 h UTC, spread max 22 h, coût minimal ~14–16 h) — descriptif certifié, contenu directionnel 3–30× sous le plancher.
- **Jamais testé** : effet de fin de mois / roulement de contrats sur l'or spot. Mécanisme articulable mais faible (flux de roll futures, pas de canal spot direct démontré) ; voir §5 — classé non éligible en l'état faute de canal causal spot.

### D5 — Événements & annonces
- **Post-annonce** : F15 v2 (alignement corrigé seq 112) **échec 0/6** (seq 109–113, budget exogène 6/60) : après la première minute, ni continuation ni retournement capturables, nets aux deux ancres.
- **Pré-annonce** : B1 **échec 0/2** (seq 125–128, Phase 9 2/12) : n = 326 poolés FOMC+NFP+CPI, T−240→T−5 min, −1,2/−3,0 bp, placebos ±7 j du même ordre. La confirmation NR conditionnelle n'a pas été déclenchée (pré-déclaré) — la cellule NR de B1 est donc **partielle par construction**, non par oubli.
- **Jamais testé** : drift **signé par la surprise** (écart publication vs consensus). Mécanisme réel (la littérature le documente sur d'autres actifs) mais le consensus point-in-time est payant → bascule en **NON FALSIFIABLE (D)** dans le périmètre 0 FCFA (voir §5 C-3). Le F14 seq 107 a d'ailleurs mesuré l'intégration au lag 0 : le marché incorpore le jour même.

### D6 — Exogène & cross-asset
- Pack exogène certifié ingénierie (seq 101–105, 0 essai) : ALFRED PIT avec `available_at_utc` DST date par date, DFII10/GVZ FRED, COT 880 semaines, FOMC 198 réunions. FRED_API_KEY : révocation toujours pendante côté propriétaire (rappel annexe F).
- F14 **non testable** (MDE 43,2 > 16,7 bp ; portes 0/5, seq 106–107, 0 essai). F16 COT **non testable** (MDE 57,6 ≫ 9,4, seq 110–111, 0 essai). Panel F10/F11 échec (D1/H4–H5). Budget exogène figé 6/60.
- **NON FALSIFIABLE (D)** : flux ETF GLD/IAU — clos définitivement seq 104 (volume ≠ flux, substitut interdit). Lead-lag intraday futures↔spot synchronisé au tick : aucune source gratuite certifiable → (D).

### D7 — Paiements structurels (seule dimension certifiée en argent, pas en prédiction)
- **Carry funding perpétuels : BTC +11,2 %/an net et ETH +13,3 %/an net CERTIFIÉS** (seq 127–129 ; IC95 nets > 0, jours+ 88 %, stabilité 3/3, sélection par profondeur sur 913 symboles, jamais par le funding). Érosion chaînée : BTC 17,4/9,9/4,2 par ère. Corrélation BTC/ETH 0,87 ; poids méta-portefeuille 57/43.
- Enterrés : ZEC (ère 2025-26 à −10,5), SOL (moyenne négative tirée par outliers, médiane +9,1). **Non certifiables (pas faux)** : SOXL/XAU/SNDK/SKHYNIX — 1 seule ère d'historique, le gate ≥3 ères est structurellement insatisfiable aujourd'hui → cellule H5 **partielle**, révisable par le seul passage du temps + ordre.
- **Prime de variance (GVZ−RV)** : mesurée descriptive deux corpus (seq 123 : +5,6 pts, 94,9 % positif R-ancien ; seq 130 : +2,2/+1,5/+0,4 R-NR, érosion continue sans inversion). Monétisation = options → **NON FALSIFIABLE (V)** dans le périmètre. Actif dormant.
- **Jamais testé** : la **dynamique** du funding (timing d'entrée/sortie sur niveau extrême du funding, par opposition au portage permanent certifié). Voir §5 C-2 — seule cellule « jamais testé » avec mécanisme articulé **et** données déjà en dépôt.

### D8 — Structure du jeu / challenge (simulation, hors budget)
- Phase 10 (seq 132–134) : E1 politiques {fixe, Kelly-fraction, F3-asservi, jeu hardi borné} × filtres, règles 2-Step exactes — meilleure P1×P2 ≈ 0,197 à μ = −2 bp ; jeu hardi écrasé par limite journalière × trailing ; Kelly à μ ≤ 0 refuse de jouer. E2 panier contrôlé : P(passage) = 0 (gains < seuil qualifiant +0,5 %, jour catastrophe −4,5 % > limite). E3 : P(passage) max ≈ 20 % ≪ 75 % (règle de cohérence) → ticket = loterie à prix connu à μ ≤ 0.
- **Partiel par nature** : μ est imposée, jamais mesurée — D8 ne peut produire ni edge ni certification, seulement la carte de valeur du contrôle. Le plafond est théorique autant qu'empirique : à espérance nulle, P(+a avant −b) = b/(a+b) ne dépend pas du calibrage.

---

## 4. Registre des budgets (état figé, seq 134)

| Budget | Consommé | État |
|---|---|---|
| Tick (Phases 1–5) | 148/150 | Figé, solde jamais dépensé |
| Panel (Phase 4) | 28/60 | Figé |
| Exogène (Phase 6) | 6/60 | Figé |
| Phase 7 (N=24) | 0/24 | Jamais nés (crible M6 0/30) |
| NR Phase 8 (N=24) | 0/24 | Jamais nés (atlas 0/6 + 0/30) |
| Phase 9 (N=12, BY(12)) | 10/12 | 2 non dépensés (confirmation NR B1 non déclenchée + marge) |
| Phase 10 | 0 (simulation) | Hors budget par ordre |
| P0 (présent document) | 0 | Hors budget par ordre |

Holdouts : anciens (OOS/HOLDOUT ≤ seq 117) et HOLDOUT_NR (2025+, lake seul) — **jamais
ouverts, jamais téléchargés localement**. Toute ouverture exige un ordre explicite.

---

## 5. Cellules « jamais testé » — tri d'éligibilité Phase 11

Critère de l'ordre : mécanisme économique **articulé** (un payeur identifié, une raison
pour laquelle le paiement persiste, un canal jusqu'à XAU/USD ou l'actif visé).

| # | Cellule | Mécanisme articulé ? | Données dans le périmètre 0 FCFA ? | Verdict d'éligibilité |
|---|---|---|---|---|
| C-1 | D4×H4 : fin de mois / roll sur spot | Faible : le roll est un flux futures ; canal spot indirect, jamais démontré | Oui (GC=F déjà collecté) | **Non éligible en l'état** — mécanisme non articulé jusqu'au spot |
| C-2 | D7×H2/H3 : **dynamique du funding** (timing sur funding extrême vs portage permanent) | **Oui** : le funding extrême rémunère la fourniture de liquidité au camp encombré ; la persistance vient des contraintes de levier du camp payeur. Payeur identifié : les longs/shorts à levier | **Oui** : séries FUNDING_*.csv déjà en dépôt (seq 127), aucun compte requis pour le test | **ÉLIGIBLE** — seule cellule remplissant les deux critères. Ne devient hypothèse que par ordre explicite Phase 11 + préreg + micro-budget. Le portage permanent certifié (seq 129) n'est pas rouvert : la cellule vise la dynamique, pas le niveau |
| C-3 | D5×H3 : drift signé par la surprise macro | Oui (littérature), mais F14 seq 107 mesure une intégration au lag 0 qui affaiblit le canal résiduel | **Non** : consensus PIT payant | **Non éligible** — bascule NON FALSIFIABLE (D) à 0 FCFA |
| C-4 | D7×H5 : carry des perpétuels récents (XAU/SOXL/SNDK/SKHYNIX) quand ils auront ≥3 ères | Oui (même payeur que C-2, niveau) | Pas encore : le temps seul manque | **Non éligible aujourd'hui** — cellule partielle (seq 129), révisable par le temps + ordre, pas par un test |
| C-5 | D3×H4+ : toute cellule maker longue | Oui (fourniture de liquidité) | Non : venue 100 % taker | **Non éligible** — NON FALSIFIABLE (V) |
| C-6 | D6×H1/H2 : lead-lag futures→spot intraday | Oui (découverte de prix COMEX) | Non : tick futures synchronisé gratuit non certifiable | **Non éligible** — NON FALSIFIABLE (D) |

**Conclusion du tri : sur l'ensemble de la matrice, exactement une cellule « jamais
testé » satisfait les deux critères de l'ordre (C-2).** Toutes les autres cellules
jamais testées échouent soit le mécanisme (C-1), soit les données (C-3, C-6), soit
l'accès venue (C-5), soit le temps (C-4). Ce document ne préenregistre rien et ne
recommande pas d'ouvrir C-2 : il constate qu'elle est la seule porte que la règle de
l'ordre laisse physiquement ouverte, et qu'elle ne s'ouvre que par ordre explicite.

---

## 6. Ce que la matrice établit (et ce qu'elle ne peut pas établir)

1. **La couverture directionnelle (D1) est saturée** : 5 horizons × 5 régimes, 4 corpus, ~190 essais figés — aucun effet n'a franchi le plancher de coût ECR ≥ 2. Ce n'est ni un problème de puissance (MDE cellulaires 0,7–5,8 bp) ni de régime inexploré.
2. **La couverture « service » (D2) est la seule positive** et elle est complète aux horizons journalier/horaire (F3/F7 L2) ; ses poches partielles (hebdo, stabilité inter-ères de calibration) sont des risques de maintenance, pas des hypothèses.
3. **La couverture structurelle (D7) a produit les seules certifications « argent »** du programme, sur des paiements en compression documentée (carry BTC/ETH). Son extension temporelle (C-4) dépend du calendrier, pas d'un budget.
4. **Les murs restants sont des murs d'accès, pas d'imagination** : maker (V), options (V), consensus PIT (D), flux ETF (D), tick futures (D), crise tick (D). À 0 FCFA, ils sont non falsifiables par construction.
5. **D8 est plafonnée par théorème** : le contrôle optimal déplace le chemin, jamais l'espérance. Phase 10 l'a chiffré aux règles exactes (plafond ≈ 20 % de passage à μ = −2 bp).

La matrice ne peut pas établir qu'il n'existe aucun edge : elle établit que dans
l'espace {8 dimensions × 5 horizons × 6 régimes} accessible à 0 FCFA, chaque cellule
est soit testée et morte, soit certifiée en service/paiement, soit fermée par un gate
de puissance, soit derrière un mur d'accès nommé. L'unique exception ouverte est C-2.

---

## ANNEXE — LES SEPT PIÈCES

### Pièce 1 — Registre seq → cellules couvertes
| Plage seq | Contenu | Cellules |
|---|---|---|
| 1–5 | Registres P3/P4, 126 hypothèses, aucun survivant | D1×H3–H5 (première génération) |
| 6–25 | Phase 1R, GLOBAL, DEEP_AXES, MONTHLY, GD07, DIST_REGIME (descriptif + candidats) | D1/D3/D4×H1–H3, R-ancien |
| 26–49 | Protocole vol gelé, VOL_MODELS, MARKET_DIMENSIONS 282/282, POST_EVENT, VOL_HOURLY, SPREAD_EPISODES, INTEGRAL_SCAN | D2/D3/D4×H1–H2 |
| 50–52 | Incident config, OWNER_CONFIG V1, décision conditionnelle | D8 (fondations) |
| 53–68 | E1 barres, E2 états, E3 mesures, E4 forward (≈ −spread), E5 gate fuite, F3 L1, F4 spread, F6 | D1/D2/D3×H1–H3 |
| 69–79 | F1, F2, F5, F7, F8 sans objet, clôture IS (144/150) | D1/D2/D4×H1–H3 |
| 80–85 | F9 non testable (MDE), F3/F7 L2, châssis + simulateur | D1×H3 (gate), D2 certifié, D8 |
| 86–92 | Panel certifié, F10/F11 échec, clôture (28/60) | D1/D6×H4–H5 |
| 93–98 | F13 4/4 non testables (n_eff < 200), clôture recherche directionnelle (148/150) | D1×H1 (gate) |
| 99–100 | Voie B : plan + journal démo (abandonnée Phase 8, seq 118) | D8 |
| 101–105 | Pack exogène certifié (PIT, DST), C3 ETF clos | D6 (ingénierie), D6 flux (D) |
| 106–107 | F14 non testable (MDE + portes 0/5) | D6×H3 (gate) |
| 108 | OWNER_CONFIG V2, C1_BG = 4,7 bp | D3/D8 (ancre) |
| 109–114 | F15 échec 0/6 (v2 honnête), F16 non testable, clôture exogène (6/60) | D5 post, D6 COT (gate) |
| 115–117 | Phase 7 : atlas M1–M6 0/30, monétisation service, clôture totale | D1/D4×H2–H5, D2 service |
| 118–121 | Phase 8 NR : collecte, atlas 0/6 + 0/30, clôture NR, HOLDOUT scellé | D1/D4×H2–H5 en R-NR |
| 122–123 | Audit coach consigné ; B2/B3 mesures descriptives | D7 prime (descriptif), D3 maker (borne) |
| 124–131 | Phase 9 : B1 échec 0/2, CARRY 2 certifiées, B2-extension, clôture (10/12) | D5 pré, D7 certifié |
| 132–134 | Phase 10 : simulation E1–E3, clôture (hors budget) | D8 |
| 135–136 | Présente matrice (hors budget) | Toutes |

### Pièce 2 — Budgets et gates
Voir §4. Gates constants du programme : préreg chaîné avant calcul ; n ≥ 200 ; R3/MDE
avant performance ; BY (jamais BH) sur le budget de la phase ; IC95 % net > 0 aux deux
ancres ; stabilité de signe 3/3 ; ECR ≥ 2. Rejet au gate = 0 essai consommé (F9, F13,
F14, F16 en sont les quatre applications documentées).

### Pièce 3 — Données et holdouts
Corpus : tick ancien 282 partitions (Kaggle, 282/282 vérifiées) ; panel 43 actifs ≤2014 ;
exogène PIT (ALFRED/FRED, `available_at_utc`, DST date par date) ; NR GC=F daily +
S3 horaire 2020 partiel + S2 spread en cron ; funding Binance Vision 913 symboles
(sélection profondeur). Holdouts anciens et HOLDOUT_NR (lake seul) : jamais ouverts.
Backfill S3 2021–2023 : non collecté (throttling IP CI), reprise par mois absents possible.
google_drive : désactivé pour cette conversation (le rappeler avant tout usage).

### Pièce 4 — Ancres de coût
C1_BG = 4,7 bp aller-retour (challenge, `OWNER_CONFIG_V2.json` seq 108, ancre historique).
Régime NR mesuré : S2 ≈ 1,35 bp, S3 intraday ≈ 2,2 bp. Carry : 40 bp aller-retour
complet amorti 1 an (déclaré prereg seq 127). Inconnues courtier jamais estimées :
slippage typique, taille de contrat, volume min/pas, tick size/value, digits — sizing
définitif conditionnel tant que la spec serveur MT5 est absente (seq 55).

### Pièce 5 — Actifs certifiés (état permanent)
F3 HAR-RV (service vol, L2) ; F7 anticipation de sauts (service, L2) ; carry funding
BTC +11,2 %/an et ETH +13,3 %/an nets (certifiés seq 129, en compression, corr 0,87,
poids 57/43 dans `meta_portfolio.py`) ; châssis durci + `meta_portfolio.py` testés
synthétique ; simulateur challenge ancré. Aucune exploitation réelle engagée : compte,
KYC, capital = décision propriétaire séparée, hors 0 FCFA.

### Pièce 6 — Incidents et leçons consignés (non rejouables)
Bug d'alignement signal/fenêtre sanctionné deux fois (F6 v1 seq 67–68 ; F15 v1 seq 112)
— jamais définir un signal sur une fenêtre qui chevauche l'entrée. Sélection carry
corrigée deux fois avant mesure (OI en unités coin ; tranche alphabétique [:60],
seq 127–129) — jamais sélectionner des candidats par leur niveau de funding.
`challenge_sim.simuler()` gelé : P(passage) = 0 mécanique sur flux continus (seq 116) —
ne pas l'utiliser pour comparer des trajectoires. Format S3 Dukascopy : t = secondes
depuis minuit UTC, prix ×1000 (lot v1 jeté). Fuite de clé FRED run2 purgée seq 105 —
**révocation par le propriétaire toujours pendante**. Logs GitHub Actions inaccessibles
depuis le sandbox : les workflows committent leurs résultats.

### Pièce 7 — Éligibilité Phase 11 (règle de l'ordre, appliquée)
Une Phase 11 ne peut naître que d'une cellule **jamais testé + mécanisme articulé +
données dans le périmètre**. Le tri du §5 n'en retient qu'une : **C-2 (dynamique du
funding)**. Conditions cumulatives si le propriétaire l'ordonne : préenregistrement
chaîné avant tout calcul sur les séries FUNDING en dépôt ; micro-budget créé par cet
ordre (aucun ancien budget n'est rechargeable) ; gates inchangés ; le portage certifié
seq 129 n'est pas un essai de C-2 et n'est pas rouvert. Toute autre cellule exige
d'abord de faire tomber son mur — donnée nouvelle certifiable, accès venue, ou temps
écoulé (C-4) — puis un ordre. Ce document, à lui seul, n'autorise rien.

---

*Fin de la matrice. Chaîne : seq 135 (MISSION P0) → seq 136 (livraison). Budgets de
recherche inchangés. Holdouts intacts. Aucune cellule rouverte.*
