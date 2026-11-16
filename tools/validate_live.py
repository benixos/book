#!/usr/bin/env python3
"""Check that the live site matches the built site in docs/.

Usage:  python3 -I tools/validate_live.py [base-url]        (standard library only)

Checks, in order: DNS, HTTPS certificate, HTTP behaviour, every file in docs/ served
and byte-identical, a custom 404, and the footer on every page.

Exit status: 0 if every check passes (warnings allowed), 1 if any check fails.
Run it after a publish, once the Pages build has finished (about a minute).
"""
import datetime
import hashlib
import pathlib
import socket
import ssl
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://book.benixos.com/").rstrip("/") + "/"
HOST = urlparse(BASE).hostname
SKIP = {"CNAME", ".nojekyll"}  # configuration files, not served as pages
FOOTER = "We use AI tools to help build and write this site; a person reviews what we publish."

fails, warns = [], []


def ok(msg):
    print(f"  ok    {msg}")


def fail(msg):
    fails.append(msg)
    print(f"  FAIL  {msg}")


def warn(msg):
    warns.append(msg)
    print(f"  warn  {msg}")


def get(url, follow=True):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "benixos-book-validate/1"})
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def main():
    print(f"Validating {BASE} against {DOCS.relative_to(ROOT)}/")

    print("DNS")
    try:
        addrs = sorted({a[4][0] for a in socket.getaddrinfo(HOST, 443, proto=socket.IPPROTO_TCP)})
        ok(f"{HOST} resolves to {', '.join(addrs)}")
    except OSError as e:
        fail(f"{HOST} does not resolve: {e}")
        return

    print("HTTPS certificate")
    try:
        with socket.create_connection((HOST, 443), timeout=20) as s:
            with ssl.create_default_context().wrap_socket(s, server_hostname=HOST) as t:
                cert = t.getpeercert()
        end = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        days = (end - now).days
        names = [v for k, v in cert["subjectAltName"] if k == "DNS"]
        ok(f"valid for {', '.join(names)}; expires in {days} days")
        if HOST not in names:
            fail(f"certificate does not name {HOST}")
        if days < 14:
            fail(f"certificate expires in {days} days")
        elif days < 30:
            warn(f"certificate expires in {days} days")
    except (ssl.SSLError, OSError) as e:
        fail(f"HTTPS handshake failed: {e}")

    print("HTTP behaviour")
    st, _, hdr = get(f"http://{HOST}/", follow=False)
    if st in (301, 308) and hdr.get("Location", "").startswith("https://"):
        ok("http redirects to https")
    elif st == 200:
        warn("http is served without redirecting to https (HTTPS is not enforced)")
    else:
        fail(f"http returned {st}")

    print("Files")
    files = sorted(p for p in DOCS.rglob("*") if p.is_file() and p.name not in SKIP)
    same = 0
    for p in files:
        rel = p.relative_to(DOCS).as_posix()
        st, body, _ = get(BASE + rel)
        if st != 200:
            fail(f"{rel}: status {st}")
        elif hashlib.sha256(body).digest() != hashlib.sha256(p.read_bytes()).digest():
            fail(f"{rel}: differs from docs/ (stale deploy or CDN cache; retry in ten minutes)")
        else:
            same += 1
        if p.suffix == ".html" and st == 200 and FOOTER not in body.decode("utf-8", "replace"):
            fail(f"{rel}: footer sentence missing")
    if same == len(files):
        ok(f"{same} files served and byte-identical to docs/")
    else:
        print(f"        {same} of {len(files)} files match")

    print("Not found")
    st, body, _ = get(BASE + "no-such-page-validate.html")
    if st == 404 and b"Page not found" in body:
        ok("a missing page returns 404 with the custom page")
    else:
        fail(f"missing page returned {st}")


if __name__ == "__main__":
    main()
    print()
    print(f"{len(fails)} failure(s), {len(warns)} warning(s)")
    sys.exit(1 if fails else 0)
