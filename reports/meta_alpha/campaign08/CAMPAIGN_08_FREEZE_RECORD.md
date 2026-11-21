# CAMPAGNE 8 — PROCÈS-VERBAL DE GEL DÉFINITIF DU PROTOCOLE F-J V2

**Date : 2026-11-13. Statut : GEL DÉFINITIF — EXÉCUTION NON AUTORISÉE.**

## 1. Décision

Le propriétaire valide le protocole consolidé V2 « Chocs minute
extrêmes et leur sillage » et autorise son gel définitif (chaîné
seq265). Le gel ne constitue pas une autorisation d'exécution : un
ordre distinct du propriétaire sera nécessaire.

## 2. Document de référence unique

`CAMPAIGN_08_PROTOCOL_V2.md` —
SHA-256 `8e8479505efa03c0387171152ff01aeff368c77cc70929c35b2dcf9a4d5e795e`,
revérifié à l'octet près au moment du gel. C'est le seul document qui
fait foi pour l'exécution.

## 3. Ordre de prévalence documentaire

1. **V2 (gelé)** — référence unique d'exécution.
2. `CAMPAIGN_08_PROTOCOL_V1.md` (`022ca0dc…9af`) et
   `CAMPAIGN_08_PROTOCOL_V1_1_ADDENDUM.md` (`b51dbdf3…279`) —
   conservés sans modification pour la traçabilité ; en cas d'écart
   avec V2, V2 prévaut et l'écart est un incident documentaire à
   consigner, jamais à corriger silencieusement.
3. Documents préparatoires (blueprint `06a49727…`, dictionnaire
   `ade2310e…`, comparaisons `1fb49e3e…`, couverture/biais
   `0d205acc…`) — valeur historique ; en particulier la numérotation
   « J-01…J-05 » y est supersédée par FJ-01…FJ-05, et la sélection des
   pseudo-événements par journée × session y est supersédée par le
   bassin par blocs de 60 minutes du V2.

## 4. Contenu verrouillé (vérification pré-gel effectuée)

- Constantes et formules validées : fenêtre causale 20 journées,
  T_D = max(10 bp, Q₉₉,₅ linéaire), prédicat strict |r_t| > T_D,
  amorçage ≥10 journées et ≥10 000 variations, I_ép = max
  |r_t|/T_{D(t)} (classes à 2), regroupement ≤15 min inclusif,
  horizons +15/+30/+60 principal, R₆₀ signée ancrée à c(t_der),
  matérialité 10 bp, éligibilité ≥200 épisodes et ≥100 grappes/bras.
- Cinq comparaisons fermées FJ-01…FJ-05, BY à m = 5 fixe, bootstrap
  2 000 réplicats par grappes-composantes connexes, graine à publier
  dans le manifeste d'exécution (constante de code, non méthodologique).
- Censure des clôtures indéterminées : silence de 15 minutes
  intégralement observé ou CLÔTURE_INDÉTERMINÉE, aucune disponibilité
  attribuée, exclusion des comparaisons.
- Appariement temporel des pseudo-événements : bassin par blocs de
  60 minutes depuis le début de session, distance de position
  ≤ 60 minutes, sans remplacement, aucune exclusion pour choc futur.
- Graphe complet de dépendance incluant les pseudo-événements FJ-05,
  frontières journalières traversées, diagnostics publiés.
- GRAPPE_DOMINANTE à 5 % d'un bras : publication descriptive
  maintenue, inférence étiquetée INFÉRENCE_FRAGILE, CANDIDATE_J1
  interdite ; COMPOSITION_SENSIBLE (FJ-05) interdit de même toute
  candidature. Aucun contrôle ne crée de p-value supplémentaire.

## 5. Restrictions maintenues

XAU/USD ; corpus IS uniquement ; holdout scellé ; aucun calcul,
extraction, bootstrap ni consultation de résultats F-J à ce stade ;
aucun backtest ni `challenge_sim` ; aucun J2/J3 automatique ; aucun
budget expérimental consommé ; FRED suspendue ; 36 cellules S12
gelées ; T0 séparé et inactif ; aucune fiche historique modifiée ;
F-G et F-I définitivement clôturées ; F-H et F-L en réserve.
