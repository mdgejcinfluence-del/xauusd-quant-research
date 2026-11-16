# ANOM-001 — REVUE APPROFONDIE SUR ARTEFACTS EXISTANTS (Mission 1R-02)

Statut de la mission: EXPLORATION DESCRIPTIVE. Aucune relecture de partitions,
aucun tick relu. Sources: ANOMALY_REGISTRY.json, rapport Phase 1R tache 1,
PARTITION_GRANULARITY.csv (parts bid-seul/ask-seul agregees par barre).

## Distinctions imposees (rappel methodologique)
1. Autocorrelation des rendements mid (ce qui vaut 0.487 au tick).
2. Autocorrelation des rendements bid seuls / ask seuls (historique validation
   profonde: 0.063 / 0.060 — non recalculable ici, aucun artefact par jambe).
3. Correlation croisee bid/ask aux decalages -5..+5 evenements: **NON PRESENTE**
   dans les artefacts disponibles (ni series par jambe, ni matrice de lags).
4. Lead-lag descriptif: depend de (3) — **non resolu**.
5. Synchronisation des mises a jour: mesuree historiquement (98.52% d'evenements
   bilateraux, 0.59% bid-seul, 0.59% ask-seul).

## Ce que les artefacts 1R confirment
- Parts agregees par barre (282 partitions, medianes): bid-seul 0.529-0.601%,
  ask-seul 0.529-0.624% selon granularite; difference mediane -0.005 a -0.013
  point; 45-47% de partitions avec bid-seul > ask-seul. Symetrie coherente avec
  la validation profonde; aucun desequilibre directionnel descriptif.
- L'autocorrelation lag-1 des rendements de BARRES mid vaut -0.0003 (EVT100),
  -0.017 (ACT500): la signature tick ne survit pas a l'agregation en barres.

## Ce que cela ne demontre pas
La disparition de l'autocorrelation apres agregation concerne les rendements
de barres mid. Elle ne refute ni ne confirme une correlation croisee decalee
entre jambes: une avance de quelques evenements d'une jambe sur l'autre serait
precisement lissee par des barres de 100+ evenements. Confondre les deux
mesures serait une erreur — la mission le signale explicitement.

## Etat final ANOM-001 (reponse a la mission)
**Phenomene tick reproduit (vagues precedentes, 282/282); mecanisme initial
refute; reexamen bid/ask decale IMPOSSIBLE avec les artefacts agreges actuels.**
Il manque, pour trancher le lead-lag: soit les sequences d'evenements par jambe
par partition, soit une matrice de correlations croisees -5..+5 precalculee.
Produire l'une ou l'autre exigerait une nouvelle lecture des partitions IS:
hors perimetre 1R-02, a autoriser distinctement si le proprietaire le souhaite.
Aucune hypothese n'est generee a partir de cet etat.
