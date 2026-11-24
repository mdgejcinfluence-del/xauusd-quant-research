# MA-EDGE-01 — 01 · AUDIT STRATÉGIQUE DES TRAVAUX ANTÉRIEURS

Matrice de synthèse (démontré / réfuté / ouvert), reconstruite depuis les verdicts gelés au
registre des essais (seq149-403), non depuis les intentions des phases :

| Domaine | Démontré | Réfuté ou non démontré | Ouvert |
|---|---|---|---|
| Direction | Signaux prédictifs H1 (M1, 12-B/12-C.2) et M15 (24-C) sur labels de reprise | Direction moyenne des amplitudes (H4, D1, FOMC : bidirectionnel, 20-C/21-D/23-C) | Direction conditionnée par une information externe causale (GVZ/COT) |
| Entrée | Entrées tick causales reproductibles (premier tick strict, 19-B/23-C/24-D) | Entrée sur seuil de score comme filtre économique (24-F : non monotone) | Deadline de non-réalisation comme architecture de sortie (jamais testée) |
| Sortie | Sortie au premier passage mesurée (24-E) : ne bat pas la sortie fixe | Stop/TP structurels des familles 22-A/22-B (archivées) ; sortie 8 h du M15 négative | Sorties fondées sur le temps de réalisation du label, préenregistrées |
| Amplitude | Mémoire d'amplitude H4/D1, expansion FOMC (+81 bp à 60 min) | Amplitude comme source de direction ou de profit (toutes phases) | Amplitude implicite (GVZ) comme contexte de qualité des événements |
| Régimes | Régimes Q90 reproductibles et causaux (24-A) | Réentraînement conditionnel H4/D1 (24-C), permissions économiques (24-D) | Régimes définis par l'information externe plutôt que par le prix passé |
| Microstructure | Texture de cotations extractible (18-B) ; coûts d'exécution auditables (19-B) | Variables de cotations comme edge économique (18-C) | Dynamique du spread (vitesse), jamais testée |
| Macro | Fenêtres FOMC = régime d'amplitude ; timestamps officiels causaux | Contexte taux J-1 (23-B nul) ; surprise (bloquée, licence) | COT, GVZ (25-A) |
| Exécution | Spread intégré une fois ; NON_EXECUTION/EXIT_CENSORED documentés | Exécution comme explication des échecs : les pertes survivent en S0 | Slippage réel broker (inconnu, aucune spécification vérifiée) |
| Modélisation | Logistiques causales prédictives sur labels de trajectoire | Conversion label → payoff (13, 24-D/24-E/24-F) | Modèles dont la cible EST le payoff net (jamais entraînés) |
| Économie du trade | Aucune espérance nette positive démontrée sur IS en 25 phases | Toutes les familles économiques testées (10, 13, 20-B, 22, 24-D) | Payoff-first : deadline de non-réalisation, contextes externes |

Connaissances solides : la mécanique d'audit (causalité, grappes, coûts) et deux signaux
prédictifs de labels. Résultats descriptifs : toutes les amplitudes. Économiquement négatif :
chaque conversion en trades testée. Hypothèse jamais testée : une cible = payoff net.
Contradiction apparente résolue en 24-E : prédire la reprise (label) n'implique pas gagner en
détenant, car le label est un événement de trajectoire, pas un rendement. Erreur méthodologique
structurelle du programme : **vingt-cinq phases ont optimisé la prédiction d'étiquettes de
trajectoire ; aucune n'a pris le payoff net comme cible d'apprentissage**.
