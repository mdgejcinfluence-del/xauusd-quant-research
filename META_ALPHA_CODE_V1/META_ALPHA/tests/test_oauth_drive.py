"""Le bouton de connexion — testé sans jamais toucher à un vrai compte.

On ne peut pas simuler Google dans un test, mais on peut vérifier :
  - que la page rend les trois états (non configuré / bouton / connecté)
  - que l'URL de consentement contient bien le sélecteur de compte
  - que le scope est LECTURE SEULE et rien d'autre
  - que les jetons ne sont jamais écrits sur disque
  - que find_corpus se comporte correctement sur un service factice
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from metaalpha.connect_app import _page, find_corpus
from metaalpha.oauth_drive import SCOPES, GoogleConsent, OAuthNotConfigured

FAKE_CLIENT = {
    "web": {
        "client_id": "1234567890-abcdef.apps.googleusercontent.com",
        "client_secret": "GOCSPX-fakefakefakefakefakefake",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}


# ---------------------------------------------------------------------------
# Scope : lecture seule, strictement
# ---------------------------------------------------------------------------
def test_scope_is_readonly_only():
    assert SCOPES == ["https://www.googleapis.com/auth/drive.readonly"]
    assert not any("drive.file" in s or s.endswith("/drive") for s in SCOPES)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
def test_not_configured_detected_cleanly():
    c = GoogleConsent(None)
    assert c.configured() is False
    with pytest.raises(OAuthNotConfigured):
        c.start("state1", "https://example.com/cb")


def test_from_env_reads_client_json(monkeypatch):
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_JSON", json.dumps(FAKE_CLIENT))
    c = GoogleConsent.from_env()
    assert c.configured() is True


def test_from_env_survives_invalid_json(monkeypatch):
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_JSON", "{ pas du json")
    assert GoogleConsent.from_env().configured() is False


# ---------------------------------------------------------------------------
# URL de consentement
# ---------------------------------------------------------------------------
def test_consent_url_selects_account_and_requests_offline():
    c = GoogleConsent(FAKE_CLIENT)
    url = c.start("st-42", "https://host.example/oauth/callback")
    assert url.startswith("https://accounts.google.com/o/oauth2/")
    assert "select_account" in url          # le sélecteur de compte
    assert "access_type=offline" in url     # pour un jeton durable
    assert "drive.readonly" in url.replace("%2F", "/").replace("%3A", ":")
    assert "st-42" in url


# ---------------------------------------------------------------------------
# Rendu de la page : trois états distincts
# ---------------------------------------------------------------------------
def test_page_renders_setup_form_without_client():
    """Sans client OAuth, la page ne montre pas le bouton mais le formulaire
    qui permet de l'activer — sans passer par un terminal."""
    html = _page("st", redirect_uri="https://h.example/oauth/callback")
    assert "Une seule chose manque" in html
    assert 'action="/configure"' in html
    assert "https://h.example/oauth/callback" in html   # l'URI exacte à copier
    assert "class=\"btn\" href=\"/start" not in html  # pas encore de bouton Google


def test_page_renders_button_when_configured(monkeypatch):
    import metaalpha.connect_app as app
    monkeypatch.setattr(app, "CONSENT", GoogleConsent(FAKE_CLIENT))
    html = app._page("st-abc", redirect_uri="https://h/cb")
    assert "Se connecter à Drive" in html
    assert "/start?state=st-abc" in html
    assert "lecture" in html.lower()


def test_page_renders_connected_state(monkeypatch):
    import metaalpha.connect_app as app
    c = GoogleConsent(FAKE_CLIENT)
    monkeypatch.setattr(app, "CONSENT", c)
    c.start("st-xyz", "https://h/cb")
    sess = c.sessions["st-xyz"]
    sess.tokens = {"access_token": "fake"}
    sess.account = {"user": {"emailAddress": "owner@example.com"}}
    html = app._page("st-xyz", redirect_uri="https://h/cb")
    assert "owner@example.com" in html
    assert "Changer de compte" in html


# ---------------------------------------------------------------------------
# Aucun jeton sur disque
# ---------------------------------------------------------------------------
def test_no_token_written_to_disk(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    c = GoogleConsent(FAKE_CLIENT)
    c.start("st", "https://h/cb")
    sess = c.sessions["st"]
    sess.tokens = {"access_token": "SECRET_TOKEN_MARKER", "refresh_token": "SECRET_REFRESH"}
    sess.account = {"user": {"emailAddress": "x@y.z"}}
    # le module n'écrit rien : aucun fichier ne doit apparaître
    assert list(tmp_path.iterdir()) == []
    # et le statut public ne contient aucun jeton
    st = c.status("st")
    assert "SECRET_TOKEN_MARKER" not in json.dumps(st)
    assert "SECRET_REFRESH" not in json.dumps(st)


def test_status_unknown_state():
    assert GoogleConsent(FAKE_CLIENT).status("nope") == {"state": "UNKNOWN"}


# ---------------------------------------------------------------------------
# find_corpus sur un service factice
# ---------------------------------------------------------------------------
class _FakeFiles:
    def __init__(self, mapping):
        self.mapping = mapping
        self.calls = []

    def list(self, **kw):
        self.calls.append(kw)
        return self

    def execute(self):
        return {"files": self.mapping}


class _FakeService:
    def __init__(self, mapping):
        self._files = _FakeFiles(mapping)

    def files(self):
        return self._files


def test_find_corpus_detects_certificate_and_partition():
    svc = _FakeService([
        {"id": "1", "name": "PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json",
         "mimeType": "application/json", "size": "100", "parents": [], "modifiedTime": "x"},
        {"id": "2", "name": "part_000001.parquet",
         "mimeType": "application/octet-stream", "size": "100", "parents": [], "modifiedTime": "x"},
    ])
    rep = find_corpus(svc)
    assert rep["summary"]["looks_like_corpus"] is True
    assert rep["certificates"] and rep["partitions"]


def test_find_corpus_empty_drive_is_honest():
    rep = find_corpus(_FakeService([]))
    assert rep["summary"]["looks_like_corpus"] is False
    assert rep["summary"]["partitions_visible"] == 0


def test_find_corpus_survives_api_error():
    class Boom:
        def files(self):
            raise RuntimeError("quota")

    rep = find_corpus(Boom())
    # une erreur d'API ne doit pas renverser le serveur
    assert rep["summary"]["looks_like_corpus"] is False
