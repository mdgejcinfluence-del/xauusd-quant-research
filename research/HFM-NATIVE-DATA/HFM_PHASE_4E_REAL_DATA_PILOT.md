# PHASE 4E — PILOTE RÉEL (données réelles uniquement, journaux CI à l'appui)

Exécuté en CI (runs `diag`, journaux commités `external_reference/PILOT_LOG.txt` et
`PILOT_EXTERNAL.json`, 4 tentatives) :
1. **Document HFM Tick Chart Trader** : HTTP 200 — le guide officiel est public ; il établit
   lui-même l'absence d'historique (voir 4A). Aucune donnée de marché HFM obtenue.
2. **HistData XAUUSD ticks 2010-01** (formulaire public, sans compte) : le POST `get.php`
   répond HTTP 200 avec **0 octet** depuis les IP du runner CI, sur trois exécutions espacées
   (dont un retry après 25 s). Classification : voie **bloquée depuis l'infrastructure CI**
   (protection anti-robot probable), non épuisée depuis un poste résidentiel — à réessayer hors
   CI si le fondateur le souhaite ; en attendant, aucune donnée HistData n'est déclarée obtenue.
3. **Stooq XAUUSD quotidien** : page de défi JavaScript anti-robot depuis le runner — rejeté
   comme source automatisable dans notre infrastructure ; le fichier HTML reçu a été supprimé,
   jamais conservé comme donnée.
Aucune donnée synthétique n'a servi ce pilote. Le seul corpus tick externe réel et vérifié du
projet reste Dukascopy (348 partitions certifiées + collecte prospective), déjà classé
`EXTERNAL_REFERENCE` et volontairement non re-téléchargé.
