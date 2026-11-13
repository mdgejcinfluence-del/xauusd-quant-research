"""Orchestrateur : DAG déclaratif, leases, checkpoints, retries, statuts terminaux.

Ce module ne fait AUCUNE science. Il exécute des unités de travail :

    unit = 1 partition Parquet  (ou 1 sous-bloc de partition)

et garantit :

- qu'une unité déjà validée n'est pas rejouée (sauf hash modifié) ;
- qu'une unité n'est exécutée que par un seul runtime à la fois ;
- que le statut terminal est toujours l'un des cinq autorisés ;
- qu'un échec donne un RESUME_FROM précis.
"""
from __future__ import annotations

import datetime as dt
import time
import traceback
from dataclasses import dataclass, field
from typing import Callable, Iterable

from . import checkpoints, leases
from .checkpoints import UnitKey
from .config import Config, code_hash
from .fs import Storage
from .governance import (
    KillSwitchActive,
    assert_not_killed,
    load_state,
    save_state,
)

TS_FMT = "%Y-%m-%dT%H:%M:%SZ"


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime(TS_FMT)


class TransientError(RuntimeError):
    """Erreur réputée transitoire (réseau, timeout, 429)."""


@dataclass
class UnitResult:
    unit_id: str
    status: str            # EXECUTED | SKIPPED_FROM_CHECKPOINT | FAILED | ABANDONED
    rows: int = 0
    elapsed_s: float = 0.0
    error: str | None = None


@dataclass
class PhaseOutcome:
    phase: str
    status: str
    units_total: int
    units_executed: int
    units_skipped: int
    units_failed: int
    resume_from: str | None
    elapsed_s: float
    errors: list[str] = field(default_factory=list)
    report_rel: str | None = None


UnitFn = Callable[[str, Storage], tuple[int, str, str]]
"""Signature : fn(unit_id, storage) -> (rows, output_rel, output_sha)

L'implémentation d'une phase fournit cette fonction. Elle ne connaît ni les
leases, ni les checkpoints, ni les retries : l'orchestrateur s'en charge.
"""


