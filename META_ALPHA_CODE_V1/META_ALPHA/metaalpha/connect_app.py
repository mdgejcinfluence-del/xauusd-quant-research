"""Le bouton « Se connecter à Drive » — application web locale.

Ce n'est pas une page statique : le consentement Google exige un échange
serveur-à-serveur (client secret + code à usage unique). Il faut donc un
processus qui écoute.

    python -m metaalpha.connect_app --port 8000

Puis ouvrir l'URL affichée. La page propose le bouton ; Google affiche son
propre sélecteur de compte ; le retour affiche l'email du compte connecté et
cherche le corpus META_ALPHA sur ce Drive.

Aucun mot de passe ne transite. Aucun jeton n'est écrit sur disque.
"""
from __future__ import annotations

import argparse
import json
import secrets
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .oauth_drive import GoogleConsent, OAuthNotConfigured

CONSENT = GoogleConsent.from_env()

SEARCH_TERMS = ("META_ALPHA", "XAUUSD", "PARTITIONS", "DGP")


# ---------------------------------------------------------------------------
# Logique métier — testable sans serveur HTTP
# ---------------------------------------------------------------------------
def find_corpus(service, *, max_per_term: int = 10) -> dict[str, Any]:
    """Cherche le corpus sur le Drive du compte connecté.

    Trois angles, parce qu'un corpus peut être nommé de plusieurs façons :
      1. le nom du dossier racine ;
      2. les certificats ;
      3. les partitions Parquet.

    Ne lit aucun contenu : uniquement des noms et des identifiants.
    """
    found: dict[str, Any] = {"roots": [], "certificates": [], "partitions": [], "queries": []}

    def q(query: str, fields: str = "files(id,name,mimeType,size,parents,modifiedTime)") -> list[dict]:
        try:
            res = service.files().list(
                q=query, spaces="drive", pageSize=max_per_term, fields=fields,
                supportsAllDrives=True, includeItemsFromAllDrives=True,
            ).execute()
            return res.get("files", [])
        except Exception as exc:
            found["queries"].append({"query": query, "error": f"{type(exc).__name__}"})
            return []

    # 1. dossiers dont le nom évoque le projet
    for term in SEARCH_TERMS:
        files = q(f"name contains '{term}' and mimeType = 'application/vnd.google-apps.folder' "
                  f"and trashed = false")
        found["queries"].append({"query": term, "hits": len(files)})
        for f in files:
            f["_matched"] = term
            found["roots"].append(f)

    # 2. certificats
    certs = q("name contains 'PHASE_0' and name contains '.json' and trashed = false")
    found["certificates"] = certs

    # 3. partitions
    parts = q("name contains 'part_000' and trashed = false")
    found["partitions"] = parts
    found["partitions_count_sample"] = len(parts)

    found["summary"] = {
        "root_folders_candidates": len({f["id"] for f in found["roots"]}),
        "certificates_found": len(certs),
        "partitions_visible": len(parts),
        "looks_like_corpus": bool(certs) and len(parts) > 0,
    }
    return found


