# ADR-001: Remove defuddle-npx-fallback

## Background
Pipeline A used `npx -y defuddle-cli` as a primary extraction path. This introduced a dependency on Node.js and an unpinned dynamic execution path (`npx -y`), which is a supply-chain security risk.

## Proposal
Replace the `defuddle-cli` external process call with the `trafilatura` Python library.

## Rationale
- **Security:** Removes `npx` and Node.js dependency; avoids running unverified code from npm at runtime.
- **Performance:** Native Python call is significantly faster than spawning a Node process.
- **Reliability:** `trafilatura` provides comparable (and often better) content extraction for modern web articles.
