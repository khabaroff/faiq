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
