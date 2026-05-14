# Security Policy

## Threat Model & Mitigations

### 1. SSRF & URL Fetching
- **Policy:** All incoming URLs (articles, YouTube, PDFs) are validated through a central `validate_url` chain.
- **Mitigation:** 
  - Blocklist for internal IP ranges (169.254.0.0/16, private ranges) and sensitive hosts (`localhost`, `metadata.google.internal`).
  - Allowed schemes: `http`, `https`. Explicitly blocks `file://`, `gopher://`, `dict://`.
  - Redirect Revalidation: Multi-step redirects are followed manually with re-validation of the final URL before fetching content.

### 2. Prompt Injection
- **Policy:** User-controlled content is treated as untrusted and wrapped in XML/marker tags.
- **Mitigation:**
  - `<<SOURCE>>` boundary convention in all prompts.
  - `SECURITY NOTICE` pattern in system prompts to reinforce constraints.
  - Pydantic validation of LLM outputs to enforce schema constraints.
  - State-machine based JSON extractor (`src/guides/json_extract.py`) to prevent greedy capture and injection outside brackets.

### 3. Supply Chain Security
- **Policy:** Strict pinning of dependencies and removal of dynamic execution.
- **Mitigation:**
  - All dependencies pinned in `pyproject.toml` and `uv.lock`.
  - **No dynamic execution:** Removed `npx -y defuddle-cli` fallbacks; moved to pure Python libraries (`trafilatura`).
  - No `curl | sh` installers allowed in deployment runbooks.

### 4. Secrets & Sensitive Data
- **Policy:** Zero-tolerance for plaintext secrets in logs or source control.
- **Mitigation:**
  - `.env` file is added to `.gitignore` and restricted with `chmod 600`.
  - Unified redaction filter (`src/guides/log_setup.py`) automatically masks tokens and keys in all logging handlers.
  - API traces are cleansed of sensitive headers before logging.

## Reporting a Vulnerability
Please report security issues directly to the maintainer via Sergei Khabarov (khabaroff@gmail.com).
