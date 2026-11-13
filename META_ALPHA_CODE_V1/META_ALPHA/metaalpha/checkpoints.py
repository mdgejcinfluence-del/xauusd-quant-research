"""Checkpoints liés au triplet (input_hash, code_hash, config_hash).

Règle du kit (§15.3) : « reprise uniquement de l'unité incomplète ».
Un checkpoint n'est valide que si les trois hashes correspondent ; sinon
il est INVALIDÉ (écrit comme tel, jamais supprimé) et l'unité est rejouée.
"""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from typing import Any

from .fs import Storage

CKPT_REL = "00_GOVERNANCE/checkpoints"


@dataclass(frozen=True)
class UnitKey:
    phase: str
    unit_id: str
    input_hash: str
    code_hash: str
    config_hash: str

    @property
    def value(self) -> str:
        import hashlib

        raw = "|".join(
            [self.phase, self.unit_id, self.input_hash, self.code_hash, self.config_hash]
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:24]

    @property
    def rel(self) -> str:
        return f"{CKPT_REL}/{self.phase}/{self.unit_id}.json"


def load(storage: Storage, key: UnitKey) -> dict | None:
    p = storage._resolve_read(key.rel)
    if not p.exists():
        return None
    try:
        return storage.read_json(key.rel)
    except json.JSONDecodeError:
        return None


def is_valid(storage: Storage, key: UnitKey) -> bool:
    ck = load(storage, key)
    if not ck:
        return False
    if ck.get("status") != "VALID" or ck.get("key") != key.value:
        return False
    # la sortie doit toujours être présente : un checkpoint orphelin est rejoué
    return storage.exists(ck.get("output_rel", ""))


def invalidate(storage: Storage, key: UnitKey, reason: str) -> None:
    ck = load(storage, key) or {}
    ck.update(
        {
            "phase": key.phase,
            "unit_id": key.unit_id,
            "status": "INVALIDATED",
            "invalid_reason": reason,
            "invalidated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
    )
    storage.write_atomic_json(key.rel, ck)


def write(
    storage: Storage,
    key: UnitKey,
    *,
    output_rel: str,
    output_sha: str,
    rows: int,
    elapsed_s: float,
    runtime: str,
    attempts: int,
    extra: dict[str, Any] | None = None,
) -> None:
    payload = {
        "phase": key.phase,
        "unit_id": key.unit_id,
        "key": key.value,
        "input_hash": key.input_hash,
        "code_hash": key.code_hash,
        "config_hash": key.config_hash,
        "output_rel": output_rel,
        "output_sha": output_sha,
        "output_exists": storage.exists(output_rel),
        "rows": rows,
        "elapsed_s": round(elapsed_s, 3),
        "runtime_id": runtime,
        "attempts": attempts,
        "status": "VALID",
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    if extra:
        payload.update(extra)
    storage.write_atomic_json(key.rel, payload)
