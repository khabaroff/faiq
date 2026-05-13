---
title: Curated Context Engineering VS LLM Wiki Two Approaches To Knowledge
slug: 2026-04-12-curated-context-engineering-vs-llm-wiki_-two-approaches-to-knowledge-
source_url: https://agentarchitectures.substack.com/p/curated-context-engineering-vs-llm-wiki
source_type: article
fetched_at: 2026-05-13
lang: en
---

## Abstract

As AI agent systems take on increasingly complex domain work — debugging distributed systems, analyzing large codebases, performing root-cause analysis across multiple evidence streams — they need reliable access to domain knowledge that exceeds what fits in a single context window. Two fundamentally different architectures have emerged for this problem:

1\. **LLM Wiki** — an LLM actively maintains a living, cross-linked knowledge base, integrating new information by revising existing entries.

2\. **Curated Context Engineering (CCE)** — human-curated, section-loadable knowledge files designed for selective on-demand loading within strict context window budgets.

This article provides a detailed comparison grounded in production experience, covering architecture, scaling behavior, failure modes, maintenance costs, and the conditions under which each approach excels or collapses.

## 1\. The Problem Both Approaches Solve

Modern LLMs have a fundamental limitation: their parametric knowledge (what’s baked into the weights) is frozen at training time, can’t be audited, and can’t be edited. When building an agent system for a specific domain — a large codebase, an enterprise product, a specialized engineering discipline — the agent needs access to knowledge that is:

\- **Domain-specific**: Internal architectures, proprietary protocols, undocumented behaviors

\- **Current**: Reflecting the latest code, specs, and lessons learned

\- **Structured**: Organized for efficient retrieval, not just dumped into context

\- **Trustworthy**: Traceable to sources, auditable, correctable

Standard Retrieval-Augmented Generation (RAG) partially addresses this by retrieving relevant document chunks at query time. But RAG treats documents in isolation — chunks are connected only by retrieval accident. There’s no structural understanding of how pieces of knowledge relate to each other.

Both the LLM Wiki and Curated Context Engineering go beyond RAG to provide structured, relational domain knowledge. They diverge sharply in \*how\* that structure is created and maintained.

## 2\. Architecture Overview

### LLM Wiki Architecture

The LLM Wiki pattern, popularized by Andrej Karpathy’s “second brain” concept \[1\] and analyzed in depth by the \*Extended Brain\* newsletter \[2\], structures knowledge into three layers:

```markup
knowledge-base/
├── SCHEMA.md              # Layer 3: Rules for formatting and behavior
├── index.md               # Master navigation hub
├── log.md                 # Ingestion history
│
├── sources/               # Layer 1: IMMUTABLE — LLM reads, never writes
│   ├── S-001-design-spec.md
│   ├── S-002-postmortem.md
│   └── ...
│
├── concepts/              # Layer 2: LLM-MAINTAINED WIKI
│   ├── C-001-topic-a.md          # Cross-linked entries with
│   ├── C-002-topic-b.md          # frontmatter, provenance,
│   └── ...                       # and bidirectional references
│
├── patterns/
│   ├── P-001-pattern-a.md
│   └── ...
│
└── scripts/
    └── lint-wiki.py       # Automated health checks
```

**Core operations:**

\- **Ingest**: New material doesn’t just get filed — the LLM reads it alongside existing entries, asks “what does this change about what we know?”, and updates all affected entries. Integration, not accumulation.

\- **Lint**: Periodic audit that finds orphan pages, missing connections, contradictions, and stale content.

\- **Navigate**: Structured querying through metadata, tags, and explicit relationships.

### Curated Context Engineering (CCE) Architecture

CCE structures knowledge as human-curated, section-loadable files optimized for selective injection into an LLM’s context window:

```markup
domain-knowledge/
├── MODULE_INDEX.md              # Compact routing map (~1,500 tokens)
│
├── expert/
│   └── SKILL.md                 # Agent operating protocol
│
├── modules/                     # One file per domain module
│   ├── component-a/
│   │   └── component-a.skill.md # Section-loadable knowledge
│   ├── component-b/
│   │   └── component-b.skill.md
│   └── ...
│
├── workflows/                   # Task-type process templates
│   ├── debugging.workflow.md
│   ├── feature.workflow.md
│   └── ...
│
├── workers/                     # Search worker templates
│   ├── code-search.worker.md
│   └── verification.worker.md
│
└── investigation-memory/        # Compressed learned patterns
    └── MEMORY.md                # Flat index, max 200 lines
```

