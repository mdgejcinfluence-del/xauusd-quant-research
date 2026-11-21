# CAMPAGNE 6 — LISTE FERMÉE DES CINQ COMPARAISONS F-G (provisoire, pré-gel)

**Statut : PRÉPARATION — aucun calcul.** Liste fermée proposée pour la
famille F-G ; chaque comparaison précise hypothèse, variable principale
(une seule, cf. redondances du dictionnaire), population, unité, fenêtre,
matérialité, dépendances mécaniques, inférence. Famille de cinq,
correction BY séparée (voir méthode). Seuils de matérialité (livrable 8)
justifiés sous le tableau.

| ID | Hypothèse descriptive exacte | Variable principale | Population (A vs B) | Unité | Fenêtre | Matérialité | Dépendances mécaniques possibles |
|---|---|---|---|---|---|---|---|
| C6-01 | La forme d'une journée dépend de celle de la journée précédente (persistance) | ER du jour j (médiane) | j dont j−1 est « directionnel » (ER_{j−1} ≥ 0,30, constante à geler) vs j dont j−1 est « oscillant » (ER_{j−1} ≤ 0,10) ; paires de journées utilisables consécutives | journée j, grappe = semaine civile (à geler) | journée complète | 0,05 d'ER | persistance de volatilité : si l'amplitude persiste, ER peut persister sans persistance de « forme » propre ; ventilation par amplitude de j publiée |
| C6-02 | La forme diffère selon l'amplitude de la journée | ER (médiane) | tercile haut vs tercile bas d'amplitude A_bp **contemporains, décennaux, étiquetés rétrospectifs** | journée, grappe-journée | journée complète | 0,05 d'ER | **audit spécifique ci-dessous** : S = L/A est mécaniquement lié à A (exclu comme variable primaire ici) ; ER partage L avec A par la volatilité du jour |
| C6-03 | La forme diffère selon le jour de semaine | ER (médiane) | lundis vs vendredis (jour UTC) | journée, grappe-journée | journée complète | 0,05 d'ER | amplitude et couverture du lundi (réouverture hebdomadaire) diffèrent structurellement ; ventilation par statut de couverture publiée |
| C6-04 | La localisation interne du parcours diffère selon le signe du déplacement net | heure du point médian τ (médiane, minutes) | journées Δ_bp ≥ +seuil vs Δ_bp ≤ −seuil (DÉPLACEMENT FAIBLE exclu, compté) | journée, grappe-journée | journée complète | 30 minutes | PD serait mécaniquement déterminé par le signe (publié en secondaire seulement) ; τ dépend de L total, rétrospectif |
| C6-05 | La forme a évolué entre ères | ER (médiane) | 2010–2013 vs 2017–2020 (2014–2016 publiée, hors contraste) | journée, grappe-journée | journée complète | 0,05 d'ER | changement de microstructure et de couverture sur dix ans ; A_bp et taux de couverture publiés par ère ; aucun découpage intra-ère ajusté |

## Audit spécifique C6-02 (dépendances mathématiques amplitude ↔ forme)

- S = L/A contient A au dénominateur : comparer S entre terciles de A
  testerait en partie une identité comptable. **S est donc exclu comme
  variable primaire de C6-02** et n'y sera publié qu'en secondaire
  averti, ou pas du tout (à trancher au gel).
- ER = |Δ|/L ne contient pas A, mais L et A sont deux mesures de
  l'activité du jour (corrélation attendue par construction du marché).
  Le contraste par terciles d'amplitude est donc un contraste **entre
  régimes d'activité contemporains**, descriptif et rétrospectif : il ne
  démontre ni que l'amplitude « cause » la forme, ni l'inverse.
- Contrôles de publication exigés : médianes de A_bp, L et |Δ|/A par
  bras ; si ER diffère mais |Δ|/A aussi dans le même sens avec S
  constant, la lecture « forme » devra être déclassée en lecture
  « déplacement relatif », et publiée comme telle.

## Seuils de matérialité — justification (livrable 8)

- **0,05 d'ER** : ER vit sur [0,1] ; 5 points représentent, pour une
  journée d'amplitude donnée, un écart de géométrie visible (passer
  d'un parcours dont 10 % du chemin sert le déplacement net à 15 %),
  cohérent avec l'échelle « 5 points » utilisée pour les proportions
  des campagnes 4–5. En dessous, l'écart est déclaré sous le seuil
  matériel même s'il est significatif.
- **30 minutes pour τ** : en dessous d'une demi-heure de décalage du
  point médian de parcours, la différence de localisation interne est
  du même ordre que l'incertitude de couverture minute ; seuil à
  confirmer au gel.
- Aucun seuil n'est calibré sur des résultats : aucun n'a été observé
  à ce stade (calculs interdits).

## Ce qui n'est pas dans la famille

Aucune comparaison de rentabilité entre formes, aucun déclencheur,
aucune réutilisation des candidates C5, aucun conditionnement par les
terciles poolés rétrospectifs de F3 (audit seq196/199). Si la validation
du protocole devait réduire la famille (par exemple retirer C6-02 pour
dépendance mécanique jugée rédhibitoire), la liste réduite et sa
justification seraient gelées **avant** tout calcul.
