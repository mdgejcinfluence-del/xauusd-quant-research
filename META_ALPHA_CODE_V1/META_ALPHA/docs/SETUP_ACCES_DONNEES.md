# Accès aux données — guide pas à pas

Ce guide fait exactement deux choses : donner au système un accès **en lecture**
au corpus certifié de votre Drive, et un token **révocable** pour Kaggle.

Durée : ~15 minutes. Coût : **0 FCFA**.

> **À lire avant de commencer.** Je ne détiens aucun de vos identifiants. Le
> compte de service que nous créons est un robot Google, sans mot de passe, qui
> n'a accès qu'au dossier que vous lui partagez explicitement. Il se révoque en
> supprimant son accès au dossier. Aucun mot de passe Google n'est jamais demandé
> ni stocké.

---

## Étape 0 — Sur quel compte Google êtes-vous ?

Vous m'avez dit que le corpus est sur un **Drive spécial, différent de celui
connecté à cette conversation**. C'est important : le compte de service doit
être partagé avec **ce compte-là**, pas avec l'autre.

Notez l'adresse email exacte du compte propriétaire du corpus. Elle ressemble à
`quelquechose@gmail.com`. Vous en aurez besoin à l'étape 4.

---

## Étape 1 — Créer un projet Google Cloud

1. Ouvrir <https://console.cloud.google.com/>
2. En haut, cliquer sur le sélecteur de projet → **Nouveau projet**
3. Nom : `meta-alpha-research` → **Créer**
4. Attendre quelques secondes, puis sélectionner ce projet.

*Note : Google Cloud demande une carte bancaire pour certains services, mais
**pas** pour l'API Drive en lecture. Si une carte est demandée à un moment,
arrêtez-vous et dites-le-moi — nous utiliserons un autre chemin.*

---

## Étape 2 — Activer l'API Drive

1. Menu ☰ → **API et services** → **Bibliothèque**
2. Chercher **Google Drive API**
3. Cliquer dessus → **Activer**

Attendre que le bouton passe à « Gérer ». C'est fait.

---

## Étape 3 — Créer le compte de service et sa clé

1. Menu ☰ → **API et services** → **Identifiants**
2. **Créer des identifiants** → **Compte de service**
3. Nom du compte de service : `meta-alpha-reader`
4. **Créer et continuer**
5. Pour « Rôle » : **ne rien sélectionner** (laisser vide) → **Continuer**
6. **Terminé**

Puis, sur la liste des identifiants :

7. Cliquer sur le compte de service `meta-alpha-reader`
8. Onglet **Clés** → **Ajouter une clé** → **Créer une clé**
9. Type : **JSON** → **Créer**

Un fichier `.json` se télécharge. **Renommez-le `sa.json`** et gardez-le sur
votre ordinateur. Ce fichier est la clé : ne le partagez pas, ne le commitez pas.

Ouvrez-le avec un éditeur de texte : vous y trouverez une ligne
`"client_email": "meta-alpha-reader@meta-alpha-research.iam.gserviceaccount.com"`.
**Copiez cette adresse email** — c'est l'identité du robot.

---

## Étape 4 — Partager le dossier du corpus avec le robot

C'est l'étape qui donne réellement l'accès. Sans elle, la clé ne sert à rien.

