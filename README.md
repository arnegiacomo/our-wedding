# arneandklara.wedding

Single page for our wedding. Plain HTML, CSS and some JS, hosted on GitHub Pages.

Run locally with `python3 dev.py` - serves on http://localhost:8000 with live reload
on any `.html`, `.css` or `.js` change.

Regenerate the link preview card with `python3 gen-og.py` after changing the photo,
the date or the palette. Bump `?v=` on `og:image` in `index.html` when it changes.