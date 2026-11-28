import sys, pathlib, tempfile, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from ere.kernel import Kernel, BudgetExceeded
from ere.cycle import run_cycle
from ere.forecast import evaluate_coverage

def test_kernel_idempotent_resume_and_journal():
    with tempfile.TemporaryDirectory() as td:
        k = Kernel(f"{td}/k.db")
        t1 = k.create_task("x", {"a": 1}); t2 = k.create_task("x", {"a": 1})
        assert t1 == t2  # pas de duplication
        k.transition(t1, "RUNNING")
        assert k.resume_interrupted() == [t1] and k.pending() == [t1]
        assert k.verify_journal()

def test_knowledge_stale_keeps_history():
    with tempfile.TemporaryDirectory() as td:
        k = Kernel(f"{td}/k.db")
        k.put_knowledge("vol", {"v": 1}); k.put_knowledge("vol", {"v": 2}, supersedes="vol")
        assert k.knowledge("vol")["body"]["v"] == 2
        k.mark_stale("vol", "rupture prouvee"); assert k.knowledge("vol")["status"] == "STALE"

def test_cycle_no_signal_world():
    rng = random.Random(3)
    rets = [rng.gauss(0, 1) for _ in range(600)]
    with tempfile.TemporaryDirectory() as td:
        out = run_cycle(Kernel(f"{td}/k.db"), rets, "monde-sans-signal")
        assert out["qualification"] == "NOT_IDENTIFIED" and out["verdicts"]["H-NULLE"] == "RETENUE"
        assert out["prochaine_recherche"] != "ouvrir_segment_protege"

def test_cycle_volatility_regime_world():
    rng = random.Random(5); rets = []; vol = 0.3
    for i in range(600):
        if i % 100 == 0: vol = 2.0 if vol < 1 else 0.3
        rets.append(rng.gauss(0, vol))
    with tempfile.TemporaryDirectory() as td:
        out = run_cycle(Kernel(f"{td}/k.db"), rets, "monde-regimes-vol")
        assert out["verdicts"]["H-REGIME-VOL"] == "RETENUE"

def test_forecast_coverage_no_leakage_structure():
    rng = random.Random(7)
    rets = [rng.gauss(0, 1) for _ in range(500)]
    out = evaluate_coverage(rets, window=200)
    assert out["n_previsions"] == 300 and 60 <= out["couverture_q10_q90_pct"] <= 95
