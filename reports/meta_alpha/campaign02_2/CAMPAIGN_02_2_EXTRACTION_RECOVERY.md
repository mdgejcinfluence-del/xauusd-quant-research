# CAMPAGNE 2.2 — PLAN DE REPRISE DE L'EXTRACTION

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Aucune donnée ne doit
être fabriquée, imputée ou déclarée complète sans preuve.

## Diagnostic séparé des deux pannes

**403 Kaggle.** La librairie `kaggle==1.6.17` reçoit 403 Forbidden sur les 8
datasets privés (`shalom5123/xauusd-is-b01..b07`, `xauusd-is-missing13`), slug
propriétaire corrigé compris ; le repli HTTPS direct (Bearer puis basic auth)
ajouté au moteur reçoit la même réponse. Constat déjà rencontré dans le programme
(seq 141 : 403 de la même librairie, contourné alors par Drive). Hypothèses non
tranchées, à vérifier côté propriétaire du compte : clé API héritée révoquée ou
remplacée par un jeton d'un format que la librairie ne sait pas présenter ;
permissions des datasets. **Action requise hors sandbox** : régénérer/vérifier la
clé Kaggle du compte `shalom5123` et mettre à jour les secrets CI
(`KAGGLE_USERNAME`, `KAGGLE_KEY`) — aucune manipulation d'identifiants n'est
faite ici.

**Quota Drive.** `gdown` reçoit « Too many users have viewed or downloaded this
file recently » sur les partitions testées. Ce refus est temporaire (message de
Google : réessai sous 24 h) et a été aggravé par les trois tentatives
d'extraction de la campagne (≈ 282 partitions chacune). **Règle de reprise :
ne pas multiplier les téléchargements Drive** tant que le quota n'est pas
rétabli ; un seul passage par lot, dans l'ordre, avec journal.

## Possibilités de reprise (par ordre de préférence)

1. **Kaggle réparé** (clé régénérée) : relancer la matrice 8 lots telle que
   commitée ; chaque lot télécharge son dataset en une fois (≈ 40 partitions),
   écrit `timeline_parts/<lot>_*.csv` + couverture, commit séparé. Contrôles :
   somme des journées par lot, total ≥ 2 400 journées et recoupement des comptes
   d'épisodes avec le brut Campagne 1 sur tout le corpus avant toute synthèse.
2. **Drive rétabli** (quota reposé, sans nouvelle sollicitation entre-temps) :
   même matrice, le repli Drive existant du moteur prend le relais lot par lot ;
   ne lancer qu'une fois, jamais de relance en boucle.
3. **Reprise depuis l'existant** : l'extraction partielle validée (2010 →
   2014-03) est déjà commitée et sert de premier lot de fait ; la reprise ne doit
   produire que les périodes manquantes (à partir de mars 2014) puis fusionner
   par déduplication sur `date|grappe|snapshot_min`, en conservant les parties
   séparées comme preuve.

## Garde-fous de la reprise

- Procédure identique au gel seq 170 : aucun paramètre modifié après consultation
  des résultats partiels ; les statistiques T0 du périmètre restreint ne doivent
  pas influencer les seuils de la reprise (les terciles seront recalculés sur le
  périmètre repris, de façon documentée).
- Aucune synthèse décennale publiée tant que la matrice de couverture
  (ère × famille) n'est pas complète et recoupée ; toute période encore manquante
  sera écrite comme manquante.
- Un seul run à la fois ; en cas de nouvel échec d'accès, journal commité et arrêt,
  pas de retry agressif (protection du quota).
