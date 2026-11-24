# SHADOW — collecte prospective (prêt, non activé)

- `shadow_collector.py` : squelette de collecte Bid/Ask horodatée (source à brancher par le
  fondateur : export plateforme ou capture démo autorisée). Refuse toute date <= borne du
  holdout consommé (2026-09-30T23:59:58.864Z).
- `shadow_scoring.py` : applique hors ligne la règle préenregistrée (deadline 120 min) et la
  référence 8 h aux événements collectés, comptabilité 19-B S0/S1/S2, bootstrap par grappes.
Aucun ordre n'est émis par ces scripts ; ils ne lisent que des fichiers de cotations fournis.
Activation bloquée : aucune source de flux gratuit vérifiable n'est connectée (voir
SHADOW_OBSERVATION_DESIGN.md).
