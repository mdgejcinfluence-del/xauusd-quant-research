# META ALPHA — REGISTRE DES MODÈLES ÉCONOMIQUES

*Bibliothèque vivante (mission fondatrice 009). Un modèle n'est jamais
VALIDATED sur les données qui ont servi à le construire.*

## ME-001 — INVENTORY_RECOVERY (récupération d'inventaire)

- **Origine** : Colorful drops (HFM 99001292), 5 paniers / 12 transactions.
- **Source potentielle de rendement** : fenêtres de récupération — le
  prix revient au voisinage du prix moyen pondéré après une excursion
  adverse, permettant une liquidation proche de l'équilibre avec un
  gain faible mais fréquent.
- **Mécanisme** : entrées acheteuses sur contexte favorable, accumulation
  progressive sur recul (−4,7 à −6,6 bp observés), PWA déplacé vers le
  prix, sortie pendant une jambe favorable proche du PWA.
- **Risque rémunéré accepté** : porter une exposition défavorable
  croissante sans stop observé ; risque de non-récupération et de queue
  (inconnu chez le provider).
- **Signatures observées** : renforcements 65–88 % du temps sous le PWA
  avant récupération, clôtures −0,25 à +7,9 bp du PWA, ΔPnL 30 s positif
  avant 5/5 clôtures (DIRR-003, CDME-004, EIDR-005, EMI-006).
- **Hypothèses concurrentes** : cadence interne, condition hybride,
  variable hors-Mid (équivalentes sur 5 clôtures) ; fourniture de
  liquidité NON démontrée (renforcements ≠ market making).
- **Détection dans nos données** : signature mesurable dans le corpus
  (trajectoires de retour au prix moyen après excursion) — test de
  fréquence/rendement net pas encore exécuté comme modèle autonome.
- **Nos moteurs candidats** : V1 et V2-F2 gelés — **REJECTED comme
  exploitations** (BACKTEST-2026-001 : −30,40 et −33,24 USD modèle ;
  LMD-008 : déficit concentré dans l'accumulation × coûts, sortie
  plafonnée au PWA, aucun stop). Leur échec condamne ces
  implémentations, pas le modèle économique supposé du provider, dont
  la rentabilité reste UNVERIFIED (statistiques publiques seulement).
- **État** : **HYPOTHESIS / IDENTIFICATION_IN_PROGRESS** (mécanisme
  comportemental FORTEMENT ÉTAYÉ ; edge net NON VALIDÉ).
- **Dépendances** : partage le risque « excursion adverse durable »
  avec tout modèle d'accumulation futur.

## ME-002 — TEMPORARY_DISLOCATION (déséquilibre temporaire)

- **État** : DISCOVERED (famille définie par la constitution, §2).
  Aucune observation de trader ne l'a encore isolée chez Colorful ;
  signature (écarts inhabituels et résorption) détectable dans le
  corpus 2010-2026. Rendement net après coûts : non mesuré.

## ME-003 — IMPULSE_CONTINUATION (impulsion)

- **État** : DISCOVERED (famille). Chez Colorful, la voie rapide H3 est
  une signature d'entrée compatible mais l'avantage directionnel après
  entrées simulées est réfuté comme mécanisme principal (AESR-002 :
  +0,31/+0,82/+0,14 bp à 60/300/900 s). Non mesuré comme modèle autonome.

## ME-004 — LIQUIDITY_PROVISION (fourniture de liquidité)

- **État** : INSUFFICIENT_DATA. Exigerait Bid/Ask et profondeur réels du
  lieu d'exécution ; les ticks Dukascopy ne prouvent aucune
  rémunération de liquidité capturée. Aucune affirmation faite.
