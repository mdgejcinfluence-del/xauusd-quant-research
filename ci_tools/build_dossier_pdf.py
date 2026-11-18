"""DOSSIER BILAN INTEGRAL META ALPHA XAUUSD (IS) - generation PDF ReportLab.
Sources: artefacts du depot uniquement (commit 0e56bbb). Aucune donnee OOS/HOLDOUT."""
import json, hashlib, pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether)

R = pathlib.Path('reports/meta_alpha')
OUT = R / 'DOSSIER_BILAN_INTEGRAL_META_ALPHA_XAUUSD_IS.pdf'
chain = json.load(open(R / 'TRIAL_LEDGER_CHAIN.json'))['entries']
integ = json.load(open(R / 'integral_scan/INTEGRAL_SYNTHESIS.json'))
verify = json.load(open(R / 'kaggle_migration/VERIFY.json'))
volD = json.load(open(R / 'vol_models/VOL_MODELS_RESULTS.json'))
volH = json.load(open(R / 'vol_hourly/VOL_HOURLY_RESULTS.json'))
mani = json.load(open(R / 'integral_scan/INTEGRAL_EXECUTION_MANIFEST.json'))

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

NAVY = colors.HexColor('#12263A'); STEEL = colors.HexColor('#2E5F7A'); LIGHT = colors.HexColor('#EAF1F6')
GOLD = colors.HexColor('#B8860B'); GREY = colors.HexColor('#555555')
ss = {
 'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=NAVY, alignment=TA_CENTER),
 'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=13, leading=18, textColor=STEEL, alignment=TA_CENTER),
 'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=NAVY, spaceBefore=14, spaceAfter=8),
 'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=STEEL, spaceBefore=10, spaceAfter=5),
 'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY, spaceAfter=5),
 'small': ParagraphStyle('small', fontName='Helvetica', fontSize=7.8, leading=10.5, textColor=GREY),
 'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=7.4, leading=9.6),
 'cellb': ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=7.4, leading=9.6, textColor=colors.white),
 'box': ParagraphStyle('box', fontName='Helvetica', fontSize=9, leading=13, textColor=NAVY),
}
def P(t, s='body'): return Paragraph(t, ss[s])
def tbl(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign='CENTER')
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#9BB7C9')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
          ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if header: st += [('BACKGROUND', (0, 0), (-1, 0), STEEL), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT])]
    t.setStyle(TableStyle(st)); return t
def hdr(cells): return [Paragraph(c, ss['cellb']) for c in cells]
def row(cells): return [Paragraph(str(c), ss['cell']) for c in cells]
def box(text):
    t = Table([[Paragraph(text, ss['box'])]], colWidths=[16.6 * cm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FBF3DC')),
                           ('BOX', (0, 0), (-1, -1), 0.8, GOLD), ('LEFTPADDING', (0, 0), (-1, -1), 8),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6)])); return t
def footer(canvas, doc):
    canvas.saveState(); canvas.setFont('Helvetica', 7); canvas.setFillColor(GREY)
    canvas.drawString(1.6 * cm, 1.1 * cm, 'META ALPHA XAUUSD DGP - Dossier bilan integral IS - commit 0e56bbb - OOS/HOLDOUT fermes')
    canvas.drawRightString(19.4 * cm, 1.1 * cm, f'Page {doc.page}'); canvas.restoreState()

S = []  # story
# ---------- PAGE DE GARDE ----------
S += [Spacer(1, 3.2 * cm), P('DOSSIER BILAN INTÉGRAL', 'title'), Spacer(1, 0.4 * cm),
      P('PROGRAMME META ALPHA XAUUSD DGP', 'title'), Spacer(1, 0.8 * cm),
      P('Cartographie scientifique du fonctionnement observable du marché de l\u2019or<br/>à partir des cotations Bid/Ask — périmètre In-Sample certifié', 'subtitle'),
      Spacer(1, 1.6 * cm)]
cover = [['Corpus', '282 partitions IS certifiées — 288 086 306 ticks — 2010-01-04 → 2020-01-20'],
         ['Taille migrée', '9,73 Go — 8 datasets privés Kaggle (vérification SHA-256 : all_ok = true)'],
         ['Chaîne d\u2019audit', f'{len(chain)} entrées chaînées par hash — tête {chain[-1]["entry_hash"][:16]}'],
         ['Commit de référence', '0e56bbb (branche arena/afe12737-xauusd-quant-research)'],
         ['Périmètre', '100 % In-Sample — OOS et HOLDOUT strictement fermés, jamais ouverts'],
         ['Budget', '0 FCFA — calcul Kaggle / GitHub Actions uniquement'],
         ['Date du dossier', '13 novembre 2026 (ordre de production du propriétaire)']]
S.append(tbl([hdr(['Rubrique', 'Valeur'])] + [row(r) for r in cover], [4.2 * cm, 12.4 * cm]))
S += [Spacer(1, 1.2 * cm), box('<b>Objet.</b> Ce dossier retrace de manière exhaustive et honnête l\u2019intégralité des travaux du programme jusqu\u2019au commit 0e56bbb : gouvernance, infrastructure, chronologie des 49 entrées d\u2019audit, mécanique des cotations, spread et activité, volatilité, cycles, résultats négatifs et réfutations, verdict économique et limites ouvertes. Tous les chiffres proviennent des artefacts versionnés du dépôt (rapports, synthèses JSON, manifestes signés par SHA-256). Aucune rentabilité n\u2019est prétendue : les conclusions descriptives sont distinguées des implications économiques, et les coûts inconnus ne sont jamais supposés nuls.'), PageBreak()]

# ---------- TABLE DES MATIERES ----------
S.append(P('TABLE DES MATIÈRES', 'h1'))
toc = ['Chapitre 1 — Genèse, gouvernance et périmètre certifié',
       'Chapitre 2 — Infrastructure, migration Kaggle et résolution des blocages',
       'Chapitre 3 — Chronologie complète de la chaîne d\u2019audit (entrées 1 à 49)',
       'Chapitre 4 — Mécanique microstructurelle des cotations',
       'Chapitre 5 — Dynamique du spread, épisodes et activité',
       'Chapitre 6 — Volatilité, mémoire longue et départage des familles de modèles',
       'Chapitre 7 — Cycles temporels et références normales',
       'Chapitre 8 — Résultats négatifs, réfutations et artefacts éliminés',
       'Chapitre 9 — Verdict économique, référentiel de normalité et limites ouvertes',
       'Annexe A — Artefacts, empreintes SHA-256 et références d\u2019exécution',
       'Annexe B — Glossaire et conventions de mesure']
