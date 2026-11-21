# PHASE 10-A — PROCÈS-VERBAL DE GEL DÉFINITIF ET RAPPORT DE VÉRIFICATION DOCUMENTAIRE

**Date : 2026-11-13. Statut : PROTOCOLE GELÉ — EXÉCUTION NON
AUTORISÉE.** Le gel ne vaut pas autorisation d'exécution ; la
prochaine décision du responsable portera uniquement sur
l'éventuelle autorisation d'exécuter la campagne.

## 1. Décision

Le responsable de recherche accepte les deux dernières constantes —
**P90(MAE) ≤ 10 × C_ref**, **ES90(MAE) ≤ 15 × C_ref**, **délai maximal
d'entrée de 120 secondes** — et autorise le gel définitif du
protocole PHASE 10-A (chaîné seq282–283). Ces décisions sont
intégrées aux documents concernés.

## 2. Les sept documents gelés — SHA-256 définitifs

| Document | SHA-256 |
|---|---|
| PHASE10A_PROTOCOL.md | `ba64f4eede8c58f21ed4cd04448ef30a7a8ed46e6ca6c9b5da0926bdeb9d056c` |
| PHASE10A_DICTIONARY.md | `9dff87bcb81df14e996b2019dc8bd03f00a11a92f212732542dfba19a87cf3d6` |
| PHASE10A_COST_MODEL.md | `18a599cd188b3ffef1116ec63b171e6913bd6e81b371149373e9679e59cd1c6c` |
| PHASE10A_VALIDATION_PLAN.md | `ed55b7d819c2f21fb6cd78ced5dd929619bfd603e8f10533323f489a231c0e4d` |
| PHASE10A_RISKS_AUTHORIZATIONS.md | `3f06b743429666e3b8ae563a3fe9002ec003fca84b0dde01652c190c00b6bcc1` |
| PHASE10A_ADDENDUM_VALIDATION.md | `fff4c5212ff324c14a0042230a3173050121ac006cda861616999be91102a843` |
| PHASE10A_ADDENDUM_FINAL.md | `10dadebffd76d1700e9657140a3a335b58aa9d283517d54c53098b1a467b1501` |

**Ordre de prévalence** : en cas d'écart entre documents, l'addendum
final prévaut sur l'addendum de validation, qui prévaut sur les cinq
documents de conception ; tout écart constaté après le gel est un
incident documentaire à consigner en chaîne, jamais à corriger
silencieusement. L'addendum de validation (seq279) conserve son
en-tête daté « gel non autorisé » : il est conservé inchangé pour la
traçabilité et son statut est supersédé par le présent procès-verbal.
Aucune définition ne peut être modifiée après le gel sans nouvelle
décision formelle et nouvelle entrée dans la chaîne.

## 3. Rapport de vérification documentaire (points imposés)

1. **Décisions intégrées** : limites de queue et délai d'entrée
   acceptés reportés dans l'addendum final (§1, §2, §5), le modèle de
   coûts (porte de queue élargie et éligibilité d'entrée), le
   dictionnaire (lignes Délai d'entrée, P90, ES90, MAE de grappe), le
   protocole (statut gelé et renvois) et le document des risques
   (autorisations 1–2 marquées obtenues/effectuées).
2. **Références croisées réconciliées** : C_ref, portes 1–4, famille
   F10-01…F10-06, BY m = 6, grappes-composantes connexes et règle des
   5 % portent le même sens dans les sept documents ; F10-06 est
   unilatéral (H1 : ratio > 1) partout où son hypothèse est écrite.
3. **Seuils P90/ES90 par événement ET par grappe** : vérifié —
   addendum final §1 (application séparée, le dépassement d'une des
   deux distributions suffit), modèle de coûts (porte de queue
   élargie), dictionnaire (MAE_g défini), plan de validation §4.1.
4. **Échec d'une porte ⇒ arrêt, sans substitution par un sous-groupe** :
   vérifié — plan de validation §4, point 1, phrase explicite ;
   modèle de coûts §2 (« sans test de significativité pour voir »,
   portes non abaissées ni contournées) ; les ventilations sont des
   diagnostics non confirmatoires (addendum de validation §2).
5. **Délai de 120 secondes identique partout** : vérifié — addendum
   final §2 (règle et horloge à la réouverture, interruptions,
   week-ends), dictionnaire (ligne Délai d'entrée : même Δmax, même
   t_ouv, même statut INÉLIGIBLE_ENTRÉE_TARDIVE), modèle de coûts
   (éligibilité d'entrée, « règle identique au dictionnaire »),
   protocole (§ statut et cadre de mesure).
6. **SHA-256 définitifs calculés** après intégration (tableau §2) ;
   aucune modification postérieure au présent procès-verbal n'est
   permise sans nouvelle décision chaînée.

## 4. Interdictions maintenues

Aucun calcul de recherche, aucune extraction, aucune consultation du
corpus IS pour la Phase 10, aucun accès au holdout 2020–2026, aucun
backtest stratégique, aucun `challenge_sim`, aucune construction de
stratégie, aucune promotion automatique J2/J3, aucune consommation
de budget. XAU/USD uniquement ; FRED interdite ; 36 cellules S12
inchangées ; T0 non activé ; candidates P9 non reprises ; campagnes
et phases closes non relancées.
