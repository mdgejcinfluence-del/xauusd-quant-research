# PHASE 11-B — AUDIT D'INTÉGRITÉ, DE PROVENANCE ET D'ADMISSIBILITÉ DES MANIFESTES

**Référence méthodologique : PHASE 11-A gelée définitivement (seq300,
protocole sha256 `fdfb04ed…`). Autorisation chaînée seq301. Audit en
lecture seule : aucune trajectoire reconstruite, aucun seuil ni aucune
grappe recalculés, aucune donnée de prix lue, holdout 2020–2026 ni
monté, ni listé, ni lu.**

## Verdict : BLOQUÉ

Un défaut critique d'identifiants (ANO-11B-01) empêche de garantir
l'admissibilité par grappe exigée par le protocole gelé. Tous les
autres contrôles critiques (provenance, comptes, exclusions, fenêtres
causales, périmètre IS) sont conformes. Conformément à la règle de
verdict, un résultat partiellement conforme n'est pas présenté comme
un PASS, et aucune correction n'a été appliquée pour l'obtenir.

## 1. Périmètre et sources

Populations F10-01 (H1) et F10-03 (H4), séparées, issues exclusivement
de la correction Phase 10 (amendement seq289, résultat seq294).
Manifeste définitif retenu après examen de provenance :
`reports/meta_alpha/phase10/PHASE10_EVENTS_CIBLE.csv.gz`
(128 937 octets, sha256 `57b7b8af…`), produit par le run correctif
**45011013927** (8 lots Kaggle + étape 2 + synthèse corrective) et
committé par le workflow (`817b974`). Le manifeste initial
`PHASE10_EVENTS.csv.gz` (run 44919631588, commit `9abf9c3`) est
**invalide pour F10-01/F10-03** (zéro événement, défaut NaN seq287) :
il est conservé comme preuve historique et exclu comme source ;
il ne contient d'ailleurs que F10-02/04/05/06. Inventaire complet :
`PHASE11B_MANIFEST_INVENTORY.csv` (20 lignes, chemins, rôles,
campagnes, tailles, SHA-256, statuts). Cohérence des 282 partitions
IS : vérification d'artefacts du run correctif
(`CORRECTION_ARTIFACT_VERIFICATION.json`) — 282/282 partitions,
comptages concordants avec seq288, 3 540 993 barres M1, barres
H1 59 184 / H4 15 195 déclarées.

## 2. Résultats F10-01 (H1)

Attendus = observés : **3 134 détectés, 3 107 admissibles, 27 non
admissibles** (grappes enregistrées en agrégat : 2 617). Timeframe
uniforme H1 ; sens ∈ {−1, +1} ; t_signal parsable partout, croissant,
plage 2010-01-14 19:00 → 2019-12-13 15:00 UTC (dans l'IS) ; **0
doublon** (ligne complète et clé composite famille+t_signal+sens).
Non admissibles traçables sans recouvrement : 4 entrées inéligibles
+ 23 fenêtres incomplètes = 27. Éligibles : t_entree, t_sortie et
seuil_bp présents partout.

## 3. Résultats F10-03 (H4)

Attendus = observés : **762 détectés, 660 admissibles, 102 non
admissibles** (grappes en agrégat : 597). Timeframe uniforme H4 ;
t_signal 2010-03-10 20:00 → 2019-12-12 16:00 UTC ; **0 doublon**.
Non admissibles : 1 entrée inéligible + 101 fenêtres incomplètes
= 102. Éligibles complets sur t_entree, t_sortie, seuil_bp.

## 4. Identifiants d'événements et de grappes — défaut critique

Le manifeste définitif contient 15 colonnes (famille, timeframe,
t_signal, ere, sens, spread_bp, entree_eligible, fenetre_complete,
t_entree, t_sortie, rendement_signe_bp, mae_bp, mfe_bp,
range_fenetre_bp, seuil_bp) et **aucune colonne d'identifiant
d'événement ni d'identifiant de grappe**. Correspondance avec le
protocole gelé : t_signal ↔ fin de la bougie déclencheuse (t0),
sens ↔ direction d fixée à t0, seuil_bp ↔ seuil Q95 appliqué ;
**P0 n'est pas stocké** (voir ANO-11B-03).

- Événements : identité garantie par la clé composite
  (famille, t_signal, sens), vérifiée unique (0 doublon) —
  ANO-11B-02, mineure.
- **Grappes (ANO-11B-01, bloquante)** : les identifiants de grappes
  de Phase 10 n'ont jamais été matérialisés par événement ; seuls
  les comptes agrégés (2 617 / 597) figurent dans
  `PHASE10_CORRECTION_RESULTS.json`. La mission interdit tout recalcul
  et exige la conservation des identifiants historiques, tandis que
  le protocole gelé (§2) prescrit des grappes « reconstruites à
  l'identique » (algorithme des composantes connexes, versionné dans
  `ci_tools/phase10_synthesize.py`, fonction `composantes`). L'audit
  ne choisit pas silencieusement entre ces deux lectures : en l'état,
  l'appartenance de chaque événement à sa grappe historique n'est pas
  matérialisable depuis les artefacts, et l'analyse à poids égal par
  grappe du protocole ne peut pas être garantie.

