# MA-EDGE-02 — RECHERCHE DE FLUX BID/ASK : BILAN ET CLASSEMENT

Question : existerait-il une source XAUUSD Bid/Ask gratuite, licite, automatisable, suffisante
pour alimenter le SHADOW ? Réponse : **oui pour l'observation prospective (niveau B, proche A)** —
le flux historique public de Dukascopy. Le blocage déclaré à la clôture MA-EDGE-01 est levé,
avec les limites écrites ci-dessous.

## Sources examinées

| Source | Bid/Ask | Accès | Temps réel | Historique | Licence/conditions | Classe | Décision |
|---|---|---|---|---|---|---|---|
| **Dukascopy datafeed public** (`.bi5` horaires) | Oui, tick ms, volumes | HTTP public, **sans compte ni clé** | Différé ≈ 1 h (fichier horaire clos) | Depuis 2003 (XAUUSD) | Accès public documenté ; recherche interne, pas de redistribution commerciale | **B+** (A pour une exécution chez Dukascopy même) | **RETENUE** |
| Darwinex TickData FTP | Oui, tick | Compte réel vérifié (sans dépôt), identifiants FTP personnels | Non (historique) | Depuis ~2017 | Conditions compte client | B | Repli si Dukascopy échoue ; exige les identifiants du fondateur |
| TrueFX (Integral OCX) | Oui, top-of-book ms | Historique gratuit après inscription ; flux = payant (FIX pro) | Payant | Depuis 2009 | Prix **indicatifs** institutionnels, non exécutables chez TrueFX | B−/C+ | Rejetée comme source principale (indicative) ; utilisable en contrôle croisé |
| HistData.com | Oui, tick/M1 | Gratuit sans compte | Non | Long, XAU/USD inclus | Personnel/éducatif, redistribution restreinte, **aucune garantie** ; horodatage EST fixe, résolution dégradée par périodes (secondes entières mi-2026) | C+ | Rejetée (qualité d'horodatage insuffisante pour une échéance à 60 s) |
| MT5 comptes démo courtiers (IC Markets, Pepperstone, etc.) | Oui, flux du courtier | Compte démo nominatif, terminal MT5 (Windows/ passerelle) | Oui | Limité | Identité du fondateur requise ; conditions du courtier | A− potentiel | Connecteur à préparer ; **bloquée uniquement par l'identité**, pas par le coût |
| OANDA / FXCM / FOREX.com API | Oui | Compte (démo possible selon juridiction) | Oui | Partiel | Identifiants personnels | A− potentiel | Même statut que MT5 démo |
| Miroirs GitHub de ticks Dukascopy (ex. dépôt 2026 hebdomadaire) | Oui | Git clone | Hebdomadaire | 2026 | Licence du dépôt MIT sur l'emballage ; les données restent régies par les conditions Dukascopy | B (provenance à revérifier) | Contrôle croisé seulement |
| CME/COMEX, flux options, carnet | Oui | Licencié payant (déjà chiffré 25-A) | Oui | Oui | Licence | A | Hors budget 0 — inchangé |

## Pourquoi Dukascopy est retenue

1. **Bid et Ask simultanés au tick**, horodatage UTC milliseconde, instrument XAUUSD spot réel et
   négociable chez l'émetteur du flux (pas un indice).
2. **Automatisation triviale et stable** : fichiers horaires publics numérotés, format `.bi5`
   documenté par de multiples implémentations ouvertes ; aucun identifiant, donc aucune
   information du fondateur requise.
3. **Historique postérieur au préenregistrement récupérable à tout moment** : la collecte peut
   être quotidienne (cron CI 03:30 UTC) sans « temps réel » au sens du trading — SHADOW est une
   observation, pas une exécution ; le différé d'une heure ne viole aucune règle du contrat, car
   la décision simulée n'utilise que des cotations ≤ t.
4. Limites assumées : représentativité = cotations Dukascopy (spread propre à ce courtier) ;
   aucune exécution réelle n'en sera déduite ; les résultats resteront nommés hypothétiques.
   Si le fondateur désigne plus tard son courtier cible, la même architecture acceptera son flux
   MT5 démo (niveau A−) sans changer le protocole.

Vérification technique (runs CI `edge02` 45452658440 et suivants) : **critères satisfaits** sur
les heures échantillons 2026-11-23/24 (42 899–49 642 ticks/heure, Bid < Ask sans exception,
horodatages strictement croissants, spread médian 0,40–0,45 USD, écart maximal < 3 s).
Retard de publication mesuré : fichiers horaires publiés par lots, plusieurs heures après la
clôture de l'heure (17:00 UTC pas encore disponible à 18:50 UTC) → collecte quotidienne par cron
(03:30 UTC) adoptée ; les heures en échec 503 sont réessayées automatiquement.
