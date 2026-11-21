# CAMPAGNE 4 — QUALITÉ DES DONNÉES, INCIDENTS ET LIMITES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Couverture

| Contrôle | Résultat |
|---|---|
| Partitions chargées / attendues | **282 / 282** (garde d'intégrité satisfaite) |
| Barres M1 reconstituées | 3 540 993 (recoupement exact avec les campagnes 2.3/3) |
| Journées présentes / utilisables (≥ 300 barres) | 3 097 / **2 572** (525 sous le seuil de qualité, exclues des mesures et comptées) — 2 572 est aussi le nombre de journées du fichier F3 gelé, recoupement publié |
| Journées classées | État courant 2 532 (amorçage causal 40 journées) ; tercile causal F3 2 011 (amorçage des prédictions ≈ 500 journées + fenêtre de terciles) ; NON_CLASSE publiés partout |
| Épisodes / transitions | 1 281 épisodes ; 1 280 transitions d'épisodes cataloguées (286 confirmées, 994 non confirmées) ; aucun suppression |
| Bootstrap | Blocs mobiles de 20 journées, 2 000 réplicats, **2 000 valides pour chacune des dix comparaisons, 0 exclu** — le poste de calcul redouté au PV (recalcul complet par réplicat) a tenu (≈ 19 min de synthèse locale), aucune dégradation méthodologique n'a été nécessaire |

## Incidents d'exécution

1. **Premier run CI (44884286806)** : échec du moteur à
   l'`AttributeError` — `Ju.skew` désigne la méthode pandas et non la
   colonne d'asymétrie. Correctif d'implémentation (`Ju['skew']`, idem
   synthèse), définitions inchangées, tests temporels reverdits, second
   run (44884486846, commit `d8d42c8`) propre. Aucun résultat n'avait été
   produit ni consulté avant le correctif.
2. **Seuil matériel de C4-02/C4-10** : premier passage de la synthèse avec
   un seuil de 0,05 (unité des proportions) sur des statistiques exprimées
   en points (×100) ; corrigé en 5 points conformément au gel, avec
   statistiques et intervalles inchangés (seule la lecture de C4-10 passe
   en « significative sous le seuil matériel »). Consigné dans la
   cartographie §4 et ici.
3. Récupération CI par commit du runner (patron campagne 3, bruts gzip) :
   aucun incident cette fois.

## Limites méthodologiques publiées

- **Granularité des durées** : durées d'épisodes en journées entières,
  médianes de 1–2 jours ; les intervalles de C4-03 sont discrets et larges
  ([0,50 ; 2,00]) — publiés tels quels.
- **Fenêtres post-transition fragiles** : la troncature à la prochaine
  candidate (règle gelée) ne laisse que 9 et 5 fenêtres exploitables pour
  C4-01/C4-06 ; ces comparaisons sont publiées non éligibles plutôt
  qu'élargies après coup. Toute fenêtre plus tolérante serait une nouvelle
  campagne préenregistrée.
- **États relatifs** : les terciles roulants décrivent une position dans
  les 60 journées précédentes, pas un niveau absolu ; RV absolue et
  log-ratio sont publiés dans les bruts quotidiens pour empêcher la
  confusion (dictionnaire §3).
- **C4-08 contemporaine** : l'état courant est connu à la clôture du jour
  qu'il conditionne ; l'association est publiée sans antériorité et ne
  peut fonder aucun conditionnement à l'ouverture.
- **C4-09 largement mécanique** : voir l'avertissement de la fiche
  ANO-C4-002.
- Échelle journalière uniquement : la campagne ne dit rien d'échelles plus
  lentes (hebdomadaires/mensuelles), non autorisées dans le dictionnaire.

## Périmètres interdits — état

Holdout / post-2020 : non accédé. Flux prospectif T0 : inexistant, non
utilisé, chantier inactif. FRED : suspendue. Budgets de trading : aucune
consommation (tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 ·
P9 10/12, inchangés). 36 cellules S12 : intactes. Fiches des campagnes
0 à 3 : non modifiées ; sensibilité ANO-C2-003/006/008/012 : non
recalculée, conformément à l'ordre.
