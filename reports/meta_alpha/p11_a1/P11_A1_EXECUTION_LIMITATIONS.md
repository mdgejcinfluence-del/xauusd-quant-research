# P11-A1 — LIMITES CONCERNANT L'EXÉCUTION RÉELLE

Ce document borne ce que les cotations reconstituées **ne peuvent pas** établir. Il
fait partie du verdict : le C du rapport principal porte sur les conditions de
cotation, pas sur l'exécution.

## 1. Trois objets distincts, souvent confondus

| Objet | Ce que P11-A1 en sait |
|---|---|
| **Spread observé** | Mesuré tick par tick, minute par minute (rapport §A) : revenu à l'habituel dès T+1 en médiane |
| **Déplacement du prix** | Le premier mouvement (médiane 11,4/12,3/6,8 bp FOMC/NFP/CPI, atlas M2) se produit dans la minute 0 ; c'est un déplacement réalisé, antérieur à toute entrée post-annonce augmentée d'une latence — décrit, jamais assimilé à un rendement |
| **Slippage** | Écart entre prix coté à la décision et prix effectivement obtenu. **NON MESURABLE** : le programme ne contient aucun fill réel. Il n'est ni nul ni estimé dans cet audit |

## 2. Ce qu'une cotation ne prouve pas

- Une cotation affichée dans le flux historique ne garantit pas qu'un ordre transmis
  par un particulier à cet instant aurait été exécuté, ni à ce prix : latence réseau,
  files d'exécution du courtier, requotes et élargissements propres à chaque venue
  sont absents du corpus.
- Le flux du corpus est le flux de référence du programme ; un compte retail chez un
  courtier donné reçoit des cotations qui peuvent différer (marquage du spread,
  politique d'exécution), dans des proportions inconnues du dépôt.
- Les pointes tick de la minute 0 (spreads maximaux > 20 bp au P90 des événements
  FOMC/NFP, P99 tick 5–9 bp en médiane) coïncident avec l'ajustement de prix : ce sont
  précisément les instants où l'écart cotation/exécution peut être maximal, et où un
  ordre au marché paie le déplacement en cours, pas celui qui reste.

## 3. Ce qu'il faudrait pour trancher l'exécution (hors mandat actuel)

- Un journal d'exécutions réelles (même en démo) horodaté à la milliseconde avec prix
  demandés/obtenus — le programme n'en possède pas et P11-A1 n'en crée pas.
- Ou, à défaut, un protocole où le slippage entre comme **inconnue bornée par scénarios
  déclarés** (jamais comme mesure), ce qui relève de la proposition éventuelle évoquée
  au rapport principal, soumise à autorisation explicite.

## 4. Conséquence pour toute suite

Même sous verdict C, aucune conclusion de rentabilité n'est permise : rentabilité =
déplacement post-entrée − (spread + commission + slippage), et deux des termes de
droite (déplacement capturable post-T+1, slippage) restent non mesurés à ce jour — le
premier par interdiction de tester un signal pendant P11-A1, le second par absence
structurelle de données d'exécution.
