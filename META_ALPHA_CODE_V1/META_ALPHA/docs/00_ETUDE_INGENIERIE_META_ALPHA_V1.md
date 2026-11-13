# META ALPHA — XAUUSD DGP
## Étude d'ingénierie pour un agent quantitatif autonome exécutable

**Version :** 1.0
**Date :** 13 novembre 2026
**Périmètre :** `XAUUSD_TICK_ONLY_V1`, chaîne analytique Phases 2 → 9
**Document source :** `META_ALPHA_DOSSIER_STRATEGIE_ET_FEUILLE_DE_ROUTE_V1.md` (lu intégralement, 772 lignes)
**Budget plafond :** 6 000 FCFA — soit **9,15 EUR** (parité fixe XOF/EUR = 655,957)

> **Ce que ce document est :** une étude d'ingénierie avec le code, les commandes et les tests qui vont avec. Ce n'est pas un argumentaire commercial.
> **Ce que ce document n'est pas :** une promesse de rentabilité, ni une preuve qu'un edge existe, ni une garantie de service 24 h/24 à coût nul.

---

# RÉPONSE EN TÊTE — LES 5 POINTS EXIGÉS

## 1. Ce qui est techniquement possible avec 6 000 FCFA

| Possible | Détail |
|---|---|
| **Corpus 685 M ticks traité intégralement en < 24 h** | Oui, sur CPU, à coût 0 FCFA, en découpant le travail en segments de ≤ 4 h exécutés en parallèle. Débit réaliste 3–8 M ticks/s en scan analytique DuckDB (70–240 s par partition Parquet, 348 partitions), sous réserve de benchmark réel (voir §7). |
| **Infrastructure entièrement gratuite** | Oui : GitHub (code, Actions, artefacts) + Google Drive (données/artefacts) + Colab/Kaggle (calcul) + DeepSeek ou Gemini Flash (IA). Aucun service payant n'est **nécessaire**. |
| **Orchestrateur avec reprise, verrous, checkpoints** | Oui, à écrire (≈ 600 lignes Python, fourni dans ce dossier). C'est la seule brique non disponible « prête à l'emploi » gratuitement. |
| **Machine d'états avec gates et autorisations propriétaire** | Oui, code fourni (`metaalpha/governance.py`). Sceptre Holdout implémentable réellement (scellement cryptographique). |
| **Un LLM de supervision à coût quasi nul** | Oui : DeepSeek V3 ≈ 0,14 $/M entrée, 0,28 $/M sortie ; un cycle complet de phase coûte **moins de 40 FCFA**. Alternative gratuite : Gemini Flash free tier / NVIDIA NIM. |
| **Préparer le robot MQL5** | Oui (Phase 9 = spécification + traduction mécanique), mais **pas** la promesse de parité ni le déploiement réel. |

## 2. Ce qui n'est PAS possible ou PAS garanti

| Impossible / non garanti | Pourquoi (vérifié, sources en §2) |
|---|---|
| **Un service 24 h/24 garanti et gratuit** | Colab gratuit : session ≤ 12 h, déconnexion à l'inactivité, **exécution en arrière-plan non disponible** (réservée à Pro+). Kaggle : ≤ 12 h, quota GPU hebdomadaire, notebooks interactifs coupés à l'inactivité. GitHub Actions : job ≤ 6 h, runner éphémère, disque perdu. **Aucun de ces trois n'est un serveur permanent.** |
| **Tenir 10 h de conception + déploiement + 24 h de calcul avec 0 humain devant l'écran** | Non. Il faut soit une VM always-free (Oracle, non fiable en capacité ARM : « Out of Capacity » fréquent), soit un déclenchement/relance manuel ou par webhook entre les segments. Le modèle honnête est **« travail par segments de 4 h relancés automatiquement ou par un clic »**, pas « daemon permanent gratuit ». |
| **GPU utile pour ce projet** | Non. Le goulot est l'I/O Parquet + agrégations colonnaires, pas le calcul matriciel dense. DuckDB/Polars sur CPU saturent le débit disque. **Un GPU n'accélérerait rien** ; il compliquerait et coûterait. Kaggle GPU est même un choix *inférieur* ici (moins de RAM CPU exploitable, quota). |
| **Une IA qui « trouve » les edges** | Non et ce serait contraire au kit. L'IA ne fait que **lire, vérifier, résumer, signaler**. Toute formule vient d'un registre humain. |
| **Dépassement budgétaire automatique** | Évitable, mais uniquement par des garde-fous actifs (`BUDGET_CAP`, clés API sans facturation, quotas). Détail §3. |
| **Garantie que les ressources gratuites le restent** | Non. Exemple concret et récent : Oracle a **réduit** son Always Free ARM de 4 OCPU/24 Go à 2 OCPU/12 Go en 2026 ; Hugging Face exige désormais un plan payant pour créer un Space Docker ; Colab a **supprimé** l'exécution planifiée en mars 2026. Toute architecture doit supposer que le gratuit est révocable. |

## 3. Architecture recommandée (résumé)

> **« Segmented Research Engine »** — un moteur de calcul reprenable, exécuté par segments courts sur des runtimes gratuits interchangeables, piloté par GitHub Actions, avec un LLM en *superviseur non décisionnaire*.

Trois principes non négociables :

1. **Le calcul mathématique ne dépend jamais d'un LLM.** Le LLM ne peut ni créer une formule, ni changer un seuil, ni ouvrir le Holdout, ni promouvoir un edge.
2. **Le moteur est sans état local.** Tout état vit sur Drive (checkpoints, leases, manifests). N'importe quel runtime peut reprendre n'importe quel segment. C'est ce qui rend la fermeture d'une session Colab **sans effet** sur le travail.
3. **Le travail est découpé en unités ≤ 4 h**, ce qui est en dessous du plancher de tous les quotas gratuits (12 h Colab, 12 h Kaggle, 6 h Actions). La contrainte « 6 h max Actions » devient un atout : elle force le découpage.

**Rôle des outils retenus :**

| Outil | Rôle exact | Pourquoi lui |
|---|---|---|
| **DuckDB + Parquet + PyArrow** | Moteur analytique unique, in-process, out-of-core | Déjà la référence des certificats hérités ; zéro risque de rupture de sémantique ; spill disque ; multi-thread |
| **Polars** | Transformations de features par partition uniquement | Plus rapide que DuckDB sur les expressions colonnaires par bloc ; jamais sur 685 M lignes d'un coup |
| **Python stdlib + `fcntl`/verrou Drive** | Orchestrateur maison | Prefect/Airflow/Dagster = serveur + DB + RAM, incompatible avec runners éphémères. GitHub Actions n'orchestre que le *démarrage*, pas l'état |
| **GitHub** | Version, revue, CI, déclenchement, journal des runs | Gratuit, traçable, adapté au contrat « une phase = une livraison » |
| **GitHub Actions** | *Démarreur* + *garde-fous* + *rapports* — **jamais** moteur de calcul long | 6 h/job, minutes gratuites limitées en privé → usage : lancer, tester, notifier |
| **Google Drive** | Vérité persistante : corpus, artefacts, checkpoints, leases | Déjà là, déjà certifié, déjà la cible des livrables |
| **Colab / Kaggle** | Calculateurs interchangeables pour les segments longs | Gratuits, RAM correcte (12–30 Go), CPU multi-cœur |
| **DeepSeek V3 (ou Gemini Flash free)** | Superviseur : lecture de rapports, détection d'incohérences, rédaction | Coût par phase < 40 FCFA |
| **GitHub Issues + e-mail + webhook** | Notification d'échec et rapport | Gratuit, zéro serveur |

## 4. Budget détaillé

Conversion : **6 000 FCFA = 9,15 EUR ≈ 9,95 USD** (1 EUR = 655,957 XOF fixe ; 1 USD ≈ 0,92 EUR).

| Poste | Mise en place | Mensuel | Variable | Plafond |
|---|---|---|---|---|
| GitHub Free (code + Actions) | 0 | 0 | 0 (public) / 2 000 min privé | 0 FCFA |
| Google Drive (déjà utilisé) | 0 | 0 | 0 (15 Go existants) | 0 FCFA |
| Colab gratuit | 0 | 0 | 0 | 0 FCFA |
| Kaggle gratuit | 0 | 0 | 0 | 0 FCFA |
| DuckDB / Polars / Python | 0 | 0 | 0 | 0 FCFA |
| DeepSeek V3 (superviseur) | 0 | ~0 | ~0,05–0,35 USD/mois | **plafond dur 5 USD** |
| **Total infra** | **0 FCFA** | **0 FCFA** | **0–320 FCFA/mois** | — |
| **Réserve d'accélération** (optionnelle) | — | — | Colab Pro 1 mois 9,20 € ≈ 6 034 FCFA | **HORS budget : à ne pas activer** |
| **Reliquat engagement (IA) sur 12 mois** | — | 320 FCFA × 12 ≈ 3 840 FCFA | — | **< 6 000 FCFA ✔** |

**Coût initial réel : 0 FCFA.** Les 6 000 FCFA ne servent **pas** à louer du calcul : ils constituent une **réserve d'IA et d'imprévus** qui finance ~12 mois de supervision LLM. C'est le meilleur usage de 9,15 EUR dans ce projet, parce que le calcul nécessaire est déjà gratuit.

**Coût par exécution :**
- Segment de 4 h sur Colab/Kaggle : **0 FCFA**.
- Cycle de supervision IA d'une phase (≈ 3 appels de 60 K entrée / 6 K sortie) : ≈ 0,008 USD ≈ **5 FCFA**.
- Phase complète (≈ 8 cycles) : ≈ **40 FCFA**.

**Coût d'une interruption et d'une reprise :**
- Interruption d'un segment : perte ≤ 1 unité de checkpoint. Unités calibrées à ≤ 10 min → **perte ≤ 10 min de calcul, 0 FCFA**.
- Reprise : relance = 1 requête Drive + 1 job. **Coût monétaire 0 FCFA** ; coût humain ≈ 1 clic (ou automatique si le watchdog est actif).
- Interruption définitive de Colab (compte suspendu) : bascule Kaggle = **0 FCFA**, le moteur ne voit pas la différence (même image, même état Drive).

**Risques de dépassement et parade :**

| Risque | Parade implémentée |
|---|---|
| Clé API LLM qui part en boucle | `BUDGET_CAP_USD` dans `config/execution_config.json` + compteur persistant sur Drive ; au-delà → arrêt, bascule sur mode `NO_LLM` |
| GitHub privé qui dépasse 2 000 min | Workflows limités à ≤ 10 min ; usage public ou passage en `workflow_dispatch` uniquement |
| Colab Pro activé par erreur | Aucune carte enregistrée dans le compte de service ; règle : pas de moyen de paiement attaché |
| Oracle/VM payante activée | Non retenu dans l'architecture recommandée (voir §3) |

## 5. Délai réel de déploiement

| Périmètre | Durée réaliste | Confiance |
|---|---|---|
| Infrastructure + moteur + tests sur échantillon (Étapes 1–7) | **8 h 30** | Élevée |
| Benchmark réel + première exécution contrôlée (Étapes 8–9) | **+ 1 h 30** | Moyenne (dépend du débit Drive réel) |
| **Total pour un système validé techniquement** | **≈ 10 h** | Réaliste, mais **à condition d'avoir accès à la racine Drive et aux 348 partitions dès la 1ʳᵉ heure** |
| Première phase scientifique réellement complète (Phase 2 analytique) | **+ 1 à 4 jours** de temps machine segmenté | Non garantie : dépend du débit mesuré et du volume d'écritures |
| Découverte d'un edge | **Non planifiable.** Résultat `NO_EDGE` parfaitement acceptable | — |

**Le risque n° 1 sur le délai de 10 h n'est pas la technique, c'est l'accès aux données.** Voir §11.

---

# 1. AUDIT DOCUMENTAIRE — CE QUI EST ÉTABLI VS CE QUI EST SEULEMENT ÉVOQUÉ

## 1.1 Ressources **confirmées** (attestées par certificat, avec hash à vérifier)

| Élément | Statut | Ce que ça autorise |
|---|---|---|
| Source primaire XAUUSD Dukascopy BI5 Bid/Ask | `CERTIFIED` (P1) | Lecture seule. 11 136 fichiers, 685 118 625 ticks |
| DGP Base chronologique V5R10 | `CERTIFIED` (P2) | Lecture seule. 348 partitions, 685 118 625 lignes, 2010-01-04 → 2026-09-30 |
| Validation Mid / spread / ordre chronologique | `PASS` (auto-déclaré) | Base de travail fiable **pour les contrôles déclarés** |
| Absence de données synthétiques / interpolation / OHLC | `false` (auto-déclaré) | Interdit toute reconstruction ; interdit toute réintroduction |
| Out-of-core, DuckDB primaire, reprise | `true` | La même pile technique est confirmée opérationnelle sur ce corpus |

## 1.2 Ressources **évoquées mais non prouvées** — traitées comme NON ACQUISES

