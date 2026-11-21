# CAMPAGNE 8 — DOSSIER DE CLÔTURE F-J

**Protocole gelé V2 (seq266) ; exécution autorisée seq267, confirmation
de gel seq268 ; run CI 44911859012 vert du premier coup (commit runner
d'extraction). En attente de validation du propriétaire.**

## Résultats (détails : CAMPAIGN_08_REPORT.md et CAMPAIGN_08_COMPARISONS.csv)

- **FJ-01 NÉGATIF** (+0,17 bp [−0,81 ; +1,61], q BY 1,000).
- **FJ-02 SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL** (−3,74 bp
  [−5,38 ; −1,78], q 0,0057 ; seuil matériel 10 bp).
- **FJ-03 NÉGATIF** (−2,52 bp [−4,23 ; +0,16], q 0,312).
- **FJ-04 NÉGATIF** (−1,47 bp [−3,24 ; −0,17], p 0,029, q 0,166).
- **FJ-05 NON ÉVALUABLE** (12 grappes seulement, GRAPPE_DOMINANTE —
  plus grande composante 99,8 % — et COMPOSITION_SENSIBLE ; aucune
  lecture inférentielle, descriptif publié).

**Aucune candidate J1 ; catalogue ANO-C8 vide** (CAMPAIGN_08_ANOMALY_CATALOG.md).

Faits : 14 735 chocs causaux, 7 905 épisodes (1 322 mixtes publiés
séparément ; 72 clôtures indéterminées censurées) ; retracement médian
à une heure −5,07 bp, soit environ un tiers de l'amplitude de
l'épisode ; nouveau choc dans l'heure suivant 29,6 % des épisodes.

## Provenance et intégrité

Extraction intégralement régénérée par le run 44911859012
(282/282 partitions, 3 540 993 barres M1) ; synthèse locale
(campaign08_synthesize.py). La synthèse a connu trois correctifs de
code avant publication (détails au registre des incidents) ; aucune
définition gelée ni aucun chiffre d'extraction n'a été modifié, et les
lectures finales proviennent de la passe complète corrigée.

## Hashes SHA-256 des livrables

- CAMPAIGN_08_REPORT.md : `baf5ba5547219b9e998bb9f2cf5b86b23808a06534ecc9d28c9620931a084e71`
- CAMPAIGN_08_COMPARISONS.csv : `6532cadeca4f501e5872736112c3fc2700c5029d3c1a656ecdd4d22c6b0bb60b`
- CAMPAIGN_08_DETAILS.json : `068d8049fe24aaa73ed7faa0429bad8806d5a015e2e1ab61a3e3196f22053b29`
- CAMPAIGN_08_EPISODES.csv.gz : `9e2ca3fb785a46fb2b3c4675a94c25ff587b30cdfcc9e08f2786d97dbc611486`
- CAMPAIGN_08_PSEUDOS.csv.gz : `077fe823420e51650b2e967a7d1366bd8dec1135be766e7f1aa8c3005411ac65`
- C8_COVERAGE.json : `99202f386686a1ce9a165903fef10398ad6903bbc56c14805a46d42366ec732c`
- CAMPAIGN_08_ANOMALY_CATALOG.md : `7d4b432d024c8384e3f8ef83f999770e92b875b2aaa2415c0d34d80d368e1e89`
- CAMPAIGN_08_PSEUDO_REPORT.md : `778c09d9a58b27498e4ea14534d9fa0ed6ba4deee93607f2585b84980f720133`
- CAMPAIGN_08_COVERAGE_DIAGNOSTICS.md : `bace441d315bc3483d2c8fe8449ca11219cbcd6094325a3bb1f259d8ceb2fccb`
- CAMPAIGN_08_INCIDENTS_LIMITS.md : `f8245fce5b22f452bfa54d272c975f42786ee883190fce396b1cfb2e3df79ece`
- campaign08_engine.py : `1a47b7f9754b3ed33ccc88adc1d655be9fd3cea14742d9a676a85d6e0e108077`
- campaign08_synthesize.py : `8348fcabeb01dc4efc5d68c541300927a0dce5ac5db04d43939e640e43c9b8e5`

Restrictions maintenues : corpus IS seul, holdout scellé, aucun
backtest ni J2/J3, budgets inchangés, fiches historiques non modifiées,
F-G et F-I définitivement clôturées.
