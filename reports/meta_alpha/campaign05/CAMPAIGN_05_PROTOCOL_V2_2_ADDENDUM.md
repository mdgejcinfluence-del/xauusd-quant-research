# CAMPAGNE 5 — ADDENDUM FORMEL V2.2 AU PROTOCOLE V2 + ADDENDUM V2.1

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE — AUCUN
CALCUL LANCÉ, AUCUN RÉSULTAT DE CAMPAGNE 5 CONSULTÉ.** Addendum produit
après validation conditionnelle (seq 217). Il précise, sur les seuls
points énumérés, le protocole V2 (sha256
`818837fd5fb500b2906685367ea72acc18c2b5ddfce64de3bdfe5c8239818331`) et
l'addendum V2.1 (sha256
`509a2863ca633a6f6ad985fe55223b97a1bb743e1011e2cb6a966d59ad67bd45`),
tous deux conservés inchangés. En cas de tension entre V2.1 et le présent
texte, **le V2.2 prévaut** sur les quatre points ci-dessous. Ensemble
V2 + V2.1 + V2.2 soumis à validation définitive.

## Correction 1 — Frontières temporelles : « avant B » contre « au plus tard à B »

Chaque événement conserve deux horodatages distincts : **début de barre**
(date de l'événement) et **heure de disponibilité** (début + 1 minute,
clôture de la barre M1). Deux prédicats, jamais confondus :

- **avant B** : disponibilité **strictement inférieure** à B ;
- **au plus tard à B** : disponibilité **inférieure ou égale** à B.

Application aux trois frontières des comparaisons (toutes utilisent le
prédicat **avant**, au sens strict) :

| Comparaison | Règle définitive (disponibilité) | Équivalent en début de barre |
|---|---|---|
| C5-06 — première atteinte **avant 08:00 UTC** | disponibilité **< 08:00** | barre débutant au plus tard à **07:58** |
| C5-08 — formées **avant 13:00** / **à partir de 13:00** | avant : disponibilité **< 13:00** ; à partir de : disponibilité **≥ 13:00** | avant : début ≤ 12:58 ; à partir de : début ≥ 12:59 |
| C5-09 — première atteinte hebdomadaire **avant mercredi 00:00 UTC** | disponibilité **< mercredi 00:00** | barre débutant au plus tard à **mardi 23:58** |

La formulation du V2.1 pour C5-06 (« au plus tard à 08:00 », barre de
07:59) est **abrogée** : une barre débutant à 07:59 n'est disponible qu'à
08:00, donc pas « avant 08:00 ». Aucune comparaison de la campagne
n'utilise le prédicat « au plus tard à » ; il est défini ici pour
interdire toute réintroduction ambiguë.

## Correction 2 — Première atteinte réelle identifiable contre première atteinte observée

