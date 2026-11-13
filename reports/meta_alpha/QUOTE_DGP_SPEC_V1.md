# QUOTE_DGP_SPEC_V1 — Schéma réel du corpus (découvert, jamais présommé)

**Source :** footers Parquet des 348 partitions, lien public Drive `META_ALPHA_XAUUSD_DGP`
**Preuves :** `INVENTORY_348.json` (348/348), `PROBE_000184.json`, `SCHEMA_PROBE_V1.json`

## Colonnes (16, toutes les partitions)
observation_id int64 · timestamp_utc timestamp[us, UTC] · bid/ask/mid/spread_abs/spread_rel double ·
bid_volume/ask_volume (type variable, voir groupes) · symbol string · source_file string ·
file_row_number int64 · previous_timestamp timestamp[us, UTC] · previous_mid/log_return/abs_log_return double

## Deux signatures de schéma (et non une) — blocs contigus
| Groupe | Partitions | Volumes | 1re colonne | Lignes |
|---|---|---|---|---|
| `fa1e4b2b96a29903` | 000001–000294 (294) | double | observation_id | 357 867 122* |
| `bee1fc6dc6b43616` | 000295–000348 (54) | uint32 | timestamp_utc | 327 251 503 |

*inclut les 48 227 lignes de la 000184 re-sondée directement.
**Total : 685 118 625 lignes = certificat Phase 2, écart 0.**

## Règles d'interprétation (passation §11, non négociables)
- Un tick = changement de cotation, pas une transaction. `bid_volume`/`ask_volume`
  ne sont pas du « volume réel » sans preuve de sémantique.
- L'hétérogénéité est documentée, pas corrigée silencieusement : tout moteur
  devra normaliser explicitement (cast des volumes, sélection de colonnes par nom).
- Fuseau : UTC explicite dans le type Parquet. Précision : microseconde.
- Doublons, égalités de timestamp, gaps, quotes invalides : à mesurer en L2/L4,
  pas encore établis — ne rien affirmer avant mesure.
