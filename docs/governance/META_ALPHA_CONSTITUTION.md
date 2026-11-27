# META ALPHA — CONSTITUTION PERMANENTE

*Mission fondatrice 009 (seq478). Ce document est la référence permanente
du projet. Toute future mission est évaluée par rapport à lui.*

## 1. Objectif fondamental

META ALPHA découvre les **modèles économiques** exploités par les traders
qui génèrent régulièrement des revenus, identifie les phénomènes de
marché qui rendent ces modèles rémunérateurs, et construit **ses propres
systèmes** capables de détecter et d'exploiter ces phénomènes,
indépendamment des traders observés.

**L'unité fondamentale de recherche n'est pas le trader. C'est le modèle
économique.** Les traders sont des sources de découverte ; les
transactions sont des indices ; les données de marché sont le terrain
d'identification ; nos moteurs sont nos instruments d'exploitation ; la
validation indépendante est notre filtre de vérité ; le portefeuille de
modèles complémentaires est notre objectif final.

## 2. Loi économique fondatrice (hypothèse directrice, non un fait)

« Les traders qui gagnent régulièrement sur l'or ne gagnent pas
nécessairement parce qu'ils prédisent mieux les mouvements. Ils peuvent
gagner parce qu'ils occupent une position économique particulière dans
le marché, acceptent certains risques rémunérés, fournissent un service
de liquidité ou exploitent des circonstances dans lesquelles les autres
participants ont besoin d'agir. »

Familles à étudier sans s'y limiter : fourniture de liquidité,
déséquilibres temporaires, récupération d'inventaire, mouvements
impulsifs — et toute famille nouvelle suggérée par les observations.
Des renforcements et des sorties proches du prix moyen ne prouvent pas
une activité de market making.

## 3. Ce que nous ne cherchons pas

Copier les entrées exactes d'un trader ; reproduire toutes ses
transactions ; retrouver son code ou chaque paramètre ; identifier une
milliseconde de déclenchement sans nécessité économique ; accumuler des
transactions sans question d'identification ; optimiser une simulation
jusqu'à un résultat positif artificiel. Ces travaux ne sont légitimes
que s'ils servent directement l'identification ou la validation d'un
modèle économique.

## 4. Les trois questions obligatoires (pour chaque trader étudié)

1. **Quel modèle économique exploite-t-il ?** (source potentielle du revenu)
2. **Pourquoi ce modèle peut-il générer un rendement ?** (phénomène,
   conditions, risques acceptés en contrepartie)
3. **Comment exploiter ce même phénomène avec nos propres ordres ?**
   (détection dans nos données, nos entrées/sorties/risques, rendement
   net après tous les coûts)

## 5. Méthode de découverte

Extraire le maximum d'information économique des observations
disponibles (transactions publiques, séquences, volumes, délais, prix,
trajectoires, statistiques publiques), puis identifier précisément les
informations supplémentaires réellement nécessaires. Aucun minimum
universel de transactions : cinq paniers peuvent révéler une logique
d'accumulation, jamais prouver une rentabilité durable. Chaque demande
de données répond à une question d'identification concrète.

## 6. Données et leurs distinctions (jamais mélangées)

Ticks Dukascopy (348 partitions certifiées, 685 118 625 ticks,
2010-01-04 → 2026-09-30) ; cotations HFM ; transactions authentiques
des traders ; simulations de nos moteurs ; contrefactuels. Pour chaque
modèle : signature → fréquence → rendement brut → coûts réalistes
(comptés une fois) → simulation → pertes extrêmes → validation
indépendante → capacité/stabilité. Détecter un phénomène ne suffit pas :
il faut une exécution rentable.

## 7. Nos propres ordres

Nous ne copions pas les entrées des traders. Nos horaires, volumes et
sorties peuvent différer ; seul le phénomène économique compte, s'il est
reproductible. L'edge se juge en rendement net après spread, commission,
slippage et financement — jamais au seul taux de réussite. Un avantage
brut inférieur aux coûts n'est pas un edge.

## 8. Portefeuille de modèles

Objectif final : plusieurs sources de rendement suffisamment
différentes (registre `META_ALPHA_MODEL_REGISTRY.md`), étudiées en
corrélations, pertes simultanées, régimes, risques communs et capacité.
Un modèle peut être rejeté, conditionnel, trop risqué ou non
identifiable : tous ces résultats sont utiles et conservés.

## 9. Science et identifiabilité

Distinguer toujours : **FAIT OBSERVÉ / INFÉRENCE / HYPOTHÈSE ÉCONOMIQUE /
MÉCANISME IDENTIFIÉ / AVANTAGE ÉCONOMIQUE VALIDÉ**. Qualifications
normalisées : DÉMONTRÉ ; FORTEMENT ÉTAYÉ ; COMPATIBLE MAIS NON
IDENTIFIÉ ; NON DÉMONTRABLE AVEC LES DONNÉES DISPONIBLES ; RÉFUTÉ.
Quand plusieurs modèles restent compatibles : les énumérer, identifier
leurs différences, chercher le test discriminant le moins coûteux. Ne
pas multiplier les campagnes sur un problème mathématiquement non
identifiable avec les observations disponibles. Avant toute mission :
quelle incertitude réduit-elle, quelle décision changera-t-elle ?

## 10. Interdictions absolues

Transformer META ALPHA en copie automatique de traders ; confondre
comportement observable et modèle économique ; déclarer un modèle
identifié ou un edge validé sans preuves (jamais VALIDATED sur les
données de construction) ; inventer données ou résultats ; mélanger
réel et simulé ; lookahead ; double comptage des coûts ; créer une
nouvelle version d'un moteur pour améliorer les chiffres ; sacrifier
moteurs et résultats gelés ; multiplier les campagnes sans question
économique ; accepter une dérive parce qu'une instruction est détaillée
ou vient de ChatGPT ; tout contournement de plateforme, accès non
autorisé ou ordre réel sans mandat explicite distinct.

## 11. Gouvernance

GitHub est la source unique de vérité. `main` n'est jamais modifiée
directement ; les moteurs et résultats certifiés sont préservés ; chaque
mission passe le contrôle du garde-fou (`META_ALPHA_DRIFT_GUARD.md`)
avant exécution ; les décisions structurantes vont au journal
(`META_ALPHA_DECISION_LOG.md`) et au registre des procès-verbaux
(`reports/meta_alpha/TRIAL_LEDGER_CHAIN.json`).

**Nous ne cherchons pas à devenir les traders que nous observons. Nous
cherchons à découvrir les mécanismes économiques qui les rémunèrent,
puis à les exploiter avec notre propre intelligence quantitative.**
