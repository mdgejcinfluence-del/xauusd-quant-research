# MÉCANISME DE LA PATIENCE

La patience n'est ni une durée minimale (D clôture à 17 s) ni une temporisation :
c'est une **conséquence de l'état** — tant que le panier est en régime adverse et
que la condition de sortie (jambe favorable vers le PWA) n'est pas réunie, le
système conserve et renforce. Nos moteurs clôturent trop vite parce que leur
règle (premier retour au PWA après 60 s) transforme en sortie ce qui, chez le
trader, n'est qu'un passage. L'écart 82 % vs 40 % de paniers ≤ 120 s vient de la
règle de sortie du moteur, pas d'un paramètre de durée à ajuster — corriger par
une temporisation fixe serait un artifice refusé.