**Core operations**:

\- **Route**: On every invocation, the agent reads the MODULE\_INDEX (always loaded, ~1,500 tokens) and identifies which module SKILL files are relevant. Loads only the needed sections — not entire files.

\- **Cache**: The agent’s context is split into a static prefix (cached across turns) and a dynamic suffix (per-turn). Multi-turn conversations reuse the cached prefix.

\- **Verify**: Knowledge claims are cross-referenced against live systems (code search, API calls) before being asserted as facts.

\- **Learn**: After completing an investigation, compress the key findings into a few-line memory entry for future hypothesis priming.

### Side-by-Side Structural Comparison

```markup
| Dimension                     | LLM Wiki                                        | CCE                                          |
| ----------------------------- | ----------------------------------------------- | -------------------------------------------- |
| **Who maintains knowledge**   | LLM (with human oversight)                      | Human (with LLM assistance)                  |
| **Knowledge structure**       | Cross-linked graph                              | Section-loadable flat files                  |
| **Update model**              | Integration — new info revises existing entries | Accumulation — entries updated independently |
| **Loading strategy**          | Load by query relevance                         | Load by module routing + section selection   |
| **Context cost per query**    | Variable, grows with knowledge size             | Bounded, controlled by section selection     |
| **Cross-entry relationships** | Explicit bidirectional links                    | Centralized interaction map                  |
| **Error propagation**         | Spreads through integration                     | Contained within single file                 |
| **Provenance**                | Tracked per-claim to immutable sources          | Optional, per-section                        |
| **Maintenance trigger**       | Ingest/lint operations (can be automated)       | Human-initiated reviews                      |
```

## 3\. The Filing Clerk vs. the Librarian

The framing that best captures the philosophical difference comes from the **Extended Brain** essay \[2\]:

> “There is a filing clerk and there is a librarian. The filing clerk takes documents as they arrive, assigns each one a number, and puts it in a drawer. The librarian reads the document, then walks the stacks and updates everything the document changes.”

The LLM Wiki aspires to be the librarian: each new piece of information is traced through existing knowledge, and all affected entries are updated. Knowledge compounds through integration.

CCE is a **disciplined filing clerk with an excellent index**. Documents are filed carefully, organized into sections, and tagged for retrieval. But one document’s arrival doesn’t automatically trigger updates to other documents. The human curator decides when and how to propagate changes.

Neither is inherently superior. The question is which model’s failure modes are more tolerable for your domain.

> “The filing clerk doesn’t have these problems only because the filing clerk never attempts integration in the first place. The absence of ambition is not the same as correctness.”
> 
> — **Extended Brain** \[2\]

But the inverse is equally true: **the presence of ambition is not the same as improvement**. Integration that introduces errors is worse than isolation that doesn’t.

## 4\. When Each Approach Excels

### LLM Wiki Excels When:

**The knowledge domain is broad and loosely coupled.** A team wiki covering engineering practices, onboarding guides, API documentation, and postmortems benefits from integration. When a postmortem reveals that payment retries interact badly with auth rate-limiting, the wiki updates both the payments page and the auth page. No single person would think to make both updates.

**Cross-domain insight is the primary value.** If the goal is to discover relationships between topics that no one has explicitly connected, the LLM’s ability to trace implications across entries is the core feature. Research synthesis, competitive analysis, and knowledge discovery workflows benefit most.

**The knowledge base serves multiple use cases.** When both humans (browsing via Obsidian or a web interface) and agents (querying via structured metadata) consume the same knowledge, the wiki’s dual interface — narrative for humans, structured for agents — justifies the overhead.

**Accuracy is important but not safety-critical.** The wiki can self-correct through lint operations, but errors can propagate before being caught. If a wrong answer means “the agent gives a suboptimal suggestion” rather than “an engineer acts on a false root-cause diagnosis,” the risk/reward favors integration.

### CCE Excels When:

**The knowledge domain is deep and tightly coupled.** When modules interact in complex, interdependent ways — where a wrong claim about one component’s behavior directly affects reasoning about three others — you want errors to stay contained. A wrong SKILL file entry for Component A shouldn’t silently propagate to Components B, C, and D.

**Context window budget is the binding constraint.** When every token matters — because the agent also needs to hold MCP search results, worker outputs, user context, and multi-turn history — you can’t afford wiki overhead. CCE’s section-level loading and token-budget discipline keep domain knowledge costs bounded and predictable.

