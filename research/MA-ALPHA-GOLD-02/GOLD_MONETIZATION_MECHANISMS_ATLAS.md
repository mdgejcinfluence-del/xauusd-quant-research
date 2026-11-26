# ATLAS DES MÉCANISMES DE MONÉTISATION (registre complet : HYPOTHESIS_AND_MECHANISM_REGISTER.csv)

Synthèse des verdicts de ce cycle :
1. **Fourniture de liquidité de très court terme (M-EXP-01)** : le reflux post-impulsion vaut
   ≈ +0,2 bp brut — le spread entier. En preneur de liquidité nous le *payons* ; en fournisseur
   il faudrait ordres limites, file d'attente et gestion d'inventaire (données absentes). Le
   mécanisme existe ; il n'est pas accessible avec notre exécution au marché.
2. **Prime de variance (M-EXP-03)** : mesurée réelle sur l'or (IV > RV suivante, écart médian
   +2,0 points, RV ne dépasse l'IV que 29,7 % du temps). C'est la rémunération de qui vend
   l'assurance-saut. Monétisation = options (licence) ; une grille spot n'en est pas un équivalent.
3. **Grilles/paniers (M-EXP-02)** : 61,8 % d'épisodes gagnants, PnL moyen −1,7 bp, perte
   flottante pire −1 112 bp·unités, ruine à buffer 500 bp dans 0,7 % des journées — le profil
   « petits gains, queue lourde » est confirmé par nos propres données.
4. **Exposition sélective (M-EXP-04)** : aucun bloc horaire ne survit au coût d'un aller-retour
   quotidien ; le drift de l'or n'est pas monétisable par simple fenêtre d'exposition.
5. **Hedging pressure (littérature)** : prime documentée sur futures multi-matières, mesurable
   chez nous uniquement en hebdomadaire via COT — déjà testée comme règle (G-EXP-01) : instable.
6. **Transfert de risque événementiel** : les annonces concentrent l'amplitude (Phase 23) ;
   qui fournit la liquidité pendant l'annonce encaisse le spread élargi et le risque de saut —
   non simulable honnêtement sans carnet ni fills.
Conclusion de l'atlas : chaque mécanisme réel a un payeur et un risque identifiés ; ceux qui
sont accessibles à un preneur de liquidité retail ont été mesurés ≈ 0 ou négatifs après coûts ;
ceux qui paient (variance, liquidité, hedging pressure futures) exigent des instruments/données
licenciés ou une infrastructure d'exécution que META ALPHA n'a pas.