1. Ouvrir <https://drive.google.com/> en étant connecté au **compte qui possède
   le corpus** (celui de l'étape 0)
2. Trouver le dossier **`META_ALPHA_XAUUSD_DGP`**
3. Clic droit → **Partager**
4. Coller l'adresse du compte de service de l'étape 3 :
   `meta-alpha-reader@meta-alpha-research.iam.gserviceaccount.com`
5. Permission : **Lecteur** (surtout pas Éditeur)
6. **Décocher** « Envoyer une notification » (le robot ne lit pas ses mails)
7. **Partager**

> Ne partagez **pas** tout votre Drive. Uniquement ce dossier. Le robot ne verra
> rien d'autre — c'est la garantie technique, pas une promesse.

---

## Étape 5 — Récupérer l'identifiant du dossier racine

Le système a besoin de l'ID du dossier `META_ALPHA_XAUUSD_DGP`.

1. Dans Drive, **double-cliquer** sur le dossier `META_ALPHA_XAUUSD_DGP`
2. Regardez la barre d'adresse du navigateur. Elle ressemble à :
   `https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz123456`
3. La partie après `/folders/` est l'ID. Copiez-la.

C'est la valeur de `GDRIVE_ROOT_FOLDER_ID`.

---

## Étape 6 — Tester l'accès (2 minutes)

Avant de configurer GitHub, on vérifie que ça marche vraiment.

Le dépôt doit être cloné localement. Puis :

```bash
pip install -r requirements-drive.txt
export GDRIVE_SA_JSON="$(cat sa.json)"
export GDRIVE_ROOT_FOLDER_ID="1AbCdEfGhIjKlMnOpQrStUvWxYz123456"
python -m metaalpha.drive_preflight
```

**Résultat attendu :**

```
"status": "PASS"
"partitions_count": 348
"p1_sha256_canonical": "a1b2c3..."
"p2_sha256_canonical": "d4e5f6..."
```

**Si vous obtenez autre chose, c'est normal la première fois.** Le message
d'erreur dit exactement quoi corriger :

| Erreur | Cause | Correction |
|---|---|---|
| `NO_REMOTE_BACKEND` | variables non exportées | refaire `export` dans le même terminal |
| `CERTIFICATE_MISSING` | mauvais dossier racine | vérifier `GDRIVE_ROOT_FOLDER_ID` : c'est bien le dossier qui contient `04_CHECKPOINTS/`, pas un sous-dossier |
| `PARTITION_COUNT_MISMATCH` | 347 ou 349 partitions | **arrêt volontaire** — on ne continue pas avec un corpus qui ne correspond pas au certificat |
| `403` ou `404` | dossier non partagé | refaire l'étape 4 avec l'email exact du robot |
| `ImportError` | dépendances manquantes | `pip install -r requirements-drive.txt` |

**Envoyez-moi la sortie exacte** (le JSON). Elle contient les deux SHA-256 qui
deviendront la référence inviolable du projet. Aucune donnée n'y apparaît.

---

## Étape 7 — Mettre les secrets dans GitHub (je vous guiderai)

À faire **après** que j'ai créé le dépôt. Le guide précis sera publié quand vous
m'aurez donné le nom d'utilisateur GitHub. En résumé, ce sera :

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

| Nom | Valeur |
|---|---|
| `GDRIVE_SA_JSON` | **tout le contenu** du fichier `sa.json` |
| `GDRIVE_ROOT_FOLDER_ID` | l'ID de l'étape 5 |
| `KAGGLE_USERNAME` | (étape 8) |
| `KAGGLE_KEY` | (étape 8) |

---

## Étape 8 — Token Kaggle

Kaggle n'est **pas** nécessaire pour commencer. Il le devient pour exécuter les
calculs lourds hors de votre machine.

1. Ouvrir <https://www.kaggle.com/settings>
2. Section **API** → **Create New Token**
3. Un fichier `kaggle.json` se télécharge, contenant `username` et `key`
4. Garder ce fichier ; il servira à l'étape 7

**Ce token se révoque** depuis la même page, un clic. C'est la différence
essentielle avec un mot de passe.

> Rappel important : le compte Kaggle doit respecter les conditions d'usage
> (recherche personnelle, non commerciale, 12 h par exécution, 30 h GPU/semaine).
> Nous n'utilisons **pas** le GPU — uniquement le CPU, 2 cœurs, 4 GB.

---

## Ce qui reste vrai après tout ça

Le corpus n'est pas copié ici. Il reste sur votre Drive. Le système lit une
partition à la fois, écrit ses résultats dans une zone de recherche séparée, et
ne touche jamais aux certificats.

Si un jour vous voulez couper l'accès : supprimer le partage de l'étape 4 suffit,
instantanément. Rien à révoquer ailleurs.