**Precision matters more than coverage.** In root-cause analysis, debugging, and engineering investigation, a small amount of verified knowledge is far more valuable than a large amount of integrated-but-possibly-stale knowledge. CCE’s “verify against live code before asserting” principle prioritizes precision.

**The domain changes at code speed.** When the underlying system evolves with every code commit, knowledge that was true last week may be false today. CCE handles this by treating SKILL files as pointers to investigation strategies (”search for X in directory Y”) rather than assertions of truth. The agent always verifies against the current state.

**You need auditability.** When an agent’s conclusion will be acted upon by engineers — filing a bug, proposing a fix, triggering a failover procedure — you need to trace exactly which knowledge led to that conclusion. CCE’s explicit “I loaded Section X of Module Y, then searched for Z” is more auditable than the wiki’s diffuse cross-referencing.

## 5\. Failure Modes

### LLM Wiki: The False Coherence Problem

The most dangerous failure mode of integrated knowledge systems is **false coherence** — an error that, once integrated, spreads by becoming internally consistent \[2\].

**How it happens:**

1\. An error enters the system (wrong fact, misread spec, outdated information)

2\. The ingest operation integrates the error into related entries

3\. Related entries update to be consistent with the error

4\. Multiple entries now mutually reinforce the false belief

5\. Lint finds no contradictions — entries agree with each other

6\. The system has achieved internal consistency around a false belief

\*\*Why it’s hard to detect:\*\* Traditional quality checks (contradiction detection, orphan finding) fail because the entries \*agree\*. The error is only discoverable by comparison against external ground truth — which may not be readily available.

**Example:**

```markup
Step 1: Wiki entry incorrectly states that Component X acquires Lock A
        before Lock B (actually the reverse)

Step 2: Ingest runs. The "Lock Ordering" pattern entry is updated to
        include Component X's (incorrect) ordering.

Step 3: The "Debugging Deadlocks" workflow references the pattern entry.

Step 4: Three entries now consistently describe the wrong lock order.
        They cite each other. Lint finds no contradictions.

Step 5: Agent uses this knowledge during a root-cause analysis.
        Produces a confident but incorrect diagnosis.
```

**Mitigation strategies:**

\- Maintain an immutable source layer — original documents that the LLM cannot modify, used as ground truth for re-verification

\- Track provenance per-claim (not just per-entry) — “this claim came from Source X, §3.2”

\- Implement confidence decay — reduce confidence when a claim is only supported by internal wiki citations, not external sources

\- Periodic adversarial review — dedicated process that challenges integrated beliefs against external evidence

### CCE: The Staleness Problem

CCE’s primary failure mode is **silent staleness** — knowledge that was correct when curated but has drifted from reality without any visible signal.

**How it happens:**

1\. A SKILL file is written based on a spec and code inspection

2\. The code evolves (refactors, new features, bug fixes)

3\. The spec may be updated, but nobody tells the agent system

4\. The SKILL file’s claims gradually diverge from reality

5\. No lint or integration process detects the drift

6\. Agent reasons from outdated knowledge

**Why it’s hard to detect:** Unlike the wiki, where errors propagate visibly (to other entries), CCE errors are **silently contained**. The wrong information sits in one file, never triggering updates or contradictions elsewhere. It’s only discovered when the agent uses it and gets a wrong answer.

**Mitigation strategies:**

\- Structured staleness scoring — track when each SKILL file section was last verified, with escalating risk levels

\- “Verify before asserting” protocol — the agent cross-references SKILL file claims against live code/systems before stating them as facts

\- Investigation memory feedback — when a SKILL-file-primed hypothesis turns out wrong, flag the specific section for review

\- Immutable source snapshots — store the spec version each SKILL section was based on, enabling diff-based staleness detection

### Comparative Failure Analysis

```markup
| Failure Mode                     | LLM Wiki                                                          | CCE                                                  |
| -------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------- |
| **Error propagation**            | High — errors spread through integration                          | Low — errors contained in single file                |
| **Silent staleness**             | Medium — lint catches some, misses coherent errors                | High — no automatic detection                        |
| **Confident wrong answers**      | High — multiple cross-referencing entries create false confidence | Medium — single-source claims are easier to question |
| **Recovery difficulty**          | Hard — must trace all entries touched by the error                | Easy — update one file                               |
| **Detection mechanism**          | External ground truth comparison                                  | Live system verification                             |
| **Blast radius of single error** | Multiple entries, potentially the whole graph                     | One module's knowledge                               |
```

## 6\. Scaling Behavior as Knowledge Grows

