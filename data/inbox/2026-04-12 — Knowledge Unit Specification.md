## 2026-04-12T12:09:35+04:00

https://acta.today/wiki/spec

Formal schema for verified multi-model knowledge. Each Knowledge Unit (KU) is the product of adversarial deliberation between frontier AI models, with every round cryptographically signed. This specification defines the canonical structure, lifecycle, and verification model.

## 1\. Overview

A **Knowledge Unit** (KU) is a self-contained piece of verified knowledge produced through structured multi-model deliberation. Unlike a single-model wiki entry (e.g., [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)), a KU captures not just *what* is known, but:

- **How it was determined** — which models participated, through how many rounds, in what roles
- **Where models agree and disagree** — structured consensus with explicit disagreement records
- **Cryptographic proof** — Ed25519 signatures on every deliberation round, verifiable offline
- **Lifecycle state** — whether the knowledge is current, stale, or has been superseded

**Design principle:** A Knowledge Unit must be independently verifiable by anyone who receives it, without contacting the issuing system. The verification protocol uses VOPRF (RFC 9497) for issuer-blind verification — the verifier never learns what it is verifying.

## 2\. Knowledge Unit Schema

The canonical representation is JSON. Implementations MUST produce objects conforming to this schema. Fields follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) requirement levels.

### 2.1. Core Fields

idstringMUST

Unique identifier. Format: `ku-{nanoid12}`. Immutable once assigned. Example: `ku-z36vuoreb2k3`

versionintegerMUST

Schema version. Current: `1`. Incremented on breaking schema changes.

canonical\_questionstringMUST

