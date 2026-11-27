# DIAGNOSTIC — SÉLECTIVITÉ DES ENTRÉES (D2)

V1 ouvre ~17 paniers/jour (3 728 en ~8,5 mois ; 90,6 % par voie rapide) là où les
observations réelles montrent quelques paniers par session. Décomposition (nov.
complet, jours locaux) : V1 379 paniers contre 230 pour V2-F2, qui reste très actif.
Catégories mesurées lors des campagnes précédentes : réentrées en chaîne 0,1–9 s
après clôture (V1, corrigée en partie par F2) ; entrées répétées dans la même zone
d'impulsion ; aucune feature causale testée (ret5/15/30/60m, reprises, positions,
volatilité, heure) ne sépare les entrées réelles des simulées excédentaires
(COLORFUL-FILTER-002, résultat négatif conservé). Les non-entrées réelles restent
majoritairement `ABSENCE_OF_TRADE_NOT_PROVEN` (page publique de 6 lignes) : la
condition de sélection du trader demeure **inconnue**, et aucun filtre nouveau
n'est proposé à partir des 5 paniers (sur-ajustement refusé).
