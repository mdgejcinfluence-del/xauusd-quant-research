# PHASE 13-A.1 — RAPPORT DE VALIDATION DU CONTRAT ÉCONOMIQUE

**Nature : validation documentaire de cohérence. Aucun accès au
holdout, aucune extraction, aucun backtest, aucune simulation,
aucun calcul économique effectués.**

## 1. Préflight

- Chaîne de traçabilité valide avant mission : 328 entrées, tête
  seq328 `08e81d5596af…` ; autorisation 13-A.1 chaînée en seq329
  (`8a36d53e…`).
- Commit de référence vérifié : HEAD = distant `b69e226` (Phase
  13-A), arbre propre avant écriture.
- Livrables 13-A reverifiés **inchangés** (SHA-256 identiques à
  seq328) : protocole `a4d85f00911ceb1f…`, contrat V1
  `03e1f7eb755aebafd…`, inventaire `c9b5e9c75aebc0631…`,
  faisabilité `24fc1097fcfca2fd…`, préenregistrement V1
  `56d408f3beee1073…`. Aucun ancien document n'a été écrasé : la
  correction passe par un addendum et des versions V2.

## 2. Critères du verdict et contrôles effectués

Contrôles automatisés de cohérence inter-documents (parsing JSON,
constantes, chaînes normatives) — **tous conformes** :

| Critère | Contrôle | Résultat |
|---|---|---|
| Entrée strictement postérieure à la confirmation | Fenêtre `t_decision < quote_timestamp < t_decision + 60 secondes` (bornes strictes) présente à l'identique dans l'addendum, le contrat V2 et le préenregistrement V2 ; `p_M1` calculé après la clôture ; NON_EXECUTION sinon ; ticks Bid/Ask réels, jamais de Mid reconstruit | CONFORME |
| Sortie aux prix exécutables corrects | Sortie unique à la clôture de la fenêtre de 8 bougies H1 ; Bid (long) / Ask (court) de clôture de la dernière minute M1 ; horodatages conservés ; censure motivée, jamais prolongée | CONFORME |
| Spread compté une seule fois | Mention normative « intégré une seule fois par les prix Bid/Ask » dans l'addendum, la convention de coûts et le contrat V2 ; convention Mid Phase 10 explicitement exclue | CONFORME |
| Commissions explicitement exclues | `COMMISSION_EXCLUDED_BY_DESIGN` concordant dans les trois documents normatifs ; étiquette obligatoire `NET_OF_SPREAD_BEFORE_COMMISSION_AND_SLIPPAGE` partout ; interdiction de « rentabilité nette démontrée » | CONFORME |
| Trois scénarios de slippage entièrement définis | Grille S0/S1/S2 = 0 / 0,5 / 1,0 bp par côté (aller-retour 0 / 1,0 / 2,0 bp) identique dans la convention de coûts, le contrat V2 et le préenregistrement V2 ; formules de dégradation défavorable par côté et par direction ; statut hypothétique, non mesuré ; aucun scénario ajoutable après observation des résultats | CONFORME |
| Règle d'exposition inchangée | `p_M1 > 0.7591463414634146` (M0 gelé) identique dans tous les documents ; modèle H1 gelé référencé par son SHA-256 `1bcb3b70…` | CONFORME |
| Concordance générale | Verdicts `ECONOMIC_CONTRACT_FROZEN` concordants (contrat V2 et préenregistrement V2) ; conditions d'arrêt (> 10 % NON_EXECUTION, > 5 % spreads non finis) reprises ; holdout 2020–2026 exclu partout ; H4 exclu | CONFORME |

## 3. SHA-256 des livrables 13-A.1

- `PHASE13A1_CAUSAL_EXECUTION_ADDENDUM.md` :
  `4b3d9265abadbe8d4d4456d59949958f67c4bed4c631ffc119dac75562fabbb0`
- `PHASE13A1_COST_CONVENTION.json` :
  `e7e273667418f894847fb82d28ff4dbf72458cd183274dca9f1cf6dd17fc5f7a`
- `PHASE13A1_EXECUTION_CONTRACT_V2.json` :
  `86ae5d3436962b36289beae8392df5e75676e79050833cc0620b949ffbc558a7`
- `PHASE13A1_PREREGISTRATION_V2.json` : voir SHA-256 calculé au
  checkpoint (consigné dans l'entrée de chaîne du verdict).

## 4. Verdict

**`ECONOMIC_CONTRACT_FROZEN`** — l'entrée est strictement
postérieure à la confirmation (`t_decision < quote_timestamp <
t_decision + 60 s`, ticks Bid/Ask réels), la sortie est définie
aux prix exécutables corrects (Bid long / Ask court à la clôture
de la fenêtre de 8 bougies H1), le spread n'est compté qu'une
fois, l'exclusion des commissions est explicitement assumée
(`COMMISSION_EXCLUDED_BY_DESIGN`, étiquette
`NET_OF_SPREAD_BEFORE_COMMISSION_AND_SLIPPAGE`), et les trois
scénarios de slippage hypothétiques sont entièrement définis et
gelés. Tous les documents concordent.

Ce gel n'autorise ni extraction, ni backtest, ni simulation, ni
stratégie. La Phase 13-B (étude économique exploratoire sur l'IS,
niveau 2) reste soumise à une décision distincte ; toute
validation économique complète future exigera en outre un barème
de commissions réel documenté ou une exclusion explicitement
justifiée, consignée par décision chaînée.
