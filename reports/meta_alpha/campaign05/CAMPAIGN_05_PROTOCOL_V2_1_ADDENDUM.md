# CAMPAGNE 5 — ADDENDUM FORMEL V2.1 AU PROTOCOLE V2

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE — AUCUN
CALCUL LANCÉ.** Addendum produit après validation de l'architecture
(seq 214) ; il complète et, sur les seuls points qu'il énumère, **précise**
le protocole consolidé V2 (`CAMPAIGN_05_PROTOCOL_V2.md`, sha256
`818837fd5fb500b2906685367ea72acc18c2b5ddfce64de3bdfe5c8239818331`,
conservé inchangé). Ensemble V2 + V2.1 soumis à validation définitive ;
hashes chaînés avant toute extraction si validation. Objectif des six
corrections : qu'aucune absence de données ne soit lue comme une absence
d'événement, et qu'aucune information de clôture ne soit datée d'avant
sa disponibilité.

## Correction 1 — Couverture et données manquantes (règles figées)

**Définitions.** Un **trou** = plus d'une minute sans barre entre deux
barres M1 consécutives présentes (durée du trou = minutes sans barre).
Le **taux de couverture** d'une unité = barres M1 présentes / minutes
théoriques de l'unité : journée 1 440 ; sessions ASIE 480, LONDRES 300,
NEW YORK 480, NUIT 180 ; fenêtres 5/15/30/60 = leur durée. Chaque taux
est publié par événement et en distribution par ère ; il n'existe pas de
« journée supposée complète ».

**Journée observable pour F-F** — trois statuts mutuellement exclusifs,
publiés pour les 2 572 journées utilisables attendues et toute journée
sous le seuil de 300 barres (celles-ci restent exclues et comptées) :
- **COMPLETE** : ≥ 1 368 barres présentes (couverture ≥ 95 % des minutes
  00:00–23:59), première barre au plus tard à 00:10, dernière au plus tôt
  à 23:50, et **aucun trou > 30 minutes** entre la première et la
  dernière barre ;
- **PARTIELLE** : utilisable (≥ 300 barres) mais ne satisfaisant pas
  COMPLETE ;
- **EXCLUE** : < 300 barres (déjà prévue au V2).

**Conséquences contraignantes.**
- Une **première atteinte** observée dans une journée COMPLETE est
  retenue normalement. Dans une journée PARTIELLE : si un trou > 15
  minutes précède l'atteinte le même jour, l'atteinte est classée
  **CENSUREE_ANTERIORITE** (une atteinte plus précoce a pu survenir dans
  le trou sans être observable) — exclue des comparaisons C5-06 à C5-08,
  comptée et publiée ; sans trou > 15 minutes avant elle, elle est
  retenue et marquée « journée partielle ».
- Une journée ne peut être déclarée **contenue** (ni atteinte ni touch)
  que si elle est COMPLETE. Une journée PARTIELLE sans atteinte observée
  est classée **CONTENUE_NON_ETABLIE** : exclue du dénominateur de
  C5-10, comptée et publiée — l'absence d'atteinte observée n'y est
  jamais assimilée à une absence d'atteinte réelle. Une journée
  PARTIELLE **avec** touch observé reste « touch », sans franchissement
  établi.
- **Sessions et fenêtres (F-E)** : une fenêtre d'ouverture n'est
  observable que si sa couverture est ≥ 90 % (par exemple ≥ 54 des 60
  minutes de la première heure) **et** sans trou > 15 minutes ; sinon
  l'issue correspondante est censurée et comptée. La session est publiée
  avec son taux de couverture ; une session de couverture < 50 % est
  inéligible à toute observable de session (comptée).
- **Semaines (F-F hebdomadaire)** : le statut de la semaine distingue,
  séparément, (a) la validité du **niveau de référence** (semaine
  précédente utilisable, V2) et (b) l'observabilité de la semaine
  courante : COMPLETE si ≥ 4 journées utilisables dont aucune journée
  PARTIELLE ne précède l'atteinte hebdomadaire observée sans la censurer
  selon la règle journalière appliquée récursivement (trou > 15 minutes
  dans une journée partielle antérieure à l'atteinte = atteinte
  hebdomadaire CENSUREE_ANTERIORITE). Une semaine sans atteinte observée
  n'est « contenue à l'échelle hebdomadaire » pour aucun usage si une de
  ses journées est PARTIELLE ou EXCLUE au-delà des statuts publiés.

