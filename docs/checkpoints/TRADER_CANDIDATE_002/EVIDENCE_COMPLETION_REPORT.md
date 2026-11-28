# ERE-TR002-002 — Complétion des preuves et porte d'identification

**Issue : C (données indisponibles), avec les éléments partiels de B
documentés. Verdict maintenu : NOT_IDENTIFIED — niveau N2.**

## 1. Sources effectivement inspectées

Les deux HTML archivés (empreintes revérifiées OK au manifeste), les
trois captures, le dossier brut et le rapport d'entrée de seq504–505,
plus une recherche documentaire externe sur l'heure serveur HFM.
Inspection profonde des HTML : 133 balises script, aucun état sérialisé
contenant les transactions — les seules occurrences des dates des
épisodes sont les cellules du tableau rendu. Aucun prix, aucun
identifiant de position, aucun fuseau n'existe dans ces fichiers.

## 2. Fuseau horaire — statut : UNKNOWN (candidat documenté, non prouvé)

Des sources tierces (revues de courtiers, non officielles) décrivent
les serveurs HFM/MT5 comme **GMT+2 l'hiver, GMT+3 l'été**, ce qui
donnerait GMT+2 le 27 novembre 2026. Mais : (a) ce ne sont pas des
documents officiels HFM ; (b) rien ne prouve que l'horodatage de la
page web du provider soit l'heure serveur plutôt qu'une heure
d'affichage. Conformément à la règle de la mission, le fuseau n'est
**pas** déduit d'une coïncidence de marché et reste **UNKNOWN**.
La preuve qui le lèverait : un export de compte (MT5 : historique avec
identifiants), une capture indiquant explicitement le fuseau, ou une
documentation officielle HFM liant l'affichage web à l'heure serveur.

## 3. Prix d'entrée et de sortie — statut : ABSENTS

Absent des HTML, des captures et de tout état embarqué. Ils ne seront
jamais reconstruits à partir des profits affichés (le profit dépend du
contrat, du lot et des coûts — l'inversion serait une fabrication).
**Demande documentaire minimale au fondateur** (un seul des éléments
suffit à rouvrir le dossier) : export d'historique MT5/HFM du provider
couvrant le 2026-11-27 avec identifiants de position, prix d'ouverture
et de clôture ; à défaut, captures de l'historique détaillé affichant
les prix et le fuseau.

## 4. Audit de la correction de déduplication

Correction de seq505 confirmée et durcie : l'empreinte couvre tous les
champs descriptifs, **y compris désormais `position_id`** (ajouté aux
champs reconnus). Tests de non-régression ajoutés (20/20 PASS) :
même taille + mêmes horaires + profits différents → 2 positions
conservées ; identifiants différents → conservées ; vrai doublon
strict → détecté, et la source brute n'est jamais mutée. Nouveau :
`build_episodes` reconstruit les épisodes en conservant les
`source_refs` de chaque position — traçabilité vérifiée sur le dossier
réel (3 épisodes × 2 positions, toutes référencées). Aucun autre
dossier ingéré n'est affecté (Colorful et la tranche synthétique ne
passent pas par cette empreinte ; tranche re-vérifiée : NOT_IDENTIFIED).

## 5. Alignement avec les ticks — statut : NON EXÉCUTÉ (par règle)

Le protocole est prêt (conversion explicite depuis un fuseau source
documenté, horodatages originaux conservés, distinction absence de
données / absence de correspondance, vérification de couverture des
partitions) mais **aucune recherche de signature n'a été exécutée** :
les horaires ne sont pas qualifiés. Le constat descriptif de la
campagne précédente (épisode plat en UTC malgré un profit affiché) est
exactement le type d'artefact qu'un alignement incertain transformerait
en fausse conclusion.

## 6. Hypothèses encore ouvertes

H-SR (supports/résistances), H-IMP (impulsion), H-SCALP
(micro-mouvements), H-FRAC (fractionnement — mécanique d'exécution,
compatible avec toutes), inconnue. Pour chacune, l'observation qui la
départagerait est consignée au rapport seq505 ; aucune n'a bougé,
faute de données nouvelles — c'est le résultat correct.

## 7. Verdict

**NOT_IDENTIFIED, N2.** La porte d'identification reste fermée, non
par échec du système mais parce que les trois données qui la lèveraient
(fuseau prouvé, prix, identifiants) ne sont pas dans les sources
autorisées. Le dossier se rouvrira sur production d'un seul élément de
la demande du §3, sans nouveau protocole à inventer.

*Sources externes citées : revues tierces sur l'heure serveur HFM
(fx-brokers.com, fxfan.club, forex.in.rs) — statut documentaire faible,
utilisées uniquement pour formuler le candidat GMT+2, jamais comme preuve.*
