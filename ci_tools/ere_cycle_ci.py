"""Cycle ERE en CI (Phase 7): l'etat du noyau voyage par Git.

Le snapshot SQLite n'est jamais commite tel quel (binaire, conflits);
l'etat transfere est un export JSON verifiable (missions, taches,
hypotheses, tete du journal chaine), reconstruit a chaque cycle.
Idempotent: rejouer le meme export ne duplique ni tache ni publication
(cles = hash de spec / canon d'hypothese). Aucun acces ME-001.
"""
import json, pathlib, sys
sys.path.insert(0, '.')
from ere.kernel import Kernel

STATE = pathlib.Path('reports/meta_alpha/ere_state/STATE.json')
DB = '/tmp/ere_cycle.db'

def export_state(k, missions):
    out = {"missions": [], "journal_head_count": k.db.execute("SELECT COUNT(*) FROM events").fetchone()[0],
           "publications": k.publication_count()}
    for mid in missions:
        m = k.mission(mid)
        out["missions"].append({**m, "open_hypotheses": k.open_hypotheses(mid),
                                "meta_research_task": k.ensure_meta_research(mid)})
    return out

def main():
    prev = json.loads(STATE.read_text()) if STATE.exists() else {"missions": []}
    k = Kernel(DB)
    ids = []
    if not prev["missions"]:  # amorcage: deux flux separes (§8 de la mission)
        ids = [k.create_mission("Identifier un mecanisme economique XAUUSD reproductible (flux marche)", "B"),
               k.create_mission("Comprendre les comportements trader observes et leurs inconnues (flux trader)", "A")]
    else:
        for m in prev["missions"]:
            ids.append(k.create_mission(m["objective"], m["stream"]))  # idempotent par hash
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(export_state(k, ids), indent=1, sort_keys=True))
    print(json.dumps(export_state(k, ids), indent=1, sort_keys=True))

if __name__ == '__main__':
    main()
