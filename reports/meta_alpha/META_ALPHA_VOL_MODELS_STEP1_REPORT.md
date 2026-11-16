# META ALPHA — MODELES CONTINUS DE VOLATILITE, ETAPE 1 (IS, protocole valide)

Execution du protocole gele valide par le proprietaire (+ amendement
auto-valide consigne: construction d'une serie journaliere, les artefacts
existants ne contenant aucune serie de volatilite temporelle).
Serie: variance realisee journaliere tick (somme des r^2 mid), recombinee en
3097 jours calendaires 2010-2019 (run distant 43948461635, 14 min, apres un
echec de nom de script conserve: 43943944772). Modeles: GARCH(1,1) gaussien
et Student, FIGARCH (lib arch), ARFIMA(0,d,0) sur log-RV (d estime GPH par
bloc: valeurs dans VOL_MODELS_RESULTS.json), SV approximee AR(1) sur log-RV,
reference naïve constante. Perte unique QLIKE sur la variance du lendemain,
5 blocs chronologiques par entrainement expansif, previsions 1-pas.
Reproductibilite: ci_tools/daily_vol.py + ci_tools/fit_vol_models.py.

## Resultat: NON DEPARTAGE — sur les trois perimetres
Perte QLIKE moyenne (plus bas = meilleur) et gagnants de blocs:
- IS complet: ARFIMA -8.206 (meilleure moyenne), FIGARCH -8.382, SV -8.386,
  GARCH_T -8.466, GARCH_N -8.482, naïf -8.543. Gagnants de blocs: SV, GARCH_T,
  GARCH_T, ARFIMA (blocs 2-5) — aucun modele a 4/5.
- Ancien regime (avant 2012-10): ARFIMA -7.783 meilleure moyenne, gagnants
  ARFIMA/GARCH_T/SV — non departage.
- Regime recent (2012-10+): les six modeles tiennent en 0.23 de perte
  (ARFIMA -8.905, naïf -8.837, SV -8.690 dernier) — non departage, et ecarts
  faibles: la volatilite journaliere recente est presque aussi bien prevue
  par sa moyenne que par les modeles a memoire.
Conformement au critere gele (>=4/5 blocs ET meilleure moyenne), le verdict
est **NON DEPARTAGE** partout. C'est le resultat final de l'etape 1, pas un
echec a contourner: aucune re-parametrisation ne sera tentee.

## Lecture scientifique
La memoire de la volatilite est reelle (les modeles battent le naïf en
moyenne sur IS complet et l'ancien regime) mais sa forme (courte GARCH,
longue ARFIMA/FIGARCH, stochastique) n'est pas identifiable de maniere
stable a l'echelle journaliere sur cet echantillon: les gagnants tournent
selon les blocs et les perimetres. En regime recent, l'avantage des modeles
a memoire devient mince. Aucun modele discret n'a ete teste (interdit et
inutile ici): l'explication continue reste la reference, sans qu'une famille
continue particuliere puisse etre proclamee.

## Limites
RV journaliere tick sensible a la microstructure (bruit de mesure aux
changements de regime de cotation); ARFIMA d estime par GPH (approximation);
SV approximee par AR(1) sur log-RV (pas un filtre particulaire);
previsions FIGARCH/GARCH a parametres figes par origine de bloc.
Comparaisons par paires avec IC bootstrap par blocs: VOL_MODELS_RESULTS.json.

## Suite (gouvernance)
L'etape 2 du protocole (confirmation OOS) exige, par construction, un ordre
explicite du proprietaire: elle n'est PAS engagee. Point de reprise: decision
proprietaire sur l'ouverture eventuelle de l'etape 2, ou poursuite de la
cartographie IS sur d'autres dimensions.
