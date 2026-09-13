#!/bin/bash
# gen.sh <out.png> <prompt> [imgs...]
set -e
OUT="$1"; shift
PROMPT="$1"; shift
KEY=$(nvdesk secrets get IH_API_KEY)
ARGS=()
for i in "$@"; do ARGS+=(-F "image[]=@$i"); done
curl -s https://inference-api.nvidia.com/v1/images/edits \
  -H "Authorization: Bearer $KEY" \
  -F model="gcp/google/gemini-3-pro-image" \
  "${ARGS[@]}" \
  -F prompt="$PROMPT" \
  -F n=1 -o /tmp/resp_$$.json
python3 - "$OUT" /tmp/resp_$$.json <<'PY'
import sys,json,base64
out,resp=sys.argv[1],sys.argv[2]
d=json.load(open(resp))
if 'data' not in d: print('ERR',str(d)[:500]); sys.exit(1)
open(out,'wb').write(base64.b64decode(d['data'][0]['b64_json']))
print('wrote',out)
PY
rm -f /tmp/resp_$$.json
