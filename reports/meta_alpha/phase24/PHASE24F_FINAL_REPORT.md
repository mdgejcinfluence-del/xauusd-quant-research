# PHASE 24-F — RAPPORT FINAL : LE SCORE CLASSE LE LABEL, PAS L'ARGENT

Statut : `EXPLORATORY_POST_HOC`. Aucune règle de sélection n'est produite par cette phase.

**Réponse à la question de clôture : non.** Le score M15 contient une information de classement
prédictive réelle et stable — la fréquence de réalisation du label croît de façon monotone avec
le score dans les deux populations (jusqu'à 0,77-0,85 dans les classes hautes). Mais il ne
distingue pas les événements économiquement favorables :

- La frontière de point mort construite sur la calibration (P_BE = 0,654, à partir de
  G = +18,01 bp et L = 34,05 bp) est franchie en fréquence par la classe [0,70 ; 0,75) sans que
  son espérance devienne positive (−4,36 bp) : à l'intérieur des classes, les gains réalisés
  rétrécissent pendant que les pertes restent entières. Réaliser le label plus souvent ne suffit
  pas quand chaque réalisation rapporte moins.
- L'espérance S2 est négative dans toutes les classes évaluables de l'évaluation et dans trois
  des quatre classes de calibration ; la seule classe positive change de signe entre les deux
  populations.
- Les faux positifs sont diffus : score médian 0,65-0,66 contre 0,68-0,69 pour les vrais
  positifs, profils de variables causales quasi identiques — non séparables sans nouveau
  prédicteur, ce qui est interdit.

Verdicts : calibration et évaluation — `M15_SCORE_PREDICTIVE_BUT_ECONOMICALLY_NONMONOTONIC` ;
compléments `M15_ECONOMIC_BREAK_EVEN_NOT_REACHED` (développement) et
`M15_FALSE_POSITIVES_NOT_SEPARABLE` (évaluation). Il n'y a donc pas de base pour une phase de
décision coût-sensible fondée sur ce score seul : la relation économique cohérente qui aurait
pu la justifier est absente, et le rapport le conclut sans ajouter de filtre artificiel.
Aucun passage en démonstration ou en réel n'est autorisé.
