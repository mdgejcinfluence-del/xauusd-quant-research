import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from ere.engines import (engine_a_ingest, engine_b_profile, engine_c_hypotheses, engine_d_knowledge,
    engine_e_design, engine_g_identify, engine_h_gate, engine_ib_portfolio, EngineF)
from ere.runner import TaskRunner
import tempfile

TRADES = [{"side":"buy","open_time":"t0","close_time":"t3"},{"side":"buy","open_time":"t1","close_time":"t3"}]

def test_pipeline_to_not_identified():
    d = engine_a_ingest(TRADES, [{"texte":"+2000% annonce"}], ["capital","historique complet"])
    assert d.claims[0]["verified"] is False
    p = engine_b_profile(d); s = engine_c_hypotheses(p)
    assert len(s.hypotheses) >= 2 and s.includes_unknown
    assert engine_d_knowledge(["queues"])
    f = EngineF(["partition_synthetique"])
    plan = engine_e_design(s, f.catalog())
    rep = f.execute(plan, [(i*5, 2000.0) for i in range(50)])
    g = engine_g_identify(s, [rep], plan)
    assert g.qualification == "COMPATIBLE MAIS NON IDENTIFIÉ" and not g.candidat_h
    with pytest.raises(PermissionError): engine_h_gate(g, {"approbateur":"fondateur"})
    assert engine_ib_portfolio([])["n"] == 0

def test_non_testable_requires_g_countersign():
    d = engine_a_ingest(TRADES, [], []); s = engine_c_hypotheses(engine_b_profile(d))
    plan = engine_e_design(s, EngineF([]).catalog())
    assert plan.avis.valeur == "NON_TESTABLE_EN_L_ETAT"
    with pytest.raises(ValueError): engine_g_identify(s, [], plan, countersign_non_testable=False)
    g = engine_g_identify(s, [], plan, countersign_non_testable=True)
    assert g.qualification.startswith("NON DÉMONTRABLE")

def test_runner_idempotent_and_resumes(tmp_path=None):
    with tempfile.TemporaryDirectory() as td:
        spec = {"tache":"synthetique","version":1}
        calls = []
        r1 = TaskRunner(td, spec); m1 = r1.run_shards(["s1","s2"], lambda s: calls.append(s) or s.upper())
        r2 = TaskRunner(td, spec); m2 = r2.run_shards(["s1","s2"], lambda s: calls.append(s) or s.upper())
        assert calls == ["s1","s2"] and m1["task_hash"] == m2["task_hash"]
