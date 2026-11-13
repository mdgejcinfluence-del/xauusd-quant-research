"""Verrou par bail (lease) : empêche deux exécutions concurrentes.

Google Drive n'offre pas de verrou transactionnel distribué. Le protocole
retenu est donc « create-if-absent + bail + heartbeat » :

  acquire()  -> création exclusive du fichier de bail
             -> si présent mais expiré, on peut le reprendre
             -> sinon LeaseHeld
  heartbeat() -> repousse la date d'expiration
  release()  -> supprime le bail si on en est propriétaire

Un worker mort perd son bail au plus tard après `ttl`. Le bail est donc
auto-réparateur : aucun déblocage manuel n'est requis.
"""
from __future__ import annotations

import os
import socket
import time
import uuid
from dataclasses import dataclass
from typing import Any

from .fs import Storage

LEASES_REL = "00_GOVERNANCE/leases"


class LeaseHeld(RuntimeError):
    def __init__(self, owner: str, expires_utc: str) -> None:
        super().__init__(f"bail détenu par {owner} jusqu'à {expires_utc}")
        self.owner = owner
        self.expires_utc = expires_utc


def runtime_id() -> str:
    return f"{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:6]}"


@dataclass
class Lease:
    storage: Storage
    rel: str
    owner: str
    ttl: int

    def heartbeat(self) -> None:
        self.storage.write_atomic_json(
            self.rel,
            {"owner": self.owner, "expires": time.time() + self.ttl, "pid": os.getpid()},
        )

    def release(self) -> None:
        p = self.storage._resolve_read(self.rel)
        try:
            cur = self.storage.read_json(self.rel)
        except FileNotFoundError:
            return
        if cur.get("owner") == self.owner:
            p.unlink(missing_ok=True)

    def __enter__(self) -> "Lease":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.release()


def acquire(storage: Storage, name: str, ttl: int = 1800, owner: str | None = None) -> Lease:
    owner = owner or runtime_id()
    rel = f"{LEASES_REL}/{name}.lease"
    payload = {"owner": owner, "expires": time.time() + ttl, "pid": os.getpid()}

    if storage.try_create_exclusive(rel, payload):
        return Lease(storage, rel, owner, ttl)

    cur = storage.read_json(rel)
    if float(cur.get("expires", 0)) < time.time():
        # bail expiré : reprise autorisée
        storage.write_atomic_json(rel, payload)
        return Lease(storage, rel, owner, ttl)

    import datetime as _dt

    exp = _dt.datetime.fromtimestamp(float(cur.get("expires", 0)), _dt.timezone.utc).isoformat()
    raise LeaseHeld(str(cur.get("owner")), exp)