## 5. Exclusions et fenêtres causales

Exclusions : statuts d'admissibilité cohérents et motifs traçables
par les deux indicateurs (décompositions ci-dessus, sans
recouvrement). Fenêtres causales inéligibles : **H1 202 et H4 208
`INELIGIBLE_CAUSAL_WINDOW`** enregistrées dans
`P10_CIBLE_COVERAGE.json` (chaîné seq294), issues de la règle amendée
(fenêtre fixe de 250, minimum 200 valides, aucune prolongation ni
imputation — moteur versionné, tests synthétiques 14/14) ;
elles restent inéligibles et ne sont pas confondues avec les comptes
d'événements. Limite (ANO-11B-04) : traçabilité en agrégat seulement,
aucun registre par fenêtre ; une vérification unitaire exigerait un
recalcul interdit par la mission.

## 6. Compatibilité avec le protocole 11-A (sans calcul de trajectoire)

Conforme : populations séparées ; horodatages UTC exploitables et
dans l'IS ; bougie déclencheuse identifiable sans ambiguïté
(t_signal + timeframe + sens) ; distinction début de minute /
disponibilité à la clôture déjà inscrite au protocole gelé
(`extreme_*_utc`, résolution M1, aucun ordre intraminute prétendu).
Références M1 : corpus IS documenté (282 partitions, 3 540 993
barres M1, 8 lots) ; la complétude par horizon t+1…t+8 devra être
établie en Phase 11-C — non vérifiable à ce stade par construction
de la mission. Limites : P0 non stocké (ANO-11B-03, relu sur M1 en
11-C selon le protocole) ; grappes non matérialisées (ANO-11B-01).

## 7. Anomalies, preuves et correction requise

Anomalies détaillées dans `PHASE11B_AUDIT_RESULT.json` :
ANO-11B-01 (critique, bloquante, grappes), ANO-11B-02 (mineure,
event_id), ANO-11B-03 (limite, P0 non stocké), ANO-11B-04 (limite,
registre des fenêtres en agrégat). Preuves : empreintes SHA-256 de
l'inventaire, comptages structurels reproductibles par
`ci_tools/phase11b_audit.py` (lecture seule), concordances croisées
manifeste ↔ résultats de synthèse (seq288/seq294) ↔ couverture.

**Correction documentaire éventuellement nécessaire (décision
distincte du responsable, non appliquée)** : autoriser soit
(a) la matérialisation, dans un nouvel artefact sans modification
des populations, des identifiants `event_id` (clé composite) et
`grappe_id` par l'algorithme historique inchangé des composantes
connexes de Phase 10, soit (b) un amendement formel du protocole
gelé précisant le mode d'identification retenu pour la Phase 11-C.

## 8. Procès-verbal

Autorisation : seq301. Exécution : audit structurel en lecture seule
des artefacts du dépôt (script versionné `ci_tools/phase11b_audit.py`,
sha256 `131df4e9…`), aucun accès aux partitions ni au holdout.
Preuves : inventaire et empreintes ci-dessus, résultat
machine-readable `PHASE11B_AUDIT_RESULT.json`. Verdict : **BLOQUÉ**
(ANO-11B-01). Résultat chaîné seq302 ; livrables committés et
vérifiés distants (voir la chaîne et le commit associé).

**Même en cas de levée ultérieure du blocage, la Phase 11-C
(analyse anatomique H1/H4) nécessitera une autorisation distincte.
Aucune conclusion comportementale n'est produite par le présent
audit.**