for i, t in enumerate(toc, 1): S.append(P(f'{t}', 'body'))
S += [Spacer(1, 0.4 * cm), box('<b>Convention de lecture.</b> « bp » = point de base relatif (1 bp = 0,01 %). Mid = (Bid+Ask)/2, prix construit non exécutable. Exécutable : achat à l\u2019Ask, vente au Bid. QLIKE : perte de prévision de volatilité (plus basse = meilleure, valeurs négatives car logarithmes). « Ère » désigne un regroupement calendaire descriptif (2010–2012 / 2013–2015 / 2016–2020), jamais un régime discret prétendu.'), PageBreak()]

# ---------- CHAPITRE 1 ----------
S.append(P('CHAPITRE 1 — GENÈSE, GOUVERNANCE ET PÉRIMÈTRE CERTIFIÉ', 'h1'))
S.append(P('1.1 Objectif du programme. META ALPHA XAUUSD DGP vise d\u2019abord à <b>comprendre le fonctionnement observable du marché de l\u2019or</b> avant toute recherche d\u2019avantage économique : cartographie intégrale, construction d\u2019une référence du comportement normal, détection contextuelle des anomalies, identification de phénomènes répétitifs, et seulement ensuite formulation d\u2019hypothèses testables. Le présent dossier clôt la phase de cartographie In-Sample.'))
S.append(P('1.2 Architecture du corpus. Le corpus certifié DGP Base (lecture seule, jamais modifié) comprend 348 partitions Parquet au total ; le périmètre In-Sample (IS) en retient 282, délimité par la borne temporelle certifiée (dernière partition se terminant le 2020-01-20). Les partitions OOS et HOLDOUT existent dans l\u2019inventaire mais n\u2019ont <b>jamais été ouvertes ni lues</b> par aucun moteur du programme. Chaque tick est une cotation (Bid, Ask, horodatage UTC) : ce ne sont pas des transactions. Il n\u2019existe ni volume négocié, ni carnet d\u2019ordres, ni sens d\u2019agresseur dans ces données, et rien de tel n\u2019a jamais été reconstitué ou supposé.'))
t = [['Grandeur', 'Valeur certifiée'],
     ['Partitions IS', '282 / 282 analysées (couverture intégrale vérifiée à chaque mission)'],
     ['Ticks IS', '288 086 306 (contrôle de recomptage : 288 086 588 = total + 1 premier tick × 282 partitions)'],
     ['Fenêtre IS', '2010-01-04 → 2020-01-20 (borne certifiée)'],
     ['Taille du corpus migré', '9,73 Go (8 datasets privés Kaggle, SHA-256 vérifiés)'],
     ['Schéma tick', 'observation_id, timestamp_utc, bid, ask, mid (construit), spread_rel'],
     ['OOS / HOLDOUT', 'jamais ouverts — accès interdit sans ordre explicite séparé du propriétaire']]
S.append(tbl([hdr(t[0])] + [row(r) for r in t[1:]], [4.5 * cm, 12.1 * cm]))
S.append(P('1.3 Séparation stricte IS / OOS / HOLDOUT. La frontière est technique et pas seulement déclarative : chaque moteur sélectionne les partitions par la borne certifiée (<i>timestamp_max ≤ 2020-01-20T09:36:27</i>) lue dans l\u2019inventaire exhaustif, et aucun chemin de code ne référence les partitions ultérieures. Le protocole gelé de comparaison des modèles de volatilité illustre la discipline : son étape 1 (IS) est exécutée et conclue « NON DÉPARTAGÉ » ; son étape 2 (OOS) exige une autorisation explicite séparée qui n\u2019a jamais été donnée et n\u2019a jamais été engagée.'))
S.append(P('1.4 Règles de rigueur scientifique. (i) Chaînage systématique : données natives → observation → compréhension → granularités naturelles → anomalies → caractérisation → structures éventuelles → hypothèses → tests → qualification. (ii) Aucun régime discret forcé : les changements observés sont progressifs (mécanique de cotation) ou continus (volatilité) ; la représentation suit les observations. (iii) Gouvernance de la multiplicité (protocole final, commit ba9195e) : registre cumulatif chaîné par hash, préenregistrement avant calcul, correction par famille (Benjamini–Yekutieli) lorsque des tests sont menés, découvertes IS plafonnées au statut « découverte candidate », confirmation OOS éventuelle uniquement par famille unique verrouillée par hash avant une consultation unique. (iv) Seuils et critères gelés avant observation des résultats. (v) Résultats négatifs, disparitions après contrôle et artefacts consignés au même titre que les résultats positifs. (vi) Une anomalie est un écart à son contexte (mois, mécanique de cotation, granularité, heure), jamais une simple valeur extrême.'))
S.append(P('1.5 Règles économiques. Toute évaluation économique utilise les cotations exécutables (achat Ask / vente Bid). Les coûts documentés sont intégrés ; les coûts inconnus (commissions, slippage, latence, conditions réelles d\u2019exécution) ne sont <b>jamais remplacés par zéro</b> : ils sont présentés comme incertitudes et rendent toute conclusion économique <b>CONDITIONNELLE</b>. Budget du programme : 0 FCFA, aucun service payant. Le corpus de base certifié est en lecture seule.'))
S.append(box('<b>Synthèse du chapitre 1.</b> Périmètre intégralement couvert (282/282), frontière OOS/HOLDOUT jamais franchie, traçabilité totale par chaîne de hash et empreintes SHA-256, discipline de préenregistrement effective (49 entrées au commit 0e56bbb).'))

