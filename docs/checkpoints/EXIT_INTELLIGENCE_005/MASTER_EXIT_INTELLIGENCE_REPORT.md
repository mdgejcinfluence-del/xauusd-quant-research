# EIDR-005 — MASTER EXIT INTELLIGENCE REPORT

Fait nouveau central : **toutes les règles causales de premier passage testées
se déclenchent trop tôt** — de 19 à 246 secondes avant les clôtures réelles
(premier retour au PWA, momentum, décélération, retracement confirmé, seuil de
PnL à +3 bp qui échoue en outre chez C). Le trader ne liquide donc pas au premier
instant où l'état devient favorable : sa sortie comporte une composante de
**persistance ou de confirmation** dont les bornes sont mesurées mais dont la
nature exacte (durée de persistance, cadence d'évaluation, condition
supplémentaire) est observationnellement équivalente sur cinq clôtures. La
proximité des sommets locaux est la conséquence géométrique de ce comportement,
pas son déclencheur. Livrables : registre des hypothèses de sortie (7 entrées,
premiers passages réfutés), moteur de sortie causal spécifié en famille
paramétrique bornée — aucun point de paramètre inventé — architecture dynamique
complète et scorecards. La reconstruction du mécanisme central tient ; ses
paramètres ponctuels exigent des clôtures réelles indépendantes.
