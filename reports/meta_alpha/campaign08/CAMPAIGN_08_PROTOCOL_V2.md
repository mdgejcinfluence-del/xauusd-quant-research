# CAMPAGNE 8 — PROTOCOLE CONSOLIDÉ F-J V2 « CHOCS MINUTE EXTRÊMES ET LEUR SILLAGE »

**Statut : CONSOLIDATION FINALE SOUMISE — NON GELÉE, AUCUN CALCUL.**
Le présent V2 consolide et remplace, comme texte unique soumis au gel,
le protocole V1 (seq260) et son addendum V1.1 (seq262), en y intégrant
les trois verrouillages du fondateur (seq263). Les paramètres déjà
validés ne sont pas rouverts. XAU/USD, corpus IS uniquement ; holdout
scellé ; aucun backtest ni `challenge_sim` ; aucun J2/J3 automatique ;
aucun budget expérimental consommé ; FRED suspendue ; 36 cellules S12
gelées ; T0 séparé et inactif ; aucune fiche historique modifiée ;
F-G et F-I définitivement clôturées ; F-H et F-L en réserve.

## 1. Objet

Anatomie événementielle des variations M1 exceptionnellement
importantes : fréquence, intensité, direction (haussière et baissière
séparément), regroupement temporel, sillage (continuation, retour
partiel, retournement, stabilisation, nouveau choc), contextes
historiques et intrajournaliers. Aucun présupposé prédictif ou
exploitable ; toute candidate éventuelle serait J1 sans promotion.

## 2. Données et dictionnaire mathématique

Corpus IS constitué : 282 partitions, 3 540 993 barres M1, 3 097
journées présentes. Horodatage = début de barre ; la clôture c_t d'une
barre est disponible à la fin de sa minute. Un **segment** est une
suite de barres consécutives espacées d'exactement 1 minute.

- Variation minute : **r_t = ln(c_t / c_{t−1}) × 10⁴ (bp)**, définie
  uniquement si la barre précédente appartient au même segment. Aucune
  variation n'est calculée à travers un trou ou une reprise.
- Jour d'attribution : journée UTC de la barre. Ères : 2010–2013,
  2014–2016, 2017–2020.
- Sessions UTC : **S1 00:00–06:59, S2 07:00–12:59, S3 13:00–20:59,
  S4 21:00–23:59** (début de session : 00:00, 07:00, 13:00, 21:00).

## 3. Détection causale des chocs

- Fenêtre de référence du jour D : variations valides des **20
  journées présentes précédentes** (toutes celles disponibles si leur
  nombre est entre 10 et 19).
