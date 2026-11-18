# PACK EXOGÈNE — CERTIFICATION DE COMPLÉTION (seq 103, suite du rapport seq 102)

Ingénierie de collecte uniquement : 0 essai consommé (tick 148/150, panel 28/60 figés), 0 analyse, 0 statistique, 0 graphique.

## Definition of Done — checklist gelée de l'ordre
| Item | Statut |
|---|---|
| C1 — 7 séries macro PIT + FOMC | ✅ 11 séries PIT ALFRED livrées + table FOMC 2010→2028 (198 réunions) |
| C2 — DFII10 + GVZCLS (+ DGS10/DGS2 officiels) | ✅ les 4 séries officielles FRED livrées, proxys Yahoo seq 102 conservés et consignés |
| C3 — GLD/IAU clôture honnête | ✅ clos définitivement (seq 104) : flux non certifiables, volume GLD ≠ flux, substitut interdit à jamais |
| 3 datasets mis à jour, VERIFY all_ok = true | ✅ 28 (IS) / 27 (OOS) / 27 (HOLDOUT) fichiers, noms+tailles égaux |
| Audit anti-fuite rejoué sur l'intégralité | ✅ max(available_at_utc) exposé = 2020-01-19 19:00 UTC ≤ 2020-01-20T09:36:27 |
| Registre chaîné, aucun essai, aucune analyse | ✅ seq 103 MISSION, seq 104 C3, seq 105 RESULTAT |

## C1 — Point-in-time ALFRED (available_at = vintage + publication ET→UTC, DST date par date)
| Série | Versions | Vintages | Couverture référence |
|---|---|---|---|
| PAYEMS (NFP) | 3 917 | 231 | 2009→2026-10 |
| UNRATE | 2 209 | 231 | 2009→2026-10 |
| CPIAUCSL / CPIAUCNS | 2 932 / 2 035 | 243 / 230 | 2009→2026-10 |
| PCEPI / PCEPILFE | 3 766 / 3 764 | 229 | 2009→2026-09 |
| GDP (3 estimations confondues en vintages) | 1 207 | 225 | 2009→2026-07 |
| ICSA (claims hebdo) | 13 172 | 923 | 2009→2026-11 |
| DFEDTARL | 62 391 | 5 170 | 2009→2026-11 |
| FEDFUNDS | 2 035 | 233 | 2009→2026-10 |
| DFEDTARU | 6 531 | — (voir note) | 2009→2026-11 |

Note DFEDTARU : ALFRED répond « The series does not exist in ALFRED » (message consigné au journal du manifeste). Repli documenté : série FRED courante, série d'événement de politique monetaire (valeur fixée par le communiqué, non révisée), available_at = jour de décision 14:00 ET converti DST. Aucun panel de vintages fabriqué.
Note profondeur : les panels démarrent aux vintages 2009 (décision d'ingénierie du collecteur, `observation_start=2009-01-01`) ; couverture réelle consignée série par série au MANIFEST.

Contrôle DST (vérifié sur les fichiers IS livrés) : FOMC janvier → 19:00 UTC, juillet → 18:00 UTC ; CPI février 2009 → 13:30 UTC, mars/avril 2009 → 12:30 UTC. Aucune conversion à décalage fixe.

FOMC : 198 réunions 2010-01-27→2028-01-26 (81 dans le périmètre IS), sources officielles federalreserve.gov (calendriers + `json/calendar.json` + pages `fomchistoricalAAAA.htm`), statement J2 14:00 ET→UTC.

## C2 — Officiel FRED (référence primaire ; proxys Yahoo seq 102 conservés au manifeste)
DFII10 : 5 973 j (2003→2026-11) · GVZCLS : 4 647 j (2008→2026-11) · DGS10 : 5 973 j · DGS2 : 5 973 j. L'ancienne clef manifeste `fred_taux_reel` (échec v1) est supersédée par `fred_dfii10_officiel`.

## Incidents consignés (jamais effacés)
1. **Run 2 (44330373562)** : la clé FRED est apparue dans des URLs d'erreur journalisées au manifeste — purgée dès le run suivant (commit 7c0ebec), erreurs sanitisées (`api_key=REDACTED`) depuis. **Action propriétaire : révoquer la clé sur sa page FRED** (déjà prévue par l'ordre : accès temporaire).
2. Run 2 historique : requête vintage-par-vintage trop lente → timeout 300 min ; remplacée par l'API ALFRED native toutes-vintages par millésime.
3. Run 4 (44391827832) : HTTP 400 FRED sur l'année courante (`realtime_end` postérieur à aujourd'hui) → séries entières perdues ; corrigé run 5 (borne à aujourd'hui, années déjà collectées préservées).
4. FOMC pré-2021 : pages d'archives `fomc_historical_year.htm?year=` sans dates exploitables (sondes 44410567839→44412132793, journal `FOMC_PROBE.txt` versionné) ; résolu par `json/calendar.json` officiel (≥2017) puis pages `fomchistoricalAAAA.htm` (2010→2016).
5. Vérification Kaggle : arrêt prématuré sur comptage (fichiers de l'ancienne version) → attente d'égalité complète des tailles (run 5+).

## Scellés
OOS/HOLDOUT : métadonnées seulement, contenu jamais téléchargé par un moteur ; barrière fail-closed inchangée. SHA-256 par fichier dans VERIFY_IS/OOS/HOLDOUT.json ; journal complet des requêtes et bascules dans MANIFEST.json (`completion_seq103`).

## Arrêt
STOP. Le pack complet dort — scellé, certifié, honnête — jusqu'à préenregistrement neuf + budget neuf + gate R3 + ordre explicite du propriétaire. Rappel : révoquer la clé FRED (hygiène de desk, accès temporaire terminé).