| Élément | Traitement correct dans l'architecture |
|---|---|
| SHA-256 des certificats | **Non fournis dans le document.** Le moteur les calcule au préflight et les gèle dans `EXECUTION_BASELINE_V1.json` — c'est la 1ʳᵉ action de la Phase 2 |
| Schéma réel des 348 partitions (colonnes, types, taille fichier) | **Inconnu.** Ne doit pas être supposé. Le préflight le *mesure* et le consigne |
| Taille totale du corpus sur disque | **Inconnue.** Détermine la faisabilité des copies locales → à mesurer |
| Historique Oracle/RAF (80 % S3 / 20 % G4, S3 non nul 104/104) | **Explicitement hors périmètre.** Ne pas importer, ne pas reconstruire. Reste archivé |
| `PHASE_CONTROL_STATE.json` | À charger s'il existe, sans importer d'ancien état analytique |
| Kit `..._KIT_v1.1.0.zip` (20+ contrats) | **Non fourni dans cette session.** Les contrats de phase cités ici sont dérivés du dossier maître ; les gates définitifs doivent être relus dans le ZIP |
| Politique propriétaire (`OWNER_POLICY_REQUIRED`) : seuils, coûts, latence, swap, multiplicité | **Absente.** ⇒ toute promotion économique est `BLOCKED_POLICY_REQUIRED`. Le système tourne quand même, en mode descriptif |
| Les 19 familles scientifiques non définies | Restent à définir **par le propriétaire**, jamais par le LLM |

## 1.3 Contraintes fortes déduites du document (et leur traduction en code)

| Contrainte du doc | Traduction technique obligatoire |
|---|---|
| §2.1 une phase à la fois, arrêt et revue | La machine à états refuse toute transition non autorisée ; `phase_gate.py` ne peut pas ouvrir P3 sans `owner_approval` signé |
| §2.4 ne pas inventer de seuils économiques | `PolicyMissingError` levée si un seuil est requis et absent → statut `BLOCKED_POLICY_REQUIRED` |
| §5.5 DuckDB in-process, jamais 685 M en RAM | `STREAM_UNIT` : lecture par partition, agrégation, écriture ; garde-fou mémoire dur |
| §7.1 split 60/20/20 en durée calendaire | Calculé depuis `timestamp_min`/`timestamp_max` certifiés, gelé dans `VALIDATION_SPLITS_V1.json` avant tout mining |
| §7.2 purge/embarqué basée sur horizon temporel réel | `purge = max(H_label, H_détention, H_exécution)` en **secondes**, jamais en lignes |
| §7.3 Holdout scellé jusqu'à P8 | Scellement cryptographique (clé hors Drive) — voir §8.7 |
| §15.2 statuts terminaux | Enum fermé, aucune autre valeur acceptée par le code |
| §15.3 3 tentatives max, reprise unitaire | `retry: 3` dans la config ; checkpoint lié au triplet (entrée, code, config) |

## 1.4 Ce que les certificats ne prouvent PAS (rappel, inchangé)

Aucun edge, aucune causalité de variable, aucune survie à l'OOS, aucun coût réel, aucune parité MQL5. **Le moteur que je propose ne prétend rien de tout cela : il est conçu pour tenter de le démontrer et pour accepter l'échec.**

---

# 2. RECHERCHE TECHNOLOGIQUE — ÉTAT VÉRIFIÉ DES OFFRES (novembre 2026)

> Toutes les valeurs ci-dessous ont été vérifiées par recherche web le 13/11/2026. **Elles changent.** Chaque ligne indique le point de vigilance opérationnel. Vérifiez vos propres quotas dans la console avant de vous engager.

## 2.1 Google Colab (gratuit)

| Dimension | Valeur constatée 2026 | Conséquence pour nous |
|---|---|---|
| Durée de session | ≤ 12 h | Un segment de 4 h passe sans risque |
| Déconnexion inactivité | ~90 min (non publié officiellement) | **Rédhibitoire pour un job non supervisé** si vous comptez sur l'onglet |
| Exécution en arrière-plan / terminal | **Non disponible en gratuit** (Pro+ uniquement) | Ne jamais concevoir « je lance et je ferme l'onglet » |
| Mémoire | ~12–13 Go (mesures utilisateurs, non publié) | Suffisant pour 1 partition à la fois + agrégats |
| GPU T4 | 15–30 h/semaine **dynamique, non garanti**, indisponible en heure de pointe | **Inutile ici** — voir §7.4 |
| Exécution planifiée | **Supprimée en mars 2026** | Ce n'est pas un ordonnanceur |
| Drive | Montage natif `/content/drive` | Point d'entrée des données |

**Verdict :** excellent *calculateur*, mauvais *ordonnanceur*, mauvais *service permanent*. Utilisable uniquement en mode « segment court + checkpoint Drive ».

## 2.2 Kaggle Notebooks (gratuit)

| Dimension | Valeur constatée | Conséquence |
|---|---|---|
| Session | ≤ 12 h CPU/GPU (9 h TPU) | OK pour segments courts |
| RAM | **~30 Go CPU**, 29 Go avec GPU | **Meilleur que Colab** pour nos scans |
| CPU | 4 cœurs | Débit DuckDB correct |
| Disque persistant | 20 Go `/kaggle/working` | Ne suffit pas pour le corpus → Drive obligatoire |
| « Save & Run All » | Continue même onglet fermé, dans la limite 12 h | **Utile** : le meilleur mode pour un segment |
| Planification | Quotidienne/hebdomadaire possible | Le seul runtime gratuit avec un vrai déclencheur |
| GPU | P100 retiré sept. 2026 ; 2×T4 ; quota ~30 h/sem | Sans intérêt pour ce projet |
| Drive | Pas natif — nécessite montage manuel / upload dataset | Frottement d'intégration |

**Verdict :** **meilleur calculateur gratuit** (RAM + planification + Save&RunAll). C'est le runtime recommandé pour les segments longs, Colab en secours.

## 2.3 GitHub + GitHub Actions

| Dimension | Valeur constatée | Conséquence |
|---|---|---|
| Minutes privées (Free) | 2 000 min/mois | Un workflow de 10 min × 60 runs = 600 min → OK |
| Dépôt public | Illimité | Recommandé **si** aucun secret/donnée n'y est commité (jamais) |
| Durée max d'un job | **6 h** (5 jours self-hosted) | Plancher de découpage : **≤ 4 h** |
| Timeout workflow | 35 jours | Non bloquant |
| Concurrence Free | 20 jobs | Le verrou anti-concurrence doit être **applicatif** (voir §8.4) |
| Stockage artefacts | 500 Mo (Free), cache 10 Go/dépôt | **Ne jamais** y stocker le corpus ni des Parquet volumineux → Drive |
| Cron minimum | 5 min | Suffisant pour un watchdog toutes les 30 min |
| Runners | Éphémères, disque perdu | **Ce n'est pas un serveur.** Uniquement démarrage + vérification |

**Verdict :** parfait pour la **gouvernance** (revue, CI, tests, déclenchement, rapports, journal). Inadapté au calcul long.

## 2.4 Cloudflare

| Service | Gratuit | Pertinence réelle ici |
|---|---|---|
| Workers | 100 000 req/j, **10 ms CPU**/req, cron 5 max | 10 ms CPU ⇒ **impossible** de faire du calcul. Utile seulement comme **endpoint webhook** d'alerte ou mini-API de statut (lecture d'un JSON sur R2) |
| R2 | 10 Go, egress gratuit | Stockage de **rapports/artefacts légers** possible, mais Drive le fait déjà. Aucun gain |
| Durable Objects (SQLite) | 100 k req/j, 13 000 GB-s/j | Le **seul verrou distribué gratuit et fiable** (voir §8.4, option B) |
| Cron Triggers | 5 par compte | Déclencheur de secours |

**Verdict :** **pas un moteur de calcul.** Un seul usage justifié : verrou distribué (Durable Object) + endpoint de veille. **Optionnel** — le verrou fichier sur Drive suffit et évite une dépendance.

## 2.5 NVIDIA

| Offre | Réalité 2026 | Pertinence |
|---|---|---|
| build.nvidia.com / NIM API | ~1 000 crédits à l'inscription (jusqu'à 5 000 sur demande), ~40 req/min, pas de carte bancaire, API OpenAI-compatible | **Alternative LLM gratuite crédible** pour le superviseur |
| GPU Colab/Kaggle | T4/P100 | Inutile pour ce projet |
| NIM self-hosted | nécessite GPU (payant ou local) | Hors budget |

**Verdict :** NVIDIA = **fournisseur de LLM gratuit de secours**, pas un accélérateur de notre charge de travail.

## 2.6 Hugging Face

| Dimension | Réalité 2026 | Conséquence |
|---|---|---|
| Spaces Docker / Gradio | **Plan payant requis pour créer** | Ne pas compter dessus pour héberger un worker |
| CPU Basic 2 vCPU / 16 Go | existe, mais création de Space compute = payant | À écarter |
| Sleep 48 h sans visiteur | — | Pas un service permanent |
| Inference credits | 0,10 $/mois (Free) | Insuffisant comme API principale |

**Verdict :** **écarté** de l'architecture. Mentionné pour que personne ne le propose comme « serveur gratuit » : ce n'est plus vrai en 2026.

## 2.7 Oracle Cloud Always Free (et autres VM « always free »)

| Dimension | Réalité 2026 | Conséquence |
|---|---|---|
| ARM Ampere A1 | **réduit à 2 OCPU / 12 Go** en 2026 (était 4/24) | Encore suffisant pour un worker 24/7 |
| Récupération des instances inactives | **oui, sur 7 jours** (CPU P95 < 20 %, réseau < 20 %, mémoire < 20 %) | Un worker qui attend un job est « inactif » ⇒ risque réel de récupération |
| Capacité ARM | « Out of Capacity » fréquent selon région | Provisioning non garanti |
| Carte bancaire | **exigée** à l'inscription (vérification) | Risque de dépassement si mal configuré |

**Verdict :** c'est **la seule façon d'obtenir un vrai 24 h/24 à coût nul**, mais elle est (a) non garantie, (b) soumise à récupération, (c) exige une carte. Je la classe **Option B du plan d'exploitation**, pas dans l'architecture de base. Détails §8.1.

## 2.8 APIs LLM — comparatif coût réel pour notre usage

| Fournisseur | Tarif (vérifié) | Gratuit ? | Notre usage |
|---|---|---|---|
| **DeepSeek V3** | 0,14 $/M in (0,014 cache), 0,28 $/M out | Non (mais très bas) | **Recommandé** : ~40 FCFA/phase |
| Gemini Flash / Flash-Lite | free tier plafonné (quotas publiés variables, ~20–1 500 req/j selon modèle/projet) | Oui, plafonné | **Recommandé en 1ᵉʳ recours** (gratuit) |
| NVIDIA NIM | ~1 000 crédits, 40 req/min | Oui, plafonné | Secours |
| OpenRouter `:free` | 20 req/min, **50 req/j** (1 000 si ≥ 10 $ achetés une fois) | Oui, très plafonné | Secours ponctuel |
| Modèle local (llama.cpp/Ollama) | 0 $ | Oui | Sur l'Option B (VM 12 Go) uniquement |
| GPT/Claude premium | 100× le coût DeepSeek | Non | **Exclu** par le budget |

## 2.9 Orchestration Python open source — pourquoi aucune ne convient telle quelle

| Solution | Verdict pour ce projet |
|---|---|
| **Airflow** | Serveur + metadata DB + scheduler + webserver. RAM ≥ 2–4 Go permanente. **Incompatible** avec runners éphémères et budget 0 |
| **Prefect / Dagster** | Mieux, mais l'UI/agent suppose un processus résident (Cloud gratuit mais dépendance externe + données qui sortent) |
| **Celery + Redis** | Broker à héberger = serveur permanent. Non |
| **Luigi** | Dépend d'un démon central, mêmes limites |
| **Snakemake / Make** | Excellents pour la reproductibilité **fichier → fichier**, insuffisants pour leases, budgets, gates propriétaire |
| **GitHub Actions seul** | Ordonne des *runs*, pas des *unités* ; pas d'état ; 6 h max |
| **Orchestrateur maison (retenu)** | ~600 lignes : DAG déclaratif + lease Drive + checkpoints hashés + budget + reprise ciblée. **Zéro dépendance, zéro serveur, zéro coût** |

**Distinction exigée par le cahier des charges, explicitement respectée :**
- **Orchestrateur de calcul** = le DAG Python (`metaalpha/orchestrator.py`). Déterministe, sans IA.
- **Agent LLM** = couche optionnelle de *revue* (`metaalpha/ai_supervisor.py`). Ne peut pas créer de tâche de calcul, ne peut pas modifier un artefact.
- **Aucune opération mathématique ne passe par le LLM.** Zéro exception.

---

# 3. TROIS ARCHITECTURES COMPARÉES

## 3.1 Architecture A — Entièrement gratuite, « best effort » (0 FCFA)

```
GitHub (code, CI, issues)  ──dispatch──►  Colab/Kaggle (segments 4 h)
        ▲                                        │
        │                              écrit/lit  │
        └──────── rapports ◄──────── Google Drive ┘
                          (corpus, checkpoints, leases, artefacts)
              LLM : Gemini Flash free / NVIDIA NIM / aucun
```

