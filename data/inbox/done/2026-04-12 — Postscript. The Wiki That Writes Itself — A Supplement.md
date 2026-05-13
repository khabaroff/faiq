## 2026-04-12T12:22:17+04:00

https://extendedbrain.substack.com/p/postscript-the-wiki-that-writes-itself

*After [this essay](https://extendedbrain.substack.com/p/the-wiki-that-writes-itself) was published, Andrej Karpathy released his own detailed write-up of the system — not a tweet thread, but a proper [idea file on GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) intended to be shared with an LLM agent as a starting point for building your own wiki.* It is precise, considered, and worth reading in full. It confirms the essay’s main architecture description, sharpens a few details, adds one significant historical reference, and — importantly — does not disturb the central argument about what these systems can and cannot do for writers.

What follows is an accounting of what Karpathy’s document changes, what it adds, and what it leaves untouched.

## What the Idea File Clarifies

## The Schema Layer: The Human’s Real Contribution

The essay describes Karpathy’s system as one where the human curates sources and asks questions while the LLM does everything else. This is accurate but incomplete. Karpathy’s document adds a third layer that the essay underplays: the *schema* — a configuration file (he calls it CLAUDE.md for Claude Code, or AGENTS.md for Codex) that defines the wiki’s structure, conventions, and workflows. It tells the LLM how to ingest a source, how to answer a query, how to maintain consistency across pages, what formats to use, what to prioritize.

Karpathy writes that this schema is *co-evolved* by the human and the LLM over time as you figure out what works for your domain. This matters for the essay’s argument. The human’s intellectual contribution to the system is not just curation and questioning — it is also the ongoing design of the rules by which knowledge gets organized and maintained. That is a more active and genuinely cognitive role than the essay implied. The schema is, in a sense, the writer’s theory of how their domain should be structured, expressed as instructions to an AI. Building it well is itself a form of thinking.

## Indexing Demystified: Two Files, Two Jobs

Early in the original conversation that became this essay, the question was raised: what did Karpathy mean by *indexing*? The essay addressed this, but Karpathy’s document is considerably more precise. There are two special files, and they serve entirely different purposes.

**index.md** is content-oriented. It is a catalog of every page in the wiki — each entry listing a link, a one-line summary, and optional metadata such as date or source count, organized by category. When the LLM receives a query, it reads the index first to identify which pages are relevant, then drills into those pages to synthesize an answer. This is what makes query-time RAG unnecessary at moderate scale: the LLM navigates its own wiki the way a knowledgeable librarian navigates a library they personally built and maintain.

**log.md** is chronological. It is an append-only record of what happened and when — every ingest, every query, every lint pass. Karpathy notes that if each entry begins with a consistent prefix, the log becomes parseable with simple Unix tools, so you can run a single command to see the last five things that happened to your wiki. The log gives both you and the LLM a timeline of the wiki’s evolution, which helps orient a new session without re-explaining context from scratch.

The distinction is clean and worth holding onto: the index knows what is in the wiki; the log knows what has been done to it.

## NotebookLM: Named Explicitly as the Contrast Case

The essay’s NotebookLM section was written without access to Karpathy’s own framing of the distinction. His document supplies it directly. He writes: *“NotebookLM, ChatGPT file uploads, and most RAG systems work this way”* — meaning they retrieve from raw documents at query time and re-derive knowledge from scratch on every question. He is drawing the contrast himself, which means the essay’s comparison was not an external imposition but a reflection of Karpathy’s own intent. The wiki is explicitly designed as a departure from the RAG paradigm, not an enhancement of it.

## What the Idea File Adds

## Vannevar Bush and the Memex: A Richer Genealogy

The most significant addition in Karpathy’s document is a historical reference the essay missed entirely. **He situates his system in the lineage of Vannevar Bush’s** ***Memex*** — a concept Bush described in his 1945 essay *As We May Think*. The Memex was a vision of a personal, curated knowledge store with associative trails between documents: private, actively maintained, with the connections between documents treated as valuable as the documents themselves.

Bush’s vision was closer to what Karpathy is building than to what the web became. The web is public, algorithmically indexed, and optimized for search by strangers. The Memex was personal, hand-curated, and optimized for the associative thinking of a single mind over time. The part Bush could not solve — and said so explicitly — was maintenance. Who keeps the trails current? Who updates the cross-references when new material arrives? Who notices when an old claim has been superseded?

The LLM handles that. This is Karpathy’s answer to Bush’s open problem, eight decades later.

This adds a richer intellectual genealogy to the essay’s story. The line now runs: Bush imagined it in 1945 — a personal knowledge machine with living associative trails. Luhmann built a partial version of it by hand across 40 years, solving the synthesis problem through the discipline of personal formulation, but at enormous human cost in maintenance labour. Karpathy automates the maintenance that defeated every previous attempt, using LLMs to do the bookkeeping that humans abandon. The essay’s Luhmann discussion remains entirely valid within this longer arc — Luhmann’s insight about the cognitive value of friction in formulation is unaffected by the Bush reference — but the arc itself is now longer and more historically grounded.

## The Schema as a Use-Case Multiplier

Karpathy’s document enumerates a range of contexts the essay touched on only briefly. The same architecture applies to tracking personal goals and psychology over time; to reading a novel chapter by chapter and building a companion wiki of characters, themes, and plot threads; to business intelligence fed by Slack threads and meeting transcripts; to competitive analysis, due diligence, trip planning, hobby research. The system is domain-agnostic because the schema layer absorbs all the domain-specific configuration.

For writers specifically, this opens an interesting possibility the essay did not explore: using the wiki not just for research on external topics but for tracking the evolution of your own thinking across a long project — filing your drafts, your notes-to-self, your abandoned arguments, and letting the LLM maintain a living picture of where your ideas have been and where they are going. The wiki as a mirror of a writer’s intellectual development over time, not just a repository of sources.

## What the Idea File Does Not Change

The essay’s central argument stands intact, and Karpathy’s document inadvertently reinforces it.

He writes that the human’s job is *“to curate sources, direct the analysis, ask good questions, and think about what it all means.”* The LLM does *“everything else.”* This is precisely the division the essay identified — and precisely where the essay’s critique begins. Curating sources, asking good questions, and thinking about what it all means are real intellectual contributions. But they are not the same as the act of writing that discovers what you think in the process of trying to say it.

The hormetic resistance argument is unaffected. Karpathy correctly identifies the maintenance burden as the reason humans abandon wikis — the cost of keeping cross-references current, updating summaries when new sources arrive, noticing when old claims have been superseded. LLMs solve this problem completely. But solving the maintenance problem is not the same as solving the synthesis problem. The wiki can be immaculately maintained and still not have done the work that produces original thought. These are different problems, and only one of them is addressed by the system.

Luhmann’s core insight — that the friction of formulating an idea in your own words is not inefficiency but mechanism — is not troubled by anything in Karpathy’s document. Karpathy is building better infrastructure for accumulating and navigating knowledge. Luhmann was building a discipline for converting knowledge into understanding through the irreplaceable act of personal reformulation. Both are genuine contributions. They address different stages of the same larger process, and a writer needs both.

The recommended hybrid remains the same: use Karpathy’s system — or NotebookLM — for the reconnaissance and domain-mapping stages. Use something closer to Luhmann’s discipline for the synthesis and argument-development stage, where you must stop reading other people’s formulations and start building your own. The AI compiles the territory. The writer still has to walk it.

—

*Karpathy’s full idea file is available at*

## LLM Wiki

A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts. A few examples:

- **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like [Tolkien Gateway](https://tolkiengateway.net/wiki/Main_Page) — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
- **Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered.

## Architecture

There are three layers:

**Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.

**The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain.

## Operations

**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

**index.md** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. Organized by category (entities, concepts, sources, etc.). The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure.

**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently.

## Optional: CLI tools

At some point you may want to build small tools that help the LLM operate on the wiki more efficiently. A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. [qmd](https://github.com/tobi/qmd) is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool). You could also build something simpler yourself — the LLM can help you vibe-code a naive search script as the need arises.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `raw/assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Dataview** is an Obsidian plugin that runs queries over page frontmatter. If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists.
- The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.

## Note

This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't. For example: your sources might be text-only, so you don't need image handling at all. Your wiki might be small enough that the index file is all you need, no search engine required. You might not care about slide decks and just want markdown pages. You might want a completely different set of output formats. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.