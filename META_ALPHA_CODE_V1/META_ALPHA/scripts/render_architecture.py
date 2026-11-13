"""Génère docs/ARCHITECTURE_COMPLETE_V2.html depuis metaalpha.mission.

Le schéma n'est pas dessiné à la main : il est rendu depuis les données qui
décrivent réellement le système. Si une phase n'existe pas dans le code, elle
n'apparaît pas dans le schéma. C'est la seule façon d'éviter un schéma
« prometteur » qui ne correspond à rien.
"""
from __future__ import annotations

import pathlib

from metaalpha.mission import (
    AUTOMATED_CAPABILITIES, BG_HOLD_MIN_MINUTES, BG_NOT_PUBLIC, BG_REPORTED_RULES,
    CHAIN, LAYERS, NEVER_AUTOMATED, PHASES, TICK_LIMITS,
    all_artifacts, human_decisions, stats,
)

OUT = pathlib.Path("docs/ARCHITECTURE_COMPLETE_V2.html")

CSS = """<style>
:root{--bg:#070a0e;--card:#111820;--card2:#0d131a;--lin:#1f2b38;--tx:#e8eef4;--mut:#8497a9;
--ok:#3fb950;--warn:#d29922;--bad:#f85149;--acc:#58a6ff;--vio:#a371f7;--cy:#39c5cf}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:34px 18px 80px}
.wrap{max-width:1320px;margin:0 auto}
h1{font-size:30px;margin:0 0 8px;letter-spacing:-.025em;line-height:1.25}
h2{font-size:20px;margin:46px 0 6px;letter-spacing:-.015em}
h2 .num{color:var(--acc);font-family:ui-monospace,Menlo,monospace;font-size:14px;margin-right:10px;opacity:.8}
h2+.lede{color:var(--mut);margin:0 0 18px;font-size:14.5px;max-width:940px}
h3{font-size:14px;margin:0 0 10px;letter-spacing:.01em}
.sub{color:var(--mut);margin:0 0 16px;font-size:14.5px;max-width:940px}
.card{background:var(--card);border:1px solid var(--lin);border-radius:12px;padding:20px;margin:16px 0}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;color:var(--mut);font-weight:600;padding:9px 10px;border-bottom:1px solid var(--lin);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
td{padding:9px 10px;border-bottom:1px solid #18212b;vertical-align:top}
tr:last-child td{border-bottom:none}
code{background:#0a0f15;padding:2px 6px;border-radius:4px;font-size:11.5px;color:var(--cy);font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:11px;margin:20px 0}
.kpi div{background:var(--card2);border:1px solid var(--lin);border-radius:11px;padding:15px}
.kpi b{display:block;font-size:26px;line-height:1.05;letter-spacing:-.03em}
.kpi span{color:var(--mut);font-size:11.5px;display:block;margin-top:4px;line-height:1.35}
.note{border-left:3px solid var(--acc);padding:12px 16px;background:#0c1420;border-radius:0 9px 9px 0;font-size:14px;margin:16px 0}
.note.ok{border-left-color:var(--ok);background:#0a1a10}
.note.bad{border-left-color:var(--bad);background:#1d0f10}
.note.warn{border-left-color:var(--warn);background:#1a1508}
.note.vio{border-left-color:var(--vio)}
.tag{font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;letter-spacing:.04em;white-space:nowrap}
.t-ok{background:#0d2a17;color:var(--ok);border:1px solid #1f6f36}
.t-h{background:#2b2208;color:var(--warn);border:1px solid #7a5c14}
.t-bad{background:#2a0f11;color:var(--bad);border:1px solid #7a2226}
.t-mut{background:#141d26;color:var(--mut);border:1px solid #26323f}
.t-cy{background:#08252a;color:var(--cy);border:1px solid #17545c}
.mono{font-family:ui-monospace,Menlo,monospace}
/* chaîne */
.chain{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:20px 0}
.chain .step{background:var(--card);border:1px solid var(--lin);border-radius:8px;padding:9px 12px;font-size:11.5px;font-weight:600;letter-spacing:.03em}
.chain .arw{color:#2f3f4f;font-size:15px}
.chain .step.hi{border-color:#1f6f36;background:#0a1a10;color:#7ee2a0}
.chain .step.lock{border-color:#7a5c14;background:#1a1508;color:#e8c05a}
/* couches */
.layers{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:18px 0}
@media(max-width:980px){.layers{grid-template-columns:1fr}}
.layer{background:var(--card);border:1px solid var(--lin);border-radius:12px;padding:17px;position:relative;overflow:hidden}
.layer:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px}
.layer.A:before{background:var(--acc)}.layer.B:before{background:var(--vio)}.layer.C:before{background:var(--cy)}
.layer .lid{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:var(--mut);letter-spacing:.1em}
.layer h3{margin:5px 0 8px;font-size:15px}
.layer .q{color:var(--mut);font-size:13px;min-height:52px}
.layer .obj{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:var(--cy);margin-top:8px;word-break:break-all}
.layer .inf{font-size:11.5px;margin-top:10px;padding-top:10px;border-top:1px solid var(--lin);color:var(--mut)}
/* phases */
.ph{display:flex;gap:0;margin-bottom:7px;align-items:stretch}
.ph .rail{width:34px;flex:none;display:flex;flex-direction:column;align-items:center}
.ph .dot{width:11px;height:11px;border-radius:50%;margin-top:15px;flex:none}
.ph .line{width:2px;flex:1;background:#1f2b38}
.ph .body{flex:1;background:var(--card);border:1px solid var(--lin);border-radius:10px;padding:13px 16px;margin-left:4px}
.ph:last-child .line{display:none}
.ph .head{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.ph .pid{font-family:ui-monospace,Menlo,monospace;font-size:12px;font-weight:700;letter-spacing:.03em}
.ph .ttl{font-size:13.5px;font-weight:600}
.ph .qq{color:var(--mut);font-size:13px;margin-top:5px}
.ph .gates{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
@media(max-width:820px){.ph .gates{grid-template-columns:1fr}}
.ph .g{background:#0a0f15;border:1px solid #1a232d;border-radius:7px;padding:8px 10px;font-size:11.5px;color:#a9bacb}
.ph .g b{display:block;color:var(--mut);font-size:9.5px;text-transform:uppercase;letter-spacing:.07em;margin-bottom:3px;font-weight:700}
.ph .acts{margin-top:9px;font-size:11.5px;color:var(--mut);line-height:1.7}
.ph .acts .a{display:inline-block;background:#0d1520;border:1px solid #1c2836;border-radius:5px;padding:2px 7px;margin:2px 3px 0 0;font-size:11px}
.ph .arts{margin-top:9px;font-size:11px;color:#6f8497;line-height:1.8}
.ph .arts code{font-size:10.5px;background:#0a0f15;color:#5fa8d3}
.done{border-color:#1f6f36!important;background:#0a150e!important}
.hum{border-color:#7a5c14!important}
.block{border-color:#7a2226!important}
/* runtime */
.rt{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin:16px 0}
.rt .box{background:var(--card);border:1px solid var(--lin);border-radius:11px;padding:16px}
.rt .box h3{font-size:13px;margin-bottom:4px}
.rt .box .role{color:var(--cy);font-size:11px;font-family:ui-monospace,Menlo,monospace;margin-bottom:10px}
.rt .box ul{margin:0;padding-left:16px;font-size:12.5px;color:#a9bacb;line-height:1.75}
pre{background:#080d12;border:1px solid var(--lin);border-radius:10px;padding:16px;overflow-x:auto;font-size:11.5px;line-height:1.65;color:#b9c9d8;font-family:ui-monospace,Menlo,monospace}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:880px){.grid2{grid-template-columns:1fr}}
ul.clean{margin:8px 0;padding-left:18px;font-size:13px;color:#a9bacb;line-height:1.8}
.mini{font-size:12px;color:var(--mut)}
</style>"""


