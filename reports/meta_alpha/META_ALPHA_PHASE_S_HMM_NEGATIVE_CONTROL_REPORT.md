# META ALPHA — PHASE S : CONTRÔLE NÉGATIF DU HMM (simulation uniquement)

Question: la chaîne HMM envisagée pour la Phase 1R invente-t-elle des états
discrets dans un processus GARCH continu **sans aucun régime**?
Aucune donnée réelle lue (ni IS, ni OOS, ni Holdout). Aucun paramètre modifié
silencieusement: la chaîne est celle de la Phase S, inchangée.

## Configuration et traçabilité
- Générateur: GARCH(1,1) ω=0,05, α=0,10, β=0,85; n=4000; échelle 1e-4.
- Chaîne: granularisation |r| en barres de 10 (référence), HMM gaussien sticky=50,
  K=2 vs K=1 comparés par BIC. Sensibilités: barres 50; sticky 10/200; K=3.
- Graines **2000-2011: jamais utilisées** pour calibrer quoi que ce soit.
- Critère préenregistré dans le code avant exécution: « le HMM invente des régimes
  si BIC préfère K=2 dans > 50% des répétitions ».
- Hashes SHA-256: `phase_s_hmm_neg.py` 47d04016…, `phase_s_sim.py` d13d1317…,
  résultats `HMM_NEGATIVE_CONTROL.json` 7f2b30c3… (valeurs complètes au commit).
- Coût mesuré: 15,2 s CPU pour 32 ajustements. 0 Fcfa.

## Résultats par répétition (configuration de référence, extrait chiffré)
- **BIC préfère K=2 dans 12/12 répétitions** (gain BIC médian ≈ 66,7 en faveur de K=2).
- État minoritaire occupé à ~31% (médiane): pas un état résiduel, deux « régimes »
  équilibrés et plausibles en apparence.
- Bascules médianes: 36 par série de 400 barres; durée moyenne d'état ≈ 11 barres.
- Sensibilité: sticky 10 ou 200 ne change rien (8/8 K=2 préféré); **K=3 aussi
  préféré (4/4)** — plus on offre d'états, plus le HMM en « trouve ».
- Seule atténuation: en barres de 50, BIC préfère K=1 (0/12): l'agrégation grossière
  lisse le regroupement GARCH jusqu'à le rendre invisible au critère — ce qui montre
  que le verdict dépend de la granularité, pas d'une vérité d'état.

## Comparaison avec la segmentation (Phase S)
Même maladie, autre organe: la segmentation BIC hallucinait des ruptures dans le
GARCH (corrigée par pénalité renforcée, au prix de l'aveuglement aux vrais régimes
de volatilité); le HMM, lui, **structure le regroupement continu de volatilité en
deux états discrets nets, stables et reproductibles** — donc encore plus convaincants
en apparence, et tout aussi fallacieux comme preuve d'états discrets.

## Verdict final
**La chaîne HMM, telle que configurée, INVENTE DES RÉGIMES sur processus GARCH
continu (critère préenregistré déclenché à 100%).** Elle n'est pas validée comme
détecteur autonome d'états discrets. Ce qu'elle mesure réellement ici est la
persistance de la volatilité (ANOM-002), qu'elle discrétise arbitrairement.
Implication pour toute Phase 1R future (non autorisée, non commencée):
un état HMM ne pourra être présenté comme "régime découvert" que s'il survit à
un contrôle négatif de ce type appliqué à des substituts GARCH calibrés, et à une
comparaison explicite contre un modèle continu (GARCH/ARFIMA) à protocole gelé —
exactement le rôle prévu du test T4 dans le protocole corrigé.
Toutes les répétitions, y compris les sensibilités, sont conservées dans
`phaseS/HMM_NEGATIVE_CONTROL.json`.
