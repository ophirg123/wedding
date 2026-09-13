#!/bin/bash
# gen_asset.sh <out.png> <prompt>  — transparent PNG asset via gpt-image-2
set -e
OUT="$1"; PROMPT="$2"
KEY=$(nvdesk secrets get IH_API_KEY)
curl -s -X POST https://inference-api.nvidia.com/v1/images/generations \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "$(python3 -c '
import json,sys
print(json.dumps({"model":"openai/openai/gpt-image-2","prompt":sys.argv[1],
"size":"1024x1536","quality":"high","background":"transparent","output_format":"png","n":1}))' "$PROMPT")" \
  -o /tmp/asset_$$.json
python3 - "$OUT" /tmp/asset_$$.json <<'PY'
import sys,json,base64
out,rp=sys.argv[1],sys.argv[2]
d=json.load(open(rp))
if 'data' not in d: print('ERR',str(d)[:400]); sys.exit(1)
open(out,'wb').write(base64.b64decode(d['data'][0]['b64_json'])); print('wrote',out)
PY
rm -f /tmp/asset_$$.json
