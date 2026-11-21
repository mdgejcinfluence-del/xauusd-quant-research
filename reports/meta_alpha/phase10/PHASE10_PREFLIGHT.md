# PHASE 10 — RAPPORT DE PRÉFLIGHT (avant tout calcul)

**Date : 2026-11-13. Résultat : CONFORME sur tous les points contrôlés.**

1. **Hashes des sept documents gelés** : revérifiés à l'octet près,
   identiques au procès-verbal de gel seq283 —
   protocole `ba64f4ee…`, dictionnaire `9dff87bc…`, modèle de coûts
   `18a599cd…`, plan de validation `ed55b7d8…`, risques/autorisations
   `3f06b743…`, addendum de validation `fff4c521…`, addendum final
   `10dadebf…` ; procès-verbal lui-même `14ed57bc…`.
2. **Chaînage documentaire** : chaîne vérifiée valide (283 entrées,
   tête seq283 GEL) ; commit de référence du gel `a2c85344…` = HEAD
   courant et ancêtre du présent travail.
3. **Périmètre IS** : le moteur n'accède qu'aux partitions de
   `INVENTORY_348_EXHAUSTIVE.json` dont l'horodatage maximal est
   antérieur ou égal à la borne IS_END 2020-01-20 09:36:27 UTC
   (282 partitions), via les lots Kaggle/Drive déjà constitués.
4. **Holdout** : aucune partition postérieure à IS_END n'est listée,
   montée ni lue par le processus ; aucun chemin d'accès 2020–2026
   n'existe dans le code d'exécution.
5. **Portes avant inférence** : la synthèse applique les portes 1–4
   (magnitude, espérance nette centrale, queue MAE/P90/ES90 par
   événement et par grappe, effectifs) avant tout calcul de p-value ;
   une famille arrêtée ne produit aucune p-value.
6. **Multiplicité** : BY à m = 6 fixe — facteur 6 conservé dans le
   numérateur même si certaines hypothèses s'arrêtent aux portes
   sans produire de p-value.

Opérationnalisations déclarées (sans modification des définitions
gelées) : signaux calculés sur clôtures Mid, mesures de rentabilité
sur prix Bid/Ask ; entrée approchée par la première cotation de la
barre suivante (ouverture Bid/Ask de la barre d'entrée), le délai de
120 s étant contrôlé par la présence de la barre au créneau attendu
ou à la première barre après une fermeture régulière (coupure
quotidienne vers 21 h UTC, week-end) — approximation étiquetée ;
barre de timeframe valide si elle contient au moins la moitié de ses
minutes attendues ; sortie à l'ouverture exécutable de la première
barre débutant à ou après la fin de la fenêtre.