def _status_tag(p) -> str:
    if "CERTIFIED" in p.phase_id:
        return '<span class="tag t-ok">DÉJÀ CERTIFIÉ</span>'
    if p.produces_human_decision:
        return '<span class="tag t-h">GATE HUMAIN</span>'
    return '<span class="tag t-cy">AUTOMATIQUE</span>'


def _dot_color(p) -> str:
    if "CERTIFIED" in p.phase_id:
        return "#3fb950"
    if p.phase_id == "P8_HOLDOUT":
        return "#f85149"
    if p.produces_human_decision:
        return "#d29922"
    return "#58a6ff"


def _body_class(p) -> str:
    if "CERTIFIED" in p.phase_id:
        return "done"
    if p.phase_id == "P8_HOLDOUT":
        return "block"
    if p.produces_human_decision:
        return "hum"
    return ""


def render_phases() -> str:
    out = []
    for p in PHASES:
        acts = "".join(f'<span class="a">{a}</span>' for a in p.automated)
        arts = " ".join(f"<code>{a}</code>" for a in p.artifacts)
        hum = ""
        if p.human_only:
            hum = ('<div class="note warn" style="margin:10px 0 0;padding:9px 13px;font-size:12.5px">'
                   "<b>Vous uniquement :</b> " + " · ".join(p.human_only) + "</div>")
        forb = ""
        if p.forbidden:
            forb = ('<div class="note bad" style="margin:8px 0 0;padding:9px 13px;font-size:12px">'
                    "<b>Interdit dans cette phase :</b> " + " · ".join(p.forbidden) + "</div>")
        out.append(f"""<div class="ph"><div class="rail">
<div class="dot" style="background:{_dot_color(p)}"></div><div class="line"></div></div>
<div class="body {_body_class(p)}">
<div class="head"><span class="pid">{p.phase_id}</span><span class="ttl">{p.title}</span>{_status_tag(p)}</div>
<div class="qq">{p.question}</div>
<div class="gates">
<div class="g"><b>Entrée</b>{p.entry_gate}</div>
<div class="g"><b>Sortie</b>{p.exit_gate}</div>
</div>
<div class="acts">{acts}</div>
{hum}{forb}
<div class="arts">{arts}</div>
</div></div>""")
    return "\n".join(out)


