# RE-ENTRY-001 — RECONSTRUCTION DE LA STRATÉGIE « COLORFUL DROPS » (HFM 99001292, XAUUSDc)

## A. Inventaire autonome (exécuté, rien demandé à l'utilisateur)
- Dépôt GitHub : **aucun** fichier HTML HFM, aucun historique du fournisseur 99001292 (recherche
  nominative exhaustive). Google Drive (connecteur actif, recherché) : **aucun** fichier HFM /
  Colorful / 99001292 / XAUUSDc. Kaggle : aucun dataset de transactions du fournisseur.
- Ressources réelles utilisées : les **6 transactions de référence du 2026-11-26** fournies dans
  l'ordre de mission (heures affichées, sens, volumes, profits de panier 11 et 13 — sans prix,
  fuseau non indiqué) ; les **ticks Dukascopy du 2026-11-26** (collecte prospective du projet,
  complétée ce cycle jusqu'à couvrir la fenêtre ; Bid/Ask ms UTC, `DUKASCOPY_PRIMARY` —
  référence comparative, jamais présentée comme cotation HFM) ; les spécifications XAUUSDc
  observées (compte Cent, contract size 1) consignées en seq431, non rétro-appliquées.

## B. Fuseau horaire — déterminé par cohérence économique (balayage préenregistré UTC+0..+5)
Seul **UTC+2** rend les **deux** paniers positifs sur les prix Dukascopy, dans le même ordre
que les profits affichés (A +0,070 < B +0,100 pour 11 < 13) ; UTC+3 rend A nettement négatif,
UTC+0/+4/+5 contredisent au moins un signe. UTC+2 est aussi le fuseau serveur usuel des entités
HFM en heure d'hiver. Statut : **FORTEMENT ÉTAYÉ** (serveur GMT+2), non confirmé tant qu'un
export horodaté du terminal n'a pas été confronté.

## C. Première entrée — suivi d'impulsion haussière (2/2 paniers, UTC+2)
Avant la première entrée : A +11,7 bp sur 5 min (+6,3 bp/3 min, +5,6 bp/1 min), prix à **83 %**
du range des 15 dernières minutes ; B +11,4 bp sur 5 min, prix à **81 %** du range. Les deux
premières entrées sont des Buy pris **après une impulsion haussière établie, près du sommet
récent** — cohérent avec la déclaration du profil (« trend-following »). Aucun indicateur n'a
été testé : l'observation (impulsion + position haute dans le range) précède toute hypothèse
d'indicateur. Statut : **FORTEMENT ÉTAYÉ** sur 2 paniers ; le seuil exact (amplitude, fenêtre)
reste **NON DÉTERMINABLE** avec n=2.

## D. Renforcements — contre le mouvement, pas en pyramide (H1 étayée, H2 réfutée sur ces cas)
Déplacements depuis la première entrée, au moment des ajouts : A −4,1 bp (ajout 2, +40 s) puis
−6,6 bp (ajout 3, +180 s) ; B −3,0 bp (+29 s) puis −4,7 bp (+598 s). Les ajouts surviennent
**lorsque le prix recule contre les Buy ouverts**, à des distances de quelques bp et des délais
de dizaines de secondes à ~10 min : **H1 (renforcement martingale) FORTEMENT ÉTAYÉE** ;
H2 (pyramiding favorable) contredite par les deux paniers ; H4 (périodique pur) contredite par
les intervalles irréguliers (40/180 s ; 29/598 s) ; H3 non requise à ce stade. La distance
déclencheur exacte (fixe en bp ? en multiple du spread ? perte flottante ?) : **NON DÉTERMINABLE**
avec 2 paniers — les ajouts 2 surviennent tôt (−3 à −4,5 bp) dans les deux cas.

## E. Volumes — séquence 0,01 → 0,01 → 0,02 (identique sur les deux paniers)
Le doublement n'intervient qu'à la **troisième** position ; exposition finale 0,04 lot par
panier, prix moyen abaissé à chaque ajout (A : entrée moyenne ≈ 3567,4 pour une première à
3568,8). Compatible avec une grille à multiplicateur différé (×1, ×1, ×2) ; incompatible avec
une martingale classique dès le second trade (qui doublerait à l'ajout 2). Règle complète
(position 4+ ?) : **HYPOTHÈSE À TESTER** sur d'autres paniers.

## F. Clôtures — sortie de panier en profit après retour au-dessus du prix moyen
A se ferme (19 min 12 s) quand le Mid (3569,47) repasse au-dessus du prix moyen du panier ;
B se ferme (11 min 55 s) de même (3570,88 contre moyenne ≈ 3568,0) ; clôtures groupées à la
seconde près. Le fait décisif : **B s'ouvre 2 secondes après la clôture de A** — la machine
enchaîne immédiatement un nouveau panier tant que l'impulsion de fond persiste. Objectif chiffré
exact (points, devise, % du panier) : **NON DÉTERMINABLE** sans les prix HFM réels ; le
mécanisme « take-profit de panier au retour au-dessus du prix moyen pondéré » est
**FORTEMENT ÉTAYÉ**. Échelle de grandeur : profits reconstruits +0,070/+0,100 USD par unité de
contrat contre 11/13 affichés — la conversion exacte dépend de la devise du compte (¥ affiché)
et du contract size Cent ; seul l'ordre et les signes sont utilisés comme preuve.

## G. Comparaison des modèles (explication, pas rentabilité)
A (tendance seule) : explique les premières entrées, **pas** les ajouts contre le mouvement.
B (tendance + renforcement défavorable) : explique entrées, ajouts, volumes et clôtures des
deux paniers — **modèle retenu comme le plus explicatif**. C (renforcement favorable) :
contredit par les déplacements mesurés. D (hybride variable) : inutile à ce niveau de preuve.

## H. Risques (profil + mécanique reconstruite)
Profil affiché : 67,37 % de transactions positives mais gain moyen (22) **inférieur** à la perte
moyenne (28) — signature comptable d'un système à paniers martingale (beaucoup de petits gains
de panier, pertes unitaires plus grosses), drawdown maximal affiché 31,81 %. La mécanique
reconstruite implique : exposition croissante contre la tendance (0,01→0,04 dès 3 positions,
progression au-delà inconnue), perte flottante maximale non bornée par un stop observé, et
risque de panier qui ne revient jamais au prix moyen (chute prolongée de l'or après une
impulsion). Aucun des deux paniers de référence n'illustre l'échec ; l'échantillon est biaisé
vers des cycles complets et gagnants — le risque de queue reste **HYPOTHÈSE À TESTER** sur un
historique de transactions plus large, pas mesuré ici.

## I. Prochaines étapes (sans solliciter de fichier que l'environnement peut produire)
1. Élargir l'échantillon : toute page d'historique du fournisseur accessible publiquement ou
   exportable depuis le compte copié du fondateur (le cas échéant) multiplierait les paniers —
   c'est la seule ressource qui lèverait les NON DÉTERMINABLE (seuils, position 4+, objectif).
2. À défaut, observation prospective : notre collecte Dukascopy + le replay existant permettent
   de tester le Modèle B **préenregistré** en descriptif sur d'autres impulsions (sans jamais le
   valider sur le holdout ni le présenter comme la stratégie du trader).
3. Le fuseau serait confirmé par un seul export MT4/MT5 horodaté du compte suiveur, si le
   fondateur en dispose déjà — aucune création de compte n'est requise par cette mission.
