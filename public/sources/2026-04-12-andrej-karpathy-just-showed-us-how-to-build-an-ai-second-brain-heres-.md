---
title: Andrej Karpathy Just Showed Us How To Build An AI Second Brain Heres
slug: 2026-04-12-andrej-karpathy-just-showed-us-how-to-build-an-ai-second-brain-heres-
source_url: https://mattpaige68.substack.com/p/andrej-karpathy-just-showed-us-how?r=llvd&utm_medium=ios&triedRedirect=true
source_type: article
fetched_at: 2026-05-13
lang: en
---

Most people use AI the same way every time. Upload a document. Ask a question. Get an answer. Close the tab.

Tomorrow, you upload the same document. Ask a slightly different question. The AI starts from scratch. No memory of yesterday. No accumulated understanding. No synthesis across everything you’ve ever asked.

This is how NotebookLM works. It’s how ChatGPT file uploads work. It’s how most RAG systems work. And it’s fundamentally broken for anyone trying to build knowledge over time.

Andrej Karpathy just proposed a better way. And it might be the most useful AI workflow I’ve seen this year.

---

## What Karpathy Proposed

In [two posts on X](https://x.com/karpathy/status/2040470801506541998?s=20) that went massively viral last week, Karpathy outlined a pattern he’s calling the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The idea is simple but powerful:

Instead of having your AI re-read raw documents every time you ask a question, **have the AI incrementally build and maintain a persistent wiki**: a structured, interlinked collection of markdown files that compounds over time.

When you add a new source, the AI doesn’t just index it for later retrieval. It reads it, extracts the key information, and *integrates it into the existing wiki* updating entity pages, revising topic summaries, noting where new information contradicts old claims, and strengthening the overall synthesis.

The difference from what most people do today:

RAG (what you’re doing now) LLM Wiki (Karpathy’s approach) **When you add a source** It gets chunked and embedded for later retrieval The AI reads it, summarizes it, updates every relevant page in your wiki **When you ask a question** AI searches for relevant chunks, pieces together an answer from scratch AI reads the pre-built wiki pages, gives you an answer with citations already in place **Over time** Nothing accumulates. Every query starts from zero. The wiki gets richer. Cross-references build up. Contradictions are flagged. **Maintenance** None needed (but quality doesn’t improve either) The AI handles all maintenance, and that’s the whole point.

Karpathy put it perfectly: *“Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don’t get bored, don’t forget to update a cross-reference, and can touch 15 files in one pass.”*

---

## The Architecture: Three Layers

The pattern has three layers, and understanding them is key to making this work.

**1\. Raw Sources** — Your curated collection of source documents. Articles, PDFs, notes, clipped web pages. These are immutable. The AI reads from them but never modifies them. This is your source of truth.

**2\. The Wiki** — A directory of AI-generated markdown files. Summaries, entity pages, concept pages, comparisons, an index. The AI owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the AI writes it.

**3\. The Schema** — A configuration file (CLAUDE.md for Claude Code) that tells the AI how the wiki is structured, what conventions to follow, and what workflows to execute when ingesting sources, answering questions, or maintaining the wiki. This is what makes the AI a disciplined wiki maintainer rather than a generic chatbot.

Karpathy’s metaphor is perfect: **“ [Obsidian](https://obsidian.md/) is the IDE. The LLM is the programmer. The wiki is the codebase.”**

![](https://substackcdn.com/image/fetch/$s_!liSC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f50257c-8691-4e53-b94f-1748cd017a5e_979x862.png)

---

## How to Build One (Step by Step)

To test this out, I decided to go all in. I loaded every [Substack](https://substack.com/@mattpaige68) article I’ve ever published into an [Obsidian](https://obsidian.md/) vault using this exact structure, with Claude Code as the engine. Within an hour, I had 56 interconnected wiki pages — every article broken down into its thesis, key claims, data cited, products covered, and recurring themes. All cross-referenced. All queryable. It’s now the foundation I use to research and draft new articles.

Here’s exactly how to set this up with [Claude Code](https://www.anthropic.com/product/claude-code) and [Obsidian](https://obsidian.md/). The whole thing takes about 15 minutes.

### What You Need

- **Claude Code** installed and running (if you haven’t set it up yet, [here’s my complete beginner’s guide](https://open.substack.com/pub/mattpaige68/p/the-complete-beginners-guide-to-claude))
- **Obsidian** — download free from [obsidian.md](https://obsidian.md/)
- **Obsidian Web Clipper** — [install from the Chrome Web Store](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf)

### Step 1: Create Your Obsidian Vault

Open Obsidian, click “Create new vault,” and give it a name. This is just a folder on your computer where all your markdown files will live.

![](https://substackcdn.com/image/fetch/$s_!WbI4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d0ef978-fbd1-41d5-8604-465b6c43a20e_1028x1110.png)

### Step 2: Give Claude Code the Karpathy Gist

Open Claude Code pointed at your Obsidian vault folder. Then paste [Karpathy’s gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and tell Claude Code to implement it:

> “Here is Andrej Karpathy’s [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Please implement this as my personal knowledge base in this Obsidian vault. Create the full directory structure, the CLAUDE.md schema file, the index, the log, and all templates. Use [his gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as the first source to ingest.”

Then paste the full content from [Karpathy’s gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

That’s it. Claude Code will:

- Create the folder structure (`raw/`, `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, etc.)
- Write a complete CLAUDE.md schema file with all the rules, page types, and workflows
- Create the index and activity log
- Ingest the gist itself as the first source
- Build out entity and concept pages from the gist content

![](https://substackcdn.com/image/fetch/$s_!tJij!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e936af7-400e-499b-a32e-ccf05c9e14fc_1642x1986.png)

When it’s done, switch over to Obsidian. You’ll see the full wiki structure in the file explorer and your first set of interlinked pages in the graph view.

### Step 3: Configure the Obsidian Web Clipper

This is how you’ll get sources into your wiki fast.

1. Open the [Obsidian Web Clipper extension settings](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf)
2. Set the default vault to the one you just created
3. Set the default folder to `raw/` — this is where clipped articles will land
4. Now when you’re reading an article you want to save, click the clipper icon and it drops a clean markdown copy into your raw folder

### Step 4: Ingest Your First Real Source

Find an article, research paper, or document relevant to whatever you’re building this wiki for. Clip it with the Web Clipper (or paste a URL directly to Claude Code).

Then tell Claude Code:

> “Ingest the new file in raw/”

Claude Code will read the source, present a summary and key claims for your review, then file everything: a source summary page, entity pages for people and products mentioned, concept pages for ideas covered, all cross-referenced and added to the index.

One source. Five to fifteen wiki pages updated. That’s the compounding effect Karpathy is talking about.

### Step 5: Query Your Wiki

Now ask a question:

> “What do we know about \[topic\] across all sources?”

Claude Code reads the index, pulls the relevant pages, and synthesizes an answer with `[[wikilink]]` citations back to specific sources. If the answer is substantial, it can file it as a new wiki page so your explorations compound too.

### Step 6: Keep It Healthy

Periodically, tell Claude Code to run a health check:

> “Lint the wiki”

It’ll scan for contradictions between pages, orphan pages with no links, stale claims that newer sources have superseded, and missing cross-references. It reports everything organized by severity and offers to fix each issue.

---

## Why This Is Better Than What You’re Doing Now

The core insight is one of those things that seems obvious once you hear it: **the bottleneck to maintaining a useful knowledge base has never been the reading or the thinking. It’s the bookkeeping.**

Updating cross-references. Keeping summaries current. Noting when new data contradicts old claims. Maintaining consistency across dozens of pages. That’s the work humans abandon. And it’s exactly what LLMs are built for.

The wiki stays maintained because the cost of maintenance is near zero.

And because it’s just a folder of markdown files, you get version history with git, beautiful graph visualization in Obsidian, and full portability. No vendor lock-in, no proprietary database, no subscription beyond Claude.

---

## 5 Use Cases That Make This Worth Building

Karpathy describes this as a general-purpose pattern. Here are five specific ways to use it that go beyond “I want to organize my notes.”

### 1\. A Substack or Newsletter Editorial Brain

This is how I’m using it. Every article I’ve published gets ingested. Not just stored, but broken down into structured pages tracking my thesis, key claims, data I cited, products I covered, and recurring themes.