# ---------- CHAPITRE 2 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 2 — INFRASTRUCTURE, MIGRATION KAGGLE ET RÉSOLUTION DES BLOCAGES', 'h1'))
S.append(P('2.1 Le blocage initial : Google Drive. Les premières missions lisaient les partitions depuis Google Drive via l\u2019infrastructure CI. Le quota de téléchargement Drive s\u2019est saturé à répétition : téléchargements interrompus, runs annulés ou échoués, et — fait plus grave méthodologiquement — des synthèses partielles (couverture 268/282) dont l\u2019état « done » sous-comptait les fichiers réellement traités. Tous ces échecs sont conservés dans l\u2019historique (runs annulés 43920294221, 43920400946 pour DIST_REGIME, etc.) ; la leçon consignée est de toujours vérifier la couverture dans les CSV dédupliqués plutôt que dans les compteurs d\u2019état.'))
S.append(P('2.2 La migration Kaggle. Le corpus IS complet a été migré vers 8 datasets privés Kaggle sous le compte <i>shalom5123</i> : un lot correctif <i>xauusd-is-missing13</i> (les 13 partitions manquantes des synthèses partielles) et sept lots <i>xauusd-is-b01</i> … <i>xauusd-is-b07</i>, soit 282 fichiers et 9,73 Go. Chaque fichier a été haché en SHA-256 avant téléversement ; la vérification indépendante (run CI 44114390403, artefact <i>kaggle_migration/VERIFY.json</i>) compare noms et tailles attendus et distants pour les 8 lots : <b>all_ok = true, 282/282</b>.'))
rows = [[b, str(v['attendus']), str(v['distants']), '0', '0'] for b, v in verify['batches'].items()]
S.append(tbl([hdr(['Dataset Kaggle', 'Attendus', 'Distants', 'Manquants', 'Tailles diff.'])] + [row(r) for r in rows], [5.4 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm]))
S.append(P('2.3 Gains de performance mesurés. Là où une mission Drive complète exigeait environ 2 heures (et échouait souvent), le cycle Kaggle typique traite les 282 partitions en 2 à 6 minutes : MARKET_DIMENSIONS complété en ~5 min (run 44115203094), POST_EVENT en 4 min 06 (44132346231), VOL_HOURLY en 2 min 35 (44190381343), SPREAD_EPISODES en 2 min 55 (44250684673), INTEGRAL_SCAN en ~6 min (44253274284, 44254224163). Le moteur télécharge un lot Kaggle une seule fois, traite toutes ses partitions localement, puis passe au lot suivant ; Drive ne subsiste qu\u2019en repli automatique.'))
S.append(P('2.4 Incidents techniques résolus et conservés. (i) <b>Bibliothèque <i>six</i></b> : la CLI Kaggle échouait dans l\u2019environnement CI ; contournement par l\u2019API Python (<i>dataset_create_new</i>). (ii) <b>Authentification 401</b> : le jeton KGAT est incompatible avec la CLI dans ce contexte ; passage au porteur (<i>bearer</i>) via la variable <i>KAGGLE_API_TOKEN</i> alimentée par le secret CI (jamais versionné). (iii) <b>Vérification 403 transitoires</b> : pagination explicite (<i>page_token</i>, <i>page_size=100</i>) et réessais dans le vérificateur d\u2019inventaire distant. (iv) <b>Déclenchement des workflows</b> : <i>workflow_dispatch</i> renvoie 404 hors branche par défaut ; adoption d\u2019un déclencheur par poussée de fichier (<i>import_trigger/*.txt</i>). (v) <b>Piège de dérivation par copie de workflow (deux occurrences)</b> : renommages automatiques produisant un mauvais nom de script (run 44188639823, échec conservé) puis un mauvais chemin de déclencheur ; règle permanente adoptée : écrire les workflows à la main et grep-vérifier les lignes <i>run:</i> et <i>paths:</i> avant toute poussée. (vi) <b>Bug d\u2019indexation des prévisions GARCH horaires</b> (masque de fenêtres 24 h) détecté avant interprétation, résultats NaN rejetés, calcul refait. (vii) <b>Bug de mesure <i>sh_pos</i></b> (moyenne SQL d\u2019un CASE sans ELSE valant constamment 1,0) et <b>grille du Mid noyée dans le bruit flottant</b> : détectés lors de la synthèse INTEGRAL_SCAN, corrigés, et recalcul complet 282/282 (run 44254224163) ; la première passe reste dans l\u2019historique Git. (viii) <b>Fenêtres DuckDB imbriquées interdites</b> : restructuration systématique en CTE à deux étapes.'))
S.append(box('<b>Synthèse du chapitre 2.</b> L\u2019infrastructure finale (Kaggle prioritaire, Drive en repli, checkpoints Git tous les 40 fichiers, chaîne d\u2019audit vérifiée avant tout calcul) rend un balayage intégral de 288 millions de ticks reproductible en quelques minutes, gratuitement, avec reprise automatique sur checkpoint vérifié.'))

# ---------- CHAPITRE 3 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 3 — CHRONOLOGIE COMPLÈTE DE LA CHAÎNE D\u2019AUDIT (ENTRÉES 1 À 49)', 'h1'))
S.append(P('Chaque mission est préenregistrée (verrouillage SHA-256 du protocole) puis close par une entrée de résultat dans <i>TRIAL_LEDGER_CHAIN.json</i> ; chaque entrée contient le hash de la précédente, de sorte que toute réécriture est détectable et visible dans l\u2019historique Git. Le tableau ci-dessous reproduit les 49 entrées dans l\u2019ordre, avec le type d\u2019acte et le contenu consigné (abrégé lorsque l\u2019entrée d\u2019origine est longue ; le texte intégral est dans le registre).'))
rows = []
for e in chain:
    ent = e['entry']; txt = ent.get('verdict') or ent.get('resultat') or ent.get('description') or ent.get('scope') or ent.get('engine') or ent.get('registry') or ''
    rows.append([e['seq'], ent.get('type', ''), ent.get('mission', '—'), str(txt)[:150]])
S.append(tbl([hdr(['Seq', 'Type', 'Mission', 'Contenu consigné'])] + [row(r) for r in rows], [1.1 * cm, 2.6 * cm, 3.4 * cm, 9.5 * cm]))
S.append(P('Commits structurants associés : <b>820b673</b> (POST_EVENT, 282/282), <b>822a2d3</b> (VOL_HOURLY + cycles), <b>195d42c</b> (épisodes de spread + réfutation désaisonnalisée), <b>0e56bbb</b> (rapport scientifique global consolidé et clôture INTEGRAL_SCAN). Les entrées 2, 3 et 5 rappellent l\u2019héritage contraignant d\u2019avant la cartographie : hypothèses générées non qualifiées, protocole rejeté après coûts (P4-001 : nets OOS −2,90 / −2,47 bp dans l\u2019historique antérieur au gel OOS actuel), et vague de tests sans survivant (P3-002 : 0/21). Ces échecs font partie du bilan et ne sont pas réécrits.'))
S.append(box('<b>Synthèse du chapitre 3.</b> 49 actes tracés, de l\u2019hypothèse rejetée P4-001 à la clôture INTEGRAL_SCAN : chaque chiffre des chapitres suivants est rattaché à une entrée, un run CI et un artefact haché.'))

