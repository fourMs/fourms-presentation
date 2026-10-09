#!/usr/bin/env python3
"""Build a flat PDF of the fourMs Lab deck.

Screenshots every slide with headless Chrome at 1920x1080 and assembles the
pages with Pillow. Run from anywhere:

    .venv/bin/python tools/build_pdf.py                       # every slide, stacks included
    .venv/bin/python tools/build_pdf.py --venue Oslo --date "9 October 2026"

The deck is served over HTTP rather than opened as file:// so that the
images and scripts load the same way as they do in a
talk.
"""
import argparse
import http.server
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
from urllib.parse import urlencode

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PRES = os.path.dirname(HERE)
INDEX = os.path.join(PRES, "index.html")

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser")
               if shutil.which(c)), None)


def slide_addresses():
    """Every slide as an "h" or "h/v" address, in the order Space walks them.

    Counts tag nesting rather than trusting indentation, which drifts as the
    deck is edited.
    """
    html = open(INDEX, encoding="utf8").read()
    body = html.split('<div class="slides">', 1)[1].rsplit("</div>\n</div>", 1)[0]

    out, depth, h, v, had_child = [], 0, -1, 0, False
    for m in re.finditer(r"<section\b[^>]*>|</section\s*>", body):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0 and not had_child:
                out.append(str(h))            # a stack of one: plain "h"
        else:
            if depth == 0:
                h, v, had_child = h + 1, 0, False
            else:
                out.append(f"{h}/{v}")
                v += 1
                had_child = True
            depth += 1
    return out


def serve(directory):
    """Serve the deck on a free port; returns (port, shutdown)."""
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=directory, **kw)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown


def shoot(url, out, budget):
    subprocess.run(
        [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
         "--hide-scrollbars", "--window-size=1920,1080",
         # Cross-origin iframes do not paint reliably under virtual time with
         # site isolation on, which leaves the live embeds blank.
         "--disable-features=IsolateOrigins,site-per-process",
         "--disable-site-isolation-trials",
         f"--virtual-time-budget={budget}", f"--screenshot={out}", url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", default=None, help="occasion on the title slide")
    ap.add_argument("--date", default=None, help="date on the title slide")
    ap.add_argument("--budget", type=int, default=3000,
                    help="milliseconds of virtual time per slide")
    ap.add_argument("-o", "--out", default=None, help="output PDF path")
    args = ap.parse_args()

    if CHROME is None:
        sys.exit("No Chrome or Chromium found on PATH.")

    addresses = slide_addresses()
    total = len(addresses)
    out = args.out or os.path.join(PRES, "fourms.pdf")

    query = {k: v for k, v in (("venue", args.venue), ("date", args.date)) if v}

    port, shutdown = serve(PRES)
    qs = urlencode(query)
    base = f"http://127.0.0.1:{port}/index.html?{qs}&" if qs else \
           f"http://127.0.0.1:{port}/index.html?"

    pages = []
    with tempfile.TemporaryDirectory() as tmp:
        try:
            for i, addr in enumerate(addresses):
                png = os.path.join(tmp, f"s{i:03d}.png")
                print(f"  slide {i + 1}/{total}  ({addr})   ", end="\r", flush=True)
                # fragments=false so a click-revealed slide prints complete
                shoot(f"{base}print=1&fragments=false#/{addr}", png, args.budget)
                if os.path.exists(png):
                    pages.append(Image.open(png).convert("RGB"))
                else:
                    print(f"\n  ! slide {i + 1} did not render; skipped")
        finally:
            shutdown()

        if not pages:
            sys.exit("Nothing rendered.")
        pages[0].save(out, save_all=True, append_images=pages[1:],
                      resolution=150.0)

    print(f"\nWrote {out} — {len(pages)} page(s)")


if __name__ == "__main__":
    main()
