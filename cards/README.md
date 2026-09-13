# Static invitation cards (for sending as an image)

Rebuilt from `index.html` itself, so they cannot drift from the live page.

| file | use |
|---|---|
| `invitation_he.jpg`        | Hebrew — the main one |
| `invitation_dati.jpg`      | dati front (Ronen's format) |
| `invitation_dati_back.jpg` | dati back — names, date, the Rebbe's ksav yad |
| `invitation_nl.jpg`        | Dutch |

1800px wide (2700 tall), the hero at 2x. WhatsApp recompresses anything sent as
a photo — send **as a document** to keep this quality.

## Rebuild

```bash
python3 tools/make_card.py front         # writes _card.html
WAIT=8 tools/.venv/bin/python tools/shot.py "file://$PWD/_card.html" /tmp/c.png 900 1360
magick /tmp/c.png -crop 1800x2700+0+0 +repage -quality 92 -strip cards/invitation_he.jpg
# ?lang=nl and ?lang=dati for the other two; tools/back_card.html for the back
```
