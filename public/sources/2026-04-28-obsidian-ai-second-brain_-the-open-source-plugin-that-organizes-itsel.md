---
title: Open my-wiki/ in Obsidian
slug: 2026-04-28-obsidian-ai-second-brain_-the-open-source-plugin-that-organizes-itsel
source_url: https://agricidaniel.com/blog/claude-obsidian-ai-second-brain
source_type: article
fetched_at: 2026-05-13
lang: en
---

![Cover image for I Turned Obsidian Into a Self-Organizing AI Brain  -  Here's the Open-Source Plugin](https://agricidaniel.com/images/blog/claude-obsidian-cover.webp)

Cover image for I Turned Obsidian Into a Self-Organizing AI Brain - Here's the Open-Source Plugin

## Your Obsidian Vault Is Probably a Graveyard

The personal knowledge base AI market hit $1.65 billion in 2025 and is growing at 30.3% CAGR toward $6.15 billion by 2030 ([Research and Markets](https://www.researchandmarkets.com/reports/6226503/personal-knowledge-base-ai-market-report), 2026). Yet most people's Obsidian vaults are digital graveyards. Notes go in, links don't get made, and six months later you can't find anything. I've been there. Hundreds of notes, zero connections, and the guilt of knowing the system only works if you maintain it.

The typical advice is "just build a Zettelkasten" or "use bidirectional links." That's the PKM equivalent of telling someone to floss more. Technically correct, practically useless, because **the bottleneck isn't the method - it's the maintenance**.

So I built [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) - a Claude Code plugin that does the organizing for you. It reads your sources, extracts entities and concepts, cross-references everything with wikilinks, flags contradictions, and maintains a living index. You throw documents at it. It builds a wiki. And the wiki gets smarter with every source you add.

Key Takeaways

- claude-obsidian implements Karpathy's LLM Wiki pattern with 10 specialized skills and zero manual filing
- The hot cache system preserves ~500 words of session context between conversations, eliminating the "recap problem" that wastes tokens
- AI-driven knowledge management saves knowledge workers 30-45% of time on information retrieval ([McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai), 2025)
- Works across Claude Code, Gemini CLI, Codex CLI, and Cursor - not locked to one AI provider

## What Is Karpathy's LLM Wiki Pattern?

Andrej Karpathy - co-founder of OpenAI, former Tesla AI director - shared an approach to personal knowledge management that bypasses traditional RAG entirely ([VentureBeat](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an), 2026). Instead of embedding your notes into vectors and doing semantic search, you structure them as plain markdown files that an LLM can read directly. The LLM doesn't just search your notes - **it writes and maintains them**.

Here's how Karpathy described it: you index source documents into a `raw/` directory, then use an LLM to "compile" a wiki - a collection of `.md` files with summaries, backlinks, and categorization into concepts with articles linking them all. Obsidian serves as the frontend where you view raw data, the compiled wiki, and derived visualizations. The LLM writes and maintains all of the wiki data rather than you doing it manually.

Why does this beat RAG for personal knowledge? Three reasons:

- **No vector database** - No embeddings, no Pinecone, no ChromaDB. Just markdown files on your disk.
- **Human-readable output** - The wiki is browsable in Obsidian with graph view, wikilinks, and full-text search - even without an LLM running.
- **Compounding intelligence** - Each new source gets cross-referenced against everything already in the wiki. The 50th source is dramatically more useful than the first.

claude-obsidian is my implementation of this pattern. It's not the only one - there are several on GitHub - but it's the most complete, with **10 specialized skills, 2 parallel agents, and a hot cache system** that none of the others have.

![Obsidian graph view showing claude-obsidian wiki with color-coded entities, concepts, and sources interconnected via wikilinks](https://agricidaniel.com/images/blog/claude-obsidian-graph-view.webp)

A real claude-obsidian vault in graph view - entities (blue), concepts (green), sources (white) automatically cross-referenced

<svg viewBox="0 0 560 380" style="max-width:100%;height:auto;font-family:'Inter',system-ui,sans-serif" role="img" aria-label="Personal Knowledge Base AI Market growing from $1.27B in 2024 to $6.15B by 2030"><title>Personal Knowledge Base AI Market Growth</title> <desc>Horizontal bar chart showing market growth: 2024 $1.27B, 2025 $1.65B, 2026 $2.16B, 2028 $3.67B, 2030 $6.15B. Source: Research and Markets, 2026.</desc> <text x="280" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="currentColor">Personal Knowledge Base AI Market Growth</text> <text x="280" y="46" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.45">30.3% CAGR - $1.27B to $6.15B</text> <line x1="130" y1="60" x2="130" y2="320" stroke="currentColor" opacity="0.3" stroke-width="1"></line><line x1="130" y1="320" x2="540" y2="320" stroke="currentColor" opacity="0.3" stroke-width="1"></line><line x1="130" y1="112" x2="540" y2="112" stroke="currentColor" opacity="0.08" stroke-width="1"></line><line x1="130" y1="164" x2="540" y2="164" stroke="currentColor" opacity="0.08" stroke-width="1"></line><line x1="130" y1="216" x2="540" y2="216" stroke="currentColor" opacity="0.08" stroke-width="1"></line><line x1="130" y1="268" x2="540" y2="268" stroke="currentColor" opacity="0.08" stroke-width="1"></line><text x="120" y="92" text-anchor="end" font-size="13" fill="currentColor" opacity="0.8">2024</text> <rect x="130" y="74" width="85" height="32" rx="4" fill="#38bdf8" opacity="0.7"></rect><text x="222" y="95" font-size="12" font-weight="700" fill="currentColor">$1.27B</text> <text x="120" y="144" text-anchor="end" font-size="13" fill="currentColor" opacity="0.8">2025</text> <rect x="130" y="126" width="110" height="32" rx="4" fill="#38bdf8" opacity="0.8"></rect><text x="247" y="147" font-size="12" font-weight="700" fill="currentColor">$1.65B</text> <text x="120" y="196" text-anchor="end" font-size="13" fill="currentColor" opacity="0.8">2026</text> <rect x="130" y="178" width="144" height="32" rx="4" fill="#f97316"></rect><text x="281" y="199" font-size="12" font-weight="700" fill="currentColor">$2.16B</text> <text x="120" y="248" text-anchor="end" font-size="13" fill="currentColor" opacity="0.8">2028</text> <rect x="130" y="230" width="245" height="32" rx="4" fill="#f97316" opacity="0.85"></rect><text x="382" y="251" font-size="12" font-weight="700" fill="currentColor">$3.67B</text> <text x="120" y="300" text-anchor="end" font-size="13" fill="currentColor" opacity="0.8">2030</text> <rect x="130" y="282" width="410" height="32" rx="4" fill="#f97316"></rect><text x="500" y="303" font-size="12" font-weight="800" fill="white">$6.15B</text> <text x="280" y="355" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.35">Source: Research and Markets (2026)</text></svg>

## What Does claude-obsidian Actually Do?

Obsidian has 2,700+ community plugins and over 100 AI-related ones ([NxCode](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026), 2026). Most of them do one thing: chat with your vault. Smart Connections does semantic search. Copilot does RAG-based Q&A. They're point solutions. **claude-obsidian is a complete knowledge operating system with 10 specialized skills:**

| Skill | What It Does | Trigger |
| --- | --- | --- |
| **wiki** | Setup vault, scaffold structure from description | /wiki |
| **wiki-ingest** | Extract entities, create cross-referenced pages | ingest \[source\] |
| **wiki-query** | Search vault with citations to specific pages | what do you know about X? |
| **wiki-lint** | Find orphans, dead links, contradictions, gaps | lint the wiki |
| **save** | File conversations as structured wiki notes | /save |
| **autoresearch** | Autonomous web research loops with gap-filling | /autoresearch \[topic\] |
| **canvas** | Visual reference boards with images and PDFs | /canvas |
| **defuddle** | Strip web page clutter, save 40-60% tokens | auto on URLs |
| **obsidian-markdown** | Syntax reference for wikilinks, callouts, embeds | how do I wikilink? |
| **obsidian-bases** | Create Obsidian Bases database views over vault | create a base |

The key differentiator? **These skills compound.** When you ingest a source, the wiki-ingest agent doesn't just summarize it - it creates entity pages, concept pages, cross-references them against every existing page, flags contradictions with `[!contradiction]` callouts, and updates the index. The 50th source you add doesn't create 10 isolated notes. It creates 10 notes woven into a mesh of 500.

## How Does the Hot Cache Eliminate Session Amnesia?

Federal Reserve research quantified generative AI's time savings at 5.4% of work hours - about 2.2 hours saved weekly ([AutoFaceless](https://autofaceless.ai/blog/ai-productivity-statistics-2026), 2026). But a huge chunk of that time gets wasted on a problem nobody talks about: **session amnesia**. Every time you start a new Claude conversation, the AI has zero memory of your last session. You spend 5-10 minutes re-explaining context. Every. Single. Time.

claude-obsidian solves this with a **hot cache** - a file at `wiki/hot.md` that stores ~500 words of the most recent session context. When you start a new conversation, the plugin silently reads `hot.md` first, restoring the AI's working memory. No recap needed. No "where were we?" prompts.

Here's what the hot cache typically contains:

- What you were working on in the last session
- Key decisions made and their rationale
- Which wiki pages were recently created or updated
- Open questions or next steps you mentioned

It's around 500 tokens to read - less than 0.25% of Claude's context window. But it eliminates the 2,000-3,000 tokens you'd otherwise waste on re-establishing context. That's a 4-6x return on a tiny token investment.

## From Raw Source to Connected Wiki in 60 Seconds

Obsidian's 1.5 million users spend an average of 43 minutes per day in the app ([NxCode](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026), 2026). How much of that time goes to actually organizing knowledge versus just adding notes? With claude-obsidian, the workflow looks like this:

**Step 1: Drop a source into `.raw/`**

Drag a PDF, paste a URL, or dump a transcript. The `.raw/` directory is immutable - original sources are never modified.

**Step 2: Run `ingest this`**

The wiki-ingest agent (powered by Sonnet, up to 30 turns) reads the source and:

- Extracts named entities (people, tools, companies)
- Identifies concepts (patterns, frameworks, methodologies)
- Creates or updates wiki pages using standardized templates
- Adds wikilinks between related pages
- Flags contradictions with existing knowledge
- Logs the operation in `wiki/log.md`
![claude-obsidian welcome canvas showing the 3-step workflow: drop sources, AI processes everything, your brain vault grows](https://agricidaniel.com/images/blog/welcome-canvas.gif)

The welcome canvas - drop sources, AI processes, your vault grows

**Step 3: There is no step 3.**

That's it. One command, and a 20-page PDF becomes 8-15 interconnected wiki pages with proper frontmatter, cross-references, and provenance tracking. You didn't create a single folder, tag, or link manually.

**Our finding:** In testing across 30+ sources (research papers, meeting transcripts, technical docs), the wiki-ingest agent consistently produces 8-15 wiki pages per source with an average of 12 wikilinks per page. A 200-page vault built from 25 sources had 94% of its pages connected to at least two others - zero manual linking required.

## How Does It Compare to Smart Connections and Copilot?

Claude Code's plugin ecosystem has grown to 340 plugins and 1,367 agent skills as of April 2026, with the official marketplace hosting 101 plugins including 33 from Anthropic ([Gradually AI](https://www.gradually.ai/en/claude-code-statistics/), 2026). But within Obsidian's AI plugin landscape, Smart Connections and Copilot are the incumbents. Here's how claude-obsidian differs fundamentally:

<svg viewBox="0 0 560 420" style="max-width:100%;height:auto;font-family:'Inter',system-ui,sans-serif" role="img" aria-label="Radar chart comparing claude-obsidian, Smart Connections, and Copilot across 6 dimensions"><title>AI Obsidian Tools Comparison</title> <desc>Radar chart comparing claude-obsidian, Smart Connections, and Copilot for Obsidian across 6 capabilities: Knowledge Organization, Cross-Referencing, Research Automation, Multi-Model Support, Session Memory, and Vault Maintenance. claude-obsidian scores highest overall.</desc> <text x="280" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="currentColor">AI Obsidian Tools - Capability Comparison</text> <text x="280" y="46" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.45">Scored 0-10 across 6 dimensions</text> <polygon points="280,90 445,175 445,305 280,390 115,305 115,175" fill="none" stroke="currentColor" opacity="0.08" stroke-width="1"></polygon><polygon points="280,130 405,195 405,285 280,350 155,285 155,195" fill="none" stroke="currentColor" opacity="0.08" stroke-width="1"></polygon><polygon points="280,170 365,215 365,265 280,310 195,265 195,215" fill="none" stroke="currentColor" opacity="0.08" stroke-width="1"></polygon><polygon points="280,210 325,235 325,245 280,270 235,245 235,235" fill="none" stroke="currentColor" opacity="0.08" stroke-width="1"></polygon><line x1="280" y1="90" x2="280" y2="390" stroke="currentColor" opacity="0.08" stroke-width="1"></line><line x1="115" y1="175" x2="445" y2="305" stroke="currentColor" opacity="0.08" stroke-width="1"></line><line x1="445" y1="175" x2="115" y2="305" stroke="currentColor" opacity="0.08" stroke-width="1"></line><text x="280" y="80" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.8">Knowledge Org</text> <text x="455" y="175" text-anchor="start" font-size="10" fill="currentColor" opacity="0.8">Cross-Ref</text> <text x="455" y="310" text-anchor="start" font-size="10" fill="currentColor" opacity="0.8">Research Auto</text> <text x="280" y="405" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.8">Multi-Model</text> <text x="105" y="310" text-anchor="end" font-size="10" fill="currentColor" opacity="0.8">Session Memory</text> <text x="105" y="175" text-anchor="end" font-size="10" fill="currentColor" opacity="0.8">Vault Maint</text> <polygon points="280,98 437,179 437,301 280,370 131,301 131,179" fill="#f97316" opacity="0.15" stroke="#f97316" stroke-width="2"></polygon><circle cx="280" cy="98" r="4" fill="#f97316"></circle><circle cx="437" cy="179" r="4" fill="#f97316"></circle><circle cx="437" cy="301" r="4" fill="#f97316"></circle><circle cx="280" cy="370" r="4" fill="#f97316"></circle><circle cx="131" cy="301" r="4" fill="#f97316"></circle><circle cx="131" cy="179" r="4" fill="#f97316"></circle><polygon points="280,178 357,211 357,269 280,302 211,269 211,211" fill="#38bdf8" opacity="0.12" stroke="#38bdf8" stroke-width="2"></polygon><circle cx="280" cy="178" r="4" fill="#38bdf8"></circle><circle cx="357" cy="211" r="4" fill="#38bdf8"></circle><circle cx="357" cy="269" r="4" fill="#38bdf8"></circle><circle cx="280" cy="302" r="4" fill="#38bdf8"></circle><circle cx="211" cy="269" r="4" fill="#38bdf8"></circle><circle cx="211" cy="211" r="4" fill="#38bdf8"></circle><polygon points="280,162 365,215 349,277 280,318 219,269 203,211" fill="#a78bfa" opacity="0.12" stroke="#a78bfa" stroke-width="2"></polygon><circle cx="280" cy="162" r="4" fill="#a78bfa"></circle><circle cx="365" cy="215" r="4" fill="#a78bfa"></circle><circle cx="349" cy="277" r="4" fill="#a78bfa"></circle><circle cx="280" cy="318" r="4" fill="#a78bfa"></circle><circle cx="219" cy="269" r="4" fill="#a78bfa"></circle><circle cx="203" cy="211" r="4" fill="#a78bfa"></circle><rect x="140" y="408" width="12" height="3" rx="1" fill="#f97316"></rect><text x="158" y="412" font-size="10" fill="currentColor" opacity="0.7">claude-obsidian</text> <rect x="260" y="408" width="12" height="3" rx="1" fill="#38bdf8"></rect><text x="278" y="412" font-size="10" fill="currentColor" opacity="0.7">Smart Connections</text> <rect x="400" y="408" width="12" height="3" rx="1" fill="#a78bfa"></rect><text x="418" y="412" font-size="10" fill="currentColor" opacity="0.7">Copilot</text></svg>

The fundamental difference is scope. Smart Connections and Copilot are **chat interfaces** - they answer questions about your existing notes. claude-obsidian is a **knowledge engine** - it creates, organizes, maintains, and evolves your notes autonomously. It's the difference between a search bar and a research assistant.

Smart Connections uses RAG with vector embeddings. You ask a question, it finds similar notes, returns excerpts. Useful, but it can't create new notes, can't cross-reference, can't flag that your note from January contradicts your note from March. Copilot adds multi-model support and vault-wide chat, but again - it's a Q&A layer on top of static notes.

claude-obsidian's query system also cites specific wiki pages, not training data. When it answers a question, you get `[[wiki/entities/Claude Code]]` links - not hallucinated facts. You can click through to verify every claim.

## The Autonomous Research Loop Nobody Else Has

The AI-driven knowledge management market is growing at 46.7% CAGR, reaching $11.24 billion in 2026 ([Global Industry Analysts](https://www.giiresearch.com/report/tbrc1978064-ai-driven-knowledge-management-system-global.html), 2026). One reason: AI isn't just retrieving knowledge anymore - it's generating it. claude-obsidian's `/autoresearch` skill takes this seriously.

Give it a topic. It runs an autonomous research loop:

1. **Round 1:** Web search, fetch top sources, extract key findings
2. **Round 2:** Identify gaps in coverage, search for missing angles
3. **Round 3:** Synthesize findings, resolve contradictions, file as wiki pages

The output isn't a wall of text. It's structured wiki pages with proper frontmatter, source citations, and cross-references to your existing knowledge. Every claim links back to its source. Every entity gets its own page. And the research gets woven into your vault's existing knowledge graph.

You configure objectives and constraints in a `program.md` file, so the research agent knows what depth you want, which sources to prioritize, and when to stop. It's not a blind scraper - it's guided research with provenance tracking.

**From my experience:** I used `/autoresearch` to build a wiki on AI marketing automation. In three rounds, it produced 23 wiki pages covering tools, workflows, pricing models, and competitive positioning. Two of those pages directly informed blog posts that now rank on page 1 for their target keywords. The research that used to take me a full weekend now takes 15 minutes of supervision.

## Works Across Claude, Gemini, Codex, and Cursor

Claude Code is the most-used AI coding tool according to a Pragmatic Engineer survey of 15,000 developers, with a 46% "most loved" rating and 22,000+ GitHub stars ([Gradually AI](https://www.gradually.ai/en/claude-code-statistics/), 2026). But what if you use Gemini? Or Codex? claude-obsidian works across all of them.

The plugin ships with a `setup-multi-agent.sh` script that installs it for:

- **Claude Code** - Auto-discovered from plugin directory
- **Gemini CLI** - Installed to `~/.gemini/skills/claude-obsidian`
- **Codex CLI** - Installed to `~/.codex/skills/claude-obsidian`
- **OpenCode** - Installed to `~/.opencode/skills/claude-obsidian`
- **Cursor** - Workspace-local installation
- **Windsurf** - Workspace-local installation

This is the local-first philosophy that makes Obsidian powerful. Your vault is a folder of markdown files. Your AI tool is a plugin that reads and writes those files. If Claude goes down, your wiki still works. If you switch to Gemini next year, your knowledge comes with you.

<svg viewBox="0 0 560 380" style="max-width:100%;height:auto;font-family:'Inter',system-ui,sans-serif" role="img" aria-label="Donut chart showing claude-obsidian's 10 skills distributed across 4 capability areas"><title>claude-obsidian Skill Architecture</title> <desc>Donut chart showing skill distribution: Knowledge Building (ingest, autoresearch, save) 30%, Knowledge Retrieval (query, obsidian-markdown, obsidian-bases) 30%, Vault Maintenance (lint, defuddle) 20%, Visual Layer (canvas, wiki) 20%. 10 skills total.</desc> <text x="280" y="28" text-anchor="middle" font-size="15" font-weight="700" fill="currentColor">claude-obsidian Skill Architecture</text> <text x="280" y="46" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.45">10 skills across 4 capability areas</text> <path d="M280,80 A140,140 0 0,1 420,220 L370,220 A90,90 0 0,0 280,130 Z" fill="#f97316"></path><path d="M420,220 A140,140 0 0,1 280,360 L280,310 A90,90 0 0,0 370,220 Z" fill="#38bdf8"></path><path d="M280,360 A140,140 0 0,1 180,284 L214,257 A90,90 0 0,0 280,310 Z" fill="#a78bfa"></path><path d="M180,284 A140,140 0 0,1 280,80 L280,130 A90,90 0 0,0 214,257 Z" fill="#22c55e"></path><text x="280" y="212" text-anchor="middle" font-size="28" font-weight="800" fill="currentColor">10</text> <text x="280" y="232" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.6">skills</text> <text x="380" y="140" font-size="11" font-weight="600" fill="#f97316">Knowledge</text> <text x="380" y="154" font-size="11" font-weight="600" fill="#f97316">Building (3)</text> <text x="400" y="290" font-size="11" font-weight="600" fill="#38bdf8">Retrieval (3)</text> <text x="150" y="310" text-anchor="end" font-size="11" font-weight="600" fill="#a78bfa">Maintenance (2)</text> <text x="160" y="140" text-anchor="end" font-size="11" font-weight="600" fill="#22c55e">Visual (2)</text> <rect x="120" y="370" width="12" height="3" rx="1" fill="#f97316"></rect><text x="138" y="374" font-size="9" fill="currentColor" opacity="0.7">ingest, autoresearch, save</text> <rect x="310" y="370" width="12" height="3" rx="1" fill="#38bdf8"></rect><text x="328" y="374" font-size="9" fill="currentColor" opacity="0.7">query, markdown, bases</text></svg>

## Three Ways to Install - Two Minutes to Start

Obsidian crossed 1.5 million users in early 2026 with 22% year-over-year growth ([Fueler](https://fueler.io/blog/obsidian-usage-revenue-valuation-growth-statistics), 2026). If you're one of them, here's how to get started:

**Option 1: Clone as a vault (recommended)**

```
git clone https://github.com/AgriciDaniel/claude-obsidian.git my-wiki
bash my-wiki/bin/setup-vault.sh
# Open my-wiki/ in Obsidian
```

**Option 2: Claude Code marketplace**

```
claude plugin marketplace add AgriciDaniel/claude-obsidian
```

**Option 3: Add to existing vault**

Copy `WIKI.md` into your vault root and run `/wiki` - the setup wizard handles the rest.

The plugin uses three MCP connection options for vault access:

- **mcp-obsidian** (REST API) - Recommended. Uses Obsidian's Local REST API plugin.
- **MCPVault** (Filesystem) - No plugin needed. Reads files directly.
- **Direct REST** - Manual HTTP calls for power users.

The vault comes pre-configured with four Obsidian plugins: Calendar, Thino, Excalidraw, and Banners. The `.obsidian/` config is included so graph view colors are already set up - entities in one color, concepts in another, sources in a third.

## How Does the Vault Stay Healthy Over Time?

AI copilots improve knowledge-worker productivity by 30-45% ([McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai), 2025). But productivity gains mean nothing if your knowledge base degrades over time. That's where `wiki-lint` comes in.

Run `lint the wiki` and the lint agent scans for eight categories of issues:

- **Orphan pages** - Notes with no inbound links
- **Dead wikilinks** - Links pointing to non-existent pages
- **Contradictions** - Conflicting claims across pages
- **Missing pages** - Referenced but never created
- **Unlinked mentions** - Entity names in text without wikilinks
- **Incomplete metadata** - Missing frontmatter fields
- **Empty sections** - Stub content that needs expansion
- **Stale index** - Index doesn't match actual vault contents

Every issue gets a severity level and a suggested fix.

![Obsidian canvas Wiki Map showing claude-obsidian architecture with Hot Cache, LLM Wiki Pattern, Karpathy entity, and navigation zones](https://agricidaniel.com/images/blog/claude-obsidian-wiki-map.webp)

The Wiki Map canvas - visual architecture showing how entities, concepts, and sources connect

Here's the insight that most AI knowledge management tools miss: **the value of a knowledge base is proportional to its link density, not its note count**. A vault with 100 notes and 500 cross-references is more useful than one with 1,000 notes and 50 links. claude-obsidian's entire architecture is designed to maximize link density - every skill that creates content also creates connections.

## Frequently Asked Questions

### Does claude-obsidian work without an internet connection?

The vault itself is fully offline - it's local markdown files. The AI skills require a connection to Claude's API (or whatever model you're using). But you can browse, search, and edit your wiki in Obsidian without any internet. The `/autoresearch` skill needs web access, but ingestion from local files works offline with local models via Ollama.

### How does it handle conflicting information from different sources?

When wiki-ingest detects that a new source contradicts an existing wiki page, it creates a `[!contradiction]` callout on the relevant page. It doesn't silently overwrite - it flags both claims with their sources so you can resolve the conflict. This is critical because Karpathy's pattern emphasizes provenance: every fact traces back to its source document.

### What's the maximum vault size it can handle effectively?

Karpathy's guidance is that a team wiki under ~500 articles works well with markdown + keyword search. claude-obsidian's token-disciplined query system reads `hot.md` first (~500 tokens), then `index.md` (~1,000 tokens), then 3-5 relevant pages (~3,000 tokens). This keeps total context usage under 5,000 tokens per query, even for vaults with 300+ pages.

### Can I use it with Notion or other note apps instead of Obsidian?

Not directly. claude-obsidian is built for Obsidian's local-file architecture. Notion's 4.2 million organizations use a cloud-based proprietary format ([Revoyant](https://www.revoyant.com/blog/best-ai-note-taking-apps-in-2026), 2026). The plugin reads and writes `.md` files - if your app stores notes as local markdown (like Logseq or Foam), you could potentially adapt it, but Obsidian is the supported platform.

### Is it free?

Yes. MIT licensed, fully open source. You pay for the AI model API usage (Claude, Gemini, etc.), but the plugin itself costs nothing. Obsidian is also free for personal use.

## The Wiki That Builds Itself

The note-taking app market is projected to hit $4.89 billion by 2033 at 22% CAGR ([Axis Intelligence](https://axis-intelligence.com/best-note-taking-apps-2026-47-ai-tools/), 2026). Most of that growth will come from AI-native tools that do the work humans hate - organizing, linking, and maintaining knowledge. claude-obsidian is my bet on what that looks like.

It's Karpathy's pattern, productized. It's 10 skills that cover the full lifecycle from source ingestion to vault maintenance. It's a hot cache that remembers your context between sessions. And it's open source - 358 stars and growing - because knowledge tools should be owned, not rented.

- Star the repo on [GitHub](https://github.com/AgriciDaniel/claude-obsidian)
- Learn more [about me](https://agricidaniel.com/about) and the tools I'm building
- See how it fits into [my full AI marketing automation stack](https://agricidaniel.com/blog/ai-marketing-automation-stack)
- Build your own Claude Code skills with [Skill Forge](https://agricidaniel.com/blog/skill-forge-build-claude-code-skills)
- Join the [Claude Code community on Skool](https://www.skool.com/claude-code)

## Related Posts

- [Best Claude Code Skills in 2026](https://agricidaniel.com/blog/best-claude-code-skills-2026) - The definitive ranking of skills that actually save time
- [Build Your Own Claude Code Skills with Skill Forge](https://agricidaniel.com/blog/skill-forge-build-claude-code-skills) - From idea to published skill in minutes
- [AI Marketing Automation: The Open-Source Stack I Use Daily](https://agricidaniel.com/blog/ai-marketing-automation-stack) - The full stack at $50/month
- [Claude Code Just Replaced Your Entire SEO Stack](https://agricidaniel.com/blog/claude-code-seo-stack) - How I replaced $300/month in SEO tools

Join 2,800+ AI Marketing Builders

Get workflow templates, automation blueprints, and connect with SEOs, agency owners, and creators who ship.

[JOIN FREE →](https://www.skool.com/ai-marketing-hub)