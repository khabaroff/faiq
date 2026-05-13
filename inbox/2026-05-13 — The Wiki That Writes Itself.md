## 2026-05-13T13:17:26+04:00

https://extendedbrain.substack.com/p/the-wiki-that-writes-itself

![](https://substackcdn.com/image/fetch/$s_!MSmq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e2487b9-a965-475b-b2a4-6edd7e91bfd8_1376x768.png)

## Part I: Karpathy’s Mission Statement

On April 2, 2025, **Andrej Karpathy** — one of the founding figures of modern AI and the man who coined the term “vibe coding” — posted something that got the internet’s attention. He announced, almost casually, that he had shifted how he uses large language models. He was no longer spending most of his time asking them to write code. He was spending it manipulating knowledge.

That sentence — spending more tokens manipulating knowledge than manipulating code — is worth sitting with. Coming from Karpathy, it signals something. His earlier idea, vibe coding, had upended how programmers work by treating code as cheap, fast, and disposable. You describe what you want in plain English, the AI writes it, you iterate without guilt. The code doesn’t matter; the outcome does. Now he was applying the same logic to knowledge itself.

The system he described is architecturally simple but conceptually ambitious. Think of it as a personal Wikipedia — except one that writes, maintains, and expands itself, with you acting more as editor-in-chief than author.

## Part II: How the Architecture Works

## The Two-Tier Structure

The foundation is a split between two folders on your computer. The first is called **raw/**. This is the inbox — a place where you drop everything you want to learn from: research papers, articles clipped from the web, images, datasets, GitHub repositories, PDFs. Nothing in the raw folder is processed or organized. It’s just material.

The second layer is the **wiki** — a growing collection of markdown files that the LLM has written and maintains. These files are structured, interlinked, and synthesized. Where the raw folder contains a dozen papers on, say, the free energy principle in neuroscience, the wiki contains a clear article on what the free energy principle is, a separate article on its critics, backlinks connecting it to related concepts, and visualizations where helpful. You don’t write any of this. The LLM does.

This is the key design decision. Karpathy is explicit: he does not manually edit or add anything to the wiki. ***He curates what goes into the raw folder, and he asks questions. Everything else — summarization, synthesis, filing, interlinking — is the LLM’s job.***

## Compilation, Not Summarization

The word Karpathy uses for what the LLM does is **compile** — and the choice of word is deliberate. A compiler, in software, takes raw source code and transforms it into something structured and executable. Karpathy’s LLM takes raw sources and transforms them into a navigable knowledge structure. It’s not just summarizing — it’s reorganizing, categorizing, creating new articles for concepts that appear repeatedly, and managing a web of cross-references.

To continue the example: if you drop fifteen papers on Karl Friston’s free energy principle into the raw folder, the LLM doesn’t just produce fifteen summaries. It writes a synthesis article on the principle itself, notes where authors agree and disagree, creates a backlinked article on active inference as a related concept, and flags connections to, say, predictive coding. The output is a mini-encyclopedia, not a reading list.

## What Indexing Actually Means Here

One of the most interesting technical choices Karpathy made involves what he did not use. The conventional approach for making an AI “search” a large document collection is called RAG — Retrieval-Augmented Generation — which involves converting all your documents into numerical vectors and doing a semantic similarity search every time you ask a question. It works, but it requires significant setup, and it can miss conceptual connections that aren’t captured by word similarity.

Karpathy discovered he didn’t need any of this. Instead, the LLM maintains its own plain-text index files — essentially a table of contents and short summaries of each article in the wiki. When you ask a complex question, the LLM reads its own index, decides which articles are relevant, follows the links between them, and synthesizes an answer. It navigates the wiki the way a knowledgeable librarian would navigate a library they built themselves.

At his current scale — around 100 articles and 400,000 words on a recent research topic — this fits comfortably within a large context window. The index is the LLM’s own memory of what it knows and where it lives.

![](https://substackcdn.com/image/fetch/$s_!bB_K!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe885fb2-81a0-48e9-b4f3-51f4e77ff999_1376x768.png)

## Health Checks and the Living Wiki

What prevents the wiki from becoming stale is a process Karpathy calls health checks, or linting — borrowed from software development, where a linter scans code for errors and inconsistencies. Periodically, an LLM agent passes over the entire wiki looking for contradictions between articles, gaps in coverage, outdated claims that could be updated via a web search, and candidates for new articles that aren’t yet written.

The result is a system that doesn’t just store knowledge — it audits itself. It notices when two articles are making claims that don’t quite agree. It surfaces the question you haven’t asked yet. This is where the system starts to feel less like a filing cabinet and more like something that talks back.

## The Q&A Loop and the Write-Read-Rewrite Cycle

When Karpathy asks the system a complex question, the answer doesn’t disappear into the chat log. It gets filed back into the wiki as a new article — often rendered as a markdown document, a slideshow, or a data visualization. The knowledge base grows not just from new raw sources but from the questions you ask of it.

This creates a feedback loop: you add sources, the LLM compiles them, you ask questions, the answers get filed as new material, the wiki grows more sophisticated, which enables better answers to harder questions. The system is self-reinforcing in the best sense.

![](https://substackcdn.com/image/fetch/$s_!_aRy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92429cba-dde2-41f2-9e92-2a776e6d7139_1376x768.png)

## Part III: The Tools — and Why They’re Optional

Karpathy uses *Obsidian* — a popular personal knowledge management application — as the reading interface for his wiki. Obsidian renders markdown beautifully, shows a visual graph of how articles link to each other, and offers a *Web Clipper* browser extension that converts web articles to clean markdown files with a single click. It also supports plugins like Marp, which can render slide presentations directly from markdown.

But here’s the important thing: Obsidian is not the system. It’s a window into the system. The actual architecture — the raw folder, the compiled wiki, the LLM agents doing the compilation and health checks — exists entirely as plain text files on your computer. The LLM doesn’t know or care that Obsidian is involved. It reads and writes markdown files. That’s it.

You could swap Obsidian for *Logseq*, or *Foam* (a lightweight VS Code extension that brings bidirectional linking to any markdown folder), or Roam Research, or nothing at all — just a folder you browse in your file manager. The system would be identical. The reading interface is cosmetic. What matters is the structure of the files and the quality of the agents working on them.

Karpathy himself acknowledges this. He ends his original post with a telling admission:

> *“I think there is room here for an incredible new product instead of a hacky collection of scripts.”*

What he has now is a set of command-line tools he vibe-coded himself, some Obsidian plugins, and a lot of prompt engineering. It works — for someone with his technical background. But the core idea is much simpler than the current implementation suggests, and it doesn’t depend on any particular tool.

## Part IV: Enter NotebookLM — The Polished Cousin

Before we go further into the intellectual history, it is worth pausing on a tool that many readers will already be using, and that overlaps with Karpathy’s system enough to cause confusion: Google NotebookLM. On the surface, it seems to do many of the same things. You upload sources, ask questions, get synthesized answers. But the differences are architectural, and they matter enormously for a writer thinking about which system to build their intellectual life around.

## What NotebookLM Does

NotebookLM is Google’s AI-powered research tool, free to use with a Google account and available on web and mobile. You upload up to 50 sources per notebook — PDFs, Google Docs, URLs, YouTube videos, Word files — and the system answers questions grounded strictly in those sources, with inline citations. So far, this is similar to Karpathy’s Q&A layer.

But NotebookLM goes further in one direction: the output formats. Beyond text answers, it can generate audio overviews — podcast-style conversations between two AI hosts who discuss your sources in a conversational, often surprisingly lifelike tone. You can even join the podcast in real time, interrupting to ask questions. It can produce video overviews with narrated slides, generate interactive mind maps that visualize connections between concepts in your sources, create flashcards and quizzes for testing recall, and produce study guides, timelines, FAQs, and briefing documents. The September 2025 updates added custom tone and structure controls, so you can tune outputs toward a student audience or an expert one, toward a debate format or an in-depth analysis.

On paper, this looks like it does everything Karpathy’s system does, plus a rich multimedia layer on top. The reality is more nuanced.

## The Fundamental Difference: Session vs. System

Karpathy’s system is designed to grow, learn, and compound over time. New sources go into the raw folder; the LLM incrementally updates the wiki; answers to questions get filed back in as new articles; health checks surface gaps; the whole structure becomes more sophisticated with each cycle. It is a living system. It remembers everything. It builds on itself.

NotebookLM does allow a feedback loop of sorts: chats can be saved as notes, and notes can be converted into sources at any time, effectively feeding your Q&A back into the corpus. This is closer to Karpathy’s write-read-rewrite loop than it might first appear. But the key difference is that this loop is manual and deliberate — you decide what to save and promote. In Karpathy’s system, the LLM automatically files answers back into the wiki, runs health checks unprompted, and incrementally updates the compiled structure as new raw sources arrive. One is a garden you can choose to tend; the other tends itself. Sources in NotebookLM are also static by default — if a document changes, you manually remove the old version and upload the new one — and there is no autonomous mechanism that audits the notebook overnight, surfaces gaps, or suggests new connections across the whole corpus without being asked.

A good analogy: Karpathy’s system is a garden you tend over years — it grows richer with each season, develops its own internal ecology, and surprises you with what volunteers in unexpected corners. NotebookLM is a very well-equipped library reading room. You bring your stack of books, work with them expertly, and when you leave, the room resets for the next visitor. Both are genuinely useful. Only one compounds.

## Ownership, and What It Implies

Karpathy’s system lives on your computer as plain text files you own outright. You can move them, back them up, run local models against them, hand them to a different AI tool in three years when something better exists. The knowledge infrastructure is yours, structured in a format — markdown — that will be readable by humans and machines for decades.

NotebookLM lives in Google’s cloud, structured on Google’s terms. For a writer building a long-term intellectual infrastructure — something that might compound across ten or twenty years of work — the question of who controls the filing cabinet is not trivial. Google products have been discontinued before. Terms of service change. And more subtly: when your knowledge lives inside someone else’s product, the shape of that product begins to shape how you organize your thinking. You think in notebooks, in sources, in the formats the tool supports. Karpathy’s system, by contrast, is just files. It has no opinions about how you should think.

## The Seductive Multimedia Layer

The features that made NotebookLM go viral — the podcast audio overviews, the video explainers, the flashcards and quizzes — deserve a closer look from a writer’s perspective, because they are not all equal in what they offer.

The audio podcast feature is genuinely remarkable as a piece of technology — two AI hosts discuss your uploaded biosemiotics papers in a warm, conversational tone, interrupting each other, building on each other’s points. But for a writer, this is arguably the most dangerous feature of all. It optimizes for effortless consumption. You listen while commuting. The material washes over you in a pleasantly organized way. You feel informed. But you have done none of the work of formulation, none of the hormetic resistance that builds real understanding. It is the intellectual equivalent of watching a documentary about a country versus actually going there. Enjoyable, efficient, and not quite the same thing.

Flashcards and quizzes are more honest in what they do: they test memorization of content the system has already synthesized. This is useful for students who need to pass exams on material defined by someone else. For a writer whose goal is original synthesis, memorizing an AI-generated summary is the wrong target entirely. You don’t need to remember the AI’s formulation — you need to build your own.

The mind map is the genuinely interesting feature for serious intellectual work. It generates an interactive visual graph of concepts in your sources, which you can expand node by node, each sub-topic linking back to the specific papers that discuss it. Used correctly, the mind map is not a destination but a provocation — a way to see the terrain before you walk it yourself. If it surfaces a connection you hadn’t noticed, or a gap where the map goes quiet, and that observation sends you back to your sources or to your own writing with a new question, it has done valuable work. Used incorrectly — as a substitute for building your own conceptual map through reading and writing — it short-circuits the very process that generates original thought.

## Where Each Tool Belongs in a Writer’s Workflow

Think of the two tools as occupying different moments in the research-to-writing arc. NotebookLM excels at rapid domain entry: you have a new topic, you don’t know the landscape yet, you upload a dozen papers and let it generate a mind map and a podcast overview to get oriented. This is the reconnaissance phase. It is fast, low-friction, and genuinely useful for building a preliminary map before you decide which territory deserves deeper work.

Karpathy’s system belongs at the next stage: the sustained, multi-month or multi-year engagement with a domain where you want your knowledge infrastructure to grow and compound alongside your thinking. It requires more setup, demands technical comfort, and gives you something NotebookLM never will: a persistent, locally-owned, self-improving knowledge base that accumulates the intellectual investment of a serious research project.

Neither, however, addresses the deepest need of the writer: the stage where you must stop consuming other people’s synthesized knowledge and start building your own argument in your own voice. For that, we need to look at a very different tradition — one that predates AI by half a century, and whose core insight neither of these tools has yet replaced.

## Part V: Niklas Luhmann’s Zettelkasten

To understand what Karpathy is doing and what it might be missing, it helps to look at the most famous personal knowledge system in intellectual history: the Zettelkasten of the German sociologist **Niklas Luhmann**.

Luhmann was one of the most prolific social theorists of the twentieth century, producing over 70 books and 400 articles across a career that spanned four decades. When asked how he managed to produce so much, his answer was always the same: he didn’t do it alone. He had a conversation partner — his **Zettelkasten**.

A Zettelkasten (literally “slip box” in German) is a system of index cards, each containing a single idea, each with a unique address, each linked by hand to related cards. Luhmann’s contained roughly 90,000 cards by the time he died. But the number is less interesting than the method.

## The Luhmann Method

When Luhmann read something interesting, he would do two things. First, he wrote a bibliographic note on a separate card — essentially a citation with a brief summary of the source. This is his raw/ folder equivalent. Second, and crucially, he would write a Zettel: a new card, in his own words, expressing what the idea meant to him and how it connected to other ideas he was already thinking about. He would then give this card a unique address — not a simple sequential number, but a branching alphanumeric code like 1/1a/3b — that encoded where in the conceptual neighborhood this thought lived. And he would add manual links to other cards it connected with.

He was explicit that simply copying quotes was useless. The act of rewriting — of translating someone else’s idea into your own formulation — was where understanding actually happened. The Zettelkasten accumulated not a library of sources, but the evolving structure of Luhmann’s *own* thought.

## Where Karpathy and Luhmann Align

The surface resemblance between the two systems is real and worth taking seriously. Both separate raw sources from processed knowledge. Both treat the links between ideas as more valuable than the ideas in isolation. Both are designed to compound — the more you put in, the more generative the outputs become. And both are explicitly not filing cabinets: they’re designed to surprise you, to surface unexpected connections, to “talk back.”

Karpathy’s health checks that surface “candidates for new articles” and his Q&A answers being filed back into the wiki are genuinely Luhmannian in spirit. The system doesn’t sit still. It grows, it self-audits, it generates new questions from its existing contents.

## Where They Fundamentally Diverge

But here the similarity ends, and the difference goes all the way down.

For Luhmann, the act of writing the Zettel was not a step in the process of building a knowledge base. *It was the process of thinking.* The friction of having to express someone else’s idea in your own words — the resistance you feel when the translation doesn’t quite work, when your formulation exposes a gap in your understanding — that friction was not inefficiency to be removed. It was the signal that genuine integration was happening.

Karpathy’s system removes this friction entirely by design. The LLM does the writing. Karpathy contributes curation and questions. The wiki accumulates a sophisticated, synthetic intelligence about a domain. But it is not, in any deep sense, Karpathy’s intelligence. It is an LLM’s synthesis of sources Karpathy chose to include. For Luhmann, this would be a category error: you have built an excellent library, but you have not done any thinking.

A useful analogy: imagine you wanted to get fit. One approach is to hire a personal trainer who does the physical exercise on your behalf, then reports to you what it felt like. You gain a detailed map of what fitness involves — the muscle groups, the progression, the principles — but your body has done none of the work. Luhmann’s Zettelkasten is the exercise. Karpathy’s wiki is the report from the trainer.

The second deep difference is what we might call structural ownership. Each of Luhmann’s Zettels had an address he assigned himself — and the addressing system was meaningful. Card 1/1a/3b lives in a specific conceptual neighborhood. Luhmann knew where things lived because he had placed them there deliberately. He carried a mental model of the structure of his own knowledge. Karpathy’s system outsources this structural cognition to the LLM’s index files and Obsidian’s graph renderer. You don’t need to know where things live. You just query. This is more powerful for retrieval — but it may be weaker for the kind of deep structural understanding Luhmann was cultivating.

Third: Luhmann maintained one Zettelkasten his entire life. The value came from 40 years of a single mind’s encounters with ideas accumulating in one place, building density and unexpected connections across decades. Karpathy’s system seems oriented toward domain-specific wikis built for specific research questions. This makes it a powerful research tool. It makes it a weaker lifetime intellectual companion.

## Part VI: What This Means for Writers

All of the above becomes especially sharp when we ask: what does Karpathy’s system offer a writer? Not a researcher who happens to publish papers, but someone whose primary goal is to write essays, arguments, books — to produce thinking in the form of prose that a reader will experience?

The honest answer is: it offers a great deal for some stages of the work, and potentially undermines the most important stage.

## Where It Genuinely Helps

For domain entry — getting up to speed on an unfamiliar field — the system is genuinely powerful. If you’re writing an essay about, say, the philosophy of biology and you need to understand the landscape of ideas in biosemiotics, having an LLM compile 100 interlinked articles from your curated sources gives you a working map of the territory in a fraction of the time it would take to build that map by reading alone. The graph of backlinks surfaces structural relationships you might have missed reading sequentially. The health checks point you toward gaps you didn’t know existed.

For identifying connections across sources — noticing that an idea in a 2003 paper rhymes with a claim in a 2025 paper — the compiled wiki does something a human reader working linearly cannot easily do. You’d need to hold both in working memory simultaneously. The wiki makes these structural connections visible at a glance.

For research conversations — asking “what do these sources collectively say about X?” and getting a synthesized answer — the system is far superior to searching a folder of PDFs. The Q&A loop produces genuine synthesis, not just retrieval.

## The Hormetic Resistance: Why Friction Is the Writer’s Friend

Here we need to introduce a concept from biology: hormesis. Hormesis is the phenomenon where a small dose of something stressful — exercise, heat, mild toxins — makes an organism stronger, while removing all stress leaves it weaker. The muscle grows because it was made to struggle. The immune system learns because it was exposed to challenge.

The friction a writer encounters when trying to express a difficult idea in their own words is hormetic. It is not a bug in the process of thinking — it is the mechanism of thinking. When your sentence breaks down halfway through because you realize you don’t actually understand the concept you’re trying to explain, that breakdown is the most valuable moment in the writing session. It tells you exactly where your understanding ends. It forces you to rebuild the idea more carefully. The resistance is the growth.

Karpathy’s system, by design, eliminates this resistance. The LLM writes fluent, well-organized synthesis. There is no breakdown. There is no moment where the language reveals a gap in understanding, because the LLM doesn’t have gaps — it has confident prose covering whatever territory the sources provided. The writer who reads this prose may feel they understand the topic. They may have an excellent map. But they have not done the hormetic work of building the understanding in their own conceptual architecture.

Consider a concrete case. A writer is exploring the idea that biological cells interpret their environment — that interpretation is not just a human or animal phenomenon but a fundamental feature of life. They drop thirty papers into the raw folder. The LLM compiles a beautiful wiki: articles on biosemiotics, on Peirce’s sign theory applied to molecular processes, on Hoffmeyer’s code duality, on the epistemic cut between the physical and the symbolic. The writer reads these articles and feels fluent in the domain.

But then they sit down to write their own essay. And they find they don’t know where to start. Because the wiki has organized the domain — it has given them a map — but it has not given them an argument. It has not given them a position. It has not given them the particular angle through which this writer, with this sensibility and these preoccupations, sees something worth saying. That angle only emerges through the struggle of writing. The moment when you try to write your first sentence and it collapses is the moment your real thinking begins.

## Writing Is Thinking, Not Reporting

The deepest point here is one that experienced writers know but is easy to forget: writing is not the final step in a thinking process that has already happened. ***Writing is where the thinking actually occurs.***

When you sit down to write an essay and you know roughly what you want to say, the act of writing doesn’t transcribe your pre-existing thoughts — it discovers what you actually think. The essay finds its argument in the process of being written. Sentences that seemed clear in your head become confused on the page; the confusion points to real confusion in the thought. Ideas that seemed separate turn out to be the same idea; ideas that seemed connected turn out to be in tension. The page is a thinking machine, and it only works when you are genuinely struggling with something you haven’t yet resolved.

This is why the novelist **E.M. Forster** ’s line has stayed in circulation for a century: “How do I know what I think until I see what I say?” The act of saying is not reporting on knowing — it is producing knowing. The sentence you write is not a container for an idea you already had; it is the idea taking form for the first time.

![](https://substackcdn.com/image/fetch/$s_!kbUK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F465ee98c-74ce-4ebc-b5e2-bb3c43d0e14d_1376x768.png)

A wiki compiled by an LLM cannot participate in this process, because the LLM has no stake in the thinking. It has synthesized what the sources say. It has not struggled with what you, specifically, believe or what angle on this domain would be genuinely your own. It has given you a base camp. The mountain is still unclimbed.

## A Hybrid That Preserves What Matters

The most useful approach for a writer is a hybrid that takes the best of both systems. Use Karpathy’s architecture for the raw and mapping layers: let the LLM build the interconnection graph, surface gaps, maintain the index, identify unexpected cross-source connections. This is domain scaffolding, and the LLM does it better than any human could.

But keep the synthesis layer human. When the LLM shows you that two ideas are structurally connected, don’t read its synthesis article. Write your own. Take the connection it has surfaced and struggle with it in your own words. What does this connection actually mean? Does it hold up? Where does it break down? What would it imply if it were true? This is where your voice and your argument live.

You might also reorient the health check mechanism. Instead of having the LLM resolve inconsistencies between articles — which produces tidy, premature closure — have it surface the inconsistencies and stop there. “Here are three things in your corpus that seem to be in tension.” The tension is the gift. The writer’s job is to sit with it until something new emerges from the pressure.

In this configuration, the wiki is not the output of your thinking. It is the well-organized input to it. The scaffolding, not the building. The map of the territory you’re about to enter on foot, knowing the map is not the same as walking the ground.

## Conclusion: Two Different Bets on What Knowledge Is For

Karpathy and Luhmann are ultimately making different bets about what a personal knowledge system is for.

**Karpathy’s bet is that the bottleneck is synthesis and retrieval** — that if you can build a system that rapidly organizes and connects a large domain of sources, you can move faster, ask better questions, and build on a richer foundation than any individual working alone. This is a bet on knowledge as infrastructure. It’s powerful, and for many purposes — research, decision-making, domain mastery — it is exactly right.

**Luhmann’s bet is that the bottleneck is understanding** — that the value of a knowledge system is not how much it knows but how deeply it has been integrated into a single mind that can generate new thoughts from it. The Zettelkasten was not infrastructure for knowledge retrieval. It was a technology of thinking, designed to keep a mind in productive friction with its own prior work across a lifetime.

For writers, Luhmann’s bet is closer to the truth — but Karpathy’s tools are too useful to ignore. The synthesis is: use the machine to build the map, then insist on walking the territory yourself. Let the LLM handle the compilation. Reserve the thinking for yourself.