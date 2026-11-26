# AUDIT D'ACCESSIBILITÉ DES ACTIVITÉS ÉCONOMIQUES

Classement final par activité (définitions §7 de la mission) :
- Gestion de la dérive (deadline) : `DIRECTLY_ACCESSIBLE_TO_META_ALPHA` — en test prospectif ;
  reclassée `RISK_MANAGEMENT_CANDIDATE_NOT_PROVEN_PROFIT_SOURCE` : elle réduit une perte, elle
  ne crée pas de revenu démontré.
- Hygiène d'exécution (abstention spread/annonces) : `DIRECTLY_ACCESSIBLE_TO_META_ALPHA` —
  amélioration de risque, pas une source de profit.
- Fourniture de liquidité sur impulsions : `ECONOMICALLY_UNATTRACTIVE` dans sa forme testée —
  même la borne optimiste de remplissage perd −0,43 bp avant spread de sortie (P-EXP-01) ; la
  fourniture professionnelle (carnet, file, retrait aux annonces) serait
  `REQUIRES_PROFESSIONAL_INFRASTRUCTURE`.
- Prime de variance : `REQUIRES_DIFFERENT_FINANCIAL_INSTRUMENT` (options CME sur GC ou options
  sur GLD via compte titres) + `ACCESSIBLE_WITH_ADDITIONAL_LICENSED_DATA` pour l'historique fin.
- Hedging pressure / basis / carry futures : `REQUIRES_DIFFERENT_FINANCIAL_INSTRUMENT` (GC/MGC).
- Arbitrage de structure et market making sur carnet : `REQUIRES_PROFESSIONAL_INFRASTRUCTURE`.
- Grilles : `ECONOMICALLY_UNATTRACTIVE` (risque de ruine documenté GOLD-02/03).
Verdict global : `META_ALPHA_ONLY_RISK_MANAGEMENT_IMPROVEMENT_IDENTIFIED`, avec une voie
conditionnelle `META_ALPHA_REQUIRES_ADDITIONAL_INSTRUMENT_ACCESS` pour la prime de variance.
