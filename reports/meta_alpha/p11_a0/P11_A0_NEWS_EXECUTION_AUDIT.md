# P11-A0 — AUDIT DESCRIPTIF DE LA CAPTURABILITÉ DES MOUVEMENTS POST-ANNONCE

**Autorisation propriétaire du 2026-11-18 (seq 139). Étape préalable uniquement.**
Ce n'est ni une Phase 11, ni une recherche de signal directionnel, ni une réouverture
de F15. Aucun budget expérimental consommé, aucune donnée téléchargée, aucun paramètre
optimisé, aucune « meilleure minute » recherchée, aucun taux de réussite stratégique
calculé, aucun edge déclaré. La version F15-v1 purgée (seq 112) n'a pas été utilisée.
Holdouts intacts. Données : exclusivement les artefacts déjà présents dans le dépôt Git.

**Question unique :** les mouvements des cinq premières minutes post-annonce sont-ils
réellement inexploitables par un particulier, ou leur impossibilité d'exploitation
est-elle simplement présumée ?

**Statut final autorisé : audit descriptif terminé, décision stratégique en attente
du propriétaire.**

---

## 1. Ce qui existe dans le dépôt — et ce qui n'y existe pas

L'audit ne peut mesurer que ce que les artefacts locaux contiennent. Inventaire honnête :

| Artefact en dépôt | Contenu exploitable pour P11-A0 | Limite |
|---|---|---|
| `phase6/f15_events/F15_EVENT_PNL.csv` (v2, seq 112–113) | Par événement réel (346 lignes après exclusion des placebos ±30 j) : spread coté **au tick d'entrée ≥ T+5 min**, amplitude du premier mouvement T→T+5, PnL exécutables passés à 15/60/240 min (rappel descriptif) | **Un seul instant de spread par événement : T+5.** Aucune trajectoire T−5→T+30 |
| `phase7/ATLAS_DATA.json` M2 (seq 116) | Médianes d'amplitude \|mouvement\| à 5/15/60/240 min et spread médian d'entrée, par type | Médianes seulement ; pas de distribution par minute |
| `phase6/F15_F16_GATES.json` (seq 109) | Spread médian IS global 2,33 bp ; ancres C1_hist 3,33 bp / C1_BG 4,7 bp aller-retour | Référence globale, pas de profil événementiel |
| Tick brut 282 partitions | **Absent du dépôt Git** (lac Kaggle externe aux artefacts versionnés) | Le téléchargement étant interdit par l'autorisation, aucune trajectoire tick n'a été reconstituée |

