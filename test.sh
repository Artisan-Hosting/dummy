#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Remove only top-level numeric directories (1, 2, ..., 100, etc).
find . -mindepth 1 -maxdepth 1 -type d -regextype posix-extended -regex './[0-9]+' -exec rm -rf {} +

# Regenerate repo contents.
NUM_DIRS=500 python3 file.py

# Stage all changes in the repo.
git add --all

# Commit only when there is something staged.
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

commit_message="${1:-Testing update $(date '+%Y-%m-%d %H:%M:%S')}"
git commit -m "$commit_message"

current_branch="$(git branch --show-current)"
git push origin "$current_branch"