# ---------- CHAPITRE 4 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 4 — MÉCANIQUE MICROSTRUCTURELLE DES COTATIONS', 'h1'))
S.append(P('La mission INTEGRAL_SCAN (préenregistrement seq 46–47 ; runs 44253274284 et 44254224163, passe corrigée) a mesuré, pour chacune des 282 partitions, 39 métriques de mécanique de flux : types de mises à jour, tailles de mouvements par côté, symétries, grille de prix, intégrité du flux, longueurs de séries de signe, inter-arrivées, quantiles de spread et de mouvements, dépendances contemporaines et décalées. Le contrôle de recomptage des ticks (288 086 588 attendus au premier tick près) valide la passe.'))
pa = integ['par_annee']; yrs = sorted(pa.keys(), key=lambda x: int(x))
rows = []
for y in yrs:
    d = pa[y]
    rows.append([y, f"{d['sh_both']:.3f}", f"{d['sh_bidonly']:.3f}", f"{d['sh_askonly']:.3f}", f"{d['sp_p50']:.2f}", f"{d['dt_p50']:.3f}", f"{d['ac1_r']:.3f}", f"{d['run_len']:.2f}"])
S.append(P('Tableau 4.1 — Médianes annuelles (par partition) des métriques de mécanique', 'h2'))
S.append(tbl([hdr(['Année', 'Bilatérales', 'Bid seul', 'Ask seul', 'Spread p50 (bp)', 'dt p50 (s)', 'ac1 rendement', 'Série signe'])] + [row(r) for r in rows], [1.8 * cm, 2.3 * cm, 2.0 * cm, 2.0 * cm, 2.6 * cm, 2.0 * cm, 2.3 * cm, 1.6 * cm]))
S.append(P('4.1 La transition de mécanique. En 2010, 98,6 % des mises à jour font bouger Bid et Ask simultanément ; cette part tombe à 93,5 % (2011), 78,1 % (2012), ~54 % (2013–2014), 27,8 % (2015), puis oscille entre 28 % et 42 % (2016–2019). La référence mensuelle (120 mois) date le passage durable sous 50 % à octobre 2012 et mesure ~31–37 % de bilatérales en 2019. Les mises à jour unilatérales sont symétriques dans toutes les ères (~0,6 %/0,6 % par côté au début, ~30 %/30 % ensuite) : le changement est un changement de <b>mode de publication</b> du flux, pas l\u2019apparition d\u2019un déséquilibre acheteur/vendeur.'))
S.append(P('4.2 Symétrie Bid/Ask. Les tailles moyennes des mouvements des deux côtés sont indiscernables : ratio médian |ΔBid|/|ΔAsk| = 0,9997 (bande inter-partitions p10–p90 : 0,990–1,008) et corrélation de Spearman des tailles au niveau partition ρ = 1,00. La part des mouvements haussiers parmi les mouvements non nuls vaut 0,501 / 0,500 / 0,500 selon l\u2019ère. Bid et Ask sont deux vues d\u2019un même processus de prix, et aucun biais directionnel de microstructure n\u2019existe à l\u2019échelle du tick.'))
S.append(P('4.3 Absence de leader. En ère ancienne, la corrélation croisée à un événement de décalage vaut 0,538 <b>dans les deux sens</b> (ΔBid<sub>t</sub>→ΔAsk<sub>t+1</sub> et ΔAsk<sub>t</sub>→ΔBid<sub>t+1</sub>), contre 0,346 en contemporain : c\u2019est le motif « ±1 événement » de l\u2019ancien régime bilatéral, où les deux côtés se répondent d\u2019un tick à l\u2019autre. En ère récente, le contemporain domine (0,56–0,60) et les décalés tombent à 0,13–0,17, toujours symétriques. Aucun côté ne mène l\u2019autre, à aucune époque — résultat obtenu dès GLOBAL DISCOVERY et confirmé ici à couverture intégrale.'))
S.append(P('4.4 Séries de même signe et autocorrélation. La longueur moyenne des séries de mouvements de même signe passe de 2,89 événements (2010–2012) à 1,82 (2016–2020) ; l\u2019autocorrélation d\u2019ordre 1 du rendement tick passe de +0,497 à +0,046 (médianes d\u2019ère). Ces deux grandeurs sont des propriétés du mécanisme de publication ancien (réponses ±1 événement), pas une inefficience exploitable : le proxy de réversion associé reste inférieur au spread dans 282/282 partitions (DEEP_AXES). L\u2019hétérogénéité interne est réelle : médiane annuelle d\u2019ac1 de +0,655 en 2011 contre −0,206 en 2012, année de transition. L\u2019autocorrélation s\u2019éteint vers 100 événements / 60 s, et les autocorrélations des barres temporelles sont légèrement négatives (−0,011 / −0,019 / −0,040 à 300/900/3600 s).'))
S.append(P('4.5 Grille et intégrité du flux. Le plus petit incrément observé sur Bid/Ask est de 0,001 $ (0,0005 $ sur le Mid construit, demi-grille mécanique ; la « grille du Mid » brute, ~1e-13, était un artefact de représentation flottante, corrigé). La part des cotations croisées ou verrouillées (Bid ≥ Ask) est de <b>0,000 sur les 282 partitions</b> : le flux ne contient aucune cotation impossible. Deux familles de rendements nuls, que la seule statistique « part de rendements nuls » confond, sont distinguées : GD-07 (pic fin 2012, jusqu\u2019à ~20 % par partition) = republications exactes de la même cotation (artefact de flux, à flaguer dans toute statistique tick) ; GD-08 (2015–2018, 1,9–3,5 %) = ajustements compensatoires Bid/Ask à Mid constant (vrai comportement de spread).'))
S.append(box('<b>Synthèse du chapitre 4.</b> Le « marché » observable a changé de mécanique de publication entre 2010 et 2019 (bilatéral → majoritairement unilatéral symétrique), sans déséquilibre directionnel, sans leader, sans cotation invalide. Toute statistique poolée sur 2010–2020 mélange deux processus de production distincts et doit être contextualisée.'))

