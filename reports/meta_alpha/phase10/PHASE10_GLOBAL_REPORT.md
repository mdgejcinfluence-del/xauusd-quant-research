# PHASE 10 — RAPPORT GLOBAL COMPARATIF (F10-01 à F10-06)

**Statut : résultats historiquement évalués sur corpus IS 2010–2020
(jamais des confirmations). Protocole gelé PHASE 10-A (seq283),
préflight conforme (seq284–285), ordre d'exécution seq284.
Holdout 2020–2026 jamais ouvert. Aucune promotion, aucune stratégie,
aucun septième test, aucune optimisation des seuils.**

Provenance des runs : run moteur 44919631588 vert (282 partitions IS) ;
sa synthèse a échoué sur un défaut de code (incident seq286) ;
deux relances moteur ont échoué par dégradation des téléchargements
externes (un timeout de 360 min) ; la synthèse corrigée a été exécutée
en mode `synth_only` sur les artefacts du run moteur réussi
(runs 44947740855, 44948062005, 44948472815 verts), résultats committés
par le workflow (`9abf9c3`). Tests temporels synthétiques 8/8 avant
exécution.

## Résultats par famille

| Famille | Détectés | Éligibles | Grappes | Net central moyen | Verdict |
|---|---|---|---|---|---|
| F10-01 H1 extrêmes Q95 | 0 | 0 | — | — | **NON ÉVALUABLE** (incident seuils) |
| F10-02 H1 cassures 20 barres | 5 652 | 5 477 | 2 972 | −4,51 bp | **NÉGATIF ÉCONOMIQUE** (porte 2) |
| F10-03 H4 extrêmes Q95 | 0 | 0 | — | — | **NON ÉVALUABLE** (incident seuils) |
| F10-04 H4 cassures 30 barres | 1 257 | 1 003 | 508 | −1,63 bp | **NÉGATIF ÉCONOMIQUE** (porte 2) |
| F10-05 D1 extrêmes Q90 | 246 | 184 | 162 | −16,19 bp | **NÉGATIF ÉCONOMIQUE** (porte 2) |
| F10-06 D1 compression → expansion | 657 | 657 | 430 | ratio médian 0,898 | **NÉGATIF ÉCONOMIQUE** (BY m=6 : p = 1,0) |

Aucune famille n'est POSITIVE ÉCONOMIQUE. Aucune p-value directionnelle
n'a été produite : les familles directionnelles évaluables se sont
arrêtées à la porte 2 (espérance nette centrale ≤ 0) avant toute
inférence, conformément aux portes gelées. F10-06, seule famille à
atteindre l'inférence, rejette l'expansion post-compression
(ratio médian 0,898 < 1 ; p bootstrap par grappes = 1,0 ; inchangé
après BY à m = 6).

Lecture : les cassures H1 perdent en moyenne −2,81 bp brut
(−4,51 net) ; les cassures H4 sont nulles en brut (+0,07) et négatives
après coûts ; les journées D1 extrêmes se retournent violemment contre
le signe (−14,49 bp brut). Les amplitudes existent (MAE médianes
24–67 bp, porte 1 franchie partout) mais ne sont pas capturables dans
le sens du signal aux prix exécutables. diagnostics par ère
(non confirmatoires) : F10-04 positive en 2010–2013 seulement
(+2,44 bp net, n=405), négative ensuite — aucune substitution par
sous-groupe n'est autorisée ni effectuée.

## Incident méthodologique (arrêt, pas de correction silencieuse)

F10-01 et F10-03 : les quantiles roulants Q95 ont été calculés sur des
fenêtres contenant des rendements NaN (barre manquante précédente,
typiquement la reprise du lundi) ; le quantile devenait NaN et aucun
événement n'a été détecté. Les définitions gelées ne sont pas en
cause : l'implémentation doit exclure les rendements indéfinis de la
fenêtre causale de 250 valeurs. **Aucune correction ni relance n'est
effectuée sans nouvelle décision formelle chaînée du responsable.**
F10-01/F10-03 restent NON ÉVALUABLES.

## Limitations

- Entrée approchée par l'ouverture Bid/Ask de la barre suivant le
  signal ; le délai de 120 s est contrôlé par la présence au créneau
  attendu ou à la première barre après fermeture régulière
  (approximation étiquetée au préflight).
- Barres de timeframe valides à ≥ 50 % de leurs minutes attendues ;
  MFE/MAE = extrema de trajectoire, jamais des rendements réalisables.
- Coûts : spread observé dans les prix Bid/Ask ; commission (0,7 bp)
  et slippage (1,0 bp) hypothétiques déduits une seule fois ; aucun
  coût réel de courtier.
- Corpus IS uniquement ; toute confirmation exige un ordre distinct
  (holdout, prospectif), de même que toute correction de l'incident
  F10-01/F10-03 ou toute suite J2/stratégie.

Rapports par famille : `RESULT_F10-01.md` … `RESULT_F10-06.md` ;
données : `PHASE10_EVENTS.csv.gz`, `PHASE10_RESULTS.json`.
