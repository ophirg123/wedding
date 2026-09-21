#!/usr/bin/env python3
"""Measure EVERY text run on the invitation for size and real contrast.

Two things the CSS can't tell you:
  * contrast against the *actual* pixels behind the glyphs (the paper is a
    photographic texture with foliage over parts of it, not a flat colour)
  * the rendered size in print terms (pt at the card's real width)

So: drive Chrome, walk every text node, get its box + colour, then sample the
rendered screenshot to find the darkest ink and the local background.

Fails loudly. Exit 1 if anything is under the thresholds.
"""
import base64, json, os, subprocess, sys, time, urllib.request
from io import BytesIO
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_W_MM = 127.0          # 5 inch card
MIN_PT    = 7.0            # below this, print shops warn
MIN_PX    = 12.0           # on screen, size is px not pt
MIN_CR    = 4.5            # WCAG AA body
MIN_CR_LG = 3.0            # AA for large text (>=18pt, or >=14pt bold)
PORT      = 9333


def cdp(ws, mid, method, params=None):
    import websocket  # noqa
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == mid:
            return m.get("result", {})


def relLum(rgb):
    c = [v / 255 for v in rgb]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    l1, l2 = sorted([relLum(a), relLum(b)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


JS = r"""
(() => {
  const out = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while (n = walk.nextNode()) {
    const t = n.textContent.replace(/\s+/g, ' ').trim();
    if (!t) continue;
    const el = n.parentElement;
    if (!el) continue;
    const cs = getComputedStyle(el);
    // opacity/visibility can be set on any ancestor (the sticky bar is
    // opacity:0 until you scroll), so walk up rather than trusting the parent
    let hidden = false;
    for (let a = el; a && a !== document.documentElement; a = a.parentElement) {
      const acs = getComputedStyle(a);
      if (acs.visibility === 'hidden' || acs.display === 'none' || +acs.opacity === 0) { hidden = true; break; }
    }
    if (hidden) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const b = r.getBoundingClientRect();
    if (b.width < 1 || b.height < 1) continue;
    if (b.bottom < 0 || b.top > document.documentElement.scrollHeight) continue;
    out.push({
      text: t.slice(0, 28),
      cls: el.className && el.className.toString ? el.className.toString().slice(0,24) : '',
      x: b.x, y: b.y, w: b.width, h: b.height,
      px: parseFloat(cs.fontSize),
      weight: cs.fontWeight,
      color: cs.color,
      family: cs.fontFamily.split(',')[0].replace(/['"]/g, ''),
      tracking: cs.letterSpacing,
    });
  }
  return JSON.stringify(out);
})()
"""


def run(url, label, width, height, viewport_mm, is_print=True):
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
    c("Page.enable")
    c("Page.navigate", {"url": url})
    time.sleep(9)
    c("Runtime.evaluate", {"expression":
        "document.querySelectorAll('.fade-up,.tl-item,.tl-vid').forEach(e=>{"
        "e.style.opacity=1;e.style.transform='none';e.style.filter='none'})"})
    time.sleep(1)

    res = c("Runtime.evaluate", {"expression": JS, "returnByValue": True})
    runs = json.loads(res["result"]["value"])

    # capture the WHOLE page: elements below the fold were being sampled
    # against clipped pixels, which faked 1.0:1 ratios
    shot = c("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
    img = Image.open(BytesIO(base64.b64decode(shot["data"]))).convert("RGB")
    arr = np.asarray(img).astype(int)
    dpr = img.size[0] / width
    ws.close()

    # px -> pt at the printed card width
    mm_per_px = viewport_mm / width
    pt_per_px = mm_per_px * 72.0 / 25.4

    bad = []
    for r in runs:
        pt = r["px"] * pt_per_px
        x0, y0 = int(r["x"] * dpr), int(r["y"] * dpr)
        x1, y1 = int((r["x"] + r["w"]) * dpr), int((r["y"] + r["h"]) * dpr)
        x0, y0 = max(0, x0), max(0, y0)
        x1 = min(arr.shape[1], x1); y1 = min(arr.shape[0], y1)
        if x1 <= x0 or y1 <= y0:
            continue
        patch = arr[y0:y1, x0:x1].reshape(-1, 3)
        lum = patch.sum(1)
        # Ink coverage varies hugely (tracked display figures cover <5% of their
        # box; dense small text covers ~25%). A fixed percentile therefore lets
        # paper leak into the "ink" sample and fakes a low contrast ratio. Use
        # the extreme tails instead, which are glyph core and clear paper.
        if lum.max() - lum.min() < 12:
            continue                     # uniform patch: element not painted
        ink = patch[lum <= np.percentile(lum, 2)].mean(0)
        bg  = patch[lum >= np.percentile(lum, 85)].mean(0)
        cr = contrast(ink, bg)

        w = r["weight"]
        try: wnum = int(w)
        except ValueError: wnum = 700 if w == "bold" else 400
        large = pt >= 18 or (pt >= 14 and wnum >= 700)
        need = MIN_CR_LG if large else MIN_CR

        probs = []
        if is_print and pt < MIN_PT: probs.append(f"{pt:.1f}pt < {MIN_PT}")
        if not is_print and r["px"] < MIN_PX: probs.append(f"{r['px']:.0f}px < {MIN_PX}")
        if cr < need:   probs.append(f"contrast {cr:.1f}:1 < {need}")
        if probs:
            bad.append((r, pt, cr, "; ".join(probs)))

    print(f"{label:12s} {len(runs):3d} text runs measured")
    for r, pt, cr, why in bad:
        print(f"    {r['cls'][:18]:18s} {r['text'][:24]:24s} {pt:5.1f}pt "
              f"w{r['weight']:3s} cr {cr:4.1f}:1   {why}")
    return len(runs), bad


def main():
    import websocket  # noqa: F401
    prof = "/tmp/readprof"
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    p = subprocess.Popen([chrome, f"--remote-debugging-port={PORT}",
                          f"--user-data-dir={prof}", "--headless=new",
                          "--no-first-run", "--hide-scrollbars", "--remote-allow-origins=*", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    total, allbad = 0, []
    try:
        # the printed card: 900px wide artboard = 127mm
        for lang, q in [("he", ""), ("dati", "?lang=dati"), ("nl", "?lang=nl")]:
            n, bad = run(f"file://{ROOT}/_card.html{q}", f"card {lang}", 900, 1600, CARD_W_MM)
            total += n; allbad += bad
        # the live page on a phone: 430px viewport ~ 66mm of real glass
        for lang, q in [("he", ""), ("dati", "?lang=dati"), ("nl", "?lang=nl")]:
            n, bad = run(f"file://{ROOT}/index.html{q}", f"page {lang}", 430, 932, 66.0, is_print=False)
            total += n; allbad += bad
    finally:
        p.terminate()

    print(f"\n{total} runs checked, {len(allbad)} problems")
    if total < 100:
        print("REFUSING: too few runs measured, the walker is broken")
        sys.exit(1)
    sys.exit(1 if allbad else 0)


if __name__ == "__main__":
    main()
