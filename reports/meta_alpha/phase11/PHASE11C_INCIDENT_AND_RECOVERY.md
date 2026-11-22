# PHASE 11-C — RAPPORT D'INCIDENT ET DE REPRISE CONTRÔLÉE

**Verdict : `CI_RECOVERED_AND_PHASE11C_COMPLETED`**

Mission corrective : diagnostic d'abord, aucune relance aveugle,
correction de la cause exacte, une seule reprise contrôlée. Le
présent rapport distingue l'erreur d'interface (réponse précédente
interrompue) de l'échec réel du CI, qui a eu lieu et est documenté
ci-dessous. Branche de travail réelle :
`arena/afe12737-xauusd-quant-research` (la désignation
« …-recherche-quantitative » de la mission corrective est une
coquille ; aucun travail n'a été fait sur une autre branche).

## 1. Chronologie des incidents

| Étape | Preuve |
|---|---|
| seq305 : autorisation + préflight 11-C chaînés ; commit `71c3ec2` | chaîne valide (305 entrées vérifiées) |
| Commit `4f74a4b` : moteur d'anatomie + job CI dédié | moteur livré **tronqué à la ligne 141** (fichier de 141 lignes, expression interrompue `cand = np.where(y[p`) |
| Run **45015419598** (head `4f74a4b`, 11:03 UTC) : 8/8 lots verts, job `P11-C anatomie` en échec à l'étape « Analyse anatomique Phase 11-C » | API GitHub Actions (étapes par job) |
| Commit `cd4601b` : le job d'analyse committe son journal même en échec | journal d'erreur conservé au commit `4c3d2a8` : `SyntaxError: '[' was never closed`, ligne 141 |
| Run **45016320712** (head `cd4601b`, 11:14 UTC) : même échec d'analyse (moteur toujours tronqué) ; échec secondaire du job de synthèse Phase 10 à son étape de commit (voir §5) | API GitHub Actions |
| Commit `18d4e27` : réécriture de la fin du moteur (141 → 297 lignes) | diff §4 |
| Run **45017167617** (head `18d4e27`, 11:24 UTC, 25 min) : **entièrement vert** ; livrables committés par le workflow (`746b645`) | API GitHub Actions + commit distant |
| Réponse précédente interrompue par l'utilisateur avant la synthèse finale | aucun échec CI correspondant ; le run était déjà vert |

La « tentative de relance ayant précédé le message rouge » de la
capture correspond donc à une interruption d'interface, pas à un
échec GitHub Actions : le dernier run réel (45017167617) est vert.

## 2. État exact de la branche et des commits

- HEAD local = HEAD distant = `746b645` (vérifié par
  `git ls-remote` après récupération du commit CI), arbre propre
  (`git status --short` vide avant la présente rédaction).
- Chaîne des commits 11-C : `71c3ec2` (seq305) → `4f74a4b` (moteur
  tronqué) → `cd4601b` (journal en échec) → `4c3d2a8` (journal
  d'erreur committé par le CI) → `18d4e27` (correction) →
  `746b645` (livrables, auteur github-actions).
- Périmètre réel des modifications depuis le dernier état stable
  (`433450a`, seq304) : **10 fichiers, 4 389 insertions, 1
  suppression** (workflow +55 lignes environ, moteur 297 lignes,
  chaîne, journaux et livrables). Les chiffres « +404107 / 158
  fichiers » de la capture ne correspondent pas à ce périmètre :
  l'écart complet de la branche depuis sa base `98bfd35` vaut
  961 fichiers / 933 807 insertions (tout l'historique du
  programme) ; seuls les chiffres ci-dessus, mesurés par
  `git diff --stat`, font foi pour la Phase 11-C.
- Aucune modification étrangère à la Phase 11-C : le diff depuis
  `433450a` ne touche que le workflow, le moteur 11-C, la chaîne et
  les livrables 11-C. Aucun reset, aucune suppression de commit.

## 3. Cause racine de chaque échec

1. **Run 45015419598** : `SyntaxError: '[' was never closed`
   (ligne 141) — le fichier `ci_tools/phase11c_engine.py` committé
   en `4f74a4b` était tronqué en pleine expression dans la section
   touche/réintégration. Cause : écriture de fichier interrompue
   avant la fin du moteur (`synthese`, bootstrap et `main`
   absents). Échec du moteur, pas de l'infrastructure.
2. **Run 45016320712** : même SyntaxError (le commit `cd4601b` ne
   changeait que le workflow, pas le moteur), plus un échec
   secondaire du job historique « P10 synthèse » à son étape de
   commit : ce job se déclenche aussi quand les lots réussissent
   (condition héritée) et tente de committer des artefacts Phase 10
   concurrents pendant un run 11-C. Anomalie de workflow réelle
   mais **sans effet sur les livrables 11-C** (voir §5).
3. **Interruption d'interface finale** : aucun run associé ; ne pas
   confondre avec un échec CI.

## 4. Diff précis de la correction

Commit `18d4e27` : `ci_tools/phase11c_engine.py`, **+157/−2 lignes**
(141 → 297 lignes). Ajout de tout ce qui manquait après la ligne
141 : fin de la section touche/réintégration (réintégration
confirmée, retours, reprise post-réintégration), retracement de la
bougie déclencheuse, composition de session de la déclencheuse,
classification des archétypes, fonction de quantiles `q`, bootstrap
par grappes `bootstrap_grappes` (2 000 répétitions, graine
20261122), `main` (chargement des 8 lots, jointure avec la carte
11-B.1 avec assertion de complétude 3 767 événements) et `synthese`
(horizons, archétypes, sessions, couverture, chevauchement H1/H4,
écriture des livrables). Aucune autre fonction modifiée ; le
workflow n'a pas été touché par la correction.

## 5. Audit du workflow

Mode `phase11c` correctement déclaré (input booléen) ; job dédié
`analyse11c` conditionné à cet input, `needs: lots`, et les lots
s'exécutent si `cible || phase11c` (huit lots réutilisés, chaque
partition téléchargée une fois par lot) ; transmission des barres
par artefacts `p10-bars-*` → `bars_artifacts` déterministe ;
permissions du job d'analyse limitées à `actions: read` +
`contents: write` (nécessaire au commit des livrables) ; commit des
livrables en `if: always()` (journal conservé même en échec) ;
publication d'artefacts 90 jours. Aucune autre phase déclenchée par
le mode 11-C, pas de double chemin pour l'analyse elle-même.
**Anomalie résiduelle documentée** : le job historique de synthèse
Phase 10 s'exécute aussi lors des runs 11-C (sa condition inclut le
succès des lots) et peut échouer à son étape de commit ; il
n'altère ni les populations ni les livrables 11-C, et sa
neutralisation exigerait une modification de workflow hors du
périmètre minimal de la présente correction — elle est signalée,
pas corrigée silencieusement.

