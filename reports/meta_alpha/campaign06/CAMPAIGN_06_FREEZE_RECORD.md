# CAMPAGNE 6 — PROCÈS-VERBAL DE GEL DÉFINITIF DU PROTOCOLE F-G

**Décision du propriétaire : validation du dossier F-G V1.1 + V1.2 +
V1.2.1 + V1.2.2 et autorisation du chaînage du gel définitif.**
Enregistrée au registre chaîné en seq238 (autorisation) et seq239
(gel). **Le gel ne vaut pas autorisation d'exécution : un ordre
explicite distinct du propriétaire sera nécessaire pour lancer les
calculs F-G.**

## Documents gelés (SHA-256 vérifiés un par un avant chaînage)

| Document | SHA-256 complet |
|---|---|
| `CAMPAIGN_06_PROTOCOL_V1_1.md` | `0fdb39204c25d38c4d4628113d5572cd7962ae6209d6e26b95133419efee4c76` |
| `CAMPAIGN_06_PROTOCOL_V1_2_ADDENDUM.md` | `046df8d949203a5c7d890f736e5781441750225959eb309373ea829bba731217` |
| `CAMPAIGN_06_PROTOCOL_V1_2_1_ERRATUM.md` | `78ef301f6defba193cb121dfaa76382a3eff19af9e255b5ace43919ded11cc1c` |
| `CAMPAIGN_06_PROTOCOL_V1_2_2_ERRATUM.md` | `b8e853db2e2170d5e13a95914c1d42447e54c6a7c5ac345bdc6781f474d8b3b1` |

Ordre de prévalence en cas de tension : V1.2.2 > V1.2.1 > V1.2 > V1.1.
Les quatre fichiers sont présents dans le dépôt, inchangés depuis leur
validation respective (hashes revérifiés à l'identique au moment du
gel), et leurs empreintes sont inscrites dans l'entrée de gel seq239
de `reports/meta_alpha/TRIAL_LEDGER_CHAIN.json`, chaîne revérifiée
valide après ajout.

## Contenu gelé (rappel, sans modification)

- Famille F-G « Forme des trajectoires journalières », cinq
  comparaisons fermées C6-01..C6-05, famille BY préenregistrée de cinq
  à m = 5 fixe (H₅ = 2,283333), lectures fermées incluant
  STRUCTURELLEMENT_NON_EVALUABLE.
- Définitions segmentaires : L intra-segment uniquement, Δ_seg sur la
  même population que L (ER ≤ 1 démontré), Δ_jour jamais en ratio avec
  L, D = Σ|g_i|, ρ = part des discontinuités observées dans le parcours
  mesuré (jamais la proportion réelle du non-observé).
- Priorité des statuts de journée : (1) L = 0, D = 0 → PLATE OBSERVÉE
  (ER et ρ indéfinies si dénominateurs nuls) ; (2) L = 0, D > 0 →
  INDÉTERMINÉE — DISCONTINUITÉS (ρ = 1 publiable en descriptif, sans
  reclassification) ; (3) L > 0, ρ > 0,5 → DOMINÉE PAR LES
  DISCONTINUITÉS OBSERVÉES ; (4) autres cas → éligibilité de couverture
  cumulée (trou de session ≤ 15 min, cumul ≤ 30 min, taux ≥ 95 %),
  DÉPLACEMENT FAIBLE (|Δ_seg| < 5 bp, prioritaire), classes ER
  (≤0,10 / 0,10–0,30 / ≥0,30).
- **PLATE OBSERVÉE décrit exclusivement les observations disponibles ;
  ce statut ne constitue pas une preuve d'immobilité du marché pendant
  les périodes non observées.**
- Règle B15 (fenêtre UTC fixe 21:00–22:00, option A, conditions
  simultanées, HALTE_INDÉTERMINÉE sans exemption en cas de doute),
  règle prudente C6-01 à priorité figée (CONTRÔLE_INDÉTERMINÉ →
  FRAGILE_SIGNE → FRAGILE_MATÉRIALITÉ → ROBUSTE, aucune p additionnelle),
  C6-02 (ER seul test ; S sans p ni q ; déclassement borné par
  |ln(ratio)| vs ln(1,15)), seuil de 30 minutes = matérialité seule de
  C6-04.

## Intégrité et restrictions

Aucun calcul F-G, aucune extraction exploratoire, aucune consultation
de résultats n'a eu lieu pendant la préparation ni pendant le gel.
Aucune formule ne peut plus être modifiée : toute correction ultérieure
exigerait un addendum chaîné distinct, avant exécution. Restrictions
inchangées : XAU/USD exclusivement ; holdout 2020–2026 scellé ; aucun
backtest stratégique ni `challenge_sim` ; aucun J2/J3 automatique ;
aucun budget expérimental consommé ; FRED suspendue ; 36 cellules S12
gelées ; T0 séparé et inactif ; aucune modification des fiches
historiques ; F-H et F-I en réserve.

**STATUT : PROTOCOLE F-G DÉFINITIF GELÉ (seq239) — EXÉCUTION EN
ATTENTE D'UN ORDRE DISTINCT DU PROPRIÉTAIRE.**
