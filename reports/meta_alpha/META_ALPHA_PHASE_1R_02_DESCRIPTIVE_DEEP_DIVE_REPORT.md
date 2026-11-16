# META ALPHA — MISSION 1R-02 : EXPLORATION DESCRIPTIVE APPROFONDIE

Cadre: protocole 1R FINAL + gouvernance multiplicite. Perimetre respecte:
**artefacts existants uniquement** — aucune partition, aucun tick, aucun OOS,
aucun Holdout relu. Statut de tous les resultats: **EXPLORATION DESCRIPTIVE**.
Mission inscrite a la chaine avant calculs (seq 9, tete 4fd47465...).
Aucune nouvelle famille inferentielle, aucune p-value ajoutee.

## 1. Artefacts reellement examines (verifies, hashes conformes au rapport tache 1)
- `reports/meta_alpha/phase1r/PARTITION_GRANULARITY.csv` — 846 lignes (282x3), SHA df08a6ba...
- `reports/meta_alpha/phase1r/MONTHLY_SERIES.csv` — 1191 lignes partition-mois, SHA de97a9a0...
- `PHASE_1R_PREREG.json` (ddd09ef3...), moteur `phase1r_series.py` (049f238c...),
  STATE.json (282/282), ANOMALY_REGISTRY.json, rapports tache 1 et validation profonde.
- Commit distant verifie: 6663913; run 43752027483: success (GitHub API).
- Chaine TRIAL_LEDGER_CHAIN: 8 entrees a l'ouverture, valide, tete eb7b4d26...

## 2. Calculs derives reellement effectues
Medianes/IQR/quantiles des agregats par partition; ventilation par tiers d'IS
(T1=218, T2=33, T3=31 partitions); Spearman inter-partitions (n=282) et sur
segments partition-mois; ratios de queues p99/|p1|; parts bid-seul/ask-seul;
concordances d'ac1 entre granularites. Code execute en session sur les CSV,
resultats reproduits dans MULTI_GRANULARITY_COMPARISON.md et le registre
DESCRIPTIVE_PHENOMENA_REGISTER.json (9 phenomenes F01-F09).

## 3. ANOM-001: etat precis (detail: ANOM_001_DEEP_REVIEW.md)
Phenomene tick **reproduit** historiquement (ac1 mid 0.487, 282/282);
mecanisme "mises a jour separees" **refute** (98.52% d'evenements bilateraux).
Artefacts 1R: symetrie bid-seul/ask-seul confirmee (0.53-0.62% chaque jambe).
**Correlation croisee decalee bid/ask (-5..+5): non calculable** — aucun artefact
ne contient les series par jambe ni l'ordre fin des evenements. La disparition
de l'autocorrelation en barres (-0.0003 a 100 evenements) est une mesure
differente: elle ne refute pas un lead-lag, qui serait lisse par l'agregation.
Verdict de mission: **reexamen partiel; lead-lag non resolu faute d'artefact.**

## 4. Comparaison des trois granularites (faits calcules)
- ac1: ~0 (EVT100), -0.017 stable en signe mais faible (ACT500), -0.112 mais
  concentre sur T1 (VOL10bp: -0.152 / -0.005 / +0.001) → non concluant.
- Concordance de l'ac1 d'une partition entre granularites: rho 0.12-0.27 seulement.
- Queues de rendements symetriques aux 3 echelles (p99/|p1| = 1.05-1.11), mediane ~0.
- Relations inter-partitions fortes en Spearman (spread~intensite -0.76..-0.82;
  spread~vol +0.71..+0.78) mais **ecologiques** (melange d'epoques, cf. §6).

## 5-6. Relations supplementaires et stabilite entre tiers
Stables en signe: ac1 ACT500 negatif faible (3 tiers); symetrie des queues;
symetrie bid/ask; signes des Spearman aux 3 granularites.
Derive monotone entre tiers (vol et spread en baisse, intensite en hausse) —
**interpretation bloquee**: tiers desequilibres (218/33/31 partitions; tailles
de partitions de 683 a 43 282 barres medianes) et possible changement de
densite du flux fournisseur. Ce n'est pas une evolution de marche etablie.

## 7. Resultats instables, negatifs, non concluants
- VOL10bp ac1: instable → NON CONCLUANT (artefact de construction possible:
  fermeture par budget cumule de |r|).
- EVT100 ac1: nul (resultat negatif propre, pas un echec).
- Aucun phenomene nouveau promu; aucun nombre impose. Registre F01-F09 joint,
  tous en EXPLORATION DESCRIPTIVE.

## 8. Analyses impossibles avec les artefacts (donnees manquantes precises)
| Analyse | Manquant | Pourquoi les agregats ne suffisent pas | Perimetre requis (autorisation distincte) |
|---|---|---|---|
| Correlation croisee bid/ask -5..+5, lead-lag | series d'evenements par jambe ou matrice de lags par partition | les parts bid/ask agregees perdent l'ordre et les delais | relecture IS tick (bid, ask, horodatages) sur 282 partitions, ou calcul distant dedie |
| Autocorrelations bid-seul / ask-seul | rendements par jambe | seul le mid est agrege | idem |
| Distributions d'inter-arrivees | quantiles des deltas temps | seule l'intensite moyenne par barre existe | idem |
| Comportement post-gap fin | series autour des gaps | les barres excluent les franchissements de gaps par construction | idem |
| Relations intra-periode (de-confoundues) | agregats par fenetre temporelle homogene | partitions de tailles tres heterogenes melangeant les epoques | re-agregation par mois calendaires depuis les ticks, ou artefacts mensuels par partition plus fins |
Aucune de ces lectures n'a ete faite. Elles attendent une autorisation distincte.

## 9-11. Fichiers, commits, reprise
Fichiers crees: ce rapport, ANOM_001_DEEP_REVIEW.md,
MULTI_GRANULARITY_COMPARISON.md, DESCRIPTIVE_PHENOMENA_REGISTER.json,
PHASE_1R_02_EXECUTION_MANIFEST.json (dossier phase1r_02/), chaine mise a jour.
Point de reprise exact: decision du proprietaire sur (a) clore l'exploration
descriptive, ou (b) autoriser distinctement un calcul distant cible lead-lag
bid/ask sur IS, ou (c) autre orientation. Aucune suite n'est engagee.

## Limites generales
Agregats de partitions (pas de pooled tick); medianes robustes mais dispersion
inter-partitions large; segments "mensuels" = partition-mois; selection
cumulative IS partagee entre toutes les vagues (148 tests + vagues
descriptives): rien ici n'est une confirmation independante.
