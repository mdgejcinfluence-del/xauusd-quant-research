# CAMPAGNE 7 — PROCÈS-VERBAL DE GEL DÉFINITIF DU PROTOCOLE F-I V1

**Décision du propriétaire : validation du protocole consolidé F-I V1
et autorisation du gel définitif.** Enregistrée au registre chaîné en
seq249 (autorisation) et seq250 (gel). **Le gel ne vaut pas
autorisation d'exécution : aucun calcul, aucune extraction et aucune
consultation de résultats F-I ne sont autorisés à ce stade ; un ordre
explicite distinct du propriétaire sera nécessaire.**

## Document gelé (SHA-256 vérifié avant chaînage)

| Document | SHA-256 complet |
|---|---|
| `CAMPAIGN_07_PROTOCOL_V1.md` | `250909314f7df58eba43c0a848a49bfa09387f70c8f025249cc8c527e110f382` |

## Documents compagnons (intégrité confirmée, hashes de la préparation seq246 revérifiés à l'identique)

| Document | SHA-256 complet |
|---|---|
| `CAMPAIGN_07_FI_BLUEPRINT.md` | `749d345648e62a2a53b753473d0c5e63a7a84b7da85cd4ee331ca8060a578158` |
| `CAMPAIGN_07_FI_DICTIONARY.md` | `334c893982ef3caafceb381e11a40394613e9b043f98791dcd6a58d8b710d2d2` |
| `CAMPAIGN_07_FI_COMPARISONS.md` | `a89e5a2a9df85f7d295734408b9ff93df06a807f9c26a6445cca2b543d2ec69b` |
| `CAMPAIGN_07_FI_COVERAGE_BIASES.md` | `d8c06fef39825bd9876a1cfaf0c77696383fcc39b0d9e049982d01b79d07d815` |

En cas de tension, le protocole consolidé V1 prévaut sur les documents
compagnons.

## Incident documentaire mineur (transparence du gel)

Lors de la vérification pré-gel, le fichier du protocole présentait le
hash `0291a70d…` au lieu du hash validé `25090931…`. Diagnostic : une
correction cosmétique d'un caractère (espace dans une référence de
hash tronquée, ligne 7 : « `d8c06fe f…` ») avait été appliquée au
fichier **après** l'émission du hash soumis au propriétaire. Le fichier
a été restauré **à l'octet près** dans l'état correspondant au hash
validé (revérifié : `250909314f…82`), et c'est cet état exact qui est
gelé. La coquille subsiste donc dans la référence tronquée de la
ligne 7 ; elle est sans portée (le hash complet du document compagnon
concerné figure au présent procès-verbal : `d8c06fef39825b…`). Aucune
autre différence de contenu n'existe entre les deux états (diff Git :
une ligne, un caractère).

## Contenu gelé (rappel, sans modification)

- Placebo : G50 +25 USD demi-pas exact (référence primaire, I-01,
  I-02, I-03, I-05) ; R100 +25 USD translation non équivalente (quart
  de pas, descriptive uniquement) ; R10 +5 USD demi-pas exact (dans le
  périmètre du protocole) ; aucun placebo multiple de 10.
- Cinq comparaisons I-01..I-05, constantes (bande d'approche 25 bp,
  washout 60 min, seuil de rejet 25 bp, suivi 60 min), contrôle de
  composition déterministe sans p ajoutée, BY famille de cinq à m = 5
  fixe, lectures fermées.
- Aucune modification méthodologique après le gel, sauf addendum
  distinct chaîné avant toute exécution.

## Restrictions

Aucun calcul F-I pendant la préparation ni pendant le gel. XAU/USD
exclusivement ; holdout 2020–2026 scellé ; aucun backtest ni
`challenge_sim` ; aucun J2/J3 automatique ; aucun budget expérimental
consommé ; FRED suspendue ; 36 cellules S12 gelées ; T0 séparé et
inactif ; fiches historiques non modifiées ; candidates C5 sans
priorité ; F-H en réserve.

**STATUT : F-I V1 — PROTOCOLE DÉFINITIF GELÉ (seq250) — EXÉCUTION EN
ATTENTE D'UN ORDRE DISTINCT DU PROPRIÉTAIRE.**
