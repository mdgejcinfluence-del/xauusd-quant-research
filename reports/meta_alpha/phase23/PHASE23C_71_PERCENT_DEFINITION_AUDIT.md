# PHASE 23-C — AUDIT DE LA STATISTIQUE « 71 % » DE LA PHASE 23-B

Définition exacte retrouvée dans le moteur 23-B (`phase23b_engine.py`, lignes 311-316) :

- Numérateur : 52 événements ; dénominateur : 73 événements FOMC (tous avaient un rendement
  15 minutes non nul). 52/73 = 71,2 %.
- `rend_15m` et `rend_60m` sont tous deux mesurés depuis le **premier tick strictement après t0**
  (prix d'entrée Mid), pas depuis P0 (dernier Mid avant t0) et surtout **pas depuis P15**.
- La statistique vaut : signe(rendement t0→60m) == signe(rendement t0→15m).

C'est donc une **continuation depuis le prix de départ** (le déplacement initial est-il toujours
présent à 60 minutes ?), et non une continuation après les quinze premières minutes. Les deux
notions, calculées séparément en 23-C (référence P0, dernier Mid avant t0) :

- continuation depuis P0 à 60 min : 69,9 % (cohérent avec les 71 % — l'écart vient de la référence
  premier-tick-après-t0 vs P0) ; à 240 min : 68,1 % ;
- **continuation après les 15 premières minutes : 52,1 % à 60 min et 58,3 % à 240 min** —
  statistiquement indiscernable d'un pile ou face à 60 minutes.

Conclusion de l'audit : les 71 % mesurent la persistance du déplacement initial par rapport au
niveau de départ ; ils ne démontrent **aucune progression directionnelle après P15** susceptible
de fonder une entrée à t+15. Ne jamais fusionner les deux notions.
