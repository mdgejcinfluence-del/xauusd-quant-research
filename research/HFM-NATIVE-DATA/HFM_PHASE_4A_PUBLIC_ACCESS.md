# PHASE 4A — ACCÈS PUBLIC HFM SANS COMPTE : VOIE HISTORIQUE INEXISTANTE

## Tick Chart Trader — examiné en priorité, réfuté pour l'historique (preuves)
Guide officiel HFM (PDF public `static.hfm.com/.../tick-chart-trader-user-guide-HFSV-en.pdf`,
consulté ce cycle, téléchargement du seul document — pas de données) : l'application « compile
les graphiques de ticks **à partir du moment où elle démarre. Elle ne donne pas accès à des
données de ticks historiques** » (§1/§2) ; le bouton Download (§4.3) exporte en TSV (date, Bid,
Ask) **uniquement les ticks enregistrés depuis le lancement**, pour le symbole affiché. Conditions
officielles Premium Trader Tools (HFSV, 2026) : service réservé aux **clients à compte réel**
(dépôt ≥ 100 USD, au moins un trade clôturé de ≥ 3 min par 30 jours). Réponses aux 10 questions :
(1) encore distribué oui, via les outils Premium ; (2) téléchargement public du guide oui, de
l'outil non (compte réel requis) ; (3) compte HFM **obligatoire** ; (4) connexion MT4/5 au
serveur HFM obligatoire (l'outil est un add-on terminal) ; (5) historique sans authentification :
**non** ; (6) les ticks exportés seraient bien ceux du flux du compte connecté — mais seulement
depuis le démarrage de l'outil ; (7) Bid et Ask séparés oui (TSV) ; (8) retour à 2010 :
**impossible par construction** (aucun historique, seulement l'enregistrement en direct) ;
(9) profondeur : la session d'exécution ; (10) export automatisable en principe (EA MT5), mais
c'est alors l'adaptateur `hfm_native_authenticated` — hors contrainte « sans compte ».
**Verdict 4A : aucun téléchargement historique HFM public sans compte n'existe via cet outil.**
Son usage futur éventuel = collecte **prospective** HFM LIVE/SHADOW après ouverture de compte
par le fondateur — décision qui lui appartient et qui n'est pas requise ici.

## Autres voies publiques HFM examinées
Portail myHF et FAQ officielles : l'« historique » offert est l'historique **de transactions du
client** (compte requis), pas un historique de cotations téléchargeable. Aucun fichier public de
cotations historiques, aucun endpoint documenté, aucun archive de prix publié par HFM n'a été
trouvé. Statut de la voie : `HFM_NATIVE_VERIFIED` — **aucune source**.
