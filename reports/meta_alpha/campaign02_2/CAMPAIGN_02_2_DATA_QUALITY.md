# CAMPAGNE 2.2 — QUALITÉ, COUVERTURE ET BLOCAGE D'ACCÈS

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Contrôle | Résultat |
|---|---|
| Périmètre livré (instantanés) | 12 144 épisodes de dépassement, 777 journées, 2010-01-04 → 2014-03-11 ; 1 328 lignes RETEST de cassures — extraction du premier run, relue et recoupée contre les comptes Campagne 1 sur le même périmètre |
| Couverture décennale | **NON ATTEINTE à la date de livraison** : voir blocage ci-dessous. La garde de couverture ajoutée au moteur (≥ 200 journées par lot, erreur explicite) empêche toute livraison silencieusement partielle à l'avenir ; la présente livraison étiquette son périmètre au lieu de le masquer |
| Blocage d'accès (preuves commitées) | Kaggle API : 403 Forbidden sur les 8 lots, slug corrigé `shalom5123/...` compris (journaux `timeline_parts/*_log.txt`) ; repli HTTPS direct : 403 également ; Google Drive (gdown) : refus temporaire de quota (« Too many users have viewed or downloaded this file recently ») sur les partitions testées. Trois tentatives d'extraction consignées : run monolithique partiel (rejeté par le contrôle), run timeout 350 min, matrice 8 lots |
| Défaut corrigé pendant la campagne | Première version du moteur : la ligne T0 des cassures retestées était remplacée par la ligne RETEST (305 lignes T0 seulement dans le brut partiel) ; corrigé (lignes T0 et RETEST distinctes) dans le moteur par lots commité — les statistiques RETEST du rapport n'utilisent que les lignes RETEST, non affectées |
| Fenêtres | Issues bornées à T0+60 (gel) : positions à +60 indéfinies pour les instantanés T+1/+3/+5 (cellules vides par construction) ; invalidation après retest mesurée sur la même borne |
| Censure | Réintégrations censurées à 60 min conservées comme catégorie (`censure_60`) ; aucune imputation |
| Cohérence ancien/nouveau | Sur le périmètre commun, les comptes d'épisodes et les taux de réintégration reproduisent les ordres de grandeur Campagne 1 (85,3 % à T0 sur 2010–14) ; la profondeur rétrospective `prof60_retrospective_bp` est recalculée et stockée à part, étiquetée |
| Reproductibilité | Moteurs commités (`campaign022_engine.py` monolithique puis par lots), workflows et journaux CI commités, y compris les journaux d'échec — aucune trace effacée |
| Données fabriquées | Aucune. Les cellules non mesurées sont vides ou absentes, jamais comblées |