| Critère | Note |
|---|---|
| Coût | **0 FCFA** |
| Performance | Débit identique aux autres (le CPU ne change pas) |
| Simplicité | Moyenne (mais code fourni) |
| Fiabilité | Moyenne : dépend d'un déclenchement humain ou d'un cron GitHub toutes les 30 min |
| Autonomie | **Partielle** : pas de 24/24 garanti ; reprend après relance |
| Reproductibilité | **Excellente** (hashs + DAG déclaratif) |
| Sécurité | Bonne (secrets dans Actions/Colab Secrets) |
| Reprise | Excellente (checkpoints Drive) |

## 3.2 Architecture B — Hybride, petit budget (recommandée)

Architecture A **+ un worker always-free sur Oracle Cloud ARM (2 OCPU/12 Go)** qui exécute les segments dès qu'un job apparaît, **et** conserve Colab/Kaggle pour les segments lourds.

| Critère | Note |
|---|---|
| Coût | 0 FCFA en régime établi ; carte requise pour l'inscription (aucun débit) |
| Autonomie | **Élevée** : le worker poll toutes les 5 min ⇒ vrai enchaînement des phases autorisées |
| Fiabilité | Bonne mais non garantie (récupération d'inactivité ⇒ parade : heartbeat + cron `nice` qui consomme un peu de CPU, et le worker se recrée) |
| Risque budget | Faible si **aucune ressource payante** n'est créée ; risque = erreur de configuration. Parade : compte séparé, pas d'upgrade |
| Complexité | + 2 h de mise en place (provisioning, systemd) ; provisioning ARM parfois indisponible |

## 3.3 Architecture C — « Performante » sous 6 000 FCFA

Architecture B **+ Colab Pro 1 mois (9,20 € = 6 034 FCFA)** pour obtenir 24 h/session et l'exécution en arrière-plan.

| Critère | Note |
|---|---|
| Coût | **6 034 FCFA > 6 000 FCFA** ⇒ **dépasse le plafond de 34 FCFA.** Strictement non conforme |
| Gain réel | Sessions 24 h au lieu de 12 h, background execution. **Aucun gain de débit CPU** |
| Verdict | **Refusée.** Le gain (ne pas découper) ne vaut pas 100 % du budget et l'architecture par segments supprime déjà le besoin |

> Variante C′ sous le plafond : Colab Pro **1 mois** si vous acceptez de consommer l'intégralité du budget en un mois puis de revenir au gratuit. **Je ne la recommande pas** : elle ne finance pas la recherche, elle finance du confort.

## 3.4 Recommandation

> **Architecture B, déployée en deux temps.** On démarre sur A (0 h de dépendance externe, opérationnel en 10 h) et on ajoute le worker Oracle dès qu'il est provisionné. Si le provisioning ARM échoue (fréquent), **on reste sur A sans rien perdre** : le moteur est identique, seul le déclencheur change.

**Pourquoi B :**
1. C'est la seule qui satisfasse « automatisation continue 24 h/24 » **sans dépenser un franc**.
2. Elle sépare proprement *déclencheur* (worker/Colab/cron) et *moteur* (identique partout) : aucune dépendance à un fournisseur.
3. Elle garde 6 000 FCFA intacts pour l'IA de supervision, soit ~12 mois d'autonomie.

**Pourquoi pas C :** elle viole le plafond pour un bénéfice nul sur le débit scientifique.

---

# 4. ARCHITECTURE GLOBALE (livrable A)

## 4.1 Diagramme des composants

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         PLAN DE CONTRÔLE (gouvernance)                       │
│                                                                              │
│  GitHub repo (privé)                    GitHub Actions                       │
│  ├─ metaalpha/  (moteur)                ├─ ci.yml        (tests, lint)       │
│  ├─ config/execution_config.json        ├─ watchdog.yml  (cron 30 min)      │
│  ├─ contracts/  (gates, schémas)        ├─ phase_run.yml (dispatch manuel)   │
│  └─ docs/                               └─ notify.yml    (issue + mail)     │
│                                                                              │
│  OWNER_GATE : approbations signées (issues + fichier scellé)                 │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ dispatch / polling
┌───────────────▼──────────────────────────────────────────────────────────────┐
│                      PLAN D'EXÉCUTION (calculateurs interchangeables)        │
│                                                                              │
│   Worker Oracle ARM (opt.)      Colab (segment ≤4h)      Kaggle (≤12h)       │
│        └──────────────┬──────────────────┬───────────────────┘               │
│                       ▼                  ▼                                   │
│              ┌──────────────────────────────────┐                            │
│              │  METAALPHA ENGINE (même image)   │                            │
│              │  orchestrator → units → checkpoints│                          │
│              │  DuckDB in-process + Parquet      │                           │
│              └──────────────────────────────────┘                            │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ fsspec/GDrive + verrou lease
┌───────────────▼──────────────────────────────────────────────────────────────┐
│                    PLAN DE DONNÉES (Google Drive — vérité persistante)       │
│                                                                              │
│  META_ALPHA_XAUUSD_DGP/                                                      │
│  ├─ 00_RAW / 01_PARQUET ... (LECTURE SEULE — scellé, hashé)                  │
│  ├─ 04_CHECKPOINTS/  (certificats P1, P2 — LECTURE SEULE)                    │
│  └─ RESEARCH_V1_XAUUSD_TICK_ONLY/  (ÉCRITURE AUTORISÉE ICI SEULEMENT)        │
│       ├─ 00_GOVERNANCE/ (state, leases, approvals, budget)                   │
│       ├─ 10_REGISTRIES/ (variable, formula, trial ledger)                    │
│       ├─ 20_DERIVED/    (dérivés Parquet par phase)                          │
│       ├─ 30_RESULTS/    (par phase)                                          │
│       ├─ 40_REPORTS/    (rapports JSON/MD)                                   │
│       └─ 90_LOGS/       (logs, manifests, checksums)                         │
└──────────────────────────────────────────────────────────────────────────────┘
                │ lecture de rapports (jamais d'écriture)
┌───────────────▼──────────────────────────────────────────────────────────────┐
│                   PLAN COGNITIF (optionnel, non décisionnaire)               │
│  AI Supervisor : Gemini Flash free → NVIDIA NIM → DeepSeek (plafonné)        │
│  Rôle : lire, résumer, détecter incohérences, rédiger. AUCUN pouvoir.        │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Flux de données

```
348 partitions Parquet (Drive, lecture seule)
   │  1 unité = 1 partition (ou 1 sous-bloc de partition)
   ▼
DuckDB : SELECT colonnes utiles → agrégats/features causales
   │
   ├─► écriture .tmp sur Drive (jamais le nom final)
   ├─► validation : schéma + nombre de lignes + invariants + sha256
   ├─► publication atomique : rename .tmp → .parquet + .sha256
   └─► checkpoint unité : {input_hash, code_hash, config_hash, output_sha}
                │
                ▼
        Dérivés analytiques (20_DERIVED) → mining (P3) → validation (P4)
        → stress (P5) → qualification (P6) → portefeuille (P7) → Holdout (P8)
```

**Règles de flux inscrites dans le code :**
- Aucune lecture d'une partition écrase quoi que ce soit hors `RESEARCH_V1_*`.
- Toute écriture est **write-temp → validate → rename**. Un fichier au nom final existe ⇒ il est valide.
- Aucun `read_parquet('.../*.parquet')` global dans une unité : seule la partition de l'unité est lue.

## 4.3 Flux de contrôle

```
        ┌──────────────┐
        │ IDLE         │◄────────────────────────────┐
        └──────┬───────┘                             │ reprise
               │ owner_approval(phase)               │
               ▼                                     │
        ┌──────────────┐  gate KO    ┌───────────────┴──┐
        │ PHASE_RUNNING├────────────►│ BLOCKED_WITH_RESUME│
        └──────┬───────┘             └──────────────────┘
               │ toutes unités OK + gate criteria OK
               ▼
   ┌────────────────────────────────────────┐
   │ PHASE_COMPLETE_AWAITING_OWNER_REVIEW   │──► (aucune transition auto)
   └────────────────────────────────────────┘
               │ échec technique
               ▼
        ┌──────────────┐
        │ FAILED_TECHNICAL │  (RESUME_FROM précis obligatoire)
        └──────────────┘
```

Le Holdout est **hors de ce graphe** tant que `holdout_seal.state != UNSEALED_APPROVED` (P8 uniquement, une seule fois).

## 4.4 Rôle précis de chaque outil

| Outil | Fait | Ne fait JAMAIS |
|---|---|---|
| DuckDB | Lit/agrège/écrit Parquet out-of-core | Ne charge pas tout en RAM (limite imposée) |
| Polars | Expressions par partition | Pas de collecte globale |
| Orchestrateur maison | DAG, leases, checkpoints, retries, budget | Ne décide pas de science |
| GitHub Actions | Tests, dispatch, watchdog, notifications | **Pas de calcul > 10 min** |
| Drive | Vérité persistante | Pas de lock transactionnel natif (⇒ lease) |
| Colab/Kaggle | Calcul jetable | Pas de persistance locale |
| AI Supervisor | Revue, rédaction, alerte | **Aucune écriture** dans registres/artefacts |

---

# 5. BUDGET DÉTAILLÉ (livrable C)

## 5.1 Tableau de conversion et principe

- 1 EUR = **655,957 XOF** (parité fixe, vérifiée 12/11/2026)
- 6 000 XOF = **9,149 EUR**
- 1 USD ≈ 0,92 EUR ⇒ 6 000 XOF ≈ **9,95 USD**
- Tous les tarifs ci-dessous sont en USD/EUR ; la conversion est faite avec les taux ci-dessus.

## 5.2 Coût de mise en place

| Poste | Coût |
|---|---|
| Compte GitHub Free | 0 |
| Google Drive (déjà existant) | 0 |
| Colab / Kaggle | 0 |
| Python + DuckDB + Polars (pip) | 0 |
| DeepSeek : crédit minimum d'activation | ~1,00 USD ≈ 655 FCFA *(optionnel, non requis pour démarrer)* |
| **Total minimum de mise en place** | **0 FCFA** (ou 655 FCFA si crédit LLM prépayé) |

## 5.3 Coût mensuel prévisionnel

| Scénario | Détail | FCFA/mois |
|---|---|---|
| **S1 — 100 % gratuit** | Gemini Flash free tier (ou aucune IA) ; tout le reste gratuit | **0** |
| **S2 — gratuit + DeepSeek occasionnel** | 8 phases × 8 cycles × 6 FCFA ≈ 380 FCFA | **≈ 250–400** |
| **S3 — usage intensif** | 30 cycles/jour × 30 j × 6 FCFA | **≈ 5 400 (plafonné à 3 280 = 5 USD)** |

## 5.4 Coût par exécution (unitaire)

| Exécution | Temps | Coût |
|---|---|---|
| Préflight + vérif hash certificats | < 1 min | 0 |
| Segment de calcul 4 h (Colab/Kaggle/worker) | 4 h | **0** |
| Scan complet 348 partitions (si découpé en 12 segments) | ~48 h machine | **0** |
| Cycle de supervision IA (60 K in / 6 K out, DeepSeek V3) | ~30 s | ≈ **5 FCFA** |
| Cycle de supervision IA (Gemini Flash free) | ~30 s | **0** |
| Rapport de phase complet (8 cycles + rédaction) | ~10 min | ≈ **40 FCFA** |

## 5.5 Coût des APIs (plafonds durs)

| API | Modèle | Plafond mensuel configuré | Mécanisme |
|---|---|---|---|
| DeepSeek | `deepseek-chat` | **5,00 USD** (3 280 FCFA) | `BUDGET_CAP_USD` + compteur `90_GOVERNANCE/budget_ledger.json` sur Drive, **vérifié avant chaque appel** |
| Gemini | `flash-lite` | 0 (quota gratuit) | Retour HTTP 429 → bascule automatique |
| NVIDIA NIM | `meta/llama-*` | 0 (crédits gratuits) | 429 → bascule |
| **Aucune** | mode `NO_LLM` | 0 | Le système **fonctionne sans** (voir §6.5) |

## 5.6 Coût d'une interruption / d'une reprise

| Événement | Perte | Coût de reprise |
|---|---|---|
| Fermeture de session Colab au milieu d'une unité | ≤ 1 unité (≤ 10 min) | 0 FCFA ; 1 relance |
| Coupure réseau pendant une écriture | 0 (fichier `.tmp` jeté) | 0 FCFA ; l'unité est rejouée |
| Perte du worker Oracle | 0 | 0 FCFA ; recréation (peut échouer si capacité ARM indisponible ⇒ reste sur Colab) |
| Panne GitHub Actions | 0 | 0 FCFA ; dispatch manuel |
| Perte totale de l'état local | 0 | L'état est **sur Drive**, pas en local ⇒ reprise gratuite |
| Corruption d'un artefact publié | 0 | Détecté par `sha256` au prochain préflight ⇒ unité rejouée |

**Point clé :** le coût d'une interruption est **nul en argent**, et borné en temps à la granularité de checkpoint (10 min). C'est le résultat direct du principe « l'état vit sur Drive ».

## 5.7 Risques de dépassement et garde-fous techniques

| Risque | Probabilité | Impact | Garde-fou **implémenté** |
|---|---|---|---|
| Boucle LLM incontrôlée | Moyenne | Moyen | Cap USD + compteur persistant + `max_calls_per_run` + bascule `NO_LLM` |
| Carte attachée → facturation cloud | Faible | **Élevé** | Aucune ressource payante créée ; compte Oracle dédié sans upgrade ; checklist §9.3 |
| Dépassement minutes Actions | Faible | Faible | Workflows ≤ 10 min, `concurrency` + `timeout-minutes` |
| Stockage Drive saturé (15 Go) | Moyenne | Moyen | `09_QUOTA` : budget disque vérifié avant écriture ; artefacts compressés ; purge **interdite sur les certifiés** |
| Service gratuit supprimé | Moyenne | Moyen | Moteur identique partout ⇒ bascule runtime en < 30 min |

## 5.8 Recommandation budgétaire finale

> **Dépense recommandée : 0 FCFA pour l'infrastructure ; 0 à 655 FCFA de crédit DeepSeek prépayé (optionnel) ; 5 345 à 6 000 FCFA conservés en réserve non utilisée.**

La réserve n'est **pas** à dépenser. Elle existe pour absorber (a) une accélération ponctuelle si un benchmark montre un blocage, (b) un changement d'offre gratuite. **Aucun service payant ne doit être activé sans un `OWNER_APPROVAL` écrit dans `00_GOVERNANCE/approvals/`.**

---

# 6. PLAN DE DÉPLOIEMENT EN 10 HEURES (livrable D)

## 6.1 Tableau chronologique

| # | Travail | Durée | Résultat vérifiable | Dépend de |
|---|---|---|---|---|
| **1** | Audit ressources + création comptes + **vérification accès Drive** | 0 h 45 | `AUDIT_RESSOURCES.md` ; soit `ACCESS_OK`, soit `BLOCKED_DRIVE_PATH` | — |
| **2** | Dépôt GitHub, structure, secrets, protection de branche | 0 h 45 | `git push` OK ; Actions vert sur `ci.yml` | 1 |
| **3** | Connexion sécurisée Drive (service account ou OAuth user) | 1 h 00 | `python -m metaalpha.preflight` liste 348 partitions **sans rien écrire** | 1, 2 |
| **4** | Moteur analytique : DuckDB, unit runner, écriture atomique | 1 h 30 | `pytest -q` → 100 % vert sur fixtures | 2 |
| **5** | Orchestrateur : DAG, leases, checkpoints, retries | 1 h 30 | 2 workers concurrents ⇒ 1 seul travaille (test `test_lease_exclusion`) | 4 |
| **6** | Checkpoints + reprise + anti-boucle | 1 h 00 | kill -9 au milieu d'une unité ⇒ reprise ne rejoue que l'unité | 5 |
| **7** | Tests sur échantillon réel (1 partition) | 0 h 45 | `SAMPLE_RUN_REPORT.json` avec hashs | 3, 6 |
| **8** | **Benchmark de performance réel** | 1 h 00 | `BENCHMARK_REPORT.json` : ticks/s, RAM, disque, ETA | 7 |
| **9** | Première exécution contrôlée (Phase 2 analytique, préflight seul) | 0 h 30 | `PHASE_2_PREFLIGHT_REPORT.json` + `EXECUTION_BASELINE_V1.json` | 8 |
| | **TOTAL** | **9 h 45** | Infrastructure validée, **pas** une phase scientifique achevée | |

## 6.2 Commande par commande

### Étape 1 — Audit et accès (0 h 45)

```bash
# 1.1 Vérifier que le corpus est accessible
python -c "import os; print(os.path.exists('/content/drive/MyDrive/META_ALPHA_XAUUSD_DGP'))"

# 1.2 Créer l'arborescence de gouvernance (JAMAIS dans les dossiers certifiés)
python -m metaalpha.bootstrap --root /content/drive/MyDrive/META_ALPHA_XAUUSD_DGP

# 1.3 Vérifier les hashes des certificats hérités (lecture seule)
python -m metaalpha.preflight --verify-certificates
```

**Fichiers produits :** `00_GOVERNANCE/AUDIT_RESSOURCES.md`, `00_GOVERNANCE/CERTIFICATE_HASHES.json`
**Test de sortie :** le script affiche `348` partitions et deux hashes SHA-256. Sinon → `BLOCKED_DRIVE_PATH`.

### Étape 2 — Dépôt (0 h 45)

```bash
gh repo create meta-alpha-research --private --source=. --remote=origin
git add -A && git commit -m "chore: bootstrap META ALPHA engine v1.0"
git push -u origin main
gh secret set GDRIVE_SA_JSON < sa.json        # service account
gh secret set METAALPHA_ROOT --body "/content/drive/MyDrive/META_ALPHA_XAUUSD_DGP"
```

**Test de sortie :** `ci.yml` vert (lint + tests).
**Règle absolue :** aucun `.parquet`, aucune donnée, aucun token dans le dépôt (`.gitignore` fourni).

### Étape 3 — Drive (1 h 00)

Deux méthodes, **la première est recommandée** :

| Méthode | Quand | Sécurité |
|---|---|---|
| **A. Compte de service Google Cloud** + partage du dossier Drive avec son e-mail (rôle Lecteur sur le corpus, Éditeur sur `RESEARCH_V1_*`) | Cloud (worker Oracle, Actions) | **Meilleure** : permissions minimales, révocable, pas de mot de passe |
| **B. OAuth utilisateur** (Colab `google.colab.auth`, ou `gcloud auth`) | Colab/Kaggle uniquement | Acceptable ; le token reste en mémoire de session |

```bash
# A. Compte de service
gcloud iam service-accounts create metaalpha-runner
gcloud iam service-accounts keys create sa.json --iam-account metaalpha-runner@PROJECT.iam.gserviceaccount.com
# Puis, dans Drive : partager META_ALPHA_XAUUSD_DGP avec l'e-mail du SA
#   -> rôle "Lecteur" sur la racine (protège les certifiés)
#   -> créer RESEARCH_V1_XAUUSD_TICK_ONLY et le partager en "Éditeur"

python -m metaalpha.preflight --auth service_account --verify-access --read-only-check
```

**Interdictions inscrites dans le code :** jamais de mot de passe Google dans un script ; jamais de token dans un dépôt ; le SA n'a **pas** le droit d'écriture sur `00_RAW`, `01_PARQUET`, `04_CHECKPOINTS`.

### Étape 4 — Moteur (1 h 30)

```bash
pip install -r requirements.txt    # duckdb, polars, pyarrow, google-api-python-client, pytest
python -m pytest tests/ -q
python -m metaalpha.bench --fixture      # benchmark sur données synthétiques (contrôle des chemins de code)
```

### Étape 5 — Orchestrateur (1 h 30)

```bash
python -m metaalpha.orchestrator --dry-run --phase PHASE_2_ANALYTICAL   # affiche le DAG
python -m pytest tests/test_lease_exclusion.py -q
```

### Étape 6 — Reprise (1 h 00)

```bash
pytest tests/test_resume.py -q      # simule un kill -9 au milieu d'une unité
```

### Étape 7 — Échantillon réel (0 h 45)

```bash
python -m metaalpha.preflight --sample part_000001.parquet --out 40_REPORTS/SAMPLE_RUN_REPORT.json
```

### Étape 8 — Benchmark (1 h 00)

```bash
python -m metaalpha.bench --real --partitions 3 --out 40_REPORTS/BENCHMARK_REPORT.json
```

→ produit les **vraies** mesures. Tant que ce fichier n'existe pas, **aucune extrapolation n'est autorisée** (cf. §7).

### Étape 9 — Exécution contrôlée (0 h 30)

```bash
python -m metaalpha.orchestrator --phase PHASE_2_ANALYTICAL --stage PREFLIGHT --execute
```

Statut attendu : `PHASE_COMPLETE_AWAITING_OWNER_REVIEW` **du préflight uniquement**, pas de la phase entière.

## 6.3 Permissions et secrets

| Secret | Où | Portée | Rotation |
|---|---|---|---|
| `GDRIVE_SA_JSON` | GitHub Secrets + `/etc/metaalpha/sa.json` (worker, chmod 600) | Lecture corpus + écriture `RESEARCH_V1_*` | 90 j |
| `DEEPSEEK_API_KEY` | GitHub Secrets | Facturation plafonnée | 90 j |
| `HOLDOUT_SEAL_KEY` | **HORS Drive et HORS GitHub** (gestionnaire de mots de passe du propriétaire) | Scellement P8 | jamais |
| `NOTIFY_WEBHOOK` | GitHub Secrets | Envoi | 180 j |

## 6.4 Tests de validation (installation ≠ exécution ≠ validation scientifique)

| Niveau | Test | Preuve attendue |
|---|---|---|
| Installation | `pip install` + import | `python -c "import metaalpha"` OK |
| Exécution | 1 unité sur fixture | fichier produit + sha256 |
| **Validation technique** | 3 tests ci-dessous | **rapport avec hashs** |
| Validation scientifique | Phase 2 complète + gate | **hors des 10 h** |

Les 3 tests qui prouvent que l'infrastructure fonctionne **réellement** :
1. **Idempotence** : relancer la même unité deux fois ⇒ même sha256, aucun re-calcul (checkpoint reconnu).
2. **Exclusion** : deux processus lancent la même unité en parallèle ⇒ un seul écrit, l'autre sort en `LEASE_HELD`.
3. **Reprise** : `kill -9` au milieu ⇒ relance ⇒ **seule** l'unité incomplète est rejouée, les autres sont `SKIPPED_FROM_CHECKPOINT`.

## 6.5 Ce que les 10 h ne couvrent pas (à dire clairement)

- La Phase 2 analytique complète (registres des 19 familles, pilote de granularité, dérivés).
- Le benchmark sur les 348 partitions (seulement 3 partitions à l'étape 8).
- Toute la Phase 3 à 9.
- La politique propriétaire (`OWNER_POLICY_REQUIRED`) sans laquelle aucune promotion économique n'est possible.

---

# 7. ARCHITECTURE LOGICIELLE (livrable E)

## 7.1 Arborescence du dépôt

```
meta-alpha-research/
├── metaalpha/
│   ├── __init__.py
│   ├── config.py           # chargement + hash de la config
│   ├── fs.py               # abstraction Drive/local, écriture atomique, sha256
│   ├── leases.py           # verrou exclusif (anti double exécution)
│   ├── checkpoints.py      # checkpoint lié à (input_hash, code_hash, config_hash)
│   ├── duck.py             # connexion DuckDB bornée (RAM, threads, temp)
│   ├── units.py            # unités de travail = 1 partition
│   ├── orchestrator.py     # DAG, retries, budget, statut terminal
│   ├── governance.py       # machine à états, gates, scellement Holdout
│   ├── preflight.py        # phase 2 : hash certificats, sémantique, accès
│   ├── ai_supervisor.py    # LLM non décisionnaire (optionnel)
│   ├── registry.py         # DGP Variable / Formula / Trial Ledger
│   ├── phases/
│   │   ├── p2_analytical.py
│   │   ├── p3_mining.py        (squelette — code seulement après autorisation)
│   │   └── ...
│   └── bench.py            # benchmark réel
├── config/execution_config.json
├── contracts/ (gates, schémas JSON)
├── tests/
├── .github/workflows/{ci,watchdog,phase_run}.yml
├── requirements.txt
├── .gitignore
└── docs/00_ETUDE_INGENIERIE_META_ALPHA_V1.md
```

## 7.2 Modules et responsabilités

| Module | Responsabilité unique | Interdit |
|---|---|---|
| `fs.py` | Abstraction de stockage + écriture atomique + sha256 | Ne connaît aucune science |
| `leases.py` | Exclusion mutuelle | N'écrit pas de résultats |
| `checkpoints.py` | Décide « à refaire / à sauter » | Ne décide jamais de science |
| `duck.py` | Une seule façon d'ouvrir DuckDB, avec limites | Ne peut pas charger > `memory_limit` |
| `units.py` | 1 unité = 1 partition = 1 transaction logique | Une unité n'écrit jamais hors de son dossier |
| `orchestrator.py` | Ordre, tentatives, statut terminal | **N'ouvre jamais le Holdout** |
| `governance.py` | États, gates, scellement | Aucun contournement possible par argument CLI |
| `registry.py` | Registres versionnés | Refuse un statut sauté (cycle strict) |
| `ai_supervisor.py` | Lecture/rapport | **Aucun accès en écriture** ; reçoit un `readonly=True` |

## 7.3 Gestion des checkpoints

Unité = `(phase, unit_id, input_hash, code_hash, config_hash)`.
Un checkpoint est **valide** si et seulement si les 3 hashes correspondent. Sinon il est **invalidé** (jamais supprimé : on écrit `INVALIDATED` et on rejoue).

```json
{
  "phase": "PHASE_2_ANALYTICAL",
  "unit_id": "part_000017",
  "input_hash": "sha256:…",
  "code_hash": "sha256:…",
  "config_hash": "sha256:…",
  "output_sha": "sha256:…",
  "rows": 1971243,
  "elapsed_s": 41.2,
  "status": "VALID",
  "attempts": 1,
  "created_utc": "2026-11-13T…",
  "runtime_id": "colab-…"
}
```

## 7.4 Gestion des erreurs

| Catégorie | Exemple | Politique |
|---|---|---|
| Transitoire | timeout Drive, 429, réseau | **3 tentatives**, backoff exponentiel + jitter |
| Déterministe | schéma inattendu, NaN interdit, invariant violé | **1 tentative**, échec immédiat, `RESUME_FROM` précis |
| Gouvernance | Holdout demandé sans approbation, seuil absent | **0 tentative**, `BLOCKED_POLICY_REQUIRED` / `HOLDOUT_SEALED` |
| Budget | cap LLM atteint | Bascule `NO_LLM`, poursuite du calcul |

## 7.5 Monitoring et rapports

- `40_REPORTS/<PHASE>/<timestamp>_report.json` (machine) + `.md` (humain)
- `90_LOGS/<PHASE>/<unit_id>.log`
- `00_GOVERNANCE/state.json` : état courant, dernière unité, compteur de coût
- `00_GOVERNANCE/heartbeat.json` : écrit toutes les 60 s → le watchdog sait si le worker est vivant
- Notification : GitHub Issue automatique + e-mail (Actions) ; webhook Cloudflare optionnel

## 7.6 Ce que le code refuse de faire (garde-fous réels, pas déclaratifs)

| Situation | Comportement codé |
|---|---|
| Écrire hors de `RESEARCH_V1_*` | `PermissionError` levée par `fs.py` (allowlist de racines) |
| Lancer P3 sans approbation P2 | `PhaseTransitionError` |
| Lire le Holdout | `HoldoutSealedError` — la fonction exige une clé qui n'existe pas dans l'environnement |
| Sauter un statut de formule | `RegistryCycleError` |
| Promouvoir un edge sans politique | `PolicyMissingError` → `BLOCKED_POLICY_REQUIRED` |
| Traiter un coût inconnu comme 0 | `CostSemanticError` (un coût non fourni doit être `SCENARIO` ou bloquant) |
| Écrire un fichier sans validation | impossible : `publish()` valide puis renomme |

---

# 8. ARCHITECTURE IA (livrable F)

## 8.1 Modèle recommandé

| Rang | Modèle | Coût | Justification |
|---|---|---|---|
| 1ᵉʳ | **Gemini Flash-Lite / Flash (free tier)** | 0 | Gratuit, contexte 1 M, suffisant pour lire un rapport JSON de phase |
| 2ᵉ | **NVIDIA NIM** (build.nvidia.com) | 0 (crédits) | API OpenAI-compatible, 40 req/min |
| 3ᵉ | **DeepSeek V3** | 0,14 $/M in · 0,28 $/M out | Qualité de raisonnement supérieure, coût résiduel. **Plafonné à 5 USD/mois** |
| 4ᵉ | **Mode `NO_LLM`** | 0 | Le système complet fonctionne sans aucun LLM |

**Aucun GPU n'est requis.** Un modèle local n'aurait aucun intérêt économique : le coût d'un appel DeepSeek (5 FCFA) est inférieur au temps machine d'un modèle local mal quantifié.

## 8.2 Fonction exacte de l'IA — liste fermée

| # | L'IA FAIT | # | L'IA NE FAIT PAS |
|---|---|---|---|
| 1 | Résumer un rapport de phase en langage clair | 1 | Inventer ou modifier une formule |
| 2 | Détecter des **incohérences internes** (ex. `rows` ≠ somme des partitions) | 2 | Choisir un paramètre, une fenêtre, un seuil |
| 3 | Signaler qu'un livrable obligatoire manque | 3 | Créer une tâche de calcul |
| 4 | Rédiger le corps du rapport de revue propriétaire | 4 | Modifier un artefact, un registre, un certificat |
| 5 | Proposer des **questions** au propriétaire | 5 | Ouvrir le Holdout ou approuver une gate |
| 6 | Comparer un rapport à un contrat et pointer un écart | 6 | Qualifier un edge (`LOCKED_FOR_HOLDOUT` / `CERTIFIED`) |
| 7 | Traduire un journal d'erreur en diagnostic lisible | 7 | Décider qu'un résultat est « bon » |

## 8.3 Consommation de tokens (estimation)

| Cycle | Entrée | Sortie | Coût DeepSeek |
|---|---|---|---|
| Revue d'un rapport de phase | ~60 000 tokens (rapport + contrat) | ~6 000 | ≈ 0,0102 USD ≈ **6,7 FCFA** |
| Diagnostic d'erreur | ~8 000 | 1 500 | ≈ 0,0015 USD ≈ 1 FCFA |
| Rapport de revue propriétaire (rédaction complète) | ~30 000 | 5 000 | ≈ 0,0056 USD ≈ 3,7 FCFA |

Avec **cache de contexte** (le contrat est réutilisé à chaque appel) : entrée facturée 0,014 $/M ⇒ **−90 %** sur la partie contrat.

## 8.4 Protection contre les décisions scientifiques inventées

Quatre barrières indépendantes, toutes dans le code :

1. **Barrière de données** : le superviseur reçoit un objet en lecture seule (`ReadOnlyView`) ; il n'a pas d'identifiant d'écriture.
2. **Barrière de schéma** : sa sortie est validée par un JSON Schema strict. Un champ inconnu ⇒ rejet. Il ne peut produire que `{resume, incoherences[], manquants[], questions[]}`.
3. **Barrière de gouvernance** : aucune valeur produite par l'IA n'est lue par `governance.py`. La promotion d'un edge exige un `owner_approval` humain signé.
4. **Barrière de registre** : `registry.py` refuse toute entrée dont `created_by != "HUMAN"` pour les champs `mathematical_definition`, `parameters`, `thresholds`.

Test dédié : `tests/test_ai_has_no_write_access.py` — vérifie que le superviseur lève `PermissionError` sur toute tentative d'écriture.

## 8.5 Alternatives sans API

| Situation | Solution |
|---|---|
| Aucune API disponible | Mode `NO_LLM` : le moteur produit les rapports JSON **structurés** ; la lecture est humaine |
| Volonté de zéro dépendance réseau | `llama.cpp` + un modèle 7B Q4 sur le worker Oracle 12 Go (5–8 tok/s) — **lent mais local** |
| Coupure d'un fournisseur | Chaîne de repli automatique : Gemini → NVIDIA → DeepSeek → `NO_LLM` |

---

# 9. PLAN D'EXPLOITATION 24 h/24 (livrable H) — LES 10 QUESTIONS

> **Avertissement préalable, non négociable :** un notebook Colab gratuit **n'est pas** un service 24 h/24. Colab ne fournit ni terminal, ni exécution en arrière-plan, ni planification sur le gratuit, et déconnecte à l'inactivité. Toute architecture qui prétend le contraire est fausse. Ce qui suit décrit ce qui est **réellement** obtenable.

## Q1. Comment le système continue-t-il lorsqu'une session Colab se ferme ?

**Il ne « continue » pas dans la session : il reprend dans une autre.**

Le moteur est conçu pour que la mort brutale d'un runtime soit un événement **normal et prévu** :

1. Chaque unité dure **≤ 10 min** (paramètre `UNIT_MAX_SECONDS`). Une partition = une unité.
2. À la fin de chaque unité : écriture atomique du résultat sur Drive + checkpoint.
3. À la fermeture : l'unité en cours est perdue (≤ 10 min), son `.tmp` est jeté.
4. La relance (worker, Colab, Kaggle, Actions) lit `state.json`, voit la dernière unité `VALID`, reprend à `n+1`.
5. `recover()` balaie les `.tmp` orphelins et les marque `ABANDONED`.

**Aucune reprise manuelle de calcul :** on ne relance pas la phase, on relance le moteur qui saute ce qui est fait.

## Q2. Où le processus est-il réellement exécuté ?

| Segment | Lieu réel | Déclencheur |
|---|---|---|
| Unités courtes (< 10 min) | GitHub Actions runner (éphémère) | cron / push / dispatch |
| Unités moyennes (10 min – 4 h) | Colab (manuel/API) ou Kaggle « Save & Run All » | humain ou API |
| Unités longues (> 4 h) | Découpées en segments de ≤ 4 h | idem |
| **24/7 réel (option B)** | **Worker Oracle ARM 2 OCPU/12 Go**, `systemd` + poll 5 min | service |
| IA de supervision | API distante | appel HTTP |

**Il n'existe pas de « cloud gratuit permanent ».** La seule dalle permanente gratuite est une VM always-free (Oracle), avec ses limites (§2.7).

## Q3. Comment reprendre automatiquement une tâche interrompue ?

Trois mécanismes qui se recouvrent :

1. **Reprise intra-run** : `run_phase()` boucle sur les unités ; une exception transitoire → retry (3 max) ; une exception fatale → arrêt propre + `RESUME_FROM` écrit.
2. **Reprise inter-run (watchdog)** : cron GitHub toutes les 30 min → lit `heartbeat.json` ; si `now - heartbeat > 30 min` et `state.pending_units > 0` → redéclenche.
3. **Reprise sur nouveau runtime** : Colab/Kaggle/worker relancent la même commande ; l'état Drive rend l'opération idempotente.

## Q4. Comment empêcher deux exécutions concurrentes de modifier les mêmes résultats ?

**Verrou par bail (lease) persistant sur Drive**, avec expiry — c'est le point faible de Drive (pas de lock transactionnel natif), donc on utilise un protocole « create-if-not-exists + bail + heartbeat » :

```python
# metaalpha/leases.py (simplifié)
def acquire(name, ttl=1800):
    path = LEASES / f"{name}.lease"
    payload = {"owner": runtime_id, "expires": now() + ttl, "pid": os.getpid()}
    if fs.try_create_exclusive(path, payload):     # O_EXCL / create-if-absent
        return Lease(path, ttl)
    cur = fs.read_json(path)
    if cur["expires"] < now():                     # bail expiré → reprise autorisée
        fs.write_atomic(path, payload)
        return Lease(path, ttl)
    raise LeaseHeld(cur["owner"], cur["expires"])
```

Complété par :
- **heartbeat** renouvelé toutes les 60 s (un worker mort perd son bail en ≤ 30 min) ;
- **écriture atomique** (`.tmp` + `rename`) : même en cas de course résiduelle, le fichier final n'est jamais partiel ;
- **`concurrency:` GitHub Actions** pour éviter les doublons de workflow ;
- **test automatisé** `test_lease_exclusion.py` : 2 processus concurrents ⇒ exactement 1 exécution.

*Option renforcée :* un Durable Object Cloudflare (SQLite) comme verrou atomique véritable, si Cloudflare est activé. Non retenu par défaut (dépendance supplémentaire).

## Q5. Comment enregistrer la progression sur Google Drive ?

| Fichier | Fréquence | Contenu |
|---|---|---|
| `00_GOVERNANCE/state.json` | à chaque unité | phase, unités faites/restantes, statut terminal |
| `00_GOVERNANCE/heartbeat.json` | 60 s | `{runtime_id, utc, unit}` |
| `10_REGISTRIES/*.json`, `TRIAL_LEDGER.csv` | append-only | registres (jamais réécrits, seulement complétés) |
| `20_DERIVED/<phase>/*.parquet` | à chaque unité validée | dérivés + `.sha256` |
| `90_LOGS/<phase>/<unit>.log` | en flux | logs |
| `40_REPORTS/<phase>/*` | fin de phase | rapports |

Toute écriture : `write .tmp → validate → rename`. Un fichier final = un fichier valide.

## Q6. Comment recevoir un rapport en cas d'échec ?

- **GitHub Issue automatique** (via `actions/github-script`) : titre `[META ALPHA] FAILED_TECHNICAL — PHASE_2 — part_000123`, corps = 30 dernières lignes de log + `RESUME_FROM` + lien vers l'artefact.
- **E-mail** : notification d'Issue (gratuit, natif GitHub).
- **Option** : webhook Cloudflare Worker → Telegram/e-mail si vous préférez une alerte instantanée (0 FCFA dans le quota gratuit).

## Q7. Comment contrôler la consommation CPU, RAM et stockage ?

| Ressource | Contrôle | Implémentation |
|---|---|---|
| RAM | `memory_limit` DuckDB (ex. 4 Go) + `temp_directory` sur disque | `duck.py` refuse de démarrer sans limite explicite |
| CPU | `SET threads = N` (N = cœurs-1) | évite de saturer un runtime partagé |
| Disque | vérif d'espace libre avant chaque écriture + quota d'artefacts | `fs.check_free_space()` ; refus si < 2 Go libres |
| Drive | quota 15 Go surveillé | `state.json.disk_used_mb` ; alerte à 80 % |
| Temps | `UNIT_MAX_SECONDS` + `--max-runtime` | arrêt propre avant la limite du runtime (ex. 3 h 40 pour un plafond de 4 h) |
| Coût LLM | compteur USD persistant | `budget_ledger.json` vérifié **avant** l'appel |

## Q8. Comment empêcher les dépassements financiers ?

Cinq verrous cumulatifs :
1. **Aucun moyen de paiement** attaché aux comptes de calcul (Colab/Kaggle/Actions gratuits).
2. `BUDGET_CAP_USD = 5.00` en dur dans `execution_config.json` ; compteur persistant sur Drive.
3. `max_llm_calls_per_run = 20` ; `max_output_tokens = 4000`.
4. Bascule automatique `NO_LLM` au plafond — **le calcul continue**.
5. Règle de gouvernance : toute activation d'un service payant exige un fichier `00_GOVERNANCE/approvals/PAYMENT_APPROVED_<date>.json` signé ; **sans lui, les workflows refusent de démarrer** (`guard_cost_policy.py`).

## Q9. Comment redémarrer le système après une panne ?

| Panne | Détection | Redémarrage |
|---|---|---|
| Runtime tué | heartbeat périmé | watchdog → nouveau run (auto) |
| Worker Oracle arrêté | absence de heartbeat | `systemctl restart` ou recréation de l'instance |
| Instance Oracle récupérée (inactivité) | absence de heartbeat | recréation + restitution du disque (état sur Drive ⇒ rien à restaurer) |
| Actions indisponible | issue « no run » | dispatch manuel (1 clic) |
| Drive indisponible | exceptions transitoires | retries 3×, puis `BLOCKED_WITH_RESUME` |
| Corruption d'artefact | `sha256` au préflight | unité rejouée automatiquement |

**Règle d'or :** l'état ne vit jamais sur le runtime. Un runtime mort est un incident **sans** impact sur les données.

## Q10. Comment assurer une surveillance permanente sans payer un serveur coûteux ?

| Solution | Coût | Fiabilité | Reco |
|---|---|---|---|
| **Cron GitHub Actions (30 min)** | 0 (2 000 min/mois en privé : un cron de 1 min × 48/j = 1 440 min ⇒ **choisir 30 min et un job de < 60 s**) | Bonne | **Retenu (base)** |
| Worker Oracle ARM (poll 5 min) | 0 | Bonne mais révocable | **Retenu (option B)** |
| Cloudflare Worker cron + lecture état R2 | 0 | Bonne | Optionnel |
| UptimeRobot / ping externe | 0 | Correct | Optionnel |
| VPS payant 3–5 €/mois | 2 000–3 300 FCFA/mois | Excellente | **Refusé** (budget) |

> ⚠️ **Piège arithmétique à éviter :** un cron GitHub toutes les 5 minutes = 288 jobs/jour. Même à 1 min par job, cela consomme 8 640 min/mois **dans un dépôt privé** — largement au-delà des 2 000 min gratuites. **Recommandation : cron toutes les 30 min, job < 60 s, ou dépôt public (minutes illimitées, aucun secret dans le code).**

## 9.11 Synthèse honnête sur le 24/24

| Niveau d'automatisation | Atteignable gratuitement ? | Ce qu'il faut accepter |
|---|---|---|
| Aucune intervention pendant un segment de 4 h | **Oui** (Kaggle Save&RunAll, ou Colab lancé) | Lancer le segment |
| Enchaînement automatique des unités dans une phase | **Oui** (orchestrateur) | — |
| Reprise automatique après coupure | **Oui** (watchdog 30 min) | Latence de reprise ≤ 30 min |
| Enchaînement de plusieurs **phases** | **Non** — et c'est voulu | Revue propriétaire obligatoire (§2.1 du kit) |
| Service 24/24 garanti par SLA | **Non, avec 0 FCFA** | Option B (VM always-free, non garantie) ou VPS payant |

**Le projet n'a d'ailleurs pas besoin d'un 24/24 permanent** : il a besoin d'un moteur qui, **quand on le lance**, ne perde jamais de travail et ne se trompe jamais sur l'état. C'est précisément ce que le découpage par segments garantit, et c'est plus important que l'uptime.

---

# 10. PLAN DE CALCUL (livrable G)

## 10.1 Faut-il un GPU ? — Réponse argumentée

**Non. Un GPU n'apporte aucun gain à ce projet, et en coûte.**

| Charge de travail réelle | GPU utile ? | Pourquoi |
|---|---|---|
| Scan de 685 M lignes Parquet, colonnes timestamp/bid/ask | Non | Débit limité par l'I/O et le décodage colonnaire, pas par le FLOPs |
| Agrégations roulantes, quantiles, corrélations par bucket | Non | DuckDB/Polars vectorisent déjà sur CPU ; le temps part en mémoire et en I/O |
| Walk-forward sur ~10⁴–10⁶ trades | Non | Charge ridicule (quelques secondes CPU) |
| Tests de randomisation / bootstrap (10⁴ rééchantillonnages) | Marginalement | CPU multi-cœur suffit ; un GPU ajoute de la complexité de transfert |
| Un éventuel modèle ML non linéaire (P3) | Peut-être | Mais ce serait un choix scientifique à pré-enregistrer, pas une nécessité d'infrastructure |

**Conclusion :** le bon moteur est **DuckDB sur CPU**, ce qui est déjà la configuration certifiée de la Phase 2 héritée. Introduire un GPU violerait la cohérence de la chaîne et n'irait pas plus vite.

## 10.2 Budget de ressources cible (par runtime)

| Ressource | Colab gratuit | Kaggle gratuit | Oracle ARM (opt.) |
|---|---|---|---|
| CPU | ~2 vCPU | 4 vCPU | 2 OCPU (4 threads) |
| RAM | ~12–13 Go | ~30 Go | 12 Go |
| Disque local | ~70–100 Go éphémère | ~20 Go persistant + scratch | 200 Go bloc (partagé) |
| Recommandation | `memory_limit=4GB`, `threads=2` | `memory_limit=8GB`, `threads=4` | `memory_limit=6GB`, `threads=4` |

**Configuration DuckDB imposée** :
```sql
SET memory_limit='8GB';
SET threads=4;
SET temp_directory='/tmp/duckdb_spill';   -- jamais sur Drive (latence réseau)
SET preserve_insertion_order=false;        -- gain mémoire sur gros scans
```

## 10.3 Le benchmark obligatoire (avant toute extrapolation)

`metaalpha/bench.py` mesure **sur vos données réelles** :

| Métrique | Méthode |
|---|---|
| Débit lecture Parquet | octets lus / s (3 partitions, colonnes réelles) |
| Ticks traités / s | lignes / s sur un agrégat représentatif |
| RAM pic | `tracemalloc` + `resource.getrusage` |
| CPU | temps process / temps mural |
| Espace temporaire | taille max de `temp_directory` |
| Temps des transformations | par étape (scan, feature, label, écriture) |
| Coût des écritures Drive | Mo/s en écriture réelle |
| Temps de validation | hash + comptage |

**Aucun chiffre de performance ne doit être publié avant que `BENCHMARK_REPORT.json` existe.** C'est une exigence du cahier des charges (§10) et une règle du projet (§2.3).

## 10.4 Faisabilité des 24 heures — analyse conditionnelle

**Ce qui est certain (arithmétique, pas benchmark) :**

- 348 partitions à traiter ⇒ si chaque partition prend **T** secondes, le temps CPU total est `348 × T`.
- Pour tenir en 24 h **en un seul flux** : `T ≤ 248 s` (4 min 08 s).
- Pour tenir en 24 h **en parallèle sur 6 segments simultanés** : `T ≤ 1 488 s` (24 min 48 s).
- Le nombre de segments simultanés gratuits disponibles : 2 notebooks Colab + 1 session Kaggle + 1 job Actions ≈ **4** en pratique.

**Ordres de grandeur (à VALIDER par le benchmark, jamais à présenter comme mesurés) :**
- Un scan analytique DuckDB d'une partition de ~2 M lignes avec 5–8 colonnes : typiquement **quelques secondes à quelques dizaines de secondes** ⇒ `T ≈ 5–60 s` est plausible.
- Si `T = 30 s` ⇒ 348 × 30 = **2,9 h** de CPU ⇒ **< 24 h sans parallélisme**.
- Le facteur limitant devient alors **la latence Drive** (lecture des 348 fichiers + écriture des dérivés), pas le calcul.

**Conclusion préliminaire (à confirmer par benchmark) :** traiter **une passe** sur le corpus en < 24 h est plausible sur l'infrastructure gratuite. En revanche :

| Étape | Faisable en 24 h ? |
|---|---|
| Préflight + hash certificats + sémantique | **Oui** (< 1 h) |
| Une passe de scan complète (features de base) | **Probable** (à confirmer) |
| Construction des 3 registres complets | **Non** — c'est un travail de spécification, pas de calcul |
| Phase 3 mining complet (baselines + contrôles négatifs + multiplicité) | **Non** — plusieurs passes sur le corpus |
| Phases 4→9 | **Non** — dépendent des résultats précédents |

**Optimisations possibles si le benchmark est défavorable :**
1. Ne lire que les colonnes utiles (projection) — gain 2–10×.
2. Ne lire que les row groups nécessaires (prédicat sur timestamp).
3. Copier temporairement les partitions sur le disque local du runtime (Drive → local) avant scan : gain souvent majeur.
4. Réduire le nombre de features par passe (une passe = un groupe de features).
5. Paralléliser sur 3–4 runtimes gratuits (segments disjoints).
6. **Coût minimal d'une accélération :** Colab Pro 1 mois = 9,20 € = **6 034 FCFA** (dépasse le budget de 34 FCFA) ; un VPS 4 vCPU/8 Go ≈ 5 €/mois = 3 280 FCFA (dans le budget, mais mensuel ⇒ épuise la réserve en < 2 mois). **Conclusion : l'accélération payante n'est pas rentable ; les optimisations logicielles le sont.**

---

# 11. PLAN SCIENTIFIQUE (livrable I)

## 11.1 Correspondance Phase du kit ↔ implémentation

| Phase | Ce que le moteur exécute | Garde-fou anti-fraude codé |
|---|---|---|
| **P2 analytique** | Préflight hashé, sémantique quote, pilote de granularité, registres, split gelé, dérivés | Refus de démarrer si hash certificat ≠ référence |
| **P3 mining** | Hypothèses préenregistrées uniquement, baselines, tests nuls, contrôles négatifs | `Trial Ledger` **append-only** ; refuse une hypothèse absente du registre ; refuse un accès Holdout |
| **P4 validation** | Probes anti-look-ahead, IS/OOS, walk-forward, replay Bid/Ask, coûts | `assert_no_future()` sur chaque feature ; fills **interdits** sur la quote du signal |
| **P5 stress** | Scénarios préenregistrés, sous-périodes, régimes, contrôles négatifs | Un scénario non préenregistré est refusé (`UnregisteredScenarioError`) |
| **P6 qualification** | Application mécanique des critères, sans nouveau tuning | Refuse toute écriture de paramètre après le gel |
| **P7 portefeuille** | Uniquement edges `LOCKED_FOR_HOLDOUT` ; sinon portefeuille inactif `NO_EDGE` | Refuse d'inventer une sleeve ; poids estimés passé seul |
| **P8 Holdout** | Ouverture unique, miroir indépendant | Clé de scellement absente de l'environnement ⇒ impossible sans action humaine |
| **P9 MQL5** | Spécification + traduction mécanique + parité | Aucune réécriture de logique autorisée ; parité testée, pas supposée |

## 11.2 Comment le data leakage est empêché (6 barrières concrètes)

1. **Séparation physique des features et des labels** : dossiers distincts (`features/`, `labels/`), jamais joints dans un même calcul de feature.
2. **Contrat de disponibilité** : chaque variable déclare `availability_ts` ; `assert_causal(df)` vérifie `feature.timestamp <= decision_timestamp`.
3. **Décalage obligatoire** : aucun label dont l'horizon dépasse la fin de l'IS n'entre dans l'IS.
4. **Purge/embargo en temps réel** : `purge_seconds = max(horizon_label, horizon_détention, horizon_exécution)` — jamais un nombre de lignes arbitraire.
5. **Split par durée calendaire** : 60/20/20 calculés sur `timestamp_min`/`timestamp_max` **certifiés**, gelés avant P3.
6. **Probes anti-look-ahead** : pour chaque feature, on rejoue le pipeline sur une fenêtre tronquée et on vérifie que la valeur à `t` est **identique**. Une différence ⇒ `LOOKAHEAD_DETECTED`.

## 11.3 Comment un edge est validé (et rejeté)

```
Candidat
  ├─ Trial Ledger complet ? ──non──► REJECTED (traçabilité)
  ├─ Causalité OK ? ───────────non──► REJECTED
  ├─ IS statistiquement significatif après multiplicité ? ──non──► REJECTED
  ├─ OOS / walk-forward stable ? ──non──► REJECTED
  ├─ Survit aux coûts (nets, scénario explicite) ? ──non──► REJECTED
  ├─ Survit au stress préenregistré ? ──non──► REJECTED
  ├─ Politique propriétaire disponible ? ──non──► DEFERRED / BLOCKED_POLICY_REQUIRED
  └─ sinon ──────────────────────────────► LOCKED_FOR_HOLDOUT
```

**Multiplicité :** le nombre total d'essais est lu depuis le Trial Ledger, et la correction (Bonferroni / Benjamini-Hochberg / White's Reality Check selon la famille) est appliquée **sur ce total**, pas sur le sous-ensemble favorable.

**Coûts :** un coût inconnu n'est jamais 0. Trois états possibles : `OBSERVED` (spread mesuré), `SCENARIO` (hypothèse explicite, étiquetée), `UNKNOWN ⇒ BLOCKED_POLICY_REQUIRED`. Le code lève `CostSemanticError` si un P&L net est calculé avec un coût `UNKNOWN`.

## 11.4 Comment le portefeuille est construit

1. Filtrer : uniquement `LOCKED_FOR_HOLDOUT`.
2. Si vide ⇒ `NO_EDGE` + `PORTFOLIO_POLICY.json` avec `{"active": false, "risk": 0}`. **Aucune stratégie inventée.**
3. Sinon : mesurer chevauchement des signaux, corrélation des rendements, co-drawdowns, concentration temporelle et par régime, turnover, contribution marginale.
4. Politique **simple et causale** : poids estimés sur le passé autorisé **seulement**, gelés avant évaluation OOS. Pas de Markowitz/HRP/Kelly full-sample.
5. Toutes les sleeves sont XAUUSD ⇒ le rapport indique explicitement « **non diversifié multi-actifs** ».

## 11.5 Comment le robot MQL5 est préparé

- `EA_SPEC.json` = traduction **mécanique** du système figé (aucune optimisation).
- Mêmes conventions Bid/Ask, mêmes timestamps, mêmes règles d'entrée/sortie/risque.
- Harnais de parité sur les mêmes quotes ordonnées ; écarts = échec.
- **`DEPLOYMENT_READINESS.json` ne vaut jamais « prêt pour le réel »** sans preuves shadow/demo séparées.

---

# 12. GOUVERNANCE ET SÉCURITÉ (points 11 et 12 du cahier des charges)

## 12.1 Machine à états et préautorisation

| Classe de tâche | Auto-exécutable ? | Condition |
|---|---|---|
| Technique déterministe (scan, hash, écriture validée) | **Oui** | Dans la phase approuvée |
| Validation déterministe (schéma, comptage, invariants) | **Oui** | Règles préenregistrées |
| Choix scientifique (formule, paramètre, seuil) | **Non** | `OWNER_APPROVAL` explicite |
| Passage de phase | **Non** | Revue + signature |
| Ouverture du Holdout | **Non, une seule fois** | Clé de scellement + approbation |
| Déploiement réel du robot | **Non** | Approbation + preuves demo/shadow |

**Mécanisme de préautorisation** : `contracts/preauthorization.yaml` liste les tâches répétitives autorisées *à l'avance* (ex. « relancer une unité échouée ≤ 3 fois »). Toute tâche non listée ⇒ `BLOCKED`.

**Gel de scellement du Holdout** (réel, pas symbolique) :
```
seal = HMAC-SHA256(key=HOLDOUT_SEAL_KEY, msg=sha256(VALIDATION_SPLITS_V1.json) || sha256(CANDIDATE_LOCK_MANIFEST.json))
```
La clé n'existe ni sur Drive ni dans le dépôt. Sans elle, `open_holdout()` lève `HoldoutSealedError`. L'ouverture écrit `HOLDOUT_UNSEALED_ONCE.json` ; une seconde tentative échoue définitivement.

## 12.2 Sécurité

| Exigence | Implémentation |
|---|---|
| Secrets séparés du code | GitHub Secrets / `/etc/metaalpha/` chmod 600 ; `.gitignore` strict |
| Tokens à permissions minimales | SA Google : Lecteur corpus / Éditeur `RESEARCH_V1_*` seulement |
| Journalisation | log par unité, append-only, UTC |
| Sauvegardes | manifestes + hashs sur Drive ; export mensuel des rapports (léger) |
| Protection des sources | allowlist d'écriture dans `fs.py` ; refus d'écriture sur P1/P2 |
| Verrouillage concurrent | lease + heartbeat + écriture atomique |
| Contrôle des écritures | validation avant rename ; `sha256` vérifié en relecture |
| Limites de dépenses | `BUDGET_CAP_USD` + ledger persistant + `guard_cost_policy.py` |
| Arrêt d'urgence | fichier `00_GOVERNANCE/KILL_SWITCH` ⇒ toute unité vérifie et s'arrête au prochain point sûr |
| Vérification des dépendances | `requirements.txt` épinglé + `pip-audit` en CI |

---

# 13. INFORMATIONS MANQUANTES (ne bloque pas l'étude, mais bloque certaines phases)

| # | Information manquante | Impact | Qui/quoi la fournit |
|---|---|---|---|
| 1 | **Accès au corpus depuis l'environnement de travail actuel** — `META_ALPHA_XAUUSD_DGP` est absent du Drive connecté (0 résultat sur `META_ALPHA`, `XAUUSD`, `PHASE_0*`) | **BLOQUANT pour l'étape 7-8** | Vous : exécuter le préflight sur le compte où se trouve le corpus |
| 2 | **SHA-256 des deux certificats** (non fournis dans le document) | Bloque le gel `EXECUTION_BASELINE_V1.json` | `preflight.py --verify-certificates` les calcule |
| 3 | **Schéma réel des partitions** (colonnes/types/taille) | Bloque la sémantique quote | mesuré par le préflight |
| 4 | **Taille totale du corpus** (Go) | Détermine la faisabilité des copies locales | mesuré |
| 5 | **Politique propriétaire** : seuils, coûts (commission/swap/latence/slippage), min trades, max DD, politique de multiplicité | **Bloque toute promotion économique** (P6+) | Vous |
| 6 | **Les 20+ contrats du kit v1.1.0** (ZIP) | Les gates définitifs doivent être relus dans le ZIP ; ce document n'en est qu'une synthèse | Vous |
| 7 | **Les 19 familles scientifiques non définies** | Bloque la complétude du Formula Registry (P2) | Vous (jamais le LLM) |
| 8 | **Timezone et règles de session** | Bloque toute feature temporelle/session (`DEFERRED`) | Vous |
| 9 | **Fuseau et convention du timestamp** dans les Parquet | Bloque l'alignement décision/exécution | mesuré + politique |
| 10 | **Broker cible et conditions d'exécution** (pour P9) | Bloque la readiness réelle | Vous |

**Aucune de ces lacunes n'empêche de livrer et valider l'infrastructure en 10 h.** Elles empêchent de prétendre qu'une phase scientifique est terminée.

---

# 14. DÉCISION FINALE (livrable J)

## 14.1 Architecture recommandée

> **Segmented Research Engine — Option B.**
> Moteur Python sans état (DuckDB + Parquet + Polars) exécuté par segments de ≤ 4 h sur des runtimes gratuits interchangeables (Kaggle > Colab > Actions), état persistant et verrou par bail sur Google Drive, gouvernance par machine à états + gates signés, LLM de supervision non décisionnaire plafonné à 5 USD, dépôt GitHub comme source de vérité du code.

## 14.2 Pourquoi c'est la meilleure option

| Critère | Pourquoi B gagne |
|---|---|
| **Coût** | 0 FCFA d'infrastructure ; 6 000 FCFA conservés |
| **Performance** | Identique à une architecture payante : le goulot est l'I/O, pas le CPU |
| **Rigueur scientifique** | Les garde-fous sont dans le code, pas dans les bonnes intentions (allowlist d'écriture, `assert_causal`, Trial Ledger append-only, scellement HMAC du Holdout) |
| **Résilience** | L'état sur Drive rend tout runtime jetable ; reprise gratuite et bornée à 10 min |
| **Réversibilité** | Aucune dépendance forte à un fournisseur : changer de runtime = changer une commande |
| **Honnêteté** | Ne promet pas de 24/24 garanti ; propose une automatisation forte là où elle est réellement obtenable |

## 14.3 Coût réel estimé

- **Infrastructure : 0 FCFA**, de façon permanente.
- **IA : 0 à 400 FCFA/mois** (plafond dur 5 USD).
- **Sur 12 mois : 0 à 4 800 FCFA** ⇒ **sous les 6 000 FCFA**, avec réserve.
- **Aucun frais variable caché** identifié.

## 14.4 Délai de mise en place

- **9 h 45** pour l'infrastructure validée (étapes 1–9).
- **+ 1 à 4 jours** de temps machine segmenté pour la première phase scientifique complète (Phase 2), sous réserve du benchmark.

## 14.5 Limites restantes — assumées

1. Pas de 24/24 garanti sans VM always-free (non garantie elle-même).
2. La latence Drive peut devenir le goulot ; à mesurer.
3. Aucune promotion économique possible avant la politique propriétaire.
4. Aucun edge démontré à ce jour — et `NO_EDGE` reste un résultat valide.
5. Le kit v1.1.0 doit être relu pour les gates définitifs ; ce document le synthétise, ne le remplace pas.
6. La parité MQL5 et la readiness live sont hors de portée de cette phase.

## 14.6 Première action à réaliser (maintenant, dans l'ordre)

```bash
# 1. Se placer sur le compte Google qui possède le corpus
# 2. Cloner le squelette livré
cd ~/META_ALPHA && pip install -r requirements.txt

# 3. Lancer le préflight — il ne modifie RIEN
python -m metaalpha.preflight --root "<RACINE_DRIVE>" --verify-certificates --verify-access
```

**Le préflight doit afficher :** 2 hashes SHA-256, `348` partitions, `timestamp_min/max`, et `PHASE_3_STARTED=false`.
**S'il affiche autre chose :** `BASELINE_PATH_CONFLICT` ou `BLOCKED_DRIVE_PATH` → on s'arrête et on corrige le chemin, conformément à §5.1 du dossier maître. On ne « choisit pas silencieusement une autre source ».

---

# 15. ANNEXES — CODAGE LIVRÉ

Voir les fichiers du dossier `META_ALPHA/` :

| Fichier | Contenu |
|---|---|
| `metaalpha/fs.py` | Stockage + écriture atomique + sha256 + allowlist |
| `metaalpha/leases.py` | Verrou par bail anti-concurrence |
| `metaalpha/checkpoints.py` | Checkpoints liés aux hashes |
| `metaalpha/duck.py` | DuckDB borné (RAM/threads/spill) |
| `metaalpha/orchestrator.py` | DAG, retries, statuts terminaux, budget |
| `metaalpha/governance.py` | Machine à états, gates, scellement Holdout |
| `metaalpha/registry.py` | Variable/Formula Registry + Trial Ledger (cycle strict) |
| `metaalpha/preflight.py` | Phase 2 préflight (lecture seule) |
| `metaalpha/ai_supervisor.py` | LLM non décisionnaire avec plafond |
| `metaalpha/bench.py` | Benchmark réel (débit, RAM, disque, ETA) |
| `config/execution_config.json` | Tous les paramètres, y compris budgets |
| `.github/workflows/*.yml` | CI, watchdog, exécution de phase |
| `tests/*` | Idempotence, exclusion, reprise, no-write IA |

**Aucun de ces fichiers ne contient de formule scientifique.** Ce sont des mécanismes. Les formules viendront des registres humains, phase par phase, comme l'exige le kit.

---


---

# ANNEXE B — BENCHMARK RÉELLEMENT EXÉCUTÉ (13/11/2026, environnement de conception)

> **Portée exacte de cette annexe.** Ces mesures ont été exécutées sur un
> environnement de conception (conteneur Linux, CPU partagé), sur des fichiers
> **synthétiques** de taille comparable à une partition réelle. **Elles ne
> mesurent pas votre corpus**, ne mesurent pas la latence Google Drive, et ne
> constituent donc **pas** le `BENCHMARK_REPORT.json` officiel du projet.
> Elles donnent un ordre de grandeur honnête et, surtout, elles valident la
> méthode de mesure.

Environnement : Python 3.13, DuckDB 2.0.0, PyArrow 26.0.1, Polars 2.1.0.

## B.1 Lecture Parquet + agrégat (2 000 000 lignes, 3 colonnes, 19,1 Mo)

| Threads | Temps | Lignes/s | Débit | RSS pic |
|---|---|---|---|---|
| 1 | 0,174 s | 11 507 772 | 110 Mo/s | 430 Mo |
| 2 | 0,108 s | 18 466 610 | 176 Mo/s | 430 Mo |
| 4 | 0,092 s | 21 673 096 | 207 Mo/s | 430 Mo |

**Lecture :** un simple scan/agrégat n'est pas le facteur limitant. 685 M de
lignes à ~20 M lignes/s ⇒ ~35 s de pur scan. Le coût réel viendra des
**fenêtres roulantes** et de l'**I/O Drive**, pas de la lecture.

## B.2 Charge réaliste : 3 fenêtres roulantes matérialisées (avg, stddev, corr sur 100 lignes)

| Threads | Temps | Ticks/s |
|---|---|---|
| 1 | 1,10 s | 1 822 963 |
| 2 | 0,66 s | **3 021 248** |
| 4 | 0,65 s | 3 059 550 |

**C'est le chiffre à retenir : ~3 M ticks/s** pour une passe de features
causales réalistes (2 threads, configuration recommandée Colab).

## B.3 Extrapolation honnête — avec intervalle, pas un chiffre unique

| Scénario | Débit retenu | 685 118 625 ticks | < 24 h ? |
|---|---|---|---|
| Une passe de features, 2 threads, sans latence Drive | 3,0 M ticks/s | **≈ 3 min 47 s** | Oui, très largement |
| Même passe, pénalité I/O Drive ×10 (hypothèse pessimiste) | 0,3 M ticks/s | **≈ 38 min** | Oui |
| Même passe, 3 features × facteur 3 | 1,0 M ticks/s | **≈ 11 min** | Oui |
| 10 passes complètes (mining P3), 2 threads | 3,0 M ticks/s | **≈ 38 min** | Oui |
| 50 passes (mining exhaustif + contrôles négatifs) | 3,0 M ticks/s | **≈ 3 h 10** | Oui |

**Conclusion mesurée :** le calcul de type « scan + features » **n'est pas** le
obstacle des 24 h. **L'obstacle réel sera :**
1. la latence de lecture des 348 fichiers depuis Drive (à mesurer sur votre compte) ;
2. le temps d'**écriture** des dérivés (dizaines de Go à travers Drive) ;
3. le travail humain de **spécification** des registres (les 19 familles), qui n'est pas du calcul.

**Donc :** oui, le corpus peut être traité en < 24 h sur l'infrastructure
gratuite — mais un benchmark sur **vos** 3 premières partitions reste
obligatoire avant de l'affirmer (étape 8 du plan).

## B.4 Piège méthodologique rencontré pendant le benchmark (à connaître)

Un premier essai de mesure des fenêtres roulantes a donné **112 M ticks/s** :
l'optimiseur de DuckDB avait **éliminé** les colonnes calculées, non utilisées
par le `COUNT(*)`. Le chiffre était faux d'un facteur 37.

**Leçon inscrite dans `bench.py` :** un benchmark doit **matérialiser** ce qu'il
prétend mesurer (checksum sur les colonnes produites), sinon il mesure le vide.
Cette erreur est exactement le type de « performance inventée » que le cahier
des charges interdit.

## B.5 Validation fonctionnelle de la chaîne (34 tests, tous verts)

| Test | Ce qu'il prouve |
|---|---|
| `test_write_denied_on_certified_base` | Écriture impossible sur `00_RAW`, `01_PARQUET`, `04_CHECKPOINTS` |
| `test_lease_exclusion` | 2 runtimes ⇒ 1 seul travaille |
| `test_expired_lease_can_be_taken` | Un worker mort ne bloque pas le système |
| `test_first_run_executes_then_second_skips_same_output` | **Idempotence** : 12/12 unités sautées au 2ᵉ passage |
| `test_changed_input_hash_forces_reexecution` | Une entrée modifiée force le recalcul |
| `test_resume_after_simulated_kill` | Reprise ciblée, aucune unité rejouée inutilement |
| `test_transient_retry_then_success` | 3 tentatives sur erreur transitoire |
| `test_deterministic_error_stops_immediately` | Pas de retry sur erreur déterministe |
| `test_holdout_single_open_and_tamper_detection` | Ouverture unique + détection de modification |
| `test_holdout_sealed_without_key` | Impossible d'ouvrir sans la clé |
| `test_unknown_cost_is_never_zero` | Un coût `UNKNOWN` bloque le calcul net |
| `test_registry_requires_human_authorship` | Une formule `created_by=LLM` est refusée |
| `test_formula_status_cannot_skip` | Cycle de statut strict |
| `test_trial_ledger_is_append_only` | Les essais négatifs sont conservés |
| `test_ai_has_no_write_access` | Le superviseur IA ne peut pas écrire |
| `test_ai_rejects_out_of_schema` | Sortie IA hors schéma rejetée |
| `test_preflight_detects_missing_certificate` | Blocage si certificat absent |
| `test_preflight_detects_wrong_partition_count` | Blocage si 12 ≠ 348 partitions |

Reproduire : `python -m pytest tests/ -q` puis `python scripts/demo_end_to_end.py`.

*Fin du document. Version 1.0 — 13 novembre 2026.*
*Ce document ne constitue ni une promesse de rentabilité, ni une preuve d'edge, ni une garantie de disponibilité des services gratuits cités.*

---

# ANNEXE C — COMMENT LANCER DES SESSIONS TEMPORAIRES SANS NAVIGATEUR

> **La question posée :** « Comment lance-t-il Colab ou les GPU alors que ce sont des sessions temporaires ? »
>
> **La réponse courte :** il ne faut **pas** lancer Colab, et il ne faut **pas** de GPU.
> On lance des **kernels Kaggle batch** depuis une ligne de commande, et c'est le
> **découpage en unités** — pas la durée de la session — qui produit le résultat.

## C.1 Le renversement de conception

L'erreur intuitive est de chercher « un endroit où le programme tourne en permanence ».
C'est le mauvais objectif : il est coûteux et fragile.

| Approche naïve | Approche retenue |
|---|---|
| Trouver une machine qui tourne 24/7 | **Rendre la session morte sans conséquence** |
| Colab ouvert, cellule qui tourne des heures | 1 partition téléchargée → calculée → publiée → supprimée |
| Si la session meurt, tout est perdu | Si la session meurt, ≤ 1 unité est perdue |
| Relancer = recommencer | Relancer = reprendre à l'unité suivante |

**Conséquence :** la durée de session cesse d'être un problème d'architecture.
Elle devient un simple paramètre de dimensionnement (`segment_minutes`).

## C.2 Pourquoi **Kaggle** et pas Colab

C'est le point technique décisif, et il n'est pas intuitif.

| Capacité | Colab gratuit | Kaggle gratuit |
|---|---|---|
| Lancer depuis une CLI, sans navigateur | **Non.** Pas d'API d'exécution publique. Le MCP officiel exige OAuth + un processus local + un navigateur pour l'autorisation, et le runtime meurt à ~90 min d'inactivité | **Oui.** `kaggle kernels push -p <dir>` **téléverse ET exécute**, puis `status` / `logs` / `output` pilotent le cycle de vie |
| Exécution quand on ferme l'onglet | Non (Pro+ seulement) | **Oui** (exécution batch, l'onglet n'existe pas) |
| Planification | Supprimée (mars 2026) | API pilotable depuis un cron |
| RAM | ~12–13 Go | **~30 Go** |
| GPU | T4, non garanti | 2×T4 / P100 — **mais inutile ici** |

**Verdict :** Colab est excellent pour explorer à la main. Pour de l'autonomie,
**Kaggle est le seul runtime gratuit réellement pilotable par programme.**
Colab reste utile comme runtime de secours lancé manuellement (2 clics), pas comme pivot.

## C.3 Le cycle complet, sans navigateur (implémenté et testé)

```
GitHub Actions (cron 30 min, job < 2 min)
        │
        │ 1. lit les checkpoints VALIDES sur Drive  ->  combien d'unités restent ?
        │ 2. plan_units() choisit le lot suivant (pur, déterministe)
        │ 3. génère un kernel jetable (main.py + kernel-metadata.json)
        │ 4. `kaggle kernels push`   <-- lance l'exécution, sans navigateur
        │ 5. `kaggle kernels status` (poll) puis `output` (rapport + logs)
        │ 6. re-lit l'état Drive ; si progrès -> segment suivant ; sinon STOP
        ▼
Kernel Kaggle jetable (max 12 h)
        │ télécharge 1 partition via l'API Drive (Drive ne peut pas être monté ici)
        │ calcule 1 unité -> publie dérivé + checkpoint sur Drive -> supprime le local
        │ recommence jusqu'à `max_units` ou `segment_minutes`
        ▼
Session détruite. Aucune conséquence.
```

**Aucune étape ne demande d'ouvrir un navigateur.** Aucune session n'a besoin de survivre.

## C.4 Pourquoi aucun GPU — argument définitif

| Question | Réponse mesurée |
|---|---|
| Le goulot est-il le calcul flottant ? | Non : lecture Parquet + fenêtres roulantes |
| Débit mesuré sans GPU | 3,0 M ticks/s (2 threads) |
| Temps théorique d'une passe sur 685 M ticks | ~3 min 47 s |
| Gain attendu d'un GPU | quasi nul (pas de produit matriciel dense) |
| Coût d'un GPU | quota hebdomadaire consommé pour rien + complexité |
| **Décision** | `enable_gpu: false` **en dur** dans le générateur de kernel |

Le dire franchement : **demander un GPU ici serait une faute d'ingénierie**, pas une
optimisation. C'est pourquoi ce n'est pas un réglage mais une valeur fixée dans le code
(`metaalpha/dispatch.py`, `build_kernel_dir`).

## C.5 Les secrets, sans jamais les écrire

| Secret | Où il vit | Comment le kernel y accède |
|---|---|---|
| `GDRIVE_SA_JSON` | Kaggle Secrets (chiffré) + GitHub Secrets | `UserSecretsClient().get_secret(...)` → variable d'environnement **en mémoire** |
| `KAGGLE_KEY` / `KAGGLE_USERNAME` | GitHub Secrets | variables d'environnement du runner |
| `HOLDOUT_SEAL_KEY` | **nulle part** dans le cloud de calcul | absent ⇒ impossible d'ouvrir le Holdout depuis un kernel |

Le kernel poussé **ne contient aucun secret** (vérifié par test : `test_kernel_script_contains_no_secret_and_no_formula`).
Il ne contient **aucune formule** non plus : il clone le dépôt à une révision épinglée
et appelle `run_segment()`. Le code de calcul reste celui revu par un humain.

## C.6 Le garde-fou qui manquait : NO_PROGRESS_STOP

En construisant la boucle, un défaut est apparu : **un segment qui ne publie rien mais
se termine « COMPLETE »** ferait repousser indéfiniment le même lot — consommation de
quota sans progrès. C'est exactement la « boucle d'audit répétitive » interdite au §15.3 du kit.

Correctif implémenté et testé (`test_autonomy_loop_stops_when_no_progress`) :
si après un segment complet le nombre d'unités validées n'a pas augmenté, la boucle
s'arrête et consigne `NO_PROGRESS_STOP`.

## C.7 Coût et limites de ce mécanisme

| Élément | Valeur |
|---|---|
| Quota consommé par cycle de dispatch | ~2 min de runner GitHub (2 000 min/mois en privé ⇒ ~960 cycles/mois théoriques) |
| Quota Kaggle consommé | temps d'exécution CPU du kernel (pas de quota GPU puisqu'aucun GPU) |
| Coût monétaire | **0 FCFA** |
| Latence de reprise après incident | ≤ 30 min (période du cron) |
| Ce qui reste manuel | (1) la première autorisation de phase ; (2) l'ouverture du Holdout ; (3) la revue de fin de phase — **et c'est voulu** |
| Ce qui reste fragile | les quotas gratuits peuvent changer ; le kernel peut être mis en file d'attente à une heure de pointe |

## C.8 Mise en service — 4 commandes

```bash
# 1. identifiants Kaggle dans le dépôt (jamais dans le code)
gh secret set KAGGLE_USERNAME --body "<pseudo>"
gh secret set KAGGLE_KEY      --body "<clé-api>"
gh secret set GDRIVE_SA_JSON  --body "$(cat sa.json)"
gh secret set GDRIVE_ROOT_FOLDER_ID --body "<id_du_dossier_Drive>"

# 2. créer le kernel privé une première fois (via UI, 1 minute, une seule fois)
#    titre : meta-alpha-segment  -> le slug doit correspondre exactement

# 3. autoriser la phase (geste propriétaire, tracé)
python -c "from metaalpha.fs import Storage; from metaalpha.governance import approve_phase; \
approve_phase(Storage.open('$METAALPHA_ROOT'), 'PHASE_2_ANALYTICAL', 'je-approuve-la-phase-2')"

# 4. laisser le cron travailler (ou déclencher à la main)
gh workflow run dispatch-segments.yml -f phase=PHASE_2_ANALYTICAL -f dry_run=false
```

Après cela, le cycle tourne seul : planification → kernel → collecte → replanification.
**Il s'arrête tout seul à la fin de la phase autorisée**, par conception.

## C.9 Ce que ce mécanisme ne fera jamais

- Il ne passera pas à la phase suivante sans signature propriétaire.
- Il n'ouvrira pas le Holdout (clé absente du runtime de calcul).
- Il ne lancera pas de GPU.
- Il ne modifiera pas une formule, un seuil ou un split.
- Il ne déclarera pas un edge qualifié.

Testé : `python -m pytest tests/test_dispatch.py tests/test_segment.py -q` (18 tests dédiés).
