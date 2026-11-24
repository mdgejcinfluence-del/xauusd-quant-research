# MA-EDGE-02 — AUDIT TECHNIQUE DU CONTRAT « DEADLINE 120 MIN » (règle gelée seq407)

Audit point par point. La règle n'est **pas modifiée** ; seuls des points d'exécution ambigus
sont clarifiés (registre seq409), toujours dans le sens le plus strict.

1. **Déclenchement** : événement = réintégration M15 détectée par la procédure 24-B reproduite
   (`ci_tools/edge02_shadow.py::detecter`) : impulsion |corps| ≥ Q90 des 250 barres précédentes,
   clôture confirmant le déplacement, puis première clôture strictement de l'autre côté de P0 ;
   t_decision = clôture de la barre de réintégration. Score M15_TIME_ONLY (coefficients 24-C
   committés) **strictement** supérieur à 0,560955 → sélection. Causalité : n'utilise que des
   barres closes et les quatre variables connues à t_decision. ✅ sans fuite.
2. **Confirmation** (clarifié) : une clôture M15, postérieure à t_decision et dont l'instant de
   clôture est **≤ t_decision + 120 min**, strictement au-delà du niveau de référence favorable
   gelé (meilleur niveau de clôture favorable atteint avant la réintégration, sens de l'événement).
   C'est exactement la première réalisation du label 24-B restreinte à l'échéance.
3. **Invalidation** : la clôture au-delà de l'extrême adverse (définition 24-B) **ne déclenche
   aucune sortie** dans la règle comme dans la référence ; elle n'intervient que dans la
   comptabilité descriptive. Aucun stop caché n'existe.
4. **Réalisation après l'échéance** : sans effet — la position simulée est déjà liquidée à
   l'échéance ; l'événement reste classé « non confirmé à l'échéance ».
5. **Prix d'exécution** : entrée = premier tick réel strictement après t_decision (Ask LONG /
   Bid SHORT), fenêtre 60 s sinon `NON_EXECUTION` (événement compté, exclu de la paire
   économique, jamais de prix fictif). Sorties : premier tick strictement après l'instant visé,
   fenêtre 60 s, sinon `EXIT_NONEXECUTABLE` (compté et rapporté ; paire exclue de l'analyse
   principale, taux d'exclusion publié).
6. **Censure et trous de données** : si aucune cotation n'existe dans une fenêtre d'exécution,
   ou si une barre M15 de la fenêtre [t_decision, échéance] est sans tick (marché fermé exclu :
   week-ends et jours fériés Dukascopy), l'événement est marqué `DONNEES_INSUFFISANTES`,
   exclu de l'analyse appariée principale, **compté et listé**. Une barre incomplète en fin de
   collecte donne `CENSURE_FENETRE`, comme en 24-B.
7. **Événements qui confirment** : ils suivent la sortie de référence (t_decision + 480 min) dans
   les deux bras — contribution identique, différence appariée nulle par construction ; ils sont
   conservés dans la population (les exclure biaiserait la comparaison en faveur de la règle).
8. **Appariement et dépendance** : différence par événement (règle − référence), bootstrap par
   grappes = composantes connexes de fenêtres [t0, t0+8h) qui se chevauchent (définition 24-B),
   10 000 tirages, graine 2129 (contrat SHADOW). Succès = espérance de la règle > référence **et**
   borne inférieure IC95 de la différence > 0. Aucune ré-estimation de la taille d'échantillon
   après observation des résultats ; le suivi est continu, l'évaluation suit ce protocole.
9. **Départ prospectif (correction importante)** : le préenregistrement seq407 est devenu public
   au commit du **2026-11-24T17:12:57Z**. Les événements entre la fin du holdout
   (2026-09-30T23:59:58.864Z) et cet instant **ne sont pas** une validation prospective : ils sont
   interdits pour l'évaluation de la règle (au plus, exploration documentée). Le pipeline verrouille
   `DEPART_PROSPECTIF = 2026-11-24T17:12:57Z`.
10. **S0/S1/S2** : comptabilité 19-B inchangée (spread une fois via Bid/Ask réels, S2 principal,
    commissions exclues, nommage hypothétique complet).

Conclusion d'audit : la règle est exécutable en temps réel sans ambiguïté après ces
clarifications ; le code `edge02_shadow.py` les implémente et l'auto-test synthétique passe
(détection, entrée ≤ 60 s, sortie deadline, déduplication idempotente).