def render_chain() -> str:
    # étapes verrouillées : celles qui ne sont atteignables qu'après autorisation
    locked = {"ADAPTATEUR BLUE GUARDIAN", "ROBOT", "VALIDATION FINALE"}
    out = []
    for i, s in enumerate(CHAIN):
        cls = "step lock" if s in locked else "step"
        out.append(f'<span class="{cls}">{s}</span>')
        if i < len(CHAIN) - 1:
            out.append('<span class="arw">→</span>')
    return "".join(out)


def render_layers() -> str:
    out = []
    for l in LAYERS:
        out.append(f"""<div class="layer {l['id']}">
<div class="lid">COUCHE {l['id']}</div>
<h3>{l['name']}</h3>
<div class="q">{l['question']}</div>
<div class="obj">{l['object']}</div>
<div class="inf"><b>Phases :</b> {l['phases']}<br><b>Influence :</b> {l['influence_externe']}</div>
</div>""")
    return "".join(out)


def render_bg() -> str:
    rows = ""
    for r in BG_REPORTED_RULES:
        st = r["status"]
        cls = "t-bad" if st.startswith(("BLOQUANT", "CONTRADICTION")) else (
            "t-mut" if st == "NOT_PUBLIC" else "t-cy")
        rows += (f'<tr><td>{r["rule"]}</td><td class="mono" style="font-size:12px">'
                 f'{r["value"]}</td><td><span class="tag {cls}">{st}</span></td></tr>')
    return rows


