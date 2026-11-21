# CAMPAGNE 4 — NOTE DOCUMENTAIRE DE CLÔTURE : TRANSITIONS CENSURÉES À DROITE

**DESCRIPTIF — NOTE DOCUMENTAIRE, AUCUN CALCUL, AUCUNE DONNÉE SOURCE
MODIFIÉE.** Ajout postérieur au rapport historique (seq 202) et à son
complément (seq 204), qui sont tous deux conservés inchangés. La présente
note fait foi, à compter de ce jour, pour la lecture du compte des
transitions dans tous les documents de synthèse de la campagne 4.

## Détail faisant foi

Le total des transitions non confirmées publié (994) **inclut** l'unique
transition censurée à droite identifiée au complément seq 204 : la
transition HAUT → BAS candidate le **2019-12-16**, dernier jour du corpus,
dont la confirmation était impossible à observer (persistance observable
d'un jour, corpus terminé au soir du 2019-12-16). Elle ne doit pas être
lue comme une transition réellement non confirmée (rechute observée) :
son motif est une **censure d'observation**, non un comportement du
marché.

Le détail à présenter désormais, partout où le compte est cité :

| Catégorie de transition (entre épisodes consécutifs) | Nombre |
|---|---|
| Confirmées (persistance ≥ 3 journées observée) | **286** |
| Réellement non confirmées (rechute observée avant 3 journées) | **993** |
| Censurée à droite (fin de corpus, confirmation inobservable) | **1** |
| **Total des transitions entre les 1 281 épisodes** | **1 280** |

Symétriquement, aucune transition n'est censurée à gauche : la chaîne des
états commence après l'amorçage causal (indice 40, 2010-03-01) et la
première transition entrante du premier épisode n'existe pas par
construction d'une chaîne — ce cas est distinct d'une censure et n'affecte
que le premier épisode. Les durées d'épisodes censurées aux deux bords
(premier et dernier épisodes) restent exclues des médianes de durées et
comptées, comme déjà appliqué dans les sorties (`censure_bord`).

Le catalogue `CAMPAIGN_04_TRANSITIONS.csv` n'est pas modifié : la ligne du
2019-12-16 y figure avec `confirmee = False`, `persistance = 1`, et se
reconnaît sans ambiguïté comme l'unique candidate datée du dernier jour
du corpus ; la présente note lui attache son motif.
