# CTRS-007 — RAPPORT EXÉCUTIF (clôture de campagne)

**Verdict : B — RECONSTRUCTION PARTIELLE AVEC FRONTIÈRE D'IDENTIFIABILITÉ**
(justification complète : `FINAL_SCIENTIFIC_VERDICT.md`).

Le système de Colorful drops est reconstruit comme une **famille bornée** :
contexte haussier M15 (H3, candidate) → entrée Buy → accumulation
d'inventaire sur excursion adverse (−4,7 à −6,6 bp, intervalles observés)
→ gestion par prix moyen pondéré → sortie au voisinage du PWA pendant une
jambe favorable, par un déclencheur non ponctuel que cinq clôtures ne
permettent pas d'identifier (cadence à phase libre, condition hybride et
variable hors-Mid restent observationnellement équivalentes).

Démontré : la mécanique du PWA, les trajectoires de récupération, la
réfutation des déclencheurs simples (premiers passages 19–246 s trop
tôt ; persistance unique et cadence ancrée éliminées sur grilles
complètes), et la non-rentabilité de nos moteurs gelés V1/V2 sur 2026.
Non démontré : la formule de sizing (C réfute le doublement universel),
le déclencheur exact de clôture, tout stop, tout comportement Sell, et
la rentabilité du provider (statistiques publiques non vérifiées :
+6,01 ¥/transaction affichés, jamais présentés comme preuve).

Aucun paramètre arbitraire n'a été ajouté pour « compléter » le système.
Les modules non identifiés sont marqués comme tels dans l'architecture.
`profitable_edge=False` pour tous nos moteurs.
