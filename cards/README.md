# Static invitation cards (for sending as an image)

Rebuilt from `index.html` itself, so they cannot drift from the live page.

| file | use |
|---|---|
| `invitation_he.jpg`        | Hebrew — the main one |
| `invitation_dati.jpg`      | dati front (Ronen's format) |
| `invitation_dati_back.jpg` | dati back — names, date, the Rebbe's ksav yad |
| `invitation_nl.jpg`        | Dutch |

Three formats of each, all rendered at **3x — 2700x4050**:

| format | when |
|---|---|
| `.png` | lossless master — text is pixel-crisp, no JPEG mush around the letters |
| `.pdf` | 300 dpi, for a print shop — 22.9 x 34.3 cm at that density |
| `.jpg` | q92, for sending — ~1 MB |

WhatsApp recompresses anything sent as a *photo* and will soften the small
Hebrew type. **Send the PNG (or PDF) as a document** to keep it sharp.

## Rebuild

```bash
python3 tools/make_card.py front         # writes _card.html
DPR=3 WAIT=9 tools/.venv/bin/python tools/shot.py "file://$PWD/_card.html" /tmp/c.png 900 1360
magick /tmp/c.png -crop 2700x4050+0+0 +repage -strip cards/invitation_he.png
# ?lang=nl and ?lang=dati for the other two; tools/back_card.html for the back
```
