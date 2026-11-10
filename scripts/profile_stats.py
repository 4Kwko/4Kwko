"""Build the profile statistics cards from the public GitHub API.

Writes assets/stats-{pt,en}-{dark,light}.svg and keeps assets/stats.svg
(Portuguese, dark) for links made before the themed versions existed.
The profile repository itself is left out of the counts.
"""

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

from theme import FONT, THEMES

LOGIN = "4Kwko"
ASSETS = Path(__file__).resolve().parents[1] / "assets"

COPY = {
    "pt": {
        "title": "Atividade pública de João Montagner no GitHub",
        "heading": "GitHub em números",
        "updated": "Atualizado em {d:%d/%m/%Y}",
        "labels": ["repositórios públicos", "atualizados em 90 dias", "primeiro ano no GitHub"],
        "bar": "Linguagem principal por repositório (conta repositórios, não linhas de código)",
        "latest": "Atualizações recentes",
        "day": "%d/%m/%Y",
        "desc": "{repos} repositórios públicos, {recent} atualizados nos últimos 90 dias, conta criada em {since}. Linguagem principal por repositório: {langs}. Dados da API pública do GitHub em {d:%d/%m/%Y}.",
    },
    "en": {
        "title": "João Montagner's public GitHub activity",
        "heading": "GitHub at a glance",
        "updated": "Updated {d:%Y-%m-%d}",
        "labels": ["public repositories", "updated in 90 days", "first year on GitHub"],
        "bar": "Main language per repository (counts repositories, not lines of code)",
        "latest": "Recent updates",
        "day": "%Y-%m-%d",
        "desc": "{repos} public repositories, {recent} updated in the last 90 days, account created in {since}. Main language per repository: {langs}. Public GitHub API data from {d:%Y-%m-%d}.",
    },
}


def fetch(path: str):
    request = Request(
        "https://api.github.com/" + path,
        headers={"User-Agent": "profile-stats-script", "Accept": "application/vnd.github+json"},
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def collect() -> dict:
    user = fetch(f"users/{LOGIN}")
    repos = fetch(f"users/{LOGIN}/repos?per_page=100&type=owner")
    owned = [r for r in repos if not r["fork"] and r["name"].lower() != LOGIN.lower()]
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=90)
    recent = sum(
        1 for r in owned if datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")) >= cutoff
    )
    latest = sorted(
        (r for r in owned if not r["archived"] and r["pushed_at"]),
        key=lambda r: r["pushed_at"],
        reverse=True,
    )[:3]
    return {
        "date": now,
        "numbers": [len(owned), recent, user["created_at"][:4]],
        "languages": Counter(r["language"] for r in owned if r["language"]).most_common(5),
        "latest": [(r["name"], datetime.fromisoformat(r["pushed_at"])) for r in latest],
    }


def card(data: dict, lang: str, theme: str) -> str:
    c, t = COPY[lang], THEMES[theme]
    d = data["date"]
    langs = ", ".join(f"{name} {count}" for name, count in data["languages"])
    desc = c["desc"].format(repos=data["numbers"][0], recent=data["numbers"][1],
                            since=data["numbers"][2], langs=langs, d=d)
    latest = [(name, pushed.strftime(c["day"])) for name, pushed in data["latest"]]
    height = 344 + 45 * len(latest) if latest else 270
    if latest:
        desc += f' {c["latest"]}: ' + ", ".join(f"{name} ({day})" for name, day in latest) + "."
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(c["title"])}</title>',
        f'<desc id="desc">{escape(desc)}</desc>',
        f'<rect width="960" height="{height}" rx="16" fill="{t["bg"]}"/>',
        f'<g font-family="{FONT}" fill="{t["text"]}">',
        f'<text x="40" y="48" font-size="22">{escape(c["heading"])}</text>',
        f'<text x="920" y="48" text-anchor="end" fill="{t["muted"]}" font-size="18">{escape(c["updated"].format(d=d))}</text>',
    ]
    for index, (number, label) in enumerate(zip(data["numbers"], c["labels"])):
        x = 40 + index * 300
        parts.append(f'<text x="{x}" y="112" font-size="46" font-weight="700">{number}</text>')
        parts.append(f'<text x="{x}" y="142" fill="{t["muted"]}" font-size="19">{escape(label)}</text>')
    parts.append(f'<text x="40" y="184" fill="{t["muted"]}" font-size="16">{escape(c["bar"])}</text>')
    total = sum(count for _, count in data["languages"]) or 1
    position = 40.0
    for index, (name, count) in enumerate(data["languages"]):
        color = t["series"][index]
        width = 880 * count / total
        parts.append(f'<rect x="{position:.1f}" y="198" width="{max(width - 3, 1):.1f}" height="12" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{40 + index * 176}" y="242" font-size="18" fill="{color}">{escape(name)} {count}</text>')
        position += width
    if latest:
        parts.append(f'<line x1="40" x2="920" y1="267" y2="267" stroke="{t["line"]}"/>')
        parts.append(f'<text x="40" y="307" font-size="22">{escape(c["latest"])}</text>')
    for index, (name, day) in enumerate(latest):
        y = 326 + index * 45
        label = name if len(name) <= 52 else f"{name[:49]}..."
        parts.append(f'<rect x="40" y="{y}" width="880" height="37" rx="5" fill="{t["panel"]}"/>')
        parts.append(f'<circle cx="59" cy="{y + 19}" r="4" fill="{t["series"][0]}"/>')
        parts.append(f'<text x="75" y="{y + 25}" font-size="21">{escape(label)}</text>')
        parts.append(f'<text x="903" y="{y + 25}" text-anchor="end" font-size="19" fill="{t["muted"]}">{day}</text>')
    parts.append("</g></svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    data = collect()
    for lang in COPY:
        for theme in THEMES:
            (ASSETS / f"stats-{lang}-{theme}.svg").write_text(card(data, lang, theme), encoding="utf-8")
    (ASSETS / "stats.svg").write_text(card(data, "pt", "dark"), encoding="utf-8")
    print("Updated public profile statistics.")
