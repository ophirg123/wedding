#!/usr/bin/env python
"""Report hero text that collides with the background artwork."""
import subprocess, sys, os
from PIL import Image
import numpy as np
LANGS = ['', '?lang=dati', '?lang=nl']
src = open('index.html', encoding='utf-8').read()
t = src.replace("</style>", "  .fade-up{opacity:1!important;transform:none!important;filter:none!important}\n</style>", 1)
t = t.replace("</body>", """<script>setTimeout(()=>{const h=document.querySelector('.hero').getBoundingClientRect();
const els=[...document.querySelectorAll('.hero-text .invite1,.hero-text .invite2,.hero-text .names,.hero-text .date,.hero-text .hebdate,.hero-text .venue,.hero-text .reception,.hero-text .parent-names,.hero-text .parent-label,.hero-text .seeyou,.hero-text .aye,.hero-text .pasuk')];
const o=els.filter(e=>e.offsetParent).map(e=>{const r=document.createRange();r.selectNodeContents(e);const c=r.getBoundingClientRect();
return [e.className.split(' ')[0],((c.left-h.left)/h.width*100).toFixed(1),((c.right-h.left)/h.width*100).toFixed(1),((c.top-h.top)/h.height*100).toFixed(1),((c.bottom-h.top)/h.height*100).toFixed(1)].join(',')});
document.title=o.join(' | ');},700);</script></body>""")
open('_w.html', 'w', encoding='utf-8').write(t)
a = np.asarray(Image.open('assets/g_bg.jpg').convert('RGB')).astype(float)
H, W, _ = a.shape
g = a[:, :, 1] - a[:, :, 2]
leaf = (a.sum(2) < 560) & (g > -4)          # foliage only, not the pale gold arc
fail = 0
for L in LANGS:
    out = subprocess.run(['tools/.venv/bin/python', '/tmp/wcheck.py',
                          'file://' + os.getcwd() + '/_w.html' + L, '430'],
                         capture_output=True, text=True).stdout
    line = out.split('::')[-1].strip()
    bad = []
    for part in line.split('|'):
        p = [x.strip() for x in part.split(',')]
        if len(p) != 5: continue
        n, x0, x1, y0, y1 = p
        X0, X1 = int(float(x0)/100*W), int(float(x1)/100*W)
        Y0, Y1 = int(float(y0)/100*H), int(float(y1)/100*H)
        box = leaf[max(Y0,0):Y1, max(X0,0):X1]
        if box.size and box.mean()*100 > 0.5:
            bad.append(f'{n} {box.mean()*100:.2f}% (x {x0}-{x1})')
    print(f'{L or "he":12s} {"OK" if not bad else "OVERLAP"}')
    for b in bad: print('   ', b); fail += 1
os.remove('_w.html')
sys.exit(1 if fail else 0)
