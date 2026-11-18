# PHASE 4 « PANEL » — SYNTHÈSE (IS panel ≤ 2014-12-31 ; OOS 2015-2019 et HOLDOUT ≥ 2020 jamais ouverts)

## Données certifiées
Panel de 43 futures continus ajustés (source GitHub publique JuBaMan/Time-Series-Momentum-Study, zip SHA-256 au manifeste `PANEL_MANIFEST.json`, hash par fichier, dates de début certifiées 1959→2015). Prix = colonne « low » des séries ajustées par ratio (convention du dépôt source, vérifiée dans son code) : séries de rendements continus ajustées des rolls, **pas des prix exécutables** — limite consignée. Univers principal : 31 marchés débutant ≤ 1999 ; évaluation 2000–2014. Les moteurs tronquent à 2014-12-31 en fail-closed (assert sur la borne).

## Gate de puissance — TESTABLE (de justesse)
15 ans × 31 actifs : SE(Sharpe) ≈ 0,26 → MDE 80 % = **0,72 < 0,8 visé**. Le panel résout bien le problème de F9 (0,93), sans le rendre confortable.

## Verdicts (critères gelés avant calcul)
| Famille | Meilleure variante | Sharpe net | Années + | DSR | PBO | Stress ×2 | Verdict |
|---|---|---|---|---|---|---|---|
| F10 XSMOM (16 essais) | L=63, tercile, risk-parity | 0,56 | 60 % | 0,878 | 0,557 | 0,34 | **ÉCHEC** |
| F11 TSMOM panel (12 essais) | L=126, EWMA, cap 30 % | 0,28 | 53 % | 0,586 | 0,821 | 0,14 | **ÉCHEC** |
| F12 blend | — | — | — | — | — | — | **SANS OBJET** (condition F10∧F11 non remplie) |

Contrôles sains : placebo côté (signal inversé : Sharpe −1,01 / −0,55) et rangs mélangés (−1,29) perdent comme prévu — la mécanique de test n'est pas en cause. Le détail par blocs est éloquent : le momentum de ce panel gagne sur les premiers blocs et perd sur les derniers (F11 : +0,83/+1,05/+0,99 puis −0,90/−0,28) — décroissance du phénomène sur la fenêtre IS 2000–2014 dans cette implémentation gelée (univers, prix « low », rebalancement hebdomadaire, coûts 2 bp/côté), pas un artefact de signe.

## Budget panel
28/60 essais consommés (F10 16 + F11 12). Les 32 restants (dont réserve de robustesse 28) ne sont **pas** dépensés : la règle d'arrêt §6 s'applique — après l'échec des deux familles gelées, re-griller serait exactement le data-mining que le budget devait empêcher.

## Ce que ce verdict dit et ne dit pas
Il dit : sur cet univers, cette fenêtre IS et cette implémentation préenregistrée, le momentum journalier ne survit pas à nos critères (Sharpe ≥ 0,8, DSR, PBO, stress). Il ne dit pas que le momentum « n'existe pas » dans la littérature : il dit qu'il ne passe pas **notre** protocole, à **nos** coûts, sur **nos** données gratuites — avec leurs limites (prix ajustés non exécutables, rolls par ratio, univers survivant du dépôt source). Toute réouverture exigerait un nouveau préenregistrement et une justification nouvelle (autre source de données certifiée, autre univers), pas une variante de plus.

## Clôture du programme (§6)
Aucune dépense de challenge (aucune composante directionnelle qualifiée, simulateur sans objet à trancher). Actifs permanents, réutilisables sur tout futur corpus : cartographie XAUUSD complète (Phases 1–3), F3 et F7 validées L2, châssis de sizing/gouvernance, simulateur de challenge paramétré, chaîne d'audit SHA-256 de bout en bout. OOS XAUUSD, OOS panel et HOLDOUT restent fermés, intacts, pour le jour où une hypothèse nouvelle — née d'ailleurs que d'un re-grillage — justifiera de les ouvrir sur ordre explicite.
