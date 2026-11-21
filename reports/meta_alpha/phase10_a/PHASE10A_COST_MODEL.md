# PHASE 10-A — MODÈLE DE COÛTS ET PORTES ÉCONOMIQUES ÉLIMINATOIRES

## 1. Modèle de coûts (D)

- **Spread observé** : mesuré sur ticks Bid/Ask à la barre de décision
  et intégré aux prix d'entrée/sortie Bid/Ask. Quand les prix sont
  Bid/Ask, le spread est payé **une fois** dans les prix ; il est
  interdit de le soustraire à nouveau. En repli Mid (étiqueté
  non exécutable), un aller-retour coûte un spread complet, compté
  une seule fois.
- **Commissions** : non observées dans le corpus → scénarios
  hypothétiques étiquetés (bp aller-retour), jamais présentés comme
  des relevés.
- **Slippage et latence** : non mesurables sur barres → scénarios
  (favorable / central / défavorable), le scénario défavorable
  élargissant aussi le spread (×1,5) à titre de proxy déclaré.
- **Swap/financement** : nul pour des fenêtres intraday ; pour D1 et
  toute tenue au-delà de la clôture, un coût de swap **hypothétique**
  par nuit doit être ajouté avant toute lecture — déclaré, jamais omis.
- **Stops et remplissages partiels** : non modélisables sans carnet ;
  le MAE publié borne le risque d'exécution, sans prétendre le remplir.

Trois scénarios d'étape B sont repris comme grille par défaut
(commission 0,0/0,7/1,4 bp ; slippage 0,5/1,0/3,0 bp aller-retour),
à re-geler dans le protocole d'exécution.

## 2. Portes économiques éliminatoires (E) — définies avant toute campagne

Appliquées dans l'ordre, **avant** toute lecture inférentielle :

1. **Porte de magnitude** : la médiane de l'excursion absolue à
   fenêtre fixe de la famille doit atteindre **au moins 3× le coût
   total central aller-retour** estimé au spread médian de la famille.
   En dessous, les mouvements typiques ne peuvent pas absorber les
   coûts : **arrêt de la famille**, résultat publié comme négatif
   économique, sans test de significativité « pour voir ».
2. **Porte d'espérance brute** : l'espérance brute de la variable
   primaire (prix exécutables Bid/Ask, ou Mid étiqueté) doit être
   **strictement supérieure au coût total central**. Sinon arrêt :
   une espérance qui ne couvre pas le scénario central ne sera pas
   sauvée par le scénario favorable.
3. **Porte de queue** : le MAE médian ne doit pas excéder **3× la
   valeur absolue de l'espérance nette centrale** ; une espérance
   positive portée par une queue adverse disproportionnée est classée
   fragile et arrêtée à ce stade. **Porte de queue élargie (gel)** :
   **P90(MAE) ≤ 10 × C_ref** et **ES90(MAE) ≤ 15 × C_ref**, appliquées
   **séparément** à la distribution par événement et à la distribution
   par grappe (définitions exactes : addendum final §1) ; le
   dépassement sur l'une des deux distributions arrête la famille.
   S'y ajoute l'éligibilité d'entrée : première cotation au plus
   **120 secondes** après l'ouverture attendue de la barre suivant le
   signal, sinon l'événement est INÉLIGIBLE_ENTRÉE_TARDIVE (addendum
   final §2, règle identique au dictionnaire des variables).
4. **Porte d'effectif** : au moins 200 événements et 100 grappes
   temporelles par bras ; sinon famille déclarée non évaluable.

Une famille qui franchit les portes n'est **pas** une stratégie :
elle devient seulement éligible à l'étape de validation (§ plan de
validation), puis à une confirmation indépendante hors corpus exploré
avant tout statut J2/E1. Les seuils 3× sont des constantes de
conception à valider par le propriétaire au gel ; ils sont choisis
pour que l'erreur de mesure, le slippage réel et la dérive des coûts
ne puissent pas, à eux seuls, inverser le signe d'une espérance.
