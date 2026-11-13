# META ALPHA — État d'infrastructure (13 novembre 2026, session autonome)

## Fait et prouvé
- Code V1 importé (SHA-256 consigné), scan secrets propre, **143/143 tests verts**.
- 4 démos exécutées : contrats, échelle L0–L7, dispatch (perte de segment sans rejeu), bout-en-bout.
- Hook pre-commit installé. Dépendances non déclarées corrigées (google-auth-oauthlib, pytz).
- Certificats P1/P2 : CERTIFIED, vérifiés valeur par valeur sur les octets réels.
- **BASELINE_HASH_MANIFEST.json écrit** : empreintes canoniques P1 `9bbeb9a2…`, P2 `bb3b63f1…`,
  empreinte de liste des 348 partitions `sha256:2b21ef60…`.
- **Inventaire 348/348 clos** : total 685 118 625 lignes, écart 0 vs certificat.
  Deux signatures de schéma en blocs contigus (001–294 / 295–348) — voir QUOTE_DGP_SPEC_V1.
- Accès données durable : liens publics Drive consignés (racine, partitions, certificats)
  + automatisation GitHub Actions (import, sondes, inventaire) — coût 0 FCFA.

## Point d'arrêt légitime suivant (pas un blocage technique)
L'échelle monte seule L0→L4. Le barreau L5 exige les **9 décisions de définition**
du propriétaire (horizons, fenêtres de volatilité, seuil de saut, etc.) :
`record_answers` refuse toute attribution non humaine, par conception — l'autorisation
d'être autonome ne vaut pas réponse à la place du propriétaire. Elles seront présentées
en une page simple, exemples et conséquences, quand le propriétaire le souhaite (~10 min).

## Ce qu'il manque pour le calcul distribué (phase dispatch)
Secrets GitHub à déposer par le propriétaire (jamais dans le code) :
- `KAGGLE_USERNAME` + `KAGGLE_KEY` (API Kaggle) — le seul élément demandé maintenant.
- Ensuite seulement, pour le préflight officiel par compte de service :
  `GDRIVE_SA_JSON` + `GDRIVE_ROOT_FOLDER_ID` (les liens publics couvrent déjà la lecture).

## Non fait, assumé
- Dépôt public `meta-alpha-xauusd` : bascule à présenter au propriétaire (code prêt,
  scan propre) — aucune poussée publique faite en silence.
- Moteurs P3–P7 : à écrire contre le schéma réel désormais connu, phase par phase, gate par gate.
- Holdout : scellé. Aucune ouverture. Aucune acceptation de phase à la place du propriétaire.
