# PROTOCOLE GELE (PROPOSITION A VALIDER) — COMPARAISON DE MODELES CONTINUS DE VOLATILITE

Statut: PROPOSE, NON EXECUTE. Toute execution exige la validation explicite du
proprietaire (gouvernance des tests), l'inscription a la chaine et le
verrouillage par hash de ce document. Aucun acces OOS/Holdout n'est demande
a ce stade: l'etape 1 est IS-exploratoire (statut maximal: decouverte candidate).

## Question scientifique
La memoire de la volatilite XAUUSD (ac|r| tick 0.457/0.184/0.132, era-dependante,
ac|r| par tiers 0.472/0.184/0.158) est-elle mieux decrite par (a) un GARCH a
memoire courte, (b) une memoire longue (FIGARCH/ARFIMA), (c) une volatilite
stochastique continue, ou (d) leur combinaison avec le regime de cotation
comme covariable de mesure? Aucun modele discret n'est candidat.

## Donnees et series (a construire si valide, IS uniquement)
Barres EVT100 deja construites (artefacts Phase 1R): volatilite realisee de
barre et |rendement| agrege par partition; serie mensuelle de reference.
Deux perimetres separes, jamais melanges sans mention: (i) IS complet,
(ii) regime de cotation recent seul (bilateraux < 50%, depuis 2012-10),
(iii) ancien regime seul. Republications exactes (GD-07) flaguees/exclues
dans une variante de robustesse predeclaree, pas choisie apres coup.

## Modeles concurrents verrouilles (formes exactes, pas de variantes libres)
1. GARCH(1,1) gaussien et Student (2 estimations discretes de la meme famille).
2. FIGARCH(1,d,1) — parametre d de memoire longue estime, borne [0,1].
3. ARFIMA(0,d,0) sur log(|r| + epsilon) de barres, epsilon = 1e-6 (fixe).
4. Volatilite stochastique log-normale AR(1) sur log-volatilite (estimation
   par filtre particulaire ou quasi-vraisemblance Kalman: une seule methode,
   fixee a l'inscription du code, avant resultats).
5. Reference naïve: volatilite constante par partition (base de comparaison).
Aucun HMM, aucune segmentation, aucun MSM.

## Comparaison (etape 1, IS, exploratoire)
- Fonction de perte unique: QLIKE sur la variance realisee de barre suivante.
- Metrique unique: perte moyenne QLIKE hors echantillon **interne** par blocs
  temporels (5 blocs chronologiques, estimation sur blocs precedents uniquement).
- Criteres de decision predertermines: un modele est "prefere sur IS" si sa
  perte est inferieure a celle de tous les autres dans au moins 4 blocs sur 5
  ET en moyenne; sinon verdict "non departage sur IS".
- Dependance: ecarts de perte compares par bootstrap par blocs mensuels
  (1000 replications, graine 11); pas de Diebold-Mariano sans HAC documente.
- Multiplicite: famille unique de 5 modeles x 1 metrique; les comparaisons
  deux a deux (10 paires) corrigees par BY, m=10, seuil q<0,05, declare ici.
- Robustesse predeclaree (pas de selection): memes calculs (i)/(ii)/(iii) et
  variante sans republications; toute divergence est rapportee, pas tranchee
  en choisissant la variante favorable.

## Etape 2 (NON incluse, autorisation separee ulterieure)
Si et seulement si l'etape 1 departage un modele: verrouillage par hash du
modele, des parametres de serie et de la metrique, puis consultation unique
de l'OOS comme famille de confirmation (gouvernance multiplicite du protocole
1R FINAL, section D). Aucune modification apres lecture OOS.

## Criteres d'arret
Si aucun modele ne se departage sur IS: conclusion "memoire de volatilite
continue non departagee entre familles" — resultat final de l'etape, pas un
echec a contourner par re-parametrage. Si les perimetres (ii)/(iii) se
contredisent: le resultat est l'era-dependance elle-meme.

## Budget et infra
0 FCFA, GitHub Actions CPU, series deja construites (pas de relecture tick
sauf variante republications, qui exigerait un calcul distant dedie a inscrire).
