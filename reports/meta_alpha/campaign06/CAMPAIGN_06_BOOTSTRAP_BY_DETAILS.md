# CAMPAGNE 6 — DÉTAILS DES CONTRÔLES BOOTSTRAP ET BY

- Bootstrap : 2 000 réplicats, graine 20261113, percentile 95 %,
  rééchantillonnage par grappes (grappe-journée pour C6-02..05 ;
  grappe-semaine civile du jour j pour C6-01). Effets : différences de
  médianes (ER sans unité ; τ en minutes). p bootstrap bilatérales,
  plancher 1/2 000.
- BY : famille F-G préenregistrée de cinq, **m = 5 fixe**, H₅ =
  2,283333 ; q₍ᵣ₎ = min_{s≥r}(5·H₅·p₍ₛ₎/s) plafonnée à 1, rangs sur les
  p calculables ; aucune imputation. Les cinq p étant calculables,
  aucune q NaN dans cette campagne. Recalcul de contrôle effectué à la
  synthèse : q publiées C6-01 1,000 ; C6-02 0,0057 ; C6-03 1,000 ;
  C6-04 1,000 ; C6-05 0,588.
- C6-01, contrôle par blocs mobiles de deux semaines : 498 blocs,
  2 000 réplicats, **0 invalide (0 %)** ; IC blocs [−0,0227 ; +0,0247]
  contre IC hebdomadaire [−0,0220 ; +0,0215] ; effet ponctuel identique
  −0,0007. Statut selon la priorité gelée V1.2.1 : CONTRÔLE_INDÉTERMINÉ
  écarté (498 ≥ 30 blocs, 0 % d'invalides, e ≠ 0) ; IC blocs contenant
  0 ⇒ **FRAGILE_SIGNE** (pas d'inversion : drapeau INVERSION_CONTRÔLE
  faux). Lecture hebdomadaire déjà NON_ELIGIBLE (bras A : 10 paires,
  10 semaines ; bras B : 2 137 paires, 498 semaines) ⇒ aucun
  déclassement supplémentaire (règle : lecture inchangée si déjà
  négative ou non éligible). Aucune p-value créée par le contrôle.
- C6-02, déclassement : conditions gelées évaluées — q < 0,05 vrai,
  |ΔER| ≥ 0,05 **faux** (+0,0208) ⇒ déclassement non déclenché, publié
  pour traçabilité. Décomposition (sans p ni q) : ln-ratio |Δ_seg|/A
  +0,553 ; ln-ratio S −0,326 ; borne ln(1,15) = 0,1398.
- Éligibilité : C6-01 non éligible (10 < 200 dans le bras A) ; les
  quatre autres comparaisons satisfont ≥200 journées et ≥100 grappes
  par bras (détail au tableau du rapport).
