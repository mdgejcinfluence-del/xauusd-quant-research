# P11-A1 — ANNEXE QUALITÉ ET DISPONIBILITÉ DES DONNÉES

**Périmètre** : événements FOMC/NFP/CPI du calendrier point-in-time du programme
(`F15_EVENTS.csv`, timestamps `available_at_utc`), corpus tick historique IS
(282 partitions, borne 2020-01-20T09:36:27Z), fenêtre T−5→T+30 min.

## Couverture effective

| Famille | Événements réels attendus (P11-A0) | Extraits | Couverture |
|---|---|---|---|
| FOMC | 81 | 81 | 100 % |
| NFP | 129 | 118 | 91,5 % |
| CPI | 136 | 127 | 93,4 % |
| **Total** | **346** | **326** | **94,2 %** |

Les 20 événements non extraits correspondent à des partitions dont la récupération a
échoué (voir incidents d'accès ci-dessous) ; aucun n'a été imputé ni remplacé. Chaque
mesure du rapport porte donc n = 326 événements et 36 minutes par événement
(11 736 lignes). Sur les événements extraits, la couverture temporelle médiane est de
36/36 minutes : aucun trou de minute entière au sein de la fenêtre.

## Synchronisation, fuseaux, résolution

- Événements : `available_at_utc` du pack exogène PIT (conversion America/New_York →
  UTC date par date, DST vérifié seq 105 ; FOMC 19 h UTC l'hiver / 18 h l'été).
- Ticks : `timestamp_utc` des partitions, horodatage à la seconde au plus fin ; les
  écarts inter-ticks mesurés (médiane 0,10–0,14 s en fenêtre d'annonce) reflètent la
  densité du flux, non une horloge sub-seconde certifiée — la résolution effective est
  celle de l'enregistrement d'origine, non re-vérifiable au-delà.
- Alignement : minute m = plancher((ts − T)/60 s) ; correction appliquée en cours
  d'exécution (timestamps tz-aware convertis en UTC naïf) après deux échecs consignés
  (pytz absent, soustraction tz) — moteur final chaîné au dépôt.
- Doublons : l'ordre (timestamp, observation_id) est celui du moteur F15 éprouvé ;
  aucun doublon de minute n'est possible par construction de l'agrégation.

## Incidents d'accès (consignés, sans contournement de périmètre)

1. Package `kaggle` récent : import circulaire → épinglé 1.6.17.
2. API Kaggle : **403 Forbidden** sur les lots du programme (accès modifié depuis les
   runs F15) — aucune donnée d'identification n'a été affichée ; diagnostic committé
   en type d'erreur seul.
3. Repli utilisé : miroir Drive du même corpus (patron F15 `dl_drive`, vérification
   de taille exacte par fichier) — même corpus du programme, aucune nouvelle donnée,
   aucun achat. C'est ce repli qui a produit l'extraction (run 44691627613, succès).
   Les 20 événements manquants correspondent aux partitions restées en échec de
   téléchargement après reprises.

Le corpus brut n'a jamais été versé dans Git : seuls les agrégats par minute et par
événement sont versionnés, conformément à l'autorisation.

## Différences de fournisseur et de qualité de cotation

Le corpus est le flux historique unique du programme (même fournisseur sur l'ensemble
de l'IS) : aucune comparaison inter-fournisseurs n'est possible en interne, et le
spread « habituel » de référence est donc celui du même flux (pré-annonce de chaque
événement, médiane 2,28–2,68 bp selon la famille). Les queues de distribution par
événement sont fournies (`P11_A1_EVENT_METRICS.csv`) pour qu'aucun événement
exceptionnel ne déforme silencieusement les globales : P99 du spread médian de minute
à T+1 = 11,5 bp (FOMC) contre médiane 2,9 bp — l'écart est visible, pas moyenné.

## Quantités restées NON MESURABLES après P11-A1

- Slippage réel, latence d'ordre, probabilité de remplissage : aucune donnée
  d'exécution n'existe dans le programme (structurel, cf. rapport d'exécution).
- Cotations « périmées » au sens d'un courtier donné : le flux ne porte pas de drapeau
  de staleness ; seuls les écarts inter-ticks sont mesurés (proxy déclaré comme tel).
- Conditions d'un compte retail spécifique : hors corpus par construction.
