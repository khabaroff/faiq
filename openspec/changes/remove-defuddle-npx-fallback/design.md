# Design: Trafilatura Integration

## Architecture
- Replace `src/guides/fetch/url.py` logic that called `subprocess.run(["npx", "defuddle-cli", ...])`.
- Implement `trafilatura.extract()` with configuration for high-quality Markdown output.

## Implementation Details
- Handle edge cases where `trafilatura` returns None by falling back to `jina.ai` reader API (as secondary fallback).
- Ensure headers (User-Agent) are consistent with the rest of the project.
