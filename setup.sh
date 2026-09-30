#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v hugo >/dev/null; then
  command -v brew >/dev/null || { echo '请先安装 Homebrew，或安装 Hugo 0.167.0 及以上版本。'; exit 1; }
  brew install hugo
fi
if [[ ! -e docs/.git ]]; then
  git submodule update --init docs
fi
# Submodules are checked out detached after a fresh clone.
if [[ -z "$(git -C docs branch --show-current)" && -z "$(git -C docs status --porcelain)" ]]; then
  git -C docs switch master
fi
hugo version
echo '环境准备完成。运行 make preview 预览，运行 ./deploy.sh 发布。'
