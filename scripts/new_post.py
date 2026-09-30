#!/usr/bin/env python3
"""Create a draft page bundle using only the Python standard library."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description='创建文章草稿：图片和正文保存在同一文件夹')
p.add_argument('category', choices=['tech', 'read', 'life'])
p.add_argument('slug', help='稳定的英文短链接，例如 wkwebview-notes')
p.add_argument('title', help='文章标题（包含空格时加引号）')
p.add_argument('--series', default='', help='可选专题名')
p.add_argument('--order', type=int, default=1, help='专题中的阅读顺序')
a = p.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a.slug):
    p.error('slug 仅允许小写英文、数字和连字符')
now = dt.datetime.now().astimezone()
folder = ROOT / 'content/posts' / a.category / str(now.year) / a.slug
# The explicit URL is independent of title/year/folder. Reject collisions across years.
url = f'/en/posts/{a.category}/{a.slug}/'
for existing in (ROOT / 'content').rglob('*.md'):
    if f'url: {json.dumps(url)}' in existing.read_text():
        p.error(f'短链接已存在：{existing.relative_to(ROOT)}')
folder.mkdir(parents=True, exist_ok=False)
data = {'title': a.title, 'date': now.isoformat(timespec='seconds'), 'lastmod': now.isoformat(timespec='seconds'),
        'url': url, 'author': 'Sharker', 'categories': [{'tech':'技术','read':'阅读','life':'生活'}[a.category]],
        'tags': [], 'description': '', 'draft': True}
if a.series:
    data.update(series=[a.series], series_order=a.order)
body = {'tech':'## 问题与背景\n\n## 环境与复现\n\n## 分析与实现\n\n## 验证与结论\n\n## 参考资料\n',
        'read':'## 阅读对象与问题\n\n## 核心观点\n\n## 我的理解与实践\n\n## 未解决的问题\n\n## 参考资料\n',
        'life':'## 发生了什么\n\n## 我的观察\n\n## 下一步行动\n'}[a.category]
file = folder / 'index.md'
file.write_text('---\n' + ''.join(f'{k}: {json.dumps(v, ensure_ascii=False)}\n' for k,v in data.items()) + '---\n\n' + body)
print(f'已创建草稿：{file.relative_to(ROOT)}\n预览地址：http://localhost:1313{url}\n完成 description 和 tags 后，写好正文，再将 draft 改为 false。')
