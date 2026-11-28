# EXPANSION-001 — Audit de prévision, campagne par année civile, diagnostic des échecs

## Axe 1 — Audit de la baseline de volatilité (927 prévisions réelles)

| Mesure | Glissant (notre modèle) | Référence inconditionnelle |
|---|---|---|
| Couverture q10–q90 (cible 80 %) | **79,6 %** | 79,0 % |
| Largeur moyenne d'intervalle | **18,88 bp** | 20,43 bp |
| Couverture en régime calme / moyen / agité | 77,5 / 79,1 / 82,4 % | 80,1 / 77,1 / 79,5 % |

Verdict d'audit : baseline **calibrée mais à peine meilleure que la
référence naïve** (+0,6 point de couverture, intervalles 8 % plus
étroits). La couverture n'est ni une précision directionnelle, ni une
utilité économique, ni une rentabilité — c'est un instrument de mesure
du risque de volatilité, qualifié comme tel (PARTIELLEMENT QUALIFIÉ).

## Axe 2 — Campagne indépendante n°2 (CI, 33 partitions, 136 M ticks, 2010–2026)

Échantillonnage par année civile (2 partitions/an), segments gelés seq514 :

| Famille | Découverte | Validation | Confirmation | Statut |
|---|---|---|---|---|
| Activité (ticks/barre) → volatilité suivante | forte 5,40 vs faible 2,41 bp | 4,96 / 2,15 | 6,51 / 2,48 | **INVARIANTE (ratio ≈ 2,3× partout)** — même fait que la persistance, vu par l'activité |
| Rafale de volatilité → amplitude suivante | 6,39 vs base 3,76 | 5,82 / 3,39 | 8,13 / 4,19 | invariante : la volatilité élevée persiste à court terme |
| 3 barres de même signe → rendement suivant | −0,16 / +0,40 bp | −0,14 / +0,23 | 0,00 / +0,05 | **aucune continuation ni réversion directionnelle** après séquences |

## Axe 3 — Diagnostic des échecs appliqué (taxonomie codée `ere/diagnosis.py`)

- Asymétrie de volatilité (réfutée deux fois) : mode **G** (non
  reproductible, signe instable) → l'expérience suivante n'est pas un
  nouveau seuil mais une réplication par année — faite ici, famille close.
- Réversion après extrême 1 min (51–55 % au Mid) : mode **B/H en
  attente** — effet trop faible pour être distingué des coûts sans
  mesure exécutable Bid/Ask dédiée ; ne pas conclure à l'absence.
- Persistance de volatilité : ce n'est pas un échec mais une signature
  de régime sans direction — toute tentative de la trader
  directionnellement serait un mode **F** (hypothèse mal formulée).

## Axes 4–6 — Sélection adaptative et continuité

La priorisation du noyau combine désormais : valeur informative
(hypothèses départagées), coût, segment disponible, **et diagnostic du
dernier échec** (un mode G impose une réplication avant toute nouvelle
exploration de la même famille ; un mode H impose une géométrie à plus
grande marge). La reprise, l'idempotence et la détection de doublons
sont celles du noyau (28 tests + 3 nouveaux, 31/31). Limite inchangée
et documentée : pas d'ordonnanceur permanent dans l'environnement —
la continuité passe par Git + le journal du noyau, reprises en session.

## Matrice de qualification

| Capacité | Statut |
|---|---|
| Prévision probabiliste de volatilité | PARTIELLEMENT QUALIFIÉE (calibrée, gain marginal sur le naïf) |
| Découverte de structures sur corpus | QUALIFIÉE (2 campagnes CI reproductibles, 155 M ticks cumulés) |
| Diagnostic des échecs A–H | QUALIFIÉ (codé, testé, appliqué) |
| Sélection autonome des recherches | PARTIELLEMENT QUALIFIÉE (règles + diagnostic ; pas d'apprentissage du score) |
| Mécanisme économique N5+ / stratégie | NON QUALIFIÉ — aucun candidat ne survit aux coûts et segments |
| Autonomie continue sans session | NON QUALIFIÉE (pas d'ordonnanceur) |

**Conclusion stricte :** les résultats synthétiques (tests), réels
(campagnes CI, audit de prévision) et les conclusions sont séparés
ci-dessus ; la structure invariante du marché échantillonné reste la
persistance conjointe activité-volatilité, sans contenu directionnel
exploitable démontré à ce jour.
