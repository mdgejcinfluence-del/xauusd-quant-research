# PHASE 6B — SYNTHÈSE ET FERMETURE DU PROGRAMME EXOGÈNE

## Bloc 1 — Config ancrée (seq 108)
`OWNER_CONFIG_V2.json` : CHALLENGE_CONFIG 2-Step Pro documentée ; BROKER_CONFIG prudent haut (contrat 100 oz, spread 1,25 bp, commission $5/côté retenue, slippage 0,6 bp placeholder) ; **C1_BG aller-retour = 4,7 bp** (la formule de l'ordre ; son « ~4,3 » était un arrondi bas — valeur haute retenue, écart consigné). Swap toujours UNKNOWN. **En attente propriétaire** : relevé démo gratuit d'une semaine (spread 14h/22h UTC, commission aller-retour, swap) → V3 hachée, avant tout frais. Le simulateur de challenge peut désormais tourner en mode ancré documenté (toujours CONDITIONNEL tant que le relevé démo n'a pas remplacé les estimations tierces).

## Bloc 3 — F16 COT continu : NON TESTABLE (seq 111)
Gate R3 avant toute performance : 524 semaines, 262 paris, σ(2 sem) = 332,9 bp → **MDE 57,6 bp** contre 9,4/6,7 bp d'effet minimal aux deux ancres. N=2 non exécutés, 0 essai consommé.

## Bloc 2 — F15 fenêtres macro × tick : ÉCHEC 0/6 (N=6 consommés, budget EXOGÈNE 6/60)
Gate R3 TESTABLE (MDE 4,4–6,0 bp < effets minimaux). Extraction tick complète (375 événements gelés, premier croisement des deux corpus).

**Incident d'alignement v1 (seq 112, consigné avant verdict)** : le premier mouvement (T+60s→T+5min) définissait la direction alors que l'entrée v1 était à T+60s — le signal connaissait sa propre fenêtre. Résultats v1 rejetés et purgés, jamais consignés. v2 : entrée au premier tick ≥ T+5min, premier mouvement connu avant l'entrée.

Verdicts v2 (H=60 min gelé, nets aux deux ancres) :

| Variante | n | Net hist (bp) | Net BG (bp) | IC95 hist | Verdict |
|---|---|---|---|---|---|
| FOMC dérive | 81 | −0,4 | −1,2 | [−11,7 ; +10,8] | ÉCHEC |
| FOMC retournement | 81 | −7,4 | −8,2 | [−18,6 ; +4,0] | ÉCHEC |
| NFP dérive | 118 | −6,7 | −7,8 | [−16,3 ; +2,8] | ÉCHEC |
| NFP retournement | 118 | −0,5 | −1,6 | [−10,1 ; +9,0] | ÉCHEC |
| CPI dérive | 127 | −1,3 | −2,7 | [−5,5 ; +2,7] | ÉCHEC |
| CPI retournement | 127 | −5,3 | −6,7 | [−9,5 ; −1,2] | ÉCHEC |

Placebos calendaires ±30 j : tous silencieux (IC contenant 0) — le protocole est sain, il n'y a simplement rien. Après la publication et la première minute écartée, le premier mouvement ne continue pas et ne se retourne pas de façon capturable : les deux directions paient le spread et meurent autour de zéro — la vérité E4 de la Phase 1, retrouvée à l'échelle de l'événement macro. L2 sans objet (0/6 en L1).

## Fermeture (règle d'arrêt Phase 6 §6, confirmée par l'ordre 6B)
F14 NON TESTABLE, F15 ÉCHEC, F16 NON TESTABLE → **le programme EXOGÈNE est fermé définitivement pour ces données** : consigné, chaîné, sans re-grillage. Budget final EXOGÈNE : **6/60 consommés** (les 54 restants ne seront jamais dépensés — ils n'existent plus comme autorisation).

## Ce qui demeure — le capital permanent
F3 (prévision de volatilité, gelée L2) · F7 (alerte de spread, gelée L2) · le châssis durci (kill-switch, gouverneur, CUSUM, Kelly-crise, décision sur borne basse) · le simulateur de challenge, désormais ancré sur des coûts documentés (4,7 bp) · la voie B et son gate démo inchangé · trois packs exogènes scellés et certifiés · 114 entrées d'audit qui ne mentent pas.

En six phases, sur trois corpus (tick, panel 43 actifs, exogène point-in-time), chaque famille directionnelle a été testée avec ses gates calculés avant ses performances — et le marché a répondu non à chaque fois, proprement. La prochaine décision appartient au propriétaire, en connaissance de cause : la phase démo de la voie B (gratuite), le relevé de coûts sur démo (gratuit), ou l'arrêt là. Aucun frais ne se justifie sur la base d'un edge directionnel : il n'y en a pas dans ces données, et c'est désormais prouvé trois fois.