# ---------------------------------------------------------------------------
# Rendu HTML
# ---------------------------------------------------------------------------
def _page(state: str, *, redirect_uri: str) -> str:
    st = CONSENT.status(state)
    connected = st.get("state") == "CONNECTED"
    configured = CONSENT.configured()

    if not configured:
        body = """
<div class="warn">
  <b>Une seule chose manque : le client OAuth Google.</b>
  <p>Ce ne sont pas vos identifiants Google. C'est une paire publique
  <code>client_id</code> / <code>client_secret</code> que Google exige de toute
  application qui affiche un bouton « Se connecter ». Créez-la une fois (4 minutes),
  collez-la ci-dessous, et le bouton s'active immédiatement.</p>
</div>

<ol class="steps">
  <li>Ouvrir <a href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noopener">console.cloud.google.com/apis/credentials</a></li>
  <li><b>Créer des identifiants</b> → <b>ID client OAuth</b></li>
  <li>Type d'application : <b>Application Web</b></li>
  <li>Dans <b>URI de redirection autorisés</b>, coller exactement :
      <pre id="redirect-uri">__REDIRECT__</pre>
      <button class="btn tiny" onclick="navigator.clipboard.writeText(document.getElementById('redirect-uri').textContent.trim());this.textContent='copié ✓';return false">copier</button></li>
  <li>Créer → copier le <b>client ID</b> et le <b>client secret</b></li>
  <li>Les coller ci-dessous</li>
</ol>

<form method="post" action="/configure" class="cfg">
  <label>Client ID
    <input name="client_id" placeholder="1234567890-xxxxxxxx.apps.googleusercontent.com" required>
  </label>
  <label>Client secret
    <input name="client_secret" type="password" placeholder="GOCSPX-…" required>
  </label>
  <input type="hidden" name="redirect_uri" value="__REDIRECT__">
  <button class="btn" type="submit">Activer le bouton</button>
</form>
<p class="hint">Ces deux valeurs restent en mémoire du processus. Elles ne sont écrites
sur aucun disque et ne quittent jamais ce serveur — sauf vers Google, qui les a émises.</p>
"""
    elif not connected:
        body = f"""
<a class="btn" href="/start?state={state}">
  <svg width="19" height="19" viewBox="0 0 48 48" aria-hidden="true"><path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-2.8-.4-4H24v7.3h12c-.2 2-1.5 5-4.4 7l6.7 5.2c4-3.7 6.8-9.1 6.8-15.5z"/><path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-6.9-5.4c-1.9 1.3-4.4 2.2-7.6 2.2-5.8 0-10.7-3.8-12.5-9.1l-7.1 5.5C8 41 15.4 46 24 46z"/><path fill="#FBBC05" d="M11.5 28.4a13.5 13.5 0 0 1 0-8.8l-7.1-5.5a22 22 0 0 0 0 19.8l7.1-5.5z"/><path fill="#EA4335" d="M24 9.5c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.9 3.2 29.9 1 24 1 15.4 1 8 6 3.4 14.1l7.1 5.5C12.3 14.3 17.2 9.5 24 9.5z"/></svg>
  Se connecter à Drive
</a>
<p class="hint">Google s'ouvre, vous choisissez le compte, vous autorisez la <b>lecture</b> du Drive.
Aucun mot de passe ne passe par ce serveur. Le jeton reste en mémoire et se révoque en un clic.</p>
<div class="why">
  <b>Pourquoi « lecture seule » ?</b> Le corpus certifié ne doit jamais être modifiable.
  Le système écrit ailleurs, dans un dossier distinct. Ce choix est dans le code, pas dans une consigne.
</div>"""
    else:
        acct = st.get("account", {})
        email = acct.get("email") or "compte inconnu"
        body = f"""
<div class="ok">
  <b>Connecté.</b>
  <div class="acct">{email}</div>
</div>
<p class="hint">C'est bien ce compte que vous vouliez ? Si non, déconnectez-vous et recommencez :
Google reproposera le sélecteur.</p>
<div class="row">
  <a class="btn small" href="/scan?state={state}">Chercher le corpus sur ce Drive</a>
  <a class="btn ghost" href="/forget?state={state}">Changer de compte</a>
</div>
<div id="scan"></div>
<div class="why">
  <b>Étape suivante, une seule fois :</b> créer un compte de service et partager le dossier
  corpus avec lui. Le bouton sert à trouver et confirmer le bon Drive&nbsp;; le compte de service
  sert à faire tourner le système à 3 h du matin sans vous. Les deux ensemble, pas l'un contre l'autre.
</div>"""

    body = body.replace("__REDIRECT__", redirect_uri)

    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>META ALPHA — Connexion Drive</title>
