# META ALPHA — GLOBAL MARKET BEHAVIOUR DISCOVERY : RAPPORT GLOBAL

Perimetre reel: **282 partitions IS, 288 086 588 ticks (2010-2020)** lues a
distance (run **43820220182, success, 2 h 14**, 0 Fcfa). OOS et Holdout jamais
ouverts. Pre-enregistrement GLOBAL_PREREG.json verrouille (chaine seq 11-12).
Statut de tout ce qui suit: exploration descriptive; aucune confirmation
independante; aucun test de strategie; aucune hypothese testee.

## Bug propre a cette mission (documente, non masque)
Les colonnes share_bonly/share_aonly/share_both du fichier tick sont **invalides**:
sur fixture, `bid-lag(bid)` etait lu comme une difference et non comme le lag,
donnant 0/1 partout. Prouve sur fixture a jambes independantes (les correlations
croisees y valent ~0, ce qui valide le reste du moteur). Colonnes exclues;
les parts utilisees sont celles, validees, des vagues precedentes
(bid-seul/ask-seul 0.59%/0.59%, bilateraux 98.52%). Script corrige pour l'avenir.

## 1. Le phenomene tick n'est pas un invariant: il s'effondre avec l'epoque
Autocorrelation lag-1 des rendements mid, medianes par tiers d'IS:
**T1 0.497 -> T2 0.113 -> T3 0.034.** Par jambe: bid 0.105 -> -0.057.
La memoire de volatilite suit la meme pente (ac|r| lag1: 0.472 -> 0.184 -> 0.158).
ANOM-001 decrivait donc surtout le marche/flux des premieres annees, pas une
loi permanente du XAUUSD. Explications concurrentes ouvertes: changement de
densite ou de nature du flux fournisseur, evolution reelle du marche.

## 2. Bid/Ask: pas de leader, une synchronisation oscillante
Correlation croisee des rendements par jambe (mediane 282 partitions):
decalage -5..+5: -0.016, -0.108, -0.076, -0.125, **+0.528, +0.412 (0), +0.530**,
-0.124, -0.074, -0.109, -0.016. Le profil est **symetrique**: correlation a
+/-1 evenement (0.53) superieure au contemporain (0.41), negative a +/-2.
Aucune jambe ne precede l'autre descriptivement; le motif evoque des mises a
jour quasi synchrones avec oscillation microstructurelle a 1-2 evenements.
La piste lead-lag ouverte depuis la validation profonde est ainsi **refermee
descriptivement**: il n'y a pas d'avance directionnelle a exploiter, meme en
principe. Aucune conclusion causale ou predictive n'est tiree.

## 3. Carte des echelles: ou les dependances vivent et meurent
ac1 des rendements de barres (mediane 282): 10 evenements **-0.138**;
30 s **-0.126**; 50 evt -0.017; 60 s -0.023; **100 evt -0.0003**; 300 s -0.011;
500 evt -0.017; 1000 evt -0.031. Une reversion descriptive existe a tres petite
echelle (10 evt/30 s) et s'eteint vers 100 evenements/60 s. Elle n'a jamais ete
confrontee au spread dans un test: aucune valeur economique n'est affirmee.
La volatilite, elle, garde sa memoire a toutes les echelles (ac|r| tick
0.457/0.184/0.132) — comportement continu classique.

## 4. Spread et activite
Spread relatif median 3.99 bp (p95 5.06, p99 5.69); persistance tick 0.633,
en hausse entre tiers (0.583 -> 0.826). Les relations spread/activite/volatilite
deja vues (1R-02) restent ecologiques et confondues par l'epoque: non reinterpretees.

## 5. Anomalies et structures (registres joints)
GD-01 effondrement historique de l'ac1 tick; GD-02 motif croise bid/ask
symetrique; GD-03 reversion a 10 evt/30 s; GD-04 persistance du spread;
GD-05 memoire de volatilite era-dependante. Structures: volatilite a memoire
continue, microstructure era-dependante, dependance d'echelle — toutes
explicables par des mecanismes continus ou de cotation.
**Aucun regime discret n'est demontrable a l'issue de cette exploration**:
aucune structure ne s'est imposee qui exige du discret, et aucune n'a ete
testee a protocole gele contre les modeles continus (hors perimetre). Les
modeles continus restent l'explication de reference.

## Resultats negatifs et non concluants (conserves)
Lead-lag directionnel: absent. Regimes discrets: non demontres. Colonnes
shares du run: invalides (bug ci-dessus). Relations inter-partitions de 1R-02:
ecologiques, non causales.

## Questions pour une phase ulterieure (non testees, non preenregistrees)
(1) L'effondrement de l'ac1 tick est-il un effet de flux ou de marche?
(2) Le motif croise +/-1 evenement est-il stable par epoque?
(3) La reversion a 10 evenements/30 s survit-elle a une confrontation au
spread a protocole gele? Leur transformation en hypotheses exige la procedure
gouvernee habituelle et une decision du proprietaire.

## Limites
Medianes de partitions; tiers desequilibres (218/33/31) et tailles de partitions
heterogenes; mid = construction; tick != transaction; aucune session supposee.
Point de reprise: decision du proprietaire sur les questions ci-dessus ou
cloture. Preuves: run 43820220182, chaine, hashes des CSV et du code joints au
commit de ce rapport (GLOBAL_*_PARTITION.csv, GLOBAL_MARKET_OBSERVATION.json,
NATURAL_GRANULARITY_MAP.json, MARKET_ANOMALY_REGISTER.json,
BEHAVIOURAL_STRUCTURE_MAP.json, MARKET_DISCOVERY_LEDGER.json,
GLOBAL_DISCOVERY_EXECUTION_MANIFEST.json).
