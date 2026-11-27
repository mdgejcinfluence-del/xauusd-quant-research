# CTRS-007 — INVENTAIRE ET RÉCUPÉRATION (final)

Modèle d'état causal (par tick, passé seulement) : PWA dynamique, volume
cumulé, PnL latent bp, distance au PWA, excursions min/max, temps sous /
au-dessus du PWA, ΔPnL 30/300 s. Implémentation de référence : trajectoires
DIRR-003 + moteur EMI-006.

Faits (trajectoires A–E) : paniers de récupération 65–88 % de leur vie
sous le PWA ; PnL latent min −4,99 (B), −8,78 (A), −15,30 bp (C) ;
clôtures à −0,25 / +2,83 / +3,40 / +6,18 / +7,91 bp du PWA ; régime
immédiat D/E : creux seulement −0,63 / −1,59 bp.

Interprétation défendable : le PWA est la **référence de gestion**
(le système attend son voisinage sur une jambe favorable), sans être le
déclencheur (premier retour réfuté, EIDR-005). La variable de pilotage
exacte (PWA vs PnL monétaire vs distance) est NOT_IDENTIFIED — ces
variables sont colinéaires sur des paniers à volume quasi constant.
Conséquence mécanique ≠ condition décisionnelle : maintenu séparé.