**Principe** : toute minute manquante avant un événement peut avoir
caché un franchissement antérieur non observable (y compris un
franchissement suivi d'un retour pendant l'absence — les données ne
permettent pas de l'exclure). Deux statuts, jamais confondus :

- **ATTEINTE REELLE IDENTIFIABLE** : franchissement strict dont **toute
  la période d'observation antérieure dans la période est continue**,
  c'est-à-dire aucune minute manquante entre le début de la période
  (00:00 UTC du jour pour le journalier ; **lundi 00:00 UTC** pour
  l'hebdomadaire) et l'heure de disponibilité de l'événement — chaque
  minute attendue y est représentée par une barre présente. « Minute
  manquante » = minute d'horloge sans barre M1, quelle qu'en soit la
  cause (trou de cotation, pause, absence de données) : le protocole ne
  prétend pas distinguer ces causes.
- **ATTEINTE OBSERVEE** : premier franchissement strict présent dans les
  barres observées, mais précédé d'**au moins une minute manquante** dans
  la période. Elle est datée et décrite, mais **jamais présentée comme
  la première atteinte réelle** : un franchissement antérieur a pu
  survenir pendant l'absence.

**Règles qui en découlent.**
- Les comparaisons **C5-06, C5-07, C5-08 et C5-09** ne retiennent que les
  atteintes **REELLES IDENTIFIABLES** ; les atteintes OBSERVEES y sont
  **censurées** (motif CENSURE_OBSERVATION), **publiées séparément avec
  leurs effectifs** par côté, par ère et par statut de journée/semaine.
- Pour C5-09, le contrôle de continuité court du **lundi 00:00 UTC
  jusqu'à la disponibilité de l'événement**, à travers toutes les
  journées de la semaine concernée : un seul trou, y compris le lundi ou
  le mardi, fait passer l'atteinte — même observée le mercredi ou
  après — au statut OBSERVEE. Les trous postérieurs à l'événement
  n'affectent pas son statut (ils peuvent censurer ses **issues**, selon
  les règles de fenêtres).
- La censure d'antériorité du V2.1 (trou > 15 minutes) est **absorbée et
  remplacée** par la présente règle, plus stricte : le seuil de 15
  minutes ne sert plus à établir une première atteinte (il continue de
  régir la censure des fenêtres d'issues, correction 4).
- Symétriquement, un **touch** n'est « premier touch réel identifiable »
  que sous la même condition de continuité ; les touch observés après
  une absence sont publiés comme touch observés, hors comparaisons.

## Correction 3 — Journées contenues et C5-10 : la couverture n'est pas une preuve d'absence

**Formule et bornes (précisées)** : le **taux de couverture** d'une
journée = (nombre de barres M1 présentes dont le début tombe dans
[00:00, 24:00)) / **1 440 minutes attendues** × 100. Le statut
**COMPLETE** du V2.1 (qualité générale) exige en outre : taux ≥ 95 %
(≥ 1 368 barres), première barre débutant **au plus tard à 00:10**,
dernière barre débutant **au plus tôt à 23:50**, aucun trou > 30 minutes
entre première et dernière barres. Ce statut est un **critère de qualité
générale** (éligibilités F-E/F-F hors C5-10) ; il ne prouve l'absence
d'aucun événement pendant d'éventuelles minutes absentes.

**Classification pour C5-10 (fait foi)** :
- **CONTENUE ETABLIE** : aucune atteinte ni touch observés **et** les
  **1 440 minutes** de la journée sont représentées (première barre à
  00:00, dernière débutant à 23:59, aucune minute manquante) — seule
  cette observation intégrale établit l'absence d'atteinte et de touch
  pour la journée ;
- **CONTENUE NON ETABLIE** : aucune atteinte ni touch observés, mais au
  moins une minute manquante — publiée, et **exclue du dénominateur
  principal de C5-10** ;
- journées avec atteinte ou touch observés : hors population « contenue »
  par construction.
Le dénominateur de C5-10 = journées CONTENUE ETABLIE + journées avec
atteinte ou touch observés (toutes ères confondues par bras d'ère) ;
numérateur = CONTENUE ETABLIE du bras. Il est publié d'avance que ce
dénominateur peut être faible, voire insuffisant (couverture minute à
minute intégrale rare en présence de pauses de cotation) : la
comparaison serait alors **non éligible**, publiée comme telle, plutôt
qu'assouplie. Le seuil de 95 % n'est pas modifié ; son usage est
désormais explicitement borné à la qualité générale.

## Correction 4 — Contrôle de couverture distinct par fenêtre F-E

Pour **chaque fenêtre** (+5, +15, +30, +60 minutes) de chaque événement
F-E, une ligne de contrôle est produite et publiée (fichier de qualité
des fenêtres), comportant : **barres attendues** (durée de la fenêtre en
minutes : 5, 15, 30, 60), **barres observées** (barres présentes dont le
début tombe dans la fenêtre), **taux de couverture** (observées/attendues
× 100), **trous identifiés** (nombre et durée maximale, en minutes), et
**statut** :

| Statut de fenêtre | Condition | Traitement |
|---|---|---|
| **COMPLETE** | couverture = 100 %, aucun trou | Observables calculés, sans marque |
| **PARTIELLE** | couverture ≥ 90 % et trou maximal ≤ 15 min (fenêtre 60) ou ≤ 5 min (fenêtres 5/15/30) | Observables calculés et publiés **avec la marque « fenêtre partielle » et son taux** ; jamais présentés comme une observation intégrale |
| **CENSUREE** | couverture < 90 % ou trou au-delà des seuils ci-dessus | Aucune observable calculée sur cette fenêtre ; ligne publiée avec son motif |

Aucune amplitude, RV ou excursion n'est calculée silencieusement sur
une fenêtre incomplète : le statut accompagne chaque observable, les
comptes par statut sont publiés par session et par ère, et les
comparaisons C5-01 à C5-05 n'utilisent que les fenêtres COMPLETE ou
PARTIELLE (parts de PARTIELLE publiées par bras ; si un bras repose à
plus de moitié sur des fenêtres PARTIELLE, sa lecture est publiée avec
cet avertissement, sans exclusion après coup).

## Tableau des dix comparaisons — révisions induites (le reste est inchangé)

| ID | Révision V2.2 |
|---|---|
| C5-01 | Inchangée, sous réserve du contrôle de couverture par fenêtre (correction 4) joint à chaque observable |
| C5-02 | Inchangée (V2.1 correction 4), sous réserve de la correction 4 |
| C5-03 | Inchangée, sous réserve de la correction 4 |
| C5-04 | Inchangée, sous réserve de la correction 4 |
| C5-05 | Inchangée (V2.1 correction 5), sous réserve de la correction 4 |
| C5-06 | Frontière convertie en disponibilité **< 08:00** (début ≤ 07:58) ; population restreinte aux atteintes **REELLES IDENTIFIABLES**, atteintes OBSERVEES censurées et publiées séparément (corrections 1–2) |
| C5-07 | Population restreinte aux atteintes REELLES IDENTIFIABLES ; OBSERVEES publiées séparément |
| C5-08 | Bornes de disponibilité confirmées au sens strict (< 13:00 / ≥ 13:00) ; population restreinte aux atteintes REELLES IDENTIFIABLES |
| C5-09 | Frontière disponibilité < mercredi 00:00 confirmée ; continuité contrôlée **depuis lundi 00:00** ; seules les atteintes REELLES IDENTIFIABLES sont retenues |
| C5-10 | Dénominateur restreint aux journées à observation classificatoire complète : CONTENUE ETABLIE (1 440/1 440 minutes) contre journées avec atteinte/touch observés ; CONTENUE NON ETABLIE publiée hors dénominateur ; non-éligibilité possible assumée d'avance |

## Résumé des changements par rapport au V2.1

1. Prédicats de frontière formalisés (avant = disponibilité
   strictement inférieure ; au plus tard = inférieure ou égale) ; la
   règle C5-06 du V2.1 est abrogée et remplacée par disponibilité
   < 08:00 (début de barre ≤ 07:58) ; début de barre et disponibilité
   restent deux horodatages séparés partout.
2. Statuts **ATTEINTE REELLE IDENTIFIABLE / ATTEINTE OBSERVEE** créés :
   la garantie d'antériorité exige une continuité minute à minute
   complète depuis le début de la période (lundi 00:00 pour
   l'hebdomadaire) ; les atteintes observées sont censurées des
   comparaisons C5-06 à C5-09 et publiées séparément ; l'ancienne
   censure « trou > 15 minutes » est remplacée pour les atteintes.
3. **CONTENUE ETABLIE** exige 1 440/1 440 minutes observées ; le seuil
   de 95 % (formule et bornes 00:10/23:50 désormais explicites) est
   confirmé comme critère de qualité générale et explicitement
   disqualifié comme preuve d'absence d'événement ; C5-10 peut en
   résulter non éligible, assumé d'avance.
4. Contrôle de couverture **par fenêtre** (+5/+15/+30/+60) avec attendu,
   observé, taux, trous et statut COMPLETE/PARTIELLE/CENSUREE publiés ;
   aucun observable calculé silencieusement sur une fenêtre incomplète ;
   avertissement publié si un bras repose majoritairement sur des
   fenêtres partielles.

Aucune autre clause des documents V2 et V2.1 n'est modifiée. **STATUT :
PROTOCOLE V2 + ADDENDA V2.1 ET V2.2 — EN ATTENTE DE VALIDATION
DÉFINITIVE. AUCUN CALCUL N'A ÉTÉ LANCÉ, AUCUNE DONNÉE SOURCE MODIFIÉE,
AUCUN RÉSULTAT DE CAMPAGNE 5 CONSULTÉ.**
