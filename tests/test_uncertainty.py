import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from ere.uncertainty import partial_identification_bounds, classify_data_reliability, prioritize_experiments

def test_bounds_are_partial_not_point():
    lo, hi = partial_identification_bounds({"UTC": -0.1, "GMT+2": 25.6, "GMT+3": -2.0})
    assert lo == -2.0 and hi == 25.6

def test_reliability_classification():
    assert classify_data_reliability({"instrument":1,"side":1,"open_time":1}) == "UTILISABLE_AVEC_RESERVES"
    assert classify_data_reliability({"side":1,"open_time":1}) == "INSUFFISANT_POUR_IDENTIFICATION"
    assert classify_data_reliability({"instrument":1,"side":1,"open_time":1,"timezone":"UTC","open_price":1}) == "UTILISABLE"

def test_prioritization_blocks_without_segment():
    out = prioritize_experiments([{"nom":"a","hypotheses_departagees":3,"cout_relatif":1.0,"segment_disponible":False},
                                  {"nom":"b","hypotheses_departagees":2,"cout_relatif":1.0,"segment_disponible":True}])
    assert out[0]["nom"] == "b" and out[1]["bloque"] is not None
