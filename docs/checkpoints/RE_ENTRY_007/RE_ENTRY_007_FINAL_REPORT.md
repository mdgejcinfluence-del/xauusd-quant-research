# RE-ENTRY-007 — RAPPORT CONSOLIDÉ (intégration du nouveau snapshot annoncé)

Branche de travail : `arena/afe12737-xauusd-quant-research` (branche de session
imposée ; la branche dédiée demandée n'a pas été créée, règle de session prioritaire —
écart documenté, `main` intacte). Références gelées revérifiées : V1/V2 intouchés,
matching corrigé seq448, H3/F2 et leurs falsifications inchangés.

## 1. Fichier annoncé : obstacle documenté
`myHF _ HFM Broker.html78.html` a été recherché dans tout l'espace de travail et dans
Google Drive connecté : **0 résultat**. Il n'a donc pas pu être examiné intégralement
ni haché — le prétendre serait faux. L'audit a été exécuté sur les preuves
équivalentes disponibles : les 3 snapshots immuables RE-ENTRY-003
(`snapshot_2026-11-27_121328/121331/122240.json`) et un contrôle de la page publique
par navigation ordinaire ce cycle. Si le fichier est déposé ultérieurement, son
ingestion se fait par `hfm_public_collector.py ingest` sans réécrire l'historique.

## 2. Statistiques vérifiées (contrôle du jour, valeurs telles qu'affichées)
49 595 fermées (33 425 gagnantes / 16 170 perdantes), 0 ouverte, rentabilité 67,4 %,
gain moyen ¥22,37, perte moyenne ¥−27,82, lot moyen 0,03, durée moyenne 20 min 14 s,
DD max 31,81 %, gain 12 420,75 %, levier 1:500, JPY, frais 10 %, dépôt min ¥35 000,
121 abonnés. **Identiques aux valeurs attendues et aux captures précédentes —
évolution confirmée : aucune.** Ces agrégats ne prouvent aucune rentabilité nette
reproductible et ne permettent pas de reconstruire des décisions.

## 3. Déduplication (clé composite du collecteur, protocole RE-ENTRY-003)
6 lignes visibles ; **6 déjà connues et confirmées, 0 nouvelle, 0 ambiguë**
(`TRANSACTION_DEDUP_AUDIT.csv`). Regroupements confirmés : 10:30 = panier C
(3 positions, −6 ¥), 10:45 = D (1 position, +1 ¥), 11:00 = E (2 positions, +3 ¥) —
comptés comme 3 paniers, jamais comme 6 décisions indépendantes.

## 4. Classification du flux
**FLUX PUBLIC INCHANGÉ.** Formulation correcte : « Aucune nouvelle transaction n'est
visible dans le flux public observé depuis la dernière transaction affichée
(2026-11-27 11:01:27, heure affichée). » Cela ne prouve pas que le trader est inactif.

## 5. Collecteur
`hfm_public_collector.py` existe (fetch/ingest/baskets, snapshots immuables SHA-256,
déduplication par clé composite) ; dernières captures prouvées : 2026-11-27 12:13–12:22
UTC. Aucune exécution automatique continue n'est démontrée (cron inopérant sur branche
non-défaut, CI = 403 sans contournement) : la cadence de 15 min est une configuration,
pas une garantie. Limites inchangées : 6 lignes visibles, pas de pagination.

## 6. Impact scientifique
Confirmées : aucune. Réfutées : aucune nouvelle. Non testables :
`NOT_TESTABLE_WITH_CURRENT_OBSERVATIONS` (H3, F2, clôtures). Conclusions
COLORFUL-FILTER-002 préservées intégralement ; aucun seuil déplacé, aucun filtre
ajouté sur les cinq paniers. La chronologie des statistiques est créée
(`PROVIDER_STATS_TIMELINE.csv`, 3 captures, toutes identiques).

## 7. Prochaine étape
Voir `NEXT_EVIDENCE_REQUIREMENTS.md` : déposer le fichier HTML annoncé ou capturer
des transactions postérieures au 2026-11-27 11:01:27 ; chaque nouveau panier sera
classé d'abord, comparé au modèle gelé ensuite.
