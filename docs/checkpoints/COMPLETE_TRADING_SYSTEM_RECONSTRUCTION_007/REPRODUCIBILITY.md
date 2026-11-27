# CTRS-007 — REPRODUCTIBILITÉ

```
git rev-parse HEAD            # 3589a61 au départ de CTRS-007 (seq472)
/tmp/metaalpha-venv/bin/python ci_tools/emi006_lab.py
/tmp/metaalpha-venv/bin/python docs/checkpoints/EXIT_MECHANISM_IDENTIFICATION_006/EXIT_ENGINE_TESTS.py
/tmp/metaalpha-venv/bin/python ci_tools/ctrs007_finalize.py
/tmp/metaalpha-venv/bin/python ci_tools/test_ctrs007.py
```

Entrées gelées : trajectoires DIRR-003, checkpoints EIDR-005/EMI-006,
moteurs V1/V2 intouchés. Manifeste `MANIFEST_SHA256.json` vérifiable.
Préenregistrement seq472, résultats seq473.