This is where the two approaches diverge most dramatically.

### LLM Wiki Scaling Curve

```markup
Knowledge Quality
    │
    │     ╭──── Sweet spot (50-200 entries)
    │    ╱ ╲
    │   ╱   ╲──── Diminishing returns
    │  ╱     ╲
    │ ╱       ╲── False coherence risk zone
    │╱         ╲
    └─────────────────────── Entries
         50   200   500   1000+
```

**Small scale (10-50 entries):** Wiki shines. Cross-linking is manageable. Ingest operations trace implications quickly. Lint is fast and cheap. The compounding benefit of integration is felt immediately.

**Medium scale (50-200 entries):** Sweet spot. Enough knowledge for meaningful cross-domain insights. Lint operations catch real issues. Maintenance is manageable with regular lint cycles.

**Large scale (200-500 entries):** Strain emerges. Contradiction detection becomes O(n²) in the number of claims. Ingest operations that need to “read existing entries” now face hundreds of pages. The LLM’s ability to trace implications degrades as the knowledge graph grows beyond what fits in a single context window. Lint operations become expensive (50,000-100,000+ tokens per full pass).

**Very large scale (500+ entries):** The wiki’s fundamental assumption — that the LLM can hold enough of the knowledge graph in context to make correct integration decisions — breaks down. Ingest operations become partial and potentially inconsistent. False coherence risk grows because the LLM can’t see enough of the graph to detect contradictions.

### CCE Scaling Curve

```markup
Knowledge Quality
    │
    │          ╭── Plateau (quality bounded by curation effort)
    │         ╱
    │        ╱
    │       ╱
    │      ╱
    │     ╱── Linear growth (each module adds value independently)
    │    ╱
    │   ╱
    └─────────────────────── Modules
         5    15    30    50+
```

**Small scale (1-5 modules):** CCE requires more upfront effort than a wiki (human curation is slower than LLM ingest). Initial setup cost is higher.

**Medium scale (5-15 modules):** CCE hits its stride. The MODULE\_INDEX routes efficiently. Section-level loading keeps context costs bounded. Each new module adds predictable value without affecting existing modules.

**Large scale (15-30 modules):** The MODULE\_INDEX grows but remains manageable (~2,000-3,000 tokens). Cross-module interaction maps become harder to maintain manually. The human curation bottleneck becomes the primary constraint — there’s more knowledge to maintain than a single curator can keep current.

**Very large scale (30+ modules):** The routing problem gets harder. The MODULE\_INDEX may need hierarchical organization (domain → sub-domain → module). But the context window cost per query remains bounded — you still load only 2-3 module sections per task, regardless of how many modules exist. \*\*Scalability is in the read path, not the write path.\*\*

### Key Scaling Difference

The LLM Wiki’s cost scales with **total knowledge base size** (because ingest and lint must consider the whole graph). CCE’s cost scales with **query-relevant knowledge size** (because you only load what you need). As the knowledge base grows past a few hundred entries, this difference becomes decisive.

```markup
| Scale Metric                  | LLM Wiki                                            | CCE                                               |
| ----------------------------- | --------------------------------------------------- | ------------------------------------------------- |
| **Per-query context cost**    | Grows with KB size (more cross-refs to load)        | Bounded (load 2-3 sections regardless of KB size) |
| **Ingest cost per new entry** | Grows with KB size (must check all related entries) | Constant (write one file, update index)           |
| **Lint cost per cycle**       | O(n²) for contradiction detection                   | O(n) for staleness checks                         |
| **Error blast radius**        | Grows with integration density                      | Constant (one file)                               |
| **Quality ceiling**           | Bounded by LLM's integration accuracy at scale      | Bounded by human curation bandwidth               |
```

## 7\. Context Window Economics

For AI agent systems where the LLM’s context window is a precious, limited, temporary workspace, the token economics of each approach matter enormously.

### LLM Wiki: Variable and Growing

A wiki entry for a domain component might include:

\- Frontmatter with metadata, tags, and cross-links (~100 tokens)

\- Main content (~500-1,000 tokens)

\- Provenance links per section (~50-100 tokens)

\- Append-only update history (~100-500 tokens, growing over time)

\- Bidirectional relationship references (~50-200 tokens)

**Total per entry: ~800-1,900 tokens**, growing over time as updates accumulate.

Loading three relevant entries plus the index for a single query: **~4,000-8,000 tokens** of domain knowledge.