- **T_D = max(10 bp, Q₉₉,₅(|r| sur la fenêtre)**, Q₉₉,₅ = quantile à
  99,5 % par interpolation linéaire (type 7). T_D est fixé avant
  l'ouverture de D et constant pendant D.
- Éligibilité : D est éligible si **≥ 10 journées antérieures valides**
  et **≥ 10 000 variations valides** dans la fenêtre ; sinon journée
  **INÉLIGIBLE_DÉTECTION** publiée, sans aucun seuil substitué.
- Prédicat strict : **choc ⇔ |r_t| > T_D**. Signe + si r_t > 0,
  − si r_t < 0. Disponibilité du choc : clôture de sa barre.
- Intensité du choc : ρ_t = |r_t| / T_{D(t)}.
- Aucun quantile poolé rétrospectif ne sert à la détection ; toute
  référence poolée serait publiée séparément comme non causale.

## 4. Épisodes, clôture verrouillée, disponibilité

- **Regroupement** : chocs consécutifs (horodatages de début de barre)
  espacés de **≤ 15 minutes (inclusif)** = même épisode ; écart
  > 15 minutes = nouvel épisode. Un épisode peut traverser minuit ;
  son jour d'attribution est celui de son **premier choc**. Chocs
  observés seulement : un trou peut masquer un choc, et rien dans le
  protocole ne prétend le contraire (voir clôture).
- **Clôture — verrouillage 1** : un épisode de dernier choc t_der n'est
  **définitivement clos** que si les **quinze minutes de silence sont
  intégralement observées** : les barres débutant à t_der+1, …,
  t_der+15 existent **toutes**, sont consécutives, et aucune n'est un
  choc. Son heure de disponibilité définitive est alors publiée :
  **t_der + 16 minutes** (clôture de la barre t_der+15).
  Si **une seule minute manque** dans cette fenêtre, ou si la série
  s'interrompt avant son terme :
  - clôture **INDÉTERMINÉE** ;
  - épisode publié comme **censuré (CLÔTURE_INDÉTERMINÉE)** ;
  - **aucune heure de disponibilité définitive** ne lui est attribuée ;
  - il est **exclu de toutes les comparaisons FJ-01…FJ-05** et de tout
    sillage ; ses descripteurs observés (chocs vus, amplitude) restent
    publiés à titre descriptif étiqueté incomplet.
  Aucun choc potentiellement masqué par un trou n'est assimilé à une
  absence de choc.
- **Classes de signe** : POSITIF (tous +), NÉGATIF (tous −), MIXTE
  (les deux). Les MIXTES sont publiés séparément et exclus des
  comparaisons directionnelles primaires.
- **Isolé** : 1 choc ; **regroupé** : ≥ 2 chocs. Descripteurs publiés :
  premier/dernier choc, disponibilité définitive (si close), nombre de
  chocs, amplitude A = max |r_t|, durée, session et position du premier
  choc (§6), jour d'attribution, ère.
- **Intensité primaire de l'épisode** (FJ-03 et descripteurs) :
  **I_ép = max_t (|r_t| / T_{D(t)})**, chaque choc rapporté au seuil de
  son propre jour. Classes : **MODÉRÉ** 1 < I_ép < 2 ; **MAJEUR**
  I_ép ≥ 2. Amplitude en bp, somme des |r|, nombre de chocs et durée :
  descriptifs seulement.
- **Unité statistique primaire : l'épisode clos non MIXTE.** Les chocs
  intra-épisode ne sont jamais des observations indépendantes.

## 5. Sillage (rétrospectif par construction)

Ancrage : **c₀ = c(t_der)**, clôture de la dernière barre de choc,
disponible à t_der + 1.

- **Continuation signée — formule unique** :
  **R_h = s × ln( c(t_der + h) / c(t_der) ) × 10⁴ (bp)**, s = signe de
  l'épisode (pour un pseudo-événement, signe de sa variation propre) ;
  prix final c(t_der + h) = clôture de la barre débutant à t_der + h,
  disponible à t_der + h + 1. Horizons descriptifs +15, +30 ;
  **horizon principal +60**.
- **Censure de fenêtre** : R_h exige l'existence de la barre
  t_der + h et **aucun trou > 15 minutes** sur (t_der, t_der + h] ;
  sinon **CENSURE_FENÊTRE** à cet horizon, taux publiés par bras.
- **Retour partiel** : max(0, −R₆₀) / A. **Retournement** : R₆₀ < −A.
  **Excursions** favorable/défavorable à 60 min (barres haut/bas,
  signées par s, bp depuis c₀). **Stabilisation** : (Σ |r| des
  60 minutes suivant l'ancrage) / (Σ |r| des 60 minutes précédant le
  premier choc, choc exclu), chaque somme exigeant son segment complet.
  **Nouveau choc** : premier choc d'un épisode ultérieur dans
  (t_der, t_der + 60]. Tout ordre dépendant d'un parcours inobservé
  est **indéterminé** et censuré.
- Le sillage tout entier est une mesure **rétrospective de l'épisode
  clos** ; aucune disponibilité en temps réel n'est revendiquée, ni
  pour l'épisode (connu à t_der + 16 au plus tôt), ni pour R₆₀
  (t_der + 61).

## 6. Pseudo-événements (FJ-05) — verrouillage 2

- **Activité antérieure** : **A_avant(x) = Σ_{k=1..60} |r_{x−k}|**
  (60 minutes précédant x, x exclue), exigeant 60 barres consécutives
  segment-complètes ; même définition pour les épisodes (x = premier
  choc) et les pseudo-événements.
- **Position dans la session** : **pos(x) = minutes écoulées depuis le
  début de la session de x** jusqu'à x (x = premier choc pour un
  épisode, minute retenue pour un pseudo-événement). La position du
  premier choc de chaque épisode est publiée.
- **Bassin de sélection** : pour éviter le biais de position de la
  « première minute du jour », le bassin retient, pour chaque journée
  éligible, chaque session et chaque **bloc de 60 minutes compté depuis
  le début de la session**, la **première minute éligible m** du bloc :
  r_m défini et ≠ 0 ; m n'est pas un choc ; **aucun choc dans les
  60 minutes précédant m** ; A_avant(m) calculable. Au plus un
  pseudo-événement par (journée, session, bloc). **Signe du
  pseudo-événement = signe de r_m.** Aucune propriété du sillage futur
  de m n'intervient ni dans la sélection ni dans aucune exclusion :
  un choc ultérieur dans son sillage est publié (drapeau NOUVEAU_CHOC),
  jamais un motif de retrait.
