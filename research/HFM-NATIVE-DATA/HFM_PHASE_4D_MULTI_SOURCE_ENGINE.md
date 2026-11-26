# PHASE 4D — ADAPTATEURS MULTI-SOURCES (collecteur étendu, MT5 non bloquant)

`ci_tools/hfm_collector.py` conserve ses modes MT5 (`probe/pilot/collect/selftest`,
adaptateur `hfm_native_authenticated` futur, jamais requis) et reçoit :
- `extpilot` (nouveau, HTTP, Linux-compatible) : preuve documentaire HFM + pilote HistData réel,
  résultats horodatés dans `external_reference/PILOT_EXTERNAL.json`, brut ZIP conservé avec
  SHA-256, aucune ligne synthétique.
- Adaptateurs déclarés mais sans source à ce jour : `hfm_public` (vide, prouvé en 4A),
  `hfm_archived` (vide, prouvé en 4B) — ils lèveront une erreur explicite plutôt que de
  retomber silencieusement sur un flux externe.
Chaque adaptateur déclare sa classe de preuve (`HFM_NATIVE_VERIFIED`, `HFM_ARCHIVE_PROVEN`,
`HFM_PROVENANCE_UNCERTAIN`, `EXTERNAL_REFERENCE`, `SYNTHETIC_TEST`) dans chaque manifeste ;
le mélange des classes dans une même partition est interdit par construction (dossiers séparés).
