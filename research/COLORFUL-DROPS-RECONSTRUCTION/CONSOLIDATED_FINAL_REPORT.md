# COLORFUL DROPS — RAPPORT CONSOLIDÉ DE RECONSTRUCTION (RE-ENTRY-001 → mission globale)

## 1-2. Données et paniers observés
Fournisseur HFM 99001292 « Colorful drops » (Copy Cent, XAUUSDc, JPY, levier 1:500, profil public :
49 595 transactions clôturées, 67,4 % positives, gain moyen ¥22,37 < perte moyenne ¥27,82,
drawdown affiché 31,81 %). Échantillon réel constitué : **5 paniers, 12 transactions** (A, B du
2026-11-26 via références fondateur ; C, D, E du 2026-11-27 via page publique archivée, collecteur
`hfm_public_collector.py`). Cotations : ticks Dukascopy (comparatives, jamais HFM), fuseau
serveur UTC+2 fortement étayé. Le fournisseur n'a rien publié depuis le 2026-11-27 11:01
(serveur) ; la page contrôlée ce cycle est inchangée — interruption d'observation signalée.

## 3-8. Moteurs reconstruits (statuts)
- **Entrée initiale** : contexte d'impulsion/reprise (+11-13 bp, reprise +7,6-12,9 bp) 4/5 ;
  horloge M15 exacte 3/5 ; H1 seule et H2 seule **réfutées** ; H3 combinée = hypothèse à tester.
  Aucun Sell observé (12/12 Buy) : le modèle est muet sur la sélection du sens opposé.
- **Amorçage** : 2e entrée à 16-40 s, signe indifférent — FORTEMENT ÉTAYÉ (4 paniers).
- **Renforcement** : 3e entrée sur recul −4,7 à −6,6 bp depuis la 1re — FORTEMENT ÉTAYÉ (3).
- **Dimensionnement** : 0,01/0,01 puis 0,02 (A, B) ou 0,03 (C) — formule NON DÉTERMINABLE.
- **Clôture** : groupée 5/5, au voisinage du prix moyen pondéré (C exactement dessus, net −6 ¥) —
  déclencheur exact NON DÉTERMINABLE ; distance fixe au-dessus de la moyenne RÉFUTÉE.
- **Réinitialisation** : B ouvre 2 s après la clôture de A — FORTEMENT ÉTAYÉE (1 cas mécanique).
- **Protection** : aucun stop, aucun plafond observé ; positions 4+ NON OBSERVÉES.

## 10-13. Spécification et reproduction (moteur livré)
Spécification implémentée dans `ci_tools/colorful_replay.py` (chaque règle étiquetée par statut ;
Buy seulement ; amorçage +30 s ; renforcement à −5,5 bp, lot 0,02 ; clôture au Mid ≥ prix moyen ;
réévaluation immédiate ; coûts CENTRAL au-delà du spread payé par Bid/Ask). Replay exécuté sur
les ticks des fenêtres couvertes. **Fidélité en-échantillon, mesurée sans exclure les cas
difficiles** : entrées reproduites à ±120 s : **3/5** (B à 23 s, C à 0 s, D à 13 s) ; manquées :
A (écart 1 071 s) et E (594 s — le modèle était engagé ailleurs ou sa condition n'a pas feu au
tick exact) ; **décisions supplémentaires : 8 paniers simulés sans équivalent réel** dans les
fenêtres couvertes (3 contre 2 le 26 ; 10 contre 3 le 27). À l'intérieur des paniers ouverts, la
mécanique (amorçage, renforcement, clôture au point mort) se comporte comme spécifié. Conclusion
de reproduction : le moteur reproduit la **gestion** du panier, mais son **portail d'entrée est
trop permissif et encore mal aligné** — une condition d'entrée réelle nous échappe (probablement
un filtre d'unicité d'impulsion ou de contexte que 5 paniers ne permettent pas d'isoler).
Tout ajustement supplémentaire sur ces mêmes cas serait du sur-ajustement : il est refusé.

## 14. Économie et risque (descriptif, pas une validation)
Paniers simulés dans les fenêtres : PnL cumulé −0,028 (26) et −0,058 (27) USD par unité de
contrat après coûts centraux — le modèle actuel, trop actif, perd le spread en route ; cela ne
dit rien de la rentabilité du trader réel, dont les entrées sont plus sélectives. Risque du
mécanisme réel : exposition contre-tendance sans stop observé, sortie qui accepte le point mort
(perte nette possible, cas C), queue inconnue (aucun panier profond/long observé), drawdown
affiché de 31,81 % et gain moyen inférieur à la perte moyenne au profil — signature compatible
avec une martingale contenue par la fréquence des retours au prix moyen, non démontrée viable.

## 15. Règles : confirmées / hypothétiques / indéterminables
Confirmées par les données (au sens observationnel) : clôtures groupées ; amorçage rapide.
Fortement étayées : entrée en contexte haussier ; renforcement au recul dès la 3e ; réinitialisation
immédiate ; fuseau UTC+2. Hypothèses à tester : H3 ; seuil de recul ≈ −5 bp ; sortie au premier
retour au point mort. Réfutées : H1 seule ; H2 seule ; impulsion obligatoire ; cassure obligatoire ;
distance fixe de clôture ; H2/H4 temporelles pour la 3e. Non déterminables : signal exact, sens
Sell, formule des lots, positions 4+, plafond d'exposition, règle de coupe en perte, objectif net.

## 16. Dépendances externes bloquantes
(1) Le fournisseur est en pause depuis le 2026-11-27 : le Niveau 4 (validation indépendante)
exige ses prochains paniers, collectables uniquement par instantanés publics depuis un poste à
navigation ordinaire (CI = 403, non contourné). (2) L'historique complet resterait la voie rapide
vers les paniers profonds/perdants ; il suppose l'accès au compte suiveur, hors périmètre.
(3) La confirmation du fuseau exige un export horodaté du terminal suiveur.

## 17. État des niveaux et checkpoints
Niveau 1 (compréhension) : **partiellement atteint** (gestion du panier comprise, portail
d'entrée non isolé). Niveau 2 (formalisation) : **atteint pour le modèle candidat** (spécification
implémentée et traçable). Niveau 3 (reproduction) : **exécuté, fidélité partielle mesurée**
(3/5 entrées, 8 extras). Niveau 4 (validation indépendante) : **non atteint** — aucun nouveau
panier depuis la formulation. Niveau 5 (économie) : **descriptif seulement**. Chaîne : seq445
(spécification), seq446 (présent rapport) ; artefacts `ci_tools/colorful_replay.py`,
`REPLAY_RESULTS.json`, dossiers RE-ENTRY-001 à 006. Aucune conclusion antérieure n'a été
modifiée sans preuve ; les résultats négatifs (fidélité faible du portail) sont conservés tels quels.
