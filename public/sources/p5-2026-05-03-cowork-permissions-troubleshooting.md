---
title: P5 2026 05 03 Cowork Permissions Troubleshooting
slug: p5-2026-05-03-cowork-permissions-troubleshooting
source_url: https://anthropic.skilljar.com/introduction-to-claude-cowork/444174
source_type: article
fetched_at: 2026-05-13
lang: en
---

## Header Navigation

[Anthropic Academy](https://www.anthropic.com/learn) [Courses](https://anthropic.skilljar.com/) 

  

### ⁠

**Estimated time:** 10 minutes

### Learning objectives

- Describe the safety boundaries Cowork operates within
- Manage your usage allocation effectively
- Build the habit of reviewing outputs before acting on them

---

### Permissions and safety

![Permissions and safety: the boundaries Cowork works within](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281054%2Fslide-16-permissions-safety.1773281054304.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Security
> Permissions & safety
> 
> VM isolation
> Claude operates in a virtual machine on your
> computer, separate from your main operating
> system.
> 
> Controlled file access
> You grant permission for which files Claude
> can access. Review actions before allowing
> changes.
> 
> Network permissions
> Cowork respects your network egress
> permissions. You control Claude's internet
> access level.
> 
> Deletion protection
> Claude requires explicit permission before
> permanently deleting any files. You always
> approve first.
> 
> Important
> Cowork stores conversation history locally on your computer. Activity is not captured in Audit Logs,
> Compliance API, or Data Exports. Do not use Cowork for regulated workloads.
> **Description:** A clean security information page titled “Permissions & safety” with four feature cards arranged in a grid. The cards describe VM isolation, controlled file access, network permissions, and deletion protection. A highlighted “Important” note at the bottom warns that conversation history is stored locally and activity is not captured in certain logs or exports.


Overview

Cowork can read and write real files and connect to real systems. Here are the boundaries that shape how that works.

- **Isolated execution** — Work runs in an isolated environment on your computer, separate from your operating system. Cowork can't reach what it hasn't been granted.
- **Controlled file access** — You decide which folders Cowork can see. No grant, no access.
- **Network policies respected** — Cowork follows your organization's network rules. Restricted environments stay restricted.
- **Deletion is gated** — Permanent deletion requires your explicit approval. You'll always see a prompt first.

#### One thing worth knowing up front

Cowork conversation history is stored locally on your machine. Check your plan's documentation for current details on audit logging and compliance features—particularly if you have workloads with regulatory requirements.

### Reviewing what Cowork did

Before you send an output onward or act on a result, review it. The more polished an output looks, the more a second look is worth—Cowork's confidence is the same whether the work is right or wrong. Your review catches the difference.

The habit: **open the file. Check a number. Follow one thread of reasoning.**

### Managing usage

![Usage limits: making the most of your allocation](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281054%2Fslide-17-usage-limits-tips.1773281054721.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Best practices
> Usage limits & tips
> 
> Cowork tasks consume more usage than standard chats because multi-
> step tasks are compute-intensive. Here’s how to get the most from your
> allocation.
> 
> Batch related work
> Group related tasks into a single session to reduce overhead.
> 
> Chat for simple tasks
> Use standard chat for quick questions that don’t need file access or long execution.
> 
> Monitor your usage
> Check Settings → Usage to track how much of your allocation you’ve used.
> **Description:** A clean help/documentation page titled “Usage limits & tips” explains how cowork tasks use more allocation than standard chats. Three tip cards advise batching related work, using chat for simple tasks, and monitoring usage in Settings. The layout is minimal with icons and large white cards on a light background.


Overview

Cowork uses more of your allocation than chat does—multi-step, long-running work is more compute-intensive than a single turn. A few habits help you spend it well:

- **Batch related work.** Starting a fresh session has overhead. If you have several related tasks, do them in one session rather than separate ones.
- **Use chat for tasks that fit it.** If a task doesn't need your files, your connected tools, or a real output file, chat is often faster and less resource-intensive. The question from Lesson 1—does this need my files, tools, or a real output?—is also a good usage question.
- **Monitor where you stand.** Cowork's settings include usage visibility. Check in periodically, especially as you're building habits.

#### Choosing the right model

Which model you use also affects consumption. Claude models come in three capability tiers— **Opus**, **Sonnet**, and **Haiku** —and they trade off capability against cost. Opus handles the most complex multi-step work and uses the most allocation. Haiku is the quickest and lightest. Sonnet sits in the middle as a sensible default for everyday tasks.

Match the model to what the task needs rather than defaulting to the highest option for everything.

For more on how the tiers differ and when each one fits, see [Choosing the right Claude model](https://claude.com/resources/tutorials/choosing-the-right-claude-model). For how usage and allocation work across plans, see [plans and pricing](https://claude.com/pricing).

### Lesson reflection

- Do you have any workflow where the audit and compliance characteristics of Cowork matter? If so, check your plan's current documentation.
- Are you running tasks in Cowork that would fit just as well in chat? That's an easy place to save allocation.
- When did you last open a Cowork output and actually check something in it before sending it onward?

### What's next

The final lesson: quick troubleshooting for common issues, and the sequence of next steps to build on what you've learned.

#### Feedback

Share your feedback [here](https://forms.gle/sY9ou5fqZBd3TjHF8).

#### Acknowledgments and license

*Copyright 2026 Anthropic. All rights reserved.*

---


## Header Navigation

[Anthropic Academy](https://www.anthropic.com/learn) [Courses](https://anthropic.skilljar.com/) 

  

### ⁠

**Estimated time:** 10 minutes

### Learning objectives

- Recognize and resolve common issues people encounter with Cowork
- Know what to do next: install, build, schedule, share
- Know where to go for help beyond this course

---

### Common issues and how to approach them

![Troubleshooting: common questions](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281055%2Fslide-18-troubleshooting.1773281055077.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Troubleshooting & resources
> Common questions
> 
> “Preparing your workspace”
> Expected — Cowork is getting its environment
> ready. Give it a moment.
> 
> Claude stopped working
> Make sure the desktop app stayed open. If
> your computer went to sleep, the session may
> have ended.
> 
> Hitting usage limits
> Cowork uses more tokens than chat. Reserve it
> for complex, multi-step work. Batch related
> tasks.
> 
> Files not appearing
> Check that you’ve granted Claude the right file
> access permissions. Verify the output location.
> **Description:** A help or troubleshooting page titled “Common questions” is shown. It contains four white cards with short FAQ-style issues and explanations about workspace preparation, Claude stopping, usage limits, and missing files. The layout is clean and minimal on a light background.


Overview

#### Cowork is preparing your workspace

Cowork is getting its environment ready before starting. This can take a little longer than a regular chat session starting up. Give it a moment—this is expected, particularly the first time or after an update.

#### A task stopped mid-run

The most common cause: the desktop app was quit mid-task. Sleeping the computer is fine—the session survives and picks back up when you wake it. Quitting the app pauses the task. Check that Claude Desktop is open; if it is, check your connection.

#### Running into usage limits

Cowork uses more allocation than chat, and long-running tasks on more capable models use the most. See Lesson 10: batch related work, use chat for tasks that fit it, match your model choice to what the task needs.

#### Can't find a file Cowork said it made

The output may have landed in a different folder than you expected, or the folder Cowork was pointed at wasn't the one you thought. Check the working folder Cowork was using. Verify folder access in settings. Ask Cowork directly where it wrote the file.

### What to do next

![Now it's your turn: install a plugin, run a real task](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6oz04skclb1pbkcboeiosbn5o%2Fpublic%2F1773281055%2Fslide-19-now-its-your-turn.1773281055567.png)
> **Image OCR (auto):**
> **Type:** other
> **Text:** Now it's your turn
> 
> Pick a plugin that matches your role. Install it in
> seconds, then hand Cowork a real task from
> your week.
> 
> From Claude Desktop
> Cowork → Customize → Skills →
> Browse plugins
> 
> Install any of the 15 open-source
> plugins with one click.
> 
> From GitHub
> github.com/anthropics/knowledge-
> work-plugins
> 
> Browse source, customize for your
> team, or build your own plugin from
> scratch.
> **Description:** This is a promotional webpage section with a large headline and supporting text about choosing and installing a plugin. Two centered cards below provide options from Claude Desktop and GitHub, including installation instructions and a repository URL. The layout is clean and minimal with a light background and rounded white panels.


Overview

The goal: have a skill you trust running on a schedule. The steps to get there:

1. **Install a plugin.** Browse the library, pick one that matches your role, install it. Open the plugin folder and read one of the skill files to see what a skill actually looks like.
2. **Run something real.** Pick a task from your actual work—something that matters, even if it's small. What you're looking for: the moment you come back from doing something else and the finished file is there.
3. **Make a skill.** If you produce branded output, build a brand-guidelines skill. Otherwise, the next time you run a task and realize you'll run it again, save that session as a skill.
4. **Schedule it.** Put the skill on a schedule. If the app is closed when the task is due, it runs as soon as you reopen.
5. **Share it.** Package the skill for a teammate, or on Team and Enterprise plans, talk to your admin about making it available more broadly.

Take these at whatever pace fits your work. The sequence matters more than the timing.

### Where to go from here

- **Setup and troubleshooting** — [Getting started with Cowork](https://support.claude.com/en/articles/13345190)
- **Task ideas** — [Cowork use-case gallery](https://claude.com/resources/use-cases/)
- **Plugin source and customization** — [github.com/anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
- **Building lasting habits for working with Claude** — [AI Fluency course](https://www.anthropic.com/ai-fluency)

### Lesson reflection

- What's the first real task you'll hand to Cowork?
- Which plugin matches what you do? Is it installed?
- What workflow—one you already run manually—would save you the most time if it ran on a schedule?

### Congratulations

You've completed the Cowork end user training. You know how to describe a task, review a plan, let work run, and review the output. You know where Cowork fits in your work alongside chat. You know how to teach it something once so you don't have to explain it again.

Now pick something real and hand it over.

#### Feedback

We'd love to hear how you're using Cowork in your work. Share your feedback [here](https://forms.gle/sY9ou5fqZBd3TjHF8).

#### Acknowledgments and license

*Copyright 2026 Anthropic. All rights reserved.*