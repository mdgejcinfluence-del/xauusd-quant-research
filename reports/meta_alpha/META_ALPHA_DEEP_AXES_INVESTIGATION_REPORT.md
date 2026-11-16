# META ALPHA — INVESTIGATION APPROFONDIE AXES A/B/C (mission autonome)

Perimetre: 282 partitions IS lues a distance (run **43869516686, success,
1 h 59**, 0 Fcfa); OOS/Holdout jamais ouverts. Axe C par tiers calcule sans
relecture depuis les artefacts Global Discovery. Pre-enregistrement
DEEP_AXES_PREREG.json (chaine seq 14-15). Aucune hypothese testee, aucun test
de strategie: les "proxys" ci-dessous sont des mesures descriptives.

## Decouverte centrale (Axe A): la mecanique de cotation a change de nature
Composition des evenements de cotation (mediane annuelle des partitions):
mises a jour **bilaterales: 98,6% en 2010**, 92,7% (2011), 78,1% (2012),
54,0% (2013), 53,5% (2014), **27,3% (2015)**, puis 32-42% (2016-2019).
Les mises a jour unilaterales (bid-seul ou ask-seul) passent de ~1% a ~65%.
Transition progressive, sans rupture unique datee (sauts locaux 2010-2016,
dont part_000205, part_000213). C'est un fait natif des donnees: le processus
qui produit les cotations de 2010 n'est pas celui de 2019.
Consequences en chaine, toutes mesurees:
- l'autocorrelation tick mid (0,497 en T1 -> 0,034 en T3) appartient largement
  a l'ancien regime bilateral; elle n'est pas conditionnee par le spread
  (ac1 spread haut 0,483 vs bas 0,491);
- apres un evenement, le rendement suivant continue faiblement dans la
  direction de l'evenement (+0,07 bp unilateraux, +0,13 bp bilateraux,
  P(meme signe) 0,61-0,65), en decroissance nette entre tiers — amplitudes
  sans rapport avec le spread (~4 bp).
Qualification: **phenomene confirme descriptivement** (changement de mecanique
de cotation); impossible, avec des cotations seules, de separer "fournisseur
de flux" et "comportement de marche" — les deux lectures restent ouvertes,
mais dans les deux cas l'ac1 historique n'est pas un invariant exploitable.

## Axe B: la reversion a petite echelle est absorbee 20 fois par le spread
Proxy descriptif de reversion (moyenne de -sign(r_t)*r_{t+1} par barre, bp):
EVT10 0,193; TIME30 0,192; EVT50 0,091; TIME60 0,009. Spread median de la meme
partition: 3,99 bp. Ratio ~0,05; **0 partition sur 282** ou le proxy depasse le
spread, a toutes les echelles. De plus le proxy est concentre en T1
(0,21-0,24 bp) et ~0 en T2/T3: il appartient lui aussi a l'ancien regime.
**Resultat negatif robuste**: il n'y a pas, dans ces mesures, de reversion
economiquement significative a poursuivre; aucune strategie n'en est tiree.

## Axe C: la relation Bid/Ask a change de regime, sans jamais de leader
Profil croise par tiers: T1 domine par les decalages +/-1 evenement (0,538
contre 0,349 contemporain); T2/T3: contemporain dominant (0,564/0,588 contre
0,13-0,18 a +/-1), decalages >=2 evanescents. Coherent avec la composition:
ancien regime = jambes souvent decalees d'un pas; regime recent = unilaterales
frequentes mais contemporaines correlees. Dans les trois tiers, le profil
reste **symetrique**: aucune jambe ne precede l'autre. La relation bid/ask
n'est donc pas une loi stable, mais une propriete du regime de cotation.

## Cartographie mise a jour
- Granularites: la frontiere dependance/extinction (~100 evenements, ~60 s)
  decrit surtout l'ancien regime; en regime recent les dependances diriges
  sont deja faibles au tick.
- Phenomenes confirmes descriptivement: changement de mecanique de cotation
  (GD-06), persistance du spread, memoire continue de la volatilite.
- Refutes/absorbes: reversion petite echelle (spread), lead-lag directionnel,
  ac1 tick comme invariant.
- Regimes discrets: toujours aucun demontre; les "regimes" observes ici sont
  des regimes de **production de cotations**, pas des regimes de prix — et ils
  se succedent progressivement, ce qui plaide pour des dynamiques continues
  et des changements de flux plutot que pour des etats de marche discrets.

## Pistes prioritaires (par solidite)
1. Dater plus finement la transition de cotation (par mois) et la relier aux
   autres series (spread, intensite) — purement descriptif, artefacts a produire.
2. Tout phenomene futur doit etre rapporte **par regime de cotation** ou sur
   le seul regime recent, sous peine de melanger deux processus generateurs.
3. Les questions de volatilite continue (memoire, era-dependance) restent le
   front scientifique le plus solide; elles relvent d'un protocole gele de
   comparaison de modeles continus, a autoriser distinctement.

## Limites et reprise
Medianes de partitions (2010 sur-represente: 195 petites partitions);
composition mesuree sur changements de prix stricts; mid = construction;
tick != transaction. Livrables: DEEP_AXES_PARTITION.csv (282 lignes),
DEEP_AXES_SYNTHESIS.json, hashes au manifest. Point de reprise: decision du
proprietaire (piste 1 ou 3, ou cloture). Aucune suite engagee automatiquement.