## Correction 2 — Heure de disponibilité aux seuils horaires

La **date** d'un événement reste le début de sa barre M1 ; toute
classification « observable avant une frontière » utilise l'**heure de
disponibilité** = début de barre + 1 minute (clôture de la barre), bornes
ainsi figées :

| Comparaison | Règle figée (disponibilité) | Équivalent en début de barre |
|---|---|---|
| C5-06 « avant 08:00 UTC » | disponibilité ≤ 08:00 (borne **incluse** : une information disponible exactement à 08:00 compte comme connue à l'ouverture de Londres) | barre débutant au plus tard à 07:59 |
| C5-08 « formées avant 13:00 » vs « à partir de 13:00 » | groupe A : disponibilité **< 13:00** ; groupe B : disponibilité **≥ 13:00** | A : barre débutant au plus tard à 12:58 ; B : au plus tôt à 12:59 |
| C5-09 « avant mercredi 00:00 UTC » | disponibilité **< mercredi 00:00** (borne exclue : disponible à mercredi 00:00 = trop tard) | barre débutant au plus tard à mardi 23:58 |

## Correction 3 — Populations exactes des premières atteintes (C5-06 à C5-09)

- Seuls les **franchissements stricts** (haut > H_référence, bas <
  B_référence, prix enregistrés sans arrondi) entrent dans C5-06 à
  C5-09. Les **touch** (égalité sans dépassement) sont publiés séparément
  et n'entrent ni au numérateur ni au dénominateur de ces comparaisons ;
  une journée à touch seul n'est ni une journée à atteinte ni une
  journée contenue (voir C5-10).
- **C5-06** : population = franchissements stricts **premiers** de chaque
  côté, en journées COMPLETE (ou PARTIELLE retenue selon la correction
  1), à ordre déterminé. Dénominateur par côté = nombre de ces
  franchissements du côté ; numérateur = ceux dont la disponibilité
  satisfait la règle C5-06 ci-dessus. Un seul côté atteint : seul son
  événement existe (l'autre côté n'est ni zéro ni échec — il est absent
  de la population). Aucun côté atteint : la journée est hors population
  C5-06.
- **C5-07** : même population que C5-06 ; l'extension à +60 min est
  mesurée sur les barres suivant celle de l'atteinte ; fenêtre tronquée
  par fin de journée ou trou > 15 min = événement censuré pour cette
  variable (exclu de la médiane, compté et publié).
- **Deux atteintes successives** (HAUT puis BAS ou inverse le même
  jour) : la seconde est la première atteinte de son côté ; elle est
  retenue pour son côté, marquée « postérieure à l'atteinte opposée »,
  même grappe-journée. Atteintes HAUT et BAS dans la **même barre** :
  ordre indéterminé → sortie dédiée (§5 du V2), exclues de C5-06 à
  C5-09, effectifs publiés.
- **C5-08** : population = franchissements stricts premiers des deux
  côtés poolés (à ordre déterminé, fenêtre +60 observable ou censurée
  comptée), groupés par l'heure de disponibilité (correction 2) ;
  ventilation par côté publiée.
- **C5-09** : population = franchissements stricts premiers de chaque
  côté à l'échelle hebdomadaire, en semaines à référence valide et
  atteinte non censurée (correction 1) ; dénominateur par côté = nombre
  de ces franchissements du côté dans les semaines éligibles ; une
  semaine sans franchissement d'un côté ne compte ni pour ni contre ce
  côté (elle alimente les descriptions de semaines contenues, séparées).

## Correction 4 — Mouvement pré-ouverture et issues (C5-02)

- Amplitude du mouvement pré-ouverture A = |rendement log signé des
  60 minutes précédant l'ouverture| (bp). Si **A = 0** (rendement
  exactement nul aux prix enregistrés, y compris fenêtre sans barre —
  cette dernière étant déjà inéligible par couverture), l'événement est
  classé **MOUVEMENT_NUL**, publié, et **exclu du dénominateur** de
  C5-02 ; jamais classé poursuite.
