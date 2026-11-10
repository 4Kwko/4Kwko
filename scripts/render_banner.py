"""Render the profile banner in Portuguese and English, dark and light.

Run once after changing the copy or palette:  python scripts/render_banner.py
The pulse animation only runs when the viewer allows motion.
"""

from html import escape
from pathlib import Path

from theme import FONT, THEMES

ASSETS = Path(__file__).resolve().parents[1] / "assets"

COPY = {
    "pt": {
        "title": "João Montagner — sistemas, automações e integrações",
        "desc": "Python, APIs e SQL. Um sinal percorre três etapas: evento, automação e dados.",
        "subtitle": "sistemas · automações · integrações",
        "nodes": ["evento", "automação", "dados"],
    },
    "en": {
        "title": "João Montagner — software, automation and integrations",
        "desc": "Python, APIs and SQL. A signal travels through three steps: event, automation and data.",
        "subtitle": "software · automation · integrations",
        "nodes": ["event", "automation", "data"],
    },
}

NODE_X = (40, 355, 670)
NODE_W, NODE_H, NODE_Y = 250, 64, 200


def banner(lang: str, theme: str) -> str:
    c, t = COPY[lang], THEMES[theme]
    centers = [x + NODE_W / 2 for x in NODE_X]
    travel = centers[-1] - centers[0]
    cy = NODE_Y + NODE_H / 2
    nodes = "".join(
        f'<rect x="{x + 4}" y="{NODE_Y + 5}" width="{NODE_W}" height="{NODE_H}" rx="9" fill="{t["line"]}"/>'
        f'<rect x="{x}" y="{NODE_Y}" width="{NODE_W}" height="{NODE_H}" rx="9" fill="{t["panel"]}" '
        f'stroke="{t["line"]}"/>'
        f'<circle cx="{x + 25}" cy="{cy}" r="5" fill="{color}"/>'
        f'<text x="{x + NODE_W / 2}" y="{cy + 9}" text-anchor="middle" font-size="26" fill="{t["text"]}">'
        f"{escape(label)}</text>"
        for x, label, color in zip(NODE_X, c["nodes"], t["series"])
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 300" role="img" aria-labelledby="title desc">
<title id="title">{escape(c["title"])}</title>
<desc id="desc">{escape(c["desc"])}</desc>
<style>
.pulse {{ transform: translateX(0); }}
@media (prefers-reduced-motion: no-preference) {{
  .pulse {{ animation: travel 7s ease-in-out infinite; }}
}}
@keyframes travel {{
  0%, 8% {{ transform: translateX(0); }}
  92%, 100% {{ transform: translateX({travel:.0f}px); }}
}}
</style>
<rect width="960" height="300" rx="16" fill="{t["bg"]}"/>
<rect x="40" y="31" width="63" height="5" rx="2.5" fill="{t["series"][0]}"/>
<line x1="117" y1="33.5" x2="920" y2="33.5" stroke="{t["line"]}"/>
<g font-family="{FONT}">
<text x="40" y="103" font-family="Georgia, 'DejaVu Serif', serif" font-size="62" fill="{t["text"]}">João Montagner</text>
<text x="40" y="142" font-size="30" fill="{t["accent"]}">{escape(c["subtitle"])}</text>
<line x1="{centers[0]}" y1="{cy}" x2="{centers[-1]}" y2="{cy}" stroke="{t["muted"]}" stroke-width="2" stroke-dasharray="6 6"/>
<circle class="pulse" cx="{centers[0]}" cy="{cy}" r="7" fill="{t["accent"]}"/>
{nodes}
</g>
</svg>
"""


if __name__ == "__main__":
    for lang in COPY:
        for theme in THEMES:
            (ASSETS / f"banner-{lang}-{theme}.svg").write_text(banner(lang, theme), encoding="utf-8")
    print("Rendered 4 banners.")
