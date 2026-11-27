# STRATEGY-DISCOVERY-001 — RAPPORT FINAL

**A. Entrées.** V1 entre trop souvent parce que sa voie rapide se déclenche sur
des impulsions fréquentes et se réarme après chaque clôture au point mort ; aucune
feature causale testée ne sépare les entrées réelles des excédentaires. Le filtre
réel du trader reste inconnu ; les non-entrées sont `ABSENCE_OF_TRADE_NOT_PROVEN`.
**B. Renforcements.** L'association pertes↔3 positions est réelle mais la causalité
est `CAUSAL_EFFECT_NOT_IDENTIFIED` : le contrefactuel de novembre est censuré pour
126/140 paniers et favorable au renforcement sur les 14 évaluables.
**C. Gestion.** Squelette d'états partiellement soutenu ; clôture : 3 hypothèses
réfutées, déclencheur inconnu ; tailles : formule fixe réfutée, reste inconnu.
**D. Risque.** Queue de durée (~13,6 jours), aucun stop, exposition moteur bornée
par construction (0,04 lot), risque réel du fournisseur non calculable.
**E. Modèle.** V2 formalisée en 9 composants étiquetés (voir spécification) ;
sur novembre complet, V2 est économiquement **inférieure** à V1 (−0,930 contre
−0,432, PF 0,663 contre 0,906) tout en étant comportementalement plus fidèle sur
les fenêtres réelles (5/5). Aucun des deux moteurs n'a d'avantage économique
démontré ; la sensibilité aux coûts reste défavorable dès S0.
**F. Fidélité.** Reproduit : contexte d'entrée, amorçage, renforcement au recul
(en-échantillon). Non reproduit : sélectivité, clôtures, durées, volumes.
Échantillon indépendant disponible : **zéro** nouveau panier (page HFM toujours
inchangée ce cycle) ; validation : plan prospectif joint, V2 gelée.
**G. GitHub.** Branche de session `arena/afe12737-xauusd-quant-research` (branche
dédiée demandée non créée : règle de session ; `main` intacte), tests et
empreintes dans `RESEARCH_TEST_REPORT.md` et le manifeste du dossier.
Verdict inchangé et désormais étayé des deux côtés (économie et comportement) :
**modèle candidat partiellement fidèle, non validé ; stratégie réelle non retrouvée.**
