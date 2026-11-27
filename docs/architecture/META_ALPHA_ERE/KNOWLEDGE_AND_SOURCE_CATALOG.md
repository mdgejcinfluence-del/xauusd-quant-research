# META ALPHA ERE — CATALOGUE DES CONNAISSANCES ET SOURCES

Chaque source : utilité, fiabilité, coût, licence, fraîcheur, modules
bénéficiaires, risques. Priorité aux ressources ouvertes à coût
maîtrisé. **Aucune référence n'est citée sans existence vérifiable** ;
les entrées « à acquérir » sont marquées comme telles.

## A. Sources documentaires scientifiques (module D)

| Source | Utilité | Fiabilité | Coût/licence | Bénéficiaires |
|---|---|---|---|---|
| Journal of Finance, Review of Financial Studies, JFE (articles sur microstructure et inventaire) | fondements théoriques | haute (revue par les pairs) | accès éditeur, souvent payant | C, D, G |
| arXiv (q-fin) et SSRN | prépublications, méthodes récentes | moyenne (non relues) | ouvert | C, E |
| Ouvrages de référence : Hasbrouck, *Empirical Market Microstructure* ; Bouchaud et al., *Trades and Markets* ; Aldridge, *High-Frequency Trading* | microstructure, exécution | haute | achat ponctuel | D, F, H |
| Documentation des bourses (CME pour l'or futures) et des régulateurs (CFTC, COT) | structure de marché, positionnement | haute (institutionnel) | ouvert | D, F |
| Documentation Dukascopy / brokers | conditions d'exécution réelles | moyenne (commercial) | ouvert | F, I |

## B. Données de marché

| Source | Utilité | Statut META ALPHA |
|---|---|---|
| Corpus Dukascopy certifié (348 partitions, 685 M ticks, 2010–2026) | terrain principal de découverte | **acquis, certifié, indispensable** |
| Collecte prospective Dukascopy post-gel (ME-001.4) | validation vierge | **en cours (catégorie D)** |
| Cotations HFM Bid/Ask réelles | exécution réaliste du lieu cible, ME-004 | absent — à collecter sur compte démo, aucun ordre |
| COT (CFTC), taux, macro (BCE/Fed) | régimes et contexte | partiellement collectés (EUR-EDGE), utiles en contexte |
| Kaggle et dépôts tiers | backfills | non certifiés — interdits pour valider |

## C. Méthodes et bibliothèques logicielles (à justifier par l'usage)

Python + pandas/NumPy (en production dans le projet), PyArrow/Parquet
(stockage du corpus), DuckDB/Polars (requêtes sur 685 M de ticks — à
évaluer sur benchmark réel avant adoption), statsmodels (tests),
scikit-learn (classification supervisée des signatures, avec garde-fou
anti-surapprentissage), matplotlib (rapports). Aucune bibliothèque de
« signaux » ou d'indicateurs n'est une source de connaissance.

## D. Modèles d'IA utiles

Le modèle de langage sert d'orchestrateur et de rédacteur de
protocoles (rôle actuel de l'agent) ; toute affirmation chiffrée doit
venir d'un calcul exécuté et journalisé, jamais de la génération de
texte. Les modèles probabilistes explicites (HMM de régimes, bornes
d'identification partielle) sont préférés aux boîtes noires pour les
verdicts.

## E. Validation, mise à jour, risques

Provenance obligatoire pour chaque connaissance (source, date,
qualité, limites) ; revue du catalogue à chaque mission fondatrice ;
risques : biais de publication (les stratégies publiées sont les
gagnantes), dépendance à un fournisseur de données unique, dérive des
conditions de marché (un phénomène mesuré en 2012 peut disparaître —
d'où la segmentation découverte/validation/prospectif).
