# PHASE 6 — F14 ÉCART D'ÉQUILIBRE EXOGÈNE : SYNTHÈSE

**Verdict : NON TESTABLE au gate R3 — mission close sans exécuter les 5 variantes. 0 essai consommé (budget EXOGÈNE toujours 0/60 ; tick 148/150 et panel 28/60 inchangés).**

## Étape A (ingénierie hors budget, ordre §3.0) — `F14_ETAPE_A.json`
Dataset : 3 097 jours alignés (2010-01-04→2019-12-16), décision 22:00 UTC, tout driver pris à `available_at_utc ≤ décision` (pack IS certifié seq 105), z-scores causaux 28 j.

### Deux vitesses (mesure livrée)
Par driver : chocs |z|>2, projections locales h∈{0,1,2,3,5,10,15,21}, ajustement bi-exponentiel. τ_fast 0,9–3,0 j, τ_slow 3–30 j (souvent à la borne 30 : pas de composante lente propre identifiable), réponses cumulées à 21 j de quelques dizaines de bp, bruitées. Détail par driver dans `F14_ETAPE_A.json`.

### Trois portes par driver — **0/5**
| Driver | β (t NW) | p BY | Bus (pic) | Placebos | Verdict |
|---|---|---|---|---|---|
| DFII10 | −0,018 (−2,92) | 0,040 | **lag 0** ✗ | silencieux | RETIRÉ (ne mène pas ; |t|<3) |
| dollar | −0,007 (−1,20) | 1,0 | lag 1, placebos ≈ pic ✗ | non silencieux | RETIRÉ |
| COT net % | −0,006 (−0,96) | 1,0 | lag 5 ✗ | — | RETIRÉ |
| GVZ | −0,003 (−0,45) | 1,0 | lag 0 ✗ | — | RETIRÉ |
| volume GC | −0,002 (−0,60) | 1,0 | lag 4 ✗ | — | RETIRÉ |

Le cœur v1 (DFII10 + dollar) échoue : DFII10 a le bon signe partout (4/4 sous-périodes, monotonie −0,96) mais sa réponse aux chocs est **contemporaine** (pic à lag 0) — le taux réel est intégré le jour même, il ne reste rien à capturer en lenteur ; et |t| = 2,92 < 3. Le modèle gelé ne peut pas être formé : un driver qui échoue une porte est retiré, pas gardé « au cas où ».

### Gate R3 — NON TESTABLE
3 074 jours tradeables, durée moyenne de trade 10 j ⇒ ~307 paris indépendants ; σ(10 j) = 2,71 % ⇒ **MDE(80 %) = 43,2 bp** contre un effet minimal économique requis de **16,7 bp** (ECR ≥ 2 en C1 déclaré, haircut 0,6). MDE > effet ⇒ NON TESTABLE, consigné, variantes non exécutées. (Coûts CONDITIONNELS : BROKER_CONFIG toujours UNKNOWN — matrice déclarée au préenregistrement, aucun ancrage inventé.)

## Châssis §4 (ingénierie livrée, 0 essai)
`ci_tools/chassis_hardening.py` testé : CUSUM résidus (k=0,5σ, h=4σ) + registre de régime, Kelly à mixture de crise (π 5 %/an, horizon du trade ; Kelly simple 0,250 → mixture 0,245 sur le cas test), décision sur borne basse généralisée, médiane pondérée par crédibilité winsorisée. `meta_chassis.py` gelé intact. Un incident de test consigné : le tirage seed 7 déclenchait une fausse alerte CUSUM — paramètres inchangés, test rendu déterministe.

## Ce que cela signifie
La traduction Dantokpa tenait ou tombait sur une prédiction précise : il existe une composante **lente** de convergence vers un équilibre exogène. Sur l'or IS 2010–2020, avec des drivers certifiés point-in-time, les portes répondent non : l'information des drivers est dans le prix le jour même (lag 0), la « vague de fond » mesurée est sous le seuil détectable (43 bp de MDE contre 17 bp requis). C'est exactement le type de réponse que le gate R3 existe pour donner **avant** de dépenser un essai.

## État du programme EXOGÈNE
F14 fermée. Budget 0/60 consommé. F15 (fenêtres macro point-in-time) et F16 (extrêmes COT) restent possibles — préenregistrements séparés, ordre explicite requis. Si les trois ferment, le programme EXOGÈNE se refermera proprement (§6 de l'ordre). Aucune variante, aucun re-grillage, aucun seuil déplacé.
