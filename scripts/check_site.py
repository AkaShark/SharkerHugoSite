#!/usr/bin/env python3
"""Check a production build before publishing; no extra Python packages needed."""
import csv
import io
import json
from pathlib import Path
import re
import subprocess
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '.build/site'
errors = []
rows = list(csv.DictReader(io.StringIO(subprocess.check_output(['hugo','list','all','--noBuildLock'], cwd=ROOT, text=True, timeout=30))))
posts = [r for r in rows if r['kind']=='page' and r['section']=='posts']
published = [r for r in posts if r['draft']=='false' and (SITE / unquote(urlparse(r['permalink']).path).lstrip('/') / 'index.html').exists()]
seen = {}
for r in posts:
    if r['permalink'] in seen:
        errors.append(f"重复文章地址：{r['path']} / {seen[r['permalink']]}")
    seen[r['permalink']] = r['path']
for r in published:
    source = (ROOT/r['path']).read_text()
    front,body = source.split('---',2)[1:]
    if len(body.strip()) < 80: errors.append(f"正文过短或为空：{r['path']}")
    if not re.search(r'^description:\s*"[^"\n]+"',front,re.M): errors.append(f"缺少一句话摘要：{r['path']}")
    if re.search(r'^tags:\s*\[\s*\]',front,re.M) or not re.search(r'^tags:',front,re.M): errors.append(f"请填写标签：{r['path']}")

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.canonical=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='link' and a.get('rel')=='canonical': self.canonical=a.get('href')
        if tag in ('a','img','script','link'):
            v=a.get('href') or a.get('src')
            if v: self.links.append(v)

missing = set()
for file in SITE.rglob('*.html'):
    html=file.read_text()
    if re.search(r'%![a-z]\(', html): errors.append(f'模板格式错误：{file.relative_to(SITE)}')
    page=Page();page.feed(html)
    # Redirects have no article text and their destinations are checked as normal links.
    base='https://akashark.github.io/'+file.relative_to(SITE).as_posix()
    for link in page.links:
        u=urlparse(urljoin(base,link))
        if u.scheme not in ('http','https') or u.netloc!='akashark.github.io': continue
        path=SITE/unquote(u.path).lstrip('/')
        if not path.exists() and not (path/'index.html').exists():
            missing.add((file.relative_to(SITE).as_posix(),u.path))
for file,path in sorted(missing): errors.append(f'站内链接缺失：{file} -> {path}')
for file in SITE.rglob('*.xml'):
    try: ET.parse(file)
    except ET.ParseError as e: errors.append(f'XML 无效：{file}: {e}')
index=json.loads((SITE/'en/index.json').read_text())
index_urls=[x['permalink'] for x in index]
expected={urlparse(r['permalink']).path for r in published}
if len(index_urls)!=len(set(index_urls)): errors.append('搜索索引存在重复地址')
if set(index_urls)!=expected: errors.append('搜索索引与已发布文章不一致')
for r in rows:
    if r['draft']=='true':
        file=SITE/unquote(urlparse(r['permalink']).path).lstrip('/')/'index.html'
        if file.exists() and 'http-equiv="refresh"' not in file.read_text(): errors.append(f"草稿出现在正式构建：{r['path']}")
for item in index:
    if not item.get('content'): errors.append('搜索索引缺少全文：'+item['title'])
if not (SITE/'.nojekyll').exists() or not (SITE/'404.html').exists(): errors.append('缺少 GitHub Pages 发布文件')
if errors:
    print('\n'.join(errors[:30]));print(f'共 {len(errors)} 个问题');raise SystemExit(1)
print(f'检查通过：{len(published)} 篇正式文章；搜索、RSS、站内链接、唯一地址与草稿隔离正常。')
