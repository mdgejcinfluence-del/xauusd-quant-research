# PHASE 11-B.1 — RECONSTRUCTION DÉTERMINISTE DES IDENTIFIANTS D'ÉVÉNEMENTS ET DES GRAPPES HISTORIQUES

**Verdict : RECONSTRUCTION CONFORME — reprise de l'audit 11-B :
ADMISSIBLE POUR PHASE 11-C (Phase 11-C non autorisée par la présente
mission).** Autorisation chaînée seq303 ; audit initial bloqué seq302
(ANO-11B-01). Protocole `PHASE11_PROTOCOL.md` gelé et inchangé.

## 1. Sources historiques retrouvées (avant toute reconstruction)

- **Algorithme** : fonction `composantes` de
  `ci_tools/phase10_synthesize.py` (lignes 20–29), introduite par le
  commit `84a3c5a` (2026-11-21) et **identique à l'octet près** entre
  ce commit et HEAD (la correction ultérieure `102f865` n'a touché
  que `boot_cluster`). Elle est importée telle quelle par
  `ci_tools/phase10_synthesize_correction.py`, le code qui a produit
  les comptes de la campagne corrective **45011013927** (commit des
  résultats `817b974`). La campagne initiale 44919631588, défectueuse
  pour F10-01/F10-03, n'est pas utilisée comme source.
- **Définition exacte** : composantes connexes de recouvrement
  [t_signal, t_sortie] — événements triés par t_signal ; nouvelle
  composante si et seulement si t_signal est **strictement** supérieur
  au maximum des t_sortie déjà vus (l'égalité reste dans la
  composante) ; sinon extension de ce maximum. Aucun paramètre libre,
  aucune fenêtre ni distance.
- **Périmètre d'origine** (retrouvé dans le code de synthèse) :
  événements **admissibles uniquement** (entree_eligible = 1 et
  fenetre_complete = 1), traités **par famille séparément** (jamais de
  connexion H1–H4) ; les exclus ne participent pas au clustering et
  conservent leur statut. Ordre de traitement : tri chronologique
  interne à l'algorithme ; les appartenances sont invariantes à
  l'ordre des égalités de t_signal (même instant, même composante).

## 2. Méthode de construction des identifiants

- `event_id` : SHA-256 de la sérialisation canonique
  `famille|timeframe|t_signal|sens` (sens formaté `+1`/`-1`,
  horodatage UTC à la précision stockée), préfixé `EV-`. Aucun numéro
  de ligne, aucun hasard ; champs sources inchangés.
- `grappe_id` : `GR-<famille>-<rang>` où le rang (5 chiffres) suit
  l'ordre chronologique des composantes produit par l'algorithme
  historique. **Les identifiants d'origine n'ont jamais existé** :
  ce sont de nouvelles étiquettes déterministes attribuées aux
  composantes historiques reproduites, non la récupération
  d'identifiants originaux.
- Exclus : `grappe_id` vide (aucune appartenance artificielle),
  `statut_admissibilite` et `motif_exclusion` historiques conservés
  (ENTREE_INELIGIBLE / FENETRE_INCOMPLETE / AUCUN).
- Artefact dérivé : `PHASE11B_EVENT_CLUSTER_MAP.csv` (3 896 lignes +
  en-tête = chaque événement du manifeste représenté exactement une
  fois), sha256 `3281f594…`. Le manifeste source n'a jamais été
  modifié : empreinte `57b7b8af…` identique avant et après.

## 3. Contrôles de reproductibilité et de cohérence

| Contrôle | Attendu | Observé |
|---|---|---|
| F10-01 détectés / admissibles / non admissibles | 3 134 / 3 107 / 27 | 3 134 / 3 107 / 27 |
| F10-03 détectés / admissibles / non admissibles | 762 / 660 / 102 | 762 / 660 / 102 |
| Grappes F10-01 / F10-03 | 2 617 / 597 | **2 617 / 597** |
| event_id uniques / collisions | 3 896 / 0 | 3 896 / 0 |
| Mélange H1–H4 dans une grappe | aucun | aucun (max 1 famille par grappe) |
| Tailles de composantes | vérifiables | max 7 (H1), 4 (H4) ; 2 202 / 542 singletons |
| Seconde exécution indépendante | identique | identique à l'octet près (même sha256) |
| Empreinte du manifeste source | inchangée | inchangée |

La fidélité ne repose pas sur les seuls comptes : code, paramètres
(aucun), entrées (t_signal/t_sortie des admissibles du manifeste
correctif) et périmètre sont ceux des sources historiques vérifiées
ci-dessus ; le script de reconstruction
(`ci_tools/phase11b1_reconstruct.py`) importe la fonction historique
sans la réécrire.

## 4. Anomalies secondaires (registre conservé)

- **ANO-11B-02** (clé composite sans colonne event_id) : résolue pour
  l'identification par la matérialisation ci-dessus, unicité
  vérifiée. Ne bloque pas la Phase 11-C.
- **ANO-11B-03** (P0 non stocké) : **non bloquante**. Le protocole
  gelé définit P0 comme le Mid de clôture de la bougie déclencheuse ;
  la bougie est identifiable sans ambiguïté par t_signal + timeframe,
  et P0 est lisible sur les barres M1 IS documentées (282 partitions,
  3 540 993 barres M1). Lecture à effectuer en Phase 11-C, sans
  modifier le manifeste.
- **ANO-11B-04** (fenêtres causales en agrégat seulement, 202/208) :
  **non bloquante**. Le protocole gelé ne requiert aucun registre par
  fenêtre ; les populations de la Phase 11-C sont les événements.
  Limite conservée au registre.

## 5. Reprise des contrôles finaux de la Phase 11-B et verdict complet

Tous les contrôles de l'audit 11-B sont désormais satisfaits pour les
deux populations : provenance établie et manifeste défectueux exclu,
comptes conformes, identifiants d'événements matérialisés et uniques,
appartenances aux grappes historiques reproduites et matérialisées,
exclusions traçables, fenêtres causales conformes sur comptes
chaînés, périmètre IS respecté, holdout jamais accédé.

**Verdict complet : ADMISSIBLE POUR PHASE 11-C.** Ce verdict ne vaut
pas autorisation : la Phase 11-C (analyse anatomique H1/H4) reste
suspendue à une décision distincte du responsable. Aucune
trajectoire, aucun MFE/MAE, aucun calcul économique n'ont été
produits par la présente mission.

## 6. Procès-verbal

Autorisation seq303 ; exécution par `ci_tools/phase11b1_reconstruct.py`
(import de l'algorithme historique, double exécution concordante) ;
preuves : empreintes du manifeste source avant/après, sha256 de la
carte, comptes ci-dessus ; résultat machine-readable
`PHASE11B_1_RESULT.json` ; résultat chaîné seq304, livrables committés
et vérifiés distants (commit associé au présent livrable).
