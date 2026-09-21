#!/usr/bin/env python3
"""Check that everything is actually centred.

text-align:center centres a line inside its BOX. If the box itself is pushed
around by padding (and this design is full of per-line padding nudges added to
dodge foliage), the line is still 'centred' by CSS and visibly off-centre on
the page. So measure the rendered ink, not the CSS.

Two independent checks:
  1. box centre vs its container centre   - catches stray padding/margins
  2. INK centre vs container centre       - catches a centred box whose glyphs
                                            sit off to one side

Fails loudly. Exit 1 if anything drifts more than TOL of the card width.
"""
import base64, json, os, subprocess, sys, time, urllib.request
from io import BytesIO
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL  = 1.0          # % of container width
PORT = 9334
MIN_LINES = 8


def cdp(ws, mid, method, params=None):
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == mid:
            return m.get("result", {})


JS = r"""
(() => {
  const host = document.querySelector('.hero') || document.body;
  const hb = host.getBoundingClientRect();
  const sel = '.invite1,.invite2,.names,.date,.hebdate,.venue,.reception,'
            + '.seeyou,.parents,.pasuk,.aye,.rule,.count-title,.timeline-title';
  const out = [];
  document.querySelectorAll(sel).forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const b = el.getBoundingClientRect();
    if (b.width < 2 || b.height < 2) return;
    const parent = el.parentElement.getBoundingClientRect();
    out.push({
      cls: el.className.toString().split(' ')[0],
      text: (el.textContent || '').replace(/\s+/g,' ').trim().slice(0,22),
      x: b.x, w: b.width, y: b.y, h: b.height,
      px: parent.x, pw: parent.width,
      hx: hb.x, hw: hb.width,
      align: cs.textAlign,
      padL: cs.paddingLeft, padR: cs.paddingRight,
    });
  });
  return JSON.stringify(out);
})()
"""


def run(url, label, width, height):
    import websocket
    tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
    page = [t for t in tabs if t["type"] == "page"][0]
    ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30)
    mid = [0]
    def c(m, p=None):
        mid[0] += 1
        return cdp(ws, mid[0], m, p)

    c("Emulation.setDeviceMetricsOverride",
      {"width": width, "height": height, "deviceScaleFactor": 2,
       "mobile": False, "screenWidth": width, "screenHeight": height})
    c("Page.enable"); c("Page.navigate", {"url": url})
    time.sleep(9)
    c("Runtime.evaluate", {"expression":
        "document.querySelectorAll('.fade-up,.tl-item,.tl-vid').forEach(e=>{"
        "e.style.opacity=1;e.style.transform='none';e.style.filter='none'})"})
    time.sleep(1)
    rows = json.loads(c("Runtime.evaluate",
                        {"expression": JS, "returnByValue": True})["result"]["value"])
    shot = c("Page.captureScreenshot",
             {"format": "png", "captureBeyondViewport": True})
    img = Image.open(BytesIO(base64.b64decode(shot["data"]))).convert("RGB")
    arr = np.asarray(img).astype(int)
    dpr = img.size[0] / width
    ws.close()

    print(f"{label:12s} {len(rows):2d} blocks")
    bad = []
    for r in rows:
        hw = r["hw"]
        # 1. box centre vs hero centre
        box_c = r["x"] + r["w"] / 2
        hero_c = r["hx"] + hw / 2
        d_box = (box_c - hero_c) / hw * 100

        # 2. ink centre: find the glyph columns inside the box
        x0, y0 = max(0, int(r["x"] * dpr)), max(0, int(r["y"] * dpr))
        x1 = min(arr.shape[1], int((r["x"] + r["w"]) * dpr))
        y1 = min(arr.shape[0], int((r["y"] + r["h"]) * dpr))
        d_ink = None
        if x1 > x0 and y1 > y0:
            patch = arr[y0:y1, x0:x1]
            lum = patch.sum(2)
            r_, g_, b_ = patch[..., 0], patch[..., 1], patch[..., 2]
            # A text box often spans the full column width, so foliage sitting
            # inside it would be counted as ink and drag the centre sideways.
            # Text is near-neutral (wine/gold); leaves are strongly green.
            # NB --wine (#4b4f39) is itself an olive: g-b = 22, g-r = 4. A
            # loose green test therefore masks the body text as foliage and
            # reports wild offsets. Leaves are far greener than the ink.
            leaf = (g_ - b_ > 25) & (g_ - r_ > 10) & (lum < 620)
            # Threshold relative to the PAPER, not to the darkest pixel: if a
            # leaf intrudes it owns the dark tail, the threshold drops below
            # the (light, gold) text and only the leaf is measured as ink.
            paper = np.percentile(lum, 85)
            thr = paper - 75
            ink_mask = (lum < thr) & ~leaf
            cols = ink_mask.sum(0)
            # Foliage fills a column top to bottom; a glyph stroke does not.
            # Drop columns that are more than 60% solid, otherwise a leaf
            # sitting inside a full-width text box drags the centroid to it.
            cols = np.where(cols > 0.60 * ink_mask.shape[0], 0, cols)
            if cols.sum() > 30:
                # centroid, not first/last column: a single stray dark pixel
                # (a gold dot, the arc clipping the box) moved the midpoint by
                # a third of the card and invented failures that were not real
                xs = np.arange(len(cols))
                ink_c = float((xs * cols).sum() / cols.sum()) / dpr + r["x"]
                d_ink = (ink_c - hero_c) / hw * 100

        flags = []
        if abs(d_box) > TOL: flags.append(f"box {d_box:+.1f}%")
        if d_ink is not None and abs(d_ink) > TOL: flags.append(f"ink {d_ink:+.1f}%")
        if flags:
            pad = ""
            if r["padL"] != r["padR"]:
                pad = f"  (padding {r['padL']} / {r['padR']})"
            bad.append(f"    {r['cls'][:14]:14s} {r['text'][:22]:22s} "
                       f"{', '.join(flags)}{pad}")
    for b in bad:
        print(b)
    return len(rows), bad


def main():
    prof = "/tmp/ctrprof"
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    p = subprocess.Popen([chrome, f"--remote-debugging-port={PORT}",
                          f"--user-data-dir={prof}", "--headless=new",
                          "--no-first-run", "--hide-scrollbars",
                          "--remote-allow-origins=*", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    total, allbad = 0, []
    try:
        for lang, q in [("he", ""), ("dati", "?lang=dati"), ("nl", "?lang=nl")]:
            n, bad = run(f"file://{ROOT}/_card.html{q}", f"card {lang}", 900, 1360)
            total += n; allbad += bad
        for lang, q in [("he", ""), ("dati", "?lang=dati"), ("nl", "?lang=nl")]:
            n, bad = run(f"file://{ROOT}/index.html{q}", f"page {lang}", 430, 932)
            total += n; allbad += bad
    finally:
        p.terminate()
    print(f"\n{total} blocks checked, {len(allbad)} off-centre (tolerance {TOL}%)")
    if total < MIN_LINES * 6:
        print("REFUSING: too few blocks measured, the selector is broken")
        sys.exit(1)
    sys.exit(1 if allbad else 0)


if __name__ == "__main__":
    main()
