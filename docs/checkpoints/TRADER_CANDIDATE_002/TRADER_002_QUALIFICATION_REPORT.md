# TRADER-CANDIDATE-002 — Rapport de qualification (moteurs A→G)

**Provider :** HFM Copy Trading 147053644, « T W.B.U », Copy Pro, Nigeria affiché.
**Bio affichée :** « A price-action strategy built around key Support &
Resistance levels, market structure and price reactions. » (déclaration, N0)
**Sources :** deux fichiers HTML HFM fournis par le fondateur + 3 captures,
archivés dans ce dossier avec empreintes au manifeste. Les deux HTML sont
**deux instantanés du même profil à une minute d'intervalle** (Server Time
28 nov. 2026, 08:19 et 08:20) ; leur Trading Activity est identique.
Aucune observation n'a été complétée artificiellement.

## 1. Moteur A — qualification du dossier (`ere/intake.py`)

Dossier accepté : **6 lignes conservées, 0 doublon retiré**, provenance
complète (chaque ligne pointe vers sa ligne HTML), `b_ready = vrai`.
Le passage réel de ce dossier a corrigé un défaut de l'infrastructure :
la première version de l'empreinte de déduplication fusionnait les deux
positions de 04:05:31 (même lot 0,08, profits différents 53,12 et 45,12).
L'empreinte couvre désormais tous les champs descriptifs ; les 16 tests
passent. **Faits structurants : les 6 lignes forment 3 épisodes de
2 positions simultanées** (mêmes horaires d'ouverture et de clôture par
paire), pas 6 transactions indépendantes.

Champs absents sur 6/6 lignes : **prix d'entrée, prix de sortie, fuseau
horaire**. Statistiques de page enregistrées comme claims non vérifiées :
gain affiché 5 620,95 %, drawdown max affiché 23,76 %, balance $630,08,
profit moyen $4,10 / perte moyenne −$3,32. **Le gain affiché n'est utilisé
comme preuve de rien.**

## 2. Moteur B — comportement (faits, puis interprétations)

**Faits observés (N1).** 3 épisodes le 2026-11-27, tous Buy, XAUUSDr :

| Épisode | Positions | Lots | Durée | Profit total affiché |
|---|---|---|---|---|
| 04:05:31 → 04:05:45 | 2 | 0,08 + 0,08 | **14 s** | +98,24 |
| 07:22:04 → 07:23:04 | 2 | 0,01 + 0,10 | **60 s** | +6,17 |
| 10:19:39 → 10:21:00 | 2 | 0,01 + 0,10 | **81 s** | +14,35 |

Concentration 100 % Buy sur l'échantillon visible ; détention très
courte (14–81 s) ; entrées et sorties strictement simultanées par paire ;
tailles asymétriques dans 2 épisodes sur 3 (0,01 + 0,10).

**Interprétations (N2, étiquetées).** Ouverture fractionnée en deux
tickets (fractionnement ou double exécution — indiscernables ici) ;
style compatible avec des captures de micro-mouvements ; **aucun**
renforcement après ouverture n'est observable (les paires naissent et
meurent ensemble). Contrairement au dossier Colorful, rien n'évoque une
récupération d'inventaire : pas d'ajout différé, pas de détention longue.

**Contexte de marché (descriptif, hypothèse UTC non confirmée).** Sur les
ticks Dukascopy du 2026-11-27 : l'épisode de 07:22 coïncide avec une
hausse de ~+6,0 bp pendant la détention ; celui de 04:05 se déroule sur
un prix quasi plat (−0,1 bp) malgré +98 affichés ; la fenêtre de 10:19
ne contient aucun tick sous l'hypothèse UTC. Conclusion descriptive :
**les horodatages affichés ne sont pas alignables en UTC Dukascopy** —
le fuseau du serveur HFM est une donnée manquante bloquante.

## 3. Moteur C — hypothèses concurrentes (toutes N3, aucune privilégiée)

| Hypothèse | Soutenue par | Contredite / fragile | Donnée discriminante |
|---|---|---|---|
| H-SR : réactions support/résistance (bio) | bio déclarée ; entrées ponctuelles | aucun prix d'entrée : intestable en l'état | prix d'entrée + niveaux du jour |
| H-IMP : capture d'impulsion/micro-momentum | détentions 14–81 s ; épisode 07:22 haussier | épisode 04:05 plat en UTC ; fuseau inconnu | horodatages alignés sur ticks |
| H-SCALP : scalping de micro-mouvements indépendant des niveaux | durées, profits rapides | ne prédit rien sur les points d'entrée | distribution des entrées vs volatilité |
| H-FRAC : fractionnement d'exécution (deux tickets systématiques) | 3/3 paires simultanées | peut coexister avec toutes les autres (mécanique, pas économique) | historique complet : la paire est-elle constante ? |
| Inconnue | toujours conservée | — | — |

## 4. Moteurs D/E — plan d'expériences préenregistré (non exécuté)

Protocole gelé à l'exécution future, dans cet ordre : (1) obtenir le
fuseau du serveur et les prix d'entrée/sortie (export du compte ou
captures horodatées) ; (2) aligner les 3 épisodes sur les ticks
Dukascopy et mesurer le mouvement −5 min → +5 min autour de chaque
entrée — H-IMP prédit une accélération préalable, H-SR prédit une
proximité à un niveau extrême local, H-SCALP ne prédit ni l'un ni
l'autre ; (3) n'étendre à F (signatures sur corpus) que si l'alignement
discrimine. Aucun backtest de rentabilité n'est autorisé à ce stade.

## 5. Moteurs F/G — registre des signatures et qualification

Signatures observées (descriptives, N1/N2) : paires systématiques 3/3 ;
détentions ≤ 81 s ; Buy uniquement ; aucun ajout différé. Aucune
signature de marché n'a été recherchée (F non exécuté : l'alignement
temporel, préalable à tout calcul, est bloqué).

**Qualification G : `COMPATIBLE MAIS NON IDENTIFIÉ` — niveau atteint N2**
(profil comportemental documenté ; aucune hypothèse au-delà de N3,
aucune signature mesurée N4). Verdict de campagne : **NOT_IDENTIFIED**.

## 6. Limites et prochaines données nécessaires

1. Fuseau horaire du serveur HFM (bloquant pour tout alignement).
2. Prix d'entrée/sortie par ligne (bloquant pour H-SR).
3. Historique au-delà de 6 lignes (les statistiques de page suggèrent
   un historique plus large, non fourni et non vérifiable ici).
4. Conditions du compte (levier, spread, commissions) pour toute
   lecture économique des profits affichés — jamais pour les copier.

Ce que META ALPHA a appris : un comportement d'exécution fractionnée
ultra-courte, acheteur sur l'échantillon, sans accumulation — presque
l'opposé géométrique de Colorful. Ce qu'il ne peut pas identifier :
pourquoi ces entrées, à quels prix, et si un phénomène de marché
rémunère ce style. Les expériences ci-dessus sont celles qui réduiraient
l'incertitude, dans l'ordre.
