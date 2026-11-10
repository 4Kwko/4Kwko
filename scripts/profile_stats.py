import json
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def fetch(path):
    request = Request('https://api.github.com/' + path, headers={'User-Agent': '4Kwko-profile', 'Accept': 'application/vnd.github+json'})
    with urlopen(request, timeout=30) as response:
        return json.load(response)

user = fetch('users/4Kwko')
repos = fetch('users/4Kwko/repos?per_page=100&type=owner')
owned = [repo for repo in repos if not repo['fork']]
languages = Counter(repo['language'] for repo in owned if repo['language'])
date = datetime.now(timezone.utc).strftime('%d/%m/%Y')
stats = [(user['public_repos'], 'repositórios públicos'), (sum(repo['stargazers_count'] for repo in owned), 'estrelas nos projetos'), (user['followers'], 'seguidores')]
parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 270" role="img" aria-labelledby="title desc">', '<title id="title">Atividade pública de João Montagner no GitHub</title>', f'<desc id="desc">Dados da API pública do GitHub, atualizados em {date}. Linguagens contam repositórios pela linguagem principal.</desc>', '<rect width="960" height="270" rx="16" fill="#111b27"/>', '<g font-family="Verdana, sans-serif" fill="#f2f6fa">', '<text x="30" y="40" font-size="17">Meu GitHub em números</text>', f'<text x="930" y="40" text-anchor="end" fill="#9eafbf" font-size="12">Atualizado em {date}</text>']
for index, (number, label) in enumerate(stats):
    x = 30 + index * 310
    parts += [f'<text x="{x}" y="100" font-size="40" font-weight="bold">{number}</text>', f'<text x="{x}" y="126" fill="#9eafbf" font-size="14">{label}</text>']
parts.append('<text x="30" y="169" fill="#9eafbf" font-size="13">Linguagem principal dos repositórios próprios</text>')
total = sum(languages.values())
position = 30
colors = ['#55d8b2', '#f2bc59', '#75aaf5', '#ed8ca1', '#b2a4e8', '#98b2bc']
for index, (language, count) in enumerate(languages.most_common(5)):
    width = 900 * count / total
    color = colors[index]
    parts.append(f'<rect x="{position:.1f}" y="187" width="{width:.1f}" height="10" fill="{color}"/>')
    parts.append(f'<text x="{30+index*180}" y="225" font-size="12" fill="{color}">{escape(language)} · {count}</text>')
    position += width
parts.append('</g></svg>')
(ASSETS / 'stats.svg').write_text('\n'.join(parts), encoding='utf-8')
print('Updated public profile statistics.')
