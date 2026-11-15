# RAPPORT D'AUDIT SCIENTIFIQUE — phénomènes IS (avant toute nouvelle vague)

Exécution: run 43688191819, succès 1 h 57, 282/282 partitions IS (288M ticks),
descriptif seul, aucun Holdout, résultats initiaux conservés (PARTITION_PHENOMENA.csv
non réécrit; mesures d'audit dans audit/PARTITION_AUDIT.csv).

## 1. Audit de l'autocorrélation signée lag-1 (~0,49) — RÉSOLU comme suit
- Tri observation_id vs tri timestamp: **identiques** (écart max 0,0 sur 282 partitions).
- Timestamps dupliqués: ~0 groupe par partition. Rendements nuls: 1,25% (ne peut pas
  créer l'effet; autocorrélation hors zéros = 0,489, inchangée).
- Alignement/formule: rendement mid consécutif standard, vérifié sur les deux tris.
- Structure par retards: lag1 +0,487; lag2 -0,087; lag5 -0,055; lag10 ~0.
- Conclusion: l'effet est RÉEL dans les rendements du mid, mais sa signature
  (un seul lag positif puis extinction) désigne un mécanisme de **construction du mid**:
  bid et ask se mettent à jour séparément, un déplacement de cotation apparaît donc
  en deux demi-pas de même signe dans (bid+ask)/2. Ce n'est ni une erreur de tri ni,
  à ce stade, un phénomène exécutable: les prix Bid/Ask traitables ne contiennent pas
  ce demi-pas mécanique. Enregistré **ANOM-001, statut OBSERVATION À VÉRIFIER**:
  la vérification directe (décomposition bid-only/ask-only des paires consécutives)
  reste à faire avant toute interprétation plus forte.

## 2. Autres phénomènes approfondis
- **Regroupement de volatilité**: autocorrélation des |rendements| 0,457 (lag1),
  0,184 (lag5), 0,132 (lag20): persistance décroissante, stable en médiane.
  -> **ANOM-002, DESCRIPTIF DOCUMENTÉ** (phénomène connu; rien de prédictif démontré).
- **Mouvements après gaps**: effet concentré sur les longues interruptions
  (> 3600 s: |rendement| médian ~5 bp); les gaps courts (60-300 s) montrent une
  médiane ~0 (réouverture souvent à cotation inchangée). -> descriptif, pas d'item K
  à ce stade (mesure à affiner par durée et par session avant qualification).
- **Sauts**: >3 bp: ~1,6/10k ticks; >10 bp: quasi absents; part positive ~50%
  (symétriques); continuation au tick suivant ~0,0. -> aucun phénomène directionnel
  descriptif détecté après saut; résultat négatif conservé.
- **Spread post-saut**: retour aux niveaux normaux dès +1 à +5 ticks en médiane
  (4,0 bp constants). -> élargissement bref, pas d'item K sans mesure de durée fine.

## 3. Sélection cumulative — avertissement permanent
Ces observations proviennent d'explorations successives sur le MÊME IS (P3-001,
P3-002, phénoménologie, audit): leur valeur est descriptive et générative
d'hypothèses, jamais probante. Toute hypothèse née d'ici devra être confirmée sur
l'OOS intact, puis le Holdout scellé en phase finale. Compteur cumulatif: 148 tests.

## 4. Suite autorisée (pas encore d'hypothèses)
1. Vérification du mécanisme d'ANOM-001 (décomposition bid/ask) — descriptif.
2. Affinage gaps par durée/session documentée (sans inventer les sessions).
3. Seulement ensuite: formulation d'hypothèses citées (K/ANOM), préenregistrement,
   verrouillage, test. Aucune vague P3-003 n'est lancée par ce rapport.
