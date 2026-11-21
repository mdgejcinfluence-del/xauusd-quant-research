# CAMPAGNE 5 — COUVERTURE, COÛTS DE CALCUL ET RÈGLES DE SUSPENSION

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## 1. Matrice de couverture historique (livrable n° 6)

| Source | Périmètre | Usage campagne 5 | État |
|---|---|---|---|
| Corpus tick IS (282 partitions, `shalom5123`, HTTPS direct) | 2010-01-04 → 2019-12-16 ; 3 540 993 barres M1 reconstituées (campagnes 2.3–4) | Ouvertures, transitions, atteintes, trous inter-jours | Accessible, intégrité 282/282 vérifiée à chaque campagne |
| Bruts quotidiens campagne 4 (`CAMPAIGN_04_DAILY.csv.gz`) | 2 572 journées utilisables, états et comptages | Recoupement des journées utilisables et des sessions ; **aucune étiquette F3 poolée importée** (audit seq 199) | Commité, consulté |
| Découpage sessions des campagnes 1–4 | Sessions UTC 00–08/08–13/13–21/21–24 | Convention reprise à l'identique, publiée | Gelée par l'usage |
| Flux prospectif T0 / holdout / FRED | — | **Aucun usage** (interdits) | Non accédés / suspendue |

## 2. Périodes et cas incomplets — traitement attendu

- **Bords du corpus** : premières journées sans référence causale complète
  (60 journées) et première semaine sans semaine précédente utilisable —
  zones d'amorçage comptées et publiées, aucun événement déclaré sur
  référence censurée.
- **Journées présentes mais sous le seuil de qualité** (525 journées
  < 300 barres au sens de la campagne 4) : exclues des mesures,
  comptées ; une journée exclue ne peut servir ni de journée de référence
  H_{j−1}/B_{j−1} (on prend la précédente **utilisable**, règle du
  dictionnaire), ni rompre silencieusement une semaine (semaines à moins
  de 4 journées utilisables censurées pour l'hebdomadaire).
- **Semaines incomplètes** (jours fériés, semaines tronquées aux bords) :
  publiées avec leur nombre de journées ; extrêmes finaux hebdomadaires
  correspondants censurés.
- **Trous inter-jours** : mesurés et classés (dictionnaire F-E) ; les
  trous longs de réouverture de semaine sont attendus chaque semaine et
  ne constituent pas une anomalie de données.
- Tout écart de couverture par rapport à ces attentes suspend la synthèse
  jusqu'à explication écrite (patron des campagnes précédentes) : pas de
  publication partielle non étiquetée.

## 3. Estimation des coûts de calcul (livrable n° 8)

Sur la base des coûts constatés aux campagnes 3 et 4 (même corpus, même
machinerie) :

| Poste | Estimation | Fondement |
|---|---|---|
| Extraction CI (282 partitions, reconstruction M1, événements F-E/F-F) | ≈ 5–10 minutes de runner | Campagne 4 : extraction complète en ≈ 4 minutes ; campagne 5 ajoute les atteintes datées (calcul vectorisé par journée attendu du même ordre) |
| Validation temporelle (données synthétiques) | < 1 minute | Patron campagnes 3–4 |
| Synthèse locale (bootstrap 2 000 réplicats par famille) | ≈ 5–25 minutes | Campagne 3 : ≈ 1 minute (réplicas légers) ; campagne 4 : ≈ 19 minutes (recalcul complet par réplicat) ; campagne 5 se situe a priori entre les deux — les seuils causaux d'ouverture sont journaliers, les atteintes sont recalculées par réplicat de journées |
| Stockage des bruts | < 50 Mo compressés | Bruts gzip des campagnes 3–4 : 0,6–23 Mo par fichier |

## 4. Règles de suspension en cas de dépassement

1. Si un poste dépasse le budget CI (timeout du workflow, 350 minutes) ou
   rend la synthèse locale impraticable, **le calcul concerné est
   suspendu, documenté dans le document qualité avec le point d'arrêt
   exact, et les comparaisons non exécutées sont publiées comme telles**.
2. Aucune dégradation méthodologique de substitution n'est autorisée
   (ni réduction du nombre de réplicats, ni fenêtre élargie, ni famille
   réduite) sans nouvelle validation du propriétaire.
3. Les résultats partiels éventuellement produits avant suspension sont
   conservés, étiquetés partiels, et ne donnent lieu à aucune lecture.
4. L'extraction suit le patron éprouvé : job séquentiel unique, garde
   d'intégrité 282/282, commit unique des bruts gzip, journaux commités
   y compris en cas d'échec.
