# CAMPAGNE 2.2 — ÉTAT DU CHECKPOINT GITHUB

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Commit réconcilié

| Élément | Valeur |
|---|---|
| SHA complet | `18e6553852c38a2941c03fc507e4e236f42e4a7a` |
| Branche | `arena/afe12737-xauusd-quant-research` |
| Parent exact | `84f19a1dd1376f6b8ec97b0433c1479efed32347` |
| Vérification distante | `git ls-remote origin arena/afe12737-xauusd-quant-research` = `18e6553852c38a2941c03fc507e4e236f42e4a7a` — **le checkpoint est distant et vérifié** |
| Mode d'envoi | Push ordinaire (fast-forward `132403f..18e6553`), **aucun force push, aucune réécriture d'historique** |

## Inventaire des fichiers du commit

Le commit `18e6553` ne contient que deux fichiers (les autres éléments de la
livraison étaient déjà portés par les commits parents de la même session) :

- `reports/meta_alpha/campaign02_2/CAMPAIGN_02_2_EVENT_TIME_RECONSTRUCTION.md` (+112 lignes)
- `reports/meta_alpha/campaign02_2/CAMPAIGN_02_2_DATA_QUALITY.md` (+15 lignes)

## Contrôles effectués

- **Arbre de travail** : propre au moment du push (aucune modification non
  commitée) ; les compléments de la présente décision (seq 172) font l'objet d'un
  commit séparé postérieur, sans toucher au checkpoint.
- **Secrets** : balayage du diff du commit (motifs clé API, secret, mot de passe,
  jeton, clé privée) — aucun secret en clair ; seules des références à des *noms*
  de secrets CI (`${{ secrets.KAGGLE_KEY }}`) existent dans les workflows, ce qui
  est la forme normale et ne contient aucune valeur.
- **Historique** : la branche a avancé par fast-forwards et rebases locales de
  commits non encore poussés uniquement ; aucun commit déjà distant n'a été
  réécrit.

## Historique de l'incident

Pendant la session, le jeton d'écriture GitHub du sandbox a temporairement expiré
(push refusés, lectures et commits CI fonctionnels) ; les commits de livraison
sont restés locaux et propres pendant l'incident, puis ont été poussés tels quels
dès le rétablissement, sans modification de contenu.
