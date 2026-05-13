#!/bin/bash
# Wrapper to run commands with flock to prevent concurrent execution.
# Usage: ./cron/flock_wrapper.sh lock_name command...

LOCK_NAME=$1
shift

LOCKFILE="/tmp/guides_${LOCK_NAME}.lock"

# flock -n: non-blocking (fails if locked)
# -c: command
flock -n "$LOCKFILE" "$@"
if [ $? -ne 0 ]; then
    echo "[$(date)] Skip: $LOCK_NAME is already running."
    exit 0
fi
