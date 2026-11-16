# COMPARAISON MULTI-GRANULARITE (Mission 1R-02, artefacts Phase 1R tache 1)

Formules: medianes et IQR des agregats par partition (n=282 par granularite);
Spearman = correlation de rangs inter-partitions. Unites: rendements et
volatilite en bp (fraction x 10 000), spread relatif en bp, intensite en ev/s.
Segments mensuels = lignes partition-mois de MONTHLY_SERIES.csv (1191 lignes,
397 par granularite), pas des mois calendaires purs.

## Dependances temporelles (ac1 rendements de barres)
| Granularite | ac1 mediane | IQR | % partitions < 0 | T1 | T2 | T3 |
|---|---:|---|---:|---:|---:|---:|
| G_EVT100 | -0.0003 | [-0.034; 0.039] | 50% | +0.010 | -0.005 | -0.009 |
| G_ACT500 | -0.017 | [-0.075; 0.020] | 63% | -0.019 | -0.011 | -0.020 |
| G_VOL10bp | -0.112 | [-0.180; 0.002] | 72% | -0.152 | -0.005 | +0.001 |
Concordance inter-granularites de l'ac1 par partition: rho 0.12 a 0.27 (faible).
Le niveau d'ac1 d'une partition depend donc d'abord de la granularite choisie.

## Distributions (medianes des quantiles de partition, en bp)
| Granularite | p1 | p25 | p50 | p75 | p99 | ratio p99/|p1| | vol p50 | vol p95/p50 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G_EVT100 | -9.94 | -1.84 | -0.01 | +1.86 | +10.46 | 1.05 | 3.62 | 1.88 |
| G_ACT500 | -20.13 | -3.34 | 0.00 | +3.50 | +22.34 | 1.11 | 8.12 | 1.68 |
| G_VOL10bp | -6.05 | -1.37 | -0.01 | +1.36 | +6.41 | 1.06 | 2.33 | 1.49 |
Queues descriptivement symetriques aux 3 echelles; aucune asymetrie directionnelle.

## Spread, rythme, relations croisees (inter-partitions, n=282)
Spearman identiques en signe aux 3 granularites: spread~intensite -0.76 a -0.82;
spread~volatilite +0.71 a +0.78; intensite~volatilite -0.54 a -0.69.
Segments partition-mois: memes signes (spread~intensite -0.81 a -0.84).
**Limite majeure:** correlations ecologiques melangeant 2010-2020; la derive
entre tiers (spread 4.04 -> 1.92 bp, intensite 0.93 -> 2.81 ev/s, vol_p50
3.96 -> 1.47 bp en EVT100) peut porter l'essentiel de ces correlations.
Aucune lecture causale ni intra-periode n'est autorisee par ces agregats.

## Avertissement tiers
Tiers tres desequilibres en partitions (218/33/31) et en taille de partition
(barres medianes EVT100: 683 / 26 236 / 43 282). Toute comparaison brute entre
tiers melange evolution temporelle, decoupage du corpus et densite du flux.
