# ME-001.1 — COUVERTURE DES DONNÉES

Partitions Dukascopy certifiées (inventaire 348, téléchargées en CI par
gdown, jamais commitées) : part_000211 (2012-07-20→08-26, découverte),
part_000250 (2016-07-25→08-30, découverte), part_000289 (2020-07-29→09-03,
validation), part_000327 (2024-06-30→08-05, validation), part_000345
(2026-05-05→06-10, validation). Barres de 5 s construites depuis les
ticks Bid/Ask ; aucune donnée HFM substituée. Périodes hors partitions
(absences entre partitions, octobre 2026, etc.) : non étudiées, non
extrapolées. Contamination : les seuils et la définition d'épisode ont
été gelés en seq480 avant tout calcul et n'ont été calibrés sur aucun
résultat ; 2020–2026 avait servi à d'autres campagnes (moteurs gelés),
ce qui est déclaré — la validation est donc « à protocole gelé », pas
un holdout vierge absolu. Épisodes censurés à 24 h et à la fin de
chaque partition.
