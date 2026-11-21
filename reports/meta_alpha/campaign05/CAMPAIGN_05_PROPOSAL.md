# CAMPAGNE 5 — PROPOSITION DE CARTOGRAPHIE (À VALIDER, AUCUN CALCUL)

**PROPOSITION — PRÉPARATION NON ENCORE OUVERTE — AUCUN CALCUL LANCÉ.**
Proposition soumise au fondateur après la clôture définitive de la
campagne 4 (seq 204 et note de censure associée). Conformément au plan de
reprise de l'exploration (seq 183, §3), la campagne 5 proposée couvre les
familles **F-E (comportements temporels des sessions)** et **F-F (extrêmes
journaliers et hebdomadaires datés)**. Si le principe est validé, la
préparation complète suivra le patron des campagnes 3 et 4 (blueprint,
dictionnaire des événements soumis à validation avant calcul, méthode et
multiplicité, couverture) ; **aucune exécution n'aura lieu avant
validation du dictionnaire.**

## 1. Pourquoi ces deux familles, et pourquoi maintenant

- Ce sont les deux familles restantes du premier cercle du plan de
  reprise qui n'ont jamais reçu de traitement causal complet : les
  ouvertures de Londres et de New York ont été décrites (campagnes 1 et
  1.1), mais **l'ouverture d'Asie n'a jamais été mesurée** — elle exige un
  traitement inter-jours dédié (sa « fenêtre d'ouverture » précède 00:00
  UTC, donc la journée précédente au sens calendaire) ; les extrêmes
  journaliers (EV1/EV7) ont été décrits avec des seuils dont la campagne
  1.1 a montré qu'ils devaient être **causaux et datés**.
- Elles n'ont aucun lien de dépendance avec les candidates des campagnes
  3 et 4 : la campagne 5 ne prolonge ni n'optimise ANO-C3/C4, conformément
  à la doctrine multi-familles.
- Elles partagent une même exigence technique — dater proprement des
  événements ancrés sur des frontières (ouverture de session, formation
  d'un extrême) avec uniquement l'information antérieure — ce qui rend
  leur regroupement méthodologiquement cohérent, en familles statistiques
  séparées.

## 2. Questions scientifiques proposées

**F-E — Temporalité fine des sessions.**
1. Comment se comportent les premières minutes de chaque session
   (amplitude, volatilité réalisée, spread de contexte) lorsque l'ancrage
   est strictement causal — y compris l'ouverture d'Asie reconstruite en
   inter-jours (continuité avec la fin de la journée précédente, sans
   jamais importer d'information du jour qui commence) ?
2. Les transitions de sessions (chevauchement Londres → New York,
   fermetures, réouvertures) présentent-elles des comportements
   d'amplitude et de volatilité distincts des cœurs de session, décrits
   sans les nommer signaux ?
3. Existe-t-il des régularités de jour de semaine documentables **sans
   seuil importé** (définitions internes au corpus, gelées avant calcul) ?

**F-F — Extrêmes journaliers et hebdomadaires datés.**
4. À quel moment de la journée l'extrême (haut/bas) qui restera celui de
   la journée se forme-t-il — décrit en distinguant rigoureusement ce qui
   est connaissable en cours de journée (extrême courant daté, seuils
   causaux) de ce qui n'est su qu'à la clôture (extrême final) ?
5. Quelle est la trajectoire intrajournalière (extension, retracement,
   stagnation, mesurés après l'instantané) selon l'heure de formation de
   l'extrême courant, sans classifier la formation par son futur ?
6. Les extrêmes hebdomadaires, en tant qu'événements datés à seuils
   causaux, montrent-ils des comportements de formation et de suite
   distincts des extrêmes journaliers ?

## 3. Règles causales proposées (à geler dans le dictionnaire)

- Aucun classement par le futur : un extrême « final » est une étiquette
  de clôture, jamais un prédicteur ; les instantanés en cours de journée
  n'utilisent que l'extrême courant et des seuils calculés sur le passé
  (par exemple quantiles roulants des amplitudes à la même heure sur les
  journées précédentes — formulation exacte réservée au dictionnaire).
- Ouverture d'Asie : ancrage inter-jours explicite (fenêtre définie par
  rapport à la clôture de la journée précédente), publié comme convention,
  sans donnée fabriquée sur les heures sans cotation.
- Sessions en UTC fixes (patron campagne 4 : aucun changement d'heure
  n'existe dans les horodatages UTC ; convention publiée).
- Comparaisons préenregistrées en nombre fermé (proposition : ≤ 10,
  familles F-E et F-F séparées, correction BY par famille), bootstrap par
  grappes-journées, résultats négatifs et non éligibles conservés et
  publiés, fiches J1 descriptives sans promotion automatique au catalogue
  commun.
- Corpus IS déjà consulté uniquement ; holdout scellé ; flux prospectif
  T0 interdit et toujours inactif ; FRED suspendue (aucun calendrier
  exogène) ; aucun backtest, `challenge_sim`, optimisation ou budget
  expérimental ; 36 cellules S12 intactes ; XAU/USD seul.
- Incidents et insuffisances documentés selon le patron des campagnes 3
  et 4 (publication des non éligibles plutôt qu'élargissement de
  fenêtres ; aucune dégradation méthodologique silencieuse).

## 4. Livrables envisagés (après validation du principe, puis du dictionnaire)

Préparation : `CAMPAIGN_05_SESSION_EXTREMES_BLUEPRINT.md`,
`CAMPAIGN_05_EVENT_DICTIONARY.md`, `CAMPAIGN_05_METHOD_AND_MULTIPLICITY.md`,
`CAMPAIGN_05_DATA_COVERAGE.md`. Exécution (seulement après validation du
dictionnaire) : cartographie, timelines d'événements datés, statistiques
par instantané, registre ANO/négatifs, qualité — sur le modèle des
campagnes précédentes.

## 5. Décision demandée

Valider (ou amender) le principe, le périmètre F-E + F-F et les règles du
§3. À défaut, la proposition restera classée sans suite et une autre
famille du plan (F-G microstructure, F-H interactions, F-I motifs de
chemin) pourra être proposée. **Aucun calcul n'est engagé par la présente
proposition.**