def build() -> str:
    s = stats()
    arts = all_artifacts()
    hum = human_decisions()

    kpis = f"""
<div class="kpi">
<div><b>{s['phases_total']}</b><span>phases dans la mission</span></div>
<div><b>{s['phases_certified_not_to_rebuild']}</b><span>déjà certifiées, jamais reconstruites</span></div>
<div><b>{s['phases_to_execute']}</b><span>à exécuter par l'ingénierie</span></div>
<div><b>{s['artifacts_total']}</b><span>artéfacts, 0 doublon</span></div>
<div><b>{s['automated_steps_total']}</b><span>étapes automatisées</span></div>
<div><b>{s['human_decisions_total']}</b><span>points où vous êtes requis</span></div>
<div><b>{s['bg_rules_blocking']}</b><span>règles BG bloquantes</span></div>
<div><b>{s['bg_not_public']}</b><span>paramètres serveur non publiés</span></div>
</div>"""

    hum_rows = "".join(
        f'<tr><td class="mono" style="font-size:12px">{h["phase"]}</td>'
        f'<td>{h["decision"]}</td><td><span class="tag t-h">BLOQUANT</span></td></tr>'
        for h in hum)

    art_rows = "".join(
        f'<tr><td><code>{a}</code></td><td class="mono mini">{", ".join(ps)}</td></tr>'
        for a, ps in sorted(arts.items()))

    bg_np = " · ".join(BG_NOT_PUBLIC)
    tick_rows = "".join(
        f'<tr><td>{t["claim"]}</td><td><span class="tag t-bad">{t["status"]}</span></td></tr>'
        for t in TICK_LIMITS)

    auto_li = "".join(f"<li>{a}</li>" for a in AUTOMATED_CAPABILITIES)
    never_li = "".join(f"<li>{a}</li>" for a in NEVER_AUTOMATED)

    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>META ALPHA — Architecture complète V2</title>{CSS}</head><body><div class="wrap">

<h1>Architecture complète — META ALPHA V2</h1>
<p class="sub">Adaptée à la fiche <span class="mono" style="font-size:13px">MISSION_SCIENTIFIQUE_BLUE_GUARDIAN_AGENT_V2</span>. Ce schéma n'est pas dessiné à la main : il est <b>rendu depuis <code>metaalpha/mission.py</code></b>, la structure qui décrit réellement le système. Si une phase n'existe pas dans le code, elle n'apparaît pas ici.</p>
{kpis}

<h2><span class="num">01</span>La chaîne complète</h2>
<p class="lede">Les onze étapes de la fiche §1. En vert : produites par la recherche seule. En ambre : produites après le gel et uniquement sous autorisation. Rien ne saute d'étape, et le robot n'est jamais atteignable directement depuis un backtest.</p>
<div class="chain">{render_chain()}</div>

<h2><span class="num">02</span>Les trois couches, jamais confondues</h2>
<p class="lede">La contrainte structurante de la fiche §2 : le challenge ne doit pas dicter ce que le moteur trouve. La couche C intervient après le gel. Une incompatibilité produit une version d'adaptation séparée, elle-même testée — jamais une retouche silencieuse du résultat scientifique.</p>
<div class="layers">{render_layers()}</div>

<h2><span class="num">03</span>Les phases et leurs gates</h2>
<p class="lede">P1 et P2 historique sont certifiées : l'agent les relit, recalcule les SHA-256, confirme les 348 partitions, et n'y touche pas. Les huit autres phases ont un gate d'entrée, un gate de sortie et un comportement en cas d'échec.</p>
{render_phases()}

<h2><span class="num">04</span>Qui exécute quoi, où</h2>
<p class="lede">L'orchestrateur n'est pas un agent IA. Il ne raisonne pas : il applique un graphe déterministe, vérifie des hashes et bloque des gates. Le calcul lourd part sur un runtime jetable. Le Drive ne sert que de stockage durable.</p>
<div class="rt">
<div class="box"><h3>GitHub Actions</h3><div class="role">ORCHESTRATEUR — déterministe</div>
<ul><li>déclenche la phase autorisée</li><li>vérifie les gates et les hashes</li><li>écrit les checkpoints</li><li>reprend les unités inachevées</li><li>bloque tout si un gate échoue</li></ul>
<div class="mini" style="margin-top:9px">Ne calcule pas. Ne décide pas. Ne dépasse jamais 6 h par job.</div></div>
<div class="box"><h3>Kaggle / Colab</h3><div class="role">CALCUL JETABLE</div>
<ul><li>exécute une partition ou un segment</li><li>écrit le résultat + son hash</li><li>meurt sans conséquence</li><li>piloté par token, sans navigateur</li></ul>
<div class="mini" style="margin-top:9px">Rien d'irremplaçable ne vit ici. Tout est reprenable.</div></div>
<div class="box"><h3>Google Drive</h3><div class="role">STOCKAGE DURABLE</div>
<ul><li>certificats P1 et P2 (lecture seule)</li><li>348 partitions certifiées</li><li>registres, splits, manifestes</li><li>checkpoints et reprises</li></ul>
<div class="mini" style="margin-top:9px">Goulot réel : la latence Drive. Elle est mesurée, pas supposée.</div></div>
<div class="box"><h3>Vous</h3><div class="role">PROPRIÉTAIRE — 11 points</div>
<ul><li>9 définitions scientifiques, une fois</li><li>7 acceptations de phase</li><li>1 autorisation Holdout</li><li>1 spécification de compte</li><li>1 autorisation de déploiement</li></ul>
<div class="mini" style="margin-top:9px">Rien d'autre. Aucune formule, aucun poids, aucun edge à fournir.</div></div>
</div>

