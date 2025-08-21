#!/usr/bin/env bash
set -euo pipefail

SERVICE="pw-simple-scraper-test"
DC="${DC:-docker compose}"

REBUILD=false
if [[ "${1:-}" == "--rebuild" ]]; then
  REBUILD=true
fi

if $REBUILD; then
  echo "[INFO] Rebuilding image..."
  $DC build "$SERVICE"
else
  echo "[INFO] Checking for existing image..."
  IMG_ID="$($DC images --quiet "$SERVICE" || true)"
  if [[ -z "$IMG_ID" ]]; then
    echo "[INFO] No image found. Building..."
    $DC build "$SERVICE"
  else
    echo "[INFO] Reusing existing image: $IMG_ID"
  fi
fi

echo "[INFO] Running tests..."
exec $DC run --rm \
  -e PYTEST_ADDOPTS="" \
  "$SERVICE" \
  pytest -vv -ra -s
