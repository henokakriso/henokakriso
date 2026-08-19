#!/usr/bin/env python3
"""Generate the compact animated SVG tiles for the ARWE profile README.

Palette:
  bg      #0A0E14  near-black
  panel   #10151D  charcoal
  line    #1C2430  borders
  text    #E6EDF3  light gray
  dim     #8B98A5  secondary
  accent  #EF4444  red (single accent)

Outputs (relative to this script):
  ../assets/projects/<slug>.svg   — 8 compact animated tiles (240 x 300)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "projects")

BG = "#0A0E14"
PANEL = "#10151D"
PANEL2 = "#141B26"
LINE = "#1C2430"
TEXT = "#E6EDF3"
DIM = "#8B98A5"
ACCENT = "#EF4444"

CSS = """
@keyframes blink { 0%,100% {opacity:1;} 50% {opacity:.15;} }
@media (prefers-reduced-motion: reduce) {
  * { animation:none !important; }
}
"""

PROJECTS = [
    dict(num="01", slug="govyx", name="GOVYX", cat="AI GOVERNANCE", status="ACTIVE"),
    dict(num="02", slug="edunex", name="EDUNEX", cat="AI EDUCATION", status="ACTIVE"),
    dict(num="03", slug="locify", name="LOCIFY", cat="DIGITAL KEBELE", status="ACTIVE"),
    dict(num="04", slug="terrachain", name="TERRACHAIN", cat="TRANSPARENCY", status="ACTIVE"),
    dict(num="05", slug="bilen", name="BILEN", cat="CYBERSECURITY", status="IN DEVELOPMENT"),
    dict(num="06", slug="kidane", name="KIDANE", cat="AI MICRO-DRONE", status="IN DEVELOPMENT"),
    dict(num="07", slug="ozayn", name="OZAYN", cat="DIGITAL TWIN", status="IN DEVELOPMENT"),
    dict(num="08", slug="canivox", name="CANIVOX", cat="ROBOTICS", status="IN DEVELOPMENT"),
]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tile(p, W=240, H=300):
    name = p["name"]
    r = []
    r.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="{PANEL}"/>')
    r.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    r.append(f'<pattern id="tp_{name}" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="{LINE}" stroke-width="1" opacity=".55"/></pattern>')
    r.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#tp_{name})" opacity=".3"/>')
    r.append(f'<rect x="2" y="{H-6}" width="{W-4}" height="4" rx="2" fill="url(#tb_{name})" opacity=".9"/>')
    r.append(f'<text x="18" y="38" font-family="monospace" font-size="16" font-weight="700" letter-spacing="2" fill="{TEXT}">{esc(name)}</text>')
    r.append(f'<text x="{W-20}" y="38" text-anchor="end" font-family="monospace" font-size="11" fill="{DIM}">{p["num"]}</text>')
    r.append(f'<line x1="18" y1="54" x2="{W-18}" y2="54" stroke="{LINE}" stroke-width="1"/>')
    r.append(f'<text x="18" y="82" font-family="monospace" font-size="10" font-weight="700" letter-spacing="2.5" fill="{ACCENT}">{esc(p["cat"])}</text>')
    r.append(f'<circle cx="22" cy="114" r="4" fill="{ACCENT}"/>')
    r.append(f'<circle cx="22" cy="114" r="9" fill="none" stroke="{ACCENT}" stroke-opacity=".4"><animate attributeName="r" values="6;12;6" dur="1.8s" repeatCount="indefinite"/></circle>')
    r.append(f'<text x="36" y="119" font-family="monospace" font-size="10" letter-spacing="2" fill="{TEXT}">{esc(p["status"])}</text>')
    r.append(f'<text x="18" y="{H-58}" font-family="monospace" font-size="11" letter-spacing="2" fill="{ACCENT}">EXPLORE →</text>')
    r.append(f'<rect x="18" y="{H-42}" width="{W-36}" height="3" rx="1.5" fill="{LINE}"/>')
    r.append(f'<rect x="18" y="{H-42}" width="{(W-36) * 3 // 5}" height="3" rx="1.5" fill="{ACCENT}"><animate attributeName="opacity" values="1;.3;1" dur="2.4s" repeatCount="indefinite"/></rect>')
    r.append(f'<text x="18" y="{H-20}" font-family="monospace" font-size="9" letter-spacing="1.5" fill="{DIM}">ARWE-PSL</text>')
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><style>{CSS}</style>'
            f'<linearGradient id="tb_{name}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".06"/></linearGradient></defs>'
            + "".join(r) + "</svg>")


def main():
    os.makedirs(OUT, exist_ok=True)
    for p in PROJECTS:
        with open(os.path.join(OUT, p["slug"] + ".svg"), "w") as f:
            f.write(tile(p))
    print("generated", len(PROJECTS), "compact tiles")


if __name__ == "__main__":
    main()