#!/usr/bin/env python3
ACCENT = "#EF4444"; TEXT = "#E6EDF3"; DIM = "#8B98A5"; BG = "#10151D"; LINE = "#1C2430"
W, H = 860, 480
nodes = [("EDUNEX", 430, 70), ("LOCIFY", 170, 150), ("GOVYX", 690, 150), ("TERRACHAIN", 430, 300),
         ("BILEN", 220, 380), ("KIDANE", 640, 380), ("OZAYN", 300, 428), ("CANIVOX", 560, 428)]
edges = [("LOCIFY", "ARWE"), ("GOVYX", "ARWE"), ("EDUNEX", "ARWE"), ("TERRACHAIN", "ARWE"),
         ("BILEN", "TERRACHAIN"), ("KIDANE", "TERRACHAIN"), ("OZAYN", "BILEN"), ("CANIVOX", "KIDANE")]
pos = dict(nodes); pos["ARWE"] = (430, 225)
r = [f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>',
     f'<pattern id="ng" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{LINE}" stroke-width="1" opacity=".55"/></pattern>',
     f'<rect width="{W}" height="{H}" rx="18" fill="url(#ng)" opacity=".35"/>',
     f'<text x="{W/2}" y="38" text-anchor="middle" font-family="monospace" font-size="14" font-weight="700" letter-spacing="4" fill="{TEXT}">PROJECT ARWE — SYSTEM NETWORK</text>']
for a, b in edges:
    x1, y1 = pos[a]; x2, y2 = pos[b]
    r.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACCENT}" stroke-opacity=".3" stroke-width="1.5" stroke-dasharray="6 10"><animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.6s" repeatCount="indefinite"/></line>')
for i in range(6):
    r.append(f'<circle cx="{60+i*150}" cy="{60+(i%3)*46}" r="1.6" fill="{ACCENT}"><animate attributeName="opacity" values="0;.7;0" dur="{5+i}s" begin="{i}s" repeatCount="indefinite"/></circle>')
for name, x, y in nodes:
    r.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{BG}" stroke="{ACCENT}" stroke-width="1.5"/>')
    r.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{ACCENT}"/>')
    r.append(f'<circle cx="{x}" cy="{y}" r="10" fill="none" stroke="{ACCENT}" stroke-opacity=".5"><animate attributeName="r" values="8;16;8" dur="2.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".5;0;.5" dur="2.2s" repeatCount="indefinite"/></circle>')
    r.append(f'<text x="{x}" y="{y+34}" text-anchor="middle" font-family="monospace" font-size="12" font-weight="700" letter-spacing="2" fill="{TEXT}">{name}</text>')
ax, ay = pos["ARWE"]
r.append(f'<circle cx="{ax}" cy="{ay}" r="30" fill="none" stroke="{ACCENT}" stroke-opacity=".25"><animate attributeName="r" values="24;40;24" dur="2.6s" repeatCount="indefinite"/></circle>')
r.append(f'<circle cx="{ax}" cy="{ay}" r="20" fill="{ACCENT}" fill-opacity=".1" stroke="{ACCENT}" stroke-width="2"/>')
r.append(f'<text x="{ax}" y="{ay+6}" text-anchor="middle" font-family="monospace" font-size="14" font-weight="700" letter-spacing="3" fill="{ACCENT}">ARWE</text>')
r.append(f'<text x="{W/2}" y="{H-26}" text-anchor="middle" font-family="monospace" font-size="10" letter-spacing="2" fill="{DIM}">CLICK A NODE'S PROJECT TO OPEN ITS REPOSITORY — COMING IN THE CARD GRID BELOW</text>')
svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
       f'<style>@media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} }}</style>' + "".join(r) + "</svg>")
open('assets/arwe/network.svg', 'w').write(svg)
print("network.svg written")
