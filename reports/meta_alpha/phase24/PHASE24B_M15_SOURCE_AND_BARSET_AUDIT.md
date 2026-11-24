# PHASE 24-B — AUDIT SOURCE ET BARSET M15

Barres M15 `[t, t+15 min)` construites depuis les cotations Bid/Ask des 8 lots IS uniquement
(traitement borné par journée, DuckDB), prix Mid, aucun remplissage ni interpolation.
238 085 barres du 2010-01-04 au 2019-12-16, dont **99,58 % complètes** (≥ 10 cotations,
écart maximal < 600 s, couverture ≥ 600 s) ; les barres incomplètes restent identifiées et sont
exclues de la chaîne événementielle. Holdout 2020-2026 jamais accédé. Seules les barres
complètes alimentent impulsions, replis et réintégrations ; chaque barre conserve nombre de
cotations, premier/dernier timestamp, spread médian et écart maximal.