## 6. Contrôles du moteur

- `python -m py_compile ci_tools/phase11c_engine.py` : **OK**
  (fichier de 297 lignes, toutes les fonctions attendues présentes :
  `session_de`, `fermeture_reguliere`, `charger_barres`,
  `analyser_event`, `q`, `bootstrap_grappes`, `main`, `synthese` ;
  blocs terminés, imports résolus, `main` sous
  `if __name__ == '__main__'`).
- Validation fonctionnelle : le run complet 45017167617 a traité
  3 107 + 660 événements avec l'assertion interne de jointure
  (3 767 événements identifiés, aucun sans `event_id`), produit des
  censures cohérentes (3 + 3 lacunes anormales, effectifs par
  horizon décroissant de façon traçable) et des sorties complètes.
- Limites fonctionnelles relevées à la lecture (documentées, non
  bloquantes, définitions gelées respectées) : heuristique de
  fermeture régulière propre au moteur pour la classification des
  censures ; proportions « nouveau MFE » non calculées à t+1 (sans
  objet) ; bootstrap descriptif pondéré événements au sein des
  grappes rééchantillonnées, conformément au protocole.

## 7. Tests synthétiques

**Aucun fichier de test synthétique 11-C ni aucun résultat de test
n'est traçable dans le dépôt.** Le message du commit `18d4e27`
mentionne « test synthétique OK », mais aucun artefact ne permet
de vérifier la couverture des cas exigés (événements H1/H4, grappes
multiples, extension, repli, touche, réintégration, reprise,
ambiguïté intraminute, censures, fermeture programmée, huit
horizons, reproductibilité, production des fichiers). Conformément
à la mission corrective, aucun test n'est inventé rétroactivement :
cette traçabilité manquante est consignée comme **limite de
preuve**. La correction du moteur est établie par la compilation,
la relecture intégrale du fichier et le run réel complet — pas par
une suite synthétique archivée.

