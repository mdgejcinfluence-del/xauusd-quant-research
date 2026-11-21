# CAMPAGNE 5 — LISTE FERMÉE DES COMPARAISONS PRÉENREGISTRÉES (À VALIDER)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Dix
comparaisons maximum, **cinq par famille, jamais fusionnées** ; correction
BY **par famille de cinq** (décision écrite ici, avant calcul : les deux
familles répondent à des questions distinctes et le plan de reprise les
traite comme des familles statistiques séparées). Si le dictionnaire est
validé, cette liste sera chaînée avec lui avant tout calcul ; aucun ajout
ultérieur. Matérialité : 5 points (proportions), ratio 1,15 (médianes et
taux). Éligibilité descriptive : ≥ 200 épisodes et ≥ 100 journées (ou
semaines) par bras — minimum de lisibilité, non garantie de puissance ;
cohérence de signe dans ≥ 2 ères sur 3 quand la dimension n'est pas l'ère.
Bootstrap par grappes-journées (F-E, F-F journalier) ou par semaines
(F-F hebdomadaire), 2 000 répétitions, graine figée au gel d'exécution.

## Famille F-E (sessions)

| ID | Hypothèse descriptive | Variable | Population (A vs B) | Unité | Matérialité |
|---|---|---|---|---|---|
| C5-01 | L'amplitude d'ouverture diffère entre Londres et Asie | Amplitude des 30 minutes suivant l'ouverture (bp, médiane) | Ouvertures LONDRES vs ASIE (toutes classes d'ancrage confondues pour Asie, ventilation publiée) | Ouverture, grappe-journée | ratio 1,15 |
| C5-02 | La poursuite du mouvement pré-ouverture diffère selon la transition | P(poursuite à +30 min, définition dictionnaire) | Transitions vers NEWYORK (13:00) vs vers LONDRES (08:00) | Transition, grappe-journée | 5 points |
| C5-03 | L'ouverture d'Asie diffère selon la continuité inter-jours | Amplitude de la première heure d'Asie (bp, médiane) | Classe CONTINUITE vs TROU_INTRA_SEMAINE (REOUVERTURE_SEMAINE publiée à part, jamais dans ce contraste) | Ouverture, grappe-journée | ratio 1,15 |
| C5-04 | Les ouvertures de Londres du lundi diffèrent de celles du vendredi | Amplitude des 30 minutes suivant l'ouverture de Londres (bp, médiane) | Lundis vs vendredis (jour UTC) | Ouverture, grappe-journée | ratio 1,15 |
| C5-05 | Le contexte de spread d'ouverture diffère entre New York et Londres | Spread médian des 15 premières minutes (bp, médiane) — contexte uniquement, jamais un coût | Ouvertures NEWYORK vs LONDRES | Ouverture, grappe-journée | ratio 1,15 |

## Famille F-F (extrêmes datés)

| ID | Hypothèse descriptive | Variable | Population (A vs B) | Unité | Matérialité |
|---|---|---|---|---|---|
| C5-06 | La précocité de première atteinte diffère selon le côté | P(première atteinte avant 08:00 UTC) | Premières atteintes HAUT vs BAS (journalier) | Atteinte, grappe-journée | 5 points |
| C5-07 | L'extension après première atteinte diffère selon le côté | Extension supplémentaire à +60 min au-delà du niveau franchi (bp, médiane) | Premières atteintes HAUT vs BAS | Atteinte, grappe-journée | ratio 1,15 |
| C5-08 | Le retracement après atteinte diffère selon l'heure de formation | Retracement maximal à +60 min sous le niveau franchi (bp, médiane) | Atteintes formées avant 13:00 vs à partir de 13:00 (côtés poolés, ventilation par côté publiée) | Atteinte, grappe-journée | ratio 1,15 |
| C5-09 | La précocité hebdomadaire diffère selon le côté | P(première atteinte hebdomadaire avant mercredi 00:00 UTC) | Premières atteintes hebdomadaires HAUT vs BAS | Atteinte, grappe-semaine | 5 points |
| C5-10 | La part des journées contenues a changé entre ères | P(journée sans première atteinte ni touche, ni HAUT ni BAS) | Journées 2010–13 vs 2017–20 | Journée | 5 points |

Toutes les définitions renvoient au dictionnaire de la campagne 5 ;
résultats négatifs, sous le seuil matériel et non éligibles publiés au
registre, comme aux campagnes précédentes.
