"""Démo de bout en bout : le système instancie les familles SEUL."""
import json, pathlib, tempfile, random, datetime as dt
import pyarrow as pa, pyarrow.parquet as pq
from metaalpha.fs import Storage
from metaalpha.contracts_engine import detect_fields, derive_sample, build_phase2_contract_report
from metaalpha.decisions import record_answers, answer_template

root = pathlib.Path(tempfile.mkdtemp()) / "META_ALPHA_RESEARCH"
root.mkdir(parents=True)
part = root / "corpus" / "XAUUSD" / "2024" / "2024-01.parquet"
part.parent.mkdir(parents=True)
random.seed(7)
n, t, bid = 5000, dt.datetime(2024, 1, 2, tzinfo=dt.timezone.utc), 2063.40
ts, bids, asks = [], [], []
for i in range(n):
    t += dt.timedelta(milliseconds=random.randint(80, 900))
    bid += random.gauss(0, 0.06)
    ts.append(t); bids.append(round(bid, 2)); asks.append(round(bid + random.uniform(0.12, 0.45), 2))
pq.write_table(pa.table({"timestamp": ts, "bid": bids, "ask": asks}), part)

s = Storage.open(root)
schema = detect_fields(["timestamp", "bid", "ask"])
sample = derive_sample(part, schema, max_events=5000)
report = build_phase2_contract_report(schema=schema, sample=sample)
print("=== ÉTAT DES 8 FAMILLES ===")
for f in report["families"]:
    print(f"  {f['family_id']:24s} {f['status']:22s} {len(f['variables'])} vars")
print("\n=== QUESTIONS IRRÉDUCTIBLES ===")
for q in report["questions_for_owner"]:
    print(f"  {q['decision_id']:22s} bloque {q['blocks']}")
print(f"\néchantillon borné : {report['sample_measurement']['events_measured']} événements")
print("dérivables sans décision :", report["variables_derivable_now"])
print("bloqués par une décision  :", report["variables_blocked"])
print("phase_status :", report["phase_status"])

# 1. le propriétaire répond à 3 des 9 questions
res = record_answers(s, {"D_FENETRES_VOL": "500", "D_WARMUP_NULL": "NULL", "D_SEUIL_SAUT": "4"})
print("\n=== APRÈS 3 RÉPONSES ===")
print("  instanciées :", res["variables_instantiated"])

# 2. le système recalcule seul l'échantillon avec les nouvelles variables
smp = derive_sample(part, report["schema_detection"], max_events=5000)
print("  échantillon recalculé :", smp["status"], smp["events_measured"])

tpl = answer_template()
(pathlib.Path(".") / "00_GOVERNANCE").mkdir(exist_ok=True)
(pathlib.Path(".") / "00_GOVERNANCE" / "OWNER_DECISIONS_TEMPLATE.json").write_text(json.dumps(tpl, indent=2, ensure_ascii=False))
print("\ntemplate écrit : 00_GOVERNANCE/OWNER_DECISIONS_TEMPLATE.json")
print(json.dumps({k: tpl["answers"][k] for k in list(tpl["answers"])[:2]}, indent=2, ensure_ascii=False)[:600])
