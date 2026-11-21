# PHASE 10-A — DICTIONNAIRE DES VARIABLES

**Convention** : « décision » = clôture de la barre de l'horizon
considéré. Disponibilité = premier instant où la variable est
calculable. Toutes les variables explicatives sont closes à la
décision ; tout ce qui suit est une mesure, jamais un prédicteur.

| Variable | Définition | Disponibilité exacte |
|---|---|---|
| r_H1, r_H4, r_D1 | rendement log de clôture à clôture de la barre, ×10⁴ (bp), barres Bid/Ask et Mid séparées | clôture de la barre |
| Q95/Q90/Q25 causaux | quantiles des 250 dernières barres closes du même horizon (interpolation linéaire), recalculés à chaque décision | clôture de la barre ; inéligible si < 250 barres d'historique |
| Seuil d'extrémalité | valeur du quantile à la décision (bp), publiée par événement | clôture |
| Range de barre | (haut − bas)/clôture ×10⁴ (bp) sur Bid/Ask | clôture |
| Franchissement | clôture strictement au-delà du max (ou sous le min) des 20 (H1) / 30 (H4) clôtures-barres précédentes, extrêmes de barres | clôture de la barre de franchissement |
| Sens de l'événement | signe de r à la décision, ou sens du franchissement | clôture |
| Spread de décision | médiane des spreads tick (Ask−Bid)/Mid ×10⁴ de la barre de décision | clôture de la barre |
| Session / ère | session UTC de la décision (S1 00–07, S2 07–13, S3 13–21, S4 21–24) ; ères 2010–13/2014–16/2017–20 | connues à la décision |
| MFE / MAE | excursions maximale favorable / défavorable (bp, prix exécutables selon le sens) sur la fenêtre suivante | rétrospectives — mesures uniquement |
| Rendement signé à fenêtre fixe | rendement de la fenêtre suivante orienté par le sens de l'événement (bp, Bid/Ask) | rétrospectif — variable primaire |
| Temps d'excursion | minutes/barres jusqu'au MFE et au MAE | rétrospectif |
| Chevauchement | deux fenêtres de mesure se recouvrant dans le temps | calculé a posteriori pour les grappes |
| Censure | fenêtre suivante incomplète (trou, fin de corpus) : statut publié, jamais complétée | à la mesure |
| Délai d'entrée | t_exec − t_ouv, où t_exec = premier tick suivant la clôture du signal et t_ouv = ouverture attendue de la barre suivante (clôture du signal en cotation continue ; heure de réouverture réelle après fermeture régulière ou week-end, l'horloge ne courant qu'à la reprise) ; éligible si ≤ **120 secondes** et cotation dans la première barre suivante, sinon **INÉLIGIBLE_ENTRÉE_TARDIVE** (exclu de la rentabilité exécutable, comptabilisé en couverture) ; trou intra-session > 120 s ⇒ inéligible ; approximation par présence de barre étiquetée si ticks absents (règle identique au modèle de coûts et à l'addendum final §2) | à l'entrée |
| P90 du MAE | quantile 90 % (interpolation linéaire) des MAE_i du bras ; limite gelée ≤ 10 × C_ref, appliquée séparément par événement et par grappe | rétrospectif — porte 3 élargie |
| ES90 du MAE | moyenne des MAE_i ≥ P90 du bras ; limite gelée ≤ 15 × C_ref, appliquée séparément par événement et par grappe | rétrospectif — porte 3 élargie |
| MAE de grappe | MAE_g = max des MAE_i des événements de la grappe temporelle | rétrospectif — diagnostic et porte |

Données déclarées **indisponibles** : carnet d'ordres et profondeurs,
remplissages réels, latence mesurée, commissions et swaps d'un
courtier identifié (voir modèle de coûts : scénarios étiquetés).
