import sys, pathlib, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from ere.vertical_slice import run

def test_vertical_slice_concludes_not_identified():
    with tempfile.TemporaryDirectory() as td:
        p = run(td)
        assert p["verdict_final"] == "NOT_IDENTIFIED"
        assert p["etapes"]["porte_H"].startswith("FERMÉE")
        assert p["etapes"]["I-B_sources_admises"] == 0
        assert p["etapes"]["C_inconnu_inclus"] is True
