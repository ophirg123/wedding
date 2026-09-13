"""Capture a scrolling clip of the page -> frames, for reviewing motion."""
import json,subprocess,time,base64,urllib.request,sys,os
from websocket import create_connection
url,outdir,y0,y1,n = sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
os.makedirs(outdir,exist_ok=True)
p=subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","--headless","--disable-gpu",
  "--remote-debugging-port=9334","--remote-allow-origins=*","--user-data-dir=/tmp/cdpprof5","--window-size=900,1000"],
  stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try: tabs=json.load(urllib.request.urlopen("http://127.0.0.1:9334/json")); break
        except Exception: time.sleep(.25)
    ws=create_connection([t for t in tabs if t['type']=='page'][0]['webSocketDebuggerUrl'],timeout=30); i=[0]
    def cmd(m,pr=None):
        i[0]+=1; ws.send(json.dumps({"id":i[0],"method":m,"params":pr or {}}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==i[0]: return r
    cmd("Emulation.setDeviceMetricsOverride",{"width":430,"height":932,"deviceScaleFactor":1,"mobile":True})
    cmd("Page.enable"); cmd("Page.navigate",{"url":url}); time.sleep(3)
    for k in range(n):
        y=y0+(y1-y0)*k/max(1,n-1)
        cmd("Runtime.evaluate",{"expression":f"scrollTo(0,{y})"}); time.sleep(.25)
        r=cmd("Page.captureScreenshot",{"format":"png"})
        open(f"{outdir}/f{k:03d}.png","wb").write(base64.b64decode(r["result"]["data"]))
    print("frames:",n)
finally: p.terminate()
