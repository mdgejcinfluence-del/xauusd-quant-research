# ÉTAPE B — RAPPORT ÉCONOMIQUE P9-E : RETRACEMENT SELON L'HEURE D'ATTEINTE (ANO-C5-003)

**Avertissement de composition conservé intégralement.** Source :
`CAMPAIGN_05_ATTEINTES_JOUR.csv.gz`, premières atteintes réelles
identifiables, ordre déterminé, fenêtre +60 complète : avant 13:00
n = 1 550 ; dès 13:00 n = 445 (effectifs de la comparaison gelée C5-08).

## Distributions de composition (le cœur du dossier)

| | Avant 13:00 | Dès 13:00 |
|---|---|---|
| Sessions (C8 : S1 00–07, S2 07–13, S3 13–21, S4 21–24) | S1 63,5 % · S2 36,5 % · S3 0 % | **S3 99,6 %** |
| Ères 2010–13 / 2014–16 / 2017–20 | 34,8 / 32,9 / 32,3 % | 36,6 / 33,5 / 29,9 % |

Les deux bras sont des **sessions disjointes par construction** :
« avant 13:00 » signifie Asie et matinée européenne, « dès 13:00 »
signifie session américaine. Les ères, elles, sont comparables.

## Mouvements disponibles

| Médiane +60 min | Avant 13:00 | Dès 13:00 |
|---|---|---|
| Retracement maximal (bp) | 7,92 | 13,07 |
| Extension maximale (bp) | 14,47 | 23,96 |
| Position finale signée (bp) | +1,88 | +3,37 |

Tout croît ensemble après 13:00 — retracement, extension et position
finale : c'est l'**échelle de volatilité de la session américaine**,
pas un avantage du fade le matin. Un fade d'atteinte gagnerait en
médiane *moins* là où la fiche semblait le favoriser, et la position
finale médiane reste du côté de l'atteinte dans les deux bras
(continuation nette). Aucune espérance de fade positive ne se dégage
des grandeurs stockées ; le spread à l'atteinte n'est pas stocké en
campagne 5 (proxy observé campagne 1 : spread médian EV2 2,28 bp —
déjà du même ordre que l'écart de position finale).

## Verdict P9-E : **ABANDONNER** comme candidate stratégique

Conformément à l'ordre : l'effet dépend d'une composition (la session)
qui n'est pas comparable entre bras — l'heure d'atteinte *est* la
session. L'association ANO-C5-003 reste publiée comme fait descriptif
J1 avec son avertissement ; elle ne fonde ni règle, ni filtre, ni
candidature. Aucun contrôle supplémentaire n'a été inventé pour la
réhabiliter.
