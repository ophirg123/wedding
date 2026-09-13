#!/usr/bin/env python
"""Phone-accurate screenshot via CDP. macOS Chrome enforces a ~500px min window,
so --window-size lies; only Emulation.setDeviceMetricsOverride gives a true 430px viewport.
Usage: shot.py <url> <out.png> [W] [H] [full]   env SCROLLY=<px> to scroll first."""
import os
import json,subprocess,time,base64,urllib.request,sys,os
from websocket import create_connection
url,out = sys.argv[1],sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv)>3 else 430
H = int(sys.argv[4]) if len(sys.argv)>4 else 932
full = len(sys.argv)>5 and sys.argv[5]=='full'
p=subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","--headless","--disable-gpu",
    "--remote-debugging-port=9333","--remote-allow-origins=*","--user-data-dir=/tmp/cdpprof","--window-size=900,1000"],
    stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try: tabs=json.load(urllib.request.urlopen("http://127.0.0.1:9333/json")); break
        except Exception: time.sleep(.25)
    ws=create_connection([t for t in tabs if t['type']=='page'][0]['webSocketDebuggerUrl'],timeout=30); i=[0]
    def cmd(m,pr=None):
        i[0]+=1; ws.send(json.dumps({"id":i[0],"method":m,"params":pr or {}}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==i[0]: return r
    cmd("Emulation.setDeviceMetricsOverride",{"width":W,"height":H,"deviceScaleFactor":float(os.environ.get("DPR","2")),"mobile":True})
    cmd("Page.enable"); cmd("Page.navigate",{"url":url}); time.sleep(float(os.environ.get("WAIT","3.0")))
    sy=os.environ.get("SCROLLY")
    if sy: cmd("Runtime.evaluate",{"expression":f"scrollTo(0,{sy})"}); time.sleep(1.5)
    r=cmd("Page.captureScreenshot",{"format":"png","captureBeyondViewport":full})
    open(out,"wb").write(base64.b64decode(r["result"]["data"]))
    print("saved",out)
finally: p.terminate()
