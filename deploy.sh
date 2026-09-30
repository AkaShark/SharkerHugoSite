#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

command -v hugo >/dev/null || { echo '请先运行 ./setup.sh'; exit 1; }
if [[ ! -e docs/.git ]]; then
  git submodule update --init docs
fi
if [[ -n "$(git -C docs status --porcelain)" ]]; then
  echo 'docs 中有未提交的修改，请先检查并处理后再发布。'
  exit 1
fi
if [[ "$(git -C docs branch --show-current)" != master ]]; then
  echo 'docs 必须位于 master 分支；请先运行 git -C docs switch master。'
  exit 1
fi
git -C docs pull --ff-only origin master

# Build in isolation: a failed build must never overwrite the published checkout.
echo '正在构建正式站点（不包含草稿）...'
make check

# This repository is generated output. Delete obsolete pages and assets while protecting Git and domain configuration.
rsync -a --delete --exclude='.git' --exclude='CNAME' .build/site/ docs/
git -C docs add --all
if ! git -C docs diff --cached --quiet; then
  git -C docs commit -m "${1:-Publish blog $(date '+%Y-%m-%d %H:%M:%S %z')}"
fi
git -C docs push origin master
echo '已推送发布仓库。GitHub Pages 构建完成后生效：https://akashark.github.io/'