- **Terciles d'activité** : terciles de A_avant au sein de chaque
  session, sur l'union du bassin et des épisodes isolés de la session.
- **Appariement sans remplacement, temporellement contrôlé** : les
  épisodes isolés non MIXTES clos sont traités par ordre chronologique
  de premier choc. Pour chacun, candidats = pseudo-événements **encore
  inutilisés** de **même session, même signe, même tercile
  d'A_avant** ; le partenaire retenu **minimise |pos(pseudo) −
  pos(épisode)|**, départage déterministe par le plus petit horodatage
  (journée, minute) en cas d'égalité. Si la distance de position
  minimale dépasse **60 minutes**, ou si aucun candidat de la strate
  n'existe, l'épisode est déclaré **non apparié** (publié) : aucune
  strate n'est élargie, aucun pseudo-événement n'est réutilisé.
- **Absence de contrôle comparable** : épisodes non appariés comptés et
  publiés avec leur motif ; si les seuils d'éligibilité (§8) ne sont
  pas atteints sur les paires, FJ-05 est **NON_EVALUABLE**, sans
  assouplissement.
- **Contrôle de composition** : effectifs croisés ère × session des
  deux bras appariés publiés ; drapeau **COMPOSITION_SENSIBLE** si une
  ère < 10 % des paires ou si l'écart de part d'ère entre bras
  > 10 points (conséquences au §8). Aucun de ces contrôles ne crée de
  p-value.

## 7. Graphe de dépendance — verrouillage 3

- **Nœuds** : tous les épisodes clos utilisés par une comparaison, et,
  pour FJ-05, **les pseudo-événements appariés et leurs sillages sont
  des nœuds au même titre**, reliés en outre à leur épisode apparié
  par une arête d'appariement.
