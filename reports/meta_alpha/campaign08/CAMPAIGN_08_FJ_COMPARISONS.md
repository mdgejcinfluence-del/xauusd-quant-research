# CAMPAGNE 8 — FAMILLE DE COMPARAISONS F-J PROPOSÉE (pré-gel) ET MÉTHODE

**Statut : PRÉPARATION — aucun calcul, rien n'est gelé.** Famille fermée
proposée de cinq comparaisons (livrable 7). Variable principale
commune : **R_60** (continuation signée à +60 minutes, bp, médiane),
sauf J-05. La session UTC est traitée en **ventilation fermée publiée**
de chaque comparaison plutôt qu'en sixième test, pour conserver une
famille de cinq ; ce choix est soumis au propriétaire.

| ID | Hypothèse exacte | Variable | Population (A vs B) | Unité / grappe | Matérialité | Dépendances |
|---|---|---|---|---|---|---|
| J-01 | Le sillage des chocs haussiers diffère de celui des chocs baissiers | R_60 | épisodes isolés haussiers vs baissiers | épisode / grappe-journée | 10 bp | asymétrie de microstructure (spread, liquidité) confondue possible ; signes étudiés séparément par construction |
| J-02 | Le sillage après un épisode regroupé diffère de celui après un choc isolé | R_60 | épisodes regroupés (sillage après dernier choc) vs isolés | épisode / grappe-journée | 10 bp | les épisodes regroupés surviennent en contexte agité (activité pré-événement publiée) ; durée et nombre de chocs publiés |
| J-03 | Le sillage dépend de l'intensité du choc | R_60 | épisodes majeurs (ρ ≥ 2) vs modérés (1 ≤ ρ < 2), isolés | épisode / grappe-journée | 10 bp | ρ est relatif au seuil causal du jour : « majeur » ne signifie pas même amplitude en bp selon l'ère (amplitudes publiées) |
| J-04 | Le sillage a évolué entre ères | R_60 | épisodes isolés 2010–13 vs 2017–20 (2014–16 publiée) | épisode / grappe-journée | 10 bp | évolution de la microstructure et des seuils causaux ; fréquences et intensités par ère publiées |
| J-05 | Le sillage après un choc diffère de celui de minutes non extrêmes comparables | R_60 | épisodes isolés (tous signes, R_60 recentré par signe) vs **pseudo-événements** non extrêmes appariés par construction | épisode ou pseudo-événement / grappe-journée | 10 bp | appariement : même session, même tercile causal d'activité pré-événement, tirage déterministe (première minute éligible de chaque journée et session sans choc à ±60 min, règle à fermer au consolidé) ; jamais de tirage aléatoire ajusté aux résultats |

## Méthode statistique et multiplicité (livrable 8)

- Bootstrap par **grappes-journées**, 2 000 réplicats, graine publiée
  au gel ; différences de médianes, IC percentile 95 %, p bilatérales.
- **BY famille fermée de cinq à m = 5 fixe** (H₅ = 2,283333), règle des
  p NaN héritée des campagnes 6–7 (STRUCTURELLEMENT_NON_EVALUABLE,
  aucune imputation, facteur 5 conservé).
- **Éligibilité** : ≥200 épisodes et ≥100 grappes-journées par bras ;
  en dessous : NON_ELIGIBLE publiée, aucun assouplissement (ni délai
  de regroupement élargi, ni seuil abaissé).
- **Matérialité 10 bp sur R_60** (proposée) : à l'échelle d'un choc
  dont le plancher est déjà de 10 bp et le seuil causal typiquement
  supérieur, un écart médian de continuation inférieur à 10 bp est
  déclaré sous le seuil matériel ; justification soumise au gel, non
  calibrée sur des résultats (aucun calcul effectué).
- Lectures fermées : CANDIDATE_J1 / SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL /
  NÉGATIF / NON_ELIGIBLE / STRUCTURELLEMENT_NON_EVALUABLE.
- Publications fermées hors tests : fréquences de chocs par ère,
  session et signe ; distributions d'intensité ; taux de nouveau choc
  à 60 min ; stabilisation post/pré ; ventilations par session de
  chaque bras. Résultats négatifs et non éligibles publiés.
