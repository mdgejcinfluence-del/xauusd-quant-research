# ME-001.3 — BUDGET DE RISQUE À L'ENTRÉE

Base : 1 797 épisodes ME-001.2 avec volatilité pré-entrée (vol15,
information disponible avant l'entrée) fusionnée depuis ME-001.1
(84 % des épisodes ; écarts de segmentation documentés). Politiques
gelées en seq484, aucune optimisée sur la validation.

## Fait mathématique de départ (DÉMONTRÉ)

Une exposition constante multiplie gains et pertes par le même
facteur : elle ne change ni le signe de l'espérance, ni le PF, ni la
part des gains absorbée par la queue. Le dimensionnement ne « répare »
donc pas un edge ; seuls le **filtrage à l'entrée** et la
**pondération différenciée** peuvent modifier l'économie relative.

## Résultats (espérance bp par épisode actif, PF ; découverte → validation)

| Politique | Découverte | Validation | ES95 (val.) | Lecture |
|---|---|---|---|---|
| P0 constante | +1,08 ; PF 1,19 | +1,97 ; PF 1,37 | −98,8 | référence |
| P1 inverse-volatilité | +3,66 ; PF 1,48 | +4,41 ; PF 1,65 | −123,9 | améliore l'espérance pondérée des deux côtés, mais **aggrave la queue absolue** (exposition moyenne 1,5–1,7) |
| P2 exclusion vol > Q75 (découverte) | +2,80 ; PF 1,73 | +3,34 ; PF 1,95 | −68,8 | **améliore espérance, PF et queue des deux côtés** en écartant ~25–38 % des épisodes |

## Verdicts aux questions

1. **Limiter l'impact des non-récupérations ?** Partiellement, par
   filtrage : P2 réduit l'ES95 de ~30 % et la pire perte de −257 à
   −145 bp en validation (FORTEMENT ÉTAYÉ dans ce cadre de mesure).
2. **Part absorbable** : à budget de 1 % de capital par −200 bp, un
   épisode extrême (−546 bp) coûte 2,7 % du capital — absorbable
   isolément ; le risque réel est la répétition corrélée, non mesurée
   comme ruine faute de série de capital complète.
3. **Récupérations après coûts** : conservées par P2 (taux de
   gagnants 88→93 %), car le filtre agit avant l'entrée, pas pendant.
4. **Rendement / capital mobilisé** : faible en valeur absolue
   (quelques bp par épisode pour des durées médianes d'heures) ;
   intéressant seulement relativement aux autres politiques.
5. **Robustesse entre périodes** : direction de P2 identique en
   découverte et validation ; amplitudes variables, et le seuil 5 bp
   reste le plus fragile (P0 : +0,31 en validation sur ce
   sous-ensemble, contre un résultat négatif au catalogue complet
   ME-001.1 — écart de sous-ensemble déclaré).
6. **Dépendance aux extrêmes** : persiste partout (pire perte
   −115 à −290 bp selon politique/seuil).
7. **Renforcements nécessaires ?** NON DÉMONTRABLE ici ; l'association
   LMD-008 reste négative et rien ne montre qu'un renforcement soit
   requis pour capter la récupération mesurée sans lui.
8. **Famille candidate pour validation indépendante ?** P2 (exclusion
   sur volatilité préalable élevée) est la seule qui améliore
   simultanément espérance, PF et queue dans les deux groupes :
   **COMPATIBLE MAIS NON IDENTIFIÉ** — candidate à un protocole
   prospectif, pas un edge validé.
9. **Incertitudes** : sous-ensemble à volatilité disponible (84 %),
   Bid/Ask HFM réel, corrélation temporelle des épisodes, seuil
   d'exclusion dérivé de la découverte (à re-geler, pas à réajuster).

ME-001 reste **SIGNATURE_DETECTED**. Aucune politique n'est déclarée
optimale ; le dimensionnement gère la queue, il ne crée pas le rendement.
