# CAMPAGNE 2.3 — AUDIT DES TERCILES DE PROFONDEUR À T0

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Seuils effectivement utilisés (résultats seq 171/172 et réplication 2.3)

| Variable (à T0) | Borne BAS/MOYEN | Borne MOYEN/HAUT | Population de référence |
|---|---|---|---|
| Profondeur atteinte sur la barre de franchissement (`prof_max_jusqua_bp`, snapshot 0) | **1,4853 bp** | **3,4476 bp** | 12 138 épisodes T0 de l'extraction partielle (2010-01-04 → 2014-03-11) |
| Profondeur initiale de clôture (`profondeur_initiale_bp`) | **0,8007 bp** | **2,3646 bp** | Même population |

## Méthode de calcul

Quantiles empiriques 1/3 et 2/3 de la distribution **poolée sur tout le périmètre
extrait**, calculés après extraction (implémentation : `pd.qcut` sur les rangs,
`method='first'` pour départager les ex æquo). Les groupes obtenus comptent
4 046 à 4 048 épisodes chacun. Dans les campagnes 2/2.1, les terciles de la
profondeur (rétrospective) étaient calculés **par ère** ; ici, sur le périmètre
restreint dominé par l'ère 2010–13, le découpage est **global au périmètre** —
différence de construction écrite, non masquée.

## Caractère des seuils — ce qu'ils sont et ne sont pas

- **Descriptifs et rétrospectifs** : les bornes sont connues seulement après avoir
  observé l'ensemble du périmètre ; un épisode de 2010 est classé avec des
  quantiles incluant des données de 2013. Ils servent à décrire la répartition
  d'une association, pas à décider en temps réel.
- **Non chronologiques** : aucun seuil n'est calculé « à date » ; il n'existe dans
  cette campagne aucun seuil causal roulant.
- **Non transférables tels quels** : recalculés sur le corpus décennal, ils
  bougeront (les profondeurs de 2017–20 sont structurellement plus faibles) ; la
  reprise devra publier ses propres bornes et ne pas réutiliser celles-ci comme
  constantes.

## Exigence pour toute utilisation future (opérationnelle ou prédictive)

Tout seuil de classification utilisé à l'instant t devra être calculé
**uniquement à partir de données strictement antérieures à t** (par exemple
quantiles roulants sur une fenêtre close avant l'événement, figés à l'avance),
avec la fenêtre, la règle de mise à jour et le traitement des ex æquo spécifiés
avant calcul. Les terciles du présent audit ne satisfont pas cette exigence et ne
doivent pas être présentés comme des seuils opérationnels.

## Addendum seq 178 — seuils sur le périmètre décennal complet

| Variable (à T0) | Borne BAS/MOYEN | Borne MOYEN/HAUT | Population |
|---|---|---|---|
| Profondeur atteinte (barre T0) | **1,2499 bp** | **2,9694 bp** | 36 005 épisodes T0 avec issue mesurable (2010–2019) |
| Profondeur initiale de clôture | **0,6748 bp** | **1,9879 bp** | Même population |

Même méthode (quantiles poolés du périmètre, rétrospectifs) et même exigence pour
tout usage futur : seuils calculés uniquement sur des données antérieures à
l'événement. Les seuils du fragment 2010–2014 (1,4853/3,4476 bp) restent conservés
ci-dessus comme valeurs historiques du périmètre restreint.
