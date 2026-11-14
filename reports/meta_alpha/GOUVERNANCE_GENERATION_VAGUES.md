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

## DIRECTIVE COMPLÉMENTAIRE (propriétaire) — extraction avant toute vague
1. Le registre d'anomalies (`anomaly_registry.py`) est un OUTIL, pas une découverte:
   aucune anomalie ne doit être créée artificiellement pour l'alimenter. La prochaine
   mission est une ANALYSE RÉELLE des données IS produisant des observations mesurées.
2. Après le verdict de P3-002: INTERDICTION de passer directement à la vague suivante.
   Étape obligatoire d'extraction phénoménologique structurée sur IS: distributions,
   comportements conditionnels, granularités, changements de régime, asymétries,
   dépendances, transitions, événements extrêmes, relations spread/volatilité/
   intensité/variations, et phénomènes inattendus hors familles initiales — guidée
   par les résultats antérieurs et la base K.
3. Chaque anomalie détectée est enregistrée dans GitHub avec mesures, partitions
   sources, hashes, limites et statut (DESCRIPTIVE par défaut). La session suivante
   doit tout retrouver dans le dépôt, sans mémoire de session.
4. Les hypothèses ne sont construites QU'APRÈS cette extraction; une anomalie peut
   fonder plusieurs hypothèses si plusieurs mécanismes distincts sont justifiés;
   le nombre suit les découvertes, jamais un quota ni un produit cartésien.
5. Autonomie non démontrée: ne jamais la prétendre. Calculs/diagnostics = automatisés;
   jugement scientifique d'Arena = tracé dans décisions et préenregistrements;
   limites de continuité signalées honnêtement.
6. CONDITION DE PASSAGE (toutes requises avant toute nouvelle vague):
   verdict réel de P3-002 + extraction phénoménologique documentée + validation des
   anomalies enregistrées + justification scientifique de chaque hypothèse +
   préenregistrement et verrouillage de la vague.
