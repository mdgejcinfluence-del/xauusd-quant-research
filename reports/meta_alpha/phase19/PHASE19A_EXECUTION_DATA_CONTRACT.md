# PHASE 19-A — CONTRAT DE DONNÉES D'EXÉCUTION (si et seulement si elles existent un jour)

La présente phase **n'autorise ni envoi d'ordre, ni engagement de capital, ni compte de trading**. Ce contrat définit uniquement ce qu'une donnée d'exécution devrait contenir pour être recevable scientifiquement, si une décision distincte créait un jour une capture d'exécution (par exemple simulation ou démonstration sans capital réel).

Champs minimaux par intention d'ordre : identifiant, heure d'envoi UTC, accusé de réception, heure et prix d'exécution réels, quantité exécutée, exécutions partielles, rejets et annulations, commission réelle, swap réel le cas échéant (schéma complet : `PHASE19A_CAPTURE_SCHEMA.json` section C).

Règles permanentes : un franchissement de cotation n'est jamais une exécution (`QUOTE_CROSSING_PROXY_ONLY` reste la qualification de tout proxy) ; les prix Bid/Ask historiques ne prouvent ni remplissage, ni rang de file, ni taille ; aucune commission ou swap ne peut être inventé — réel documenté ou explicitement absent. En l'état actuel, **aucune donnée d'exécution n'existe** dans le programme et aucune n'est requise pour la suite de la recherche sur cotations.