As entries accumulate update notes and cross-references, this cost grows even for the same query. An entry that started at 800 tokens on day 1 might be 1,500 tokens six months later due to append-only updates and new cross-links.

### CCE: Bounded and Predictable

A CCE module SKILL file is designed for section-level loading:

\- Architecture section: ~500 tokens

\- Key Code Paths section: ~300 tokens

\- Common Failure Modes section: ~400 tokens

\- Full file (all sections): ~1,500-2,500 tokens

But you rarely load the full file. For a focused question, load one section (~~500 tokens). For an investigation, load 2-3 sections from 2-3 modules (~~2,000-3,000 tokens). For broad architectural questions, load full files (~4,000-5,000 tokens).

**Context cost is a function of the question, not the knowledge base size.** Adding a 20th module SKILL file doesn’t increase the cost of a query about module 3.

### Prompt Cache Economics

Both approaches benefit from prompt caching (available from providers like Anthropic and OpenAI), where a static prefix is cached and reused across turns at ~10% of the original cost. But CCE is specifically designed for this:

**CCE cache architecture:**

```markup
┌─ STATIC PREFIX (cached across turns) ─────────────┐
│  Agent operating protocol       ~800-1,400 tokens  │
│  MODULE_INDEX                   ~1,500 tokens       │
│  Workflow templates             ~1,000-2,000 tokens  │
│  Total:                         ~3,300-4,900 tokens  │
└─────────────── CACHE BOUNDARY ─────────────────────┘
┌─ DYNAMIC SUFFIX (per turn) ────────────────────────┐
│  Loaded SKILL sections          ~500-2,600 tokens   │
│  Investigation memory           ~500 tokens          │
│  Search results                 varies               │
└────────────────────────────────────────────────────┘
```

Turn 1 pays full price. Turn 2+ reuses the static prefix at ~10%, saving ~3,000-4,400 tokens per turn. Over a 5-turn investigation, the savings compound to ~12,000-17,600 tokens.

The LLM Wiki can also use prompt caching, but its variable-cost entries make the cache boundary harder to define. Which entries go in the static prefix? The index (yes), but module entries change based on the query, and their growing size makes the prefix less stable.

## 8\. Maintenance Burden

### LLM Wiki Maintenance

**Automated operations:**

\- **Ingest**: When new material arrives, the LLM reads it alongside existing entries, determines what changes, and updates affected entries. Cost: proportional to the number of affected entries (typically 3-10 entries per ingest, at ~2,000-5,000 tokens each for reading + ~500-1,000 tokens each for writing).

\- **Lint**: Periodic full-graph audit. At 100 entries, a lint pass might cost ~50,000-80,000 tokens. At 500 entries, ~200,000-400,000 tokens.

**Human operations:**

\- Review ingest proposals (did the LLM integrate correctly?)

\- Validate lint findings (are flagged contradictions real?)

\- Supply new source material

\- Resolve false coherence when detected (trace provenance, re-synthesize)

**Maintenance cost curve:** Superlinear in the number of entries. Each new entry potentially affects existing entries during ingest and increases lint cost.

### CCE Maintenance

**Human operations:**

\- Write and review SKILL files (primary cost — typically 1-3 hours per module)

\- Update MODULE\_INDEX when modules are added or restructured

\- Review investigation memory periodically (consolidate, prune)

\- Verify SKILL file accuracy against live systems (staleness checks)

**Automated operations:**

\- Staleness scoring (compare last-verified dates against thresholds)

\- Diff detection (compare source snapshots against upstream, if using immutable source layer)

**Maintenance cost curve:** Linear in the number of modules. Each new module requires its own SKILL file but doesn’t affect existing files.

### Comparative Maintenance Summary

```markup
| Maintenance Task               | LLM Wiki                                              | CCE                                         |
| ------------------------------ | ----------------------------------------------------- | ------------------------------------------- |
| **Adding new knowledge**       | LLM does integration (fast, but error-prone at scale) | Human writes SKILL file (slow, but precise) |
| **Detecting staleness**        | Lint + external validation                            | Staleness scoring + live verification       |
| **Fixing errors**              | Trace all affected entries, re-synthesize             | Update one file                             |
| **Handling contradictions**    | Lint may detect — or false coherence hides them       | Manual review — or never detected           |
| **Cost per new module**        | ~5,000-15,000 tokens (ingest + lint)                  | ~3-5 hours human time                       |
| **Cost per maintenance cycle** | ~50,000-400,000 tokens (full lint)                    | ~30 min human review per module             |
| **Scales with**                | Total entry count (superlinear)                       | Module count (linear)                       |
```

