# VÉRIFICATION DES 4 POINTS DE CONTRÔLE (réponses exactes, limites incluses)

## Point 1 — Validité mathématique du BH-FDR cumulatif sous dépendances et adaptativité
**Verdict: PARTIELLEMENT VALIDE — heuristique conservative, pas une garantie.**
- Le BH classique contrôle le FDR sous indépendance ou dépendance positive (PRDS).
  Nos tests partagent les mêmes données, labels chevauchants et features corrélées:
  la dépendance est arbitraire. Sous dépendance arbitraire, la procédure valide est
  Benjamini-Yekutieli (BY), plus conservative d'un facteur ~ln(m).
- Notre "m cumulatif" (m = toutes les vagues) est une pénalité séquentielle dans
  l'esprit de l'alpha-investing, mais ce n'est PAS une procédure à garantie prouvée
  sous sélection adaptative (le choix des hypothèses de la vague n+1 dépend des
  résultats de la vague n). Aucune méthode FDR standard ne garantit le contrôle sous
  adaptativité arbitraire sans hypothèses supplémentaires.
- Conséquence opérationnelle (déjà la règle du projet): un "survivant" du gate n'est
  jamais un edge; il doit être confirmé sur données indépendantes (OOS chronologique,
  puis Holdout scellé en phase finale). Le FDR sert de filtre anti-bruit, pas de preuve.
- Amélioration codable: passer le gate en BY (dépendance arbitraire) et conserver le
  m cumulatif. À implémenter avant le gate de P3-002 (le moteur n'a encore jugé que
  l'historique); ce changement durcit le critère, il ne peut créer aucun faux positif
  supplémentaire. **Décision: BY + m cumulatif, à coder et revalider sur l'historique.**

## Point 2 — Exactitude de la reproduction historique P3-001 / P4-001
**Verdict: reproduction au niveau VERDICT, pas reproduction bit-à-bit.**
- P4-001: le gate relit le même fichier de résultats que le verdict d'origine
  (IC bootstrap déjà calculés, seed 42): le rejet est reproduit par construction.
- P3-001: le verdict d'origine combinait BH (m=15, vague seule) calculé en session et
  le filtre économique; le moteur rejoue les contrastes depuis les mêmes buckets
  d'origine (mêmes données, mêmes définitions RET_H_ALIGN_V1) et obtient 0 survivant,
  mais par la voie dominante du filtre économique (effets 0,1-0,5 bp << 2,17 bp), pas
  par une statistique identique ligne à ligne. Les t du moteur sont naïfs (labels
  chevauchants -> optimistes), limite écrite dans le code et le rapport de gate.
- Dire "exactitude stricte" serait donc faux; l'exigence réelle — même verdict, mêmes
  données, mêmes conventions, causes identifiées — est satisfaite et documentée.

## Point 3 — Impossibilité de réécrire silencieusement l'ancrage Git
**Verdict: falsification DÉTECTABLE, non impossible. "Impossible" serait un mensonge.**
- La chaîne de hash rend toute modification d'une entrée détectable sans réécrire
  toutes les entrées suivantes (test réel: "hash invalide seq 2").
- Mais un acteur disposant des droits d'écriture sur la branche pourrait réécrire
  la chaîne entière ET l'historique Git (force-push): rien dans un dépôt Git seul
  n'est absolument immuable face à son administrateur.
- L'ancrage réel est donc triple et relatif: (a) la chaîne interne, (b) l'historique
  distant de la branche (toute réécriture y laisse des traces: commits orphelins,
  divergences visibles par tout clone antérieur — dont cette session), (c) la tête de
  chaîne publiée dans les rapports de gate successifs: réécrire l'histoire devrait
  aussi falsifier rétroactivement chaque rapport citant l'ancienne tête, ce qui est
  détectable dès qu'un seul clone ou rapport antérieur subsiste.
- Renforcement possible sans dépense: publier la tête de chaîne dans un support hors
  branche (release GitHub horodatée par la plateforme) à chaque vague. Proposé,
  non encore activé.

## Point 4 — Naissance de P3-003 exclusivement par extraction d'anomalies
**Verdict: ENGAGEMENT PROCÉDURAL CODIFIÉ, exécution à venir — pas encore un fait.**
- La charte (BASE_CONNAISSANCES_PHASE2.md) et GOUVERNANCE_GENERATION_VAGUES.md
  (admission en 5 conditions, procédure d'échec en 4 étapes, volume sans quota)
  sont committées aujourd'hui et contraignent dès maintenant mes préenregistrements.
- P3-003 n'existe pas encore et ne naîtra qu'après le verdict de P3-002, par:
  analyse approfondie IS -> phénomènes mesurés (5 mesures) -> items K nouveaux
  -> hypothèses citées. Toute hypothèse sans citation K sera refusée à l'admission.
- Limite honnête: le respect de cette règle repose sur le préenregistrement vérifié
  (chaîne) et sur ma discipline d'agent documentée dans DECISION_REQUISE.json;
  aucun code ne peut, seul, juger qu'une justification est "scientifique".
