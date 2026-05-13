## 2026-04-12T12:32:20+04:00

https://scribelet.app/blog/karpathy-llm-wiki-reaction

[Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) on LLM-maintained wikis names something the PKM world has been circling for years: the tedious part of a knowledge base isn't the reading, it's the bookkeeping. His pattern solves it by pointing the LLM at compiled external sources. There's another direction worth naming.

## Two directions, not one

Karpathy's pattern is compiled external knowledge. You curate raw sources (papers, articles, PDFs, transcripts), and the LLM authors and maintains the synthesis on top of them. Entity pages, concept pages, a log.md, a CLAUDE.md that encodes the schema. The LLM is the writer; you're the librarian pointing it at what to read.

There's an inverse shape. You write your own notes (half-formed thoughts, meeting fragments, architecture sketches, what you actually decided on Tuesday), and the LLM maintains *that*. It never authors the first draft. It cross-references, flags contradictions, catches drift, and keeps the graph connected. You're the writer; it's the librarian for the thing you wrote.

Take each pattern to the limit. Karpathy's wiki, scaled to infinity, converges toward a personalized copy of the internet, an ever-more-complete synthesis of what you've read. The inverse, scaled to infinity, converges toward a persistent copy of your own mind, what you've actually thought, kept alive. Genuinely different artifacts. Genuinely different architectures.

## The maintenance loop is the same; the source of truth is not

Both shapes need the same pipeline: ingestion, cross-referencing, contradiction detection, stale flags, synthesis, scheduled health checks. What changes is the authoring layer.

In Karpathy's pattern the LLM authors, so the maintenance loop can be aggressive. If a new source contradicts an entity page, rewrite the page. Better synthesis wins. The prior version had no sentimental value. Nobody wrote it from the inside.

In the inverse pattern the human authors, so the maintenance loop has to be careful. When you care about what *you* think, not what the best available reading of the sources says, the LLM must not overwrite your voice. It maintains *around* you. It surfaces the contradiction; you decide whether you changed your mind or misremembered something. It finds the older note that connects; you decide whether the link belongs. The diff is the interface, not the rewrite.

This is why the tools end up shaped differently even when they share the same loop. If the LLM is the author, you ship a renderer. If the human is the author, you ship an editor with a maintenance layer underneath it.

## Only one of these is a second brain

The PKM crowd will tell you that "second brain" and "personal knowledge management" aren't about having a fast retrieval system for stuff you've read. They're about the act of writing your own words, in your own voice, while the ideas are still metabolizing. Tiago Forte's CODE framework (Capture, Organize, Distill, Express) treats the last two steps as where the value actually lives. Sönke Ahrens's *How to Take Smart Notes* rests on the same claim: writing is thinking. Skip the writing and you skipped the thinking.

By that standard, only the second shape is PKM. Karpathy's pattern builds a personalized research index, and probably the best version of that artifact anyone has proposed. But the LLM is doing the distillation and the expression. Taken seriously as a methodology, "second brain" describes the tool where *you* do the distilling and the expressing, and something else keeps your output from rotting.

This is worth naming because a lot of the reaction to the gist is calling it "Karpathy's second brain." It isn't, in the sense the PKM tradition uses the term. It's a better thing for a different job: queryable external knowledge, not accumulated personal thinking.

## What that looks like as a product

We've been building the inverse shape for about a year. A few concrete pieces, in case the mapping is useful:

Background verification searches the web on a schedule and shows a diff when something you wrote has drifted from reality, the "lint pass for stale claims" applied to user-authored notes instead of ingested sources. Notes go stale the same way compiled sources do; [knowledge decay](https://scribelet.app/blog/knowledge-decay) is the underlying problem, and this is the parallel to the periodic health checks Karpathy describes.

The auto-linker finds the note you wrote six months ago that connects to the one you wrote today, across pages the LLM didn't author. Contradiction detection flags when a new note disagrees with an older one and asks you which version survives, not which the model prefers. Memory extraction pulls the entities you've been thinking about out of your notes and chats and draws the edges between them, building the same kind of graph Karpathy's wiki grows, but seeded from your thinking rather than your sources. Episodic memory is the log.md idea applied to conversations: timestamped summaries you can recall by "when did we talk about X." Procedural memory is the CLAUDE.md idea applied at runtime: rules you write once (`category='procedural'`) and the AI respects on every future turn, injected unconditionally into the system prompt.

None of this is a clone of the gist. No parity claim. Karpathy is describing a pattern a skilled user implements in Claude Code against their own sources, which is a different scope than a product that has to behave reasonably for everyone. Same problem, same shape of loop, different source of truth.

## Which one should you build?

Honest answer: depends on what you're trying to remember. If you're synthesizing a field (catching up on a new research area, compiling what's known about a topic), Karpathy's pattern is probably the right shape, and the gist is a good spec to build against. If you're accumulating your own thinking (decisions, rationales, half-formed ideas, the things you'd forget by Friday), the inverse is probably right, because the authoring layer is the thing you care about and you don't want a model rewriting it.

Most people will want both. Different tools, different jobs. The tools that try to do both usually do neither well, because the aggressive maintenance loop the compiled pattern needs is exactly the loop that eats your voice in the authored pattern.

## Closing

Both shapes are maintenance loops wrapped around different sources of truth. Karpathy's is pointed outward at the world; this other one is pointed inward at your own notes. Most people doing serious knowledge work will end up with something of each: something Karpathy-shaped for the fields they're researching, something else for the thinking they're accumulating.

If you're curious what the inverse pattern looks like as a real product, we've been building it at [Scribelet](https://scribelet.app/).

On this page