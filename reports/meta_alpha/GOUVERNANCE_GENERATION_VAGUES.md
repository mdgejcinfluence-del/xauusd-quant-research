# GOUVERNANCE DE GÉNÉRATION DES VAGUES (contraignante, dès P3-003)

## Mécanismes implémentés (versions isolées, effet après P3-002)
- `ci_tools/anomaly_registry.py`: registre d'anomalies à 15 champs obligatoires,
  statut DESCRIPTIVE par défaut, hashes code/config/données exigés.
- `ci_tools/gate_engine_v2.py`: BY + compteur cumulatif (v1 conservée intacte).
- Validité et limites du dispositif: `MULTIPLICITE_VALIDITE.md`.

## Admission d'une hypothèse (toutes conditions requises)
1. Citation d'au moins un item K de BASE_CONNAISSANCES_PHASE2.md, lui-même
   fondé sur les 5 mesures de qualification phénoménologique.
2. Lien explicite avec l'expérience parente (vague, hypothèse, diagnostic chiffré).
3. Définition mathématique complète, protocole, critères de succès ET de rejet.
4. Aucune ressemblance paramétrique avec une hypothèse rejetée (même feature,
   même horizon, seuil/fenêtre simplement déplacés = retest interdit).
5. Préenregistrement + verrouillage SHA-256 dans TRIAL_LEDGER_CHAIN.json
   AVANT tout calcul; le workflow vérifie la chaîne avant d'exécuter.

## Après un échec de vague (procédure obligatoire)
1. Lire le diagnostic quantitatif du gate (causes codées + chiffres par famille).
2. Retourner aux DONNÉES: analyse approfondie sur IS (distributions, rythmes,
   dépendances, régimes, dynamiques autour des trous de marché K5, etc.).
3. Documenter tout phénomène nouveau selon les 5 mesures -> nouvel item K.
4. Seulement alors: formuler les hypothèses de la vague suivante.
Le compteur cumulatif d'hypothèses (FDR élargi) ne se remet jamais à zéro.

## Volume
Aucun quota. Une vague peut contenir 3 hypothèses si 3 phénomènes sont
documentés, ou 300 si 300 le sont. La quantité suit la phénoménologie.
