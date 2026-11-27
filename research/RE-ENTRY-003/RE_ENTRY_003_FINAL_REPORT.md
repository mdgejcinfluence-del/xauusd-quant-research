# RE-ENTRY-003 — COLLECTE PROSPECTIVE DU FLUX PUBLIC HFM : SYSTÈME EN PLACE

## Phase A — Collecteur et environnement d'exécution (décision documentée)
Collecteur livré : `ci_tools/hfm_public_collector.py` (modes `fetch`, `ingest`, `baskets`).
Constat d'environnement, sans contournement : les runners CI reçoivent **403** (RE-ENTRY-002) et
le bac à sable local n'a pas d'accès sortant — multiplier les requêtes depuis ces environnements
est exclu. L'environnement retenu est donc **tout poste à navigation ordinaire** (poste du
fondateur ou session interactive autorisée) exécutant `fetch` en tâche planifiée ; le mode
`ingest` archive licitement tout contenu de page déjà obtenu. Chaque échec d'accès (403, réseau)
est journalisé comme un instantané d'échec, jamais masqué ni retenté agressivement.

## Phase B — Fréquence justifiée par l'observation
Repères mesurés : 49 595 transactions clôturées en ~1 an ≈ **136/jour ≈ 5,7/heure en moyenne** —
la fenêtre publique de 6 lignes couvre donc ~1 h en moyenne, mais par rafales (3 transactions
d'un panier en quelques minutes). Entre nos deux premiers instantanés du 2026-11-27 (à plus d'une
heure d'intervalle) : **0 nouvelle transaction** (compteur du profil inchangé à 49 595) — le
risque de perte dépend donc de l'activité, pas de l'horloge seule. Fréquence retenue : **15 minutes**
en heures actives (perte improbable : il faudrait > 6 transactions en 15 min, possible seulement
en rafale multi-paniers), 60 minutes la nuit ; le tableau de suivi signale tout écart anormal entre
instantanés comme « perte potentielle », jamais comme « absence de transactions ».

## Phases C-D — Archivage, déduplication, paniers (prouvés sur données réelles)
Deux instantanés réels du 2026-11-27 ingérés (`snapshots/`, SHA-256 du contenu, immuables) :
12 lignes visibles → **6 transactions distinctes** après déduplication par clé composite
(symbole|sens|volume|ouverture|clôture|profit — risque de collision signalé : deux transactions
réellement différentes mais identiques sur ces 6 champs seraient fusionnées à tort ; aucun
identifiant HFM n'existe pour faire mieux). Regroupement justifié (clôtures ≤ 3 s, ouvertures
séquentielles) : **3 paniers** — P001 = C (−6 ¥, perdant), P002 = D (+1 ¥), P003 = E (+3 ¥).

## Phase E — Synchronisation cotations : C/D/E désormais reconstructibles
L'heure Dukascopy 08 UTC du 2026-11-27 étant publiée entre-temps, les trois paniers sont
reconstruits (`BASKETS_CDE_RECONSTRUCTION.json`, Dukascopy comparatif, UTC+2 toujours
« fortement étayé », non prouvé) : C — entrée après +13,8 bp/15 min, ajouts à **−0,1 bp (20 s)**
puis −5,6 bp (lot 0,03), clôture **au prix moyen pondéré** (3673,56 contre 3673,52) pour un net
affiché de −6 ¥ : sortie au voisinage du point mort, négative après spreads/coûts — la clôture
« au retour au prix moyen » peut donc produire une perte nette. D — entrée après +12,2 bp/5 min,
sortie en 17 s. E — deuxième position à **+2,1 bp (favorable)** 16 s après la première.

## Phase F — Ce que les nouveaux paniers font aux hypothèses (5 paniers au total)
- Entrée après impulsion : désormais 4 paniers documentés sur 5 (A, B, C, D haussiers avant
  entrée ; E mitigé : +6,6 bp/15 min mais −3,0 bp/5 min). Toujours FORTEMENT ÉTAYÉE, seuil exact
  toujours NON DÉTERMINABLE.
- Renforcement : l'ajout n°2 survient très tôt (16–40 s) et parfois **sans** mouvement
  défavorable (E : +2,1 bp ; C : −0,1 bp), tandis que l'ajout n°3 survient à −4,7/−6,6 bp.
  Nouvelle lecture, **HYPOTHÈSE À TESTER** (préenregistrée ici, non testée) : entrée initiale en
  deux temps rapprochés, puis renforcement martingale seulement à partir de la 3e position.
- Lots : 3e position 0,02 (A, B) contre 0,03 (C) — formule toujours NON DÉTERMINABLE.
- Clôture : groupée sur 5/5 paniers ; au voisinage du prix moyen chez C comme chez A/B, avec un
  signe net qui dépend des coûts — « retour au prix moyen » = déclencheur plausible, pas garantie
  de gain.

## Phase G — Suivi et supervision
`SUIVI.json`/`PANIERS.csv`/`TRANSACTIONS.csv` sont régénérés par `baskets` à chaque instantané.
Supervision : lancer `fetch` toutes les 15 min (tâche planifiée du poste retenu), puis
`baskets` ; alerte si deux instantanés successifs diffèrent de 6 lignes nouvelles (perte
potentielle) ou si aucun instantané n'arrive pendant 2 h en session active ; reprise après
interruption = simple relance (les instantanés sont indépendants, aucun état à reconstruire).
Limite d'accès finale : pas d'automatisation possible depuis CI ou ce bac à sable sans
contourner le 403 — ce qui est refusé par principe.
