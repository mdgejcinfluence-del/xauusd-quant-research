"""Implémentations de phases.

AUCUNE phase future n'est codée ici avant autorisation explicite du
propriétaire (kit V1.1 §2.1). Ce paquet est volontairement vide.

Ordre d'ajout, strictement séquentiel :
    p2_analytical.py  -> après approbation PHASE_2_ANALYTICAL
    p3_mining.py      -> seulement après PHASE_2_COMPLETE + revue
    ...
Chaque module doit exposer :  unit_fn(uid, storage) -> (rows, output_rel, output_sha)
et ne connaît ni leases, ni checkpoints, ni retries (rôle de l'orchestrateur).
"""
