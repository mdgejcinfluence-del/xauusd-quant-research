import sys, pathlib, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from ere.kernel import Kernel, LeaseRejected

def K(td): return Kernel(f"{td}/k.db")

def test_mission_survives_all_refutations():
    with tempfile.TemporaryDirectory() as td:
        k = K(td); m = k.create_mission("identifier un mecanisme XAUUSD reproductible", "B")
        for i in range(3):
            c, dup, st = k.register_hypothesis(m, f"hypothese numero {i} totalement differente {i}")
            assert not dup
            assert k.record_hypothesis_verdict(m, c, "REFUTEE") == "OPEN"
        assert k.mission(m)["status"] == "OPEN"

def test_meta_research_created_when_portfolio_empty():
    with tempfile.TemporaryDirectory() as td:
        k = K(td); m = k.create_mission("mission ouverte", "B")
        assert k.ensure_meta_research(m) is not None
        c, _, _ = k.register_hypothesis(m, "la volatilite persiste apres un choc de prix")
        assert k.ensure_meta_research(m) is None  # portefeuille non vide
        k.record_hypothesis_verdict(m, c, "REFUTEE")
        assert k.ensure_meta_research(m) is not None  # re-ouverture auto

def test_fencing_expired_and_stale_workers_rejected_100pct():
    with tempfile.TemporaryDirectory() as td:
        k = K(td); t = k.create_task("x", {"a": 9})
        ep = k.acquire_lease(t, "w1", ttl_seconds=10, now=1000.0)
        rejected = 0
        for now in (1010.1, 2000.0, 1e9):  # expire
            try: k.publish(t, "w1", ep, {"r": 1}, now=now)
            except LeaseRejected: rejected += 1
        ep2 = k.acquire_lease(t, "w2", ttl_seconds=100, now=2000.0)  # nouveau worker, epoch++
        for w, e in (("w1", ep), ("w2", ep), ("w1", ep2)):  # fencing obsoletes
            try: k.publish(t, w, e, {"r": 1}, now=2001.0)
            except LeaseRejected: rejected += 1
        assert rejected == 6  # 100 % des tentatives invalides rejetees
        assert k.publish(t, "w2", ep2, {"r": 1}, now=2001.0)
        with pytest.raises(LeaseRejected):  # aucun doublon logique apres publication
            k.publish(t, "w2", ep2, {"r": 2}, now=2002.0)
        assert k.publication_count() == 1

def test_outbox_uncertain_never_blindly_redispatched():
    with tempfile.TemporaryDirectory() as td:
        k = K(td)
        op = k.outbox_enqueue("cle-1", "appel_externe", {"x": 1})
        assert k.outbox_enqueue("cle-1", "appel_externe", {"x": 1}) == op  # idempotent
        k.outbox_dispatch(op); k.outbox_mark_uncertain(op)
        assert k.outbox_dispatchable() == []  # jamais relance aveuglement
        k.outbox_resolve(op, confirmed=True); assert k.outbox_status(op) == "CONFIRMED"

def test_canonical_dedup_and_refuted_needs_justification():
    with tempfile.TemporaryDirectory() as td:
        k = K(td); m = k.create_mission("m", "A")
        c1, d1, _ = k.register_hypothesis(m, "La volatilite persiste apres un choc!")
        c2, d2, _ = k.register_hypothesis(m, "choc apres persiste volatilite la un")
        assert c1 == c2 and d2  # doublon canonique (ordre/punct. normalises)
        k.record_hypothesis_verdict(m, c1, "REFUTEE")
        _, _, st = k.register_hypothesis(m, "la volatilite persiste apres un choc")
        assert st == "BLOQUEE_DEJA_REFUTEE_SANS_JUSTIFICATION"
        _, _, st2 = k.register_hypothesis(m, "la volatilite persiste apres un choc", justification="nouvelle representation tick")
        assert st2 == "REFUTEE"  # rouvrable uniquement avec justification explicite

def test_backup_restore_fresh_environment_no_loss_no_duplicate():
    with tempfile.TemporaryDirectory() as td:
        k = K(td); m = k.create_mission("m", "B"); t = k.create_task("x", {"a": 1})
        ep = k.acquire_lease(t, "w", ttl_seconds=3600)
        k.publish(t, "w", ep, {"ok": True})
        k.backup(f"{td}/backup.db")
        k2 = Kernel(f"{td}/backup.db")  # environnement vierge = nouvelle connexion sur la sauvegarde
        assert k2.verify_journal() and k2.mission(m)["status"] == "OPEN"
        assert k2.publication_count() == 1 and k2.get(t)["status"] == "COMPLETED"
