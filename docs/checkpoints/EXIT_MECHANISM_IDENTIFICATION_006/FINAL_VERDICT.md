# EMI-006 — VERDICT FINAL

1. **État observable précédant les cinq clôtures** : PnL latent proche ou
   au-dessus du PWA sur une jambe haussière (ΔPnL 30 s : +1,6 à +7,2 bp,
   5/5) ; C clôture marginale à −0,25 bp.
2. **Durée minimale de confirmation commune** : **elle n'existe pas** —
   intersection vide sur les 35 combinaisons θ × variantes de persistance
   (B : 107,9 s favorables sans clôture ; C : 0,5 s ; D : 5,5 s).
3. **Signature de cadence périodique** : aucune cadence fixe ancrée à
   l'ouverture > 1 s n'est commune aux cinq clôtures ; la cadence à phase
   libre est non identifiable sur cinq événements.
4. **Rapides vs récupération** : même famille compatible (état favorable +
   jambe haussière) ; la différence tient à la trajectoire du PnL, pas à
   un mécanisme séparé démontrable.
5. **Famille expliquant le mieux les clôtures sans look-ahead** : la
   famille « état favorable + déclencheur non ponctuel » d'EIDR-005,
   **resserrée** : persistance unique et cadence ancrée éliminées ;
   restent cadence à phase libre, condition hybride, ou variable hors
   trajectoire Mid — équivalentes entre elles.
6. **Paramètres réellement contraints** : les bornes par panier
   (`EXIT_PARAMETER_COMPATIBILITY.csv`) et les exclusions ci-dessus.
7. **Paramètres indéterminés** : tout (θ, T) ponctuel, tout (N, φ),
   toute condition supplémentaire chiffrée.
8. **Observations nécessaires pour départager** : de nouvelles clôtures
   réelles indépendantes (idéalement ≥ 10–20, avec Bid/Ask), dont les
   instants contraindraient (N, φ) et les intervalles de persistance ;
   ou les journaux d'exécution du provider (inaccessibles, aucun
   contournement).
9. **Nature du moteur livré** : **famille compatible paramétrique et
   outil de recherche** — pas une reconstruction démontrée de l'EA.

Conclusion : EMI-006 fait progresser la connaissance par élimination
mesurée. Le mécanisme ponctuel de déclenchement reste non identifiable
avec les observations actuelles, et cette limite est démontrée
(intersections vides, contre-exemple C), non contournée.
