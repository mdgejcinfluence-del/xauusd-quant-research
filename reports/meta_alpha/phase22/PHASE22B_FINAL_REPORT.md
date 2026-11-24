# PHASE 22-B — RAPPORT FINAL : SORTIES STRUCTURELLES DES FAMILLES A ET B

Statut : `EXPLORATORY_POST_HOC`. Réconciliation exacte : 3 073 événements A / 505 reprises B, 0 manquant.
P&L libellés `HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION` (S2 principal,
commissions exclues, objectif liquidé au niveau théorique conservateur, stop au premier prix exécutable
observé). Verdicts au registre seq383.

## Famille A — Sweep & Reclaim, stop au-delà de l'extrême balayé

Le stop structurel est très proche de l'entrée (distance médiane ~10 bp : l'entrée se fait à la
réintégration, l'extrême balayé est juste au-delà du niveau), tandis que le centre de la boîte est à
~22 bp (Overnight) ou ~52 bp (Previous Day) et l'extrémité opposée à ~46–105 bp. Conséquence mécanique
et mesurée : **le stop est touché avant l'objectif dans 72–80 % des cas** (objectif d'abord : 5–27 %).
Espérance nette S2 négative partout : −2,2 à −5,8 bp, significativement négative pour 7 des 8
configurations (niveaux × cibles, q BH ≤ 0,05), médiane ≈ −10 bp (l'issue médiane est le stop),
négative dans les deux sous-périodes pour toutes les configurations. Le ratio structurel affiché
(2,2–9,9) n'est pas le ratio réalisé : le premier franchissement est presque toujours le stop.

**Verdict A : `SWEEP_STRUCTURAL_STOP_FAILURE`** (et `SWEEP_NO_STRUCTURAL_PAYOFF_ADVANTAGE`).

## Famille B — Impulse–Pullback–Resumption, stop à l'extrême du pullback, TP 1,5R / 2R

R médian ~70 bp (le pullback est profond relativement à l'entrée). TP atteint avant stop dans
seulement 24 % (1,5R) et 14 % (2R) des cas ; stop d'abord 44–46 % ; expirations 32–41 %.
Espérance nette S2 : −6,8 bp (1,5R, IC95 [−14,0 ; +0,6]) et −9,3 bp (2R, significativement négative),
R réalisé moyen −0,10 / −0,14, médianes −31/−33 bp, 37 % de pertes > 50 bp, inversion de magnitude
entre sous-périodes (−11,6/−14,6 bp en 2010-2015 contre ~0 en 2016-2019). Aucun critère cumulatif
de candidature de la section 7 n'est satisfait (registre : 0 candidat sur 10 configurations).

**Verdict B : `IMPULSE_STRUCTURAL_STOP_FAILURE`** (et `IMPULSE_NO_STRUCTURAL_PAYOFF_ADVANTAGE`).

## Réponse à la question de clôture

**Non.** Définir les sorties par des niveaux structurels connus à l'entrée ne rend ni le Sweep &
Reclaim ni l'Impulse–Pullback–Resumption économiquement intéressants sur l'IS 2010–2019 : dans les
deux familles, l'invalidation structurelle est statistiquement touchée avant l'objectif et
l'espérance après spread et slippage S2 est négative. Conformément à la condition de clôture,
**les deux concepts sont archivés sous leurs définitions testées** ; ils ne doivent pas être relancés
avec de nouveaux buffers, objectifs ou paramètres sur les mêmes événements. Toute validation
ultérieure exigerait des données véritablement nouvelles et indépendantes (la holdout 2020–2026
reste définitivement fermée).

Incidents corrigés avant interprétation : mort du runner du lot b07 lors du chargement tick global
(traitement borné par journée), identifiants et prix d'entrée déjà corrigés en 22-A et réutilisés ici.
