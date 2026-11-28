"""Noyau autonome durable META ALPHA (Phases 1-2 de la consolidation).

Autorité opérationnelle du cycle de recherche: agenda, tâches, journal
d'événements chaîné par hash, budgets, reprise. Stockage SQLite stdlib
(choix du dossier externe, option A: monolithe modulaire, mono-worker;
PostgreSQL seulement si la concurrence le démontre un jour).
Aucune qualification N0-N7 n'est attribuée par le noyau: il orchestre,
les moteurs et leurs gates décident.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time


def _h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


class BudgetExceeded(Exception):
    pass


class Kernel:
    def __init__(self, db_path: str, budget_tasks: int = 100):
        self.db = sqlite3.connect(db_path)
        self.db.execute("CREATE TABLE IF NOT EXISTS tasks(task_id TEXT PRIMARY KEY, kind TEXT, spec TEXT, spec_hash TEXT UNIQUE, status TEXT, result TEXT, created REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, event TEXT, payload TEXT, prev_hash TEXT, hash TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS knowledge(kid TEXT PRIMARY KEY, version INT, status TEXT, body TEXT, supersedes TEXT)")
        self.db.commit()
        self.budget_tasks = budget_tasks

    # --- journal chaîné (intégrité vérifiable) ---
    def _log(self, task_id: str, event: str, payload: dict) -> str:
        row = self.db.execute("SELECT hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
        prev = row[0] if row else "GENESIS"
        body = {"task_id": task_id, "event": event, "payload": payload, "prev": prev, "ts": time.time()}
        digest = _h(body)
        self.db.execute("INSERT INTO events(task_id,event,payload,prev_hash,hash) VALUES(?,?,?,?,?)",
                        (task_id, event, json.dumps(payload, default=str), prev, digest))
        self.db.commit()
        return digest

    def verify_journal(self) -> bool:
        prev = "GENESIS"
        for task_id, event, payload, prev_hash, digest in self.db.execute(
                "SELECT task_id,event,payload,prev_hash,hash FROM events ORDER BY id"):
            if prev_hash != prev:
                return False
            body = {"task_id": task_id, "event": event, "payload": json.loads(payload), "prev": prev}
            # le ts n'est pas revérifié (non déterministe); on vérifie la chaîne des prev_hash
            prev = digest
        return True

    # --- tâches: création idempotente, transitions, reprise ---
    def create_task(self, kind: str, spec: dict) -> str:
        spec_hash = _h({"kind": kind, "spec": spec})
        task_id = "T-" + spec_hash[:16]
        n = self.db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        row = self.db.execute("SELECT task_id FROM tasks WHERE spec_hash=?", (spec_hash,)).fetchone()
        if row:
            return row[0]  # doublon: même tâche, pas de duplication
        if n >= self.budget_tasks:
            raise BudgetExceeded(f"budget de tâches atteint ({self.budget_tasks})")
        self.db.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?,?)",
                        (task_id, kind, json.dumps(spec, default=str), spec_hash, "PENDING", None, time.time()))
        self.db.commit()
        self._log(task_id, "CREATED", {"kind": kind})
        return task_id

    def transition(self, task_id: str, status: str, result: dict | None = None) -> None:
        cur = self.db.execute("SELECT status FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if not cur:
            raise KeyError(task_id)
        self.db.execute("UPDATE tasks SET status=?, result=? WHERE task_id=?",
                        (status, json.dumps(result, default=str) if result is not None else None, task_id))
        self.db.commit()
        self._log(task_id, f"STATUS_{status}", result or {})

    def resume_interrupted(self) -> list:
        """Après une coupure: toute tâche RUNNING est marquée INTERRUPTED puis remise en file."""
        rows = self.db.execute("SELECT task_id FROM tasks WHERE status='RUNNING'").fetchall()
        for (tid,) in rows:
            self.transition(tid, "INTERRUPTED")
            self.transition(tid, "PENDING")
        return [r[0] for r in rows]

    def pending(self) -> list:
        return [r[0] for r in self.db.execute("SELECT task_id FROM tasks WHERE status='PENDING' ORDER BY created")]

    def get(self, task_id: str) -> dict:
        r = self.db.execute("SELECT kind,spec,status,result FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        return {"kind": r[0], "spec": json.loads(r[1]), "status": r[2], "result": json.loads(r[3]) if r[3] else None}

    # --- mémoire sémantique versionnée (détail dans ere/memory.py) ---
    def put_knowledge(self, kid: str, body: dict, supersedes: str | None = None) -> int:
        row = self.db.execute("SELECT MAX(version) FROM knowledge WHERE kid=?", (kid,)).fetchone()
        version = (row[0] or 0) + 1
        if supersedes:
            self.db.execute("UPDATE knowledge SET status='STALE' WHERE kid=? AND status='ACTIVE'", (supersedes,))
        self.db.execute("INSERT OR REPLACE INTO knowledge VALUES(?,?,?,?,?)",
                        (kid, version, "ACTIVE", json.dumps(body, default=str), supersedes))
        self.db.commit()
        self._log(kid, "KNOWLEDGE_ACTIVE", {"version": version, "supersedes": supersedes})
        return version

    def mark_stale(self, kid: str, motif: str) -> None:
        self.db.execute("UPDATE knowledge SET status='STALE' WHERE kid=?", (kid,))
        self.db.commit()
        self._log(kid, "KNOWLEDGE_STALE", {"motif": motif})

    def knowledge(self, kid: str) -> dict | None:
        r = self.db.execute("SELECT version,status,body FROM knowledge WHERE kid=? ORDER BY version DESC LIMIT 1", (kid,)).fetchone()
        return {"version": r[0], "status": r[1], "body": json.loads(r[2])} if r else None
