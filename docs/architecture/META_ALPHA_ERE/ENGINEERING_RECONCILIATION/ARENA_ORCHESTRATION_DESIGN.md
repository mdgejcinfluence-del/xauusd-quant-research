# RÉCONCILIATION — CONCEPTION DE L'ORCHESTRATION ARENA

## Réel [DÉPÔT] — ce qu'ARENA est ici, vérifié

L'agent opère **en session** dans l'environnement Arena : il lit et
écrit le dépôt, lance des commandes, dispatche la CI via `gh`
(workflow unique `phase10_all.yml`, entrées booléennes réutilisées —
limite réelle rencontrée : 25 entrées maximum par workflow), lit les
journaux et présente les résultats au fondateur. **Il n'existe aucune
API ARENA, aucun service persistant, aucun dispatch programmatique
garanti entre les sessions.** Le dossier externe [EXT] suppose par
endroits un « adaptateur ARENA » et des commandes typées : c'est une
hypothèse de conception [NV], pas une capacité.

## Conception réconciliée

- **ARENA = superviseur scientifique en session.** Il formule les
  questions, écrit les protocoles, préenregistre (registre chaîné),
  dispatche, vérifie les preuves, propose les verdicts. Il ne détient
  aucun état critique : tout ce qui compte est committé (protocoles,
  registre, journaux, objets) — un dossier se reprend depuis le dépôt
  seul (`DossierState`, Correction 6 d'ERE-REVIEW-002).
- **Le déterminisme vit dans la CI, pas dans la conversation.** Les
  jobs sont idempotents, relançables, et committent leurs résultats
  avec boucle pull-rebase/push ; la collecte prospective quotidienne
  fonctionne déjà sans session ouverte (schedule + job `me001prosp`).
- **Machine à états : celle des missions, pas un nouveau système.**
  États pratiqués : PRÉENREGISTRÉ → EN_COURS(CI) → RÉSULTATS →
  CHECKPOINT_VÉRIFIÉ. Toute machine à états de tâches plus riche ne
  sera conçue que si plusieurs exécutions concurrentes le justifient.
- **Approbations** : le fondateur approuve dans la conversation ou par
  décision journalisée ; une approbation vaut pour un tuple précis
  (modèle, protocole, budget, données, expiration) — reprise de la
  règle externe du gate H, compatible avec notre journal des décisions.

## Ce qu'il ne faut pas construire

Un « contrôleur ARENA » autonome permanent, des files d'attente, ou
toute automatisation qui déciderait seule d'ouvrir un segment de
validation ou d'activer la porte H : la gouvernance réserve ces actes
au fondateur, et l'environnement ne fournit de toute façon aucun
substrat persistant pour les porter.
