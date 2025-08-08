#!/usr/bin/env bash
set -euo pipefail

REPO_URL=${1:-"https://github.com/dperezinnopulse/GenDoc"}
BRANCH=${2:-"main"}

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Set GITHUB_TOKEN env var (Personal Access Token)" >&2
  exit 1
fi

cd "$(dirname "$0")"

git branch -M "$BRANCH"

git remote remove origin 2>/dev/null || true
# Insert token in URL safely
PROTO=$(echo "$REPO_URL" | sed -E 's#(https?)://.*#\1#')
HOST=$(echo "$REPO_URL" | sed -E 's#https?://([^/]+)/.*#\1#')
PATHP=$(echo "$REPO_URL" | sed -E 's#https?://[^/]+/(.*)#\1#')
TOKEN_URL="${PROTO}://${GITHUB_TOKEN}@${HOST}/${PATHP}"

git remote add origin "$TOKEN_URL"

git push -u origin "$BRANCH"

echo "Pushed to ${REPO_URL} on branch ${BRANCH}"