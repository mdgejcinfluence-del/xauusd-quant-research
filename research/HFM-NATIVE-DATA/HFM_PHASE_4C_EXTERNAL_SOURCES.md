# PHASE 4C — CORPUS EXTERNE SANS COMPTE (`xauusd_external_reference`, jamais « HFM »)

Comparatif des sources accessibles sans compte de trading :
- **Dukascopy (déjà détenu)** : ticks Bid/Ask ms UTC depuis 2003, corpus certifié 348 partitions
  + collecte prospective. Valeur : référence principale existante. Ne pas re-télécharger.
- **HistData.com (retenue pour pilote)** : ticks XAUUSD mensuels depuis 2009 (fichiers
  `DAT_ASCII_XAUUSD_T_AAAAMM`), téléchargement public sans compte (formulaire), fuseau EST
  documenté par le fournisseur, Bid seul selon son format tick historique — **à vérifier sur le
  fichier pilote** (en-tête inspectée avant toute classification). Valeur incrémentale réelle :
  flux **indépendant** de Dukascopy → comparaisons de cotations, spreads, trous, et profondeur
  2009-2010 antérieure à notre fenêtre IS principale. Licence : usage personnel/recherche selon
  les termes du site ; **pas de republication Kaggle publique** sans vérification — stockage
  privé et métadonnées de provenance obligatoires.
- **TrueFX** : ticks top-of-book, inscription gratuite exigée (compte de données, pas de trading),
  périmètre centré devises majeures ; XAUUSD non confirmé → non retenu à ce stade.
- **Darwinex** : FTP sur compte réel vérifié → exclu par la contrainte sans compte.
- **Dérivés publics tiers (GitHub/Kaggle)** : reproductions Dukascopy (même provenance, aucune
  indépendance) → écartés comme doublons déguisés.
Architecture retenue : Dukascopy = référence ; HistData = second flux indépendant, catégorie
`EXTERNAL_REFERENCE`, dossier séparé, champ source toujours explicite.