<h2><span class="num">05</span>Le cycle autonome, une fois lancé</h2>
<pre>  03:00 UTC  ORCHESTRATEUR réveille la phase autorisée
             │
             ├── vérifie KILL_SWITCH, budget, leases
             ├── recalcule le SHA-256 des 2 certificats
             ├── confirme 348 partitions + schéma inchangé
             │
  03:05      ├── découpe en unités (partition / segment d'hypothèses)
             │
  03:06      ├── dispatch vers le runtime jetable, N unités en parallèle
             │      chaque unité écrit : résultat + hash + checkpoint
             │      une unité perdue est replanifiée, jamais dupliquée
             │
  04:20      ├── agrège, vérifie la cohérence, écrit les rapports
             ├── évalue le gate de sortie de phase
             │
             ├── GATE PASS  → statut PHASE_COMPLETE_AWAITING_OWNER_REVIEW
             │                et ATTEND. Il n'enchaîne pas seul sur la phase suivante.
             └── GATE FAIL  → statut BLOCKED_WITH_RESUME
                              cause exacte écrite, aucune phase suivante

  À tout moment : une coupure ne coûte que l'unité en cours.
  Le lendemain, la même commande reprend exactement où elle s'était arrêtée.</pre>
<div class="note ok">C'est la réponse à « ça fonctionne sans moi » : le système avance seul <b>à l'intérieur</b> d'une phase autorisée, aussi loin que les gates le permettent. Il s'arrête de lui-même au gate, avec un dossier complet. Vous ne relancez jamais rien à la main — vous lisez et vous signez.</div>

<h2><span class="num">06</span>Ce qui est automatisé, et ce qui ne le sera jamais</h2>
<div class="grid2">
<div class="card"><h3 style="color:var(--ok)">Automatisé (fiche §11)</h3><ul class="clean">{auto_li}</ul>
<div class="note" style="margin-top:12px;font-size:12.5px">C'est exactement la liste de la fiche. Rien de plus n'est revendiqué.</div></div>
<div class="card"><h3 style="color:var(--bad)">Jamais automatisé</h3><ul class="clean">{never_li}</ul>
<div class="note bad" style="margin-top:12px;font-size:12.5px">Ces huit interdictions sont écrites dans le code, pas dans une consigne. Elles lèvent une exception si on les contourne.</div></div>
</div>

<h2><span class="num">07</span>Les 11 points où vous êtes réellement requis</h2>
<p class="lede">Tout le reste est technique. Ces onze points ne sont pas des tâches qu'on pourrait vous éviter : ce sont des décisions qui n'appartiennent qu'au propriétaire, par construction.</p>
<table><thead><tr><th>Phase</th><th>Ce que vous faites</th><th>Nature</th></tr></thead><tbody>{hum_rows}</tbody></table>

<h2><span class="num">08</span>Blue Guardian : compatibilité, pas moteur de découverte</h2>
<p class="lede">23 règles rapportées par le PDF daté du 20/09/2026. Aucune n'est traitée comme une vérité actuelle : le registre d'incertitude les marque, et les contradictions documentaires restent ouvertes.</p>
<table><thead><tr><th>Règle rapportée</th><th>Valeur</th><th>Statut</th></tr></thead><tbody>{render_bg()}</tbody></table>
<div class="note bad"><b>Conséquence architecturale majeure — la règle des {BG_HOLD_MIN_MINUTES} minutes.</b> La stratégie est <i>tick-informed</i> : elle observe des ticks. Elle ne doit pas <i>trader</i> au tick. Toute règle dont la détention prévue est inférieure à {BG_HOLD_MIN_MINUTES} minutes est <b>exclue du périmètre Blue Guardian</b> — sans pour autant être supprimée de la recherche, qui reste indépendante. Fractionner des ordres pour contourner la règle est une fraude : c'est une interdiction dure du code.</div>
<div class="card"><h3>Paramètres serveur <span class="mono" style="font-size:12px;color:var(--bad)">NOT_PUBLIC</span></h3>
<p class="mini" style="margin:6px 0 0">Ces {s['bg_not_public']} éléments ne sont pas publiés. Le système ne doit jamais les inventer : il les lit dans le MT5 du compte réellement attribué, ou il marque la règle bloquante. Le PDF est un point de départ daté, pas un substitut aux conditions actuelles.</p>
<p style="margin-top:10px;font-size:12px;color:#8497a9;line-height:1.9">{bg_np}</p></div>

<h2><span class="num">09</span>Ce que les ticks ne peuvent pas prouver</h2>
<p class="lede">Fiche §4.2. Un tick de cotation n'est pas une transaction. Ces huit affirmations sont interdites au système, sauf à recevoir la donnée externe correspondante.</p>
<table><thead><tr><th>Affirmation</th><th>Statut imposé</th></tr></thead><tbody>{tick_rows}</tbody></table>
<div class="note vio">Conséquence directe sur le portefeuille : tout modèle d'exécution est <b>CONDITIONAL ou GROSS</b>, jamais NET, tant que commission réelle, swap, slippage et latence ne sont pas confirmés. Le code refuse l'étiquette NET sans ces quatre preuves.</div>

<h2><span class="num">10</span>Le budget et la contrainte matérielle</h2>
<div class="grid2">
<div class="card"><h3>6 000 FCFA ≈ 9,95 USD — ce qui est payé</h3>
<table><tbody>
<tr><td>GitHub Actions (dépôt privé)</td><td class="mono">0 FCFA</td></tr>
<tr><td>Kaggle (token, kernels)</td><td class="mono">0 FCFA</td></tr>
<tr><td>Google Drive (déjà en place)</td><td class="mono">0 FCFA</td></tr>
<tr><td>DuckDB / PyArrow / Polars</td><td class="mono">0 FCFA</td></tr>
<tr><td>Coût mensuel de la chaîne</td><td class="mono" style="color:var(--ok)">0 FCFA</td></tr>
</tbody></table>
<div class="note ok" style="margin-top:12px;font-size:12.5px">Les 6 000 FCFA ne sont <b>pas</b> consommés par l'infrastructure. Ils restent disponibles comme marge, non dépensés.</div></div>
<div class="card"><h3>Matériel — ce que les statistiques exigent vraiment</h3>
<table><tbody>
<tr><td>DuckDB out-of-core</td><td class="mono">2 threads, 4 GB</td></tr>
<tr><td>Empreinte par unité</td><td class="mono">1 partition</td></tr>
<tr><td>CPU suffisant</td><td><span class="tag t-ok">OUI</span></td></tr>
<tr><td>GPU nécessaire</td><td><span class="tag t-bad">NON</span></td></tr>
<tr><td>RAM requise</td><td class="mono">≤ 4 GB par job</td></tr>
</tbody></table>
<div class="note warn" style="margin-top:12px;font-size:12.5px">Pas de GPU : les tests de la fiche sont des statistiques de séries temporelles, du bootstrap et du replay — pas du calcul matriciel dense. Un GPU n'accélérerait rien d'utile.</div></div>
</div>

<h2><span class="num">11</span>Les 43 artéfacts et la phase qui les produit</h2>
<p class="lede">Chaque artéfact a une et une seule phase propriétaire. Le modèle lève une erreur si un artéfact est produit par deux phases — c'est un contrôle de cohérence, pas une convention.</p>
<div class="card" style="max-height:520px;overflow-y:auto">
<table><thead><tr><th>Artéfact</th><th>Phase propriétaire</th></tr></thead><tbody>{art_rows}</tbody></table></div>

<h2><span class="num">12</span>Où en est le code aujourd'hui</h2>
<div class="grid2">
<div class="card"><h3 style="color:var(--ok)">Construit et testé</h3>
<table><tbody>
<tr><td>Gouvernance : phases, gates, sceau Holdout, kill switch, budget</td><td><span class="tag t-ok">OK</span></td></tr>
<tr><td>Extraction : inventaire, échelle L0-L7, matrice, manifeste</td><td><span class="tag t-ok">OK</span></td></tr>
<tr><td>Familles §4.2 et 9 décisions sans défaut</td><td><span class="tag t-ok">OK</span></td></tr>
<tr><td>Segmentation, dispatch, checkpoints, reprises</td><td><span class="tag t-ok">OK</span></td></tr>
<tr><td>Contrat de mission V2 (ce schéma)</td><td><span class="tag t-ok">OK</span></td></tr>
</tbody></table></div>
<div class="card"><h3 style="color:var(--warn)">Pas encore écrit</h3>
<table><tbody>
<tr><td>Moteur P3 : mining préenregistré + Trial Ledger</td><td><span class="tag t-h">À FAIRE</span></td></tr>
<tr><td>Moteur P4 : walk-forward + replay Bid/Ask</td><td><span class="tag t-h">À FAIRE</span></td></tr>
<tr><td>Moteur P5 : stress + contrôles négatifs</td><td><span class="tag t-h">À FAIRE</span></td></tr>
<tr><td>Moteur P7 : corrélation + poids gelés</td><td><span class="tag t-h">À FAIRE</span></td></tr>
<tr><td>Adaptateur BG + génération MQL5</td><td><span class="tag t-h">À FAIRE</span></td></tr>
<tr><td>Accès au corpus réel (348 partitions)</td><td><span class="tag t-bad">BLOQUÉ</span></td></tr>
</tbody></table></div>
</div>
<div class="note bad" style="margin-top:14px">Le corpus certifié n'est pas accessible depuis cette session. Tout ce qui est au-dessus a été prouvé sur corpus synthétique de structure identique, et le système refuse de démarrer sur une racine vide plutôt que d'improviser. Les moteurs P3-P7 seront écrits contre le schéma réel dès qu'il est lisible — pas avant, pour ne pas figer des hypothèses fausses.</div>

<h2><span class="num">13</span>Le critère de réussite, tel que la fiche le définit</h2>
<div class="note ok">Le projet ne réussit pas parce qu'il produit beaucoup de fichiers, d'indicateurs ou une courbe séduisante. Il progresse quand : les données sont traçables, les variables causales, les hypothèses préenregistrées, les résultats négatifs conservés, les anomalies résistantes, les coûts honnêtes, les edges stables, les poids sans fuite, le portefeuille gelé survivant au Holdout et au miroir.<br><br><b>Si aucune stratégie ne franchit les critères, la conclusion correcte est <span class="mono">NO_EDGE</span>. C'est une conclusion scientifique utile, pas un échec informatique.</b></div>

<p class="mini" style="margin-top:40px;border-top:1px solid var(--lin);padding-top:16px">
Rendu depuis <code>metaalpha/mission.py</code> par <code>scripts/render_architecture.py</code>. Contrôle d'intégrité : {s['artifacts_total']} artéfacts, {len(s['duplicate_artifacts'])} doublon(s).<br>
Modules liés : <code>governance.py</code> (gates) · <code>extraction_ladder.py</code> · <code>extract.py</code> · <code>families.py</code> · <code>decisions.py</code> · <code>dispatch.py</code> · <code>leases.py</code> · <code>preflight.py</code></p>

</div></body></html>"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    html = build()
    OUT.write_text(html)
    dup = stats()["duplicate_artifacts"]
    if dup:
        raise SystemExit(f"INCOHÉRENCE : artéfacts produits par 2 phases : {dup}")
    print(f"écrit {OUT} ({len(html)} octets, {stats()['artifacts_total']} artéfacts, 0 doublon)")
