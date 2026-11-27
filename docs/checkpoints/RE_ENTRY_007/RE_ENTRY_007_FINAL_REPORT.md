# RE-ENTRY-007 — RAPPORT CONSOLIDÉ (intégration du nouveau snapshot annoncé)

Branche de travail : `arena/afe12737-xauusd-quant-research` (branche de session
imposée ; la branche dédiée demandée n'a pas été créée, règle de session prioritaire —
écart documenté, `main` intacte). Références gelées revérifiées : V1/V2 intouchés,
matching corrigé seq448, H3/F2 et leurs falsifications inchangés.

## 1. Fichier annoncé : reçu et intégré (addendum post-seq452)
Le fichier a d'abord été introuvable (recherches documentées espace + Drive,
seq451) ; il a ensuite été **déposé par le fondateur et intégré tel quel** :
`docs/checkpoints/RE_ENTRY_007/source/myHF _ HFM Broker.html78.html`, SHA-256
`2e3a9e19d56cbfa9fe28c7fe275b0af7b7a8f3b579db623fe442c288ebddc210` (2 509 846 octets).
En-tête « saved from url » : portail `my.hfm.com/.../provider-details?provider=99001292`
— une vue portail, à ne pas confondre avec la page publique. **Aucune date de capture
n'est indiquée dans le fichier** (inconnue, non inventée). Extraction : 6 lignes,
statistiques identiques (nuance d'affichage : gain/perte moyens arrondis ¥22/¥−28 sur
le portail contre ¥22,37/¥−27,82 sur la page publique — valeurs conservées telles
quelles, sans correction silencieuse). Verdict du fichier : **aucune transaction
nouvelle** ; les 6 lignes sont celles de C/D/E déjà archivées.

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
