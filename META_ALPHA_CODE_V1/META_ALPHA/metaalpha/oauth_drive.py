"""Connexion Google par OAuth — le bouton « Se connecter à Drive ».

Différence essentielle avec le compte de service :

  * Compte de service  : robot, 24/7, aucun mot de passe. C'est ce qu'il faut
    pour l'exploitation.
  * OAuth utilisateur  : c'est VOUS qui autorisez, dans votre navigateur, le
    compte Google que vous choisissez. C'est ce qu'il faut pour la mise en
    place : choisir le Drive, trouver le corpus, lire les certificats, créer
    les dossiers de recherche.

Ce module ne demande jamais de mot de passe. Il ne voit jamais vos
identifiants : Google affiche sa propre page, le mot de passe reste chez Google.
Le serveur ne reçoit qu'un code à usage unique, puis un jeton révocable.

Le jeton reste EN MÉMOIRE du processus. Il n'est jamais écrit sur disque, jamais
versionné, jamais transmis ailleurs qu'à Google.
"""
from __future__ import annotations

import json
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from typing import Any

# Google limite la durée de vie de cette page : le serveur garde le jeton en
# mémoire, et l'iframe ne sert qu'à afficher le bouton et le statut.
CONSENT_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# Lecture du Drive suffit pour tout ce que fait ce projet. On ne demande PAS
# l'écriture globale : le corpus certifié est en lecture seule par conception.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


class OAuthNotConfigured(RuntimeError):
    """Aucun client OAuth n'est disponible côté serveur."""


class ConsentSession:
    """Une tentative de connexion : état + jeton, en mémoire uniquement."""

    def __init__(self, flow, created_at: float):
        self.flow = flow
        self.created_at = created_at
        self.tokens: dict[str, Any] | None = None
        self.account: dict[str, Any] | None = None
        self.error: str | None = None

    @property
    def expired(self) -> bool:
        return (time.time() - self.created_at) > 3600

    @property
    def state(self) -> str:
        if self.error:
            return "ERROR"
        if self.tokens:
            return "CONNECTED"
        if self.expired:
            return "EXPIRED"
        return "AWAITING_CONSENT"


class GoogleConsent:
    """Gère les sessions de consentement OAuth.

    `client_config` est un dict au format Google :
        {"web": {"client_id": ..., "client_secret": ..., "redirect_uris": [...]}}

    Fourni par l'environnement (`GOOGLE_OAUTH_CLIENT_JSON`) — jamais en dur.
    """

    def __init__(self, client_config: dict[str, Any] | None = None):
        self.client_config = client_config
        self.sessions: dict[str, ConsentSession] = {}
        self._lock = threading.Lock()

    # -- configuration ------------------------------------------------------
    def configured(self) -> bool:
        return bool(self.client_config and self.client_config.get("web", {}).get("client_id"))

    @classmethod
    def from_env(cls) -> "GoogleConsent":
        import os

        raw = os.environ.get("GOOGLE_OAUTH_CLIENT_JSON")
        if not raw:
            return cls(None)
        try:
            return cls(json.loads(raw))
        except json.JSONDecodeError:
            return cls(None)

    # -- démarrage d'une session -------------------------------------------
    def start(self, state: str, redirect_uri: str) -> str:
        """Crée une session et retourne l'URL de consentement Google."""
        if not self.configured():
            raise OAuthNotConfigured(
                "client OAuth absent : définir GOOGLE_OAUTH_CLIENT_JSON "
                "(client_id + client_secret d'un client OAuth de type Web)"
            )
        from google_auth_oauthlib.flow import Flow

        cfg = json.loads(json.dumps(self.client_config))
        cfg.setdefault("web", {})["redirect_uris"] = [redirect_uri]

        flow = Flow.from_client_config(cfg, scopes=SCOPES, redirect_uri=redirect_uri)
        url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent select_account",   # <- le sélecteur de compte
            state=state,
        )
        with self._lock:
            self.sessions[state] = ConsentSession(flow, time.time())
        return url

    # -- retour de Google ---------------------------------------------------
    def finish(self, state: str, code: str) -> ConsentSession:
        with self._lock:
            sess = self.sessions.get(state)
        if sess is None:
            raise KeyError("session inconnue ou expirée — recommencer la connexion")
        sess.flow.fetch_token(code=code)
        sess.tokens = dict(sess.flow.credentials.token or {})
        sess.tokens["refresh_token"] = sess.flow.credentials.refresh_token
        sess.tokens["expiry"] = getattr(sess.flow.credentials, "expiry", None)
        sess.account = self._whoami(sess.tokens["access_token"])
        return sess

    def _whoami(self, access_token: str) -> dict[str, Any]:
        """Quel compte a été autorisé ? Utile pour confirmer le bon Drive."""
        try:
            req = urllib.request.Request(
                "https://www.googleapis.com/drive/v3/about?fields=user,storageQuota",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as exc:      # jamais bloquant : identité non critique
            return {"error": f"{type(exc).__name__}: {exc}"}

    # -- état ---------------------------------------------------------------
    def status(self, state: str) -> dict[str, Any]:
        with self._lock:
            sess = self.sessions.get(state)
        if sess is None:
            return {"state": "UNKNOWN"}
        out: dict[str, Any] = {"state": sess.state}
        if sess.account and "user" in sess.account:
            u = sess.account["user"]
            out["account"] = {
                "email": u.get("emailAddress"),
                "name": u.get("displayName"),
            }
        if sess.account and "storageQuota" in sess.account:
            q = sess.account["storageQuota"]
            out["quota"] = {"limit": q.get("limit"), "usage": q.get("usage")}
        if sess.error:
            out["error"] = sess.error
        return out

    def credentials(self, state: str):
        """Rend des credentials utilisables par l'API Drive, depuis la mémoire."""
        with self._lock:
            sess = self.sessions.get(state)
        if sess is None or sess.tokens is None:
            return None
        from google.oauth2.credentials import Credentials

        return Credentials(
            token=sess.tokens.get("access_token") or sess.tokens.get("token"),
            refresh_token=sess.tokens.get("refresh_token"),
            token_uri=TOKEN_URL,
            client_id=self.client_config["web"]["client_id"],
            client_secret=self.client_config["web"]["client_secret"],
            scopes=SCOPES,
        )

    def build_service(self, state: str):
        creds = self.credentials(state)
        if creds is None:
            return None
        from googleapiclient.discovery import build

        return build("drive", "v3", credentials=creds, cache_discovery=False)
