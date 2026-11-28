"""Tranche verticale synthétique ERE (Phase 5).

Parcours complet A->I sur données 100% synthétiques. Le système doit
pouvoir conclure NOT_IDENTIFIED / COMPATIBLE MAIS NON IDENTIFIÉ :
aucun verdict positif n'est fabriqué pour démontrer le pipeline.
"""
from __future__ import annotations

import json
import math
import pathlib

from .engines import (EngineF, engine_a_ingest, engine_b_profile, engine_c_hypotheses,
                      engine_d_knowledge, engine_e_design, engine_g_identify,
                      engine_h_gate, engine_ib_portfolio)
from .runner import TaskRunner


def synthetic_ticks(n: int = 4000, seed: int = 11) -> list:
    # Marche déterministe avec chutes et récupérations (aucune donnée réelle).
    ticks, price = [], 2000.0
    for i in range(n):
        price += 0.05 * math.sin(i / 37.0) - (0.9 if i % 401 == 200 else 0.0) + (0.9 if i % 401 == 260 else 0.0)
        ticks.append((i * 5, price))
    return ticks


def run(workdir: str) -> dict:
    trades = [
        {"side": "buy", "open_time": "fictif-t0", "close_time": "fictif-t3"},
        {"side": "buy", "open_time": "fictif-t1", "close_time": "fictif-t3"},
        {"side": "buy", "open_time": "fictif-t2", "close_time": "fictif-t3"},
    ]
    dossier = engine_a_ingest(trades, [{"texte": "+2000% annoncé (fictif)"}],
                              ["capital", "historique complet", "commissions"])
    profil = engine_b_profile(dossier)
    hypotheses = engine_c_hypotheses(profil)
    knowledge = engine_d_knowledge(["retour", "queues"])
    f = EngineF(["partition_synthetique_001"])
    plan = engine_e_design(hypotheses, f.catalog())
    runner = TaskRunner(workdir, {"slice": "verticale-v1", "plan_hash": plan.plan_hash})
    reports = []
    def _shard(_sid):
        reports.append(f.execute(plan, synthetic_ticks()))
        return "MEASURED" if reports[-1].status == "MEASURED" else "NOT_EXECUTED"
    manifest = runner.run_shards(["shard-001"], _shard)
    g = engine_g_identify(hypotheses, reports, plan)
    try:
        engine_h_gate(g, {"approbateur": "fondateur"})
        porte_h = "OUVERTE"
    except PermissionError as e:
        porte_h = f"FERMÉE ({e})"
    portfolio = engine_ib_portfolio([])
    verdict = "NOT_IDENTIFIED" if g.qualification == "COMPATIBLE MAIS NON IDENTIFIÉ" else g.qualification
    proof = {
        "type": "TRANCHE_VERTICALE_SYNTHETIQUE",
        "donnees": "100% synthétiques, aucun tick réel, aucun trader réel",
        "etapes": {
            "A_transactions": len(trades), "A_claims_non_verifiees": len(dossier.claims),
            "B_faits": len(profil.facts), "B_interpretations": len(profil.interpretations),
            "C_hypotheses": len(hypotheses.hypotheses), "C_inconnu_inclus": hypotheses.includes_unknown,
            "D_methodes": [c["method_id"] for c in knowledge],
            "E_avis": plan.avis.valeur, "E_plan_hash": plan.plan_hash,
            "F_statut": reports[0].status if reports else "AUCUN",
            "F_mesures": reports[0].mesures if reports else None,
            "G_qualification": g.qualification, "porte_H": porte_h,
            "I-B_sources_admises": portfolio["n"],
        },
        "verdict_final": verdict,
        "run_manifest": manifest,
    }
    out = pathlib.Path(workdir) / "vertical_slice_proof.json"
    out.write_text(json.dumps(proof, indent=1, ensure_ascii=False))
    return proof


if __name__ == "__main__":
    print(json.dumps(run("/tmp/ere-vertical-slice"), indent=1, ensure_ascii=False))
