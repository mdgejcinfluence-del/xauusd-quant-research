# CAMPAGNE 4 — PROCÈS-VERBAL DE CONTRÔLE FINAL DU DICTIONNAIRE V2

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Contrôle
réalisé après validation de principe (seq 198), avant toute exécution.
Documents contrôlés, livrés intégralement dans le dépôt :
`CAMPAIGN_04_EVENT_DICTIONARY_V2.md` (le « dictionnaire ») et
`CAMPAIGN_04_COMPARISONS_FREEZE.md` (les « dix comparaisons »). Chaque
exigence du fondateur est cochée avec sa localisation exacte ; tout écart
aurait valeur de non-conformité — aucun n'a été relevé au terme du contrôle,
sous réserve des deux points de vigilance publiés (§8).

## 1. Prévision F3 connue à l'ouverture vs RV réalisée connue à la clôture

| Exigence | Localisation | Verdict |
|---|---|---|
| Causalité F3 documentée (entraînement, horizon, horodatage, seuils) | Dictionnaire §2 (tableau audité sur `ci_tools/f3_har.py` et `F3_PREREG.json`) : OLS roulant 500 journées ré-estimé chaque jour sur paires passées, horizon 1 jour, prédiction du jour j connaissable à la clôture de j−1 | Conforme |
| Non-causalité des terciles poolés historiques traitée | §2, constat explicite ; double publication : tercile **causal roulant** (quantiles 1/3–2/3 des prédictions des 250 journées précédentes disposant d'une prédiction, min 60, jour courant exclu) seul porteur de la mention « connu à l'ouverture », et tercile poolé étiqueté « référence rétrospective » | Conforme |
| RV du jour jamais présentée comme connue à son ouverture | §3 (« elle n'est jamais présentée comme disponible à son ouverture ; toute conséquence commence au plus tôt le jour suivant ») et §8 (interdit explicite) | Conforme |
| Distinction des quatre objets (passé / courant / confirmation / conséquence) | §4–§5 ; blueprint §2 | Conforme |

## 2. Seuils appliqués à la bonne variable, passé seul

Vérification variable par variable : les seuils terciles de l'état courant
s'appliquent à **RV_j** contre la distribution des RV des 60 journées
précédentes (jamais à la prédiction F3, qui a ses propres terciles causaux —
deux variables, deux seuils, §2 et §4) ; les seuils de session s'appliquent
à la RV **de la même session** (§6) ; le seuil de queue s'applique aux |r|
M1 poolés des 60 journées précédentes avec minimum de 20 000 barres (§7) ;
chaque seuil exclut le jour/la session courant(e). **Verdict : conforme.**

## 3. Formules exactes de chaque mesure (reprises intégralement)

- RV_j = √(Σ_k r_k²) × 10⁴ bp, r_k = rendements log entre clôtures M1
  consécutives **internes à la journée** (premier rendement du jour
  exclu, aucun overnight) ; journée utilisable ≥ 300 barres (§3).
- RV de session : même formule, interne à la session, premier rendement
  de session exclu ; session utilisable ≥ 60 barres (§6).
- Asymétrie g1 = m₃ / m₂^{3/2}, moments empiriques centrés **sans
  correction de biais**, rendements M1 du jour (§7).
- Fréquence d'extrêmes du jour = part des barres M1 avec |r| supérieur au
  quantile 99 causal défini ci-dessus (§7).
- Volatilité de la volatilité = écart-type des log(RV) sur les 20
  dernières journées y compris j, état par tercile contre les 60 valeurs
  précédentes excluant j (§7).
- Dispersion intrajournalière = RV_session_max / RV_session_min, si ≥ 3
  sessions utilisables (§7).
- Rendement journalier (fenêtres de conséquences) = log-clôture M1 de fin
  de journée j / fin de journée j−1, en bp (§5).
- Quantiles : interpolation linéaire partout (§1).

## 4. Horodatage des transitions et des conséquences

| Événement | Horodatage figé | Source |
|---|---|---|
| Date candidate C | Première journée d'état courant différent de l'épisode précédent | §5 |
| Date de confirmation D | C + 2 journées de cotation (3e journée consécutive dans le nouvel état) ; jamais antidatée | §5 |
| Non-confirmation | Persistance de 1 ou 2 journées puis sortie d'état ; date candidate, sens, durée et motif conservés au catalogue | §5 |
| Traversée et vitesse | Journées entre la fin de l'ancien épisode (exclue) et le début du nouvel épisode (incluse), états intermédiaires comptés ; rapide 1–2, intermédiaire 3–4, progressive ≥ 5 | §5 |
| Référence du retour à l'habituel R* | Médiane des RV des 60 journées précédant **le début de l'épisode HAUT**, figée pendant l'épisode ; retour = première journée post-épisode à RV < R*, censure 60 j publiée | §5 |
| Fenêtres de conséquences | +1–5 et +6–20 journées après D (confirmées) ou après C (non confirmées, publiées séparément), tronquées à la veille de la prochaine candidate, troncatures comptées | §5 |

**Verdict : conforme** — aucun instant n'est défini par une information
postérieure à lui sans être étiqueté comme tel (la confirmation est par
construction postérieure à la candidate, et datée comme telle).

## 5. Les dix comparaisons : population, fenêtre, unité, matérialité

Le document des dix comparaisons spécifie pour chacune (C4-01 à C4-10) :
hypothèse descriptive, variable et sa formule de rattachement, population
et appariement des bras, fenêtre, **unité statistique** (transition,
épisode ou journée — jamais mélangées), critère de matérialité (5 points ;
ratio 1,15 ; seuil spécifique C4-06 : différence de médianes de g1 ≥ 0,10,
une grandeur signée ne pouvant porter de ratio). Avertissements intégrés :
C4-02 exige l'appariement par sens ; C4-07 n'utilise que les journées
classées des deux côtés (NON_CLASSE publié) ; C4-08 est étiquetée
contemporaine sans antériorité revendiquée ; C4-10 utilise explicitement
l'état de la **veille**. **Verdict : conforme.**

## 6. Blocs, fenêtres tronquées, transitions non confirmées

- Bootstrap par **blocs mobiles de 20 journées de cotation**, 2 000
  réplicats, graine à figer au gel d'exécution ; épisodes, candidats,
  confirmations et fenêtres **recalculés dans chaque réplicat** ; règle
  des coutures publiée (confirmation tronquée par une couture = non
  confirmée dans le réplicat, uniformément).
- Fenêtres tronquées à la prochaine candidate (aucune journée ne sert
  deux fenêtres d'une même famille) ; nombre de troncatures publié par
  comparaison.
- Transitions non confirmées : catalogue obligatoire (dictionnaire §5),
  population propre de C4-02, jamais supprimées ni reclassées.
**Verdict : conforme.**

## 7. Règles de publication en cas d'effectifs insuffisants

Éligibilité descriptive : ≥ 200 journées par bras et ≥ 30 transitions par
bras pour les comparaisons de transitions — explicitement qualifiée de
**minimum de lisibilité, non de garantie de puissance** (comparaisons §1) ;
en deçà : comparaison publiée « non éligible » avec ses effectifs ; zones
d'amorçage sans état comptées et publiées (dictionnaire §1, §3) ; censures
publiées (durées §5, retours §5) ; négatifs et sous-le-seuil conservés au
registre (comparaisons §1, méthode §3). **Verdict : conforme.**

## 8. Points de vigilance publiés (non-bloquants, à charge d'exécution)

1. Le tercile causal F3 (250 journées) produit des étiquettes différentes
   des étiquettes poolées historiques : les matrices de discordance
   publieront les deux formes côte à côte sans jamais les fusionner, et
   l'audit d'impact (`F3_POOLED_LABELS_IMPACT_AUDIT.md`) fait foi pour la
   lecture des campagnes 0 à 3.
2. Le recalcul dans chaque réplicat du bootstrap est le poste de calcul
   dominant ; si son coût dépassait le budget CI, la campagne devra se
   suspendre et le documenter plutôt que dégrader la méthode en silence
   (règle d'arrêt propre, méthode §3).

## 9. Conclusion du contrôle

Le dictionnaire v2 et la liste des dix comparaisons satisfont, point par
point, aux sept corrections du retour fondateur (seq 195) et aux
exigences du présent contrôle. **Aucune exécution n'est engagée par le
présent procès-verbal** ; la validation finale d'exécution appartient au
propriétaire. Hashes des fichiers livrés : calculés et chaînés dans
l'entrée de chaîne accompagnant ce procès-verbal (seq 199–200).
