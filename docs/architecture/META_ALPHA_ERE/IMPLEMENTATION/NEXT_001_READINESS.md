# ERE-NEXT-001 — Audit post-implémentation et préparation du deuxième dossier trader

## 1. Audit post-implémentation (Phase 1)

- Cinq checkpoints ERE vérifiés sur la branche distante :
  `f391a39` (Phase 1), `d2abe92` (fix enveloppe), `2f59d92` (Phase 2),
  `36d1547` (Phases 3–4), `49d0ddc` (fix porte H), `8f8a3b1` (Phases 3–7).
  HEAD distant = `8f8a3b1` à l'ouverture, `main` à `98bfd359`, arbre propre.
- Fichiers réels : package `ere/` (taxonomy, contracts, engines, runner,
  intake, vertical_slice), `tests/` — **16/16 tests PASS** après ajout
  de la qualification d'entrée (13 initiaux rejoués à l'identique).
- Contrats présents : les huit objets (TraderDossier, BehaviorProfile,
  HypothesisSet, ExperimentPlan, SignatureReport, ModelDossier,
  EngineSpec, ValidationVerdict) + MarketWindow, AvisDeTestabilite,
  DossierState. Neuf moteurs présents comme fonctions à frontières
  appliquées ; F découpé catalog/index/signatures/execute ; I-A/I-B séparés.
- Registre chaîné cohérent avec les checkpoints (entrées seq500–501
  préenregistrement/résultats, chaîne valide).

### Origine précise de l'échec gouvernance 5/6

Le test 05 de `test_governance009.py` exige la présence du terme
anglais `HYPOTHESIS` dans le registre des modèles. Ce terme a disparu
lors de la réécriture du registre au commit **`bf3dd58` (ME-001.1,
seq480–481)** — donc **avant** toute l'exécution ERE. Vérification :
`git diff 5027af0..8f8a3b1` sur le registre = **vide** ; l'exécution ERE
n'a jamais touché ce fichier. Ce n'est **pas une régression** et cela ne
masque aucune perte de protection : le registre dit toujours
SIGNATURE_DETECTED pour ME-001 et REJECTED pour V1/V2 — seul le mot
anglais attendu par le test a été remplacé par le vocabulaire français.
Conformément à l'interdiction de modifier un test pour le rendre vert,
le test reste en l'état ; la correction éventuelle (aligner le test sur
le vocabulaire actuel du registre, ou réintroduire le terme) est une
décision de gouvernance réservée au fondateur, documentée ici.

## 2. Qualification du moteur A (Phase 2) — `ere/intake.py`

Nouveau module testé (3 tests dédiés, 16/16 au total) :

- **Formats acceptés** : dossier brut JSON-compatible `{trades, claims,
  missing_information, selection_process}` ; champs de transaction
  reconnus listés (`TRADE_FIELDS`) ; tout champ inconnu est signalé,
  jamais ignoré silencieusement.
- **Doublons** : déduplication par empreinte du contenu descriptif
  (instrument, sens, horaire, prix, volume) ; les doublons retirés sont
  listés dans le rapport, pas effacés en silence.
- **Données manquantes** : comptées champ par champ ; un champ absent
  partout devient automatiquement une information manquante déclarée.
  Rien n'est jamais rempli.
- **Provenance** : `source_ref` exigé par transaction pour déclarer la
  provenance complète ; sinon avertissement explicite.
- **Métadonnées temporelles** : fuseau DÉCLARÉ / PARTIEL / ABSENT ;
  sans déclaration complète, les horaires seront marqués incertains et
  jamais convertis en silence.
- **Prêt pour B (`b_ready`)** : exige instrument, sens et horaire
  d'ouverture sur chaque transaction retenue ; sinon blocages nommés.

### Contrat d'entrée du deuxième dossier (résumé opposable)

Obligatoire : au moins une transaction ; par transaction, les dix
champs reconnus présents comme clés (valeur ou `null` explicite) ;
`source_ref` par capture ; processus de sélection déclaré (comment ces
transactions ont été obtenues — biais de sélection documenté, jamais
caché). Recommandé pour B : prix d'ouverture/clôture, volumes,
horaires de clôture, résultats individuels. Les statistiques publiques
entrent comme claims `verified=False` et ne nourrissent aucun calcul.

## 3. Protocole de parcours réel A → G (Phase 3)

| Transition | Condition d'entrée | Condition de sortie | Interdit |
|---|---|---|---|
| → A | dossier brut + sélection documentée | `qualify_dossier` accepté, rapport d'entrée | inventer un champ |
| A → B | `b_ready=True` | faits/interpretations séparés, fenêtres `MarketWindow` déclarées avant extraction | mécanisme présenté comme fait |
| B → C | profil validé | ≥2 hypothèses + inconnue, prédictions divergentes | probabilité sans likelihood |
| C → E | hypothèses + catalogue F | avis de testabilité ; NON_TESTABLE contre-signé par G pour clore | calculer avant gel du plan |
| E → F | plan hashé, segment autorisé | mesures par segment + coût d'ordre de grandeur | segment protégé, mélange de segments |
| F → G | rapports + liste fermée des pièces | qualification constitutionnelle | pièce hors liste, statistique publique comme preuve |
| G → H | **fermé par défaut** : N5 minimum, candidature déclarée, approbation fondateur | — | tout franchissement dans cette mission |

I n'est pas déclenché : aucune donnée indépendante ni protocole de
validation n'existe pour un futur dossier à ce stade.

## 4. Préparation des données (Phase 4, lecture seule)

Inventaire réel revérifié par recalcul : **348 partitions, somme des
lignes recalculée = 685 118 625, égale au total déclaré, 0 erreur,
inventaire en lecture seule**. Le corpus reste téléchargé par la CI
depuis Drive, partitions jamais modifiées, zones prospectives ME-001
non accédées. Continuité et schémas sont ceux du corpus certifié
(Bid/Ask Parquet) ; les restrictions d'accès existantes s'appliquent.

## 5. Blocages scientifiques (liste opposable)

1. Aucun deuxième trader n'est choisi : la sélection du dossier est
   une décision du fondateur (source, droits, biais de sélection).
2. Les méthodes de B sur très peu de transactions bornent ce qui est
   descriptible ; C devra conserver l'hypothèse inconnue.
3. ME-004 (liquidité) reste bloqué faute de cotations du lieu
   d'exécution réel.
4. La validation prospective ME-001 suit sa règle d'arrêt propre ;
   elle ne peut servir ni de donnée ni d'étalon pour un nouveau dossier.
5. L'échec du test de gouvernance 05 attend une décision de vocabulaire
   (fondateur), sans urgence scientifique.

## 6. Plan de première campagne autorisée (proposé)

1. Le fondateur désigne le dossier trader n°2 et sa source.
2. Ingestion par `qualify_dossier`, rapport d'entrée checkpointé.
3. B : profil comportemental + fenêtres de marché déclarées.
4. C/D/E : hypothèses concurrentes, plan discriminant gelé et
   préenregistré au registre chaîné.
5. F : exécution sur segment de découverte autorisé uniquement.
6. G : qualification — y compris NOT_IDENTIFIED si c'est la réponse.
Aucune étape H/I sans preuves et autorisations nouvelles.

**Verdict : `SECOND_TRADER_INGESTION_READY`** — l'infrastructure peut
recevoir et qualifier un deuxième dossier dès que le fondateur le désigne.
