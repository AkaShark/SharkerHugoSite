#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Keep the original one-argument command for existing habits.
if [[ $# -eq 1 && "$1" == *.md && "$1" != /* && "/$1/" != *'/../'* ]]; then
  hugo new content "posts/$1"
else
  python3 scripts/new_post.py "$@"
fi
