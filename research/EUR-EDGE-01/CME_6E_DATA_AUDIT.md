# EUR-EDGE-01 — AUDIT CME EURO FX FUTURES (6E)

Faits : contrat 6E = 125 000 EUR, coté en USD/EUR, échéances trimestrielles, volume réel et
open interest existent **parce que c'est un marché centralisé** — à ne jamais confondre avec le
spot décentralisé. Données historiques détaillées (Time & Sales, BBO, carnet) = produits
licenciés CME DataMine/vendeurs : **achat interdit (budget 0)**. Gratuitement accessibles :
spécifications du contrat et informations publiques agrégées du site CME (pages produit),
insuffisantes pour une série de recherche 2010-2026.
Décision : bloc `LICENSE_OR_COST_BLOCKED` documenté. Les rollovers ne seront jamais fabriqués :
sans les contrats individuels licenciés, aucune série 6E n'est construite. Si une source
publique licite de volume/OI quotidien par échéance est identifiée plus tard, elle entrera par
un nouvel audit, avec ses propres colonnes et son propre calendrier.
