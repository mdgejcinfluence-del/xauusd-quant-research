# CAMPAGNE 7 — REGISTRE DES INCIDENTS ET LIMITES

## Incidents (tous détectés avant publication, aucun résultat invalide publié)
1. **Run CI 44903810557 (run 1) — marquage SIMULTANÉ erroné.** La
   première implémentation marquait « simultané » toute barre de
   contact traversant une borne de grille, ce qui excluait à tort la
   quasi-totalité des épisodes G50 et R100 (approches résolues tombées
   à 0 pour ces grilles, visible immédiatement dans le tableau de
   synthèse). La définition gelée exige **deux niveaux réels distincts**
   dans la barre. Correctif du code (aucune définition modifiée), test
   synthétique ajouté (13/13), run corrigé 44906521704 : simultanés
   2 037 → 95, approches résolues G50 0 → 1 302. **Aucune sortie du
   run 1 n'a été utilisée** ; les épisodes des autres grilles du run 1
   ne sont pas davantage repris (régénération intégrale).
2. **Synthèse — statut de composition confondu avec ses détails.** Une
   première passe de synthèse stockait le dictionnaire de détails du
   contrôle de composition à la place du statut (chaîne), neutralisant
   le déclassement gelé d'I-03. Détecté à la relecture du tableau
   (lecture CANDIDATE incompatible avec la composition sensible),
   corrigé, synthèse relancée séquentiellement : I-03 déclassée en
   ASSOCIATION_SENSIBLE_A_LA_COMPOSITION, I-02 en
   NON_EVALUABLE_COMPOSITION. Aucune p/q n'a été affectée (le contrôle
   ne crée ni ne modifie de p-value).
3. **Synthèse lente (bootstrap I-05 en recherches par étiquettes)** :
   remplacée par un bootstrap sur sommes par grappe-journée
   mathématiquement identique (mêmes grappes, même graine ajoutée en
   tête de flux — les tirages diffèrent donc de la passe lente abandonnée,
   sans aucune conséquence méthodologique, la passe lente n'ayant produit
   aucun résultat publié). Durées : extraction ~2,5 min par run,
   synthèse finale quelques secondes à ~15 min selon les passes.
4. Deux relances d'outils ont été lancées en parallèle d'éditions du
   même fichier (course déjà rencontrée en Campagne 5) ; systématiquement
   détectées par relecture (hash/contenu) et relancées en séquentiel.
   Aucun impact sur les sorties finales.

## Limites
- Bande d'approche gelée de 25 bp : très étroite — ~90 % des approches
  franchissent, les taux sont donc comprimés vers le haut et les écarts
  détectables sont mécaniquement limités. C'est un choix gelé, publié,
  non révisable dans cette campagne.
- Censures de fin de journée massives (12 657 épisodes) : les épisodes
  tardifs sont structurellement non résolus en fenêtre UTC.
- I-02 et I-05 non évaluables pour composition : les strates
  ère×session×sens des touches et de l'ère récente sont trop fines
  pour les effectifs disponibles ; déclaré sans fusion de strates.
- Placebos R100 (quart de pas) et P10 : descriptifs uniquement, jamais
  présentés comme l'expérience appariée de G50 (protocole gelé).
- Un comportement au contact ne démontre aucun mécanisme
  « psychologique » (limite C10 du protocole) ; rien ici n'est une
  preuve de capturabilité.

## Coûts et budgets
Deux runs GitHub Actions (incident du run 1 inclus) + synthèses
locales ; coût financier 0 FCFA ; aucun budget expérimental consommé
(compteurs inchangés : tick 148/150, panel 28/60, exo 6/60, P7 0/24,
NR 0/24, P9 10/12). Holdout scellé non accédé ; aucun secret exposé ;
fiches historiques non modifiées ; coquille cosmétique du protocole
gelé laissée intacte conformément à l'ordre du propriétaire.
