# CAMPAGNE 5 — REGISTRE DES CENSURES ET DONNÉES MANQUANTES

Toutes les exclusions ci-dessous résultent des règles gelées
V2 + V2.1 + V2.2, appliquées sans assouplissement.

## Corpus et journées
- Partitions chargées : 282/282 ; barres M1 : 3 540 993.
- Journées présentes : 3 097 ; journées utilisables : 2 572 ;
  525 journées EXCLUE (usage F-F) et 1 SANS_REFERENCE (premier jour,
  pas de référence veille).
- Statut de journée (qualité générale, seuil 95 % — jamais une preuve
  d'absence) : COMPLETE 395, PARTIELLE 2 177, EXCLUE 525.
- CONTENUE ETABLIE (1 440/1 440 minutes) : **0 journée** sur 2 571 à
  usage OK — voir C5-10.

## Ouvertures (F-E)
- Lignes d'ouvertures : 10 288 ; éligibles 9 190 ; inéligibles 1 098
  (règles de retard gelées ; dont les 2 ouvertures d'Asie des journées
  TROU_INTRA_SEMAINE de C5-03, retards 180 et 45 min).
- Fenêtres éligibles — 5 min : COMPLETE 8 788 / CENSUREE 402 ;
  15 min : 8 709 / 96 / 385 ; 30 min : 8 336 / 198 / 656 ;
  60 min : 8 172 / 351 / 667 (COMPLETE/PARTIELLE/CENSUREE).
  Aucun observable publié n'est calculé silencieusement sur fenêtre
  incomplète : tout PARTIELLE est compté et publié, les parts par bras
  figurent au rapport F-E (maximum 1,36 %, aucun avertissement requis).
- C5-02 : MOUVEMENT_NUL 3 (hors dénominateur), issues CENSURE 275.

## Atteintes (F-F)
- Journalières : 2 375 premières atteintes ; REELLES IDENTIFIABLES
  2 004 ; OBSERVEES 371 (minutes manquantes avant l'atteinte —
  censurées de C5-06..08, publiées séparément, jamais présentées comme
  premières réelles). Par côté : HAUT 1 022 réelles / 199 observées ;
  BAS 982 / 172.
- Hebdomadaires : 504 lignes (457 semaines touchées sur 520) ; REELLES
  IDENTIFIABLES 187 ; OBSERVEES 317 (continuité depuis lundi 00:00 UTC
  incomplète) — censurées de C5-09.
- Touches (contact sans franchissement strict) : 7, publiées à part
  (`CAMPAIGN_05_TOUCHES.csv`), hors comparaisons, comptées comme
  événements au dénominateur de C5-10 conformément au gel.
- Atteintes simultanées opposées dans la même barre : 0
  (`CAMPAIGN_05_ORDRE_INDETERMINE.csv` vide, publié tel quel).
- Censures de suivi +60 min (C5-07) : HAUT 2, BAS 7.
