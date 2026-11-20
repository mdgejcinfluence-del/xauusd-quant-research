# P11-A1 — RECONSTITUTION DESCRIPTIVE DES TICKS NEWS T−5 À T+30

**Autorisation propriétaire seq 141. Descriptif strict** : aucun signal testé, aucun PnL
stratégique, aucune optimisation, aucune meilleure minute recherchée, budget expérimental
inchangé, F15 non rouvert, holdouts intacts, Phase 11 stratégique toujours verrouillée.
Corpus : tick historique du programme (lac Kaggle, repli miroir Drive du même corpus —
voir annexe qualité), traité en CI (run 44691627613), corpus brut jamais versé dans Git.

**Couverture : 326 événements extraits sur 346 événements réels recensés en P11-A0
(94,2 %)** — FOMC 81/81, NFP 118/129, CPI 127/136. Les 20 manquants relèvent de
partitions non récupérées (voir `P11_A1_DATA_QUALITY.md`). Chaque événement est décrit
minute par minute de T−5 à T+30 (`P11_A1_EVENT_MINUTES.csv`, 11 736 lignes ;
`P11_A1_EVENT_METRICS.csv`, événement par événement ; `P11_A1_BY_MINUTE.csv`).

## A. Le spread réellement observé dans le flux (conclusion séparée)

Spread coté médian **à l'intérieur de chaque minute** (médiane des spreads tick de la
minute, puis médiane entre événements ; bp) :

| Famille | Pré-annonce (T−5→T−1, méd.) | Minute 0 | T+1 | T+2 | T+3 | T+4 | T+5 |
|---|---|---|---|---|---|
| FOMC | 2,68 | 3,07 | 2,91 | 2,82 | 2,68 | 2,64 | 2,75 |
| NFP | 2,50 | 3,82 | 2,86 | 2,72 | 2,61 | 2,54 | 2,47 |
| CPI | 2,28 | 2,62 | 2,37 | 2,33 | 2,30 | 2,31 | 2,30 |

Quantiles entre événements du spread médian de minute (bp) : à T+1, P90 = 4,9/4,6/3,2,
P95 = 5,6/5,4/3,9, P99 = 11,5/7,9/4,8 (FOMC/NFP/CPI). Au niveau tick dans la minute 0,
le spread P99 médian atteint 5,3/9,2/4,6 bp et le maximum tick par événement dépasse
20 bp au P90 (FOMC/NFP) : **des pointes brèves existent, mais elles sont des pointes** —
la médiane de minute n'explose à aucun moment.

Durée et retour : le nombre médian de minutes à spread > 2× le niveau pré-annonce de
l'événement, sur T0→T+30, est de **0** pour les trois familles (P90 = 1 minute FOMC/NFP,
0 CPI) ; la première minute repassant sous 1,5× le pré-annonce est la minute 0 en médiane
(P90 : 1–2 min) ; seuls 1,2 % des FOMC ne repassent pas sous ce seuil en 30 min.

**Conclusion A :** dans ce flux, le spread coté se dégrade modérément pendant la minute
de l'annonce (surtout NFP), porte des pointes tick brèves, et revient à son niveau
habituel dès T+1 en médiane. Le « mur de spread » présumé sur T+1→T+5 n'apparaît pas
dans les cotations. Ce n'est pas une conclusion sur l'exécution (voir §D du rapport
`P11_A1_EXECUTION_LIMITATIONS.md`), ni sur la rentabilité.

## B. Qualité et disponibilité des cotations (conclusion séparée)

- Densité : médiane de ticks par minute T0 = 269 (FOMC), 329 (NFP), 258 (CPI), contre
  ~95–160 en pré-annonce ; intervalle médian entre ticks ≈ 0,10–0,14 s pendant
  T0→T+5, contre 0,22–0,33 s avant.
- Trous : trou maximal médian dans T0→T+5 = 3,6 s (CPI), 3,0 s (FOMC), 2,0 s (NFP) ;
  P95 ≤ ~21 s. Aucune minute couverte à 0 sur les événements extraits (couverture
  médiane 36/36 minutes).
- Bid/Ask et prix médian sont présents à chaque tick (moteur : bid, ask, mid par
  cotation ; premiers bid/ask et mid de début/fin de minute dans le CSV).

