# PHASE 11-C — RAPPORT D'ANATOMIE DES GRANDS MOUVEMENTS H1/H4

**Statut : étude descriptive et mécanistique sur corpus IS 2010–2020
(jamais une preuve de rentabilité, de prévisibilité exploitable ou
d'alpha). Protocole PHASE 11-A gelé définitivement (seq300, sha256
`fdfb04ed…`), autorisation et préflight seq305, audit des manifestes
11-B (seq302) et reconstruction des identifiants 11-B.1 (seq304).
Exécution : run CI 45017167617 vert (voir
`PHASE11C_INCIDENT_AND_RECOVERY.md` pour l'incident et sa reprise).**

Méthode : populations fermées F10-01 (3 107 admissibles, 2 617
grappes) et F10-03 (660 admissibles, 597 grappes), identifiants
`event_id`/`grappe_id` de la carte 11-B.1 (étiquettes déterministes
des composantes historiques reproduites, non des identifiants
originaux). Pour chaque événement : t0 = clôture de la bougie
déclencheuse, P0 = Mid de clôture, direction d fixée à t0 ;
trajectoires Mid reconstruites depuis les barres M1 (8 lots, corpus
IS uniquement, holdout jamais accédé) ; horizons t+1…t+8 (8 h en H1,
32 h en H4) ; MFE/MAE cumulées depuis P0, déplacements de clôture,
repli depuis l'extrême favorable (distinct du MAE), touche et
réintégration confirmée de P0, reprises, archétypes gelés, sessions
UTC fixes. Aucun coût, aucune rentabilité, aucune p-value ; bootstrap
par grappes descriptif (2 000 répétitions, graine 20261122).

## Résultats H1 (F10-01, n = 3 107 ; trajectoires complètes 3 104)

Évolution médiane (événements) : le MFE cumulé croît de 14,3 bp à t+1
à **32,9 bp à t+8** (P25 13,9 ; P75 62,9 ; P90 109,6), le MAE cumulé
de 14,7 à **31,5 bp** (P90 96,9) ; le déplacement de clôture médian
reste légèrement négatif à tous les horizons (−1,9 bp à t+1, **−2,2 bp
à t+8** ; IC95 grappe [−4,1 ; −0,2]). L'extension médiane et le recul
médian sont donc du même ordre : la bougie médiane finit à peu près
à son point de départ. À poids égal par grappe, conclusions
identiques (MFE t+8 médiane des médianes 32,6 bp ; déplacement
−4,2 bp). Proportions de nouveaux MFE par étape : 35,8 % à t+2,
décroissantes jusqu'à ~10–17 % en fin de fenêtre.

Repli et réintégration : un repli sur clôtures est présent dans
**94,8 %** des événements ; la profondeur maximale du repli depuis
l'extrême favorable atteint en médiane **58,7 bp**, soit une fraction
médiane de **0,90 du corps de la bougie déclencheuse** reprise
(non plafonnée). La touche de P0 survient dans **98,8 %** des cas ;
la **réintégration confirmée dans 86,7 %**, dont **73,1 % de retours
immédiats** (première bougie). Après réintégration, une reprise
(dépassement en clôture de l'ancien meilleur niveau favorable)
intervient dans **75,4 %** des cas réintégrés.

Archétypes H1 (dénominateur 3 107) : REINTEGRATION_PUIS_REPRISE
**65,4 %** (2 032) ; FAUX_DEPART_REINTEGRE_SANS_REPRISE 21,2 % (660) ;
REPLI_PUIS_CONTINUATION 8,0 % (248) ; AUCUNE_EXTENSION_CONFIRMEE
5,2 % (162) ; REPLI_SANS_REPRISE 0,06 % (2) ;
CONTINUATION_SANS_REPLI_CONFIRME **0 %** ; CENSURE 3 (0,1 %) ;
aucun cas AMBIGU_INTRA_MINUTE.

## Résultats H4 (F10-03, n = 660 ; complètes 657)

Le MFE cumulé médian croît jusqu'à **65,2 bp à t+8** (P75 126,3 ;
P90 209,1), le MAE à **62,9 bp** ; déplacement de clôture médian
**−4,6 bp** (IC95 grappe [−10,6 ; +1,8], incluant zéro). Repli présent
dans **98,2 %** ; profondeur médiane du repli **113,9 bp**, fraction
médiane du corps reprise **0,82**. Touche de P0 : 99,7 % ;
**réintégration confirmée : 95,8 %**, retours immédiats 85,2 % ;
reprise après réintégration : **85,8 %** des réintégrés.

Archétypes H4 (dénominateur 660) : REINTEGRATION_PUIS_REPRISE
**81,7 %** (539) ; FAUX_DEPART_REINTEGRE_SANS_REPRISE 13,6 % (90) ;
REPLI_PUIS_CONTINUATION 2,4 % (16) ; AUCUNE_EXTENSION_CONFIRMEE
1,8 % (12) ; CONTINUATION_SANS_REPLI_CONFIRME 0 % ; CENSURE 3.

## Sessions UTC (déclenchement ; descriptif, sans classement de rentabilité)

En H1, les impulsions déclenchées en LONDON (n = 474) montrent les
excursions médianes les plus amples (MFE t+8 44,9 bp) et la part de
réintégration la plus élevée (93,2 %) ; NIGHT_OTHER (n = 46, faible
effectif) les plus faibles (MFE 11,0 bp). LONDON_NY_OVERLAP concentre
1 617 des 3 107 événements H1. En H4, ASIA (n = 42) affiche les plus
grandes excursions (MFE 119,2 bp) sur un effectif très réduit —
aucune sélection d'heures n'est effectuée et les cinq catégories
sont publiées intégralement (`PHASE11C_SESSION_ANATOMY.csv`,
sessions de réalisation incluses).

## Chevauchements H1/H4 (descriptif, aucune causalité)

1 514 des 3 107 événements H1 (48,7 %) ont leur t0 dans un épisode
H4 (bougie déclencheuse H4 + fenêtre d'observation de 32 h). Aucune
fusion des populations, aucune attribution causale.

## Couverture et censures

Effectifs par horizon quasi constants : H1 3 107 → 3 104, H4 660 →
657 entre t+1 et t+8 ; **3 censures LACUNE_ANORMALE par population**,
aucune censure de fin de couverture, aucune ambiguïté intraminute
détectée. Les fermetures régulières et week-ends sont traversés sans
être traités comme des défauts (temps calendaire et temps de marché
enregistrés par événement dans `PHASE11C_EVENT_PATHS.csv`).

## Réponses à la règle de conclusion

1. H1 : extension médiane croissante jusqu'à ~33 bp en 8 h, mais
   clôture médiane finale à −2,2 bp de P0 : le mouvement médian
   s'étend puis revient.
2. H4 : même anatomie à plus grande échelle (~65 bp d'extension
   médiane en 32 h, clôture médiane −4,6 bp).
3. Le repli est du même ordre que l'extension (profondeur médiane
   59 bp H1 / 114 bp H4 ; ~0,8–0,9 du corps initial repris).
4. Réintégration confirmée de P0 : 86,7 % (H1) et 95,8 % (H4) —
   le retour au niveau de départ est le comportement dominant.
5. Reprise après réintégration : 75,4 % (H1) et 85,8 % (H4) des
   événements réintégrés.
6. Continuation sans repli confirmé : **0 %** dans les deux
   populations — tout événement étendu connaît un repli sur
   clôtures ou une réintégration.
7. Sessions : amplitudes descriptivement plus fortes pour les
   déclenchements LONDON (H1) ; effectifs très inégaux, aucune
   conclusion de session « favorable » n'est tirée.
8. Événements vs grappes : distributions quasi identiques (les
   grappes sont petites : max 7 événements en H1, 4 en H4), les
   conclusions ne dépendent pas de la pondération.
9. Censures marginales (3 + 3) : elles ne limitent aucune
   conclusion ; la limite principale reste la résolution M1
   (aucun ordre intraminute) et le caractère rétrospectif IS.
10. Comportement dominant : **extension ample, repli profond,
    retour fréquent à P0, puis reprise fréquente** — une anatomie
    d'oscillation autour du niveau de départ, non une continuation
    directionnelle. Ces régularités descriptives ne constituent ni
    une preuve de prévisibilité exploitable ni une opportunité de
    trading (la Phase 10 a déjà établi l'espérance nette négative
    de l'entrée immédiate).

Livrables : `PHASE11C_EVENT_PATHS.csv` (3 767 événements admissibles),
`PHASE11C_HORIZON_METRICS.csv`, `PHASE11C_ARCHETYPES.csv`,
`PHASE11C_SESSION_ANATOMY.csv`, `PHASE11C_COVERAGE_CENSORING.csv`,
`PHASE11C_RESULTS.json`. La Phase 11-C est la dernière étape
descriptive autorisée ; toute phase ultérieure exige une décision
distincte.
