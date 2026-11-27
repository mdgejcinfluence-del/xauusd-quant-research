# RE-ENTRY-005 — SIGNAL DE PREMIÈRE ENTRÉE : CE QUE LES 5 CAS DISENT ET NE DISENT PAS

## A. Inventaire des premières entrées
5 premières entrées exploitables et reconstruites (A–E ; Dukascopy comparatif, serveur supposé
UTC+2 fortement étayé) : A 13:31:20 et B 13:50:34 (2026-11-26) ; C 10:30:00, D 10:45:00,
E 11:00:00 (2026-11-27). Aucune nouvelle transaction n'a été obtenue ce cycle (page publique
inaccessible lors du contrôle — échec journalisé, pas de contournement).

## B. Conditions préalables (fenêtres 15 s → 15 min, causalité stricte)
| Panier | ret 60 s | ret 5 min | ret 15 min | Position range 15 m | Cassure max 15 m | Reprise depuis creux 5 m |
|---|---|---|---|---|---|---|
| A | +5,4 | **+11,3** | +8,8 | 82 % | non | +12,9 bp |
| B | +4,0 | **+11,9** | +8,3 | 82 % | oui | +11,8 bp |
| C | +1,6 | +2,7 | **+13,2** | 51 % | non | +7,6 bp |
| D | +1,4 | **+12,0** | +1,1 | 93 % | non | +12,2 bp |
| E | −0,9 | **−3,1** | +6,8 | 45 % | non | +1,0 bp |
Spread médian pré-entrée homogène (1,21–1,43 bp) : le spread ne discrimine rien ici.

## C. Identification du signal — deux contextes, pas un déclencheur unique
- **Impulsion de continuation (A, B, D ; C en horizon 15 min)** : +11 à +12 bp sur 5 min (ou
  +13 bp/15 min), position haute dans le range (82–93 % chez A/B/D), reprise de +7,6 à
  +12,9 bp depuis le creux des 5 dernières minutes. C'est le contexte dominant (4/5).
- **Contre-exemple interne (E)** : entrée à 11:00:00 précises après **−3,1 bp/5 min et −8 bp/10 min**,
  à 45 % du range — aucune impulsion courte. E, C et D ouvrent exactement sur des **frontières
  M15 (:00)**, alors que A (13:31:20) et B (13:50:34, 2 s après la clôture de A) n'y sont pas.
- Hypothèses concurrentes conservées : (i) impulsion + reprise après creux (déclencheur prix) ;
  (ii) évaluation à la clôture de bougie M15 avec condition de fond haussier 15 min (E : +6,8 bp)
  mais tolérance au repli court ; (iii) redémarrage événementiel après clôture (B). Aucune ne
  rend compte seule des 5 cas ; le **signal exact reste NON DÉTERMINABLE** — le déclarer
  découvert serait une fabrication.

## D. Non-entrées (uniquement dans les fenêtres couvertes par les transactions connues)
Balayage des fenêtres 13:31–14:02 (26) et 10:30–11:01 (27) : chaque épisode « impulsion forte »
(≥ +10 bp/5 min, position ≥ 80 %) coïncide avec une entrée observée (2/2). Aucun contre-exemple
de non-entrée dans ces fenêtres courtes ; mais E prouve que l'impulsion n'est pas **nécessaire**,
et la couverture (31 minutes par jour) interdit toute conclusion de suffisance générale.

## E-F. Séquence initiale et reproduction
La séquence 1→2→3 reste celle de RE-ENTRY-004 (amorçage ≤ 40 s ; 3e sur recul −4,7 à −6,6 bp).
Un modèle de reproduction fidèle devra combiner : contexte d'impulsion/reprise **ou** frontière
M15 en fond haussier, amorçage immédiat, renforcement au recul, sortie au voisinage du point
mort. Sa fidélité ne pourra être mesurée que sur les **prochains paniers collectés** — aucun
modèle n'est sélectionné ici, aucun ne l'est sur un critère financier.

## G. Classement
| Conclusion | Statut | Paniers |
|---|---|---|
| Contexte d'impulsion/reprise avant la 1re entrée | FORTEMENT ÉTAYÉE | 4/5 (A, B, C, D) |
| Impulsion 5 min comme condition nécessaire | RÉFUTÉE | E (contre-exemple) |
| Cassure du plus haut 15 min comme déclencheur | RÉFUTÉE (1/5 seulement) | 5 |
| Frontière M15 comme horloge d'entrée | HYPOTHÈSE À TESTER | 3/5 aux frontières |
| Fond haussier 15 min (+6,8 à +13,2 bp) commun | FORTEMENT ÉTAYÉE | 5/5 |
| Signal exact de première entrée | NON DÉTERMINABLE | 5 |
| Spread comme filtre discriminant | NON DÉTERMINABLE (homogène) | 5 |

## Prochaine étape
Chaque nouveau panier collecté tranchera entre les hypothèses (i) et (ii) : une entrée hors
frontière M15 après impulsion plaiderait pour (i) ; une entrée sur frontière après repli, pour
(ii). La collecte continue ; le signal ne sera déclaré que lorsqu'un mécanisme unique rendra
compte des cas, y compris des contre-exemples.
