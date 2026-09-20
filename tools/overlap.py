#!/usr/bin/env python
"""Fail if any hero text sits on top of the background artwork.

Self-contained on purpose: an earlier version shelled out to a helper in /tmp,
and when /tmp was wiped the helper vanished, the subprocess returned an empty
string, and this script cheerfully reported OK for every language while text
was visibly buried under a leaf. It now drives Chrome itself and refuses to
pass if it cannot find the elements it is supposed to be checking.
"""
import json, os, subprocess, sys, time, urllib.request
from PIL import Image
import numpy as np
from websocket import create_connection

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['', '?lang=dati', '?lang=nl']
SEL = ('.hero-text .invite1,.hero-text .invite2,.hero-text .names,.hero-text .date,'
       '.hero-text .hebdate,.hero-text .venue,.hero-text .reception,.hero-text .parent-names,'
       '.hero-text .parent-label,.hero-text .seeyou,.hero-text .aye,.hero-text .pasuk')
MIN_ELEMENTS = 8        # if we see fewer than this, the measurement is broken
MIN_GAP = 4.0           # % of card width of clear paper required beside any text

src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
page = src.replace("</style>", "  .fade-up{opacity:1!important;transform:none!important;filter:none!important}\n</style>", 1)
page = page.replace("</body>", """<script>window.__M=()=>{const h=document.querySelector('.hero').getBoundingClientRect();
return [...document.querySelectorAll('%s')].filter(e=>e.offsetParent&&e.textContent.trim()).map(e=>{
const r=document.createRange();r.selectNodeContents(e);const c=r.getBoundingClientRect();
return {n:e.className.split(' ')[0],t:e.textContent.trim().slice(0,18),
x0:(c.left-h.left)/h.width*100,x1:(c.right-h.left)/h.width*100,
y0:(c.top-h.top)/h.height*100,y1:(c.bottom-h.top)/h.height*100};});};</script></body>""" % SEL)
tmp = os.path.join(ROOT, '_overlap.html')
open(tmp, 'w', encoding='utf-8').write(page)

art = np.asarray(Image.open(os.path.join(ROOT, 'assets/g_bg.jpg')).convert('RGB')).astype(float)
H, W, _ = art.shape
sat = art.max(2) - art.min(2)
# foliage/stem = anything with real colour or real darkness; the pale blossoms
# and the paper have neither. Deliberately generous - a false alarm is cheap.
mask = (art.sum(2) < 640) | (sat > 34)

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
proc = subprocess.Popen([chrome, "--headless", "--disable-gpu", "--remote-debugging-port=9377",
                         "--remote-allow-origins=*", "--user-data-dir=/tmp/cdp_overlap"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
failures = 0
try:
    tabs = None
    for _ in range(80):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9377/json")); break
        except Exception: time.sleep(.25)
    ws = create_connection([t for t in tabs if t['type'] == 'page'][0]['webSocketDebuggerUrl'], timeout=30)
    n = [0]
    def cmd(m, p=None):
        n[0] += 1
        ws.send(json.dumps({"id": n[0], "method": m, "params": p or {}}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r
    cmd("Emulation.setDeviceMetricsOverride", {"width": 430, "height": 932, "deviceScaleFactor": 2, "mobile": True})
    cmd("Page.enable")
    for lang in LANGS:
        cmd("Page.navigate", {"url": "file://" + tmp + lang}); time.sleep(3.0)
        res = cmd("Runtime.evaluate", {"expression": "JSON.stringify(window.__M())", "returnByValue": True})
        items = json.loads(res["result"]["result"]["value"])
        label = lang or 'he'
        if len(items) < MIN_ELEMENTS:
            print(f'{label:12s} BROKEN - only {len(items)} elements measured'); failures += 1; continue
        bad = []
        for it in items:
            X0, X1 = int(it['x0']/100*W), int(it['x1']/100*W)
            Y0, Y1 = int(it['y0']/100*H), int(it['y1']/100*H)
            box = mask[max(Y0, 0):Y1, max(X0, 0):X1]
            if box.size and box.mean()*100 > 0.5:
                bad.append(f"{it['n']} \"{it['t']}\" OVERLAPS {box.mean()*100:.1f}%")
                continue
            # not colliding is not enough - text touching a leaf looks wrong even
            # when it technically does not intersect. Require real breathing room.
            band = mask[max(Y0, 0):Y1]
            if not band.size: continue
            r = np.where(band[:, min(X1, W-1):].any(0))[0]
            l = np.where(band[:, :max(X0, 1)].any(0))[0]
            gr = r.min()/W*100 if len(r) else 99
            gl = (X0 - l.max())/W*100 if len(l) else 99
            if min(gr, gl) < MIN_GAP:
                side = 'RIGHT' if gr <= gl else 'LEFT'
                bad.append(f"{it['n']} \"{it['t']}\" only {min(gr, gl):.1f}% clear on the {side} "
                           f"(L {gl:.1f}% R {gr:.1f}%)")
        print(f'{label:12s} {"OK" if not bad else "OVERLAP"}  ({len(items)} lines checked)')
        for b in bad: print('    ', b)
        failures += len(bad)
finally:
    proc.terminate(); os.remove(tmp)
sys.exit(1 if failures else 0)
