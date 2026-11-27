# COLORFUL-FILTER-002 — RAPPORT CONSOLIDÉ UNIQUE

Préenregistrement seq449. V1/V2 gelés, intouchés (vérifiés). Page HFM recontrôlée ce
cycle : **inchangée** (49 595 fermés, dernières lignes 2026-11-27 11:01 serveur, profil
identique). Aucun snapshot nouveau, aucun doublon à traiter, aucune perte de collecte
nouvelle détectable — mais une page inchangée n'est pas une preuve d'inactivité.

## A. Validation H3/F2 — EN ATTENTE (aucune observation nouvelle)
H3 et F2 n'ont reçu **ni confirmation ni réfutation nouvelle** : le fournisseur ne
publie plus depuis le 2026-11-27. Les conditions de falsification seq443/447 restent
en vigueur, inchangées. Toute prétention de validation serait fabriquée ; l'état
correct est : en-échantillon 5/5 (V2), hors-échantillon **non testé**.

## B. Sélectivité — les 10 paniers supplémentaires V2
Dissection complète (`CLOSE_LAB_RESULTS.json`, `EXTRAS_FEATURES.json`) : 5 par voie
rapide, 5 par horloge M15 ; features causales au tick (ret5/15/30/60m, reprise,
positions 15/60m, range 5m, minute de bougie) **chevauchent intégralement** celles des
5 entrées réelles. **Aucune condition observable testée ne les élimine sans perdre une
entrée réelle (X1 : résultat négatif).** Deux caveats : (1) plusieurs extras tombent
hors des périodes où l'absence réelle est prouvée (la page ne montre que les 6
dernières transactions) — ce sont des « sans équivalent observé », pas 10 erreurs
prouvées ; (2) les extras d'horloge (ret15m ≈ +5,5 bp, reprise faible) suggèrent que
la branche horloge de H3 est la plus permissive, sans qu'un seuil propre émerge.

## C. Première entrée
Inchangé et borné : portail H3 (frontière M15 en fond haussier OU voie rapide
impulsion/reprise), unicité F2 en-échantillon, Buy seulement observé. Signal exact,
sens Sell : NON DÉTERMINABLES.

## D–E. Renforcements et volumes
Inchangés (seq440) : amorçage 16–40 s (signe indifférent), 3e sur recul −4,7 à
−6,6 bp, délai seul réfuté. D (1 position, 17 s) prouve que la clôture peut précéder
l'amorçage. Aucune séquence 4+ observée. Formule des lots : NON DÉTERMINABLE.

## F. Fermeture — trois hypothèses réfutées ce cycle (avancée négative solide)
Trajectoires tick reconstruites autour des prix moyens pondérés réels
(`colorful_close_lab.py`) :
- **C1 premier retour au-dessus de la moyenne : RÉFUTÉE.** Épisodes au-dessus de la
  moyenne avant la clôture réelle : A 4, B 8, C 2, D 4, E 2. Le trader ne ferme pas
  au premier retour (B attend 88 s après le 1er retour, A ~3,8 min après).
- **C2 objectif fixe en bp au-dessus de la moyenne : RÉFUTÉE.** Mid de clôture −
  moyenne : +6,2 / +7,9 / −0,25 / +2,8 / +3,4 bp — dispersés, C négative.
- **C3 évaluation aux frontières M15 : RÉFUTÉE.** Minutes de clôture dans la bougie :
  5, 2, 10, 0, 1.
- Observation résiduelle (descriptive, n=5) : ret60s au tick de clôture toujours
  positif (+2,6 à +8,9 bp) — les clôtures surviennent pendant une jambe haussière,
  compatible avec une sortie « sur force » ou un objectif monétaire minuscule
  (profits affichés +11/+13/−6/+1/+3 ¥), **non tranchable** avec ces données.
C'est ce mécanisme inconnu — et non le portail — qui explique l'écart de durées
(réelles 17 s à 1 152 s contre ~60 s simulées, plancher artificiel du moteur).

## G. Machine à états — formalisation partielle, transitions démontrées seulement
Démontrées/étayées : Inactif→Entrée (H3+F2) ; Entrée→Amorçage (16–40 s) **ou**
→Fermeture précoce (D, 17 s) ; Amorçage→Renforcement (recul ≈ −5 bp) ; Panier→
Fermeture groupée (déclencheur inconnu) ; Fermeture→Réentrée immédiate (B, +2 s).
Inconnues : mémoire inter-paniers, état « récupération », conditions d'arrêt des
renforcements, plafond d'exposition. La machine est un **squelette testable**, pas
une architecture établie.

## H. Fidélité
En-échantillon : V2 entrées 5/5, positions exactes 2/5, durées fausses, clôtures non
reproduites. Hors-échantillon : **aucune mesure possible** (0 observation nouvelle).
Présenter ces chiffres comme une validation serait trompeur.

## I. Risque et utilisation sur compte propre (descriptif, aucun ordre, aucune connexion)
Mécanisme = Buy contre-tendance par renforcements sans stop observé, sortie acceptant
le point mort net négatif (C). Risques structurants : exposition croissante contre
la tendance (queue inconnue : aucun panier profond observé), drawdown affiché du
fournisseur 31,81 %, gain moyen ¥22,37 < perte moyenne ¥27,82 sur 49 595 transactions,
coûts aller-retour ≈ 4–4,5 bp (à re-mesurer sur XAUUSDc réel, spread flottant, swap
long −73,56 pts, triple mercredi — specs seq429). Capital : non calculable sans la
distribution des paniers profonds, **qui est précisément la donnée manquante** ;
toute utilisation avant validation hors-échantillon et connaissance de la queue
serait une exposition à une martingale non caractérisée. Verdict d'utilisabilité :
**non utilisable en l'état**.

## J. Verdict final
**Nous possédons encore seulement un modèle candidat.** Démontré : mécanique
d'amorçage/renforcement, correction du matching, anatomie des faux paniers V1.
Probable : portail H3 + unicité F2, sortie liée au prix moyen sans déclencheur
premier-retour. Inconnu : déclencheur exact d'entrée et de clôture, lots, queue de
risque. Impossible à vérifier sans nouvelles publications du fournisseur ou un
historique légitime complet. La prochaine preuve décisive est externe, pas
analytique : les prochains paniers réels, classés d'abord selon seq443/447/449.

Artefacts : `ci_tools/colorful_close_lab.py`, `CLOSE_LAB_RESULTS.json`,
`EXTRAS_FEATURES.json`, présent rapport. Reproduction :
`/tmp/metaalpha-venv/bin/python ci_tools/colorful_close_lab.py`.
