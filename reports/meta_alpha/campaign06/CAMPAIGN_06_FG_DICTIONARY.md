# CAMPAGNE 6 — DICTIONNAIRE F-G : VARIABLES, FORMULES, CONVENTIONS

**Statut : PRÉPARATION — définitions proposées, non gelées, aucun calcul
effectué.** Toute constante marquée « à geler » devra être fixée dans le
protocole consolidé validé avant exécution.

## 1. Convention des journées et horaires (livrable 3)

- Journée = journée civile **UTC**, 00:00–23:59. Barres M1 : une barre
  par minute, horodatée par son **début** ; elle devient disponible à sa
  **clôture** (début + 1 min), convention héritée de C5/V2.2.
- Fréquence d'observation : **clôtures minute** des barres M1,
  convention unique pour toute la campagne. Justification : c'est la
  plus fine fréquence disponible uniformément sur 2010–2020 dans le
  corpus ; toute mesure de longueur de chemin dépend de la fréquence
  d'échantillonnage (effet « règle » : plus la fréquence est fine, plus
  le chemin mesuré est long), donc la convention doit rester constante,
  et les valeurs ne seront jamais comparées à des mesures calculées à
  une autre fréquence.
- Pour une journée : p₀ = cours d'ouverture de la première barre
  observée ; p_t = clôture de la t-ième barre observée (t = 1..n) ;
  H et L = plus haut / plus bas des barres observées (hauts et bas M1).

## 2. Formules (livrable 2)

- Déplacement net : **Δ = p_n − p₀** (et Δ_bp = Δ / p₀ × 10⁴).
- Longueur de chemin : **L = Σ |p_t − p_{t−1}|** sur les minutes
  observées consécutives (voir §5 pour les trous).
- Amplitude : **A = H − L** (A_bp idem).
- **Efficience de trajectoire : ER = |Δ| / L** ∈ [0, 1]. ER = 1 si le
  prix avance sans jamais reculer ; ER → 0 pour un range parfait.
  Non définie si L = 0 (journée parfaitement plate : comptée, publiée).
- **Sinuosité : S = L / A**. Rapport entre le chemin parcouru et
  l'étendue verticale traversée. Non définie si A = 0.
- **Part directionnelle : PD = #{t : signe(p_t − p_{t−1}) = signe(Δ)} /
  #{t : p_t ≠ p_{t−1}}**. Non définie si Δ = 0 ou si aucune minute ne
  bouge ; **inéligible si |Δ_bp| < seuil de déplacement faible (à geler,
  proposé : 5 bp)** — en dessous, le « sens du déplacement net » est un
  artefact de bruit (voir §4).
- **Point médian de parcours** : τ = plus petit t tel que la longueur
  cumulée Σ_{s≤t} |p_s − p_{s−1}| ≥ L/2 ; publié en heure UTC et en
  minutes depuis 00:00.
- **Asymétrie de forme : AS = ER₁ − ER₂**, où ER₁ et ER₂ sont les
  efficiences calculées séparément sur 00:00–11:59 et 12:00–23:59
  (chaque moitié avec son propre Δ et son propre L).

## 3. Redondances et relations mathématiques (à publier, jamais deux « découvertes »)

| Relation | Conséquence de doctrine |
|---|---|
| L/|Δ| = 1/ER exactement | la « sinuosité inverse » classique est **interdite** comme indicateur séparé ; S est définie par L/A précisément pour éviter de présenter une transformation inverse comme une seconde découverte |
| ER = (|Δ|/A) / S | ER, S et le ratio déplacement/amplitude partagent leurs composantes : **une seule variable primaire par comparaison** ; les deux autres peuvent être publiées à titre secondaire, jamais comptées comme confirmations indépendantes |
| PD est mécaniquement lié au signe et à la taille de Δ (les minutes dans le sens dominent d'autant plus que |Δ|/L est grand) | PD n'est variable primaire d'aucune comparaison fondée sur le signe de Δ (voir C6-04) ; il est publié en secondaire |
| ER ∈ [0,1] borné, distribution potentiellement bimodale | inférence par bootstrap percentile (médianes), pas de normalité supposée ; les éventuelles classes (directionnelle/oscillante) exigent des constantes a priori |
| L et A croissent tous deux avec la volatilité du jour | ER et S, ratios, sont sans dimension, mais pas pour autant indépendants du régime d'activité : dépendance traitée explicitement en C6-02 |

## 4. Déplacements nets nuls ou faibles

- Δ = 0 exactement : ER = 0 (valide, publié) ; PD et le signe sont non
  définis ; la journée est exclue des comparaisons par signe et comptée.
- |Δ_bp| < seuil à geler (proposé 5 bp, cohérent avec l'échelle de
  matérialité des campagnes précédentes) : classe **DÉPLACEMENT FAIBLE**,
  exclue des populations « selon le signe » et de PD, conservée pour
  ER/S/τ/AS, effectifs publiés. Aucun zéro de signe n'est imposé.

## 5. Couverture M1 et journées incomplètes (livrable 4)

Héritage C5 (statuts publiés, aucun observable silencieux) :

- Par journée : minutes attendues, observées, taux, premier/dernier
  horodatage, trou maximal, statut COMPLETE / PARTIELLE / EXCLUE selon
  les critères généraux déjà utilisés (bornes 00:10 / 23:50, trou
  > 30 min, taux ≥ 95 % pour COMPLETE).
- **Sensibilité propre à F-G** : un trou fusionne des mouvements en un
  seul saut ; L est alors sous-estimé et ER mécaniquement gonflé. En
  conséquence, le dictionnaire propose (à geler) : éligibilité
  principale si trou maximal ≤ 15 min **et** taux ≥ 90 % ; les journées
  sous ce seuil sont CENSURÉES des grandeurs de forme (pas seulement
  signalées), effectifs publiés par statut. Les contributions d'un saut
  de reprise après trou > 5 min seront marquées (nombre par journée
  publié).
- CONTENUE/absence : aucun statut de couverture ne sera jamais présenté
  comme preuve d'absence d'un mouvement.

## 6. Disponibilité temporelle et prévention des fuites (livrable 5)

- **Toutes les grandeurs F-G sont calculées sur la journée complète :
  elles sont rétrospectives, disponibles uniquement à la clôture de la
  journée (23:59 UTC, disponibilité effective 00:00 le lendemain).**
  ER₁ (première moitié) serait disponible à 12:00, mais AS, ER, S, PD
  et τ (qui dépend de L total) ne le sont qu'à la clôture.
- Aucune grandeur F-G ne peut donc conditionner une lecture « à T0 » le
  jour même ; toute utilisation prospective ultérieure devrait être
  reconstruite sur des fenêtres closes, hors de cette campagne.
- Aucune variable n'utilise d'information postérieure à sa fenêtre :
  la comparaison de persistance (C6-01) n'utilise que la forme du jour
  précédent, close avant l'ouverture du jour courant.
