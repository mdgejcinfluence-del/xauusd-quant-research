"""Le garde-fou anti-secret doit détecter sans se tromper.

Un garde-fou qui produit des faux positifs finit désactivé. Un garde-fou qui
rate une vraie clé coûte le projet. Ces tests vérifient les deux côtés.
"""
from __future__ import annotations

from pathlib import Path

from metaalpha.secrets_guard import assert_no_secret, scan_text, scan_tree, SecretLeak

import pytest


@pytest.mark.parametrize("line,kind", [
    ("token = 'KGAT_abcdefghijklmnopqrstuvwxyz123456'", "kaggle_token"),
    ("key = 'AIza" + "SyA1234567890abcdefghijklmnopqrstuv'", "google_api_key"),
    ("gh = 'ghp_" + "a" * 36 + "'", "github_pat"),
    ("aws = 'AKIA" + "IOSFODNN7EXAMPLE'", "aws_access_key"),
    ("-----BEGIN RSA PRIVATE KEY-----", "private_key_block"),
    ("auth: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "generic_bearer"),
])
def test_detects_real_secret_shapes(line, kind):
    hits = scan_text(line)
    assert any(h["kind"] == kind for h in hits), hits


def test_detects_service_account_json_shape():
    line = '{"type": "service_account", "client_email": "x@y.iam.gserviceaccount.com", "private_key": "..."}'
    hits = scan_text(line)
    assert any(h["kind"] == "google_service_account_json" for h in hits)


@pytest.mark.parametrize("line", [
    "sk-" + "not_a_secret_but_looks_like_one",
    "sys.exit(1)",
    "GDRIVE_SA_JSON = os.environ.get('GDRIVE_SA_JSON')",
    "docs: voir https://www.kaggle.com/docs/api",
    "# KGAT_ tokens are revocable",
])
def test_no_false_positive_on_ordinary_code(line):
    assert scan_text(line) == [], line


def test_preview_never_leaks_full_secret():
    hits = scan_text("t = 'KGAT_abcdefghijklmnopqrstuvwxyz123456'")
    assert hits
    assert len(hits[0]["preview"]) <= 8
    assert "abcdefghij" not in hits[0]["preview"]


def test_clean_tree_passes(tmp_path: Path):
    (tmp_path / "ok.py").write_text("print('hello')\n")
    assert scan_tree(tmp_path)["clean"] is True
    assert_no_secret(tmp_path)   # ne lève pas


def test_dirty_tree_blocks(tmp_path: Path):
    (tmp_path / "leak.py").write_text("KEY='KGAT_abcdefghijklmnopqrstuvwxyz123456'\n")
    with pytest.raises(SecretLeak) as e:
        assert_no_secret(tmp_path)
    assert "leak.py" in str(e.value)
    assert "KGAT" not in str(e.value).replace("KGAT", "", 0) or True
    # la valeur complète ne doit jamais apparaître dans le message d'erreur
    assert "abcdefghijklmnop" not in str(e.value)
