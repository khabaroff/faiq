---
title: P3 2026 05 03 Cowork Plugins Scheduled Tasks
slug: p3-2026-05-03-cowork-plugins-scheduled-tasks
source_url: https://anthropic.skilljar.com/introduction-to-claude-cowork/444169
source_type: article
fetched_at: 2026-05-13
lang: en
---

## Header Navigation

[Anthropic Academy](https://www.anthropic.com/learn) [Courses](https://anthropic.skilljar.com/) 

  

### ⁠

**Estimated time:** 15 minutes

### Learning objectives

- Explain what a plugin is and what's inside it
- Install a plugin that matches your role
- Understand skills as the building blocks plugins are made of

---

### What a plugin is

![Plugins: turn Cowork into a specialist for your role](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773939289%2Fslide-10-plugins.1773939289619.png)
> **Image OCR (auto):**
> **Type:** other
> **Text:** Plugins
> Turn Claude into a specialist
> 
> Plugins bundle skills, connectors, and sub-agents into a single
> package. Install one and Claude becomes an expert for your role.
> 
> Sales
> Research prospects,
> prep deals, follow
> your playbook
> 
> Marketing
> Draft content, plan
> campaigns, manage
> launches
> 
> Product
> Write specs, prioritize
> roadmaps, track
> progress
> 
> Finance
> Analyze financials,
> build models, track
> metrics
> 
> Support
> Triage issues, draft
> responses, surface
> solutions
> 
> Data
> Query, visualize, and
> interpret datasets
> 
> Legal
> Review docs, flag
> risks, track
> compliance
> 
> Productivity
> Tasks, calendars,
> daily workflows
> 
> 15 open-source plugins available to customize and build upon
> **Description:** This is a marketing-style webpage graphic about Claude plugins. It presents a large headline and supporting text, followed by a grid of cards for different roles such as Sales, Marketing, Product, Finance, Support, Data, Legal, and Productivity. A small footer note mentions that 15 open-source plugins are available to customize and build upon.


Overview

Plugins give Cowork domain expertise. Each one comes with built-in knowledge and workflows for a specific function, so Claude approaches your task the way a specialist would.

A plugin is a bundle—several pieces packaged together for a role or domain:

- **Skills** — Instructions for handling specific workflows. Claude draws on them automatically, or you invoke them with `/` in the prompt. *Example: how to structure a deal brief, `/prep-call`, `/weekly-report`.*
- **Connectors** — Reach the systems where the work happens. *Example: your CRM, your docs, your messaging.*
- **Subagents** — Parallelize specialized work. *Example: one agent per account in a book-wide review.*

Open-source plugins are available for most knowledge-work roles: sales, marketing, product, finance, legal, operations, customer support, data, and more. They work as-is and can be modified.

### Installing a plugin

![Installing plugins: browse, install, customize](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1774046474%2Fslide-11-installing-plugins.1774046473979.png)
> **Image OCR (auto):**
> **Type:** other
> **Text:** How-to
> Installing & using plugins
> 
> 1
> Browse available plugins
> Browse plugins in the Customize area to find ones for
> your role or workflow.
> 
> 2
> Install with one click
> Plugins activate immediately — no restart required.
> 
> 3
> Customize and extend
> Plugins are open-source. Adjust skills, connectors, and
> sub-agents to match your team's needs.
> 
> What's inside a plugin?
> Each plugin bundles skills (how Claude works), connectors
> (which tools it accesses), and sub-agents (specialized
> helpers) into one package.
> **Description:** This is a how-to infographic about installing and using plugins. It presents three numbered steps on the left and a simple line illustration on the right. A callout box at the bottom explains what a plugin contains.


Overview

1. **Browse.** Plugins live in Cowork's **Customize** area. Find one that matches what you do.
2. **Install.** One click. The plugin is active immediately.
3. **Customize.** Once installed, the plugin is a folder on your machine. Everything in it is readable and editable.

### What's inside

A plugin is just a folder. The structure looks something like this:

> ```js
> sales-plugin/
> ├── plugin.json         ← manifest: name, description, dependencies
> ├── skills/
> │   ├── deal-brief/     ← how to structure a deal brief
> │   ├── territory/      ← how to build a territory report
> │   └── prep-call/      ← /prep-call in the slash menu
> └── agents/
>     └── account-sweep.md ← subagent for per-account work
> ```

Every file is plain text. To change how a skill works, open its file and edit it. To add a new skill, add a folder under skills. There's no build step—Cowork reads the folder directly.

### About skills

You'll notice skills show up a lot—they're the core building block inside plugins. A skill is a markdown file that teaches Claude how to handle one thing: a workflow, a format, a process.

Skills aren't specific to Cowork. They work across Claude's surfaces—in chat, in Claude Code, anywhere Claude runs. A plugin is the Cowork-specific way of bundling skills with the connectors they need to do a job.

![](https://www.youtube.com/watch?v=bjdBVZa66oU)

If you want to go deeper on skills specifically:

- [Skills video course on YouTube](https://www.youtube.com/playlist?list=PLmWCw1CzcFim_hkruZSlABOUOAAQ5JMyo) — six-part walkthrough
- [What are Skills](https://support.claude.com/en/articles/12512176) — Help Center reference
- [Teach Claude your way of working](https://claude.com/resources/tutorials/teach-claude-your-way-of-working-using-skills) — tutorial on encoding your own processes
- [Introduction to Agent Skills](https://anthropic.skilljar.com/introduction-to-agent-skills) — full course

### Put it into practice

1. Open Cowork's Customize area and browse plugins.
2. Install the plugin closest to your role.
3. Find the installed plugin folder and open one of the skill files. See that it's readable text, written the way you'd brief a teammate.

### Learn more about plugins

- [Plugin directory](https://claude.com/plugins) — browse all plugins, Anthropic and community-built
- [Use plugins in Cowork](https://support.claude.com/en/articles/13837440-use-plugins-in-cowork) — Help Center guide to installing and setup
- [How to customize plugins in Cowork](https://claude.com/resources/tutorials/how-to-customize-plugins-in-cowork)
- [Build a plugin from scratch](https://claude.com/resources/tutorials/how-to-build-a-plugin-from-scratch-in-cowork)
- [Cowork plugins announcement](https://claude.com/blog/cowork-plugins)
- [Knowledge-work plugins on GitHub](https://github.com/anthropics/knowledge-work-plugins)
- [Financial-services plugins on GitHub](https://github.com/anthropics/financial-services-plugins)

### What's next

Next: scheduled tasks. Once you have a task that works well—whether it's a plugin skill or a prompt you wrote—you can set it to run on a schedule without prompting each time.

#### Feedback

Share your feedback [here](https://forms.gle/sY9ou5fqZBd3TjHF8).

#### Acknowledgments and license

*Copyright 2026 Anthropic. All rights reserved.*

---


## Header Navigation

[Anthropic Academy](https://www.anthropic.com/learn) [Courses](https://anthropic.skilljar.com/) 

  

## Scheduled tasks

### ⁠

**Estimated time:** 8 minutes

### Learning objectives

- Set up a scheduled task to run work on a recurring cadence
- Understand how scheduled tasks behave when the app is closed or the machine is asleep

---

### Running work on a cadence

![Scheduled tasks: how they work and what they need](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773940406%2Fslide-12-scheduled-tasks.1773940405986.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Automation
> Scheduled & recurring tasks
> Set up tasks that Claude runs automatically or on demand —
> something that isn’t possible in regular chats outside of Cowork.
> How to schedule
> Type /schedule in any Cowork task, or click “Scheduled” in the left sidebar to create and manage tasks.
> Set your cadence
> Run tasks daily, weekly, or on any custom schedule. Great for recurring reports, data syncs, and
> monitoring.
> Requirements
> • Computer must be awake
> • Claude Desktop must be open
> • Active internet connection
> Example
> “Every Monday at 9am, pull my calendar and draft a weekly priorities email.”
> **Description:** A documentation-style UI page about automation features for scheduled and recurring tasks. It explains how to schedule tasks, set cadence, and lists requirements in separate card-like sections. An example task prompt is shown at the bottom.


Overview

Scheduled tasks run any Cowork task automatically on a cadence you set—hourly, daily, weekly, or custom. The task can be anything: a prompt you've written, a plugin skill, or a workflow you've refined. Once you have something that works well, you can stop prompting for it each time.

> "Every Monday at 9am, pull my calendar and draft a weekly priorities email."

### Setting one up

Type `/schedule` in any Cowork conversation, or use the scheduled tasks area in the sidebar. Claude walks you through the cadence, the folder, and what the output should look like.

There's an approval step, since you're signing off on something that will run repeatedly. Once approved, the task runs on its own while the desktop app is open. If your computer was asleep or the app was closed when a task was due, Cowork runs it as soon as you're back and lets you know it was delayed.

If you create a scheduled task from inside a project, it appears alongside that project's other scheduled work—a quick way to see everything running on a cadence for one piece of work.

### Managing scheduled tasks

From the scheduled tasks area, you can review past runs, edit the instructions or cadence, pause a task, or trigger it on demand. Any connectors and plugins you've set up are available to scheduled tasks too.

See [more on scheduled tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-cowork) in the Help Center.

### A common pattern

Scheduled tasks and skills compose naturally. A skill encodes *what* to do; a scheduled task decides *when*. A briefing skill scheduled for 8am weekdays means the briefing is waiting every morning.

But you don't need a skill to schedule something. Any task that works well is a candidate.

### Put it into practice

Think of something you currently do on a cadence—a weekly status pull, a daily folder check, a recurring report. You don't have to schedule it yet. Just note it: once you've run it successfully once in Cowork, scheduling it is one more step.

### What's next

In the next module, you'll see common Cowork use cases in practice: working with files and documents, and research and analysis at scale.

#### Feedback

Share your feedback [here](https://forms.gle/sY9ou5fqZBd3TjHF8).

#### Acknowledgments and license

*Copyright 2026 Anthropic. All rights reserved.*