## Hybrid: Taking the Best of Both

The strongest architecture borrows selectively from each approach without taking on the full overhead of either.

### Start with CCE, Add Targeted Wiki Elements

**Immutable source layer (from LLM Wiki, zero query-time cost):**

When the agent fetches an external document (spec, design doc, API reference) via tool call, save a frozen snapshot with a date stamp. The agent never loads these at query time — they exist only for provenance and staleness detection.

```markup
sources/
├── component-a-design/
│   ├── v1-2026-04-02.md    # Original fetch
│   ├── v2-2026-07-15.md    # Re-fetch after change detected
│   └── changelog.md        # Diff summary between versions
```

Cost: disk storage only. Zero context tokens during normal operation.

**Provenance links in SKILL files (from LLM Wiki, ~15 tokens per section):**

Add a single line per SKILL file section tracing it to the source snapshot:

```markup
## Architecture
Component A intercepts write operations and buffers them...
(Source: v2-2026-07-15.md §3.2, verified against code 2026-07-20)
```

Cost: ~15 tokens per loaded section. For 3 sections, ~45 tokens total.

**Richer investigation memory (from LLM Wiki’s structured entries, ~100 extra tokens):**

Keep the flat, compressed format but add confidence and feedback fields:

```markup
## 2026-04-02: ISSUE-12345 — Lock ordering race in Component A
- Modules: Component A (bug origin), Component B (victim)
- Pattern: lock-ordering
- Key location: component_a.c:flush_handler():142
- Search path: search "flush_handler" → "defer_op" → "slot_reclaim"
- Confidence: high (verified against code + spec source v1)
- Hypothesis-correct: yes
```

Cost: ~100 extra tokens when loaded. Enables confidence decay and hypothesis accuracy tracking.

**Structured staleness scoring (from LLM Wiki’s lint concept, zero query-time cost):**

Track verification dates per SKILL file section in a status file:

```markup
| Module | Section | Last Verified | Source Version | Risk |
|---|---|---|---|---|
| Component A | Architecture | 2026-07-20 | v2 | low |
| Component A | Code Paths | 2026-06-15 | v1 | medium (>30d) |
| Component B | Failure Modes | 2026-03-01 | v1 | high (>90d) |
```

Cost: zero at query time. Used only during maintenance sessions to prioritize what to re-verify.

### What NOT to Borrow

\- **Automated cross-entry integration.** When Component A’s SKILL file changes, do NOT automatically update Components B and C. Flag it: “Component A Architecture updated — Components B and C interaction map may need manual review.” Let the human decide.

\- **Full lint operations.** At CCE scale, a simple staleness table replaces the need for expensive graph-wide lint. The O(n²) contradiction detection in a full wiki lint is overkill when errors are contained within single files.

\- **Append-only update history.** The wiki’s Luhmann-inspired append-only updates (”Update Oct 2026: we no longer recommend...”) are valuable for long-lived knowledge bases where historical context matters. For SKILL files that are meant to reflect \*current\* truth, clean overwrites with a Git history trail are simpler and don’t accumulate context window debt.

## 10\. Decision Framework

### Use LLM Wiki When:

```markup
| Condition                                                               | Why It Favors Wiki                                                                      |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Knowledge domain is **broad** (50+ loosely-coupled topics)              | Integration discovers cross-domain connections                                          |
| Primary value is **insight discovery**                                  | LLM connects dots humans wouldn't                                                       |
| Error cost is **moderate** (suboptimal suggestion, not wrong diagnosis) | False coherence risk is tolerable                                                       |
| Multiple consumers (humans + agents) browse the same KB                 | Wiki's dual interface justifies overhead                                                |
| Knowledge changes **slowly** (monthly, not daily)                       | Ingest/lint cycles can keep up                                                          |
| You have **token budget flexibility**                                   | Variable context cost is acceptable                                                     |
| Team has **multiple contributors** adding material                      | LLM integration scales better than asking each contributor to update all affected files |
```

### Use CCE When:

```markup
| Condition                                                             | Why It Favors CCE                                             |
| --------------------------------------------------------------------- | ------------------------------------------------------------- |
| Knowledge domain is **deep** (few tightly-coupled components)         | Error containment matters more than cross-linking             |
| Primary value is **precision** (correct diagnosis, not broad insight) | Verified, section-loaded knowledge beats integrated-but-stale |
| Error cost is **high** (engineers act on conclusions)                 | False coherence risk is intolerable                           |
| Single consumer (the agent system)                                    | No need for human-browsable narrative                         |
| Knowledge changes **at code speed** (daily commits)                   | SKILL files + live verification adapt faster than ingest/lint |
| Context window budget is **tight**                                    | Bounded, predictable token cost per query                     |
| Single domain expert curates                                          | Human curation quality beats LLM integration quality          |
```

