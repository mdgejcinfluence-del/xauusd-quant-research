# COMPARAISON ÉCONOMIQUE DES MÉCANISMES (nets, mêmes périodes, EXPLORATORY_POST_HOC)

| Mécanisme | Brut mesuré | Net mesuré | Payeur | Risque porté | Accessible ? |
|---|---|---|---|---|---|
| Fade d'impulsion 1-4 barres (liquidité) | +0,17 bp | −2,2 bp (preneur) | le suiveur d'impulsion | sélection adverse | Non (exige limites+file) |
| Vente de variance (options) | prime médiane +2,0 pts vol | non simulable | acheteurs de protection | sauts (29,7 % des fenêtres) | Non (licence) |
| Grille de retour à la moyenne | 62 % de jours gagnants | moyenne −1,7 bp/jour, queue −1 112 bp | les impatients | tendance sans retour | Oui mais rejetée (risque) |
| Exposition par bloc horaire | drift ≤ +1,4 bp/barre | négatif après 1 AR/jour | — | directionnel | Oui, sans valeur |
| Hedging pressure hebdo (COT) | instable | instable | hedgers futures | inventaire/queue | Partiellement, réfuté comme règle |
| Deadline 120 min (gestion) | mécanisme −31→tronqué | **prospectif en cours** | la dérive des non-confirmés | faux positifs rapides | Oui — seul test vivant |

Leçon unique du tableau : sur XAUUSD, la rémunération se trouve du côté de qui **fournit**
(liquidité, assurance, portage) ; META ALPHA a jusqu'ici toujours payé de ce côté-là.
