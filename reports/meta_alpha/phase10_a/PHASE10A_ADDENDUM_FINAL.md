# PHASE 10-A — ADDENDUM FINAL AVANT GEL

**Statut : VALIDATION FINALE EN COURS — GEL CHAÎNÉ NON AUTORISÉ,
EXÉCUTION NON AUTORISÉE.** Répond aux trois derniers points du
responsable de recherche. Constantes principales déjà acceptées
(fenêtre 250, Q95/Q95/Q90/Q25, porte 3 × C_ref, BY m = 6, effectifs)
conservées. **Aucune donnée consultée, aucun calcul lancé.** Les deux
constantes nouvelles proposées au §1 (limites de queue) et au §2
(délai maximal d'entrée) sont marquées **À VALIDER** : elles ne seront
acquises que par la décision de gel.

## 1. Contrôle de la queue adverse — métriques exactes

Pour un événement i entré au prix exécutable e_i (Ask si sens long,
Bid si sens court) à la première cotation de la barre suivant le
signal, soit a_i(t) l'excursion adverse signée en bp à l'instant t de
la fenêtre d'évaluation (positive quand le prix évolue **contre** le
sens de l'événement, mesurée sur le prix exécutable de sortie :
Bid si long, Ask si court) :

**MAE_i = max_{t dans la fenêtre} a_i(t) ≥ 0 (bp).**

- **P90 du MAE** : P90 = Q₉₀({MAE_i}), quantile à 90 % par
  interpolation linéaire (type 7) sur les événements du bras.
- **Expected Shortfall à 90 % du MAE** :
  **ES90 = (1 / #\{i : MAE_i ≥ P90\}) × Σ_{i : MAE_i ≥ P90} MAE_i**
  — la moyenne des pires 10 % d'excursions adverses.

Calcul **par événement** : les deux métriques sont publiées par
famille et par bras. Calcul **par grappe** : pour chaque grappe
temporelle g, MAE_g = max_{i ∈ g} MAE_i (le pire événement de la
grappe) ; P90 et ES90 sont aussi publiés sur la distribution des
MAE_g comme diagnostic de dépendance. Le critère gelé antérieur est
conservé : **MAE médian ≤ 3 × espérance nette centrale** (porte 3).

**Limites numériques proposées (À VALIDER au gel)** :
**P90(MAE) ≤ 10 × C_ref** et **ES90(MAE) ≤ 15 × C_ref**.
Justification : avec un C_ref typique de l'ordre de 4 bp (spread
~2,3 bp + 1,7 bp), ces bornes plafonnent l'excursion adverse des
pires déciles à ≈ 40 bp et leur moyenne à ≈ 60 bp — l'échelle d'une
à deux heures de mouvement ordinaire du XAU/USD, et déjà 10 à 15 fois
le coût complet d'un aller-retour. Au-delà, le risque de queue
imposerait des stops si larges que l'espérance nette, même positive,
ne serait pas défendable sans preuve d'exécution réelle ; la famille
serait arrêtée à la porte 3 élargie. Ces deux seuils s'ajoutent à la
porte 3, ils ne la remplacent pas.

## 2. Délai maximal d'entrée

Soit t_sig la clôture effective de la barre de signal et t_exec
l'horodatage de la **première cotation exécutable** (premier tick)
suivant t_sig. Soit t_ouv l'ouverture attendue de la barre suivante :
t_sig elle-même en cotation continue ; en cas de fermeture régulière
(coupure quotidienne, week-end), l'heure d'ouverture réelle de la
première barre suivant la fermeture, telle qu'observée dans les
données.

**Règle (constante À VALIDER : Δmax = 120 secondes)** : l'événement
n'est éligible à la mesure de rentabilité exécutable que si la
cotation d'entrée appartient à la première barre suivant le signal
**et** si **t_exec − t_ouv ≤ 120 s**. Au-delà :

- événement déclaré **INÉLIGIBLE_ENTRÉE_TARDIVE** : exclu de toute
  mesure de rentabilité exécutable, mais **comptabilisé et publié**
  dans les données de couverture (effectifs par famille et par cause) ;
- interruptions intra-session non programmées (trou de cotation) :
  t_ouv reste t_sig, donc tout trou de plus de 120 secondes rend
  l'événement inéligible — un prix revenu après un trou ne peut pas
  être présenté comme l'entrée du signal ;