Conséquence directe, écrite avant tout résultat : la fenêtre documentaire T−5→T+30
demandée n'est mesurable localement qu'en **un point** (l'entrée T+5 de la v2). Tout le
reste relève du « NON MESURABLE AVEC LES DONNÉES DISPONIBLES » — c'est un résultat de
l'audit, pas une esquive.

## 2. Mesures produites (descriptives, par événement : `P11_A0_EVENT_MEASURES.csv`)

### A. Comportement du spread

Spread coté au premier tick ≥ T+5 min (mesure réelle, artefact v2), par famille :

| Famille | n | Médiane | P90 | P95 | P99 | Max |
|---|---|---|---|---|---|---|
| FOMC | 81 | 2,64 bp | 4,40 | 4,97 | 5,86 | 6,72 |
| NFP | 129 | 2,51 | 4,64 | 6,61 | 12,58 | 24,65 |
| CPI | 136 | 2,28 | 4,01 | 4,90 | 12,41 | 24,65 |

Référence : spread médian IS global 2,33 bp (gate seq 109). À T+5, le spread médian est
donc **proche de son niveau habituel** (2,3–2,6 bp), avec une queue droite réelle
(P99 ≈ 6–13 bp selon la famille, max 24,7 bp).

**NON MESURABLE AVEC LES DONNÉES DISPONIBLES** (aucun artefact local ne les contient) :
spread avant l'annonce (T−5) par événement ; spread à T+1, T+2, T+3, T+4 ; durée des
épisodes de spread élevé ; délai de retour au spread habituel ; fréquence des cotations
manquantes ou périmées. Aucune de ces quantités n'a été imputée ni approximée.

### B. Comportement des cotations

Bid/Ask ne sont présents dans les artefacts que via le spread d'entrée et les PnL
exécutables passés (entrée Ask/sortie Bid et inverse, v2). Le prix médian (Mid) par
événement n'est pas versionné tick par tick. L'écart entre un « prix théorique » à un
instant de décision et le premier prix observable après cet instant — la mesure centrale
de la capturabilité — exige la série tick : **NON MESURABLE AVEC LES DONNÉES
DISPONIBLES** dans le périmètre autorisé.

### C. Coût d'exécution — distinctions impératives

| Composante | Statut dans cet audit |
|---|---|
| Spread coté à T+5 | **MESURÉ** (tableau §2.A) |
| Spread coté T+1→T+4 | NON MESURABLE AVEC LES DONNÉES DISPONIBLES |
| Slippage réel | **NON MESURABLE AVEC LES DONNÉES DISPONIBLES** — le dépôt ne contient aucune donnée d'exécution réelle (aucun fill, aucun journal de broker) ; il n'est présenté nulle part comme mesuré |
| Slippage simulé | Non produit : toute simulation exigerait des hypothèses de latence/remplissage que l'autorisation demande d'expliciter, et aucune base mesurée locale ne permet de les calibrer ; le présenter chiffré serait fabriquer une précision |
| Commission | Connue par config (0,5 bp/côté, `OWNER_CONFIG_V2`) ; incluse dans les ancres C1_hist 3,33 / C1_BG 4,7 bp aller-retour |
| Latence et incertitude de remplissage | NON MESURABLE AVEC LES DONNÉES DISPONIBLES — une cotation affichée ne garantit pas qu'un ordre transmis par un particulier aurait été exécuté à ce prix, en particulier dans les secondes d'ajustement |

### D. Capturabilité — quatre possibilités distinctes

1. **Transmettre un ordre** après `available_at_utc` : techniquement possible pour un particulier (fait de plateforme, pas une mesure).
2. **Obtenir une exécution** : non démontrable avec les artefacts — dépend de la latence et de la liquidité offerte à l'instant exact, non versionnées.
3. **Prix réellement accessible** : seul le spread coté à T+5 est mesuré (médiane ≈ habituelle, queue jusqu'à ~25 bp) ; le prix accessible à T+1→T+4 est inconnu.
4. **Rentabilité après coûts** : hors périmètre de l'audit (ce serait un test stratégique ; les rappels F15 à 15/60/240 min existent mais ne disent rien de la fenêtre 1–5 min, et les mouvements bruts de 11,4/12,3/6,8 bp — amplitudes médianes du premier mouvement, **antérieur à toute entrée licite** — ne sont assimilés à aucun rendement capturable, conformément à l'interdiction §4 de l'autorisation. Aucune comparaison de ces amplitudes au seuil de 9,4 bp n'est présentée : métriques, horizons et conditions d'exécution ne sont pas comparables.)

## 3. Tableau de classification des quantités

| Quantité | Réelle (mesurée) | Estimée (hypothèses explicites) | Non mesurable (données disponibles) |
|---|---|---|---|
| Spread coté à T+5 (méd/P90/P95/P99, par famille) | ✔ (§2.A) | | |
| Ancres de coût aller-retour C1_hist / C1_BG | ✔ (config + tick passé) | | |
| Amplitude du premier mouvement T→T+5 | ✔ (descriptive, non capturable) | | |
| Spread T−5, T+1→T+4 ; durée d'épisode ; retour à la normale | | | ✔ |
| Cotations manquantes/périmées | | | ✔ |
| Slippage réel ; latence ; probabilité de remplissage | | | ✔ |
| Slippage simulé | | (non produit, faute de calibration mesurée) | |

## 4. Clarification de la matrice (point 6 de l'autorisation)

La matrice v2 (seq 138) recense **six familles J** (jamais testées) : (1) C-2 dynamique
du funding ; (2) fenêtre événementielle T+1→T+5 ; (3) grilles combinées F3×F7×momentum
(B7-7/11/12) ; (4) vol hebdomadaire / rupture de calibration NR (D2) ; (5) fin de mois /
roll spot (D4) ; (6) inter-marchés minute/heure (défaut de recouvrement). Il n'a jamais
été dit que la fenêtre news est la seule case J.

Deux notions distinctes, à ne pas confondre :

- **Statut J** = constat documentaire : aucune entrée des 138 seq ne couvre la cellule.
- **Éligibilité à une future expérience** = jugement supplémentaire exigeant, selon la
  règle P0, un mécanisme économique articulé **et** des données dans le périmètre.
  C-2 est la seule famille J à satisfaire ces deux critères. La fenêtre T+1→T+5 est J
  **sans** cette éligibilité établie : le présent audit P11-A0 n'est pas l'expérience
  qui la testerait — c'est l'étape préalable, autorisée séparément, qui détermine si
  une expérience future mérite même d'être proposée.

## 5. Verdict

**CAS B — IMPOSSIBLE À ÉTABLIR.**

Motivation, en trois points :

1. **Le CAS A (inexploitable) n'est pas démontrable** : la seule mesure de coût dans la
   fenêtre (spread à T+5, médiane 2,3–2,6 bp ≈ niveau habituel) ne montre pas un mur de
   coût à T+5, et les minutes décisives T+1→T+4 sont non mesurées. Déclarer la fenêtre
   inexploitable exigerait précisément les mesures absentes.
2. **Le CAS C (potentiellement exploitable) n'est pas démontrable** : il faudrait établir
   qu'une exécution réelle à prix connu est possible après `available_at_utc` dans les
   minutes 1–5, slippage et remplissage inclus — quantités non mesurables avec les
   données disponibles, et dont l'absence interdit toute conclusion économique.
3. **La limitation est nommée** : ce n'est ni un mur de venue (classe I-venue : le tick
   existe dans le lac du programme) ni un mur de puissance (classe P : les gates F15
   étaient TESTABLES) — c'est une **insuffisance d'artefacts dans le périmètre autorisé**
   (dépôt Git seul, téléchargement interdit). La piste reste donc **J** (classe J de la
   matrice), et aucune conclusion économique définitive n'est autorisée.

Ce que l'audit établit positivement : l'« impossibilité d'exploitation » de la fenêtre
1–5 min était, à ce jour, **présumée** (par le préreg F15 qui entre à T+5 et par
l'exclusion documentaire de la v2 de la matrice), non mesurée ; et la seule mesure
réelle disponible (spread à T+5) ne la confirme ni ne l'infirme pour T+1→T+4.
Conformément à l'autorisation, **aucune proposition de protocole n'est soumise** : elle
ne le serait que dans le CAS C. Si le propriétaire souhaite lever l'insuffisance, la
décision qui lui revient est documentaire avant d'être statistique : autoriser ou non
la reconstitution, depuis le lac Kaggle du programme (données déjà collectées, aucun
achat), des trajectoires de spread T−5→T+30 — mesure descriptive qui ne testerait
toujours aucune hypothèse directionnelle.

## Annexe — Qualité et disponibilité des données

| Source | Couverture | Qualité constatée | Risque pour l'audit |
|---|---|---|---|
| F15_EVENT_PNL.csv | 346 événements réels (367 avec placebos exclus) : FOMC 81, NFP 129, CPI 136 ; IS jusqu'au 2020-01-20 | Extraction v2 alignement vérifié (seq 112) ; timestamps `available_at_utc` PIT | Un instant de spread par événement seulement |
| ATLAS_DATA.json M2 | Médianes par famille (n = 81–136) | Descriptif pur, aucun PnL signé (par ordre Phase 7) | Pas de quantiles par minute |
| F15_F16_GATES.json | σ 60 min, spread médian IS, ancres | Calculé avant performance (gate R3) | Référence globale, pas événementielle |
| B1_EVENT_PNL.csv | 1 039 lignes (fenêtre pré-annonce) | Même moteur v2 | Hors fenêtre post-annonce ; non utilisé pour les mesures A–D |
| Tick brut | 282 partitions au lac Kaggle | Vérifié 282/282 lors de la migration | **Non présent dans le dépôt Git** ; téléchargement interdit par l'autorisation |
| Données d'exécution réelle | — | Inexistantes dans le dépôt | Slippage/remplissage structurellement non mesurables (CAS B) |

## Section séparée — Sécurité FRED (point 7 de l'autorisation)

Vérifications effectuées sans jamais afficher ni demander la valeur de la clé :

| Contrôle | Résultat |
|---|---|
| Présence dans le dépôt GitHub (arbre HEAD actuel) | **Aucune valeur littérale** : le code lit `os.environ['FRED_API_KEY']` (`ci_tools/exogenous_complete.py`) et assainit toute URL avant journalisation (`api_key=<redacted>`) ; le grep HEAD pour une valeur longue de type clé retourne 0 occurrence |
| GitHub Actions Secrets | Le workflow `exogenous_pack_v2.yml` injecte `${{ secrets.FRED_API_KEY }}` (référence, jamais en clair). L'énumération des secrets via l'API retourne 403 depuis ce sandbox : la liste des secrets n'est pas vérifiable d'ici — à confirmer visuellement par le propriétaire dans Settings → Secrets |
| Journaux de compilation (Actions) | Inaccessibles depuis le sandbox (limitation connue, consignée) ; le code actuel assainit ses propres logs, mais l'historique des runs anciens n'est pas auditable d'ici |
| Historique Git | **Exposition historique confirmée et déjà consignée (seq 105)** : les commits `cfd3df5`, `833f13b` et `b144080` contiennent des URL de manifeste d'erreur incluant la valeur de la clé ; purge effectuée à HEAD par `7c0ebec` (« cle strippee, erreurs sanitisees »), mais la valeur demeure dans l'historique des commits ancêtres |

**Conclusion sécurité : la rotation de la clé reste nécessaire et toujours pendante
côté propriétaire** (une purge HEAD ne retire pas une valeur de l'historique Git).
Aucune valeur n'a été affichée, loguée ou transcrite dans le présent audit, et il n'est
demandé au propriétaire ni de la communiquer, ni autre chose que la révocation/rotation
auprès de FRED puis la mise à jour du secret GitHub Actions correspondant.

*Fin de l'audit. Livrables : le présent rapport, `P11_A0_EVENT_MEASURES.csv` (346
événements), `P11_A0_RESUME.json`, `ci_tools/p11_a0_audit.py`. Chaîne : seq 139
(autorisation consignée) → seq 140 (livraison). Décision stratégique : en attente du
propriétaire.*
