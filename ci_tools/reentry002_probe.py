#!/usr/bin/env python3
"""RE-ENTRY-002 — sonde de la page publique HFM strategy-view (99001292).
Objectif: trouver le mecanisme de pagination de 'Trading Activity' (endpoint/API)
pour constituer une base de paniers reels. Aucun contournement: requetes publiques
ordinaires, journalisation complete des statuts."""
import json, pathlib, re
import requests

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'research' / 'RE-ENTRY-002'
URL = 'https://www.hfm.com/int/en/copy-trading/strategy-view?account=99001292'
s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 META-ALPHA-research'
res = {}
try:
    r = s.get(URL, timeout=60); res['page'] = {'http': r.status_code, 'octets': len(r.text)}
    (OUT / 'raw_strategy_view.html').write_text(r.text)
    mots = sorted(set(re.findall(r'https?://[^"\']*(?:api|activity|trading|history)[^"\']*', r.text, re.I)))[:40]
    res['urls_candidates'] = mots
    res['mentions'] = {m: len(re.findall(m, r.text, re.I)) for m in ('api', 'ajax', 'page=', 'loadmore', 'load_more', 'DataTable', 'activity')}
    lignes = [l.strip()[:200] for l in r.text.splitlines() if re.search(r'api|ajax|activity', l, re.I)][:30]
    res['lignes_pertinentes'] = lignes
except Exception as e:
    res['erreur'] = f'{type(e).__name__}: {e}'
(OUT / 'PROBE.json').write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False)[:4000])
