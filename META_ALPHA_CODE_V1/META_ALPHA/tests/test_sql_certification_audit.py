"""Certification individuelle des traductions SQL remediees (audit proprietaire).
Chaque SQL est EXECUTE par DuckDB sur donnees controlees et compare a une
reference Python independante: formule, NULL de warm-up, frontieres, causalite."""
import math
import pytest
from metaalpha.extract import _expr_for
from metaalpha.duck import connect

ROWS=[(0,100.0,100.4),(2,101.0,101.4),(5,99.0,99.4),(9,102.0,102.4),(20,98.0,98.4)]
def run(sql):
    with connect(memory_limit="1GB", threads=1) as con:
        con.execute("CREATE TABLE base AS SELECT * FROM (VALUES "+
            ",".join(f"(TIMESTAMP '2026-01-01 00:00:{s:02d}',{b},{a})" for s,b,a in ROWS)+") v(t,bid,ask)")
        return [float(r[0]) if r[0] is not None else None for r in con.execute(f"SELECT {sql} FROM base ORDER BY t").fetchall()]

def test_mid_spread_certifies():
    assert run(_expr_for("MID",{}))==pytest.approx([100.2,101.2,99.2,102.2,98.2])
    assert run(_expr_for("SPREAD_ABS",{}))==pytest.approx([0.4]*5)
def test_ret_tick_causal_et_null():
    r=run(_expr_for("RET_TICK",{})); assert r[0] is None
    assert r[1]==pytest.approx(101.2/100.2-1) and r[2]==pytest.approx(99.2/101.2-1)
def test_roll_range_par_fenetre_null_warmup():
    r=run(_expr_for("ROLL_RANGE_MID",{"N":3}))
    assert r[0] is None and r[1] is None and r[2]==pytest.approx(2.0) and r[3]==pytest.approx(3.0)
def test_update_intensity_fenetre_temps():
    # convention certifiee: intervalle FERME [t-T, t] (RANGE DuckDB inclusif aux deux bornes)
    assert run(_expr_for("UPDATE_INTENSITY",{"T":5}))==[1,2,3,2,1]
    assert run(_expr_for("UPDATE_INTENSITY",{"T":30}))==[1,2,3,4,5]
def test_interarrival_mean_telescopique_null():
    r=run(_expr_for("INTERARRIVAL_MEAN",{"N":2}))
    assert r[0] is None and r[1] is None
    assert r[2]==pytest.approx((5-0)/2) and r[3]==pytest.approx((9-2)/2) and r[4]==pytest.approx((20-5)/2)
def test_anti_lookahead_sql_perturbation():
    sql=_expr_for("ROLL_RANGE_MID",{"N":3})
    a=run(sql)
    with connect(memory_limit="1GB", threads=1) as con:
        con.execute("CREATE TABLE base AS SELECT * FROM (VALUES (TIMESTAMP '2026-01-01 00:00:00',100.0,100.4),(TIMESTAMP '2026-01-01 00:00:02',101.0,101.4),(TIMESTAMP '2026-01-01 00:00:05',99.0,99.4),(TIMESTAMP '2026-01-01 00:00:09',9999.0,9999.4)) v(t,bid,ask)")
        b=[float(r[0]) if r[0] is not None else None for r in con.execute(f"SELECT {sql} FROM base ORDER BY t").fetchall()]
    assert a[:3]==b[:3]
def test_ret_h_horizon_illisible_refuse():
    with pytest.raises(Exception):
        _expr_for("RET_H",{"H":"bientot"})

def run_enriched(sql):
    with connect(memory_limit="1GB", threads=1) as con:
        con.execute("CREATE TABLE base AS SELECT * FROM (VALUES "+
            ",".join(f"(TIMESTAMP '2026-01-01 00:00:{s:02d}',{b},{a})" for s,b,a in ROWS)+") v(t,bid,ask)")
        q=f"""WITH with_mid AS (SELECT t,bid,ask,((ask+bid)/2.0) AS mid FROM base),
        enriched AS (SELECT t,bid,ask,mid,(mid/NULLIF(lag(mid) OVER (ORDER BY t),0)-1) AS ret_mid FROM with_mid)
        SELECT {sql} FROM enriched e ORDER BY t"""
        return [float(r[0]) if r[0] is not None else None for r in con.execute(q).fetchall()]

def test_roll_std_sur_rendements_pas_niveaux():
    # rendements mid: 101.2/100.2-1, 99.2/101.2-1, 102.2/99.2-1, 98.2/102.2-1
    import statistics
    mids=[100.2,101.2,99.2,102.2,98.2]; rets=[mids[i]/mids[i-1]-1 for i in range(1,5)]
    r=run_enriched(_expr_for("ROLL_STD_MID",{"N":2}))
    assert r[0] is None and r[1] is None  # warm-up: 2 rendements requis, 1re valeur au 3e evenement
    assert r[2]==pytest.approx(statistics.stdev(rets[0:2]))
    assert r[3]==pytest.approx(statistics.stdev(rets[1:3]))
    assert r[4]==pytest.approx(statistics.stdev(rets[2:4]))
def test_ret_h_alignement_valide():
    # H=5s: origines 0->tick a 5 (99.2), 2->tick a 9 (102.2), 5->tick a 20 (98.2), 9->tick a 20, 20->NULL
    r=run_enriched(_expr_for("RET_H",{"H":"5s"}))
    assert r[0]==pytest.approx((99.2-100.2)/100.2)
    assert r[1]==pytest.approx((102.2-101.2)/101.2)
    assert r[2]==pytest.approx((98.2-99.2)/99.2)
    assert r[4] is None  # horizon incomplet: NULL, jamais interpole

def test_ret_h_est_un_label_jamais_une_feature():
    from metaalpha.fs import Storage
    from metaalpha.extract import plan_extraction
    import os
    root=os.environ.get("METAALPHA_AUDIT_ROOT")
    if not root:
        pytest.skip("registre proprietaire non monte dans ce contexte")
    plan=plan_extraction(Storage.open(root))
    kinds={e["variable_id"]: e.get("kind") for e in plan["extractible"]}
    assert kinds.get("RET_H")=="label"
