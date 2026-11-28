# GO-LIVE-001 — Premier cycle de recherche autonome continue (seq521–522)

Missions chargées : M-877d24f6dc927e1a (flux B, marché) et
M-47e5ea8298d96be9 (flux A, trader), toutes deux OPEN. Aucun accès
ME-001, `main` inchangée, `profitable_edge=False` partout.

## Flux A — Trader Intelligence
Portefeuille construit depuis le dossier réel (`FLUX_A_PORTFOLIO.json`) :
6 lignes, 3 épisodes × 2 positions simultanées, tous Buy, prix absents,
fuseau UNKNOWN, niveau N2 NOT_IDENTIFIED. Hypothèses concurrentes TA-1
(entrées groupées), TA-2 (sorties rapides asymétriques), TA-3
(dépendance au régime), TA-NULLE (échantillon insuffisant). Aucune
donnée inventée ; la pièce qui rouvrirait l'identification reste :
fuseau documenté ou export prix+identifiants. Statut : **PARTIEL** —
investigation maintenue ouverte, non abandonnée.

## Flux B — Campagne corpus (protocole gelé seq521, familles nouvelles)
Runs CI : `46130401839` (premier passage), reprises idempotentes
`46130799899`→`46132628875`. Résultat d'infrastructure : 12/34 partitions
OK (découverte complète, 22,36 M ticks, 2010–2015) ; 22 partitions
**UNAVAILABLE** — Drive a renvoyé des interstitiels de 2 040 octets au
lieu des Parquet (~150 Mo attendus) après les téléchargements lourds du
jour ; les mêmes partitions avaient réussi le matin même (INTEL3,
seq515). Cause classée : quota/rate-limit Drive transitoire, pas un
défaut de données. Trois défauts réels du script ont été trouvés et
corrigés en cours de campagne (définition manquante, troncatures non
détectées, écriture non incrémentale) — voir l'historique Git et
`CAMPAIGN_LOG.txt`. La reprise ne retraite que les partitions
manquantes et sera relancée après reset du quota ; aucun verdict
inter-segments n'est tiré d'un segment absent.

### Résultats découverte (EXPLORATOIRES, segment unique — aucune qualification)
- Post-impulsion 5 min (|ret| ≥ d90, 7 489 impulsions) : continuation
  médiane **−0,25 bp**, positive dans 3/12 partitions → lueur de
  réversion post-impulsion, **non validée** (validation/confirmation
  manquantes). À départager au prochain cycle.
- Volatilité après impulsion 6,06 vs 3,84 bp de base : cohérent avec la
  persistance connue (signature de régime, pas une direction).
- Représentation : range intra-1 min (4,91/2,68) ≈ clôture (4,75/2,98)
  pour prédire la volatilité suivante → le range n'apporte pas de gain
  de représentation mesurable sur ce test.
- Transitions de régime : P(agité|agité) 0,445 vs P(agité|calme) 0,250
  → persistance d'état, même famille que le clustering connu.

## Prochain cycle (sélection automatique)
1. Relancer la reprise GO-LIVE-001 (22 partitions) après reset quota
   Drive ; verdict par segments gelés ensuite, sans changer le protocole.
2. Si la réversion post-impulsion survit à la validation : expérience
   discriminante au Bid/Ask (exécutabilité, mode B/H du diagnostic).
3. Flux A : attente documentée de la pièce d'identification ; aucune
   relance artificielle.

## Statuts
Flux A PARTIEL · Flux B PARTIEL (découverte exploratoire) · Endurance
72 h BLOQUÉ PAR AUTORISATION (cron sur `main`) · Aucun modèle VALIDATED.
