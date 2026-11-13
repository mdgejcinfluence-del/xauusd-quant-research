# Sécurité — dépôt public

Ce dépôt est **public par décision explicite du propriétaire**. Cette décision
est assumée et documentée. Elle impose une règle absolue : **aucun secret ne
vit ici**.

## Ce qui ne doit jamais être versionné

| Type | Où il vit à la place |
|---|---|
| `sa.json` / compte de service Google | GitHub Secret `GDRIVE_SA_JSON` |
| ID du dossier racine Drive | GitHub Secret `GDRIVE_ROOT_FOLDER_ID` |
| Token API Kaggle (`KGAT…`) | GitHub Secret `KAGGLE_KEY` + `KAGGLE_USERNAME` |
| Certificats Phase 1 / Phase 2 | Google Drive uniquement (lecture seule) |
| 348 partitions Parquet | Google Drive uniquement |
| État de gouvernance, décisions du propriétaire | Drive, `RESEARCH_.../00_GOVERNANCE/` |
| Résultats de recherche non publiés | Drive, jamais ce dépôt |

## Trois barrières automatiques

1. **`.gitignore`** — bloque parquets, certificats, `.env`, `sa.json`, clés.
2. **Hook pre-commit** (`.githooks/pre-commit`) — refuse tout commit contenant
   un motif de secret. Installer avec `python scripts/install_hooks.py`.
3. **CI `secrets`** (`metaalpha/secrets_guard.py`) — scanne l'arbre à chaque
   push et sur chaque pull request. Un secret trouvé casse le build.

Ces trois barrières sont indépendantes : en contourner une ne contourne pas les
autres.

## Ce que le garde-fou ne peut pas faire

- Il ne détecte pas une clé **reformatée** ou **encodée** hors motifs connus.
- Il ne protège pas un secret commité puis supprimé : **l'historique git le
  garde**. Si une clé est publiée par erreur, la seule réponse correcte est de
  la **révoquer immédiatement**, pas de réécrire l'historique.
- Il ne peut pas empêcher un collaborateur de coller une clé dans une issue ou
  une pull request. Ceux-là sont visibles de tous.

## Si une clé fuite

1. Révoquer la clé chez le fournisseur (Kaggle, Google Cloud) — immédiatement.
2. En émettre une nouvelle.
3. Mettre à jour le GitHub Secret concerné.
4. Écrire l'incident dans `00_GOVERNANCE/INCIDENTS.md` sur Drive.

Aucune autre étape n'est utile : réécrire l'historique d'un dépôt public ne
fonctionne pas, l'information est déjà copiée.

## Bonnes pratiques de jetons

- Préférer un **compte de service Google** à un mot de passe personnel.
  Un compte de service se révoque en une action et n'a accès qu'aux dossiers
  qu'on lui partage explicitement.
- Ne jamais partager le dossier **racine** du Drive personnel avec le compte de
  service : uniquement le dossier `META_ALPHA_XAUUSD_DGP`.
- Kaggle : le token se révoque depuis la page API tokens, un clic.
- GitHub : utiliser un *fine-grained PAT* limité à ce dépôt, jamais un token
  classique à portée globale.
- Aucun secret ne transite par une conversation, un fichier ou un notebook.

## Rapports

Ce dépôt contient de la recherche quantitative. Rien ici ne constitue une
garantie de performance, ni un conseil en investissement. Les résultats
négatifs sont conservés comme les positifs.
