#!/usr/bin/env python3
"""Regenerate assets/og.jpg and assets/apple-touch-icon.png.

The card is a screenshot of a throwaway page built from this site's own stylesheet
and hero photo, so it always matches the real page. The eyebrow and date are read
out of js/i18n.js, so editing them there is enough. The touch icon is favicon.svg
rendered at 180px, so the two marks stay identical.

    python3 gen-og.py

Needs Google Chrome. Uses sips for the JPEG, so it keeps the PNG on non-macOS.
"""
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]
WIDTH, HEIGHT = 1200, 630
ICON = 180

CSS = """
body{margin:0;width:1200px;height:630px;overflow:hidden;display:flex;
     flex-direction:column;align-items:center;justify-content:flex-end;
     text-align:center;padding:0 64px 58px;box-sizing:border-box}
.photo{position:absolute;width:1200px;height:630px}
.eyebrow{font-size:20px;margin:0 0 18px}
h1{font-size:100px;line-height:1}
.date{font-size:34px;margin:22px 0 0}
.url{margin:24px 0 0;font-size:18px;letter-spacing:.18em;text-transform:uppercase;
     color:var(--on-photo-dim)}
"""


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    sys.exit("Google Chrome not found - add its path to CHROME_CANDIDATES.")


def english():
    """Eyebrow and date from the en block of js/i18n.js."""
    src = open(os.path.join(ROOT, "js/i18n.js"), encoding="utf-8").read()
    en = src.split("no:")[0]

    def get(key):
        m = re.search(r"'%s':\s*'((?:[^'\\]|\\.)*)'" % re.escape(key), en)
        if not m:
            sys.exit(f"'{key}' not found in the en block of js/i18n.js")
        return m.group(1).replace("\\'", "'")

    return get("hero.eyebrow"), get("hero.date")


def shot(chrome, page, out, width, height):
    # Written into the repo root so the relative css/ and assets/ paths resolve.
    fd, tmp = tempfile.mkstemp(suffix=".html", dir=ROOT)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(page)
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                        f"--screenshot={out}", f"--window-size={width},{height}",
                        "--hide-scrollbars", "file://" + tmp],
                       check=True, capture_output=True)
    finally:
        os.unlink(tmp)


def main():
    chrome = find_chrome()
    eyebrow, date = english()
    png = os.path.join(ROOT, "assets/og.png")
    jpg = os.path.join(ROOT, "assets/og.jpg")
    icon = os.path.join(ROOT, "assets/apple-touch-icon.png")

    shot(chrome,
         '<!doctype html><meta charset="utf-8">'
         '<link rel="stylesheet" href="css/style.css">'
         f'<style>{CSS}</style>'
         '<body class="has-photo">'
         '<img class="photo" src="assets/hero.webp" alt="">'
         f'<p class="eyebrow">{eyebrow}</p>'
         '<h1>Arne &amp; Klara</h1>'
         f'<p class="date">{date}</p>'
         '<p class="url">arneandklara.wedding</p>',
         png, WIDTH, HEIGHT)

    shot(chrome,
         '<!doctype html><meta charset="utf-8">'
         f'<style>html,body{{margin:0;width:{ICON}px;height:{ICON}px;overflow:hidden}}'
         f'img{{width:{ICON}px;height:{ICON}px;display:block}}</style>'
         '<img src="assets/favicon.svg" alt="">',
         icon, ICON, ICON)
    print(f"  assets/apple-touch-icon.png  {ICON}x{ICON}  "
          f"{os.path.getsize(icon) / 1024:.0f} KB")

    try:
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80",
                        png, "--out", jpg], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"  sips unavailable - keeping {os.path.relpath(png, ROOT)}")
        print("  point og:image at the PNG, or convert it yourself")
        return
    os.unlink(png)
    print(f"  assets/og.jpg  {WIDTH}x{HEIGHT}  {os.path.getsize(jpg) / 1024:.0f} KB")
    print("  scrapers cache by URL - bump ?v= on og:image in index.html")


if __name__ == "__main__":
    main()