The definitive question this KU answers. Different phrasings of the same question SHOULD resolve to the same canonical form. See: [canonicalization](#canonicalization).

domainstringSHOULD

Topic classification. Values: `technology`, `science`, `health`, `policy`, `economics`, `agent_frameworks`, `agent_security`, `agent_governance`, `developer_tools`, `model_releases`, `research`.

### 2.2. Consensus Fields

consensus\_levelstringMUST

Level of agreement among participating models. Values: `unanimous`, `strong`, `split`, `divergent`. See [Section 4](#consensus).

agreedarray<string | object>MUST

Points where all participating models converge. Each entry is either a plain string claim or an object with `{ claim, confidence, evidence }`.

disputedarray<object>SHOULD

Points where models diverge. Each entry: `{ claim: string, positions: { [model]: string } }`. Preserves per-model reasoning.

synthesisstringSHOULD

Human-readable summary paragraph. Produced by the synthesis engine (Round 3). *Not part of the canonical record* — it is an editorial convenience, analogous to a legal headnote.

### 2.3. Provenance Fields

models\_usedarray<string>MUST

OpenRouter-format model identifiers used in this deliberation. Example: `["anthropic/claude-opus-4", "openai/gpt-4o", "google/gemini-2.5-pro", "x-ai/grok-3"]`

roster\_versionstringSHOULD

ISO date of the model roster snapshot. The roster evolves as new frontier models become available.

roster\_hashstringSHOULD

SHA-256 of sorted model identifiers. Enables roster version comparison.

process\_templatestringMUST

Deliberation process used. Default: `3-round`. Allows for future process evolution (e.g., `council`, `5-round`).

total\_tokensintegerMAY

Total tokens consumed across all rounds and models.

### 2.4. Lifecycle Fields

statusstringMUST

Current lifecycle state. Values: `active`, `stale`, `superseded`. See [Section 5](#lifecycle).

fresh\_untilstring (ISO 8601)MUST

Date after which this KU should be considered potentially stale. Default: 90 days from creation. Content-dependent: rapidly evolving topics may use shorter windows.

supersedesstring | nullMAY

ID of the KU this version replaces. Creates an immutable version chain.

parent\_ku\_idstring | nullMAY

For follow-up questions generated from a parent deliberation. Enables hierarchical knowledge structures.

### 2.5. Receipt Fields

receipt\_sigstring (hex)MUST

Aggregate Ed25519 signature over the canonical KU content. Produced by chaining per-round receipt hashes.

receipt\_kidstringMUST

Key identifier for the signing key. Enables key rotation without breaking verification of historical KUs.

receipt\_hashstring (hex)MUST

SHA-256 hash of all per-round receipt hashes chained in order. The chain is: `H(H(r1_1) || H(r1_2) || ... || H(r3_synth))`.

### 2.6. Complete Example

```
{
  "id": "ku-z36vuoreb2k3",
  "version": 1,
  "canonical_question": "Are large language models approaching a capability plateau?",
  "domain": "technology",
  "consensus_level": "strong",
  "agreed": [
    "Naive pretraining scaling is plateauing, but test-time compute is genuinely new",
    "The distinction matters: 'scaling' has multiple orthogonal dimensions"
  ],
  "disputed": [
    {
      "claim": "Whether reasoning chains represent true understanding vs. pattern matching",
      "positions": {
        "claude-opus-4": "Functional distinction is irrelevant if outputs are indistinguishable",
        "gpt-4o": "The distinction remains important for predicting failure modes"
      }
    }
  ],
  "synthesis": "Most models agree we are not hitting a hard ceiling on AI capability...",
  "models_used": ["anthropic/claude-opus-4", "openai/gpt-4o", "google/gemini-2.5-pro", "x-ai/grok-3"],
  "process_template": "3-round",
  "roster_version": "2026-04-01",
  "roster_hash": "a1b2c3d4...",
  "total_tokens": 18420,
  "status": "active",
  "fresh_until": "2026-07-01T00:00:00Z",
  "supersedes": null,
  "parent_ku_id": null,
  "receipt_sig": "3d2e1f0a...",
  "receipt_kid": "acta-prod-2026-001",
  "receipt_hash": "e4f5a6b7...",
  "published_at": "2026-04-01T14:30:00Z"
}
```

## 3\. Deliberation Process

The default process template (`3-round`) proceeds as follows:

| Round | Name | Participants | Purpose |
| --- | --- | --- | --- |
| **1** | Independent | 4+ models, blind to each other's identities | Each model answers the question independently. No anchoring bias. |
| **2** | Adversarial critique | Same models, assigned roles | Models critique Round 1 responses. Roles: *verifier*, *devil's advocate*, *synthesiser*, *clarity editor*. |
| **3** | Synthesis | Synthesis engine (typically one model) | Produces structured output: `agreed[]`, `disputed[]`, `consensus_level`, `follow_ups[]`. |

**Identity-blind Round 1:** During the first round, models see each other's responses labelled as "Response A", "Response B", etc. — never by model name. This prevents models from deferring to perceived authority (e.g., later models anchoring on GPT-4's answer). Model identities are revealed only after the deliberation is complete.

Each round response is individually signed:

```
// Per-round response (stored in ku_rounds table)
{
  "ku_id": "ku-z36vuoreb2k3",
  "round": 1,
  "slot": 2,
  "model": "openai/gpt-4o",
  "role": "independent",
  "content": "...",
  "tokens": 2340,
  "content_hash": "sha256:...",
  "receipt_sig": "ed25519:...",
  "receipt_kid": "acta-prod-2026-001"
}
```

## 4\. Consensus Levels

Consensus is determined structurally from the Round 3 synthesis, not editorially. The synthesis engine classifies based on agreement patterns across Round 1 and Round 2 responses.

| Level | Definition | Implication |
| --- | --- | --- |
| unanimous | All models converge on the same core claims with no substantive disagreement. | High confidence. Rare — genuine unanimity among diverse models is significant. |
| strong | Models agree on the core answer but differ on emphasis, framing, or edge cases. | Reliable. Disagreements are real but secondary. |
| split | Models agree on some claims but diverge substantively on others. | Treat with nuance. Both sides may have legitimate reasoning. The `disputed` array shows exactly where. |
| divergent | No meaningful common ground. Models reach fundamentally different conclusions. | Genuine uncertainty. This is valuable — it surfaces questions where the answer is not yet settled. |

**Consensus is not truth.** Strong consensus among 4 LLMs does not mean a claim is correct. It means 4 models with different training data, architectures, and potential biases independently arrived at the same conclusion. This is evidence, not proof. The consensus spectrum provides calibrated confidence, not certainty.

## 5\. Lifecycle Management

Knowledge Units have a defined lifecycle with three states:

Active

→

Stale

→

Superseded

active ⟶ stale (automatic, when fresh\_until passes) ⟶ superseded (when a new KU is produced with supersedes = this KU's id)

### Operations

| Operation | Trigger | Effect |
| --- | --- | --- |
| **KEEP** | Re-deliberation confirms same conclusions | Extends `fresh_until`; status remains `active` |
| **UPDATE** | Re-deliberation refines but doesn't contradict | New KU with `supersedes` pointing to old; old becomes `superseded` |
| **SUPERSEDE** | Re-deliberation contradicts previous consensus | Same as UPDATE; old KU's `status` set to `superseded` |
| **MERGE** | Two KUs cover overlapping questions | New KU with both questions as context; both old KUs become `superseded` |
| **ARCHIVE** | Question is no longer relevant | Status set to `superseded` with no replacement. Receipts remain verifiable. |

**Immutability:** A published KU is never modified in place. All "changes" produce new KUs with `supersedes` links. This ensures that receipts signed against the original content remain valid forever.

## 6\. Receipt Binding

Every Knowledge Unit is anchored by a chain of Ed25519 receipts following [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/).

### Receipt chain construction

```
// For a 3-round deliberation with 4 models:
// R1: 4 independent responses → 4 receipts
// R2: 4 critique responses → 4 receipts
// R3: 1 synthesis → 1 receipt
// Total: 9 round receipts + 3 round-level hashes + 1 aggregate

receipt_hash = SHA-256(
  SHA-256(r1_slot1.sig || r1_slot2.sig || r1_slot3.sig || r1_slot4.sig) ||
  SHA-256(r2_slot1.sig || r2_slot2.sig || r2_slot3.sig || r2_slot4.sig) ||
  SHA-256(r3_synthesis.sig)
)
```

The aggregate `receipt_sig` is produced by signing the `receipt_hash` with the gateway's Ed25519 private key. This creates a single verifiable signature that attests to the entire deliberation chain.

### Verification

```
# Verify any Knowledge Unit receipt offline
npx @veritasacta/verify receipt.json

# Exit codes (3-way contract):
# 0 = valid     (receipt is authentic and untampered)
# 1 = tampered  (receipt exists but signature fails)
# 2 = error     (could not complete verification)
```

**Issuer-blind verification:** The verification protocol uses VOPRF (RFC 9497) so the verifier never learns what it is verifying. You can prove a receipt is valid without revealing its contents to the verification service. This matters when deliberation content contains sensitive topics.

## 7\. Comparison: Single-Model Wiki vs. Knowledge Units

The [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) popularised by Karpathy solves content maintenance. Knowledge Units extend this with provenance and verification.

| Feature | Single-Model Wiki | Acta Knowledge Unit |
| --- | --- | --- |
| Format | Markdown + frontmatter | JSON with formal schema |
| Provenance | Git history | ✓ Ed25519 receipts per round |
| Multi-perspective | ✗ Single LLM curator | ✓ 4+ models × 3 adversarial rounds |
| Contradiction handling | ~ LLM flags contradictions | ✓ Structured `disputed[]` with per-model positions |
| Canonicalization | Implicit (file naming) | ✓ Explicit `canonical_question` + hierarchical inheritance |
| Freshness | Content hash / git blame | ✓ `fresh_until` + `supersedes` chain |
| Offline verifiability | ✗ None | ✓ `npx @veritasacta/verify` |
| Consensus model | ✗ N/A (single curator) | ✓ unanimous / strong / split / divergent |
| Citable identity | ~ File path | ✓ `ku-{id}` with version chain |
| Standards basis | ✗ None | ✓ IETF Internet-Draft ([receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)) |

**Not a replacement.** The LLM Wiki pattern is excellent for personal knowledge management. Knowledge Units solve a different problem: producing *shared*, *verifiable* knowledge that multiple parties can trust without trusting each other.

## 8\. Verification

Three verification paths are available:

| Method | Command / URL | Trust model |
| --- | --- | --- |
| **CLI (offline)** | `npx @veritasacta/verify receipt.json` | Zero trust — runs locally, checks Ed25519 signature |
| **Browser** | [acta.today/v/{ku-id}](https://acta.today/v/%7Bku-id%7D) | Verifier runs client-side; trusts the API for receipt data |
| **VOPRF (blind)** | Programmatic via `@veritasacta/verify-voprf` | Issuer-blind — verifier never learns what is being verified |

## 9\. IETF Standardisation

The Knowledge Unit specification is being formalized as an IETF Internet-Draft:

- **draft-farley-acta-signed-receipts** — [Published](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/). Defines the receipt format, signature algorithm, and verification protocol.
- **draft-farley-acta-knowledge-units** — *In preparation.* Defines the KU schema, lifecycle, consensus model, and receipt binding described in this specification.

Implementations are encouraged to follow this specification. The verifier CLI ([Apache-2.0](https://www.npmjs.com/package/@veritasacta/verify)) and the gateway ([MIT](https://github.com/scopeblind/scopeblind-gateway)) are the reference implementations.