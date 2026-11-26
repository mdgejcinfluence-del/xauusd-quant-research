# PHASE 2 — PREUVE DE COLLECTE : STATUT `BLOCKED_CREDENTIALS_AND_TERMINAL`

Le pilote réel (7 jours de ticks Bid/Ask + barres, provenance et schémas vérifiés) n'a **pas**
été exécuté : aucun identifiant HFM dans l'environnement, aucun terminal MT5 (Linux).
Conformément aux règles : aucun identifiant inventé, aucune donnée tierce présentée comme HFM,
aucune simulation présentée comme collecte. Ce qui est démontré à la place :
- le collecteur `ci_tools/hfm_collector.py` (modes probe/pilot/collect/selftest) ;
- le pipeline complet validé sur données **synthétiques** (selftest : 5 000 ticks, Bid<Ask,
  monotonie, spread recalculé, Parquet + SHA-256 + rapports qualité — fichier synthétique
  supprimé après test, jamais publiable) ;
- le refus explicite et journalisé du mode probe sans identifiants.
Déblocage : identifiants HFM Pro en secrets d'environnement + exécution sur poste Windows du
fondateur ou runner Windows avec terminal MT5 installé (procédure Phase 3). Dès le probe exécuté :
première date réelle par TF et ticks consignée ici, puis pilote 7 jours, puis seulement collecte.
