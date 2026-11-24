# PHASE 21-D — AUDIT SOURCE TICK

Statut : EXPLORATORY_POST_HOC. Ticks IS Kaggle (timestamp_utc, bid, ask), Mid=(bid+ask)/2, journees certifiees 21-A uniquement, holdout jamais accede.

- Journees tick reconstruites : 1973 (certifiees 21-A : 1992)
- Journees scindees entre deux lots, exclues des analyses (fragments partiels, jamais fusionnees) : ['2010-03-18', '2010-06-01', '2010-10-28']
- Ticks totaux traites : 223052554
- Doublons timestamp : 0 ; bid>ask : 0 ; prix non positifs : 0
- Journees avec gap > 300 s : 1812 (cause non etablie : GAP_CAUSE_UNVERIFIED)
- Aucune interpolation, aucun comblement. Ordre final des extremes : retrospectif uniquement, jamais predictif.