- **Arêtes** entre deux nœuds si : même jour d'attribution (pour un
  pseudo-événement, son propre jour) ; fenêtres de sillage
  [ancrage, ancrage + 60] qui se chevauchent ; sillage de l'un
  contenant un choc (ou le point d'ancrage) de l'autre ; traversée
  d'une frontière journalière par l'un de ces liens — la frontière UTC
  ne coupe **aucune** arête.
- **Grappe statistique** : composante connexe de ce graphe (fermeture
  transitive). **Unité de bootstrap : la grappe**, pour les cinq
  comparaisons. Justification : la dépendance entre sillages naît du
  futur observé partagé, des chocs ultérieurs communs et du contexte
  de journée ; la composante connexe est la plus petite unité qui les
  contient tous, y compris à cheval sur deux journées.
- **Diagnostics publiés avant lecture** : nombre de grappes, tailles
  (nœuds par grappe), part des sillages chevauchants, traversées de
  minuit, fusions inter-journalières, plus grande grappe par bras.
- **GRAPPE_DOMINANTE — conséquences fixées à l'avance**, si la plus
  grande grappe dépasse **5 % des unités d'un bras** :
  1. **Publication descriptive** : intégralement maintenue (effectifs,
     médianes, distributions) — le statut ne retire rien au descriptif.
  2. **Validité de l'inférence** : la comparaison est étiquetée
     **INFÉRENCE_FRAGILE** ; p, q et intervalles restent publiés à
     titre indicatif, mais la lecture inférentielle est plafonnée.
  3. **Autorisation de candidature** : **aucune lecture CANDIDATE_J1**
     n'est possible sous GRAPPE_DOMINANTE ; la lecture maximale est
     SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL.
  Ces contrôles ne créent **aucune p-value supplémentaire**.

## 8. Cinq comparaisons fermées, méthode, censure

Variable principale : **R₆₀**. Matérialité : **10 bp** (différence de
médianes). Bootstrap par grappes (§7), 2 000 réplicats, graine publiée
au gel ; IC percentile 95 %, p bilatérales. **BY à m = 5 fixe**
(H₅ = 2,283333) ; p NaN ⇒ STRUCTURELLEMENT_NON_EVALUABLE (aucune
imputation, facteur 5 conservé). Éligibilité par bras : **≥ 200
épisodes et ≥ 100 grappes**, sinon NON_ELIGIBLE. Lectures :
CANDIDATE_J1 / SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL / NÉGATIF /
NON_ELIGIBLE / NON_EVALUABLE / STRUCTURELLEMENT_NON_EVALUABLE —
CANDIDATE_J1 interdite sous COMPOSITION_SENSIBLE (FJ-05) ou
GRAPPE_DOMINANTE. Populations : épisodes **clos** (§4) uniquement ;
censures CLÔTURE_INDÉTERMINÉE et CENSURE_FENÊTRE exclues des bras,
taux publiés.

| ID | Hypothèse | Populations (clos, non MIXTES) |
|---|---|---|
| FJ-01 | Le sillage diffère selon le signe | isolés POSITIFS vs isolés NÉGATIFS |
| FJ-02 | Le sillage diffère selon le regroupement | regroupés vs isolés |
| FJ-03 | Le sillage dépend de l'intensité primaire I_ép | isolés MAJEURS vs isolés MODÉRÉS |
| FJ-04 | Le sillage a évolué entre ères | isolés 2010–2013 vs 2017–2020 (2014–2016 publiée hors test) |
| FJ-05 | Le sillage après un choc diffère de celui de minutes non extrêmes comparables | isolés appariés vs pseudo-événements (§6) |

Ventilation fermée publiée sans test : par session S1–S4 de chaque
bras ; fréquences de chocs par ère/session/signe ; distributions de
I_ép et des amplitudes ; parts retracées ; retournements ; taux de
nouveau choc ; stabilisation ; distributions des distances de position
des appariements FJ-05. Négatifs, non-éligibles et non-évaluables
publiés.

## 9. Couverture, biais, coût, nouveauté

Couverture : journées présentes par ère C6 — 2010–2013 : 1 245 ;
2014–2016 : 932 ; 2017–2020 : 920 ; amorçage causal inéligible en tout
début de corpus (publié). Registre des biais D1–D12 (dossiers
préparatoires) complété par : **D13** clôture indéterminée par trou
(verrouillage 1 : censurée, jamais de silence fabriqué) ; **D14** biais
de position en session des pseudo-événements (verrouillage 2 : bassin
par blocs de 60 minutes et appariement sur la distance de position) ;
**D15** dépendances pseudo-événements et inter-journalières
(verrouillage 3 : graphe unique, composantes connexes). Coût attendu :
un run CI sur le corpus existant, synthèse locale, 0 FCFA ; suspension
documentée en cas d'échec ou de dépassement, sans dégradation (ni
fenêtre raccourcie, ni seuil assoupli, ni population réduite).
Nouveauté : première famille à événement-variation daté causalement —
ni niveau (0–2, 5, 7), ni état (4), ni extension (3), ni ouverture (5),
ni forme de journée (6) ; aucun modèle ni prévision (contrairement à
F3/F7, gelés en service) ; aucune fiche C3/C4/C5 touchée.

## 10. Les dix constantes

| # | Constante | Valeur | Justification |
|---|---|---|---|
| 1 | Fenêtre causale | 20 journées précédentes | ≈ un mois : quantile 99,5 % estimable, microstructure récente |
| 2 | Quantile et prédicat | Q₉₉,₅ linéaire ; \|r_t\| > T_D strict | queue extrême ≈0,5 % ; méthode et prédicat figés |
| 3 | Plancher | 10 bp, T_D = max(10, Q₉₉,₅) | pas d'« extrême » trivial en période morte |
| 4 | Amorçage | ≥10 journées et ≥10 000 variations | en deçà, inéligibilité publiée plutôt que seuil rétroactif |
| 5 | Intensité primaire | I_ép = max \|r_t\|/T_{D(t)} ; classes à 2 | mesure unique FJ-03, invariante d'échelle causale |
| 6 | Regroupement / clôture | ≤ 15 min inclusif ; silence intégralement observé | sépare impulsion et séquence ; clôture jamais fabriquée (D13) |
| 7 | Horizons | +15/+30 descriptifs ; +60 principal | une heure pour départager continuation et retour |
| 8 | Matérialité | 10 bp sur R₆₀ | ordre du plancher de détection |
| 9 | Pseudo-événements | bassin par (jour × session × bloc 60 min) ; appariement session × signe × tercile, distance de position ≤ 60 min, sans remplacement | déterminisme, comparabilité temporelle, pas de biais de début de session (D14) |
| 10 | MIXTES | publiés séparément, exclus des primaires | signe net indéfini sans classement arbitraire |

Constantes de méthode : bootstrap grappes 2 000 réplicats, BY m = 5,
éligibilité ≥ 200 épisodes et ≥ 100 grappes par bras, GRAPPE_DOMINANTE
à 5 %.
