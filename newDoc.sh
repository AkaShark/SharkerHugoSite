#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ $# -ne 1 || "$1" != *.md || "$1" == /* || "/$1/" == *'/../'* ]]; then
  echo '用法：./newDoc.sh "tech/我的新文章.md"'
  exit 1
fi
hugo new content "posts/$1"
