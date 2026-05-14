#!/bin/bash
# scripts/deploy.sh - Symlink-based atomic deployment with rollback capability

set -e

REPO_ROOT=$(pwd)
RELEASES_DIR="$REPO_ROOT/releases"
CURRENT_SYMLINK="$REPO_ROOT/current"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
NEW_RELEASE="$RELEASES_DIR/$TIMESTAMP"

mkdir -p "$RELEASES_DIR"

echo "Deploying new release to $NEW_RELEASE..."

# 1. Create release directory and copy code
mkdir -p "$NEW_RELEASE"
rsync -a --exclude 'releases' --exclude 'current' --exclude '.git' --exclude '.venv' --exclude 'logs' --exclude 'state' --exclude 'data' . "$NEW_RELEASE/"

# 2. Setup environment
cd "$NEW_RELEASE"
uv sync --frozen

# 3. Symlink swap
ln -sfn "$NEW_RELEASE" "$CURRENT_SYMLINK"

# 4. Cleanup old releases (keep last 5)
cd "$RELEASES_DIR"
ls -1tr | head -n -5 | xargs -d '\n' rm -rf -- || true

echo "Deployment complete: $TIMESTAMP"
echo "Rollback: ln -sfn $(ls -1tr $RELEASES_DIR | tail -n 2 | head -n 1) $CURRENT_SYMLINK"
