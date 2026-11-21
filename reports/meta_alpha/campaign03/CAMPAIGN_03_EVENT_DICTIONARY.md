# CAMPAGNE 3 — DICTIONNAIRE DES ÉVÉNEMENTS (GELÉ AVANT CALCUL)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Ce dictionnaire
est soumis à validation propriétaire ; son hash sera chaîné avant toute
extraction. Aucune définition ne peut être modifiée après consultation des
résultats. Prix Mid de barres (déclaré) ; seuils toujours causaux (passé
uniquement) ; aucune variable ne classe un événement à l'aide de son futur.

## 1. Conventions communes

- Corpus : barres M1 reconstruites depuis le tick IS (282 partitions,
  2010-01-04 → 2019-12-16), agrégées en M5/M15 par clôtures de barres complètes.
- Régime F3 du jour (gelé seq 75), ères 2010–13 / 2014–16 / 2017–20, sessions
  UTC conventionnées (Asie 00–08, Londres 08–13, New York 13–21, nuit 21–24).
- Unité d'indépendance : **journée** pour IMP (plusieurs impulsions d'une même
  journée ne sont pas indépendantes), **journée** pour CONS ; bootstrap par
  journées le cas échéant.
- Censure : toute issue non observable dans sa fenêtre (fin de journée) est
  censurée, comptée et publiée ; jamais imputée.

## 2. Famille IMP — Impulsions M5 (principale) et M15 (secondaire, séparée)

| Élément | Définition gelée |
|---|---|
| Déclenchement (T0) | Clôture d'une barre M5 (resp. M15) dont le rendement absolu \|r\| ≥ **quantile 90 de \|r\| calculé sur les 60 jours calendaires précédents** de la même famille (seuil causal roulant, minimum 2 000 barres d'historique, sinon pas de déclenchement) |
| Direction descriptive | Signe du rendement de la barre de déclenchement (hausse/baisse) — étiquette de description, pas un signal |
| Amplitude initiale | \|r\| de la barre de déclenchement, en bp (connue à T0) |
| Instantanés | T0, +1, +3, +6, +12 barres de la famille |
| Variables à chaque instantané (passé uniquement) | Amplitude cumulée dans le sens de l'impulsion depuis T0 (bp) ; retracement maximal atteint jusqu'ici (cumul contraire maximal depuis T0, en % de l'amplitude initiale et en bp) ; position du prix par rapport au prix d'origine (bp, signée dans le sens de l'impulsion) ; volatilité réalisée des barres écoulées ; spread médian des M1 de la dernière barre ; amplitude déjà parcourue (range cumulé) |
| Issues (strictement après chaque instantané) | Retracement maximal ultérieur (jusqu'à +60 min après T0, borné fin de journée) ; extension supplémentaire dans le sens de l'impulsion ; position à +15/+30/+60 min après l'instantané (bp signée) ; temps jusqu'à retracement de 50 % puis 100 % de l'amplitude initiale (censuré à +60 min) |
| Regroupement | Toutes les impulsions d'une même journée forment une grappe-journée ; les chevauchements (impulsion dans la fenêtre d'issue d'une précédente) sont comptés et signalés, jamais supprimés |

La profondeur future du retracement ne classe **jamais** le déclenchement : les
groupes descriptifs éventuels n'utilisent que l'amplitude initiale et les
grandeurs d'instantané.

## 3. Famille CONS — Consolidations M1

| Élément | Définition gelée |
|---|---|
| Barre calme | Barre M1 dont le range (haut−bas) ≤ **0,5 × médiane des ranges M1 des 5 journées précédentes** (seuil causal, minimum 1 000 barres d'historique) |
| Formation (T0) | Clôture de la **6e barre calme consécutive** ; la consolidation naît à cet instant, sa durée future est inconnue |
| Range de formation | Haut−bas des 6 barres de formation, en bp (connu à T0) |
| Instantanés | T0, +3, +6, +12 minutes |
| Variables à chaque instantané | Durée écoulée depuis le début de la suite calme ; range cumulé de la consolidation jusqu'ici (bp) ; position du prix dans le range (0–1) ; ratio de compression = range cumulé / range médian horaire du même contexte ; volatilité réalisée ; spread médian |
| Sortie (issue de formation) | Première barre après T0 dont le range > **2 × le range de formation**, ou première clôture hors du range cumulé, au premier des deux ; sinon **censurée** à +120 min ou fin de journée. Les deux types de sortie sont distingués ; la sortie n'est **pas** présupposée être une expansion |
| Issues après sortie (ou après chaque instantané si pas encore sortie) | Range des 60 minutes suivantes (bp) ; excursions maximale dans le sens de la clôture de sortie et dans le sens opposé (bp, descriptif symétrique) ; position à +15/+30/+60 min par rapport au milieu du range de consolidation |
| Regroupement | Une consolidation par suite calme (pas de double compte des suites emboîtées : une nouvelle formation exige une barre non calme intercalée) ; grappe = journée |

## 4. Ce que le dictionnaire interdit

Classifier une impulsion par son retracement final ; classifier une
consolidation par son range de sortie ; présenter une variable d'instantané
tardif comme disponible à T0 ; nommer « continuation » ou « expansion » une
issue avant de l'avoir mesurée ; comparer une famille à un contexte qui n'est
pas le sien (session/régime/ère appariés selon le document de méthode).
