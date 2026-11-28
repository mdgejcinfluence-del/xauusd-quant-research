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
           "publications": k.publication_count(),
           "blocages": [
             {"id": "REVEIL-AUTONOME", "cause": "GitHub n'execute schedule/workflow_dispatch que depuis la branche par defaut; main protegee sans autorisation de modification; les poussees du bot (GITHUB_TOKEN) ne declenchent pas de workflows",
              "condition_resolution": "autorisation fondateur: workflow planifie minimal sur main OU declencheur externe autorise", "statut": "BLOQUE_PAR_AUTORISATION"},
             {"id": "PARTITIONS-2021-2026", "cause": "Drive renvoie des interstitiels de 2040 octets (quota/rate-limit) pour 14 partitions 2021-2026 non migrees vers Kaggle; les partitions IS ont ete recuperees via Kaggle avec SHA verifies (8 recuperees)",
              "condition_resolution": "reset du quota Drive ou source autorisee equivalente; reprise idempotente prete (ci_tools/ere_golive_ci.py)", "statut": "EN_ATTENTE_CONDITION_EXTERNE"}]}
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