**Conclusion B :** pendant les minutes qui suivent l'annonce, le flux cote de façon
dense et continue. Il n'y a pas de « désert de cotations » T+1→T+5 dans ce corpus.

## C. Estimations éventuelles de coûts (conclusion séparée)

Coûts **mesurés** : spread coté (§A). Ancre aller-retour incluant commission par config :
C1_hist 3,33 bp / C1_BG 4,7 bp (rappel, configurations existantes). Par rapport au spread
seul mesuré à T+1 (médiane des médianes 2,4–2,9 bp, P95 3,9–5,6 bp), l'ordre de grandeur
aller-retour complet reste celui des ancres historiques.

Coûts **non mesurés** : slippage réel (aucune donnée d'exécution dans tout le
programme), latence d'un ordre retail, probabilité de remplissage au prix coté. Aucune
estimation chiffrée de slippage n'est produite : elle ne reposerait sur aucune mesure.

## D. Limites concernant l'exécution réelle chez un courtier retail

Développées dans `P11_A1_EXECUTION_LIMITATIONS.md`. En résumé : ces cotations sont
celles du flux historique du corpus (flux de référence du programme), pas celles d'un
compte retail donné ; une cotation affichée ne prouve ni l'exécution ni le prix obtenu ;
les pointes tick de la minute 0 (max > 20 bp au P90 des événements FOMC/NFP) sont
exactement les instants où l'écart cotation/exécution peut être le plus grand ; et
l'essentiel du déplacement de prix se produit dans la minute 0, avant tout instant
d'entrée postérieur à `available_at_utc` augmenté d'une latence réaliste — question de
**déplacement**, distincte du spread, que le présent audit décrit sans la convertir en
stratégie.

## Verdict obligatoire

**C — Conditions de cotation justifiant la proposition d'un futur protocole statistique.**

Motivation bornée au mandat : les conditions de **cotation** T+1→T+5 (spread revenu à
l'habituel dès T+1 en médiane, flux dense et continu, couverture 94,2 % des événements)
ne ferment plus la porte qui était présumée fermée en P11-A0 ; la question restante —
existe-t-il, après la minute 0, un déplacement capturable net des coûts mesurés, et un
ordre retail y serait-il exécuté — est une question **statistique et d'exécution**, pas
une question de cotation, et elle n'a reçu ici aucune réponse. Le verdict C n'est pas
un edge, ne certifie rien, ne préenregistre rien et ne démarre rien : il constate
uniquement qu'une proposition de protocole préenregistré, soumise au propriétaire,
serait fondée sur des mesures réelles plutôt que sur la présomption réfutée des deux
côtés (ni « mur de spread » ni capturabilité démontrée).

Toute proposition éventuelle devra, pour être recevable : (i) être préenregistrée et
chaînée avant tout calcul ; (ii) n'utiliser que des entrées ≥ T+1 min avec prix
exécutables bid/ask (jamais le Mid) ; (iii) intégrer les distributions de spread
mesurées ici (pas une ancre forfaitaire seule) ; (iv) traiter le slippage comme
inconnue bornée par scénarios déclarés, jamais comme zéro ni comme mesuré ;
(v) respecter les gates inchangés et un micro-budget créé par ordre explicite.
**Aucune expérience ne démarre sans autorisation explicite du propriétaire.**

## Sécurité (rappel de l'autorisation)

La clé FRED n'a été ni réutilisée, ni affichée, ni copiée pendant P11-A1 (aucun appel
FRED) ; sa rotation par le propriétaire reste requise avant toute exécution nécessitant
FRED. Budgets expérimentaux vérifiés inchangés en tête des livrables.

*Livrables : présent rapport ; `P11_A1_EVENT_METRICS.csv` (326 événements) ;
`P11_A1_BY_MINUTE.csv` ; `P11_A1_EVENT_MINUTES.csv` (11 736 lignes minute) ;
`P11_A1_DATA_QUALITY.md` ; `P11_A1_EXECUTION_LIMITATIONS.md`. Chaîne : seq 141 →
seq 142. Décision finale : propriétaire, après lecture des preuves.*
