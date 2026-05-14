# Runbook: Secrets & Operations

## Secrets Rotation

### Azure OpenAI API Key

- **Where to rotate:** Azure OpenAI Studio → Keys & Endpoints → Regenerate key
- **How often:** every 90 days (corporate policy) or immediately after any suspected leak
- **Downstream impact:** Pipeline halts until new key is deployed
- **Steps:**
  1. Generate new key #2 in Azure Portal
  2. `echo "AZURE_OPENAI_API_KEY=<new_key>" >> .env`
  3. Restart pipeline or cron service
  4. Delete old key #1 after confirming pipeline runs

### Telegram Bot Token

- **Where to rotate:** @BotFather → /revoke → get new token
- **How often:** every 180 days or on team change
- **Downstream impact:** Telegram publisher stops posting; no data loss
- **Steps:**
  1. Message @BotFather, run `/revoke`
  2. Copy new token
  3. Update `.env`: `TELEGRAM_BOT_TOKEN=<new_token>`
  4. Test: `python -m guides.pipelines.g_telegram --dry-run`

### GitHub Personal Access Token (PAT)

- **Where to rotate:** GitHub Settings → Developer Settings → Personal Access Tokens
- **How often:** every 90 days (classic) or on expiration (fine-grained)
- **Downstream impact:** GitHub fetcher (repos/gists) fails with 401
- **Steps:**
  1. Settings → Developer settings → Tokens → Generate new token
  2. Required scopes: `repo` (for private repos), `gist` (for gists)
  3. Update `.env`: `GITHUB_TOKEN=<new_token>`
  4. Test: `python -m guides.fetch.github --test`

### Jina API Key

- **Where to rotate:** https://jina.ai/keys → Regenerate
- **How often:** every 180 days
- **Steps:**
  1. Log in to Jina dashboard
  2. Regenerate key
  3. Update `.env`: `JINA_API_KEY=<new_key>`

### Langfuse Keys (if enabled)

- **Where to rotate:** Langfuse Cloud → Project Settings → API Keys
- **How often:** on team change or suspected leak
- **Steps:**
  1. Create new key pair
  2. Update `.env`
  3. Delete old key pair

## Environment File Security

```bash
# .env must be owner-readable only
chmod 600 .env
ls -la .env   # expect: -rw-------
```

Never commit `.env`. `.env.example` contains empty values only — no plausible defaults (no `sk-...example`).

## CI Secrets Scan

`gitleaks` runs on every push/PR via `.github/workflows/ci.yml`.
To test locally:

```bash
# Install gitleaks
echo "AZURE_OPENAI_API_KEY=sk-test12345" > /tmp/fake_secret.txt
gitleaks detect --source . --no-git
```

If gitleaks finds a secret in CI, the build fails. Rotate the exposed secret immediately.

## Operational Procedures

### Parallel Workers Configuration
As of Sprint 3, parallel processing is enabled for PDF OCR and certain fetchers.
- **Max workers:** Recommended `CPU_COUNT * 2` or restricted by LLM Tier limits (TPM).
- **Safety:** `state.py` uses `busy_timeout=5.0` and `threading-local` connections, making it thread-safe for parallel writes.

### Database Recovery: "database is locked"
If SQLite remains locked due to a crashed process:
1. Identify holding process: `fuser state/articles.db`
2. Kill the process: `kill -9 <PID>`
3. Remove WAL files if persistent: `rm state/articles.db-wal state/articles.db-shm` (Warning: may lose last transaction)
4. Verify integrity: `sqlite3 state/articles.db "PRAGMA integrity_check;"`

### Reading Cost Reports
Cost reports are generated as JSONL in `logs/cost_report.jsonl`.
- **Tool:** Use `python -m guides.tools.cost_report --summarize` to see daily/monthly totals.
- **Filtering:** Use `jq` for custom queries on JSONL logs.

### Backup & Restore
1. **Backup:** `cp state/articles.db state/articles.db.bak`
2. **Restore:** `mv state/articles.db.bak state/articles.db`
3. **Wiki Backup:** Wiki pages are backed up in `wiki/.backups/` (10 versions kept).

## Incident Response & Troubleshooting

### Scenario: "database is locked" (Persistent)
1. **Detect:** Log entry "sqlite3.OperationalError: database is locked" in `logs/cron.log`.
2. **Mitigation:**
   - `fuser -v state/articles.db` to find PID.
   - `kill -15 <PID>` (wait 5s) or `kill -9 <PID>`.
   - If WAL files are stale: `rm state/articles.db-wal state/articles.db-shm`.

### Scenario: Telegram 429 (Rate Limit)
1. **Detect:** "TelegramError: 429 Too Many Requests".
2. **Mitigation:**
   - The pipeline handles this with exponential backoff.
   - If persistent, check if `TELEGRAM_CHANNEL_ID` is being flooded (multiple processes?).
   - Verify only one cron job is running: `crontab -l`.

### Scenario: Azure 500 / 503 / 504 Storm
1. **Detect:** Repeated "llm_retry" entries in `daily_log`.
2. **Mitigation:**
   - Check [Azure Service Health](https://status.azure.com/).
   - Reduce `--workers` if hitting regional limits.
   - Stop cron temporarily: `crontab -e` (comment out entry).

### Scenario: Broken Backup
1. **Detect:** `sqlite3 state/articles.db "PRAGMA integrity_check;"` returns errors.
2. **Mitigation:**
   - Restore from `state/articles.db.bak`.
   - If backup is also corrupt, re-run Pipeline A on `data/inbox/done/` to rebuild from source bundles.

### Scenario: Deploy Failure / Regression
1. **Rollback Command:**
   ```bash
   # Switch back to previous release folder
   PREV_REL=$(ls -1tr releases/ | tail -n 2 | head -n 1)
   ln -sfn "releases/$PREV_REL" current
   ```
