# CAMPAGNE 2 — LIMITES DES DONNÉES ET DE LA DÉTECTION

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Limite | Portée |
|---|---|
| Couverture familles | Détection limitée aux familles mesurées seq 155/157/160 : EV1, EV2, EV3, EV5, EV6, EV4, EV7 (non testée : 129 journées seulement, seuil poolé non daté — aucune comparaison EV7 n'entrait dans les 24 tests), ouvertures Londres/New York |
| Ouvertures d'Asie | **NON MESURÉES** (fenêtre avant ouverture à cheval sur la borne de journée du traitement 1.1) ; aucune détection sur ce contexte |
| F7 | Hors périmètre : la série horaire du modèle gelé n'existe pas dans le dépôt ; aucune approximation substituée (document campagne 1.1) |
| Terciles par ère | Bornes calculées sur l'ère entière (limite rétrospective écrite dans l'audit statistique) ; pas de seuils roulants strictement causaux dans cette campagne |
| Censure 60 min | Fenêtre gelée seq 157 : les non-réintégrations au-delà de 60 min sont invisibles ; aucun modèle de survie ajusté (descriptif seul) |
| Dépendance inter-journées | Bootstrap par grappes jour×niveau ; la persistance temporelle de la volatilité entre journées voisines n'est pas modélisée — IC des contrastes d'ère potentiellement optimistes |
| Granularité minute | Délais entiers en minutes ; médianes et IC affectés (T03) |
| Prix / coût | Mid descriptif déclaré ; spread = contexte médian à l'événement ; aucun coût de transaction appliqué à un quelconque gain (il n'y a pas de gain) |
| Régime F3 | Jours NON_CLASSE exclus des bras régime (n réduit, publié par test) ; régime = prévision de volatilité, jamais directionnel |
| Multiplicité | BY sur la famille fermée des 24 ; toute comparaison lue hors de cette famille (y compris dans ce document) est une lecture, pas un test |
| Échantillon | IS seul (282 partitions, borne 2020-01-20) ; holdout jamais accédé ; aucune confirmation chronologique disjointe n'a été exécutée — elle relèvera, le cas échéant, d'une autorisation J2 distincte |
