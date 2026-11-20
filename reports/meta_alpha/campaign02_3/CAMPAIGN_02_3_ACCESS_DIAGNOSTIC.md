# CAMPAGNE 2.3 (REPRISE) — DIAGNOSTIC D'ACCÈS DÉTAILLÉ (informations sensibles supprimées)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Sonde unique
autorisée (décision du propriétaire, seq 176), exécutée une fois le 2026-11-20
(run CI 44817313035). Aucune valeur d'identifiant affichée ou journalisée ; les
extraits ci-dessous sont les corps de réponse publics de l'API, expurgés.

## Résultats de la sonde (par point de vérification)

| Point de vérification | Méthode | Résultat |
|---|---|---|
| Authentification du compte propriétaire | `KaggleApi.authenticate()` (secrets CI régénérés) | Ne lève pas d'erreur d'authentification ; l'appel suivant est rejeté en autorisation |
| Accès au dataset | `dataset_list_files('marioadh/xauusd-is-b01')` | **403 Forbidden** (`ApiException`) |
| Autorisation de lecture (HTTPS direct, jeton Bearer) | GET `api/v1/datasets/list/marioadh/xauusd-is-b01` | **HTTP 403** — corps : `{"code":403,"message":"Permission 'datasets.get' was denied"}` |
| Autorisation de lecture (HTTPS direct, basic auth) | Même endpoint | **HTTP 403** — même corps |
| Accès aux fichiers nécessaires | Listage des fichiers du lot b01 | Non atteint (rejet en amont, à l'autorisation) |
| Repli Drive (contrôle unique du même run) | 1 partition, contrôle de taille | Échec rc=1 (refus de quota déjà documenté, non réessayé) |

## Diagnostic

Le message de l'API est un refus d'**autorisation** (`datasets.get` denied), pas
une panne réseau ni un dataset introuvable (qui répondrait 404). Trois causes
possibles, par ordre de vraisemblance au vu des archives du programme :

1. **Les datasets appartiennent à un autre compte.** L'historique commité de la
   migration (nov. 2026, `kaggle_migration/VERIFY.json` : `"username":
   "shalom5123"`, vérification distante `all_ok=true`, 282/282 fichiers) établit
   que les 8 datasets privés ont été créés et vérifiés sous le compte
   **`shalom5123`**. Un jeton régénéré sur le compte `marioadh` ne donne pas
   accès aux datasets **privés** d'un autre compte, même avec le bon slug : si
   le propriétaire réel des jeux de données est `shalom5123`, le slug
   `marioadh/...` désigne des datasets inexistants ou inaccessibles pour ce
   compte, et le slug `shalom5123/...` désigne des datasets privés non partagés
   avec `marioadh`. Les deux lectures produisent le même 403.
2. Le jeton régénéré n'a pas les droits de lecture API (portée restreinte) — à
   vérifier dans les réglages du jeton sur le compte concerné.
3. Les secrets CI n'ont pas pris la nouvelle valeur (à vérifier sans les
   afficher : longueur/format uniquement, jamais la valeur).

**Action propriétaire recommandée (une seule, pas de rotations répétées)** :
régénérer le jeton **sur le compte qui possède les datasets** (`shalom5123`
d'après la vérification de migration), ou partager explicitement les 8 datasets
avec le compte `marioadh` ; puis mettre à jour les secrets CI et confirmer. Une
nouvelle sonde unique sera alors lancée. Conformément à la décision, aucune
tentative supplémentaire n'a été faite après ce diagnostic.
