# AUDIT D'IMPACT — ÉTIQUETTES F3 POOLÉES DANS LES CAMPAGNES 0 À 3

**DESCRIPTIF — IS UNIQUEMENT — DOCUMENT CORRECTIF INDÉPENDANT (seq 198).**
Ce document ne modifie **aucune fiche historique originale** : il les annote
depuis l'extérieur, relié à la chaîne de preuves. Il fait suite au constat
de l'audit F3 (campagne 4, seq 196) : les prédictions HAR sont causales
(walk-forward, fenêtre roulante 500 jours, horizon 1 jour, prédiction du
jour j connaissable à la clôture de j−1), mais les étiquettes
BAS/MOYEN/HAUT utilisées jusqu'ici ont été calculées par terciles **poolés
sur l'ensemble des journées disposant d'une prédiction** (2 071 journées).
Pour une journée donnée, son étiquette dépend donc de la distribution de
prédictions de journées **postérieures** : l'étiquette n'était pas
connaissable à l'ouverture de la journée.

## 1. Preuve technique (uniforme dans tout le programme)

Chaque moteur de campagne contient le même motif, vérifié par inspection
du code versionné :

```python
f3 = pd.read_csv('F3_DAILY_PRED.csv').dropna(subset=['pred_har'])
q1, q2 = f3.pred_har.quantile([1/3, 2/3]).values      # <- poolé, tout l'échantillon
REG = {date: 'BAS' si pred_har <= q1, 'HAUT' si pred_har > q2, sinon 'MOYEN'}
```

Moteurs concernés : `campaign00_engine.py`, `campaign01_engine.py`,
`campaign011_engine.py`, `campaign022_engine.py`, `campaign03_engine.py`
(la campagne 2 consomme les bruts de la campagne 1 ; la campagne 2.1
consomme ceux des campagnes 1 et 1.1 ; la campagne 2.3 réutilise le moteur
2.2). Aucune exception n'a été trouvée : **toutes les colonnes « regime »
des campagnes 0 à 3 sont des étiquettes poolées rétrospectives.**

## 2. Ce que l'audit ne change pas

- Les **prédictions** `pred_har` jour par jour restent causales et leur
  usage comme variable continue historique n'est pas en cause.
- Les **mesures d'événements** (dépassements, cassures, impulsions,
  consolidations) et leurs issues ne dépendent pas des étiquettes F3 :
  elles sont inchangées.
- Tous les résultats conditionnés « par régime » restent **valides comme
  observations descriptives rétrospectives** : ils décrivent correctement
  comment les événements se sont répartis selon une segmentation a
  posteriori du niveau de volatilité *prévue* par un modèle causal. Les
  chiffres publiés restent exacts pour ce qu'ils mesurent.

## 3. Ce qui ne peut plus être interprété comme temps réel

- Toute lecture du type « en régime BAS/HAUT, il se passe X » **au sens
  d'une information disponible à l'ouverture de la journée ou à l'instant
  de l'événement** est retirée : l'appartenance d'une journée à un tercile
  poolé n'était pas connaissable à cet instant (elle peut changer si l'on
  ajoute des journées ultérieures à l'échantillon).
- Aucune fiche conditionnée par régime ne peut servir, en l'état, de
  conditionnement « à T0 » dans une étude ultérieure, ni alimenter le
  protocole de confirmation T0 (qui n'utilise d'ailleurs pas F3 : ses
  terciles portent sur la profondeur atteinte, seuils expanding-window —
  **non concerné par le présent audit**).
- L'ampleur numérique de l'instabilité des étiquettes (combien de journées
  changeraient de tercile en seuils causaux) n'est **pas quantifiée** ici :
  elle exige un recalcul, et le présent audit se refuse à la présumer
  faible ou forte.

## 4. Registre par campagne (détail : `F3_POOLED_LABELS_IMPACT_REGISTER.csv`)