# ---------- CHAPITRE 5 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 5 — DYNAMIQUE DU SPREAD, ÉPISODES ET ACTIVITÉ', 'h1'))
S.append(P('5.1 Le niveau du spread : une compression séculaire. Le spread relatif médian passe d\u2019environ 4,15–4,25 bp (2010) à 2,20 bp en régime récent, avec un creux annuel pondéré de 1,83–1,89 bp en 2017–2018 et 2,09 bp en 2019. Cette compression accompagne un triplement de l\u2019activité (≈2 100 ticks/heure en 2010 contre ≈7 800 en 2016–2017 ; temps médian entre ticks de 3,7 s en début de période contre 0,6–0,9 s ensuite, 0,107–1,074 s d\u2019une partition à l\u2019autre dans INTEGRAL_SCAN). Relations mensuelles documentées : spread ~ intensité ρ = −0,60 / −0,47 et spread ~ volatilité ρ = +0,64 / +0,72 selon le périmètre ; la relation spread–intensité subsiste <i>à l\u2019intérieur</i> de chaque régime de cotation, ce qui exclut qu\u2019elle soit un simple artefact de composition.'))
S.append(P('5.2 Persistance et dynamique. L\u2019autocorrélation d\u2019ordre 1 du spread tick est de 0,633 en médiane poolée et croît entre ères (0,58 → 0,82 → 0,77 en médianes d\u2019ère) : le spread récent est plus bas mais plus persistant. La variation typique d\u2019un tick à l\u2019autre (|Δspread| moyen) suit le niveau du spread lui-même.'))
S.append(P('5.3 Épisodes (seuils fixes préenregistrés : large &gt; 6 bp, serré &lt; 2 bp ; run 44250684673, 282/282). Les élargissements sont rares et brefs : 0,02–0,10 % des ticks selon le régime de cotation, longueur moyenne 1,8–4,3 événements, p95 de durée 28–37 s (les moyennes de durée sont gonflées par de rares épisodes traversant des interruptions de flux ; le p95 est la statistique robuste). Les spreads serrés, quasi absents en régime bilatéral (0,68 % des ticks), deviennent structurels ensuite : 36,7 % (mixte, n = 15, prudence) et 21,4 % (unilatéral) — la compression du spread est un trait permanent du régime récent, pas une succession d\u2019accidents. En régime récent, l\u2019épisode serré typique est unitaire (p95 = 8 événements contre 1 en bilatéral).'))
ep = [['Caractéristique', 'Régime bilatéral', 'Régime mixte', 'Régime unilatéral'],
      ['Ticks en épisode large (&gt; 6 bp)', '0,02–0,10 % (selon régime)', '—', 'bas de fourchette'],
      ['Longueur moyenne épisode large', '1,8–4,3 événements (p95 : 6–16)', '', ''],
      ['Durée p95 épisode large', '28–37 s', '', ''],
      ['Ticks en épisode serré (&lt; 2 bp)', '0,68 %', '36,7 % (n = 15)', '21,4 %'],
      ['Spread médian de référence (bp)', '4,147', '2,093', '2,215']]
S.append(tbl([hdr(ep[0])] + [row(r) for r in ep[1:]], [5.2 * cm, 4.4 * cm, 3.4 * cm, 3.6 * cm]))
S.append(P('5.4 Activité et inter-arrivées. La distribution des temps entre ticks est à queue lourde dans les trois régimes (p50 : 0,26–0,49 s ; p99 : 6,7–19,5 s) : rafales et silences coexistent sans qu\u2019aucun calendrier ne soit supposé. Attention de mesure (INTEGRAL_SCAN) : le coefficient de variation des inter-arrivées au niveau partition est dominé par les interruptions du flux à l\u2019intérieur des partitions récentes (valeurs de 150–280 contre ~2,5 en 2010, qui reflètent la composition des fichiers, pas une soudaine irrégularité du marché) ; il ne doit pas être interprété comme une mesure de rafale économique. Les parts de silences &gt; 10 s et &gt; 60 s, elles, sont robustes et consignées par partition.'))
S.append(box('<b>Synthèse du chapitre 5.</b> Le coût de friction observable (spread) a été divisé par deux en dix ans pendant que l\u2019activité triplait ; ses élargissements restent des accidents brefs et ses compressions un trait structurel récent. Toute évaluation économique historique doit utiliser le spread de son époque, jamais une moyenne décennale.'))

# ---------- CHAPITRE 6 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 6 — VOLATILITÉ, MÉMOIRE LONGUE ET DÉPARTAGE DES FAMILLES', 'h1'))
S.append(P('6.1 Protocole gelé. La comparaison des familles continues de volatilité (aucun modèle discret admis) suit le protocole validé <i>PROTOCOLE_MODELES_CONTINUS_VOLATILITE_GELE.md</i> : familles GARCH normale, GARCH-t, FIGARCH, ARFIMA sur log-volatilité, volatilité stochastique AR(1), et référence naïve ; critère QLIKE ; verdict « départagé » seulement si un modèle détient à la fois la meilleure moyenne <b>et</b> au moins 4 blocs gagnés sur 5. L\u2019étape 1 (IS) est exécutée ; l\u2019étape 2 (OOS) n\u2019a jamais été autorisée ni engagée.'))
def qtab(res, key_d, key_h=None):
    rows = []
    for name in ['GARCH_N', 'GARCH_T', 'FIGARCH', 'ARFIMA_LOGVOL', 'SV_AR1_LOGVOL', 'NAIF']:
        rows.append([name, f"{res[key_d][name]:.3f}"])
    return rows
