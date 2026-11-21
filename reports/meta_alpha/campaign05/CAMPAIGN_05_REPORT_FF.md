# CAMPAGNE 5 — RAPPORT FAMILLE F-F (extrêmes datés)

**Statut : EXÉCUTION DESCRIPTIVE TERMINÉE** selon le protocole V2 +
addenda V2.1 et V2.2 (gel chaîné seq221 avant extraction ; en cas de
tension, V2.2 prévaut). Règles appliquées : disponibilité = clôture de
la barre M1 ; « avant B » = disponibilité strictement < B ; toute minute
manquante avant une atteinte ⇒ ATTEINTE OBSERVEE (censurée des
comparaisons, publiée séparément, jamais présentée comme première
réelle) ; ATTEINTE REELLE IDENTIFIABLE seulement en continuité minute à
minute complète depuis le début de période ; franchissements stricts
seuls (les 7 touches publiées à part, hors comparaisons) ; atteintes
successives opposées retenues et marquées ; simultanées même barre :
0 observée (publié).

Populations : 2 375 premières atteintes journalières (HAUT 1 221 /
BAS 1 154) dont **2 004 REELLES IDENTIFIABLES** (HAUT 1 022 / BAS 982)
et **371 OBSERVEES** (HAUT 199 / BAS 172, censurées) ; 504 lignes
d'atteintes hebdomadaires sur 457 semaines touchées (520 semaines au
total) dont **187 REELLES IDENTIFIABLES** et **317 OBSERVEES** ;
ordre indéterminé : 0.

Méthode : bootstrap par grappes-journées (grappes-semaines pour C5-09),
2 000 réplicats, graine 20261113 ; BY séparé par famille (F-F : 5 p) ;
matérialité 5 points / ratio 1,15 symétrique ; éligibilité ≥200
épisodes et ≥100 grappes par bras.

## Résultats

| ID | Comparaison | Effet | IC 95 % | p brute | q BY (F-F) | n A/B | Lecture |
|---|---|---|---|---|---|---|---|
| C5-06 | P(atteinte réelle disponible avant 08:00) HAUT vs BAS (59,1 % vs 51,0 %) | +8,08 pts | [+3,80 ; +12,59] | 0,0005 | 0,0029 | 1 022 / 982 | **CANDIDATE_J1** (ANO-C5-002) |
| C5-07 | Extension +60 min après 1re atteinte réelle, HAUT vs BAS (15,32 vs 16,73 bp) | ratio 0,916 | [0,807 ; 1,050] | 0,234 | 0,891 | 1 020 / 975 | NÉGATIF |
| C5-08 | Retracement +60 min, atteintes <13:00 vs ≥13:00 (7,92 vs 12,88 bp) | ratio 0,615 | [0,538 ; 0,732] | 0,0005 | 0,0029 | 1 550 / 454 | **CANDIDATE_J1** (ANO-C5-003) |
| C5-09 | P(1re atteinte hebdo réelle avant mercredi 00:00) HAUT vs BAS (100 % vs 100 %) | 0,00 pt | [0,00 ; 0,00] | 1,000 | 1,000 | 106 / 81 | **NON ÉLIGIBLE** (effectifs) |
| C5-10 | P(journée CONTENUE ETABLIE) 2010-13 vs 2017-20 (0/863 vs 0/632) | 0,00 pt | [0,00 ; 0,00] | 1,000 | 1,000 | 863 / 632 | NÉGATIF (dégénéré, voir note) |

## Détails de publication exigés par le gel

- **C5-06** : frontière V2.2 stricte — disponibilité <08:00, soit barre
  débutant ≤07:58. L'asymétrie descriptive (les franchissements du haut
  de la veille surviennent plus tôt dans la journée que ceux du bas)
  est une candidate J1 sans promotion automatique. Aucune lecture
  prédictive autorisée.
- **C5-07** : censures +60 min : HAUT 2, BAS 7 (publiées). Pas de
  différence d'extension selon le côté au seuil gelé.
- **C5-08** : frontière V2.2 <13:00 / ≥13:00 sur la disponibilité.
  Ventilation par côté publiée (médianes de retracement +60 min, bp) :
  avant 13:00 HAUT 7,14 (n=813) / BAS 9,17 (n=737) ; dès 13:00 HAUT
  11,94 (n=209) / BAS 13,75 (n=245). Le sens est cohérent dans les deux
  côtés. Candidate J1 avec **avertissement de composition** : l'heure de
  formation est confondue avec la session et le régime d'activité de la
  journée ; l'association est descriptive et contemporaine, aucun
  mécanisme n'est démontré.
- **C5-09** : seules 187 atteintes hebdomadaires sont REELLES
  IDENTIFIABLES (continuité complète depuis lundi 00:00 UTC, règle
  V2.2) ; toutes sont disponibles avant mercredi 00:00 dans les deux
  bras (100 % / 100 %, différence dégénérée 0). Effectifs 106/81 sous
  le seuil d'éligibilité gelé : comparaison **déclarée non éligible**,
  aucun calcul promotionnel.
- **C5-10** : CONTENUE ETABLIE exige 1 440/1 440 minutes observées
  (V2.2). Sur 2 571 journées à usage F-F OK, **aucune** journée n'atteint
  1 440/1 440 (halte quotidienne du marché) : numérateurs 0/863
  (2010-13) et 0/632 (2017-20), différence exactement 0, IC dégénéré.
  Lecture : négatif dégénéré — la non-éligibilité de substance de C5-10
  était assumée d'avance au gel ; le critère de qualité générale 95 %
  n'a jamais été utilisé comme preuve d'absence (395 journées COMPLETE,
  2 177 PARTIELLE, 525 EXCLUE publiées au registre). Les 7 touches
  (contact sans franchissement strict) comptent comme événements au
  dénominateur conformément au gel et sont publiées à part.

Aucune association descriptive de ce rapport n'est une preuve prédictive
ni une opportunité exploitable. Aucun J2/J3 automatique.