- Seuils de 50 % : prix de déclenchement de poursuite = prix d'ouverture
  déplacé, dans le sens du mouvement pré-ouverture, de **0,5 × A** (bp
  relatifs au prix d'ouverture) ; seuil de retournement = déplacement
  inverse de 0,5 × A. Atteinte d'un seuil = franchissement strict par la
  clôture ou l'extrême de barre au-delà du prix-seuil (prix enregistrés).
- Quatre catégories **mutuellement exclusives** sur la fenêtre +30 min :
  **POURSUITE_SEULE** (seuil de poursuite atteint, jamais celui de
  retournement), **RETOURNEMENT_SEUL**, **LES_DEUX** (les deux seuils
  atteints dans la fenêtre ; si la même barre atteint les deux,
  sous-marque « ordre indéterminé » mais la catégorie reste LES_DEUX),
  **AUCUN**. Fenêtre non observable (couverture/trou, correction 1) :
  **CENSURE**, exclue du dénominateur, comptée.
- **Dénominateur exact de C5-02** = transitions éligibles (vers NEWYORK
  ou vers LONDRES) avec A > 0 et fenêtre +30 observable. **P(poursuite)**
  = (POURSUITE_SEULE + LES_DEUX) / dénominateur ; les quatre parts sont
  publiées, de sorte que la convention est réversible à la lecture.

## Correction 5 — Spread de C5-05 : formule et provenance

- Provenance : colonnes **ask, bid et mid des partitions tick IS**
  d'origine (même source que toutes les campagnes), agrégées en barres
  M1 par le même moteur de reconstruction que les campagnes 2.2 à 4.
- Formule par barre M1 : `sp_barre = médiane sur les ticks de la minute
  de ((ask − bid) / mid × 10 000)`, en bp, mid étant la colonne fournie
  par la source (prix médian tick). C'est la variable historique `sp` des
  bruts des campagnes précédentes, reprise à l'identique — aucun nouvel
  estimateur.
- Observable C5-05 : **médiane des sp_barre des 15 premières barres** de
  la fenêtre d'ouverture (médiane de médianes, publiée comme telle).
- Absences : une barre sans tick n'a pas de sp ; la fenêtre est
  éligible si **≥ 12 des 15 barres** ont un sp défini, sinon inéligible
  (comptée). Le spread n'est utilisé que comme contexte descriptif ;
  aucun coût n'en est dérivé.

## Correction 6 — Matérialité précisée

- **5 points = 5 points de pourcentage** : différence absolue de
  probabilités ≥ 0,05 dans l'échelle [0, 1].
- **Ratio 1,15 symétrique** : matériel si le ratio ≥ 1,15 **ou**
  ≤ 1/1,15 (≈ 0,8696).
- Formules des contrastes : proportions → différence p_A − p_B
  (points = × 100) ; médianes et taux → ratio valeur_A / valeur_B
  (l'ordre A/B est celui du tableau ci-dessous, constant) ; intervalles
  et p-values inchangés par rapport au protocole V2 §6.

## Tableau des dix comparaisons actualisé (fait foi avec le V2 §6)

Deux familles d'inférence distinctes, BY séparée par famille de cinq,
aucune conclusion globale sur les dix ; bootstrap grappes-journées
(F-E, F-F journalier) et grappes-semaines (C5-09) ; 2 000 répétitions ;
éligibilité ≥ 200 épisodes et ≥ 100 grappes par bras ; lectures
candidate J1 / significative sous le seuil matériel / négative / non
éligible, toutes publiées.

| ID | Famille | Contraste (formule) | Population et dénominateur (corrections 1–4) | Unité / grappe | Matérialité |
|---|---|---|---|---|---|
| C5-01 | F-E | ratio des médianes d'amplitude d'ouverture 30 min, LONDRES / ASIE | Ouvertures éligibles (retard ≤ 30 min, couverture de fenêtre ≥ 90 %) | Ouverture / journée | ratio ≥ 1,15 ou ≤ 0,8696 |
| C5-02 | F-E | différence de P(poursuite) = (POURSUITE_SEULE + LES_DEUX)/dénominateur, NEWYORK − LONDRES | Transitions éligibles A > 0 et fenêtre +30 observable (correction 4) | Transition / journée | ≥ 5 points (0,05) |
| C5-03 | F-E | ratio des médianes d'amplitude de première heure d'Asie, CONTINUITE / TROU_INTRA_SEMAINE | Ouvertures d'Asie éligibles des deux classes (REOUVERTURE_SEMAINE et FERMETURE_EXCEPTIONNELLE hors contraste, publiées) | Ouverture / journée | ratio 1,15 symétrique |
| C5-04 | F-E | ratio des médianes d'amplitude d'ouverture Londres 30 min, lundi / vendredi | Ouvertures de Londres éligibles des lundis et vendredis UTC | Ouverture / journée | ratio 1,15 symétrique |
| C5-05 | F-E | ratio des médianes de spread (médiane de médianes, correction 5), NEWYORK / LONDRES | Ouvertures éligibles avec ≥ 12/15 barres à spread défini | Ouverture / journée | ratio 1,15 symétrique |
| C5-06 | F-F | différence de P(disponibilité ≤ 08:00), HAUT − BAS | Franchissements stricts premiers par côté, ordre déterminé, journées COMPLETE ou PARTIELLE retenue (corrections 1–3) | Atteinte / journée | ≥ 5 points |
| C5-07 | F-F | ratio des médianes d'extension à +60 min, HAUT / BAS | Même population que C5-06, fenêtres +60 non censurées (censurées comptées) | Atteinte / journée | ratio 1,15 symétrique |
| C5-08 | F-F | ratio des médianes de retracement à +60 min, formées avant 13:00 / dès 13:00 (disponibilité, correction 2) | Franchissements stricts premiers poolés, ordre déterminé | Atteinte / journée | ratio 1,15 symétrique |
| C5-09 | F-F | différence de P(disponibilité < mercredi 00:00), HAUT − BAS | Franchissements stricts premiers hebdomadaires par côté, semaines éligibles non censurées (corrections 1–3) | Atteinte / semaine | ≥ 5 points |
| C5-10 | F-F | différence de P(journée contenue), ère 2010–13 − 2017–20 | Journées **COMPLETE** uniquement au dénominateur (CONTENUE_NON_ETABLIE exclue et publiée, correction 1) | Journée / journée | ≥ 5 points |

## Résumé des modifications par rapport au protocole V2

1. **Couverture** : statuts de journée COMPLETE/PARTIELLE/EXCLUE chiffrés
   (≥ 95 %, bornes de journée, trou > 30 min), censure d'antériorité des
   atteintes après un trou > 15 min, classe CONTENUE_NON_ETABLIE —
   l'absence d'atteinte observée n'est plus jamais une absence
   d'atteinte dès que l'observation est partielle ; taux de couverture
   publiés par unité (journée, session, fenêtre, semaine) ; session
   < 50 % inéligible.
2. **Disponibilité aux frontières** : classifications de C5-06/08/09
   converties en heure de disponibilité (clôture de barre), bornes
   inclusives/exclusives figées et équivalents en début de barre
   tabellisés.
3. **Populations d'atteintes** : franchissements stricts seuls, touch
   publiés hors comparaisons ; dénominateurs exacts par comparaison ;
   un seul côté atteint = absence de l'autre (ni zéro ni échec) ;
   atteintes successives opposées retenues et marquées ; simultanées
   dans une même barre exclues et publiées.
4. **C5-02** : mouvement nul (A = 0) classé MOUVEMENT_NUL, exclu du
   dénominateur, jamais poursuite ; quatre catégories exclusives
   d'issues avec sous-marque d'ordre indéterminé intra-barre ; seuils
   de 50 % en prix relatifs explicites ; P(poursuite) définie comme
   (seule + les deux)/dénominateur, parts publiées.
5. **Spread C5-05** : formule complète (médiane tick (ask−bid)/mid ×10⁴
   par barre M1, puis médiane sur 15 barres), provenance (colonnes
   ask/bid/mid des partitions tick, variable historique des campagnes
   2.2–4) et règle d'absence (≥ 12/15 barres).
6. **Matérialité** : 5 points = points de pourcentage (0,05) ; ratio
   1,15 déclaré symétrique (≥ 1,15 ou ≤ 0,8696) ; formule de chaque
   contraste écrite dans le tableau actualisé des dix comparaisons.

Aucune autre clause du protocole V2 n'est modifiée. **STATUT :
PROTOCOLE V2 + ADDENDUM V2.1 — EN ATTENTE DE VALIDATION DÉFINITIVE.
AUCUN CALCUL N'A ÉTÉ LANCÉ, AUCUNE DONNÉE SOURCE N'A ÉTÉ MODIFIÉE.**