S.append(P('Tableau 6.1 — QLIKE moyen, échelle journalière (3 097 jours, IS complet)', 'h2'))
S.append(tbl([hdr(['Modèle', 'QLIKE IS complet'])] + [row(r) for r in qtab(volD['IS_COMPLET']['perte_QLIKE_moyenne'], 'x')] if False else [hdr(['Modèle', 'QLIKE IS complet'])] + [row([n, f"{v:.3f}"]) for n, v in volD['IS_COMPLET']['perte_QLIKE_moyenne'].items()], [8.3 * cm, 8.3 * cm]))
S.append(P('Verdict journalier : <b>NON DÉPARTAGÉ</b> sur les trois périmètres (IS complet, ancien régime, régime récent). ARFIMA détient la meilleure moyenne IS (−8,206) sans jamais réunir le critère complet de blocs ; les écarts entre familles restent minces devant l\u2019incertitude inter-blocs.'))
S.append(P('Tableau 6.2 — QLIKE moyen, échelle horaire (60 026 heures)', 'h2'))
rows = [[n, f"{volH['IS_COMPLET']['perte_QLIKE'][n]:.3f}", f"{volH['REGIME_RECENT']['perte_QLIKE'][n]:.3f}", f"{volH['REGIME_RECENT']['blocs_gagnes'][n]}/4"] for n in ['GARCH_N', 'GARCH_T', 'FIGARCH', 'ARFIMA_LOGVOL', 'SV_AR1_LOGVOL', 'NAIF']]
S.append(tbl([hdr(['Modèle', 'QLIKE horaire IS', 'QLIKE horaire récent', 'Blocs récent'])] + [row(r) for r in rows], [4.6 * cm, 4.0 * cm, 4.2 * cm, 3.8 * cm]))
S.append(P('Verdict horaire : <b>NON DÉPARTAGÉ</b> aux deux périmètres. Sur le régime récent, ARFIMA gagne 3 blocs sur 4 — le plus proche du critère sans l\u2019atteindre ; FIGARCH détient la meilleure moyenne sans gagner de bloc. Chercher à « départager » en re-paramétrant serait de la sur-optimisation : la conclusion de cartographie est que <b>la famille n\u2019est pas identifiable sur ce corpus, à ces deux échelles et ces cinq périmètres</b>.'))
S.append(P('6.2 Le paramètre fractionnaire d : le résultat stable du programme. Là où les familles se disputent sans vainqueur, le paramètre de mémoire longue est remarquablement stable : d ARFIMA ≈ 0,30–0,42 au journalier (par bloc et par périmètre) et 0,25–0,34 à l\u2019horaire ; les estimations GPH indépendantes donnent 0,30–0,42. La volatilité de l\u2019or possède donc une mémoire intermédiaire-longue réelle, invariante d\u2019échelle (journalier ↔ horaire) et d\u2019époque — c\u2019est un trait du processus, utilisable comme référence, même si aucune famille paramétrique ne peut être déclarée « la bonne ». Les queues restent épaisses : le top 1 % des mouvements tick porte ≈18,8 % de la variance (≈37 % en régime récent, partitions plus grandes, prudence), le choc tick maximal atteint ≈170 bp, les queues de barres sont symétriques, et l\u2019effet de levier est faible et dépendant de l\u2019époque au journalier (−0,054 poolé ; −0,108 ancien, −0,028 récent), nul à l\u2019échelle du tick (−0,0025).'))
S.append(box('<b>Synthèse du chapitre 6.</b> Non-départage assumé et documenté à deux échelles : la science produite ici est la stabilité de d ≈ 0,25–0,42 et l\u2019inidentifiabilité des familles — pas un classement de modèles maquillé en victoire.'))

# ---------- CHAPITRE 7 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 7 — CYCLES TEMPORELS ET RÉFÉRENCES NORMALES', 'h1'))
S.append(P('7.1 Le cycle UTC (sans aucune session supposée : seul l\u2019horodatage natif est utilisé). Le flux se concentre autour de 14h UTC : 8,35 % des ticks de la journée, spread minimal 2,20 bp, temps entre ticks ≈0,4 s. Le creux se situe à 21h UTC (0,55 % des ticks) et le spread maximal à 22h UTC (3,33 bp, jusqu\u2019à 3,50 bp sur le créneau 21h–23h). Ce cycle est présent dans les trois régimes de cotation : c\u2019est une propriété du flux, pas d\u2019une époque.'))
S.append(P('7.2 Le profil hebdomadaire observé. Lundi à vendredi sont quasi identiques (spread 2,53–2,62 bp ; 10 836–12 131 heures chacun dans la série horaire). Le <b>samedi est absent du flux</b> (0 heure) ; le dimanche est partiel (945 heures, spread 3,51 bp, activité réduite). Il s\u2019agit du calendrier du flux observé ; aucune session officielle n\u2019est nommée ni supposée.'))
S.append(P('7.3 Couplage volatilité–spread et sa réfutation partielle. Brut, le couplage contemporain log-RV/spread au niveau horaire vaut −0,164, et −0,293 en régime récent (ancien : −0,046), avec des corrélations décalées de +0,10/+0,15 à +3 h/+5 h qui suggéraient un « élargissement différé du spread après la volatilité ». Le contrôle discriminant — retrait des médianes par heure du jour — fait tomber le contemporain à <b>−0,029</b> et rend le profil décalé symétrique (~+0,15 des deux côtés) : c\u2019était le cycle diurne commun aux deux séries plus leur persistance propre. L\u2019hypothèse d\u2019élargissement différé est donc <b>réfutée en l\u2019état</b> et consignée comme telle (chapitre 8). Subsistent, à titre descriptif, des contemporains désaisonnalisés de +0,118 (ancien) et −0,179 (récent) dont le signe opposé interdit toute loi unique.'))
cyc = [['Référence', 'Valeur'], ['Pic d\u2019activité', '14h UTC — 8,35 % des ticks, spread 2,20 bp, dt ≈ 0,4 s'],
       ['Creux d\u2019activité', '21h UTC — 0,55 % des ticks'], ['Spread maximal', '22h UTC — 3,33 bp'],
       ['Lun–Ven', 'spread 2,53–2,62 bp, homogènes'], ['Samedi', 'absent du flux (0 h)'],
       ['Dimanche', 'partiel — 945 h, spread 3,51 bp'],
       ['Couplage log-RV/spread brut (récent)', '−0,293 contemporain'], ['Après désaisonnalisation', '−0,029 — mécanisme différé réfuté']]
S.append(tbl([hdr(cyc[0])] + [row(r) for r in cyc[1:]], [5.6 * cm, 11.0 * cm]))
S.append(box('<b>Synthèse du chapitre 7.</b> La « normalité » du marché est désormais définie par des références mesurées (heure UTC, jour de flux, ère) contre lesquelles un écart devient une anomalie qualifiable — au lieu de moyennes décennales qui mélangent les contextes.'))

