# PLAN VOIE B — « LA DISCIPLINE EST L'EDGE » (document propriétaire, versionné tel quel)

Statut : recherche directionnelle systématique sur corpus gratuit — CLOSE (5 phases, 98 entrées).
Actifs : F3 (vol, L2) · F7 (sauts, L2) · châssis · simulateur · chaîne 98 entrées · OOS/HOLDOUT intacts.
Règle n°0 : aucune recherche directionnelle nouvelle sur ces données. Aucun re-grillage. Réouverture uniquement pour une hypothèse née d'une source NOUVELLE (volume, carnet), préenregistrement neuf, ordre explicite.

## Architecture
- L'HUMAIN → la direction : playbook écrit, 2 setups, 1 instrument (XAUUSD ; D1 tendance, H4/H1 entrée ; fenêtres 13h–16h UTC ; interdits 21h–23h, dimanche, alertes F7, annonces ±15 min ; 0–2 trades/jour ; R:R ≥ 1,5).
- LA MACHINE (châssis) → la discipline : sizing F3, évitement F7, kill-switch −2 %/jour, gouverneur −3 %/−5 %, risque/trade 0,15–0,35 %. **La machine a le veto.**
- LE SIMULATEUR → la décision : aucun frais tant que P(échec) > 25 %.

## Math du challenge (note de l'agent, consignée)
À dérive nulle, P(atteindre +T avant −D) = D/(T+D). Illustration du plan (cible type 8 %) : 55,6 % / 71,4 % / ≈40 %.
**Paramètres réels Blue Guardian 2-Step Pro 5k (OWNER_CONFIG_V1)** : Phase 1 (+10 %/−10 %) → **50 %** ; Phase 2 (+4 %/−10 %) → 71,4 % ; les deux → **≈36 %**, avant la dérive négative des coûts. EV sans edge < 0 : loterie, pas métier. Avec une petite dérive positive et le châssis qui empêche de mourir, la structure (temps illimité, T ≤ D) amplifie l'avantage.

## Phase démo (seul chantier ouvert)
Démo aux règles réelles (−4 %/jour, −10 % total), 60 jours ou ≥100 trades, journal écrit de chaque trade.
Gate GO/NO-GO : espérance démo > 0 sur ≥100 trades ET respect des règles ≥ 95 % ET challenge_sim sur stats réelles → P(échec) ≤ 25 %. Sinon : on continue la démo. Les frais sont du capital.

## Réouverture éventuelle
Données à information nouvelle (volume réel, carnet, flux de transactions) → préenregistrement neuf, même gouvernance, OOS/HOLDOUT intacts comme vérité jamais consultée.