### Use Hybrid When:

```markup
| Condition                                                        | What to Add                                                                     |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| CCE is your base but you need **provenance**                     | Add immutable source layer + provenance links                                   |
| CCE is your base but you need **staleness detection**            | Add structured staleness scoring                                                |
| LLM Wiki is your base but you need **precision for some topics** | Curate critical entries as section-loadable files, exempt from auto-integration |
| Either base, but you need **learning from past work**            | Add investigation memory with confidence tracking                               |
```

## 11\. Long-Term Outlook

### Context Windows Will Grow — Does That Change the Calculus?

Context windows have grown from 4K tokens (2023) to 200K+ tokens (2026), and will likely continue growing. This might seem to favor the LLM Wiki: if you can fit the whole knowledge base in context, why optimize for selective loading?

Three reasons CCE remains relevant even with massive context windows:

1\. **Attention degradation is real.** Empirical evidence shows that LLMs perform worse on information in the middle of very long contexts (”lost in the middle” effect \[4\]). Selectively loading 3,000 tokens of highly relevant knowledge into a 200K window outperforms dumping 50,000 tokens of mixed-relevance wiki entries.

2\. **Cost scales with context size.** Larger context windows are more expensive per-query. Loading 50K tokens of wiki at $3/M tokens costs 5x more than loading 10K tokens of curated sections. Over thousands of queries, this compounds.

3\. **The knowledge base grows faster than context windows.** A mature enterprise domain knowledge base can reach millions of tokens. Context windows will not grow fast enough to make “just load everything” viable for large domains.

### Will Agents Get Better at Integration?

As LLMs improve at multi-document reasoning, the LLM Wiki’s integration quality will improve. But the false coherence problem is fundamental — it’s not a limitation of current models but an inherent property of integrated knowledge systems. Better models make integration more \*consistent\*, but consistency is exactly what makes false coherence dangerous.

### The Convergence Hypothesis

The most likely long-term outcome is convergence: wiki-style systems will adopt more CCE-like discipline (section-level loading, context budgets, selective caching), and CCE systems will adopt more wiki-like features (automated staleness detection, limited cross-referencing, richer provenance). The hybrid approach described in Section 9 is a preview of this convergence.

## 12\. Credits and References

### Primary References

\[1\] **Andrej Karpathy**, “Second Brain / LLM Wiki” concept. Originally shared as a GitHub Gist describing a system where an LLM maintains a personal knowledge base as structured markdown files.

\- GitHub Gist: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

