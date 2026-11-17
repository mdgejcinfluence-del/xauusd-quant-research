# META ALPHA — VOLATILITE HORAIRE: DEPARTAGE DES FAMILLES + COUPLAGE SPREAD

Extension horaire (auto-validee, consignee seq 39-40) du protocole volatilite
gele. Serie horaire calendaire construite via Kaggle (run 44190381343,
2 min 35, 282/282 apres un echec de nom de script conserve): 60 026 lignes
partition-heure recombinees en serie horaire UTC (RV tick, rendement horaire,
spread). Desaisonnalisation par heure du jour apprise sur l'entrainement seul.
Memes familles, meme perte QLIKE, memes criteres qu'a l'etape journaliere.
Reproductibilite: ci_tools/hourly_series.py + ci_tools/fit_vol_hourly.py.

## Verdict: NON DEPARTAGE (a nouveau, et c'est le resultat)
Perte QLIKE moyenne / blocs gagnes (sur 4 blocs evalues):
- IS complet: FIGARCH -11.673 (meilleure moyenne, 1 bloc), ARFIMA -11.427
  (2 blocs, mais un bloc catastrophique a -9.985), SV -11.375 (1 bloc),
  GARCH_N -11.544, naïf -11.500, GARCH_T -11.357.
- Regime recent: FIGARCH -11.947 (meilleure moyenne, 0 bloc), ARFIMA -11.903
  (3 blocs sur 4 — le plus proche du critere, sans l'atteindre), naïf -11.791.
Aucun modele ne satisfait le double critere gele (meilleure moyenne ET
>=4/5 blocs). Apres deux echelles (journaliere puis horaire) et trois
perimetres, la forme de la memoire de volatilite (courte, longue ou
stochastique) n'est pas identifiable de maniere stable sur l'IS. Le parametre
de memoire longue estime reste remarquablement stable (d ARFIMA 0.25-0.34
selon blocs/perimetres): la memoire est intermediaire-longue, sans qu'une
famille la capture suffisamment mieux que les autres pour etre proclamee.
Aucune re-parametrisation ne sera tentee pour forcer un departage.

## Couplage volatilite / cycle de spread (descriptif)
- Correlation contemporaine log-RV horaire / spread horaire: -0.164 au global
  (ancien regime -0.046; recent -0.293). Lecture prudente: les heures actives
  combinent volatilite elevee et spread etroit (cycle diurne commun), sans
  causalite etablie; le renforcement recent est un fait a consigner.
- Profil decale asymetrique: correlations +0.10 a +0.15 quand la volatilite
  precede le spread de 3 a 5 heures, ~+0.05-0.07 dans l'autre sens. Compatible
  avec un elargissement differe du spread apres les heures agitees; confondu
  potentiel par le cycle diurne (les heures agitees precedent mecaniquement
  les heures creuses a spread large). Aucune regle ni hypothese n'en est tiree.

## Qualification et suite
Memoire de volatilite: phenomene confirme descriptivement, famille NON
identifiee (deux echelles concordantes). C'est une conclusion de la
cartographie, pas un chantier a rouvrir sans donnee nouvelle. Etape 2 OOS
toujours fermee (ordre explicite requis). Aucun edge n'est proclame.
