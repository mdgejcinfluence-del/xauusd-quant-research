# MARKET MAKING ET SÉLECTION ADVERSE — LE MODÈLE À TROIS TERMES

Revenu net du fournisseur = spread capté − perte de sélection adverse (markout négatif après
fill) − coût d'inventaire (variance portée × aversion) − coûts de couverture. Nos mesures
bornent le premier terme (spread médian 2,33 bp M15 ; reflux associé 0,17 bp) et sont muettes sur
les deux suivants : sans transactions ni file, le markout *d'exécution* est inobservable — un
limite touché par le prix est souvent un limite que le prix va traverser. Conditions où le
modèle peut payer (littérature) : flux majoritairement non informé, retrait discipliné aux
annonces et aux régimes de saut, inventaire plafonné et retourné vite. Conditions où il meurt :
annonces, ouvertures, tendance intraday forte. META ALPHA ne peut ni vérifier ni exercer ces
conditions sur CFD au marché ; toute proposition future devra commencer par un journal de fills
réels en démo (compte fondateur), avec markouts à 10 s/1 min/5 min comme première métrique —
avant tout backtest.
