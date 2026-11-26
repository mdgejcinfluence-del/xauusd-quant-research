# AUDIT DE ROBUSTESSE ET DE SURAPPRENTISSAGE

Multiplicité : 47 règles dans ce seul cycle, des centaines historiquement (registre seq1-420).
Même sans déflation formelle (DSR/PBO), le critère « positif sur les trois périodes disjointes »
n'est satisfait par aucune règle — le surapprentissage n'est donc pas ce qui nous sépare d'un
edge : les effets changent de signe. Sensibilités : coûts +1 bp/côté aggravent toutes les
cellules ; les barrières Mid supposent une exécution au niveau touché (majorant) ; les
événements se chevauchent (grappes) — les moyennes sont descriptives, pas des IC de validation.
La continuation après journée extrême (n=145) est le seul positif cohérent : probabilité non
négligeable qu'il soit un artefact de sélection parmi 47 règles ; il est donc classé fragile et
renvoyé à l'observation future, pas promu. Reproductibilité : script unique
`ci_tools/gold01_experiments.py`, préenregistrement commité avant calcul (seq419), artefacts
d'entrée gelés et référencés par leurs manifestes.
