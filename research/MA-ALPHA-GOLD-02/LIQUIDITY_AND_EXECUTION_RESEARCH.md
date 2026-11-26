# LIQUIDITÉ ET EXÉCUTION — LE SPREAD EST UN REVENU, POUR QUELQU'UN D'AUTRE

Mesure propre (M-EXP-01, 24 889 impulsions M15) : contredire une impulsion rapporte ≈ +0,17 bp
**brut** aux horizons 1-4 barres — autrement dit le marché rend presque exactement le spread
(2,33 bp médian) à qui absorbe le mouvement, et le facture à qui le suit. Notre exécution au
marché nous place du côté qui paie. Devenir fournisseur exigerait : ordres limites avec file
réelle (probabilité de fill et markout à mesurer, jamais « touché = exécuté »), gestion
d'inventaire, et protection contre le flux informé des annonces — aucun de ces éléments n'est
dans notre corpus Bid/Ask. Ce que l'exécution peut déjà monétiser négativement (éviter de
perdre) : filtre de spread (EXP-12 : spread de décision élevé ↔ −6,1 bp), abstention aux
annonces, NON_EXECUTION comptée plutôt que prix fictif. L'edge d'exécution accessible à META
ALPHA est donc d'abord un edge de **non-dégradation** : il protège une espérance, il n'en crée
pas. Toute simulation future de limites sera présentée comme borne optimiste tant que fills et
files ne sont pas mesurés.
