#!/usr/bin/env python3
"""Generate the startup-style hero banner for profile/README.md.

Usage: python3 scripts/gen-header.py
Writes profile/assets/header-dark.svg and profile/assets/header-light.svg.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT_DIR = Path(__file__).resolve().parent.parent / "profile" / "assets"

WIDTH, HEIGHT = 900, 380
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

EYEBROW = "AI AGENT STUDIO  ·  GREATER BAY AREA"
TITLE = "agenticker"
TAGLINE = "Agents you can see, understand & trust."
SUBLINE = "大湾区 AI 创业团队 · 让 AI Agent 真正进入业务生产"
STATS = [("8", "in-house products"), ("5", "open-source repos"), ("4", "industry domains")]

THEMES = {
    "dark": {
        "bg": "#0b0f17", "border": "#262c36", "text": "#f0f3f6", "muted": "#8b949e",
        "dot": "#1f2633", "pill": "#121826", "live": "#3fb950",
        "grad": ("#a78bfa", "#22d3ee"), "glow": ("#7c3aed", "#0891b2"), "glow_op": 0.35,
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "text": "#1f2328", "muted": "#59636e",
        "dot": "#e5e9ef", "pill": "#f6f8fa", "live": "#1a7f37",
        "grad": ("#7c3aed", "#0284c7"), "glow": ("#c4b5fd", "#a5f3fc"), "glow_op": 0.55,
    },
}


def fade(begin: float) -> str:
    return (f'<animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{begin:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" dur="0.6s" '
            f'begin="{begin:.2f}s" fill="freeze"/>')


def staged(begin: float, body: str) -> str:
    return f'<g opacity="0">{fade(begin)}{body}</g>'


def text(x: float, y: float, content: str, attrs: str) -> str:
    return f'<text x="{x}" y="{y}" text-anchor="middle" {attrs}>{escape(content)}</text>'


def glow(cid: str, cx: float, cy: float, color: str, opacity: float, dur: str) -> str:
    return (f'<radialGradient id="{cid}"><stop offset="0" stop-color="{color}" stop-opacity="{opacity}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>'), (
            f'<circle cx="{cx}" cy="{cy}" r="320" fill="url(#{cid})">'
            f'<animate attributeName="r" values="300;350;300" dur="{dur}" repeatCount="indefinite"/></circle>')


def pill(cx: float, y: float, t: dict) -> str:
    width = len(EYEBROW) * 8.0 + 44
    left = cx - width / 2
    dot = (f'<circle cx="{left + 18}" cy="{y}" r="4" fill="{t["live"]}">'
           f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')
    label = (f'<text x="{left + 32}" y="{y + 4}" font-family="{MONO}" font-size="11" letter-spacing="1.4" '
             f'fill="{t["muted"]}" xml:space="preserve">{escape(EYEBROW)}</text>')
    return (f'<rect x="{left}" y="{y - 14}" width="{width}" height="28" rx="14" fill="{t["pill"]}" '
            f'stroke="{t["border"]}"/>{dot}{label}')


def stats(cx: float, y: float, t: dict) -> str:
    step = 190
    start = cx - step * (len(STATS) - 1) / 2
    out = []
    for i, (num, label) in enumerate(STATS):
        x = start + i * step
        out.append(text(x, y, num, f'font-family="{SANS}" font-size="30" font-weight="700" fill="url(#g)"'))
        out.append(text(x, y + 22, label, f'font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["muted"]}"'))
        if i:
            out.append(f'<line x1="{x - step / 2}" y1="{y - 24}" x2="{x - step / 2}" y2="{y + 24}" stroke="{t["border"]}"/>')
    return "".join(out)


def render(t: dict) -> str:
    cx = WIDTH / 2
    g1_def, g1 = glow("glowA", 120, 40, t["glow"][0], t["glow_op"], "9s")
    g2_def, g2 = glow("glowB", WIDTH - 120, HEIGHT - 20, t["glow"][1], t["glow_op"], "11s")
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'role="img" aria-label="agenticker — {escape(TAGLINE)}">',
        "<defs>",
        f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["grad"][0]}"/>'
        f'<stop offset="1" stop-color="{t["grad"][1]}"/></linearGradient>',
        f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.2" fill="{t["dot"]}"/></pattern>',
        f'<clipPath id="card"><rect width="{WIDTH}" height="{HEIGHT}" rx="16"/></clipPath>',
        g1_def, g2_def,
        "</defs>",
        f'<g clip-path="url(#card)"><rect width="{WIDTH}" height="{HEIGHT}" fill="{t["bg"]}"/>'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#dots)"/>{g1}{g2}</g>',
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="16" fill="none" stroke="{t["border"]}"/>',
        staged(0.1, pill(cx, 62, t)),
        staged(0.3, text(cx, 156, TITLE, f'font-family="{SANS}" font-size="72" font-weight="800" '
                                          f'letter-spacing="-2" fill="url(#g)"')),
        staged(0.55, text(cx, 200, TAGLINE, f'font-family="{SANS}" font-size="22" font-weight="600" fill="{t["text"]}"')),
        staged(0.7, text(cx, 230, SUBLINE, f'font-family="{SANS}" font-size="15" fill="{t["muted"]}"')),
        staged(0.9, stats(cx, 300, t)),
        "</svg>",
    ]) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        path = OUT_DIR / f"header-{name}.svg"
        path.write_text(render(theme), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