| Campagne | Usages des étiquettes poolées | Fiches / conclusions touchées | Verdict de l'audit |
|---|---|---|---|
| 0 (seq 155) | Baselines d'atlas découpées par REGIME_BAS/MOYEN/HAUT | Aucune fiche (atlas descriptif) | Valide comme description rétrospective ; jamais une information temps réel |
| 1 (seq 158) | Colonne `regime` des événements ; comparaisons conditionnelles par régime (`CAMPAIGN_01_CONDITIONAL_COMPARISONS.csv`) | Aucune fiche ANO-C1 ne repose sur le régime (vérifié : le registre C1 ne contient aucune comparaison de régime) ; baselines par régime publiées | Valide rétrospectivement ; les écarts par régime sont des segmentations a posteriori |
| 1.1 (seq 160) | Idem (EV4, EV7, ouvertures de session) | Aucune fiche fondée sur le régime identifiée | Valide rétrospectivement |
| 2 (seq 165) | Tests T04, T07, T08, T12, T14, T16, T20 « régime BAS vs HAUT » | **4 fiches J1 fondées sur le régime : ANO-C2-003 (T07, retests), ANO-C2-006 (T12, retracement d'impulsions), ANO-C2-008 (T14, range post-consolidation), ANO-C2-012 (T20, ouvertures New York)** ; T04/T08/T16 sans fiche (négatifs ou non retenus, inchangés) | Fiches **conservées comme observations descriptives rétrospectives J1**, avec la présente annotation ; toute interprétation « condition connue au moment de l'événement » est retirée ; leurs mécanismes éventuels restent « inconnus » comme déjà écrit |
| 2.1 (seq 168) | Stratifications REGIME des analyses A/B ; tests de robustesse R06 (régime BAS seul) et R07 (régime HAUT seul) de l'ex-anomalie A | Conclusions 2.1 inchangées (l'anomalie A avait déjà été requalifiée rétrospective pour d'autres raisons) ; R06/R07 restent des contrôles de cohérence rétrospectifs | Valide rétrospectivement ; R06/R07 ne prouvent pas une disponibilité temps réel du conditionnement |
| 2.2 / 2.3 (seq 172/179) | Colonne `regime` des timelines d'instantanés ; aucune comparaison gelée de la relation T0 n'utilise le régime | **Conclusion principale T0 non touchée** (terciles de profondeur atteinte à T0, variables d'instantané closes, seuils historiques documentés) ; seules d'éventuelles lectures par régime des instantanés seraient concernées | Pas de recalcul requis pour la conclusion T0 ; les colonnes régime des bruts sont annotées rétrospectives par le présent document |
| 3 (seq 191) | Colonne `regime` des épisodes et instantanés ; comparaison gelée C3-04 (stagnation par régime) | C3-04 est un **négatif** publié : il le reste (un négatif rétrospectif ne devient pas un positif temps réel) ; ANO-C3-001/002/003 ne reposent pas sur le régime (session, amplitude causale, range de formation causal) | Candidates C3 inchangées ; C3-04 et les statistiques d'instantanés par régime = descriptions rétrospectives |

## 5. Recalculs : nécessaires, conditionnels, inutiles

- **Non requis** pour conserver l'ensemble des fiches et baselines comme
  observations descriptives rétrospectives J1 : tel est leur statut déjà
  revendiqué (aucune n'a jamais fondé de stratégie, de backtest ou de
  disponibilité temps réel dans une fiche — vérifié sur les registres,
  dont les limites écrivaient déjà « descriptif IS »).
- **Requis avant tout usage futur « à T0 »** d'un conditionnement par
  régime F3 : toute campagne qui voudrait conditionner un événement par le
  régime *connu à son instant* devra utiliser des terciles causaux (forme
  (a) du dictionnaire campagne 4 v2 : quantiles roulants sur 250 journées
  précédentes, minimum 60) et ne pourra pas importer les étiquettes
  poolées. Aucun tel usage n'existe à ce jour.
- **Conditionnel (à autoriser séparément, non exécuté ici)** : un recalcul
  de sensibilité des 4 fiches ANO-C2-003/006/008/012 sous étiquettes
  causales quantifierait la stabilité des écarts publiés. La campagne 4,
  si elle est exécutée, produira les étiquettes causales journée par
  journée ; un tel contrôle pourra alors être proposé au propriétaire
  comme comparaison préenregistrée distincte — il n'est ni inclus ni
  promis dans la présente livraison.

## 6. Formulation corrective faisant foi à compter de ce jour

Dans tout le catalogue META ALPHA, « régime BAS/MOYEN/HAUT (F3) » des
campagnes 0 à 3 se lit : **« segmentation rétrospective par terciles
poolés du niveau de volatilité prévue par le modèle causal F3 »**. Cette
lecture se substitue à toute interprétation temps réel antérieure, sans
modifier les fiches originales, qui restent le témoignage figé de leur
époque du programme.
