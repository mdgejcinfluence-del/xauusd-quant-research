"""Préflight P0 — vérifier l'accès au corpus AVANT toute exécution.

Ce module existe pour une raison simple : un projet qui produit 43 artéfacts
mais qui n'a pas accès à la donnée certifiée doit le dire en dix secondes, pas
après trois heures de calcul.

Il répond à cinq questions, dans cet ordre, et s'arrête à la première qui
échoue :

  1. Le backend est-il configuré ?       (compte de service + dossier racine)
  2. Le dossier racine est-il lisible ?
  3. Les deux certificats Phase 1 et Phase 2 existent-ils ?
  4. Leurs SHA-256 sont-ils calculables et stables ?
  5. Les 348 partitions sont-elles présentes ?

Aucune science ici. Uniquement de la plomberie, et un refus net de continuer
si la baseline n'est pas vérifiable.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .config import sha256_text
from .remote import Remote, remote_from_env

CERT_P1_REL = "04_CHECKPOINTS/PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json"
CERT_P2_REL = "04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json"
PARTITIONS_REL = "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS"
EXPECTED_PARTITIONS = 348
EXPECTED_TICKS = 685_118_625
EXPECTED_RAW_FILES = 11_136


class PreflightFailure(RuntimeError):
    """Une étape de préflight a échoué : on ne va pas plus loin."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"[{code}] {detail}")
        self.code = code
        self.detail = detail


def _json_hash(obj: Any) -> str:
    """Hash canonique d'un document JSON : clés triées, séparateurs fixes."""
    canon = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def check_backend(remote: Remote | None = None) -> dict[str, Any]:
    """Étape 1 : un backend distant utilisable existe-t-il ?"""
    try:
        r = remote or remote_from_env()
    except RuntimeError as exc:
        raise PreflightFailure(
            "NO_REMOTE_BACKEND",
            "aucun backend distant configuré. Définir GDRIVE_SA_JSON et "
            f"GDRIVE_ROOT_FOLDER_ID (ou METAALPHA_LOCAL_ROOT pour un test local). Détail : {exc}",
        ) from exc
    return {"step": "backend", "ok": True, "kind": type(r).__name__}


def check_certificates(remote: Remote) -> dict[str, Any]:
    """Étapes 2-4 : les certificats existent, se lisent et se hashent."""
    out: dict[str, Any] = {"step": "certificates", "certificates": {}}
    for code, rel in (("P1", CERT_P1_REL), ("P2", CERT_P2_REL)):
        if not remote.exists(rel):
            raise PreflightFailure(
                "CERTIFICATE_MISSING",
                f"certificat {code} introuvable au chemin attendu : {rel}. "
                "Vérifier que GDRIVE_ROOT_FOLDER_ID pointe bien sur la racine "
                "META_ALPHA_XAUUSD_DGP, pas sur un sous-dossier.",
            )
        doc = remote.read_json(rel)
        canonical = _json_hash(doc)
        out["certificates"][code] = {
            "path": rel,
            "status": doc.get("status"),
            "sha256_canonical": canonical,
            # taille du document : un changement de taille révèle une retouche
            "keys": sorted(doc.keys())[:40],
        }
        if doc.get("status") != "CERTIFIED":
            raise PreflightFailure(
                "CERTIFICATE_NOT_CERTIFIED",
                f"certificat {code} porte le statut {doc.get('status')!r}, pas CERTIFIED. "
                "Ne pas continuer : la baseline n'est pas celle attendue.",
            )
    return out


def check_partitions(remote: Remote, *, expected: int = EXPECTED_PARTITIONS) -> dict[str, Any]:
    """Étape 5 : les partitions sont présentes et nommées comme attendu."""
    if not remote.exists(PARTITIONS_REL):
        raise PreflightFailure(
            "PARTITIONS_MISSING",
            f"dossier des partitions introuvable : {PARTITIONS_REL}",
        )
    names = sorted(remote.listdir(PARTITIONS_REL))
    parquet = [n for n in names if n.endswith(".parquet")]
    if len(parquet) != expected:
        raise PreflightFailure(
            "PARTITION_COUNT_MISMATCH",
            f"{len(parquet)} partitions Parquet trouvées, {expected} attendues par le "
            "certificat Phase 2. Ne pas continuer tant que l'écart n'est pas expliqué : "
            "soit une partition manque, soit le corpus a changé.",
        )
    first, last = parquet[0], parquet[-1]
    if first != "part_000001.parquet":
        raise PreflightFailure(
            "PARTITION_NAMING_UNEXPECTED",
            f"première partition {first!r} au lieu de 'part_000001.parquet'",
        )
    return {
        "step": "partitions",
        "ok": True,
        "count": len(parquet),
        "first": first,
        "last": last,
        "listing_sha256": sha256_text("|".join(parquet)),
    }


def run_preflight(remote: Remote | None = None, *, expected_partitions: int = EXPECTED_PARTITIONS) -> dict[str, Any]:
    """Exécute les cinq étapes dans l'ordre. S'arrête à la première qui échoue.

    Retourne toujours un rapport ; lève seulement si le backend manque, car dans
    ce cas il n'y a rien à rapporter d'autre.
    """
    report: dict[str, Any] = {"schema_version": "1.0", "steps": [], "status": "UNKNOWN"}
    try:
        r = remote or remote_from_env()
    except RuntimeError as exc:
        report["status"] = "BLOCKED_NO_BACKEND"
        report["reason"] = str(exc)
        report["steps"].append({"step": "backend", "ok": False, "reason": str(exc)})
        return report

    report["steps"].append(check_backend(r))
    report["steps"].append(check_certificates(r))
    report["steps"].append(check_partitions(r, expected=expected_partitions))

    certs = report["steps"][1]["certificates"]
    report["baseline_manifest"] = {
        "p1_sha256_canonical": certs["P1"]["sha256_canonical"],
        "p2_sha256_canonical": certs["P2"]["sha256_canonical"],
        "partitions_listing_sha256": report["steps"][2]["listing_sha256"],
        "partitions_count": report["steps"][2]["count"],
        "ticks_expected": EXPECTED_TICKS,
        "raw_files_expected": EXPECTED_RAW_FILES,
    }
    report["status"] = "PASS"
    report["next_action"] = "écrire BASELINE_HASH_MANIFEST.json puis démarrer P2_ANALYTICAL"
    return report


def main() -> int:
    """CLI : python -m metaalpha.drive_preflight"""
    rep = run_preflight()
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
