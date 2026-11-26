# RISQUES ET SCÉNARIOS IMPRÉVUS

Scénarios mesurables et protections : élargissement du spread aux annonces (filtre : ne pas
entrer si spread > quantile 99 de sa distribution récente ; NON_EXECUTION comptée) ; trous de
cotation (événement classé DONNEES_INSUFFISANTES, jamais de prix fictif) ; gaps de week-end
(fenêtres d'exécution bornées, sorties au premier tick réel) ; file de pertes (arrêt de
simulation après drawdown de portefeuille prédéfini dans le protocole de confirmation) ;
défaillance de flux (collecte idempotente, retries, manifeste d'heures) ; dérive de régime
(suivi continu, évaluation uniquement aux tailles préenregistrées, jamais de ré-optimisation en
cours). Non protégeables et reconnus : choc géopolitique hors cotation, défaillance du courtier,
changement structurel du marché de l'or. Aucune promesse de couverture totale n'est faite.
