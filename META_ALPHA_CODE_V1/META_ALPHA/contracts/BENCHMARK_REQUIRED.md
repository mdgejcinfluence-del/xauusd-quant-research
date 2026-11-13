# Protocole de benchmark obligatoire

Aucun chiffre de performance (ticks/s, ETA, RAM, disque) ne peut être publié
avant que ce protocole soit exécuté sur le corpus réel.

1. Choisir 3 partitions : `part_000001`, `part_000174` (milieu), `part_000348` (fin).
2. Lancer `python -m metaalpha.bench` avec des threads = cœurs-1.
3. Mesurer :
   - débit de LECTURE depuis Google Drive (et non depuis un disque local) ;
   - débit d'ÉCRITURE d'un dérivé de même taille vers Drive ;
   - RAM pic (RSS) et espace de spill ;
   - temps de validation (hash + comptage).
4. Reporter l'intervalle bas/haut, JAMAIS un chiffre unique.
5. Vérifier que la mesure matérialise bien ce qu'elle prétend mesurer
   (piège de l'optimiseur, cf. Annexe B.4).
6. Signer `BENCHMARK_REPORT.json` (auteur, date, matériel, version du code).
