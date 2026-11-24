# EUR-EDGE-01 — SPÉCIFICATION DES SCHÉMAS

- `ticks` : `ts` (UTC, ms), `bid`, `ask` (unités de prix source, EURUSD 5 décimales), volumes de
  cotation Bid/Ask lorsqu'ils existent (jamais nommés « volume échangé »). `mid` dérivé =
  (bid+ask)/2, calculé à la lecture, pas stocké comme prix source.
- `barres_<TF>` : `bar_start` UTC, `open/high/low/close` **Mid**, `n_ticks`, TF ∈ M1, M5, M15,
  M30, H1, H4, D1. Toute barre issue d'une autre source que les ticks internes est interdite de
  mélange sans colonne `source`.
- `cot_eurofx` : dates `report_date` (mardi, référence) et `available_from` (vendredi de
  publication + marge conservative) **toujours séparées** ; positions par catégorie
  (Prod/Merc, Swap, Managed Money, Other), open interest, % OI, nombre de traders si publié.
- `rates` : `date`, `series_id`, `value`, `source_url`, `downloaded_at`, `vintage` (= date de
  téléchargement : une série révisée n'écrase jamais silencieusement l'ancien millésime).
- Conventions : prix EUR/USD en décimal (1,0850) ; spreads en pips (0,0001) et en bp relatifs
  explicités ; aucun fuseau autre qu'UTC en stockage.
