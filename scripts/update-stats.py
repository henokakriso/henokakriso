#!/usr/bin/env python3
"""Fetch real GitHub public data and render the live-status SVGs.

Outputs (committed to the repo, refreshed by .github/workflows/live-stats.yml):
  assets/github/system-status.svg   — command-center panel
  assets/github/activity.svg        — recent-activity heatmap (public events)

Uses only PUBLIC GitHub API endpoints (no token required; uses GITHUB_TOKEN
automatically when running inside GitHub Actions to raise the rate limit).
If the API is unreachable, writes a graceful "SYNC PENDING" fallback instead of
failing the build.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

USER = "henokakriso"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "github")

ACCENT = "#EF4444"
TEXT = "#E6EDF3"
DIM = "#8B98A5"
BG = "#10151D"
LINE = "#1C2430"


def api(path):
    req = urllib.request.Request("https://api.github.com" + path,
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "arwe-profile-stats"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fetch():
    user = api(f"/users/{USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed")
    events = []
    try:
        for page in (1, 2):
            ev = api(f"/users/{USER}/events/public?per_page=100&page={page}")
            events += ev
            if len(ev) < 100:
                break
    except Exception:
        pass
    return user, repos, events


def render_status(user, repos, events):
    W, H = 760, 360
    stars = sum(r["stargazers_count"] for r in repos)
    forks = sum(r["forks_count"] for r in repos)
    followers = user.get("followers", 0)
    n_repos = user.get("public_repos", len(repos))
    last = ""
    if events and events[0].get("created_at"):
        t = dt.datetime.fromisoformat(events[0]["created_at"].replace("Z", "+00:00"))
        last = t.strftime("%Y-%m-%d %H:%M UTC")
    synced = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    recent = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)

    heat = {}
    maxh = 1
    for e in events:
        created = e.get("created_at")
        if not created:
            continue
        d = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
        if d < recent:
            continue
        key = d.date()
        heat[key] = heat.get(key, 0) + 1
        maxh = max(maxh, heat[key])

    r = []
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="{BG}"/>')
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="none" stroke="{LINE}"/>')
    r.append(f'<text x="30" y="42" font-family="monospace" font-size="16" font-weight="700" letter-spacing="3" fill="{TEXT}">GITHUB // SYSTEM STATUS</text>')
    r.append(f'<circle cx="{W-36}" cy="36" r="5" fill="{ACCENT}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    r.append(f'<text x="{W-30}" y="40" text-anchor="end" font-family="monospace" font-size="10" fill="{ACCENT}">LIVE</text>')

    items = [("REPOSITORIES", n_repos), ("FOLLOWERS", followers), ("STARS", stars), ("FORKS", forks)]
    mx = max(max(v for _, v in items), 1)
    y = 78
    for label, val in items:
        bar = min(int(val / mx * 260), 260)
        r.append(f'<text x="30" y="{y}" font-family="monospace" font-size="11" letter-spacing="2" fill="{DIM}">{label}</text>')
        r.append(f'<text x="320" y="{y}" font-family="monospace" font-size="12" font-weight="700" fill="{TEXT}">{val}</text>')
        r.append(f'<rect x="30" y="{y+8}" width="280" height="6" rx="3" fill="{LINE}"/>')
        r.append(f'<rect x="30" y="{y+8}" width="{max(bar,2)}" height="6" rx="3" fill="{ACCENT}"><animate attributeName="opacity" values="1;.5;1" dur="2.8s" repeatCount="indefinite"/></rect>')
        y += 44
    r.append(f'<text x="30" y="{y+14}" font-family="monospace" font-size="11" letter-spacing="2" fill="{DIM}">LAST ACTIVITY</text>')
    r.append(f'<text x="320" y="{y+14}" font-family="monospace" font-size="12" fill="{TEXT}">{last or "—"}</text>')
    r.append(f'<text x="30" y="{y+40}" font-family="monospace" font-size="11" letter-spacing="2" fill="{DIM}">SYNC</text>')
    r.append(f'<text x="320" y="{y+40}" font-family="monospace" font-size="12" fill="{TEXT}">WEEKLY · {synced}</text>')
    r.append(f'<text x="{W/2}" y="{H-16}" text-anchor="middle" font-family="monospace" font-size="9.5" letter-spacing="2" fill="{DIM}">DATA: GITHUB PUBLIC API · NO TOKENS EXPOSED · LAST 90 DAYS ACTIVITY</text>')

    hx, hy = 30, y + 84
    W2, H2 = W - 60, H - hy - 30
    weeks = 10
    cw, ch = W2 / 10 - 6, (H2 - 20) / 7 - 6
    if cw > 26:
        cw = 26
        ch = 14
    today = dt.date.today()
    start = today - dt.timedelta(weeks=weeks - 1, days=6)
    r.append(f'<text x="30" y="{hy-12}" font-family="monospace" font-size="10.5" letter-spacing="2.5" fill="{ACCENT}">BUILD ACTIVITY — LAST {weeks} WEEKS · PUBLIC EVENTS</text>')
    d = start
    for week in range(weeks):
        for day in range(7):
            cnt = heat.get(d, 0)
            a = 0.12 if cnt == 0 else 0.25 + 0.65 * (cnt / maxh)
            x = 30 + week * (cw + 6)
            yy = hy + day * (ch + 6)
            r.append(f'<rect x="{x}" y="{yy}" width="{cw}" height="{ch}" rx="3" fill="{ACCENT}" fill-opacity="{a:.2f}"/>')
            d += dt.timedelta(days=1)
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{BG}"/>' + "".join(r) + "</svg>", heat


def render_activity(events):
    W, H = 760, 300
    recent = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)
    heat = {}
    maxh = 1
    for e in events:
        created = e.get("created_at")
        if not created:
            continue
        d = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
        if d < recent:
            continue
        key = d.date()
        heat[key] = heat.get(key, 0) + 1
        maxh = max(maxh, heat[key])
    r = []
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="{BG}"/>')
    r.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="none" stroke="{LINE}"/>')
    r.append(f'<text x="30" y="42" font-family="monospace" font-size="16" font-weight="700" letter-spacing="3" fill="{TEXT}">BUILD LOG</text>')
    r.append(f'<text x="30" y="66" font-family="monospace" font-size="10.5" letter-spacing="2.5" fill="{DIM}">REAL ACTIVITY FROM GITHUB — LAST 90 DAYS · PUBLIC EVENTS</text>')
    weeks = 13
    cw = (W - 72) / 13 - 5
    ch = 16
    today = dt.date.today()
    start = today - dt.timedelta(weeks=weeks - 1, days=6)
    d = start
    for i, wd in enumerate(["M", "T", "W", "T", "F", "S", "S"]):
        r.append(f'<text x="{30 + i * (cw + 5) - 4}" y="88" font-family="monospace" font-size="9" fill="{DIM}">{wd}</text>')
    d = start
    for week in range(weeks):
        for day in range(7):
            cnt = heat.get(d, 0)
            a = 0.1 if cnt == 0 else 0.25 + 0.65 * (cnt / maxh)
            x = 30 + week * (cw + 5)
            yy = 100 + day * (ch + 7)
            r.append(f'<rect x="{x}" y="{yy}" width="{cw}" height="{ch}" rx="3.5" fill="{ACCENT}" fill-opacity="{a:.2f}"/>')
            d += dt.timedelta(days=1)
    r.append(f'<text x="30" y="{H-24}" font-family="monospace" font-size="9.5" letter-spacing="2" fill="{DIM}">SOURCE: PUBLIC EVENTS API · AUTO-REFRESHED WEEKLY BY GITHUB ACTIONS</text>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{BG}"/>' + "".join(r) + "</svg>"



def fetch_contrib():
    import json as _j
    req = urllib.request.Request(
        "https://github-contributions-api.jogruber.de/v4/" + USER,
        headers={"User-Agent": "arwe-profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return _j.loads(resp.read().decode())


def render_contrib(data):
    days = data["contributions"]
    total = sum(d["count"] for d in days)
    acc, text, dim, bg, line = "#EF4444", "#E6EDF3", "#8B98A5", "#10151D", "#1C2430"
    W, H = 900, 210
    heat = {d["date"]: d["count"] for d in days}
    maxc = max(heat.values()) or 1
    import datetime as _dt
    r = [f'<rect width="{W}" height="{H}" rx="18" fill="{bg}"/>',
         f'<rect width="{W}" height="{H}" rx="18" fill="none" stroke="{line}"/>',
         f'<text x="30" y="42" font-family="monospace" font-size="13" letter-spacing="3" fill="{dim}">CONTRIBUTIONS - LAST YEAR</text>',
         f'<text x="{W-30}" y="40" text-anchor="end" font-family="monospace" font-size="15" font-weight="700" fill="{acc}">{total} TOTAL</text>']
    d0 = _dt.date.fromisoformat(days[0]["date"])
    start = d0 - _dt.timedelta(days=d0.weekday())
    cw = (W - 50) / 53
    ch = 16
    for day in days:
        d = _dt.date.fromisoformat(day["date"])
        week = (d - start).days // 7
        wd = d.weekday()
        if not (0 <= week < 53):
            continue
        a = 0.1 if day["count"] == 0 else 0.25 + 0.65 * (day["count"] / maxc)
        r.append(f'<rect x="{30 + week * cw:.1f}" y="{66 + wd * (ch + 6)}" width="{cw - 2:.1f}" height="{ch}" rx="4" fill="{acc}" fill-opacity="{a:.2f}"/>')
    r.append(f'<text x="30" y="{H-18}" font-family="monospace" font-size="9.5" letter-spacing="2" fill="{dim}">SOURCE: GITHUB CONTRIBUTIONS API - WEEKLY REFRESH</text>')
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            + "".join(r) + "</svg>")


def main():
    try:
        user, repos, events = fetch()
        svg, heat = render_status(user, repos, events)
        with open(os.path.join(OUT, "system-status.svg"), "w") as f:
            f.write(svg)
        with open(os.path.join(OUT, "activity.svg"), "w") as f:
            f.write(render_activity(events))
        try:
            contrib = fetch_contrib()
            with open(os.path.join(OUT, "contributions.svg"), "w") as f:
                f.write(render_contrib(contrib))
            print(f"OK user={user.get('login')} repos={len(repos)} events={len(events)} heat={len(heat)} contrib={sum(d['count'] for d in contrib['contributions'])}")
        except Exception as ce:
            print("contrib skip:", ce)
    except Exception as e:
        fallback = f'<svg width="760" height="120" viewBox="0 0 760 120" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" rx="18" fill="{BG}"/><text x="30" y="50" font-family="monospace" font-size="14" font-weight="700" letter-spacing="3" fill="{TEXT}">GITHUB // SYSTEM STATUS</text><text x="30" y="84" font-family="monospace" font-size="12" fill="{DIM}">SYNC PENDING — the weekly GitHub Actions job will refresh this panel.</text></svg>'
        for name in ("system-status.svg", "activity.svg"):
            with open(os.path.join(OUT, name), "w") as f:
                f.write(fallback)
        print("FALLBACK", e, file=sys.stderr)


if __name__ == "__main__":
    main()