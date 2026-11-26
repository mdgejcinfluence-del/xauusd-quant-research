# PHASE 1 — ÉTUDE DES MOYENS D'ACCÈS HFM

## Voies comparées
1. **MT5 natif (retenue)** : package officiel `MetaTrader5` (Windows + terminal installé),
   fonctions `copy_ticks_range`/`copy_rates_range`. Limites documentées (MetaQuotes) : les barres
   servies sont bornées par le paramètre terminal « Max. bars in chart » et par l'historique que
   le **serveur du courtier** conserve ; la profondeur tick est typiquement très inférieure à la
   profondeur barres et varie par courtier — elle doit être **mesurée** (mode `probe` : première
   date retournée par TF et pour les ticks), jamais supposée. Les timestamps MT5 sont stockés en
   UTC (convention MetaQuotes) ; le décalage serveur éventuel devra être vérifié empiriquement
   contre une référence (comparaison au flux Dukascopy sur une fenêtre commune — contrôle, pas
   substitution). Prérequis : terminal Windows connecté au compte HFM Pro (lecture seule suffit ;
   aucun droit de trading requis pour `copy_*`).
2. **Portail myHF / exports officiels** : aucun service public d'export d'historique tick
   documenté à ce jour ; voie à confirmer auprès du support HFM (demande écrite préparée :
   profondeur tick/barre par symbole, archives anciennes, format). Aucune promesse retenue.
3. **Sources institutionnelles tierces** : autorisées seulement comme corpus **séparés et
   étiquetés** (jamais « HFM »). Notre Dukascopy existant sert déjà de référence de comparaison
   (divergences de spread/horaires documentables). Tout fournisseur payant : documenté, non
   souscrit (autorisation fondateur requise).
4. **Interdites et écartées** : contournement d'authentification, endpoints inventés,
   identifiants tiers, scraping contre conditions, substitution silencieuse.

## Spécifications publiques HFM (à confirmer par le serveur, jamais appliquées rétroactivement)
Page officielle HFM XAUUSD (consultée ce cycle) : compte **Pro** — spread « dès 0,16 »
(publicitaire, à mesurer), 1 lot = 100 oz, min 0,01 lot, incrément prix 0,01, valeur tick
1 USD/lot, marge 0,05 %, swap-free 45 jours selon entité. Le symbole serveur exact (suffixe
éventuel), le fuseau serveur et l'historique des spécifications restent **à mesurer** via
`symbol_info` au probe — aucun chiffre public n'est appliqué aux années passées sans preuve.

## Conclusion Phase 1
Architecture MT5 valide et construite ; le **pilote est bloqué par l'absence d'identifiants et
de terminal Windows**, pas par le code (pipeline validé en selftest synthétique, explicitement
non-HFM). Profondeur 2010 : **inconnue à ce stade** — toute affirmation serait une fabrication.
