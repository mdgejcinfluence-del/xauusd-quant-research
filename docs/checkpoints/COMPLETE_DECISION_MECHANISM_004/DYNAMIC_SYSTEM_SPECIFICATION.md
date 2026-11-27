# SPÉCIFICATION DU SYSTÈME DYNAMIQUE

EXIT_t = f(PNL_t, PWA_t, V_t, sigma_t, T_t, N_t, R_t) : la forme la mieux
compatible (M-D) utilise PNL_t (distance au PWA), V_t (jambe favorable en cours)
et la distance au sommet local ; sigma_t, T_t, N_t, R_t sans effet identifiable.
États et transitions : voir DYNAMIC_STATE_MACHINE (DIRR-003), inchangés, avec le
détecteur de régime post-entrée ajouté (trajectoire 60 s, descriptif).
Chaque règle porte son statut ; aucune fonction complète n'est prétendue.
