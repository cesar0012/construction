#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor estático de Roque General Construction LLC con:
- URLs amigables (mapa de rutas -> archivos .html)
- Redirección 301 desde .html y trailing slash a la ruta canónica limpia
- Modo demo (DEMO=1): Cache-Control no-store + X-Robots-Tag noindex
- Cabeceras de seguridad básicas y caché de assets
- 404 controlada, sin directory listing y con protección path traversal
- /healthz para health checks; bloqueo de UAs de espejado (no de monitoreo)
"""
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
DEMO = os.environ.get("DEMO", "0") == "1"
CANONICAL_HOST = os.environ.get("CANONICAL_HOST", "")  # p. ej. "www.roquegeneral.com"

# Ruta limpia -> archivo
ROUTES = {
    "/": "index.html",
    "/about": "about.html",
    "/services": "services.html",
    "/services/siding": "services/siding.html",
    "/services/framing": "services/framing.html",
    "/services/roofing-repairs": "services/roofing-repairs.html",
    "/services/demolition": "services/demolition.html",
    "/services/junk-removal": "services/junk-removal.html",
    "/gallery": "gallery.html",
    "/contact": "contact.html",
    "/404": "404.html",
}

# UAs de herramientas de espejado que se bloquean (curl/wget pasan: health checks)
BLOCKED_UA = re.compile(r"httrack|webcopier|webzip|sitegrabber|scrapy", re.I)

MIME_EXTRA = {
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".webmanifest": "application/manifest+json",
    ".xml": "application/xml",
}


class Handler(SimpleHTTPRequestHandler):
    body_suppressed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):  # log compacto
        print("[http] %s %s" % (self.command, self.path))

    def do_HEAD(self):
        self.body_suppressed = True
        try:
            self.do_GET()
        finally:
            self.body_suppressed = False

    # ---- utilidades ----
    def _send_file(self, filename, status=200):
        path = os.path.normpath(os.path.join(ROOT, filename))
        if not path.startswith(ROOT) or not os.path.isfile(path):
            self._send_404()
            return
        ext = os.path.splitext(filename)[1].lower()
        ctype = MIME_EXTRA.get(ext) or self.guess_type(filename) or "application/octet-stream"
        try:
            with open(path, "rb") as f:
                body = f.read()
        except OSError:
            self._send_404()
            return
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if DEMO:
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Robots-Tag", "noindex, nofollow")
        else:
            if ext in (".css", ".js", ".webp", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".woff2", ".mp4", ".webm"):
                self.send_header("Cache-Control", "public, max-age=604800")
            else:
                self.send_header("Cache-Control", "public, max-age=300")
        for h, v in self._security_headers():
            self.send_header(h, v)
        self.end_headers()
        if not self.body_suppressed:
            self.wfile.write(body)

    def _security_headers(self):
        return [
            ("X-Content-Type-Options", "nosniff"),
            ("Referrer-Policy", "strict-origin-when-cross-origin"),
            ("X-Frame-Options", "SAMEORIGIN"),
        ]

    def _redirect(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        for h, v in self._security_headers():
            self.send_header(h, v)
        self.end_headers()

    def _send_404(self):
        path = os.path.join(ROOT, "404.html")
        if os.path.isfile(path):
            with open(path, "rb") as f:
                body = f.read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Robots-Tag", "noindex, nofollow")
            for h, v in self._security_headers():
                self.send_header(h, v)
            self.end_headers()
            if not self.body_suppressed:
                self.wfile.write(body)
        else:
            self.send_error(404)

    # ---- despacho ----
    def do_GET(self):
        ua = self.headers.get("User-Agent", "")
        if BLOCKED_UA.search(ua):
            self.send_error(403)
            return

        raw = self.path.split("?", 1)[0].split("#", 1)[0]

        if raw == "/healthz":
            body = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # dominio canónico (apex -> www) si está configurado
        if CANONICAL_HOST:
            host = self.headers.get("Host", "")
            if host and host.split(":")[0] != CANONICAL_HOST:
                self._redirect("https://" + CANONICAL_HOST + raw)
                return

        clean = raw.rstrip("/") or "/"
        # 1) ruta limpia exacta
        if clean in ROUTES:
            if raw != clean and raw != clean + "/":
                self._redirect(clean)
                return
            if raw.endswith("/") and clean != "/":
                self._redirect(clean)
                return
            self._send_file(ROUTES[clean])
            return
        # 2) alguien llegó a un .html -> 301 a la ruta limpia
        if clean.endswith(".html"):
            candidate = clean[:-5] or "/"
            if candidate in ROUTES:
                self._redirect(candidate)
                return
        # 3) activos estáticos
        if "." in os.path.basename(raw):
            self._send_file(clean.lstrip("/"))
            return
        # 4) todo lo demás -> 404 controlada
        self._send_404()


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    mode = "DEMO (noindex)" if DEMO else "producción"
    print(f"RGC site listo en http://0.0.0.0:{port} — modo {mode}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