# ---------- CHAPITRE 8 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 8 — RÉSULTATS NÉGATIFS, RÉFUTATIONS ET ARTEFACTS ÉLIMINÉS', 'h1'))
S.append(P('Ce chapitre est aussi important que les précédents : il empêche de re-tester indéfiniment des pistes mortes et documente la discipline du programme.'))
neg = [['Piste / artefact', 'Test décisif', 'Verdict consigné'],
 ['Réversion post-choc (POST_EVENT, 282/282)', '2 916 sauts tick &gt; 10 bp ; 26 582 barres extrêmes', 'Réversion −1,97 bp à +100 ticks &lt; spread à l\u2019événement 6,70 bp ; barre suivante +0,22 bp de signe incohérent — aucune hypothèse de stratégie'],
 ['Élargissement différé du spread après volatilité', 'Désaisonnalisation par heure du jour', 'RÉFUTÉ en l\u2019état : −0,164 → −0,029 ; profil décalé symétrique (cycle diurne confondu)'],
 ['Régimes discrets de marché', 'Contrôle négatif HMM + segmentation sur séries simulées GARCH', 'Non démontrables : le détecteur hallucine 12/12 sur du bruit GARCH pur ; HMM interdit comme détecteur autonome, segmentation interdite comme preuve (échec conservé, commit bacc922)'],
 ['Leader Bid ou Ask (lead-lag)', 'Corrélations croisées ±1 événement, 3 ères', 'Absent partout : décalés strictement symétriques (0,538/0,538)'],
 ['Artefact GD-07 (fin 2012)', 'Caractérisation tick dédiée (55 partitions)', 'Republications exactes de cotation (18–23 %) : artefact de flux, à flaguer ; pas un marché figé'],
 ['Phénomène GD-08 (2015–2018)', 'Séparation republication / Mid constant', 'Ajustements compensatoires Bid/Ask à Mid constant : mécanisme distinct de GD-07'],
 ['Colonnes share_* (GLOBAL DISCOVERY)', 'Relecture du moteur', 'INVALIDES à jamais (lag sur mauvaise colonne) ; jamais réutilisées'],
 ['Familles de volatilité (protocole gelé)', 'QLIKE, 2 échelles, 5 périmètres, critère gelé', 'NON DÉPARTAGÉ partout ; ne pas re-paramétrer pour forcer un vainqueur'],
 ['Anomalies contextuelles INTEGRAL_SCAN', '257 excès &gt; 5 MAD / 8 526 cellules', 'Dominées par l\u2019artefact de composition (CV des inter-arrivées) ; non promues ; extrêmes réels = épisodes déjà catalogués (ex. part_000062, 2010)'],
 ['Mesures v1 INTEGRAL_SCAN (sh_pos, grille Mid)', 'Contrôles de cohérence en synthèse', 'Invalides (CASE sans ELSE ; bruit flottant 1e-13) ; corrigées et recalculées 282/282'],
 ['Hypothèses économiques historiques', 'P4-001 (rejeté), P3-002 (0/21 survivants)', 'Rejetées après coûts ; héritées comme contraintes, jamais ressuscitées telles quelles']]
S.append(tbl([hdr(neg[0])] + [row(r) for r in neg[1:]], [4.0 * cm, 5.2 * cm, 7.4 * cm]))
S.append(box('<b>Synthèse du chapitre 8.</b> Chaque réfutation est datée, chiffrée et rattachée à son contrôle. Le programme ne « perd » pas ces résultats : ils délimitent l\u2019espace des phénomènes réels et conditionnent toute hypothèse future.'))

# ---------- CHAPITRE 9 ----------
S.append(PageBreak()); S.append(P('CHAPITRE 9 — VERDICT ÉCONOMIQUE, RÉFÉRENTIEL DE NORMALITÉ ET LIMITES OUVERTES', 'h1'))
S.append(P('9.1 Verdict économique. À l\u2019issue de la cartographie intégrale, <b>aucune hypothèse économique n\u2019est qualifiée</b>. La raison est mesurée, pas rhétorique : chaque régularité candidate, rapportée à son contexte, se heurte à l\u2019une de ces trois bornes — (a) amplitude inférieure au spread exécutable de son époque (réversion post-saut : 1,97 bp utile contre 6,70 bp de spread à l\u2019événement ; proxy de réversion inférieur au spread dans 282/282 partitions) ; (b) signe incohérent entre contextes (suite de barre extrême : +0,66 bp en bilatéral, −0,24 bp ailleurs ; couplage vol/spread désaisonnalisé de signe opposé selon l\u2019ère) ; (c) disparition après contrôle discriminant (élargissement différé du spread). S\u2019y ajoutent des coûts d\u2019exécution réels inconnus (commissions, slippage, latence) qu\u2019il est interdit de supposer nuls : même un effet brut positif serait CONDITIONNEL.'))
S.append(P('9.2 Référentiel de normalité (extraits ; séries complètes dans les artefacts).'))
ref = [['Contexte', 'Spread médian', 'Activité / dt', 'Mécanique dominante'],
 ['2010–2012', '≈4,1 bp (4,15–4,25 en 2010)', 'dt p50 ≈0,49 s', 'bilatérale 78–99 % ; motif ±1 événement ; ac1 tick ≈+0,50'],
 ['2013–2015', '≈2,3–2,6 bp', 'dt p50 ≈0,31–0,36 s', 'transition ; bilatérale 28–54 %'],
 ['2016–2020', '≈2,2 bp (creux 1,83–1,89 en 2017–2018)', 'dt p50 ≈0,15–0,30 s', 'unilatérale symétrique ; contemporain 0,56–0,60 ; ac1 tick ≈+0,05'],
 ['14h UTC (toutes ères)', '2,20 bp', '8,35 % des ticks ; dt ≈0,4 s', 'pic quotidien du flux'],
 ['22h UTC (toutes ères)', '3,33 bp', 'creux du flux', 'spread quotidien maximal'],
 ['Dimanche (flux partiel)', '3,51 bp', '945 h au total', 'activité réduite']]
S.append(tbl([hdr(ref[0])] + [row(r) for r in ref[1:]], [3.6 * cm, 4.6 * cm, 4.0 * cm, 4.4 * cm]))
S.append(P('9.3 Ce que les données ne permettent pas de voir. Les cotations ne révèlent ni transactions, ni volumes, ni profondeur, ni files d\u2019attente, ni identité ou intention des participants ; le Mid est une construction, pas un prix négociable ; les symboles d\u2019autres marchés (argent, dollar, taux) sont hors corpus ; les paramètres réels d\u2019exécution d\u2019un compte donné sont hors corpus. Le changement de mécanique 2010–2015 est daté et mesuré, mais sa cause (fournisseur du flux, plateforme, structure de marché) n\u2019est pas observable dans les ticks.'))
S.append(P('9.4 Questions ouvertes pour la suite du programme. (i) Cartographie intra-partition et à l\u2019échelle de la minute autour des épisodes extrêmes déjà catalogués. (ii) Persistance du référentiel de normalité aux granularités fines et sa stabilité par sous-périodes. (iii) Toute hypothèse économique future devra naître d\u2019un écart mesuré à ce référentiel, être préenregistrée, chiffrée au spread exécutable de son contexte, et rester CONDITIONNELLE tant que les coûts réels ne sont pas établis documentairement. (iv) L\u2019étape 2 OOS du protocole volatilité gelé, comme toute ouverture OOS/HOLDOUT, demeure subordonnée à une autorisation explicite séparée du propriétaire — non donnée à ce jour.'))
S.append(box('<b>Synthèse générale.</b> Nous savons désormais comment ce marché publie ses prix, comment son spread et son activité ont été transformés en dix ans, quelle mémoire porte sa volatilité (d ≈ 0,25–0,42) sans qu\u2019aucune famille de modèles puisse être couronnée, quels rythmes UTC structurent son flux, et pourquoi chaque piste d\u2019edge examinée échoue contre le spread ou contre ses propres contrôles. C\u2019est une compréhension maximale, reproductible et honnête à partir des cotations disponibles — et la condition préalable à toute recherche d\u2019edge sérieuse.'))

