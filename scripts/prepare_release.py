#!/usr/bin/env python3
"""Generate durable old-URL redirects and the GitHub Pages release markers."""
from pathlib import Path
from urllib.parse import unquote
import html
import json

ROOT = Path(__file__).resolve().parents[1]
site = ROOT / '.build/site'
redirects = json.loads((ROOT / 'planning/redirects.json').read_text())
count = 0
for old, new in redirects.items():
    oldfile = site / unquote(old).lstrip('/') / 'index.html'
    target = site / unquote(new).lstrip('/') / 'index.html'
    # A withdrawn destination should not leave a redirect pointing to missing content.
    if oldfile.exists() or not target.exists():
        continue
    oldfile.parent.mkdir(parents=True, exist_ok=True)
    escaped = html.escape(new, quote=True)
    oldfile.write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="https://akashark.github.io{escaped}"><meta http-equiv="refresh" content="0; url={escaped}"><title>文章已整理</title></head><body><a href="{escaped}">前往新页面</a></body></html>')
    count += 1
(site / '.nojekyll').touch()
# GitHub Pages needs a root-level custom 404, even though content lives under /en/.
(site / '404.html').write_bytes((site / 'en/404.html').read_bytes())
print(f'已生成 {count} 个旧地址跳转。')
