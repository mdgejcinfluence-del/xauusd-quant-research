# VALIDATION DU MOTEUR SCIENTIFIQUE (gate + registre verrouillé)

## 1. Gate déterministe — reproduction des verdicts historiques (exigée avant usage)
Commandes exécutées localement sur les données d'origine:
- `gate_engine.py buckets P3_001_RESULTS.json` -> **0 survivant** (effets 0,1-0,5 bp,
  filtre économique K2 = 2,17 bp): conforme au verdict historique
  « pattern détecté, NON qualifié ».
- `gate_engine.py trades P4_001_RESULTS.json` -> **REJETE**: conforme au verdict
  historique (IC OOS entièrement négatifs, cause ABSORBE_PAR_SPREAD).
**Reproduction: OK pour les deux.** Le moteur est autorisé à juger P3-002.

## 2. Registre verrouillé — test de falsification réel
Chaîne `TRIAL_LEDGER_CHAIN.json`: 4 entrées ancrées (verrou du registre P3-002 par
SHA-256, verdicts P3-001/P4-001). Test: modification après coup du verdict seq 2 ->
vérification = « hash invalide seq 2 » (détecté). Restauration -> « chaine valide ».
Protection: casser la chaîne exige de réécrire toutes les entrées suivantes, ce qui
laisse une trace dans l'historique Git distant du fichier (ancrage externe).
Le workflow `gate.yml` refuse tout calcul si la vérification échoue.

## 3. Correction des tests multiples séquentielle
BH-FDR avec m = compteur cumulatif de toutes les vagues (127 aujourd'hui, lu depuis
le registre chaîné), pas seulement la vague courante. Chaque vague rend la suivante
plus exigeante: c'est le prix explicite de la recherche adaptative.

## 4. Arena — limite documentée, solution en place
Voir ETUDE_ARENA_AUTOMATISATION.md: pas de LLM sans session ni budget; couche
déterministe autonome + DECISION_REQUISE.json consommée dès l'ouverture d'une session.

## 5. Reste à activer
Dès la fin du run P3-002 (43600799780, en cours, protocole intact): appliquer le gate
codé via `gate.yml` (workflow_call), consommer DECISION_REQUISE, préenregistrer la
vague suivante depuis la base K uniquement. Aucun reparamétrage des rejetées.