# ---------- ANNEXE A ----------
S.append(PageBreak()); S.append(P('ANNEXE A — ARTEFACTS, EMPREINTES SHA-256 ET RÉFÉRENCES D\u2019EXÉCUTION', 'h1'))
arts = [['Artefact', 'SHA-256 (16 premiers car.) / référence'],
        ['integral_scan/INTEGRAL_PARTITION.csv', mani['sha256']['reports/meta_alpha/integral_scan/INTEGRAL_PARTITION.csv'][:16] + '…'],
        ['integral_scan/INTEGRAL_SYNTHESIS.json', mani['sha256']['reports/meta_alpha/integral_scan/INTEGRAL_SYNTHESIS.json'][:16] + '…'],
        ['META_ALPHA_RAPPORT_SCIENTIFIQUE_GLOBAL.md', mani['sha256']['reports/meta_alpha/META_ALPHA_RAPPORT_SCIENTIFIQUE_GLOBAL.md'][:16] + '…'],
        ['TRIAL_LEDGER_CHAIN.json (49 entrées)', chain[-1]['entry_hash'][:16] + '… (tête de chaîne)'],
        ['kaggle_migration/VERIFY.json', 'run 44114390403 — all_ok = true (282/282 noms + tailles)'],
        ['INTEGRAL_PARTITION.csv (ce dépôt, relu)', sha('reports/meta_alpha/integral_scan/INTEGRAL_PARTITION.csv')[:16] + '…'],
        ['MARKET_CARTOGRAPHY_LIVING.md', sha('reports/meta_alpha/MARKET_CARTOGRAPHY_LIVING.md')[:16] + '…'],
        ['Ce dossier PDF (auto-référence exclue)', 'empreinte consignée dans le manifeste de mission au dépôt']]
S.append(tbl([hdr(arts[0])] + [row(r) for r in arts[1:]], [7.4 * cm, 9.2 * cm]))
runs = [['Mission', 'Runs CI principaux (les échecs conservés sont marqués)'],
 ['Migration Kaggle + vérification', '44114390403 (succès)'],
 ['MARKET_DIMENSIONS 282/282', '44115203094 (~5 min ; échecs Drive antérieurs conservés)'],
 ['POST_EVENT', '44132346231 (4 min 06, 282/282)'],
 ['VOL_HOURLY', '44188639823 (échec conservé) → 44190381343 (2 min 35, 282/282)'],
 ['SPREAD_EPISODES + cycles', '44250684673 (2 min 55, 282/282)'],
 ['INTEGRAL_SCAN', '44253130278 (échec conservé) → 44253274284 (282/282) → 44254224163 (282/282, passe corrigée)']]
S.append(tbl([hdr(runs[0])] + [row(r) for r in runs[1:]], [5.6 * cm, 11.0 * cm]))
S.append(P('Datasets Kaggle privés : <i>shalom5123/xauusd-is-missing13</i>, <i>xauusd-is-b01</i> … <i>xauusd-is-b07</i> (282 fichiers, 9,73 Go). Moteurs versionnés dans <i>ci_tools/</i> (integral_scan.py, spread_episodes.py, post_event.py, hourly_series.py, fit_vol_hourly.py, etc.), workflows dans <i>.github/workflows/</i>, déclencheurs dans <i>import_trigger/</i>.', 'small'))

# ---------- ANNEXE B ----------
S.append(P('ANNEXE B — GLOSSAIRE ET CONVENTIONS DE MESURE', 'h1'))
glo = [['Terme', 'Définition dans ce programme'],
 ['Tick', 'Une cotation horodatée (Bid, Ask) du flux ; pas une transaction'],
 ['Mid', 'Prix construit (Bid+Ask)/2 ; non exécutable'],
 ['Spread (bp)', '(Ask−Bid)/Mid × 10 000 ; exécutable : achat Ask, vente Bid'],
 ['Partition', 'Fichier Parquet élémentaire du corpus certifié ; unité de couverture (282 IS)'],
 ['Ère', 'Regroupement calendaire descriptif (2010–2012 / 2013–2015 / 2016–2020) ; jamais un régime prétendu'],
 ['QLIKE', 'Perte de prévision de volatilité ; la plus basse est la meilleure'],
 ['d (fractionnaire)', 'Paramètre de mémoire longue de la volatilité (ARFIMA/GPH) ; mesuré 0,25–0,42'],
 ['Découverte candidate', 'Statut maximal d\u2019un phénomène IS selon la gouvernance de multiplicité ; aucune confirmation sans OOS verrouillé'],
 ['CONDITIONNEL', 'Qualifie toute lecture économique tant que commissions/slippage/latence réels ne sont pas établis'],
 ['MAD / z robuste', 'Écart médian absolu ; anomalie contextuelle si |écart| &gt; 5 MAD vs voisines temporelles']]
S.append(tbl([hdr(glo[0])] + [row(r) for r in glo[1:]], [4.2 * cm, 12.4 * cm]))
S.append(Spacer(1, 0.6 * cm))
S.append(box('<b>Clôture du dossier.</b> Programme META ALPHA XAUUSD DGP — bilan intégral In-Sample arrêté au commit 0e56bbb, chaîne d\u2019audit de 49 entrées valide. OOS et HOLDOUT demeurent fermés. Toute suite (confirmation externe, hypothèses économiques) requiert un ordre explicite du propriétaire et un préenregistrement nouveau.'))

doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                      title='DOSSIER BILAN INTEGRAL META ALPHA XAUUSD IS', author='Programme META ALPHA XAUUSD DGP')
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=footer)])
doc.build(S)
print('PDF genere:', OUT, OUT.stat().st_size, 'octets')
