#!/bin/bash
# closing-desk — a bundle folder, opened in AppPlayer. Prerequisites: tools/appplayer.py header.
set -euo pipefail
cd "$(dirname "$0")"
echo "   [1/2] bundle is a folder of json"
python3 - <<'PY'
import json, os
b = "closing_desk.mbd"
app = json.load(open(f"{b}/ui/app.json"))
for route, uri in app["routes"].items():
    name = uri.rsplit("/", 1)[-1]
    json.load(open(f"{b}/ui/pages/{name}.json"))
print(f"   {len(app['routes'])} route(s), all resolve and parse")
PY
echo "   [2/2] open in AppPlayer, drive it, capture"
rm -f captures/*.png
python3 verify.py
COUNT=$(ls captures/*.png | wc -l | tr -d ' ')
[ "$COUNT" -eq 4 ] || { echo "   expected 4 captures, got $COUNT"; exit 1; }
