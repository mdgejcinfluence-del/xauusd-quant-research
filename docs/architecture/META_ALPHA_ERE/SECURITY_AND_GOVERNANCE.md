# META ALPHA ERE — SÉCURITÉ ET GOUVERNANCE

## Gouvernance scientifique

Constitution 009 et Drift Guard s'appliquent avant chaque mission
(classification VERT/JAUNE/ORANGE/ROUGE consignée). Registre chaîné
SHA-256 (`TRIAL_LEDGER_CHAIN.json`, 492 entrées) : préenregistrement
avant calcul, résultats après, aucune réécriture. Registre des
modèles et journal des décisions dans `docs/governance/`.

## Intégrité des actifs

Moteurs gelés (V1/V2-F2) et checkpoints certifiés immuables, hashes
vérifiés par tests ; `main` jamais modifiée (branche de session
uniquement) ; partitions de marché jamais commitées (téléchargement
CI vérifié par taille/lignes/hash) ; manifestes SHA-256 par checkpoint.

## Sécurité opérationnelle

Aucun ordre réel, aucun capital engagé, aucun contournement de
plateforme (HFM : lecture publique seulement ; CI bloquée en 403 =
constat documenté, pas de contournement) ; aucun identifiant dans le
dépôt (l'authentification GitHub/CI est gérée par la plateforme) ;
collectes limitées aux sources autorisées et journalisées ; données
personnelles : aucune (traders identifiés par leurs identifiants
publics de plateforme uniquement).

## Prévention des fuites de preuve

Le risque principal du système est interne : une hypothèse qui devient
« fait » en traversant les modules. Défenses : niveaux de preuve dans
chaque objet (DATA_CONTRACTS), porte de gouvernance du module H,
critères de validation pré-déclarés, interdiction des examens
intermédiaires sur le prospectif, tests automatisés qui vérifient les
statuts du registre (ex. ME-001 ne peut pas apparaître VALIDATED sans
verdict prospectif).
