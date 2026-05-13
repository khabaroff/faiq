## 2026-05-03T00:46:35+04:00

https://anthropic.skilljar.com/introduction-to-claude-cowork/444166

## Header Navigation

[Anthropic Academy](https://www.anthropic.com/learn) [Courses](https://anthropic.skilljar.com/)

### ⁠

**Estimated time:** 15 minutes

### Learning objectives

- Describe a task to Cowork clearly enough to get a useful plan
- Steer the approach before work begins and while it runs
- Approach finished outputs with the right reviewing mindset

---

### The core loop

![Your first task: the four-step loop](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281048%2Fslide-06-your-first-task.1773281048833.png)
> **Image OCR (auto):**
> **Type:** other
> **Text:** Walkthrough
> Your first task
> 
> 1
> Describe the outcome you want
> Be specific. “Organize my Downloads by type and date”
> is better than “clean up files.”
> 
> 2
> Review Claude's plan
> Claude will share its approach before executing. Steer if
> needed.
> 
> 3
> Monitor or step away
> Watch progress in real time, or leave and come back
> when it’s done.
> 
> 4
> Get finished outputs
> Claude delivers results directly to your file system.
> **Description:** This is a walkthrough-style instructional graphic with a large title and four numbered steps in stacked cards. On the right is a simple illustration of a hand holding a key. The layout looks like a product guide or onboarding slide rather than a UI screenshot or technical diagram.


Overview

Claude proposes a plan and waits for your approval before taking action. You adjust if needed, approve, and Claude executes. This is the pattern for every Cowork task.

#### 1\. Describe what you want back

A prompt works well when it gives Claude **what to look at**, **what you want back**, and **where it should go**. You don't have to engineer a perfect prompt—Claude will ask follow-up questions for whatever you leave out.

> "Three of our coverage companies reported earnings this week. The transcripts are in my folder along with our model and last quarter's note. Read the transcripts against our model, check what the team's been saying in #research-desk on Slack, and update the research note. Flag anything that changes our assumptions."

#### 2\. Answer a few questions

Based on your prompt and what it found, Claude asks a few questions to get the output right—which approach to take, what to prioritize, how the finished work should look. Pick one of the options Claude offers, or type your own answer.

#### 3\. Step away—or step in

A progress panel shows each step: which files Claude's reading, what it's building. For large tasks, Claude breaks the work into parts and handles them at once. Leave it and come back, or type in the chat to redirect if you see something heading somewhere you didn't mean.

#### 4\. Open your finished work

The result lands where you pointed it—saved in your folder alongside the files Claude read. If the prompt had asked for something different ("draft this as an email in Gmail" or "save to the shared Drive folder"), it would show up there instead.

Treat the result as a draft. Read it the way you'd read a first pass from a capable colleague: good work that's still yours to shape before you send it on.

### A few things that shape the experience

![Under the hood: how Cowork runs your tasks](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281049%2Fslide-07-under-the-hood.1773281049301.png)
> **Image OCR (auto):**
> **Type:** diagram
> **Text:** Under the hood
> How Cowork runs your tasks
> 
> Cowork runs directly on your computer, giving Claude access to the
> files you choose to share. Code runs safely in an isolated virtual
> machine.
> 
> Analyzes
> request
> Reads your
> prompt and
> creates a
> structured plan
> 
> Breaks into
> subtasks
> Complex work
> is divided into
> smaller,
> manageable
> pieces
> 
> Executes in
> VM
> Work runs in an
> isolated virtual
> machine
> environment
> 
> Parallelizes
> Sub-agents
> coordinate
> multiple
> workstreams
> simultaneously
> 
> Delivers
> output
> Finished files
> are placed
> directly in your
> file system
> 
> Transparency built in
> Claude surfaces its reasoning at every step. You can jump in to course-correct or provide additional
> direction at any time.
> **Description:** This is an explanatory infographic about how Cowork handles tasks. It shows a five-step flow from analyzing a request to delivering output, with short descriptions under each step. A note at the bottom emphasizes built-in transparency and the ability to intervene during execution.


Overview

![During a task: what to expect](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281049%2Fslide-08-during-a-task.1773281049667.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** During a task
> What to expect
> 
> Progress indicators
> See what Claude is doing at each step — no black box.
> 
> Steering
> Jump in to course-correct or add context mid-task. Claude adapts on the fly.
> 
> Parallel work
> For complex tasks, Claude may coordinate multiple sub-agents working simultaneously.
> 
> Deletion protection
> Claude always asks for explicit permission before permanently deleting any files.
> 
> Step away anytime
> Tasks can run for extended periods. Monitor progress live or come back later — just keep Claude Desktop open.
> **Description:** A clean informational UI page titled “What to expect” with several stacked cards describing task behavior. Each card has a small icon and a short explanation about progress indicators, steering, parallel work, and deletion protection. A highlighted note at the bottom says tasks can run for extended periods and can be monitored live or later.


Overview

You don't need to know how Cowork works under the hood to use it. But a rough picture helps you write better prompts and recognize when a task is a good fit.

- **Subagents** — When a task has independent pieces, Cowork can spin up separate workstreams that run at the same time, each with its own job and its own fresh context. Comparing four vendors: one subagent per vendor, each researching pricing, integrations, and reviews without the others' material crowding its view. Results synthesize into one output. In practice: tasks too large to hold in one conversation can be split into pieces that each fit comfortably, and each piece gets focused attention—the vendor-three analysis isn't diluted by vendor-one's details.
- **Progress is visible** — A panel shows which step is active, which files are being read, what's being built. You can follow along or ignore it.
- **You can steer while it runs** — Type in the chat to redirect if something heads somewhere you didn't mean. No need to wait for it to finish.
- **Isolated environment** — Code runs and files get built in an isolated environment on your computer, separate from your main system, without touching anything you haven't granted access to.
- **Deletion is gated** — Cowork asks before permanently deleting files. You approve or decline.

### Walkthrough: a scattered folder becomes a finished deck

Here's the loop in practice. The shape is the same for any task where you're pulling from files to produce something finished.

#### The starting point

A project folder with the usual accumulation: meeting notes, a checklist, a timeline spreadsheet, some saved emails, a comparison matrix. Different formats, loosely organized.

The goal: turn this into a leadership-ready presentation.

#### Describe the task

> "Review everything in this folder and create a leadership presentation for the tooling review. Include the vendor evaluation results, timeline, business case, and open risks. Output a PowerPoint file."

#### Review the plan

Cowork shows its plan: read the files, synthesize the proposal, build the business case, generate the deck, review the result. If you want something added—say, a PDF alongside the PowerPoint—you can say so here.

#### Let it run

Watch if you want, or go to a meeting. The work continues.

#### Open the file

The deck is a real PowerPoint file. Charts are editable elements you can click into and adjust. It's a draft you can refine, starting from a place much closer to finished than assembling it yourself.

### Start small

Begin with tasks that have clear boundaries—organizing a folder, synthesizing a set of documents. Build your intuition for what Cowork handles well, then scale up.

### Put it into practice

Use the task you identified in Lesson 1. Point Cowork at the relevant folder, describe what you want back, and run through the loop.

### What's next

Next, you'll learn how to give Cowork context it reads every session—so you don't re-explain the same things each time.

#### Feedback

Share your feedback [here](https://forms.gle/sY9ou5fqZBd3TjHF8).

#### Acknowledgments and license

*Copyright 2026 Anthropic. All rights reserved.*

---

## 2026-05-03T00:46:46+04:00

https://anthropic.skilljar.com/introduction-to-claude-cowork/444167

## Header Navigation

[Anthropic Academy](https://www.anthropic.com/learn) [Courses](https://anthropic.skilljar.com/) 

  

### ⁠

**Estimated time:** 10 minutes

### Learning objectives

- Give Cowork context that carries across every session, without re-explaining each time
- Use a project's Instructions panel to tell Claude how to work
- Set global instructions for preferences that apply everywhere

---

### Why this matters

![Projects: context that carries across sessions](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1774046473%2Fslide-09-projects.1774046473208.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Customization
> Projects
> A dedicated workspace with its own files, context, instructions, and memory. Backed by a
> real folder on your computer.
> 
> What a project holds
> 
> Instructions — tone, formatting, rules for every
> task
> Scheduled tasks — recurring work scoped here
> Context — folder, linked Chat projects, URLs
> Memory — what you’ve worked on, scoped to this
> project
> 
> Three ways to start
> 
> Start from scratch — new folder, new context
> Import from chat — bring files and instructions
> over
> Use an existing folder — wrap a folder you
> already have
> 
> Global instructions (Settings → Cowork) still apply across all projects — for preferences that don’t change.
> **Description:** A clean documentation-style page titled “Projects” under the “Customization” section. It explains what a project contains and lists three ways to start a project. A highlighted note at the bottom says global instructions still apply across all projects.


Overview

Each Cowork task starts fresh—Claude doesn't carry conversation memory from one task to the next. The way context carries over is a **project**: a named workspace backed by a real folder on your machine, with instructions and memory that persist into every task you start inside it.

If you use projects in Chat, Cowork projects work similarly—but they live locally on your computer and are built around tasks. The memory is scoped differently too: Chat remembers across all your conversations; a Cowork project's memory stays inside that project.

Projects live in Cowork's sidebar. You can start one from scratch, import from a Chat project (files and instructions come over, sync stays one-way), or wrap a folder you already have on your machine. [Full setup guide](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-cowork).

#### What goes in Instructions

Once you're in a project, the right-hand panel has an **Instructions** section. What you put there is read in every task you start from that project. Some things that tend to be useful:

- **Who's involved** — names, roles, how to reach them, so "send this to Rachel" means something
- **Where things live** — "contracts are in./Contracts, old reports in Drive /archive/\[year\]"
- **Output preferences** — "drafts go in.docx, finals in PDF, save to the deliverables subfolder"
- **Project-specific rules** — "metric units throughout, cite the source for every number"

It doesn't need to be polished. A few lines is enough. The effect: shorthand starts working. Once Instructions says who's who and where things are, "send this to the client" and "file it where the Q3 report went" mean specific things.

Claude also reads everything in your project folder. For context you want Claude to maintain—running notes, a growing glossary, anything that evolves—put it in a file there. "Add what we just covered to my notes file" works on files; the Instructions panel is yours to set.

#### Global instructions

For preferences that don't change between projects—your role, default output formats, standing rules like "ask before deleting"—use global instructions. Set them in Settings → Cowork → Global Instructions. These apply to every Cowork task, inside a project or not.

### Check it's working

From inside your project, ask: "Tell me what you know about how I work here." You'll see whether Instructions and memory are being picked up, and what's missing.

### Put it into practice

Create a project for something you're actively working on—use an existing folder if you have one. Add a few lines to Instructions: who the key people are, where related files live, one output preference. Start a task inside it and notice the folder already set in the input bar.

### What's next

In the next module, you'll learn how plugins add domain expertise to Cowork—so it approaches your task the way a specialist in your function would.

#### Feedback

Share your feedback [here](https://forms.gle/sY9ou5fqZBd3TjHF8).

#### Acknowledgments and license

*Copyright 2026 Anthropic. All rights reserved.*