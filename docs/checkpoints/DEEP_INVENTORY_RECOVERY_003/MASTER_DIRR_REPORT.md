# DIRR-003 — MASTER REPORT (Deep Inventory & Recovery Reconstruction)

Les cinq paniers réels ont été reconstruits tick par tick (`TRAJECTORY_A..E.csv`) :
prix moyen pondéré dynamique, PnL latent pondéré, temps sous le PWA. Résultat
structurant : les paniers de récupération passent **65 à 88 % de leur vie sous leur
prix moyen**, encaissent jusqu'à −15,3 bp latents, puis clôturent entre −0,25 et
+7,9 bp du PWA. Les contrefactuels à instant de sortie identique montrent le
mécanisme à l'œuvre : le renforcement abaisse le PWA et convertit une excursion
de −3,3 bp en sortie à −0,25 bp (cas C) — **un échange d'exposition accrue contre
une récupération rendue possible**, dont l'effet causal global reste non
identifié (censure documentée). Le régime immédiat (D, E) se distingue par la
trajectoire post-entrée, non par une condition d'entrée séparable ; les moteurs
actuels en produisent 82 % contre 40 % observés chez le réel — ils sur-produisent
le scalp et sous-produisent la patience.

Ce qui est clos ce cycle : le rôle exact du PWA (référence de mesure, pas
déclencheur), la dynamique complète des deux régimes, la famille réduite des
mécanismes de sortie encore compatibles. Ce qui reste non identifiable, avec la
raison précise pour chacun : le sizing, le déclencheur de sortie, le plafond de
risque — sous-identification sur 12 transactions. Statuts complets dans
`FINAL_SCIENTIFIC_CONCLUSIONS.md` ; architecture DIRR et machine à états jointes ;
aucun seuil nouveau n'a été ajusté sur les paniers réels.
