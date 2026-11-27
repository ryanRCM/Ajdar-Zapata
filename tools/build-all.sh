#!/usr/bin/env bash
# Rebuilds every menu output from the one list (tools/make-menu.py), in order, and checks them (Ryan, 26 Nov 2026:
# "update it with everything"). Stops at the first failure.
#   bash tools/build-all.sh          # everything, about 10 minutes (the TV pictures take 5)
#   bash tools/build-all.sh --quick  # skip the TV pictures and the TV check (to look at the A4 and panels first)
# Then: publish menu/a4/*.dc.html to Ryan's "Ajdar Zapata A4 Menu" artifact and menu/leaflet/*.dc.html to "Ajdar Zapata Leaflet", send Ryan the PDFs (A4, leaflet, menu/Ajdar_Zapata_TV_Board.pdf),
# commit, push to main (that puts it on the shop TVs), check Netlify, update HANDOFF.md.
set -euo pipefail
cd "$(dirname "$0")/.."
echo '1/7 printed and phone menu';  python3 tools/make-menu.py && node tools/menu-pdf.cjs
rm -f site/menu/page-*.png && pdftoppm -png -r 130 menu/Ajdar_Zapata_Menu.pdf site/menu/page
echo '2/7 TV panels';               python3 tools/make-sections.py && node tools/sections.cjs && python3 tools/make-sections.py layout
echo '3/7 A4 to send out and the leaflet'; python3 tools/a4-menu.py && node tools/a4-pdf.cjs && python3 tools/leaflet.py && node tools/a4-pdf.cjs leaflet
echo '4/7 every output against the list'; python3 tools/menu-check.py
if [ "${1:-}" = "--quick" ]; then echo 'quick: TV pictures and TV check skipped'; exit 0; fi
echo '5/7 TV pictures (5 min)';     node tools/tv-stills.cjs && node tools/board-pdf.cjs
echo '6/7 TV check';                node tools/check.cjs
echo '7/7 done: publish the A4, send the PDFs, commit, push to main, check Netlify, update HANDOFF.md'