- fermetures régulières et week-ends : l'horloge du délai ne court
  qu'à partir de la réouverture (t_ouv) ; une entrée dans les
  120 premières secondes de la séance de reprise est éligible ;
- si seules des barres (sans ticks) sont disponibles pour un
  segment, le délai est approché par la présence de la barre à son
  créneau attendu, et la mesure est étiquetée approximée.

Justification des 120 secondes : deux barres M1 — au-delà, le premier
prix n'est plus « la première cotation suivant le signal » à aucune
échelle de ce protocole (H1 minimal), et l'entrée mesurerait un autre
état de marché que celui qui a produit le signal.

## 3. F10-06 — définition complète

Pour une journée D dont le range Range_D est inférieur au Q25 causal
des ranges des 250 journées closes précédentes :

**Ratio_i = Range_{D+1} / MedCausale_D**, où

- **numérateur** : Range_{D+1} = (plus haut − plus bas de la journée
  D+1, barres Mid M1) / clôture de D+1 × 10⁴ (bp) — grandeur
  descriptive non directionnelle, le spread Bid/Ask ne s'appliquant
  pas à un range ;
- **dénominateur (référence causale)** : MedCausale_D = médiane des
  Range des **250 journées entièrement clôturées précédant D**
  (calculée à la clôture de D, sans D ni D+1) ;
- **horizon de mesure** : la journée de cotation suivante complète ;
  journée incomplète ⇒ événement censuré publié et exclu ;
- **H0 : médiane(Ratio) = 1** ; **H1 : médiane(Ratio) > 1**
  (alternative unilatérale, seule conforme à l'hypothèse
  d'expansion) ; p-value unilatérale au sein de la famille BY m = 6.

F10-06 demeure **strictement non directionnel** : même si H1 était
retenue, le résultat ne décrirait qu'une expansion d'amplitude et ne
pourrait alimenter aucune règle de sens.

## 4. Comptabilité des coûts — confirmations

1. **C_ref** (spread médian observé de la famille + 1,7 bp) est
   uniquement la **référence d'échelle des portes** 1 (magnitude ≥
   3 × C_ref) et 3 élargie (limites de queue en multiples de C_ref).
2. Les rendements calculés **Ask à l'entrée / Bid à la sortie** (et
   symétriquement) intègrent déjà le spread : il n'est soustrait
   nulle part ailleurs.
3. Le spread n'est **jamais compté deux fois** : soit il est dans les
   prix Bid/Ask, soit — repli Mid étiqueté non exécutable — il est
   déduit une fois dans l'espérance.
4. Les **1,7 bp** sont exactement les coûts complémentaires centraux
   du modèle (commission hypothétique 0,7 + slippage hypothétique
   1,0 bp aller-retour) ; ils sont déduits **une seule fois** dans
   l'espérance nette centrale (porte 2) et n'apparaissent dans C_ref
   que comme échelle comparative, pas comme second prélèvement.
5. Commissions, slippages, élargissements de spread des scénarios
   favorable/défavorable restent des **hypothèses identifiées comme
   telles**, jamais des coûts observés ; seuls les spreads tick
   Bid/Ask sont observés.

## 5. Décisions et modifications réconciliées

Par rapport au dossier et à l'addendum de validation (seq279) :
(a) porte 3 complétée par P90 et ES90 du MAE, avec limites
**10 × C_ref / 15 × C_ref proposées et non encore acceptées** ;
(b) règle d'inéligibilité d'entrée tardive avec **Δmax = 120 s
proposé et non encore accepté**, interruptions et week-ends traités
par horloge à la réouverture ; (c) alternative de F10-06 précisée
**unilatérale** (H1 : ratio > 1), conformément à la présente
décision — les autres tests restent bilatéraux ; (d) confirmations
de non-double-comptage du §4, sans changement de valeur. Tout le
reste est inchangé.

## 6. Intégrité

SHA-256 complets (chaînés en seq281) : protocole `11174d76…`,
dictionnaire `33a5174a…`, modèle de coûts `164ee4e7…`, plan de
validation `db879b89…`, risques/autorisations `35615e11…`, addendum
de validation `fff4c521…`, présent addendum (hash chaîné). Confirmé :
aucune donnée consultée, aucun calcul lancé ; gel et exécution non
autorisés. La prochaine décision est exclusivement celle du gel
définitif du protocole.
