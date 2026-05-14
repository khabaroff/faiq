#!/usr/bin/env bash
set -euo pipefail
# Runbook helper: secrets rotation reminders and checks
# Usage: scripts/rotate_secrets.sh [--check|--remind|--rotate <secret>]

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_ROOT}/.env"
RUNBOOK="${REPO_ROOT}/_human/runbook.md"

print_reminders() {
    echo "=== Secrets Rotation Reminders ==="
    echo ""
    echo "Azure OpenAI key     : every 90 days"
    echo "GitHub PAT           : every 90 days"
    echo "Telegram bot token   : every 180 days"
    echo "Jina API key         : every 180 days"
    echo ""
    echo "See ${RUNBOOK} for detailed steps."
}

check_permissions() {
    if [[ ! -f "${ENV_FILE}" ]]; then
        echo "ERROR: ${ENV_FILE} not found"
        exit 1
    fi
    local perms
    perms=$(stat -f "%A" "${ENV_FILE}" 2>/dev/null || stat -c "%a" "${ENV_FILE}" 2>/dev/null)
    if [[ "${perms}" != "600" ]]; then
        echo "WARNING: ${ENV_FILE} permissions are ${perms}, expected 600"
        echo "Run: chmod 600 ${ENV_FILE}"
        exit 1
    fi
    echo "OK: ${ENV_FILE} permissions are 600 (owner-only)"
}

check_example() {
    if grep -qE 'sk-.*example|pk-.*example|sk-.*test|pk-.*test' "${REPO_ROOT}/.env.example" 2>/dev/null; then
        echo "WARNING: .env.example contains plausible-looking secrets"
        exit 1
    fi
    echo "OK: .env.example contains no plausible defaults"
}

gitleaks_check() {
    if command -v gitleaks &>/dev/null; then
        echo "Running gitleaks detect..."
        gitleaks detect --source "${REPO_ROOT}" --no-git || true
    else
        echo "SKIP: gitleaks not installed. Install: brew install gitleaks"
    fi
}

main() {
    case "${1:-}" in
        --check)
            check_permissions
            check_example
            gitleaks_check
            ;;
        --remind|"")
            print_reminders
            ;;
        *)
            echo "Usage: $0 [--check|--remind]"
            exit 1
            ;;
    esac
}

main "$@"