class Orchestrator:
    def __init__(
        self,
        storage: Storage,
        config: Config,
        *,
        phase: str,
        unit_fn: UnitFn,
        runtime: str | None = None,
        max_runtime_seconds: int | None = None,
    ) -> None:
        self.storage = storage
        self.config = config
        self.phase = phase
        self.unit_fn = unit_fn
        self.runtime = runtime or leases.runtime_id()
        self.max_runtime_seconds = (
            max_runtime_seconds
            or int(config.get("orchestrator", "max_runtime_seconds", default=3 * 3600))
        )
        self.retries = int(config.get("orchestrator", "retries", default=3))
        self.code_hash = code_hash()
        self.config_hash = config.sha

    # ------------------------------------------------------------------
    def run(self, unit_ids: Iterable[str], input_hash_for: Callable[[str], str]) -> PhaseOutcome:
        t0 = time.time()
        dead_line = t0 + self.max_runtime_seconds
        executed = skipped = failed = 0
        errors: list[str] = []
        resume_from: str | None = None
        results: list[UnitResult] = []
        ids = list(unit_ids)

        self.storage.cleanup_orphan_tmp()

        for uid in ids:
            # arrêt propre avant la limite du runtime hôte (Colab 12h, Actions 6h)
            if time.time() > dead_line:
                resume_from = uid
                errors.append(f"MAX_RUNTIME atteint avant {uid}")
                break
            try:
                assert_not_killed(self.storage)
            except KillSwitchActive as exc:
                resume_from = uid
                errors.append(str(exc))
                break

            key = UnitKey(
                phase=self.phase,
                unit_id=uid,
                input_hash=input_hash_for(uid),
                code_hash=self.code_hash,
                config_hash=self.config_hash,
            )

            if checkpoints.is_valid(self.storage, key):
                skipped += 1
                results.append(UnitResult(uid, "SKIPPED_FROM_CHECKPOINT"))
                continue

            res = self._run_one(key, uid)
            results.append(res)
            if res.status == "EXECUTED":
                executed += 1
            elif res.status == "FAILED":
                failed += 1
                resume_from = uid
                errors.append(f"{uid}: {res.error}")
                if res.error and "DETERMINISTIC" in res.error:
                    break
            elif res.status == "ABANDONED":
                failed += 1
                resume_from = uid
                errors.append(f"{uid}: lease détenu par un autre runtime")

        elapsed = time.time() - t0
        status = self._terminal_status(executed, skipped, failed, resume_from, ids)

        outcome = PhaseOutcome(
            phase=self.phase,
            status=status,
            units_total=len(ids),
            units_executed=executed,
            units_skipped=skipped,
            units_failed=failed,
            resume_from=resume_from,
            elapsed_s=round(elapsed, 3),
            errors=errors,
        )

        self._persist(outcome, results)
        return outcome

    # ------------------------------------------------------------------
    def _run_one(self, key: UnitKey, uid: str) -> UnitResult:
        name = f"{self.phase}__{uid}"
        t0 = time.time()
        attempt = 0
        while attempt < self.retries:
            attempt += 1
            try:
                lease = leases.acquire(self.storage, name, ttl=1800, owner=self.runtime)
            except leases.LeaseHeld as exc:
                return UnitResult(uid, "ABANDONED", error=f"lease: {exc}")

            try:
                rows, out_rel, out_sha = self.unit_fn(uid, self.storage)
                if not out_sha or not out_sha.startswith("sha256:"):
                    raise ValueError("DETERMINISTIC: sortie non hashée")
                checkpoints.write(
                    self.storage, key,
                    output_rel=out_rel, output_sha=out_sha, rows=rows,
                    elapsed_s=time.time() - t0, runtime=self.runtime, attempts=attempt,
                )
                return UnitResult(uid, "EXECUTED", rows, time.time() - t0)
            except TransientError as exc:
                if attempt >= self.retries:
                    return UnitResult(uid, "FAILED", error=f"TRANSIENT after {attempt}: {exc}")
                time.sleep(min(30, 2 ** attempt))
            except Exception as exc:  # déterministe
                return UnitResult(uid, "FAILED", error=f"DETERMINISTIC: {exc}\n{traceback.format_exc(limit=2)}")
            finally:
                lease.release()

        return UnitResult(uid, "FAILED", error="retries épuisés")

    # ------------------------------------------------------------------
    def _terminal_status(
        self, executed: int, skipped: int, failed: int, resume_from: str | None, ids: list[str]
    ) -> str:
        if failed == 0 and resume_from is None and (executed + skipped) == len(ids):
            return "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"
        if failed > 0:
            return "FAILED_TECHNICAL"
        return "BLOCKED_WITH_RESUME"

    # ------------------------------------------------------------------
    def _persist(self, outcome: PhaseOutcome, results: list[UnitResult]) -> None:
        st = load_state(self.storage)
        st["active_phase"] = self.phase
        st["phase_status"] = outcome.status
        st["last_unit_done"] = next(
            (r.unit_id for r in reversed(results) if r.status == "EXECUTED"), st.get("last_unit_done")
        )
        if outcome.status == "PHASE_COMPLETE_AWAITING_OWNER_REVIEW":
            if self.phase not in st["completed_phases"]:
                st["completed_phases"].append(self.phase)
            st["pending_units"] = []
        else:
            pending = [r.unit_id for r in results if r.status == "FAILED"]
            st["pending_units"] = pending
        save_state(self.storage, st)

        rel = f"40_REPORTS/{self.phase}/{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_run.json"
        payload = {
            "phase": outcome.phase,
            "status": outcome.status,
            "units_total": outcome.units_total,
            "units_executed": outcome.units_executed,
            "units_skipped_from_checkpoint": outcome.units_skipped,
            "units_failed": outcome.units_failed,
            "resume_from": outcome.resume_from,
            "elapsed_s": outcome.elapsed_s,
            "runtime_id": self.runtime,
            "code_hash": self.code_hash,
            "config_hash": self.config_hash,
            "errors": outcome.errors[:50],
            "heartbeat_utc": utcnow(),
            "units": [r.__dict__ for r in results],
        }
        outcome.report_rel = rel
        self.storage.write_atomic_json(rel, payload)
        self.write_heartbeat(last_unit=st.get("last_unit_done"))

    def write_heartbeat(self, last_unit: str | None = None) -> None:
        self.storage.write_atomic_json(
            "00_GOVERNANCE/heartbeat.json",
            {
                "runtime_id": self.runtime,
                "phase": self.phase,
                "last_unit": last_unit,
                "utc": utcnow(),
            },
        )
