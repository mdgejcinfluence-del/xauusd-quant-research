# PHASE 25-A — HYPOTHÈSES ÉCONOMIQUES PRÉCISES (à tester seulement sous autorisation 25-B)

**H-GVZ (volatilité implicite, contexte J-1)** : le problème de la Phase 24-F est que les gains
réalisés rétrécissent pendant que les pertes restent entières. Si la volatilité implicite de la
veille (GVZ) est élevée, le marché a déjà payé pour du mouvement : les réalisations du label
seraient suivies d'excursions adverses plus profondes (MAE avant/après passage plus grand) et les
faux positifs plus coûteux ; en régime d'IV basse et compressée, les impulsions seraient plus
souvent des bruits de cotations sans suivi. Variable exacte proposée : **variation et niveau de
GVZCLS connus la veille au soir** (dernière clôture publiée avant la journée de décision),
jamais la valeur du jour même. Mécanisme testable sans modèle : comparer, par terciles de GVZ
J-1 fixés sur la calibration, la fréquence de réalisation, G, L et le MAE des événements M15.

**H-COT (positionnement hebdomadaire)** : lorsque les positions nettes acheteuses des managed
money sur l'or COMEX atteignent des extrêmes (par rapport à leur propre historique publié), le
marché est encombré : une impulsion supplémentaire attire moins d'acheteurs marginaux, les
réintégrations échouent plus souvent et plus cher (faux positifs à −31 bp en Phase 24-E).
Variable exacte : **position nette managed money du dernier rapport COT publié avant la décision**
(âge 3-10 jours, jamais le rapport de la semaine en cours), en niveau et en rang dans son
historique disponible à la date de publication.

Aucune de ces hypothèses n'autorise une régression immédiate ni un filtre : la première étape
25-B serait une cartographie causale par terciles préenregistrés, sur calibration d'abord.
