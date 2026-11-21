# CAMPAGNE 5 — RAPPORT FAMILLE F-E (événements d'ouverture de session)

**Statut : EXÉCUTION DESCRIPTIVE TERMINÉE** selon le protocole V2
(sha256 `818837fd…8331`) + addendum V2.1 (`509a2863…bd45`) + addendum V2.2
(`4ce1ee9b…1b0e`), gel chaîné seq221 avant toute extraction. Aucune
définition, fenêtre, population, seuil ou méthode n'a été modifié après
le début de l'exécution. Aucun assouplissement pour augmenter les effectifs.

Méthode : bootstrap par grappes-journées, 2 000 réplicats, graine
20261113 ; correction BY séparée par famille (F-E : 4 p calculables,
C5-03 non testable, q publié NaN) ; matérialité ratio 1,15 symétrique
ou 5 points de pourcentage ; éligibilité ≥200 épisodes et ≥100 grappes
par bras. Corpus : 282/282 partitions, 3 540 993 barres M1, 10 288
lignes d'ouvertures (4 sessions × 2 572 journées utilisables), 9 190
ouvertures éligibles (1 098 inéligibles, publiées).

## Résultats

| ID | Comparaison | Effet | IC 95 % | p brute | q BY (F-E) | n A/B | Lecture |
|---|---|---|---|---|---|---|---|
| C5-01 | Amplitude 30 min LONDRES vs ASIE (médianes 15,34 vs 12,90 bp) | ratio 1,189 | [1,148 ; 1,236] | 0,0005 | 0,0042 | 2 570 / 2 566 | **CANDIDATE_J1** (ANO-C5-001) |
| C5-02 | P(poursuite +30 min) NEWYORK vs LONDRES (61,5 % vs 59,2 %) | +2,24 pts | [−0,45 ; +4,89] | 0,101 | 0,281 | 2 565 / 2 569 | NÉGATIF |
| C5-03 | Amplitude 1re heure Asie, CONTINUITE vs TROU_INTRA_SEMAINE | non calculable | — | — | — | 2 565 / **0 éligible** | **NON ÉLIGIBLE** |
| C5-04 | Amplitude 30 min Londres, lundi vs vendredi (14,27 vs 15,66 bp) | ratio 0,912 | [0,857 ; 1,000] | 0,052 | 0,217 | 513 / 508 | NÉGATIF |
| C5-05 | Spread médian 15 min NEWYORK vs LONDRES (2,243 vs 2,239 bp) | ratio 1,002 | [0,990 ; 1,014] | 0,726 | 1,000 | 2 566 / 2 569 | NÉGATIF |

## Détails de publication exigés par le gel

- **C5-01** : fenêtres 30 min COMPLETE 8 336 / PARTIELLE 198 / CENSUREE
  656 (éligibles) ; part de PARTIELLE dans les bras utilisés : ASIE
  1,36 %, LONDRES 0,35 % — aucun bras ne repose majoritairement sur du
  partiel, pas d'avertissement. Candidate J1 au catalogue commun, sans
  promotion automatique, sans priorité.
- **C5-02** : dénominateurs après exclusion gelée — mouvement
  pré-ouverture nul : 3 (MOUVEMENT_NUL, hors dénominateur) ; issues
  CENSURE : 275. Ventilation +30 min publiée : NEWYORK POURSUITE_SEULE
  659 / RETOURNEMENT_SEUL 644 / LES_DEUX 918 / AUCUN 344 ; LONDRES
  724 / 677 / 798 / 370. L'effet (+2,2 pts) est sous le seuil matériel
  de 5 points et non significatif après BY.
- **C5-03** : population initiale TROU_INTRA_SEMAINE = 2 journées
  (2012-06-13, trou 359 min ; 2015-07-01, trou 224 min) ; les deux
  ouvertures d'Asie correspondantes sont inéligibles au titre du retard
  (180 et 45 min, classe INELIGIBLE selon les règles gelées). Bras B =
  0 éligible : comparaison **déclarée non éligible telle quelle**, aucun
  assouplissement appliqué. REOUVERTURE_SEMAINE (1) et
  FERMETURE_EXCEPTIONNELLE (1) publiées à part, jamais dans le contraste.
- **C5-04** : effet inverse du sens suggéré par l'intuition de début de
  semaine (lundis plus calmes), IC incluant 1,000 à la borne supérieure
  (1,0004) ; négatif au seuil gelé, publié tel quel.
- **C5-05** : spreads médians quasi identiques ; le spread reste un
  contexte descriptif, jamais un coût de transaction.

Aucune association descriptive de ce rapport n'est une preuve prédictive
ni une opportunité exploitable. Aucun J2/J3 automatique.
