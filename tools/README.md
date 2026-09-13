# tools

`shot.py` — phone-accurate screenshots. macOS Chrome refuses windows narrower than
~500px, so `--headless --window-size=430,932` silently renders a 500px layout and
crops it. Only CDP `Emulation.setDeviceMetricsOverride` gives a real 430px viewport.

    /private/tmp/bach/invite/.venv/bin/python tools/shot.py \
      "file://$HOME/wedding-invitation/index_green.html" /tmp/x.png 430 932
    SCROLLY=1200 ... tools/shot.py ...      # scroll before shooting
    ... tools/shot.py <url> <out> 430 932 full   # whole page

Generated icon sources live in `icons/src/` — NOT in /tmp, which gets wiped.
