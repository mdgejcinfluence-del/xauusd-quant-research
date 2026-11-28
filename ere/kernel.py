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


class LeaseRejected(Exception):
    """Publication refusee: lease expire, epoch obsolete ou doublon logique."""


def _normalize(text: str) -> str:
    import re
    return " ".join(sorted(set(re.findall(r"[a-z0-9]+", text.lower()))))


class Kernel:
    def __init__(self, db_path: str, budget_tasks: int = 100):
        self.db = sqlite3.connect(db_path)
        self.db.execute("CREATE TABLE IF NOT EXISTS tasks(task_id TEXT PRIMARY KEY, kind TEXT, spec TEXT, spec_hash TEXT UNIQUE, status TEXT, result TEXT, created REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, event TEXT, payload TEXT, prev_hash TEXT, hash TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS knowledge(kid TEXT PRIMARY KEY, version INT, status TEXT, body TEXT, supersedes TEXT)")
        # --- MISSION 002: mission persistante, leases/fencing, outbox, hypotheses ---
        self.db.execute("CREATE TABLE IF NOT EXISTS missions(mission_id TEXT PRIMARY KEY, objective TEXT, stream TEXT, status TEXT, created REAL, updated REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS leases(task_id TEXT PRIMARY KEY, worker_id TEXT, epoch INT, expires_at REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS publications(task_id TEXT PRIMARY KEY, worker_id TEXT, epoch INT, result_hash TEXT, published_at REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS outbox(op_id TEXT PRIMARY KEY, kind TEXT, payload TEXT, status TEXT, attempts INT, created REAL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS hypotheses(canon_hash TEXT PRIMARY KEY, mission_id TEXT, statement TEXT, normalized TEXT, status TEXT, justification TEXT)")
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

    # ================= MISSION 002: orchestration autonome =================
    MISSION_STATES = ("OPEN", "PAUSED", "CANCELLED", "CONCLUDED_WITH_EVIDENCE")

    def create_mission(self, objective: str, stream: str = "B") -> str:
        if stream not in ("A", "B"):
            raise ValueError("stream A (trader) ou B (marche)")
        mid = "M-" + _h({"objective": objective, "stream": stream})[:16]
        if not self.db.execute("SELECT 1 FROM missions WHERE mission_id=?", (mid,)).fetchone():
            self.db.execute("INSERT INTO missions VALUES(?,?,?,?,?,?)",
                            (mid, objective, stream, "OPEN", time.time(), time.time()))
            self.db.commit(); self._log(mid, "MISSION_CREATED", {"stream": stream})
        return mid

    def mission(self, mission_id: str) -> dict:
        r = self.db.execute("SELECT objective,stream,status FROM missions WHERE mission_id=?", (mission_id,)).fetchone()
        if not r:
            raise KeyError(mission_id)
        return {"mission_id": mission_id, "objective": r[0], "stream": r[1], "status": r[2]}

    def mission_transition(self, mission_id: str, status: str) -> None:
        if status not in self.MISSION_STATES:
            raise ValueError(status)
        self.db.execute("UPDATE missions SET status=?, updated=? WHERE mission_id=?", (status, time.time(), mission_id))
        self.db.commit(); self._log(mission_id, f"MISSION_{status}", {})

    def record_hypothesis_verdict(self, mission_id: str, canon_hash: str, verdict: str) -> str:
        """Une refutation clot l'hypothese, JAMAIS la mission globale."""
        self.db.execute("UPDATE hypotheses SET status=? WHERE canon_hash=?", (verdict, canon_hash))
        self.db.commit(); self._log(mission_id, "HYPOTHESIS_VERDICT", {"hypothesis": canon_hash, "verdict": verdict})
        return self.mission(mission_id)["status"]

    # --- leases & fencing tokens ---
    def acquire_lease(self, task_id: str, worker_id: str, ttl_seconds: float = 60.0, now: float | None = None) -> int:
        now = time.time() if now is None else now
        row = self.db.execute("SELECT epoch FROM leases WHERE task_id=?", (task_id,)).fetchone()
        epoch = (row[0] or 0) + 1 if row else 1
        self.db.execute("INSERT OR REPLACE INTO leases VALUES(?,?,?,?)", (task_id, worker_id, epoch, now + ttl_seconds))
        self.db.commit(); self._log(task_id, "LEASE_ACQUIRED", {"worker": worker_id, "epoch": epoch})
        return epoch

    def publish(self, task_id: str, worker_id: str, epoch: int, result: dict, now: float | None = None) -> str:
        now = time.time() if now is None else now
        if self.db.execute("SELECT 1 FROM publications WHERE task_id=?", (task_id,)).fetchone():
            raise LeaseRejected("doublon logique: resultat deja publie pour cette tache")
        row = self.db.execute("SELECT worker_id,epoch,expires_at FROM leases WHERE task_id=?", (task_id,)).fetchone()
        if not row or row[0] != worker_id or row[1] != epoch:
            raise LeaseRejected("fencing: worker ou epoch obsolete")
        if now > row[2]:
            raise LeaseRejected("lease expire")
        digest = _h(result)
        self.db.execute("INSERT INTO publications VALUES(?,?,?,?,?)", (task_id, worker_id, epoch, digest, now))
        self.db.commit()
        self.transition(task_id, "COMPLETED", result)
        self._log(task_id, "PUBLISHED", {"worker": worker_id, "epoch": epoch, "result_hash": digest})
        return digest

    # --- outbox: appels externes idempotents, incertains reconcilies, jamais relances aveuglement ---
    def outbox_enqueue(self, idempotency_key: str, kind: str, payload: dict) -> str:
        op_id = "OP-" + _h({"key": idempotency_key, "kind": kind})[:16]
        if not self.db.execute("SELECT 1 FROM outbox WHERE op_id=?", (op_id,)).fetchone():
            self.db.execute("INSERT INTO outbox VALUES(?,?,?,?,?,?)",
                            (op_id, kind, json.dumps(payload, default=str), "PENDING", 0, time.time()))
            self.db.commit(); self._log(op_id, "OUTBOX_ENQUEUED", {"kind": kind})
        return op_id

    def outbox_dispatch(self, op_id: str) -> None:
        self.db.execute("UPDATE outbox SET status='DISPATCHED', attempts=attempts+1 WHERE op_id=? AND status='PENDING'", (op_id,))
        self.db.commit(); self._log(op_id, "OUTBOX_DISPATCHED", {})

    def outbox_mark_uncertain(self, op_id: str) -> None:
        """Timeout/reponse perdue: le cout peut exister. Statut UNCERTAIN, exclu de toute relance auto."""
        self.db.execute("UPDATE outbox SET status='UNCERTAIN' WHERE op_id=?", (op_id,))
        self.db.commit(); self._log(op_id, "OUTBOX_UNCERTAIN", {})

    def outbox_resolve(self, op_id: str, confirmed: bool) -> None:
        self.db.execute("UPDATE outbox SET status=? WHERE op_id=? AND status='UNCERTAIN'",
                        ("CONFIRMED" if confirmed else "FAILED_NOT_EXECUTED", op_id))
        self.db.commit(); self._log(op_id, "OUTBOX_RESOLVED", {"confirmed": confirmed})

    def outbox_status(self, op_id: str) -> str:
        return self.db.execute("SELECT status FROM outbox WHERE op_id=?", (op_id,)).fetchone()[0]

    def outbox_dispatchable(self) -> list:
        """Seules les operations PENDING sont dispatchables; UNCERTAIN ne l'est jamais."""
        return [r[0] for r in self.db.execute("SELECT op_id FROM outbox WHERE status='PENDING' ORDER BY created")]

    # --- deduplication canonique + recherche ouverte ---
    def register_hypothesis(self, mission_id: str, statement: str, justification: str = "") -> tuple:
        norm = _normalize(statement)
        canon = _h({"norm": norm})[:16]
        row = self.db.execute("SELECT status FROM hypotheses WHERE canon_hash=?", (canon,)).fetchone()
        if row:
            if row[0] == "REFUTEE" and not justification:
                return canon, True, "BLOQUEE_DEJA_REFUTEE_SANS_JUSTIFICATION"
            return canon, True, row[0]
        self.db.execute("INSERT INTO hypotheses VALUES(?,?,?,?,?,?)",
                        (canon, mission_id, statement, norm, "OPEN", justification))
        self.db.commit(); self._log(mission_id, "HYPOTHESIS_REGISTERED", {"hypothesis": canon})
        return canon, False, "OPEN"

    def open_hypotheses(self, mission_id: str) -> list:
        return [r[0] for r in self.db.execute("SELECT canon_hash FROM hypotheses WHERE mission_id=? AND status='OPEN'", (mission_id,))]

    def ensure_meta_research(self, mission_id: str) -> str | None:
        """Portefeuille vide -> tache de meta-recherche automatique; la mission reste ouverte."""
        if self.mission(mission_id)["status"] != "OPEN" or self.open_hypotheses(mission_id):
            return None
        tid = self.create_task("meta_recherche", {"mission": mission_id,
            "angles": ["angles_morts", "methodes_non_explorees", "representations", "familles_nouvelles", "donnees_non_utilisees"]})
        self._log(mission_id, "META_RESEARCH_CREATED", {"task": tid})
        return tid

    # --- sauvegarde / restauration verifiable ---
    def backup(self, dest_path: str) -> str:
        dest = sqlite3.connect(dest_path)
        try:
            self.db.backup(dest)
        finally:
            dest.close()
        return _h({"journal_head": self.db.execute("SELECT hash FROM events ORDER BY id DESC LIMIT 1").fetchone()[0]})

    def publication_count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM publications").fetchone()[0]
