# PHASE 16 — AUDIT DE REMPLISSABILITÉ DES ORDRES LIMITES (AVANT TOUT CALCUL)

**Objet : déterminer, à partir des artefacts et des schémas déjà
produits (Phases 10 à 15), ce que les données tick IS permettent de
prouver au sujet du remplissage d'un ordre limite. Aucune nouvelle
extraction n'a été effectuée pour cet audit.**

## 1. Nature des données tick disponibles

Les partitions tick IS (Kaggle privé du propriétaire, agrégées en
Phases 10/12/13/14 par des requêtes DuckDB committées) contiennent,
par observation : un horodatage UTC (`timestamp_utc`, résolution
milliseconde dans les footers d'inventaire), un **Bid**, un **Ask**
(et le Mid dérivé). Les barres M1 Bid/Ask des Phases 13-B/14/15 en
sont des agrégats directs (premier/dernier tick, extrêmes). Aucun
artefact du programme ne contient :

- de prix de **transactions réellement exécutées** (trades) ;
- de **volume** échangé, ni de taille associée aux cotations ;
- de **profondeur de carnet** (niveaux au-delà du meilleur Bid/Ask) ;
- d'information de **file d'attente** ou de priorité d'exécution ;
- d'identifiant de contrepartie ou de statut d'ordre.

La signature de schéma des partitions (inventaire exhaustif
`INVENTORY_348_EXHAUSTIVE.json`) et toutes les requêtes committées
(`phase10_engine.charger`, moteurs 12-C/13-B/14/15) ne lisent que
`timestamp_utc`, `bid`, `ask`, `mid` (et `observation_id` dans les
footers). Il n'existe donc, dans le périmètre autorisé, **aucune
preuve de transaction** permettant d'établir qu'un ordre limite
aurait été servi, ni à quel rang, ni pour quelle quantité.

## 2. Conséquences pour la politique E3

- Un passage de cotation au-delà de `P_limit` (critères stricts
  gelés : `Ask < P_limit` en long, `Bid > P_limit` en court) prouve
  qu'un prix de marché a traversé le niveau ; il ne prouve ni
  l'exécution d'un ordre placé, ni son prix effectif au-delà de la
  convention retenue (`P_limit`, sans amélioration supposée).
- Le statut de qualité d'exécution de toute la Phase 16 est donc
  fixé ex ante : **`QUOTE_CROSSING_PROXY_ONLY`**. Le statut
  `TRADE_FILL_SUPPORTED` est **inaccessible** avec les sources
  autorisées et ne pourra pas être prononcé ; prétendre le
  contraire exigerait des données de transactions qui n'existent
  pas dans le programme (leur recherche éventuelle serait une
  décision distincte, hors périmètre).
- Ce que l'étude peut honnêtement mesurer : le **taux de
  franchissement** dans la fenêtre de 60 secondes, le **délai** de
  franchissement, l'**amélioration théorique de prix** (demi-spread
  initial, mécanique), et les conséquences économiques
  *conditionnelles au franchissement* — toujours présentées comme
  un proxy, aux côtés de la cohorte entière où les non-franchis
  comptent 0.
- Aucune quantité disponible, aucune priorité de file, aucun taux
  de remplissage partiel ne seront inventés.

## 3. Verdict de l'audit

`QUOTE_CROSSING_PROXY_ONLY` — l'étude Phase 16 est réalisable
comme mesure de franchissement de cotations et de ses conséquences
théoriques, sous étiquetage explicite ; elle ne peut pas établir
l'exécutabilité réelle d'ordres limites. Ce verdict est gelé
avant tout calcul et ne dépend d'aucun résultat.
