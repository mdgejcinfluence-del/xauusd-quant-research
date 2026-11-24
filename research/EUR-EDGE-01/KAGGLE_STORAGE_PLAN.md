# EUR-EDGE-01 — PLAN DE STOCKAGE KAGGLE

Compte vérifié en CI (`kaggle datasets list --mine` fonctionnel, datasets XAUUSD existants).
Règle unique : **ne monte sur Kaggle que ce que la licence autorise**, en datasets **privés**.

| Dataset prévu | Contenu | Statut |
|---|---|---|
| `EURUSD-CFTC-COT` | COT Euro FX 099741 nettoyé + brut | AUTORISÉ (domaine public) — à créer après QC |
| `EURUSD-CENTRAL-BANKS` | taux BCE/Fed/Treasury + millésimes | AUTORISÉ (citation) — après complétion des taux |
| `EURUSD-MACRO-*` | publications officielles avec dates de parution | AUTORISÉ — phase suivante |
| `EURUSD-SPOT-TICKS` / `EURUSD-SPOT-OHLC` | ticks/barres broker | **INTERDIT** sans accord écrit Dukascopy (ou autre source aux droits compatibles) |
| `EURUSD-FUTURES-6E` / `EURUSD-OPTIONS-VOLATILITY` | CME | **INTERDIT** sans licence |
| `EURUSD-RESEARCH-FEATURES` | variables dérivées | seulement si dérivées de sources autorisées |

Chaque dataset : description, fournisseur, couverture, fréquence, unités, fuseau, licence,
méthode d'acquisition, date de mise à jour, manifeste SHA-256, schéma. Aucun jeton dans GitHub
(le CI utilise le secret existant). Les quotas sont vérifiés par la taille réelle avant version.