\[2\] **Extended Brain** (Substack newsletter), “The Wiki That Thinks: Ingest, Lint, and the Question of What Knowledge Is For.” An analytical essay that examined the LLM Wiki pattern in depth, introduced the “filing clerk vs. librarian” framing, identified the false coherence problem, and proposed the three-layer architecture (immutable sources, LLM-maintained wiki, schema) as a mitigation. The false coherence analysis and immutable source layer concepts referenced throughout this article originate from this essay.[Extended\_Brain](https://extendedbrain.substack.com/p/the-wiki-that-thinks-ingest-lint?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

[

There is a filing clerk and there is a librarian. The filing clerk takes documents as they arrive, assigns each one a number, and puts it in a drawer. The librarian reads the document, then walks the stacks and updates everything the document changes. The filing clerk is faster. The librarian is rarer…

](https://extendedbrain.substack.com/p/the-wiki-that-thinks-ingest-lint?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

\[3\] **Anthropic**, “Building Effective Agents” (2024). Canonical reference for agent architecture patterns including the augmented LLM primitive (retrieval + tools + memory), prompt chaining, orchestrator-worker separation, and the principle that simpler architectures should be preferred over complex ones.

\- URL: [https://www.anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)

\[4\] **Liu et al.**, “Lost in the Middle: How Language Models Use Long Contexts” (2023). Empirical study demonstrating that LLMs perform significantly worse when relevant information is placed in the middle of long contexts versus the beginning or end.

\- arXiv: [https://www.anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)

### Additional Influences

\[5\] **Harrison Chase / LangChain**, multi-agent architecture benchmarks and the observation that single-agent performance degrades past 5-10 tools, motivating multi-agent decomposition. Blog posts and conference talks (2025-2026).

\[6\] **Niklas Luhmann**, Zettelkasten method. The append-only, never-overwrite approach to knowledge management that inspired the LLM Wiki’s update philosophy. Luhmann maintained ~90,000 index cards over 40 years using this system.

\[7\] **Paul Iusztin / ZTRON**, “How Does Memory for AI Agents Work?” (DecodingAI Substack, 2025). Documented a production team’s pivot from complex multimodal RAG to Context-Augmented Generation (CAG) with smart context window engineering for bounded domains — an approach closely aligned with CCE’s philosophy.[Decoding AI Magazine](https://www.decodingai.com/p/how-does-memory-for-ai-agents-work?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

[

Welcome to the AI Agents Foundations series: A 9-part journey from Python developer to AI Engineer. Made by busy people. For busy people…

](https://www.decodingai.com/p/how-does-memory-for-ai-agents-work?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

\[8\] **OpenAI**, “Agents” documentation (2025-2026). Formalized hierarchical agent delegation via \`agent.as\_tool()\` pattern and contributed to the industry convergence on orchestrator-worker separation.

\[9\] **Data Processing Inequality** (Information Theory). The mathematical principle underpinning the immutable source layer: no post-processing of data can increase its mutual information with the original source. Each act of synthesis can only reduce or preserve ground truth, never add to it. Referenced in \[2\].

### Terminology

\- **Curated Context Engineering (CCE)**: Term introduced in this article to describe the pattern of human-curated, section-loadable, context-budget-aware domain knowledge files. The approach draws on the broader concept of “context engineering” as discussed by multiple practitioners in the AI agent community (2025-2026), which reframes the challenge from “write better prompts” to “manage the entire information pipeline.”

\- **LLM Wiki**: Term from Karpathy \[1\], analyzed in \[2\]. Refers specifically to the pattern where an LLM actively maintains and integrates a structured knowledge base, as opposed to passively retrieving from it.

\- **False Coherence**: Term from \[2\]. The anti-pattern where an integrated knowledge system achieves internal consistency around a false belief.

### License Note

This analysis is the author’s original work based on publicly available sources cited above. The architectural patterns, concepts, and frameworks referenced are attributed to their respective creators. The comparative analysis, the CCE naming/framework, and the hybrid recommendations are original contributions.

### Appendix A: Quick-Reference Comparison Table

```markup
| Dimension                            | LLM Wiki                                     | CCE                                          | Hybrid (CCE + Selective Wiki)                      |
| ------------------------------------ | -------------------------------------------- | -------------------------------------------- | -------------------------------------------------- |
| **Setup cost**                       | Low (LLM does ingest)                        | High (human curation)                        | High (human curation + source layer)               |
| **Per-query token cost**             | Variable, growing                            | Bounded, predictable                         | Bounded + ~60 tokens provenance                    |
| **Knowledge quality at small scale** | High (integration finds connections)         | High (human curation is precise)             | Highest (precision + provenance)                   |
| **Knowledge quality at large scale** | Degrades (false coherence, context limits)   | Plateaus (bounded by curation bandwidth)     | Plateaus with better staleness detection           |
| **Error propagation**                | High                                         | Low                                          | Low                                                |
| **Error detection**                  | Lint (partial) + external validation         | Live verification + staleness scoring        | Live verification + staleness + provenance tracing |
| **Error recovery**                   | Hard (trace all affected entries)            | Easy (update one file)                       | Easy + source-grounded re-verification             |
| **Maintenance cost growth**          | Superlinear (O(n²) lint)                     | Linear (O(n) per module)                     | Linear + small source storage overhead             |
| **Cross-domain insight**             | Strong                                       | Weak (manual interaction maps)               | Weak-to-moderate                                   |
| **Context window efficiency**        | Poor at scale                                | Excellent                                    | Excellent                                          |
| **Human readability**                | High (narrative + Obsidian)                  | Medium (structured, section-oriented)        | Medium                                             |
| **Auditability**                     | Medium (provenance chains exist but complex) | High (explicit load → search → assert trail) | Highest (provenance + load trail)                  |
| **Ideal knowledge base size**        | 50-200 entries                               | 5-30 deeply curated modules                  | 5-30 modules + source snapshots                    |
| **Ideal domain shape**               | Broad, loosely coupled                       | Deep, tightly coupled                        | Deep + needs provenance                            |
```