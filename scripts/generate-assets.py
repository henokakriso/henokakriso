#!/usr/bin/env python3
"""Generate the static SVG asset system for the ARWE profile README.

Palette:
  bg      #0A0E14  near-black
  panel   #10151D  charcoal
  line    #1C2430  borders
  text    #E6EDF3  light gray
  dim     #8B98A5  secondary
  accent  #22D3EE  single accent (cyan)

Outputs (relative to this script):
  ../assets/hero/hero.svg              (animated)
  ../assets/hero/hero-animation.svg    (static fallback, same design)
  ../assets/arwe/arwe-core.svg
  ../assets/arwe/architecture.svg      (conceptual, labeled)
  ../assets/arwe/timeline.svg
  ../assets/projects/<slug>.svg        (8 clickable project cards)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")

BG = "#0A0E14"
PANEL = "#10151D"
PANEL2 = "#141B26"
LINE = "#1C2430"
TEXT = "#E6EDF3"
DIM = "#8B98A5"
ACCENT = "#EF4444"

CSS = """
@keyframes flow { to { stroke-dashoffset: -32; } }
@keyframes pulse { 0%,100% { opacity:.15; transform:scale(1);} 50% { opacity:.5; transform:scale(1.35);} }
@keyframes drift { 0% { transform:translateY(0); opacity:0;} 20% { opacity:.8;} 80% { opacity:.8;} 100% { transform:translateY(-46px); opacity:0;} }
@keyframes blink { 0%,100% {opacity:1;} 50% {opacity:.15;} }
.flow { stroke-dasharray:6 10; animation:flow 2.6s linear infinite; }
.node-pulse { animation:pulse 2.4s ease-in-out infinite; transform-origin:center; transform-box:fill-box; }
.particle { animation:drift 7s linear infinite; }
.blink { animation:blink 1.6s steps(1) infinite; }
@media (prefers-reduced-motion: reduce) {
  .flow,.node-pulse,.particle,.blink { animation:none !important; }
}
"""


def grid_pattern(cid, x, y, size):
    return f'''<pattern id="{cid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse" x="{x}" y="{y}">
<path d="M{size} 0H0V{size}" fill="none" stroke="{LINE}" stroke-width="1" opacity=".55"/></pattern>'''


def defs_open(extra=""):
    return f'<defs><style>{CSS}</style>{extra}'


# ---------------------------------------------------------------------------
# PROJECT CARDS
# ---------------------------------------------------------------------------
PROJECTS = [
    dict(num="01", slug="govyx", name="GOVYX", cat="AI GOVERNANCE BRAIN",
         desc=["Government workflow, task monitoring,", "accountability and decision-support", "infrastructure."],
         status="ACTIVE", tech="C · PHP · MySQL", badge="RANKOR INSIDE"),
    dict(num="02", slug="edunex", name="EDUNEX", cat="STUDENT + AI EDUCATION",
         desc=["Education infrastructure spanning", "students, teachers, parents, learning", "resources, assessments and AI tutoring."],
         status="ACTIVE", tech="PHP 8 · MySQL · C", badge=None),
    dict(num="03", slug="locify", name="LOCIFY", cat="DIGITAL KEBELE & IDENTITY",
         desc=["Digital local-government services,", "applications, certificates, document", "requests and digital system IDs."],
         status="ACTIVE", tech="C · PHP · MySQL", badge=None),
    dict(num="04", slug="terrachain", name="TERRACHAIN", cat="LAND + PROCUREMENT",
         desc=["Land and procurement transparency,", "verification, traceability and", "auditability infrastructure."],
         status="ACTIVE", tech="PHP · C · MySQL", badge=None),
    dict(num="05", slug="bilen", name="BILEN", cat="CYBERSECURITY",
         desc=["Defensive cybersecurity and", "threat-monitoring infrastructure for", "digital environments."],
         status="IN DEVELOPMENT", tech="C · PHP", badge=None),
    dict(num="06", slug="kidane", name="KIDANE", cat="AI MICRO-DRONE",
         desc=["Research into intelligent small", "aerial systems, sensing, autonomy", "and robotics."],
         status="IN DEVELOPMENT", tech="C · EMBEDDED", badge=None),
    dict(num="07", slug="ozayn", name="OZAYN", cat="DIGITAL TWIN AI",
         desc=["Long-term digital-twin and", "persistent AI intelligence", "research."],
         status="IN DEVELOPMENT", tech="C · PHP", badge=None),
    dict(num="08", slug="canivox", name="CANIVOX", cat="SMART ROBOTIC DOG",
         desc=["Intelligent robotics platform", "combining sensors, autonomy and", "practical applications."],
         status="IN DEVELOPMENT", tech="C · EMBEDDED", badge=None),
]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def project_card(p):
    W, H = 440, 560
    name = p["name"]
    desc = p["desc"]
    status = p["status"]
    active = status == "ACTIVE"
    sd = "fill:" + (ACCENT if active else "#F59E0B")
    st = "ACTIVE" if active else "IN DEVELOPMENT"
    badge = p["badge"]
    rows = []
    rows.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="{PANEL}"/>')
    rows.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    rows.append(grid_pattern("gp_" + name, 0, 0, 26))
    rows.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="url(#gp_{name})" opacity=".35"/>')
    rows.append(f'<rect x="2" y="{H-6}" width="{W-4}" height="4" rx="2" fill="url(#gb_{name})" opacity=".9"/>')
    rows.append(f'<text x="26" y="52" font-family="monospace" font-size="21" font-weight="700" letter-spacing="2" fill="{TEXT}">{esc(name)}</text>')
    rows.append(f'<text x="{W-34}" y="52" text-anchor="end" font-family="monospace" font-size="14" fill="{DIM}">{p["num"]}</text>')
    rows.append(f'<line x1="26" y1="72" x2="{W-26}" y2="72" stroke="{LINE}" stroke-width="1"/>')
    rows.append(f'<text x="26" y="106" font-family="monospace" font-size="13" font-weight="700" letter-spacing="3" fill="{ACCENT}">{esc(p["cat"])}</text>')
    y = 142
    for ln in desc:
        rows.append(f'<text x="26" y="{y}" font-family="sans-serif" font-size="14.5" fill="{DIM}">{esc(ln)}</text>')
        y += 26
    if badge:
        rows.append(f'<rect x="26" y="{y+2}" width="132" height="22" rx="4" fill="{PANEL2}" stroke="{ACCENT}" stroke-opacity=".35"/>')
        rows.append(f'<text x="92" y="{y+18}" text-anchor="middle" font-family="monospace" font-size="10.5" letter-spacing="2" fill="{ACCENT}">{esc(badge)}</text>')
        y += 46
    y += 10
    rows.append(f'<circle cx="30" cy="{y}" r="4.5" fill="{ACCENT}" opacity="{1 if active else .55}"><animate attributeName="opacity" values="1;.25;1" dur="2.2s" repeatCount="indefinite"/></circle>')
    rows.append(f'<text x="46" y="{y+5}" font-family="monospace" font-size="12" letter-spacing="2" fill="{TEXT}">{esc(st)}</text>')
    rows.append(f'<text x="{W-26}" y="{y+5}" text-anchor="end" font-family="monospace" font-size="12" fill="{DIM}">{esc(p["tech"])}</text>')
    rows.append(f'<line x1="26" y1="{H-96}" x2="{W-26}" y2="{H-96}" stroke="{LINE}" stroke-width="1"/>')
    rows.append(f'<rect x="26" y="{H-80}" width="140" height="3" rx="1.5" fill="{LINE}"/>')
    rows.append(f'<rect x="26" y="{H-80}" width="{94 if active else 62}" height="3" rx="1.5" fill="{ACCENT}"><animate attributeName="opacity" values="1;.4;1" dur="3s" repeatCount="indefinite"/></rect>')
    rows.append(f'<text x="26" y="{H-46}" font-family="monospace" font-size="12.5" letter-spacing="2.5" fill="{ACCENT}">EXPLORE SYSTEM →</text>')
    rows.append(f'<text x="{W-26}" y="{H-46}" text-anchor="end" font-family="monospace" font-size="11" fill="{DIM}">ARWE</text>')
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>{grid_pattern("gb_" + name, 0, 0, 20)}<linearGradient id="gb_{name}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".1"/></linearGradient></defs>
{"".join(rows)}
</svg>'''


# ---------------------------------------------------------------------------
# HERO — animated ecosystem graph
# ---------------------------------------------------------------------------
def hero(animated=True):
    W, H = 860, 540
    nodes = [
        ("EDUNEX", 430, 80, "EDUCATION"),
        ("LOCIFY", 180, 170, "GOVTECH"),
        ("GOVYX", 680, 170, "GOVERNMENT"),
        ("TERRACHAIN", 430, 330, "TRANSPARENCY"),
        ("BILEN", 230, 430, "SECURITY"),
        ("KIDANE", 630, 430, "ROBOTICS"),
        ("OZAYN", 350, 505, "INTELLIGENCE"),
        ("CANIVOX", 510, 505, "AUTONOMY"),
    ]
    edges = [("LOCIFY", "ARWE"), ("GOVYX", "ARWE"), ("EDUNEX", "ARWE"),
             ("TERRACHAIN", "ARWE"), ("BILEN", "TERRACHAIN"), ("KIDANE", "TERRACHAIN"),
             ("OZAYN", "BILEN"), ("CANIVOX", "KIDANE")]
    pos = {n: (x, y) for n, x, y, _ in nodes}
    pos["ARWE"] = (430, 235)
    r = []
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="{PANEL}"/>')
    r.append(grid_pattern("hero_grid", 0, 0, 30))
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="url(#hero_grid)" opacity=".4"/>')
    for a, b in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        r.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACCENT}" stroke-opacity=".28" stroke-width="1.5" class="flow"/>')
    for i in range(6):
        px = 60 + i * 150
        py = 60 + (i % 3) * 40
        if animated:
            anim = f'<animate attributeName="opacity" values="0;.7;0" dur="{5 + i}s" begin="{i}s" repeatCount="indefinite"/>'
            r.append(f'<circle cx="{px}" cy="{py}" r="1.6" fill="{ACCENT}">{anim}</circle>')
        else:
            r.append(f'<circle cx="{px}" cy="{py}" r="1.6" fill="{ACCENT}" opacity=".5"/>')
    for n, x, y, tag in nodes:
        label = n if n in ("GOVYX", "OZAYN") else n.title()
        r.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{BG}" stroke="{ACCENT}" stroke-width="1.5" class="node-pulse"/>')
        r.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{ACCENT}"/>')
        r.append(f'<text x="{x}" y="{y+42}" text-anchor="middle" font-family="monospace" font-size="12.5" font-weight="700" letter-spacing="2" fill="{TEXT}">{label}</text>')
        r.append(f'<text x="{x}" y="{y+58}" text-anchor="middle" font-family="monospace" font-size="9" letter-spacing="1.5" fill="{DIM}">{tag}</text>')
    ax, ay = pos["ARWE"]
    r.append(f'<circle cx="{ax}" cy="{ay}" r="34" fill="none" stroke="{ACCENT}" stroke-opacity=".25" stroke-width="1" class="node-pulse"/>')
    r.append(f'<circle cx="{ax}" cy="{ay}" r="22" fill="{ACCENT}" fill-opacity=".08" stroke="{ACCENT}" stroke-width="2"/>')
    r.append(f'<text x="{ax}" y="{ay+6}" text-anchor="middle" font-family="monospace" font-size="15" font-weight="700" letter-spacing="3" fill="{ACCENT}">ARWE</text>')
    r.append(f'<text x="430" y="{H-14}" text-anchor="middle" font-family="monospace" font-size="9.5" letter-spacing="2" fill="{DIM}">PROJECT ARWE — CONNECTED SYSTEM ECOSYSTEM</text>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs_open()}</defs>{"".join(r)}</svg>'


# ---------------------------------------------------------------------------
# ARWE core mark
# ---------------------------------------------------------------------------
def arwe_core():
    return '''<svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
<rect x="2" y="2" width="116" height="116" rx="24" fill="#10151D" stroke="#1C2430"/>
<circle cx="60" cy="60" r="42" fill="none" stroke="#22D3EE" stroke-opacity=".3" stroke-width="1"/>
<circle cx="60" cy="60" r="26" fill="#22D3EE" fill-opacity=".08" stroke="#22D3EE" stroke-width="2"/>
<text x="60" y="66" text-anchor="middle" font-family="monospace" font-size="17" font-weight="700" letter-spacing="3" fill="#22D3EE">ARWE</text>
</svg>'''


# ---------------------------------------------------------------------------
# ARCHITECTURE — conceptual ecosystem vision
# ---------------------------------------------------------------------------
def architecture():
    W, H = 760, 600
    r = []
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="{PANEL}"/>')
    r.append(grid_pattern("arc_grid", 0, 0, 30))
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="url(#arc_grid)" opacity=".35"/>')
    r.append(f'<text x="{W/2}" y="40" text-anchor="middle" font-family="monospace" font-size="15" font-weight="700" letter-spacing="4" fill="{TEXT}">PROJECT ARWE</text>')
    r.append(f'<text x="{W/2}" y="60" text-anchor="middle" font-family="monospace" font-size="10" letter-spacing="2" fill="{DIM}">ECOSYSTEM VISION — CONCEPTUAL ARCHITECTURE</text>')
    ax, ay = W / 2, 130
    r.append(f'<circle cx="{ax}" cy="{ay}" r="20" fill="{ACCENT}" fill-opacity=".1" stroke="{ACCENT}" stroke-width="2"/>')
    r.append(f'<text x="{ax}" y="{ay+6}" text-anchor="middle" font-family="monospace" font-size="13" font-weight="700" letter-spacing="2" fill="{ACCENT}">ARWE</text>')
    domains = [
        ("EDUCATION", ["EDUNEX", "LOCIFY"], 120),
        ("GOVERNMENT", ["GOVYX", "TERRACHAIN"], 320),
        ("SECURITY", ["BILEN"], 520),
        ("INTELLIGENCE", ["OZAYN"], 120),
        ("TRANSPARENCY", ["BILEN", "TERRACHAIN"], 320),
        ("AUTONOMY", ["KIDANE", "CANIVOX"], 520),
    ]
    for i, (dom, kids, cx) in enumerate(domains):
        dy = 260 + (i % 3) * 120
        r.append(f'<line x1="{ax}" y1="{ay}" x2="{cx}" y2="{dy-34}" stroke="{ACCENT}" stroke-opacity=".3" stroke-width="1.5" class="flow"/>')
        r.append(f'<text x="{cx}" y="{dy-62}" text-anchor="middle" font-family="monospace" font-size="11" font-weight="700" letter-spacing="3" fill="{ACCENT}">{dom}</text>')
        r.append(f'<rect x="{cx-92}" y="{dy-46}" width="184" height="40" rx="8" fill="{PANEL2}" stroke="{LINE}"/>')
        r.append(f'<text x="{cx}" y="{dy-19}" text-anchor="middle" font-family="monospace" font-size="12" letter-spacing="2" fill="{TEXT}">{dom}</text>')
        ky = dy + 30
        for k in kids:
            r.append(f'<circle cx="{cx}" cy="{ky}" r="4" fill="{ACCENT}" opacity=".9"/>')
            r.append(f'<text x="{cx+14}" y="{ky+5}" font-family="monospace" font-size="12.5" fill="{TEXT}">{k}</text>')
            ky += 26
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs_open()}</defs>{"".join(r)}</svg>'


# ---------------------------------------------------------------------------
# TIMELINE 2025 → 2028
# ---------------------------------------------------------------------------
def timeline():
    W, H = 760, 230
    phases = [
        (140, "2025", "FOUNDATION", ["EDUNEX", "LOCIFY"]),
        (330, "2026", "GOVERNMENT", ["GOVYX", "TERRACHAIN", "BILEN"]),
        (520, "2027", "INTELLIGENCE", ["OZAYN", "CANIVOX", "KIDANE"]),
        (710, "2028", "INTEGRATION", ["ARWE ECOSYSTEM"]),
    ]
    r = []
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="{PANEL}"/>')
    r.append(grid_pattern("tl_grid", 0, 0, 30))
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="url(#tl_grid)" opacity=".3"/>')
    r.append(f'<text x="{W/2}" y="36" text-anchor="middle" font-family="monospace" font-size="14" font-weight="700" letter-spacing="4" fill="{TEXT}">ARWE TIMELINE — 2025 → 2028</text>')
    r.append(f'<line x1="140" y1="110" x2="710" y2="110" stroke="{ACCENT}" stroke-opacity=".4" stroke-width="2" class="flow"/>')
    for cx, year, phase, kids in phases:
        r.append(f'<circle cx="{cx}" cy="110" r="8" fill="{BG}" stroke="{ACCENT}" stroke-width="2"/>')
        r.append(f'<circle cx="{cx}" cy="110" r="3.5" fill="{ACCENT}"/>')
        r.append(f'<text x="{cx}" y="80" text-anchor="middle" font-family="monospace" font-size="15" font-weight="700" fill="{TEXT}">{year}</text>')
        r.append(f'<text x="{cx}" y="140" text-anchor="middle" font-family="monospace" font-size="11" font-weight="700" letter-spacing="3" fill="{ACCENT}">{phase}</text>')
        ktext = "  ·  ".join(kids)
        r.append(f'<text x="{cx}" y="164" text-anchor="middle" font-family="monospace" font-size="10.5" fill="{DIM}">{ktext}</text>')
    r.append(f'<text x="{W/2}" y="206" text-anchor="middle" font-family="monospace" font-size="9.5" letter-spacing="2" fill="{DIM}">MULTI-YEAR TECHNOLOGY ECOSYSTEM FOR DIGITAL ETHIOPIA</text>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{defs_open()}</defs>{"".join(r)}</svg>'


def main():
    os.makedirs(os.path.join(OUT, "hero"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "arwe"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)
    with open(os.path.join(OUT, "hero", "hero.svg"), "w") as f:
        f.write(hero(animated=True))
    with open(os.path.join(OUT, "hero", "hero-animation.svg"), "w") as f:
        f.write(hero(animated=False))
    with open(os.path.join(OUT, "arwe", "arwe-core.svg"), "w") as f:
        f.write(arwe_core())
    with open(os.path.join(OUT, "arwe", "architecture.svg"), "w") as f:
        f.write(architecture())
    with open(os.path.join(OUT, "arwe", "timeline.svg"), "w") as f:
        f.write(timeline())
    for p in PROJECTS:
        with open(os.path.join(OUT, "projects", p["slug"] + ".svg"), "w") as f:
            f.write(project_card(p))
    print("generated:", len(PROJECTS) + 5, "SVG assets")


if __name__ == "__main__":
    main()
