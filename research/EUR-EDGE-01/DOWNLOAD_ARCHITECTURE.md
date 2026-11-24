# EUR-EDGE-01 — ARCHITECTURE DE TÉLÉCHARGEMENT ET DE REPRISE

Pipeline (`ci_tools/eur01_engine.py`, exécuté en CI GitHub Actions, seul environnement avec
egress) : découverte → audit licence → échantillon mesuré → acquisition par tranches →
contrôle qualité → normalisation Parquet → manifeste SHA-256 → stockage autorisé.

Principes contraignants, dans l'ordre :
1. **La licence décide avant la technique.** Aucun téléchargement massif d'une source dont les
   conditions interdisent la constitution d'une base de données (cas Dukascopy : échantillon
   technique limité à quelques heures/jours pour mesurer taille et qualité ; archive complète
   uniquement après accord écrit ou via un canal dont les conditions le permettent).
2. **Reprise** : chaque tranche (année COT, journée de ticks autorisée) est idempotente —
   manifeste par source (`data/COLLECT_MANIFEST`-équivalent), les échecs transitoires (503,
   timeouts) sont réessayés avec espacements, seuls les vides anciens et confirmés sont figés.
3. **Jamais monolithique** : échantillon 1 heure → 1 jour → 1 mois, mesures de taille/temps/
   échecs à chaque étape (voir `PROBE_TAILLES.json` : ≈ 17 k ticks pour 6 heures échantillon,
   ≈ 0,7 Go Parquet estimés pour 17 ans de ticks complets — le stockage n'est pas le problème,
   le droit l'est).
4. **Brut immuable / dérivé séparé** : les fichiers bruts (zips CFTC, CSV officiels) et les
   échantillons restent en `data/` sans correction ; toute série nettoyée est un nouvel objet
   documenté. Les différences entre courtiers ne sont jamais « corrigées ».
5. **Partitionnement** `SOURCE/INSTRUMENT/FRÉQUENCE/ANNÉE/MOIS`, horodatages UTC partout,
   convention d'origine conservée dans les métadonnées (ex. HistData EST fixe — rejeté ;
   Dukascopy UTC).
6. **Volumes jamais mélangés** : volume de cotation Dukascopy ≠ tick volume générique ≠ volume
   réel futures CME ≠ open interest. Chaque colonne porte son type.

Limite d'environnement connue : le cron GitHub ne s'exécute que depuis la branche par défaut ;
sur cette branche de session, les acquisitions sont relancées par dispatch à chaque session.
