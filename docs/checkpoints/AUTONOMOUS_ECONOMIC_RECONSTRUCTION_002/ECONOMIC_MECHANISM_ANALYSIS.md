# ANALYSE DU MÉCANISME ÉCONOMIQUE (E1–E4, préenregistrés seq462)

Résultats bruts : `MECHANISM_RESULTS.json` (script `ci_tools/mechanism_lab.py`).
1. **Le signal d'entrée n'a pas d'avantage directionnel mesurable** : après les
   379 entrées simulées V1 de novembre, les retours Mid à 60/300/900 s valent en
   moyenne +0,31/+0,82/+0,14 bp avec 46–52 % de positifs — indiscernable d'un
   hasard directionnel. L'échec économique de V1 ne vient donc pas d'un « mauvais
   sens » mais de la gestion et des coûts.
2. **Les paniers réels longs vivent sous l'eau** : A, B, C passent 81–97 % de leur
   vie sous leur premier prix d'entrée, avec des excursions adverses de −6,7 à
   −18,3 bp, avant de clôturer près du prix moyen pondéré (A/B en gain, C à −6 ¥).
   Le trader accepte un inventaire temporairement perdant et le renforce sur recul.
3. **Un second régime existe** : D et E partent immédiatement favorablement et
   clôturent en 17 s et 87 s. Deux comportements de panier coexistent.
4. **Signature du profil** : espérance affichée par transaction ≈ +6,01 ¥, portée
   par la fréquence (67,4 %) malgré un gain moyen inférieur à la perte moyenne
   (ratio 0,804) — compatible avec de petits gains fréquents compensant un risque
   de queue, dont l'échantillon ne montre aucun exemplaire.

Mécanisme le mieux compatible : **accumulation d'inventaire en excursion adverse
dans un contexte de fond haussier, avec sortie au voisinage du prix moyen, plus un
régime secondaire de scalp immédiat quand le prix part favorablement** — hybride,
pas « martingale aveugle » ni « suivi de tendance ». Statut : STRONGLY_SUPPORTED
à faible n (5 paniers) ; la bio du fournisseur (« trend-following, martingale »)
est une auto-description, pas une preuve — elle est compatible sans être utilisée.
