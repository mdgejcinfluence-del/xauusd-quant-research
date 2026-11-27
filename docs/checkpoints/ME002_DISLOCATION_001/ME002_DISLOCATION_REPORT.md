# ME-002.1 — DÉSÉQUILIBRE TEMPORAIRE : RAPPORT

Protocole gelé seq488 : écart du Mid à sa médiane causale de 15 min
≥ 5/10/20 bp, résorption tradée en fade symétrique (vente du pic au
bid, achat du creux à l'ask), sortie au retour à la médiane ou à 4 h,
coûts comptés une fois. 4 272 épisodes, 5 partitions certifiées.

## Résultat

- **Phénomène statistique : DÉMONTRÉ.** La médiane est retouchée dans
  47–86 % des cas selon seuil et segment (davantage aux petits seuils).
- **Edge net de l'exploitation symétrique : RÉFUTÉ.** Espérance après
  coût central négative dans **les 6 combinaisons groupe × seuil**
  (−2,0 à −5,2 bp), PF 0,46–0,88, en découverte comme en validation.
  La médiane des épisodes est positive (+2,4 à +18,2 bp) mais les
  épisodes non résorbés marqués à 4 h (−136 à −301 bp) dominent :
  à ces échelles, l'écart à la médiane est plus souvent le début
  d'une continuation que d'une résorption exploitable, et le gain
  jusqu'à la médiane est trop petit pour payer spread + queue.
- **Dépendance à ME-001** : les deux familles partagent le même
  terreau (excursions et retours partiels), mais ME-001 vise le retour
  au plus haut antérieur côté acheteur uniquement — sa géométrie de
  gain diffère. ME-002 sous cette forme n'apporte **aucune source de
  rendement indépendante** ; le classement « portefeuille
  diversifié » est donc refusé pour ce couple.

## Verdict

ME-002 (fade symétrique vers la médiane 15 min) : **REJECTED** comme
exploitation. Le phénomène de résorption partielle existe mais n'est
pas monétisable ainsi après coûts. Cette réfutation renforce par
contraste le statut relatif de ME-001 : ce n'est pas « tout retour
vers un niveau » qui paie, mais une géométrie précise (acheteur,
retour au plus haut, filtre de volatilité à l'entrée) — qui reste
elle-même à valider prospectivement. Aucun moteur créé.