<style>
:root{{--bg:#070a0e;--card:#111820;--lin:#1f2b38;--tx:#e8eef4;--mut:#8497a9;--ok:#3fb950;--bad:#f85149;--acc:#58a6ff;--warn:#d29922}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--tx);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:40px 18px}}
.wrap{{max-width:600px;margin:0 auto}}
h1{{font-size:23px;margin:0 0 6px;letter-spacing:-.02em}}
p.sub{{color:var(--mut);margin:0 0 26px;font-size:14px}}
.card{{background:var(--card);border:1px solid var(--lin);border-radius:14px;padding:30px 26px;text-align:center}}
.btn{{display:inline-flex;align-items:center;gap:11px;background:#fff;color:#1f1f1f;text-decoration:none;
font-weight:600;font-size:15px;padding:13px 26px;border-radius:9px;border:1px solid #dadce0;transition:.15s}}
.btn:hover{{box-shadow:0 2px 10px rgba(255,255,255,.14)}}
.btn.small{{font-size:13.5px;padding:10px 18px;background:var(--acc);color:#fff;border-color:transparent}}
.btn.ghost{{font-size:13.5px;padding:10px 18px;background:transparent;color:var(--mut);border:1px solid var(--lin)}}
.hint{{color:var(--mut);font-size:12.5px;margin:16px 0 0;line-height:1.65}}
.why{{margin-top:22px;padding-top:18px;border-top:1px solid var(--lin);color:var(--mut);font-size:12.5px;text-align:left;line-height:1.7}}
.warn,.ok{{border-left:3px solid var(--warn);padding:13px 16px;background:#1a1508;border-radius:0 9px 9px 0;font-size:13.5px;text-align:left;margin-bottom:18px}}
.ok{{border-left-color:var(--ok);background:#0a1a10}}
.warn p{{margin:8px 0 0;font-size:13px;color:var(--mut)}}
.acct{{font-family:ui-monospace,Menlo,monospace;font-size:15px;margin-top:7px;color:#fff}}
.row{{display:flex;gap:10px;justify-content:center;margin-top:18px;flex-wrap:wrap}}
code{{background:#0a0f15;padding:2px 6px;border-radius:4px;font-size:12px;color:#39c5cf}}
pre{{background:#0a0f15;border:1px solid var(--lin);border-radius:8px;padding:11px;overflow-x:auto;font-size:11.5px;color:#b9c9d8;text-align:left;margin-top:10px}}
#scan{{margin-top:20px;text-align:left}}
.res{{background:#0a0f15;border:1px solid var(--lin);border-radius:9px;padding:14px;font-size:12.5px;margin-top:12px;white-space:pre-wrap;font-family:ui-monospace,Menlo,monospace;line-height:1.7;max-height:340px;overflow:auto}}
.foot{{color:#55636f;font-size:11.5px;text-align:center;margin-top:26px;line-height:1.8}}
.steps{{text-align:left;color:var(--mut);font-size:13px;line-height:1.85;margin:0 0 20px;padding-left:20px}}
.steps b{{color:var(--tx)}}.steps a{{color:var(--acc)}}
.steps pre{{margin:6px 0;display:inline-block}}
.cfg{{text-align:left;display:grid;gap:13px;margin-top:8px}}
.cfg label{{font-size:12px;color:var(--mut);display:grid;gap:5px;font-weight:600;letter-spacing:.02em}}
.cfg input{{background:#0a0f15;border:1px solid var(--lin);border-radius:7px;padding:10px 12px;
color:var(--tx);font-size:13px;font-family:ui-monospace,Menlo,monospace}}
.cfg input:focus{{outline:none;border-color:var(--acc)}}
.btn.tiny{{font-size:11px;padding:4px 10px;background:#1a2530;color:var(--acc);border:1px solid var(--lin);vertical-align:middle}}
</style></head><body><div class="wrap">
<h1>Connexion à votre Drive</h1>
<p class="sub">Choisissez le compte Google qui contient <code>META_ALPHA_XAUUSD_DGP</code>. Google affichera son propre sélecteur — ce serveur ne voit jamais votre mot de passe.</p>
<div class="card">{body}</div>
<p class="foot">Jeton en mémoire du processus · jamais écrit sur disque · révocable dans
<a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener">votre compte Google</a> à tout moment</p>
</div>
<script>
document.querySelectorAll('[href^="/scan"]').forEach(function(a){{
  a.addEventListener('click', async function(e){{
    e.preventDefault();
    var box = document.getElementById('scan');
    box.innerHTML = '<div class="res">Recherche en cours…</div>';
    var r = await fetch(a.getAttribute('href'));
    box.innerHTML = '<div class="res">' + (await r.text()).replace(/[<>]/g,'') + '</div>';
  }});
}});
</script>
</body></html>"""


# ---------------------------------------------------------------------------
# Serveur HTTP
# ---------------------------------------------------------------------------
def make_handler(public_host: str):
    class Handler(BaseHTTPRequestHandler):
        server_version = "MetaAlphaConnect/1.0"

        def log_message(self, fmt: str, *args) -> None:   # bruit réduit
            pass

        def _send(self, code: int, body: str, ctype: str = "text/html; charset=utf-8") -> None:
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _redirect_uri(self) -> str:
            # Google exige une URI de redirection déclarée à l'identique.
            # On la déduit de l'hôte réel de la requête : le serveur fonctionne
            # donc aussi bien en local qu'derrière le proxy de prévisualisation,
            # sans configuration.
            host = (self.headers.get("X-Forwarded-Host")
                    or self.headers.get("Host")
                    or public_host)
            scheme = self.headers.get("X-Forwarded-Proto") or (
                "http" if host.startswith("localhost") or host.startswith("127.") else "https")
            return f"{scheme}://{host}/oauth/callback"

        def do_POST(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/configure":
                return self._send(404, "introuvable")
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(min(length, 8192)).decode("utf-8", "replace")
            form = urllib.parse.parse_qs(raw)
            cid = (form.get("client_id") or [""])[0].strip()
            secret = (form.get("client_secret") or [""])[0].strip()
            if not cid or not secret:
                return self._send(400, "<p>les deux champs sont requis</p>")
            CONSENT.client_config = {
                "web": {
                    "client_id": cid,
                    "client_secret": secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            }
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)

            if parsed.path == "/healthz":
                return self._send(200, json.dumps({"ok": True}), "application/json")

            if parsed.path == "/":
                state = qs.get("state", [None])[0]
                if not state:
                    state = secrets.token_urlsafe(16)
                return self._send(200, _page(state, redirect_uri=self._redirect_uri()))

            if parsed.path == "/start":
                state = (qs.get("state") or [secrets.token_urlsafe(16)])[0]
                try:
                    url = CONSENT.start(state, self._redirect_uri())
                except OAuthNotConfigured as exc:
                    return self._send(503, f"<p>{exc}</p>")
                self.send_response(302)
                self.send_header("Location", url)
                self.end_headers()
                return

            if parsed.path == "/oauth/callback":
                code = (qs.get("code") or [None])[0]
                state = (qs.get("state") or [""])[0]
                err = (qs.get("error") or [None])[0]
                if err:
                    return self._send(400, f"<p>Autorisation refusée : {err}</p>"
                                           f'<p><a href="/?state={state}">Recommencer</a></p>')
                if not code:
                    return self._send(400, "<p>code absent</p>")
                try:
                    CONSENT.finish(state, code)
                except Exception as exc:
                    return self._send(
                        400, f"<p>Échec de l'échange : {type(exc).__name__}</p>"
                             f'<p><a href="/?state={state}">Recommencer</a></p>')
                self.send_response(302)
                self.send_header("Location", f"/?state={state}")
                self.end_headers()
                return

            if parsed.path == "/scan":
                state = (qs.get("state") or [""])[0]
                svc = CONSENT.build_service(state)
                if svc is None:
                    return self._send(403, "non connecté")
                rep = find_corpus(svc)
                txt = (f"comptes: {CONSENT.status(state).get('account', {}).get('email')}\n"
                       f"dossiers candidats : {rep['summary']['root_folders_candidates']}\n"
                       f"certificats trouvés : {rep['summary']['certificates_found']}\n"
                       f"partitions visibles : {rep['summary']['partitions_visible']}\n"
                       f"ressemble au corpus : {rep['summary']['looks_like_corpus']}\n\n")
                for r in rep["roots"][:12]:
                    txt += f"  [{r['mimeType'].split('.')[-1]}] {r['name']}  → id {r['id']}\n"
                for c in rep["certificates"][:6]:
                    txt += f"  certificat : {c['name']}  → id {c['id']}\n"
                for p in rep["partitions"][:6]:
                    txt += f"  partition : {p['name']}\n"
                return self._send(200, txt, "text/plain; charset=utf-8")

            if parsed.path == "/forget":
                state = (qs.get("state") or [""])[0]
                CONSENT.sessions.pop(state, None)
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return

            return self._send(404, "<p>introuvable</p>")

    return Handler


def run(port: int = 8000, public_host: str | None = None) -> None:
    host = public_host or f"localhost:{port}"
    srv = ThreadingHTTPServer(("0.0.0.0", port), make_handler(host))
    print(f"bouton de connexion prêt sur le port {port}")
    print(f"URI de redirection à déclarer dans Google Cloud : https://{host}/oauth/callback")
    if not CONSENT.configured():
        print("ATTENTION : GOOGLE_OAUTH_CLIENT_JSON absent — le bouton s'affichera désactivé.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Bouton de connexion Google Drive")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--public-host", default=None,
                    help="hôte public (ex. 8000-abc123.e2b.app) pour l'URI de redirection")
    a = ap.parse_args()
    run(a.port, a.public_host)
