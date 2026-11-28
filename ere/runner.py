"""Infrastructure d'exécution ERE (Phase 3).

Exécution déterministe, manifeste SHA-256, checkpoints durables par
shard, reprise après interruption, idempotence par hash de tâche.
Un checkpoint n'est durable que lorsqu'il est écrit sur le disque de
résultats et relu/vérifié (équivalent local de la publication externe).
"""
from __future__ import annotations

import hashlib
import json
import pathlib


def task_hash(spec: dict) -> str:
    return hashlib.sha256(json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()


class TaskRunner:
    def __init__(self, workdir: str, spec: dict):
        self.spec = spec
        self.tid = task_hash(spec)
        self.dir = pathlib.Path(workdir) / self.tid
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "checkpoint.json"
        self.state = self._load()

    def _load(self) -> dict:
        if self.state_path.exists():
            s = json.loads(self.state_path.read_text())
            if s.get("task_hash") != self.tid:
                raise ValueError("Checkpoint incompatible avec la tâche (hash différent)")
            return s
        return {"task_hash": self.tid, "spec": self.spec, "completed_shards": [], "attempts": 0, "status": "CREATED"}

    def _save(self) -> None:
        # Écriture atomique: .tmp puis rename, puis relecture de vérification.
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1, sort_keys=True))
        tmp.replace(self.state_path)
        json.loads(self.state_path.read_text())

    def run_shards(self, shard_ids: list, fn) -> dict:
        """Exécute fn(shard_id) pour les shards non terminés. Idempotent."""
        self.state["attempts"] += 1
        self.state["status"] = "RUNNING"
        self._save()
        results = {}
        for sid in shard_ids:
            if sid in self.state["completed_shards"]:
                results[sid] = "ALREADY_DONE"
                continue
            results[sid] = fn(sid)
            self.state["completed_shards"].append(sid)
            self._save()  # checkpoint durable après chaque shard
        self.state["status"] = "COMPLETED"
        self._save()
        manifest = {
            "task_hash": self.tid,
            "spec": self.spec,
            "completed_shards": sorted(self.state["completed_shards"]),
            "attempts": self.state["attempts"],
            "checkpoint_sha256": hashlib.sha256(self.state_path.read_bytes()).hexdigest(),
        }
        (self.dir / "run_manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True))
        return manifest
