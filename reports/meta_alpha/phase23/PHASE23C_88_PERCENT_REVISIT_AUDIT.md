# PHASE 23-C — AUDIT DE LA STATISTIQUE « 88 % » DE LA PHASE 23-B

Définition exacte (moteur 23-B, ligne 211) :

- Numérateur : 64 événements ; dénominateur : 73. 64/73 = 87,7 %.
- Revisite = au moins un tick Mid, entre le premier tick strictement après t0 et t0+60 min,
  revenant au niveau ou au-delà de `prix_reference` (dernier Mid strictement avant t0), du côté
  opposé au premier tick post-annonce. Fenêtre d'observation : **60 minutes post-t0, incluant les
  15 premières minutes**. Détection : franchissement observable (≤/≥), pas égalité exacte.

Chronologie reconstruite en 23-C (référence P0, direction = réaction initiale à 15 min) :
65/73 premières revisites surviennent **avant t+15 min**, 1 entre 15 et 60 min, 7 absences à
240 min ; la revisite à 240 min concerne 90,4 % des événements. Le temps jusqu'à première revisite
est dominé par le bruit immédiat autour de P0 (médiane < 1 s dans la segmentation brute) : la
revisite est un phénomène de la phase de formation du prix post-annonce, pas un retour tardif.
Passages répétés de P0 : médiane ≈ 12-18 franchissements par fenêtre de 4 h — le prix oscille
autour de P0 ; clôture à 240 min de nouveau au-delà de P0 dans le sens initial : voir
`PHASE23C_EVENT_PATH_METRICS.parquet` (`cloture_240_au_dela_P0`).

Conclusion : les 88 % décrivent une oscillation rapide autour du prix pré-annonce dès les
premières minutes ; ce n'est ni un signal de retournement exploitable ni une validation de la
règle directionnelle.
