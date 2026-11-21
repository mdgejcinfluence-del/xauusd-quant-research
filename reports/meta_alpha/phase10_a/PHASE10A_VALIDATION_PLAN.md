# PHASE 10-A — PLAN DE VALIDATION, DÉPENDANCES, MULTIPLICITÉ, ARRÊTS

## 1. Validation temporelle (F)

- **Qualification honnête** : le corpus IS a déjà été exploré ; toute
  évaluation y est une **évaluation historique**, pas une confirmation.
  Les résultats seront publiés sous cette étiquette, sans exception.
- **Stabilité temporelle descriptive** : chaque famille est rapportée
  par ère (2010–13 / 2014–16 / 2017–20) et globalement ; une famille
  dont l'espérance brute change de signe entre ères est classée
  instable et arrêtée, sans recherche de la « bonne » période.
- **Aucune optimisation chronologique** : pas de choix de fenêtre,
  de quantile ni d'horizon après lecture ; les constantes du
  protocole validé sont les seules appliquées.
- **Confirmation future** : toute famille survivante devra faire
  l'objet d'un protocole de confirmation séparé — soit prospectif
  (données postérieures à la date de gel, collectées après coup),
  soit, sur autorisation distincte du propriétaire seulement,
  ouverture du holdout scellé. Aucune des deux n'est autorisée par le
  présent dossier.

## 2. Dépendances

Fenêtres de mesure chevauchantes et événements rapprochés : bootstrap
par **grappes temporelles** (composantes connexes des fenêtres qui se
recouvrent, franchissant les frontières de journée), comme gelé en
campagne 8 ; diagnostics publiés (nombre de grappes, plus grande
grappe, part des chevauchements). Règle de grappe dominante reprise :
au-delà de 5 % des unités d'un bras, inférence étiquetée fragile et
aucune candidature. Événements H1/H4 d'une même journée : même grappe
si leurs fenêtres se touchent.

## 3. Multiplicité

Famille fermée de **six tests** (F10-01…F10-06, F10-06 étant une porte
de magnitude sans p-value). Correction **BY à m = 6 fixe** sur les
p-values produites ; toute famille arrêtée par une porte économique
avant inférence publie « arrêtée à la porte » et conserve le facteur
de famille (pas de redistribution des seuils). Aucun test
supplémentaire, aucune ventilation transformée en test (sessions et
ères descriptives uniquement). Résultats négatifs et non évaluables
publiés au même titre que les positifs.

## 4. Conditions d'arrêt (H, plan de campagne limité)

1. Chaque famille s'arrête dès qu'une porte du modèle de coûts
   échoue ; l'arrêt est publié avec les grandeurs mesurées. **Aucune
   substitution par un sous-groupe** (ère, session, signe ou autre
   découpage) ne peut relancer une famille arrêtée : les découpages
   sont des diagnostics non confirmatoires. Les limites de queue
   P90 ≤ 10 × C_ref et ES90 ≤ 15 × C_ref s'appliquent **séparément**
   aux distributions par événement et par grappe ; un dépassement
   sur l'une des deux arrête la famille au même titre.
2. La campagne s'arrête si **aucune** famille ne franchit les portes :
   conclusion « pas de mouvement capturable aux horizons H1/H4/D1
   dans les conditions mesurées », sans élargissement de la famille,
   sans nouvel horizon, sans retour aux candidates P9.
3. Suspension immédiate et documentée en cas de dépassement des
   ressources gratuites, de données Bid/Ask insuffisantes pour les
   prix exécutables, ou d'incohérence des barres — sans dégradation
   méthodologique (pas de repli silencieux vers des mesures Mid
   présentées comme exécutables).
4. Aucune étape de construction de stratégie, de fiche opérationnelle
   ou de `challenge_sim` n'est incluse dans cette campagne : elle
   exigerait une décision ultérieure, postérieure à une confirmation
   indépendante.

## 5. Limites du protocole (G)

Le corpus IS a servi aux campagnes 0–8 et à la Phase 9 : les
événements H1/H4/D1 recoupent des phénomènes déjà décrits à d'autres
échelles (impulsions, dépassements, chocs) ; une association trouvée
ici ne serait ni nouvelle au sens fort, ni indépendante. Les barres
Bid/Ask reconstruites depuis les ticks restent des agrégats (le
premier prix exécutable après la décision n'est pas observé à la
milliseconde). Les effectifs D1 sont structurellement faibles
(≈ 2 500 journées, événements extrêmes causaux beaucoup moins). Le
protocole mesure des mouvements *capturables en principe*, pas des
profits.
