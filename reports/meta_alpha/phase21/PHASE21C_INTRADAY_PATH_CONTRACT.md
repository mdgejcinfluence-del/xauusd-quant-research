# PHASE 21-C — CONTRAT ANATOMIE INTRAJOURNALIÈRE D1

Statut : `EXPLORATORY_POST_HOC`. Sources : barres H4 certifiées 20-A + journées complètes 21-A
(1 992 journées, 2010-01-04 → 2019-12-16). Ticks non relus ; holdout interdit ; artefacts antérieurs inchangés.

## Conventions causales

Journée = 6 barres H4 (00/04/08/12/16/20 UTC). Information disponible uniquement à la clôture de chaque barre.
Le range final D1 ne sert que de dénominateur descriptif rétrospectif, jamais d'état causal.

À chaque clôture k : `CUMULATIVE_RANGE_BP = 10000×ln(cumHigh/cumLow)` ;
`PARTIAL_BODY_BP = 10000×ln(close_k/open_D1)` ; extensions = variation log-bp de l'extrême cumulé
(référence initiale = open D1), 0 si pas d'extension. Ordre intra-barre High/Low inconnu (OHLC H4).

## Familles

- Anatomie par tranche (descriptif) : range cumulé, fraction du range final, extensions High/Low.
- Premiers passages 30/60/100 bp (repères descriptifs) : première clôture où le range cumulé atteint le seuil ;
  comportement jusqu'à la clôture D1 (range additionnel, extensions, terminal, excursions).
- Nouveaux extrêmes par clôture (High/Low/les deux/aucun), comportement sur 1–3 barres restantes dans la journée.
- Direction partielle (signe du PARTIAL_BODY) conditionnelle au premier passage 30/60/100 bp.

## Inférence préenregistrée (14 tests)

Bootstrap par grappes de semaines ISO, 10 000 réplications, graine 2113, p percentile bilatérale, BH q=0,05 :
(1) événements slots 2–5 : NEW_HIGH vs AUCUN, NEW_LOW vs AUCUN, NEW_HIGH vs NEW_LOW × {terminal futur signé,
excursion future haute, excursion future basse} = 9 ; (2) premier passage 60 et 100 bp : PARTIAL_POSITIVE vs
PARTIAL_NEGATIVE × {terminal aligné, asymétrie favorable−adverse} = 4 ; (3) passage 60 bp précoce (slot ≤2) vs
tardif (slot ≥4) : range additionnel = 1. Minima 50 événements / 20 semaines ISO sinon `NON_EVALUABLE_INFERENTIAL`.
Références 4,0/4,5 bp = `REFERENCE_COST_UNVERIFIED`, couvertures descriptives. Aucun P&L, aucun signal.
