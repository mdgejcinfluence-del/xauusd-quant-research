# CAMPAGNE 2.3 (REPRISE) — MATRICE DE COUVERTURE CORRIGÉE

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Cette matrice
remplace, pour la couverture temporelle de la reconstruction 2.2, les
formulations antérieures (« 2010–2014 », « 2014–2017 partielle »), qui étaient
inexactes : l'extraction partielle n'est ni continue ni complète par année.

## Couverture exacte de la reconstruction 2.2 (épisodes T0, par année)

| Année | Épisodes | Journées | Dates couvertes | Trous documentés |
|---|---|---|---|---|
| 2010 | 4 075 | 254 | 2010-01-04 → 2010-12-31 | Aucun trou mensuel détecté |
| 2011 | 4 004 | 256 | 2011-01-03 → 2011-12-30 | Aucun trou mensuel détecté |
| 2012 | 2 831 | 174 | 2012-01-03 → 2012-12-31 | **Septembre, octobre, novembre absents** (et août partiel : 328 épisodes) |
| 2013 | 603 | 45 | 2013-01-02 → 2013-12-31 | **Seuls janvier, novembre, décembre présents** |
| 2014 | 631 | 48 | **2014-01-02 → 2014-03-11** | Tout après le 2014-03-11 absent |

**Formulation corrigée qui fait foi** : la reconstruction couvre des fragments
de 2010 à mars 2014 (777 journées au total), pas « la période 2010–2014 ». En
particulier, « 2014–2017 » n'est en **aucun sens** une période partiellement
couverte : seuls 48 jours de janvier–mars 2014 le sont, et rien de 2015, 2016 ou
2017.

## Matrice par période (état après reprise seq 176)

| Période IS | Reconstruction 2.2 | État |
|---|---|---|
| 2010–2011 | Couvertes (510 journées) | Référence reproduite (seq 175) |
| 2012 | Partielle (174 journées, trous sep.–nov.) | À compléter lors de la reprise |
| 2013 | Très partielle (45 journées) | À compléter |
| 2014-01-02 → 2014-03-11 | Couverte (48 journées) | Fragment de cohérence (seq 175) |
| 2014-03-12 → 2016 | **Non couverte** | Manquante |
| 2017–2020 (priorité propriétaire) | **Non couverte** | Manquante — partitions inventoriées, accès bloqué (diagnostic joint) |
| 2020–2026 | Hors périmètre IS autorisé | Non sollicitée (autres périmètres scellés) |

## Contrôle final (points livrables de la décision)

- **Statistiques par époque, effectifs, grappes, intervalles** :
  `CAMPAIGN_02_3_TEMPORAL_REPLICATION.csv` (inchangé par la reprise : ère
  2010–13 +13,6 pts [11,9 ; 15,3] ; fragment 2014 +13,7 [5,8 ; 21,5] ; 2017–20 :
  NON MESURÉ). Les résultats historiques partiels restent conservés séparément
  des futurs résultats étendus, comme exigé.
- **Journal de qualité** : `CAMPAIGN_02_3_DATA_QUALITY.md` + journaux de sonde
  commités (`ACCESS_PROBE.txt`, `timeline_parts/*_log.txt`).
- **Reproductibilité** : la procédure gelée (seq 170) et le moteur par lots sont
  commités et inchangés ; la reprise, dès l'accès rétabli, consistera à relancer
  la sonde puis la matrice, sans toucher aux définitions, seuils ou paramètres.
- **Blocage** : documenté dans `CAMPAIGN_02_3_ACCESS_DIAGNOSTIC.md` (403
  `datasets.get denied` après régénération des identifiants sur `marioadh` ;
  cause la plus vraisemblable : datasets privés du compte `shalom5123`).

**STATUT : BLOCAGE D'ACCÈS DOCUMENTÉ — reprise historique en attente de la
correction du compte propriétaire des datasets (action propriétaire unique,
sans rotation répétée).**
