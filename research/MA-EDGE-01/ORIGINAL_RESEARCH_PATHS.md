# MA-EDGE-01 — 04 · HYPOTHÈSES ORIGINALES ET PISTES NON EXPLORÉES

Registre complet et classé : `HYPOTHESIS_REGISTER.csv` (16 hypothèses, mécanismes, mesures,
biais, expériences, conditions d'abandon, priorités). Synthèse des pistes qui ne sont pas des
reformulations d'anciennes stratégies :

**Priorité haute**
- **H01 — Volatilité implicite de la veille (GVZ J-1)** : le marché price l'amplitude attendue ;
  notre programme n'a jamais utilisé d'anticipation, seulement du passé réalisé. Elle vise
  précisément le mécanisme de 24-F (gains qui rétrécissent, pertes entières).
- **H05 — Deadline de non-réévaluation** : la seule architecture de sortie jamais testée qui
  découle d'un fait mesuré (les faux positifs perdent −31 bp en dérivant 8 heures ; les vrais
  réalisent en 60 minutes médianes). Sortir les non-réalisés à une échéance **fixée à l'avance**
  tronque la perte sans toucher aux gagnants précoces. Exige un préenregistrement distinct et
  des événements frais pour être autre chose qu'un ajustement post-hoc.
- **H03 — Volume réel COMEX** (bloquée par la licence) : la confirmation par les transactions
  est l'information que nos cotations ne contiendront jamais.

**Priorité moyenne** : H02 (COT), H06 (alignement de tendance D1 — la direction de la tendance
n'a jamais servi, seule son amplitude), H07 (vitesse de détérioration du spread), H08 (événements
isolés hors grappe — signal fragile observé en EXP-06, à répliquer sur calibration avant tout),
H14 (profondeur de repli normalisée par la volatilité locale — proximité avec le ratio existant
explicitement signalée).

**Réfutées par les expériences de cette mission** : H09 (directions séparées), H10 (compression
asiatique), H11 (géométrie de premier passage), H12 (saisonnalité horaire), H13 (score à horizon
court). **Bloquées** : H04, H16 (licences).
