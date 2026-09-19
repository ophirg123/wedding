#!/usr/bin/env python
"""Rotate only the yellow-green foliage hues toward green. Gold and paper untouched."""
import sys
from PIL import Image
import numpy as np
def shift(arr, deg):
    r,g,b=arr[...,0],arr[...,1],arr[...,2]
    mx=arr.max(2); mn=arr.min(2); d=mx-mn+1e-9
    hue=np.zeros_like(mx)
    hue=np.where(mx==r,((g-b)/d)%6,hue); hue=np.where(mx==g,(b-r)/d+2,hue); hue=np.where(mx==b,(r-g)/d+4,hue)
    hue*=60
    s=np.where(mx>0,d/(mx+1e-9),0); v=mx
    sel=((hue>50)&(hue<110)&(s>0.25)).astype(np.float32)
    k=np.clip((s-0.25)/0.35,0,1)*sel
    hue2=(hue+deg*k)%360
    c=v*s; x=c*(1-abs((hue2/60)%2-1)); mm=v-c
    z=np.zeros_like(c)
    conds=[hue2<60,(hue2>=60)&(hue2<120),(hue2>=120)&(hue2<180),(hue2>=180)&(hue2<240),(hue2>=240)&(hue2<300),hue2>=300]
    parts=[(c,x,z),(x,c,z),(z,c,x),(z,x,c),(x,z,c),(c,z,x)]
    out=np.zeros_like(arr)
    for cnd,(rr,gg,bb) in zip(conds,parts):
        out[...,0]=np.where(cnd,rr,out[...,0]); out[...,1]=np.where(cnd,gg,out[...,1]); out[...,2]=np.where(cnd,bb,out[...,2])
    return np.clip(out+mm[...,None],0,1)
src, dst, deg = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(src)
alpha = im.split()[3] if im.mode in ('RGBA','LA') or 'transparency' in im.info else None
a = np.asarray(im.convert('RGB')).astype(np.float32)/255.0
o = Image.fromarray((shift(a, deg)*255).astype('uint8'))
if alpha is not None: o.putalpha(alpha)
o.save(dst)
print('wrote', dst)
