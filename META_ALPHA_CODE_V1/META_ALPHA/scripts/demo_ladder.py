"""Démo : la chaîne complète, sans intervention humaine sauf L5."""
import pathlib, tempfile
from tests.test_extraction_ladder import _make_corpus, _register
from metaalpha.fs import Storage
from metaalpha.extraction_ladder import advance
from metaalpha.decisions import record_answers
from metaalpha.extract import run_extraction, build_manifest
from metaalpha.inventory import build_inventory

tmp = pathlib.Path(tempfile.mkdtemp())
st = Storage.open(tmp / "META_ALPHA_RESEARCH")
raw = tmp / "corpus"; raw.mkdir()
parts = _make_corpus(raw, months=3, rows=1200)

print("### PAS 1 — le système monte seul, sans aucune intervention")
rep = advance(st, raw)
print(f"  fichiers        : {rep['inventory']['files_found']}")
print(f"  lignes          : {rep['inventory']['total_rows']:,}")
print(f"  schémas         : {len(rep['inventory']['schema_signatures'])}")
for line in rep["log"]:
    print("  " + line)
print(f"\n  barreau atteint : {rep['ladder']['current_level']}")
print(f"  suivant         : {rep['ladder']['next_level']['level']}")
print(f"  qui agit        : {rep['ladder']['who_acts_next']}")
print(f"  pourquoi        : {rep['ladder']['why']}")

print("\n### PAS 2 — le propriétaire répond une seule fois (~10 min)")
res = record_answers(st, {
    "D_HORIZONS": "5min", "D_FENETRES_VOL": "500", "D_WARMUP_NULL": "NULL",
    "D_SEUIL_SAUT": "4", "D_INTENSITE_T": "5s",
    "D_REGIME_SPREAD": "3 classes / 1 jour", "D_TIMEZONE_SESSIONS": "UTC + aucune session",
    "D_METHODE_REGIME": "DEFERRED", "D_HORIZON_LABEL": "30s",
})
print(f"  variables instanciées : {res['variables_instantiated']}")

print("\n### PAS 3 — le système reprend seul : extraction + scellement")
_register(st, "MID"); _register(st, "SPREAD_ABS"); _register(st, "RET_TICK")
inv = build_inventory(raw)
ext = run_extraction(st, inv["partitions"])
print(f"  partitions extraites  : {ext['extracted_now']}  (échecs : {ext['failed']})")
print(f"  variables refusées    : {[r['variable_id'] + ' ← ' + r['cause'] for r in ext['plan']['refused']]}")
man = build_manifest(st)
print(f"  manifeste             : {man['manifest_sha256'][:16]}…  ({man['total_rows']:,} lignes)")

print("\n### PAS 4 — relance : il ne refait rien")
ext2 = run_extraction(st, inv["partitions"])
print(f"  ré-extrait : {ext2['extracted_now']}   ignoré (déjà fait) : {ext2['skipped_already_done']}")

print("\n### PAS 5 — l'échelle reconnaît le sommet")
final = advance(st, raw)
for s in final["ladder"]["states"]:
    mark = "OK " if s["reached"] else "·  "
    auto = "auto" if s["automatic"] else "HUMAIN"
    print(f"  {mark}{s['level']:22s} {auto:6s} {s['cost']}")
print(f"\n  barreau final : {final['ladder']['current_level']}")
print(f"  qui agit      : {final['ladder']['who_acts_next']}")