## 8. Statut du nouveau run et contrôle des huit lots

Run unique de reprise : **45017167617** (head `18d4e27`), vert en
25 min 10 s. Huit lots `p10-bars-*` tous verts (b01–b07 +
missing13), job d'analyse vert, livrables committés par le
workflow au commit `746b645`. Aucune nouvelle relance n'a été
effectuée pendant le présent diagnostic.

## 9. Garde-fous et sources

- `PHASE11_PROTOCOL.md` : sha256
  `fdfb04ed71cd5317e9b342a408194ac79c42ab06188555cbc1fcb3367aa38f94`
  — **identique au gel seq300**.
- Chaîne : valide, **305 entrées** avant le présent checkpoint
  (autorisation 11-C présente une fois, seq305).
- Carte 11-B.1 : sha256 `3281f594…` inchangée ; manifeste définitif
  `57b7b8af…` inchangé ; populations F10-01/F10-03 sans
  redétection ; identifiants non recalculés (le moteur lit la
  carte et joint dessus, avec assertion).
- Données : barres M1 des 8 lots Kaggle du corpus IS 2010–2020
  (282 partitions) ; holdout ni monté, ni listé, ni lu ; aucune
  analyse économique, backtest ni optimisation ajoutés (le moteur
  ne calcule ni coûts ni espérance nette, aucune p-value).

## 10. Génération des livrables

Produits par le run vert et committés (`746b645`) :
`PHASE11C_EVENT_PATHS.csv` (3 768 lignes = 3 767 événements
admissibles + en-tête), `PHASE11C_HORIZON_METRICS.csv`,
`PHASE11C_ARCHETYPES.csv`, `PHASE11C_SESSION_ANATOMY.csv`,
`PHASE11C_COVERAGE_CENSORING.csv`, `PHASE11C_RESULTS.json`,
`PHASE11C_LOG.txt`. Le rapport principal
`PHASE11C_ANATOMY_REPORT.md` est rédigé à la suite du présent
diagnostic, exclusivement à partir de ces sorties commitées
(aucun nouveau calcul sur les données).

## 11. Empreintes SHA-256 (livrables finaux)

Calculées et chaînées au checkpoint seq306 (voir le commit
associé) : rapport d'anatomie, rapport d'incident, cinq fichiers de
données et le JSON de résultats.

## 12. Commit distant et état final

Vérification distante réellement effectuée par `git ls-remote`
(HEAD distant = HEAD local après récupération du commit CI) ;
arbre propre après commit des deux rapports. Voir seq306.

**Verdict : `CI_RECOVERED_AND_PHASE11C_COMPLETED`** — cause racine
corrigée (troncature), reprise unique réussie, livrables complets.
La Phase 11-C est la dernière étape descriptive autorisée ; toute
phase ultérieure exige une décision distincte.
