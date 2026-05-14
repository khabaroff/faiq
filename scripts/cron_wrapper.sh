#!/usr/bin/env bash
set -euo pipefail
# Cron wrapper for Guides pipeline with healthchecks.io ping
# Usage: scripts/cron_wrapper.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Load .env if present
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

LOG_FILE="${LOG_FILE:-logs/cron.log}"
mkdir -p "$(dirname "$LOG_FILE")"

# Run full pipeline
if python -m guides.pipelines.run_all >> "$LOG_FILE" 2>&1; then
  if [ -n "${HEALTHCHECKS_URL:-}" ]; then
    curl -fsS -m 10 --retry 5 "${HEALTHCHECKS_URL}" -o /dev/null || true
  fi
  echo "$(date -Iseconds) Pipeline OK" >> "$LOG_FILE"
else
  echo "$(date -Iseconds) Pipeline FAILED" >> "$LOG_FILE"
  exit 1
fi
