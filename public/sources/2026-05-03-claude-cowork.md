---
title: Claude Cowork
slug: 2026-05-03-claude-cowork
source_url: https://charliehills.substack.com/p/claude-cowork?r=llvd&utm_medium=ios&triedRedirect=true
source_type: article
fetched_at: 2026-05-13
lang: en
---

You think Claude is a chat box.

You type, it responds. That is claude.ai.

Cowork is something different. It lives on your desktop, reads your files, installs specialist plugins, and runs tasks while you sleep.

If you followed last week’s migration guide, your context is already inside Claude. This newsletter shows you what to do with it.

In this issue:

1. Six Cowork features with full setup prompts
2. Scheduled Tasks that run while you sleep
3. Where Cowork falls short

Everything in this newsletter is tested. I ran every workflow, hit every error, and documented what worked. If you are new here, welcome. If you have been reading for a while, thank you. Your subscription keeps this going.

---

Anthropic built Cowork by taking Claude Code, their agentic developer tool, and rebuilding it for non-developers (no terminal or command line required).

The workflow loop looks like this. You describe what you need. Cowork asks clarifying questions. You answer. You come back 20 minutes later to a finished document.

Here is the full workflow we are building today:

1. Set up your working folder and context files (File System Access)
2. Set standing rules so Claude knows your voice (Instructions)
3. Scrape your LinkedIn data and competitors with Apify (Connectors)
4. Align the post brief with Claude (AskUserQuestion)
5. Write the post with the Marketing plugin (Plugins)
6. Create a carousel brief and save it to Notion (Connectors)
7. Automate the research so it runs every morning (Scheduled Tasks)

Let’s go.

### Feature 1: File System Access

**Claude reads and writes files in a folder on your actual computer.**

![](https://substackcdn.com/image/fetch/$s_!AmZQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e5f57e2-676d-41e2-8cbe-5b8a4df2e430_901x504.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat
> Cowork
> Code
> 
> Let's knock something off your list
> Cowork is in research preview. Learn how to use it safely or give us feedback.
> 
> charlie_hills_prof
> ile.md
> 
> MD
> 
> daily-social-
> brieﬁng-06-03-
> 2026.md
> 
> MD
> 
> Ask me questions about what post I want to write about today.
> 
> Once you've gathered context write a /linkedin-post about it.
> 
> Downloads
> 
> Opus 4.6
> 
> Let's go →
> 
> Active tasks
> Clear all
> **Description:** A web app interface is shown with the Cowork tab selected alongside Chat and Code. The main panel invites the user to gather context from two markdown files and then write a LinkedIn post, with a prominent “Let’s go” button and model selector at the bottom. The page also shows a downloads control and faint footer text for active tasks.


Every other AI tool runs on uploads. You export something, drag it into a chat, wait, get output, download it, put it back. That whole loop is friction. Cowork removes it.

You select a folder. Claude reads everything inside it. When it creates something, it saves directly to that folder (no manual steps).

Claude reads your old reports and matches your formatting automatically. It pulls last month’s spreadsheet data to build this month’s. It references your brand guidelines mid-task without you mentioning them.

How to set it up:

1. Go to claude.com/download.
2. Download the desktop app for macOS or Windows.
3. You need a paid plan. Pro starts at $20/month.
4. Open the app, find the Cowork tab at the top.
5. Click “Work in a folder,” and point it at a local folder on your machine.

![](https://substackcdn.com/image/fetch/$s_!atRe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2d9779e-0d90-465e-98cb-231d641edb7b_990x791.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat
> Cowork
> Code
> 
> Let's knock something off your list
> Cowork is an early research preview. New improvements ship frequently. Learn more or give us feedback.
> 
> How can I help you today?
> 
> Work in a folder
> 
> Opus 4.6
> 
> Let's go →
> 
> Recent
> 
> Downloads
> /Users/charliehills/Downloads
> 
> Invoices
> /Users/charliehills/Downloads/Invoices
> 
> Desktop
> /Users/charliehills/Desktop
> 
> Documents
> /Users/charliehills/Documents
> 
> com~apple~CloudDocs
> /Users/charliehills/Library/Mobile Documents/com~apple~CloudDocs
> 
> Viral Reels
> /Users/charliehills/Downloads/Viral Reels
> 
> Content ideas + LI: Substack Export
> /Users/charliehills/Documents/Content ideas + LI: Substack Export
> 
> Charlie Hills Post Export
> /Users/charliehills/Downloads/Charlie Hills Post Export
> 
> Choose a different folder
> **Description:** This is a desktop app interface for a product called Cowork, showing a prompt to start working on something. A folder-selection dropdown is open with recent folders and file paths listed. The screen includes navigation tabs at the top and a primary action button labeled “Let’s go.”


Cowork does not carry memory between sessions the way claude.ai does. Every new session starts fresh. But you control what it reads at the start.

When you open a session, select the folder you want to work from. Cowork reads every file inside it. If you have a client folder with their brand voice, past posts, contact list, and working notes, all of that loads as context the moment you start. You do not need to re-explain anything.

This is the workaround for Cowork’s missing cross-session memory. Your files are the memory. The better your files, the less you repeat yourself.

Type /memory-management in any session to check what context is loaded. You can see which files Cowork has read, verify it has the right information, and spot gaps before you start working. Five seconds of checking saves you from realising halfway through a task that Cowork is missing half the brief.

![](https://substackcdn.com/image/fetch/$s_!mxbe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92f0b4e9-a2c0-4648-8efe-b617409f536a_2470x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Review daily tasks and plan
> 
> Chat  Cowork  Code
> 
> /productivity:memory-management
> 
> Your memory system is already set up. Here are all the files:
> 
> Working memory (hot cache): View CLAUDE.md
> 
> Deep memory: View glossary View company context
> 
> Empty directories ready for profiles: memory/people/ and
> memory/projects/ are there for when we need richer detail on specific
> people or projects.
> 
> Current state: 8 people, 8 terms, 5 projects loaded. The gaps I still have
> are SC, AM, and ArV (full names and current roles). I'll ask when they
> come up naturally.
> 
> Want me to add anything to memory right now?
> 
> Reply...
> 
> Claude
> 
> Opus 4.6
> 
> Claude · MD
> 
> Memory
> 
> Me
> 
> Charlie Hills, Content Creator & Agency Owner at Linked Agency
> (linked-agency.com).
> ~200k LinkedIn followers. Writes the MarTech AI newsletter on
> Substack.
> Runs The AI Creators Club community (on Circle, theaicreator.uk).
> Timezone: GMT. Date format: DD/MM/YYYY.
> 
> People
> 
> Who        Role
> 
> Gellei     Instagram content management
> 
> Ansh
> Kumar     Instagram + YouTube content management
> 
> ST         Head of LinkedIn content management
> 
> Utsav      Co-founder of Vislo, recurring 1:1 Thursdays 13:00 GMT
> 
> Joe        Joe at Satori Funnels (joe@satorifunnels.com), funnels
>            partner
> **Description:** This is a split-screen desktop app screenshot showing a chat/workspace on the left and a document or memory page on the right. The left pane contains a productivity memory-management message and a reply box, while the right pane shows a “Memory” document with personal details and a people table. The interface includes tabs and controls typical of an AI assistant or note-taking app.


The next step is the one that changes your output quality.

Create a folder called “Claude Context” with three files inside it.

“about-me.md” covers who you are, your role, and what good work looks like in your context. “brand-voice.md” covers how you write, your phrases, your tone, what sounds wrong to you. “working-style.md” covers how you want Claude to behave. Questions before it starts or not. Short or long outputs. Which formats.

![](https://substackcdn.com/image/fetch/$s_!i2BA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37756aa2-9d9d-4b4d-bc07-cd8e60d4a117_1628x772.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** About me
> Document · MD
> Download
> 
> Brand voice
> Document · MD
> Download
> 
> Working style
> Document · MD
> Download
> 
> Download all
> **Description:** A light-themed file list interface shows three document items: About me, Brand voice, and Working style. Each row has a document icon, a subtitle reading “Document · MD,” and a Download button on the right. Below the list is a larger “Download all” button and a small row of feedback/action icons.


Save them as.md files. These compound over time. Refine them weekly and the output tightens with each session.

If you followed last week’s guide, you already have a profile.md built from your full ChatGPT history. Drop it into this folder alongside your other context files. It gives Cowork deep context on day one.

If you have not done the migration yet, start there. It takes 20 minutes and gives you a structured profile covering your writing style, frameworks, projects, and preferences.

Cowork can access unlimited files in your granted folders. Projects in claude.ai cap at 20 files. If you need deep context on a client, put everything in a local folder and point Cowork at it.

Your first prompt after selecting this folder:

> Read all the files in this folder completely. Then give me a summary of what you know about me, how I work, and what context you have access to.

This forces Claude to absorb your context before starting anything. It also tells you immediately if your context files are written well enough.

![](https://substackcdn.com/image/fetch/$s_!pLsJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84413bf8-523e-4ce4-bcb5-3360f46a50d4_1976x1574.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat  Cowork  Code
> 
> Review files and summarize user profile
> 
> Your active projects (as of early 2026). Vislo public beta (500 users), AI Creators Club
> scaling, YouTube channel launch, hiring and team building, exploring a creator agency
> model, CHEF Framework trademark, and a live sponsored content pipeline.
> 
> Files I read.
> 
> 1. CLAUDE.md (your global instructions)
> 2. about-me.md (biographical summary)
> 3. brand-voice.md (tone, formatting, banned words, LinkedIn/newsletter/carousel rules)
> 4. charlie_hills_profile.md (comprehensive 350-line profile covering everything above in
>    full detail)
> 5. working-style.md (how you want me to operate, output preferences, content
>    workflows, special modes)
> 
> I also have access to a set of custom skills built for your workflows: LinkedIn post writer,
> carousel creator, newsletter writer, infographic generator, Substack image generator, email
> subject line generator, weekly client updates, your ICP reference, and a skill creator for
> building new ones.
> 
> That is the full picture. What do you need from me?
> 
> Reply...
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses. Give us feedback
> **Description:** This is a screenshot of the Claude chat interface on a desktop browser or app window. The conversation shows a response summarizing files read and listing active projects and custom skills. A reply box is visible at the bottom with the model selector set to Opus 4.6.


---

### Feature 2: Instructions

Instructions are standing orders you write once. They load automatically at the start of every Cowork session. No re-explaining yourself.

Global instructions apply everywhere. Folder instructions apply when you select a specific local folder. With both set up properly, Claude starts every session already knowing your name, your role, your output defaults, and your communication preferences.

How to set them up. Go to Settings > Cowork in the desktop app. Click “Edit” next to Global Instructions. Write what you want Claude to always know.

![](https://substackcdn.com/image/fetch/$s_!hiTa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F497c65ad-d4c3-418d-a57a-7d317c45ff64_986x787.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Settings
> General
> Account
> Privacy
> Billing
> Usage
> Capabilities
> Connectors
> Claude Code
> Cowork
> Desktop app
> General
> Extensions
> Developer
> Chat
> Cowork
> Code
> Cowork
> Preview
> Instructions here apply to all Cowork sessions. Use this for preferences, conventions, or context that Claude should always know.
> My name is Charlie Hills. I run a content agency and write the MarTech AI
> newsletter on Substack. I have around 200,000 followers on LinkedIn.
> 
> My default output format is plain text or markdown unless I ask for something
> else. Save documents as .md files unless I specify .docx or another format.
> 
> When writing anything in my voice: short sentences, no em dashes, no
> semicolons, British English spelling. Never use the words "leverage,"
> "deep dive," "unlock," or "game-changer." Never open with "In today's world."
> Never end with a motivational summary.
> 
> Before starting any task that involves creating content or making decisions,
> Cancel
> Save
> Delete Cowork sessions
> To delete your Cowork sessions, email Anthropic at privacy@anthropic.com.
> **Description:** This is a settings screen for an app, with a left sidebar of categories and the Cowork section selected. The main panel shows a large editable instructions text box containing custom writing preferences and personal context. At the bottom are Cancel and Save buttons, plus a note about deleting Cowork sessions by emailing Anthropic.


What to include: your name, role, and what you do. Communication preferences. Output defaults like “always save documents as.docx unless I say otherwise.” Working style preferences. Things to avoid.

Folder instructions work the same way but per project. Each client folder gets its own brief that loads automatically. Full context, every time. I’m setting this up for every client at my agency. One folder per client, one set of instructions, and every team member working from the same context.

After setting global instructions, open a new session and test it:

> Before we start any work, tell me what you know about me, how I like to work, and any standing preferences you are aware of.

![](https://substackcdn.com/image/fetch/$s_!xOVD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7051eb86-1680-4523-8ea1-6f2f3932b8b6_986x787.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat  Cowork  Code
> 
> Review user preferences and work style
> 
> Before we start any work, tell me what you know about me, how I like to work,
> and any standing preferences you are aware of.
> 
> Thought process >
> 
> Here's what I have on file, Charlie.
> 
> You run a content agency and write the MarTech AI newsletter on Substack. You have
> around 200,000 followers on LinkedIn.
> 
> Your writing style: short sentences, British English spelling, no em dashes, no semicolons.
> You avoid words like "leverage," "deep dive," "unlock," and "game-changer." You never open
> with "In today's world" and never end with a motivational summary.
> 
> Your default output format is plain text or markdown. You want .md files unless you specify
> .docx or another format.
> 
> Your working preferences: before I create content or make decisions, I ask clarifying
> questions first. I don't execute until we've aligned. If I'm less than 90% confident on
> something, I ask rather than guess.
> 
> Your time zone is GMT. Dates go DD/MM/YYYY.
> 
> I also have access to several custom skills built around your work: your newsletter style,
> 
> Reply...
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses. Give us feedback
> **Description:** A desktop chat application screenshot showing a conversation about reviewing user preferences and work style. The main pane contains a prompt and a generated summary of the user's preferences, writing style, and working habits. A reply box is visible at the bottom along with the model selector and standard app controls.


If Claude reflects your instructions back accurately, you are ready. If something is missing, fix it now.

Your context files and instructions are not set-and-forget. After every session where Claude produces something good, ask yourself if the context files need updating. New client? Add them to your about-me.md. Refined your tone? Update brand-voice.md. Changed your output preferences? Edit working-style.md.

You can also update memory mid-session. Type /memory-management and add new information directly. If you’ve landed a new client, changed your posting schedule, or shifted your content strategy, add it there. It loads into the current session immediately and persists in your files for the next one.

![](https://substackcdn.com/image/fetch/$s_!dPKa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33420550-6942-4fea-8bc7-0706928d5014_2470x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Review daily tasks and plan
> 
> Chat  Cowork  Code
> 
> /productivity:memory-management
> 
> Progress
> 4 of 4
> 
> Working folder
> 
> dashboard.html
> TASKS.md
> linkedin-post-burnout.md
> 
> Scratchpad
> 
> Context
> 
> Connectors
> Notion
> Google Calendar
> notionApi
> filesystem
> Apify MCP server
> 
> Skills
> 
> task-management
> 
> Your memory system is already set up. Here are all the files:
> 
> Working memory (hot cache): View CLAUDE.md
> 
> Deep memory: View glossary View company context
> 
> Empty directories ready for profiles: memory/people/ and memory/projects/ are there for
> when we need richer detail on specific people or projects.
> 
> Current state: 8 people, 8 terms, 5 projects loaded. The gaps I still have are SC, AM, and ArV
> (full names and current roles). I'll ask when they come up naturally.
> 
> Want me to add anything to memory right now?
> 
> Claude
> Document · MD
> 
> Cursor
> 
> Glossary
> 
> Cursor
> 
> Reply...
> 
> Opus 4.6
> **Description:** This is a screenshot of a desktop app interface, likely an AI workspace or chat tool. It shows a memory-management task with a main content area, a right sidebar listing working files and connectors, and a message composer at the bottom. The screen includes several clickable UI elements and status panels.


The rule is simple. If you find yourself re-explaining something to Claude, it belongs in a file.

Your context files give Claude your history. Your instructions give Claude your rules. Both load before you type a single message. Now we need data.

---

### Feature 3: AskUserQuestion

![](https://substackcdn.com/image/fetch/$s_!If9_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae8e194a-1582-4b23-8dc2-68c0cc0bdb83_1347x761.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat  Cowork  Code
> 
> Write LinkedIn post for today
> 
> charlie_hills_prof
> ile.md
> 
> MD
> 
> daily-social-
> briefing-06-03-
> 2026.md
> 
> MD
> 
> Progress
> 
> See task progress for longer tasks.
> 
> Downloads
> 
> Instructions · CLAUDE.md
> 
> Scratchpad
> 
> Context
> 
> Track tools and referenced files used in this task.
> 
> Ask me questions about what post I want to write about today.
> Once you’ve gathered context write a /linkedin-post-writer:linkedin-post
> about it.
> 
> Which topic from the briefing (or something else entirely) do you want to
> post about today?
> 
> 1  GPT-5.4 for marketers
> 2  MCP + tools workflow
> 3  AI changing design
> 4  Job displacement angle
> 
> Something else
> 
> 1 of 3
> 
> Skip
> 
> ↑↓ to navigate · Enter to select · Esc to skip
> **Description:** A web app workspace is shown with a task titled “Write LinkedIn post for today.” In the center, a prompt asks which topic to post about, with multiple-choice options such as “GPT-5.4 for marketers” and “MCP + tools workflow.” A right sidebar shows progress, downloads, and context panels, indicating this is an AI-assisted workflow interface.


Every other AI tool guesses when your task is unclear. Confidently. Then gives you polished output that answers the wrong question.

Cowork stops and generates a form instead. Structured questions with multiple-choice options. You iterate until you and Claude are aligned, then it executes.

I showed this to my team and it was the thing that made them reconsider ChatGPT. Claude gives you actual clickable options rather than forcing you to prompt your way to clarity. It breaks your request into subtasks, shows you the plan, and then executes step by step. ChatGPT charges ahead with assumptions. Claude asks first.

Use this as your default opener for any non-trivial task:

> I want to \[YOUR TASK\] so that \[WHAT GOOD LOOKS LIKE\]. First, read all uploaded files completely before responding. DO NOT start executing yet. Ask me clarifying questions to refine the approach. Only begin work once we have aligned.

![](https://substackcdn.com/image/fetch/$s_!uUrY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4237b20c-5647-4f92-837a-5d7ca73d2044_990x791.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat  Cowork  Code
> 
> Review files and summarize user profile
> 
> I want to write a 90-day strategic plan for my business so that I have clear
> priorities, milestones, and weekly actions for the next quarter. First, read all
> uploaded files completely before responding. DO NOT start executing yet.
> Ask me clarifying questions to refine the approach. Only begin work once we
> have aligned.
> 
> I've already read all three files in full from the previous turn. I have your complete context:
> about-me, brand-voice, and working-style.
> 
> Before I build this 90-day plan, I need to nail down a few things.
> 
> Which businesses/projects should this plan cover?
> Everything
> 
> What does success look like at the end of 90 days? Pick the primary lens.
> Revenue target
> 
> Do you have specific revenue or growth targets already in mind for Q2 2026?
> No, propose targets
> 
> What format do you want the final plan delivered in?
> Word document (.docx)
> 
> Reply...
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses. Give us feedback
> **Description:** This is a screenshot of a chat-style AI interface on a desktop app. It shows a user prompt asking for a 90-day strategic plan and a response that asks clarifying questions about scope, success metrics, targets, and output format. The bottom of the screen includes a reply box and model selector.


Try it once and you will stop writing long, engineered prompts from scratch. Context compounds. Prompt engineering depreciates.

The richer your about-me files, brand voice docs, and working style instructions, the better every output gets without extra work in the conversation. Anthropic is building the prompting layer into the tool itself. What scales is your context files, not your prompts.

---

### Feature 4: Connectors

Link your tools once and Claude references live data from them mid-session. Over 50 integrations available. Slack, Google Drive, Google Calendar, Notion, Figma, Asana, Apify, ClickUp, and more. Free on all plans.

You can also build custom MCP connectors. MCP stands for Model Context Protocol. An API connects one app to one other app. MCP connects one LLM to any app through the same standard. Anything with an API key can become a connector.

To connect: go to Settings > Connectors in Claude Desktop. Browse the directory, click a connector, authenticate, done. You only do this once.

![](https://substackcdn.com/image/fetch/$s_!cWyK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F778da554-69db-4746-858a-9f8e0a29a919_986x787.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Connectors
> Connect Claude to your apps, files, and services. Connectors are built by third parties and reviewed by
> Anthropic for safety. You can also add a custom connector.
> Featured
> All
> Search
> Type
> Categories
> Gmail
> Draft replies, summarize threads, &
> search your inbox
> Google Calendar
> Manage your schedule and coordinate
> meetings effortlessly
> Notion
> Connect your Notion workspace to
> search, update, and power workflow...
> Figma
> Generate diagrams and better code
> from Figma context
> Canva
> Search, create, autofill, and export
> Canva designs
> Slack
> Send messages, create canvases, and
> fetch Slack data
> Atlassian
> Access Jira & Confluence from Claude
> HubSpot
> Chat with your CRM data to get
> personalized insights
> Linear
> Manage issues, projects & team
> workflows in Linear
> Gamma
> Create presentations, docs, socials,
> and sites with AI
> monday.com
> Manage projects, boards, and
> Intercom
> Access to Intercom data for better
> **Description:** A modal window titled “Connectors” is open in a Claude app interface, showing a catalog of third-party integrations. It includes search and filter controls and a grid of connector cards such as Gmail, Google Calendar, Notion, Figma, Canva, Slack, Atlassian, HubSpot, Linear, and Gamma. The rest of the app is dimmed in the background, indicating this is an overlay dialog.


**Apify (Social Scraping)**

Apify scrapes data from any website. I connected it and asked Claude to pull my last 30 LinkedIn posts, rank them by engagement, and give me a full breakdown.

> Use Apify to scrape my last 30 LinkedIn posts. Rank them by engagement. Give me a full breakdown.

![](https://substackcdn.com/image/fetch/$s_!Joyb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83b9722a-1dd1-4acb-a93a-ec79eebe7b15_2470x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Analyze LinkedIn posts for content strategy
> 
> Use Apify to scrape my last 30 LinkedIn posts. Rank them by
> engagement rate. Break down the top 10 by hook style, post
> format, topic, and time posted. Then give me three content
> angles I should double down on this week.
> 
> Thought process ›
> 
> Let me find the right Apify tool for scraping your LinkedIn posts and
> get this set up.
> 
> search-actors ›
> 
> What's your LinkedIn profile URL so I can scrape your posts?
> linkedin.com/in/charlie-hills
> 
> Got it. Let me get the input schema for the best-rated scraper and then
> run it on your profile.
> 
> Used Apify MCP server integration, updated todo list ›
> 
> Reply...
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses. Give us feedback
> 
> Chat
> Cowork
> Code
> 
> Linkedin engagement analysis · MD
> 
> LinkedIn Post Engagement Analysis
> 
> 30 Posts | 10 Feb - 11 Mar 2026 | ~200K Followers
> 
> All 30 Posts Ranked by Engagement Rate
> 
> Rank  Eng  Likes  Comments  Shares  Format  Day  Hook
> Rate
> 
> 1  1.395%  2,185  560  45  Image  Fri  This is get
> ridiculous.
> Nano Ban:
> just dropp
> 
> 2  1.317%  2,081  245  309  Image  Sat  I compiled
> everything
> need to m:
> Claude Sk
> 
> 3  1.288%  1,896  346  334  Image  Tue  Anthropic
> giving awe
> $10,000 of
> education.
> **Description:** The image is a screenshot of a split-screen desktop app. On the left is a chat interface discussing LinkedIn post analysis and scraping with Apify, and on the right is a markdown document titled “LinkedIn Post Engagement Analysis” showing a ranked table of post engagement metrics. The overall layout suggests an AI-assisted workflow for analyzing LinkedIn content performance.


Claude returned the top post with exact likes, comments, and shares. An analysis of why each post performed. The topic, the format, the posting time. It identified which posts were carousels versus text-only, which surprised me because I didn’t expect it to detect format from scraped data.

The output reads like a strategy report. Content themes, underperforming formats, posting patterns. This is what my custom model Stanley does, rebuilt inside Claude with one prompt.

I ran six accounts through the same process for competitor analysis. Claude compared engagement rates, top-performing posts, trending topics, and content angles across all six.

Some data was off. One follower count was wrong by about 50k. Another account didn’t appear in the ranking at all. The directional analysis and pattern identification were solid. For client work, you verify the numbers, but the structure and insights save hours.

> Use Apify to scrape the last 20 posts from \[competitor 1\], \[competitor 2\], \[competitor 3\]. Compare engagement rates, top content themes, and formats. Give me strategic recommendations.

![](https://substackcdn.com/image/fetch/$s_!mow4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6118ce9-4468-43d4-a39b-2e496715c6b4_2470x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Analyze LinkedIn posts for content strategy
> 
> Use Apify to scrape the last 20 posts from these LinkedIn
> profiles:
> 
> https://www.linkedin.com/in/donnellychris/
> https://www.linkedin.com/in/fatima-rasheed-khan/
> https://www.linkedin.com/in/mischa-collins/
> https://www.linkedin.com/in/laraacostar/
> https://www.linkedin.com/in/alicjasmin/
> 
> Compare engagement rates across all accounts. Flag the top
> 5 posts overall and tell me what they have in common.
> Identify any trending topics or formats I should test.
> 
> Thought process >
> Let me scrape all five profiles in parallel.
> Updated todo list, used Apify MCP serv...gration >
> Got the first batch. Let me grab the remaining posts.
> 
> Reply...
> 
> Opus 4.6
> 
> Competitor engagement analysis · MD
> 
> Account Comparison
> 
> Creator  Followers  Posts  Avg
> Eng
> Rate  Avg
> Likes  Avg
> Comments  Comment:Lik
> Ratio
> 
> Jasmin
> Alic
> ~350K  20  1.187%  2,383  1,715  0.72
> Lara
> Acosta
> ~310K  20  0.709%  1,306  746  0.52
> Charlie
> Hills
> ~200K  30  0.659%  959  355  0.37
> Fatima
> Khan
> ~150K  2  0.510%  420  314  0.62
> Chris
> Donnelly
> ~530K  20  0.370%  1,092  386  0.27
> 
> Jasmin Alic has the highest engagement rate at 1.187%. His comment-
> to-like ratio (0.72) is 2.6x higher than yours (0.37). He generates
> conversation, not passive scrolling.
> 
> Your engagement rate (0.659%) sits between Lara Acosta and Fatima
> **Description:** A split-screen desktop app is shown with a chat/workspace on the left and a markdown report on the right. The left side contains a prompt asking to analyze LinkedIn posts from several profiles, while the right side shows an account comparison table with engagement metrics. The interface includes typical app controls, tabs, and a reply box, indicating this is a UI screenshot rather than a diagram.


This is step one of my daily workflow. That comes in Feature 4.

Here is what this looks like in practice.

**Slack Triage**

I asked Cowork to search my Slack DMs and surface anything I had not responded to, ordered by priority. It found unread threads and compiled a full summary.

> Search my Slack messages from the last 7 days and give me a summary of anything I need to follow up on. Organise by urgency.

![](https://substackcdn.com/image/fetch/$s_!woR8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a8f6997-86d3-437e-bca2-99f6db5e667f_1976x1500.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat  Cowork  Code
> 
> Summarize Slack messages and follow-ups
> 
> Search my Slack messages from the last 7 days and give me a summary of
> anything I need to follow up on. Organise by urgency.
> 
> Thought process >
> I'll search your Slack messages from the last 7 days across a few angles to find everything
> that needs your attention.
> Searched Slack for direct messages received after March 3, 2026 >
> Let me search more broadly for mentions of you, unanswered questions, and action items
> across your workspaces.
> Searched Slack for messages from Charlie and urgent keywords since March 3rd >
> Let me also check for any recent channel activity in your key workspaces.
> Searched Slack messages and prioritized by urgency >
> Here's what needs your attention from the last 7 days, sorted by urgency.
> HIGH URGENCY
> Elise (client. #lgm-linkedin) posted today. She tagged you and Sarah directly. She's left
> Reply...
> Opus 4.6
> Claude is AI and can make mistakes. Please double-check responses. Give us feedback
> **Description:** A desktop app window shows a chat-style workflow for summarizing Slack messages and follow-ups. The main panel contains a user request, a visible thought process, and a prioritized response section labeled HIGH URGENCY. At the bottom there is a reply input box and a model selector showing Opus 4.6.


That’s work I used to hand off to a VA. Now it takes one prompt.

**Notion Integration**

After Claude writes a LinkedIn post, I ask it to create a carousel design brief and save it as a new page in Notion. Slide-by-slide breakdown with my caption included. The design team picks it up without me writing a separate brief.

> Connect to Notion. Create a carousel design brief based on this post. Include a slide-by-slide breakdown and save it as a new page in my content calendar.

![](https://substackcdn.com/image/fetch/$s_!xLgJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff15e737f-8797-4d36-a48c-74e4489005ac_1638x1712.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Carousel Brief: The Engagement O...
> 
> Carousel Brief: The Engagement O...
> Private
> Share
> 
> Carousel Brief: The Engagement
> OS (466 Days to 100k)
> 
> Overview
> 
> Post topic: LinkedIn Engagement OS — the system behind 0 to 100k in 466 days
> 
> Post type: Observation + Decision Rule
> 
> Goal: Teach the before/during/after posting rhythm. Drive reposts and comments.
> 
> Slide count: 9 slides (Cover + 7 content + CTA)
> 
> Dimensions: 1080 x 1350px (portrait, fills mobile viewport)
> 
> Brand palette: Mint green, purple, bright blue, yellow, orange, lime green, dark navy
> 
> Visual style: Hand-drawn vertical flowchart feel. Large bold illustrations per
> section. Connecting arrows between stages. Cream dot-grid paper background.
> 
> Slide-by-Slide Brief
> 
> Slide 1 — Cover
> 
> Headline: 466 days. 0 to 100k followers.
> 
> Sub-headline: The Engagement OS behind every post.
> 
> Visual: Bold number “466” as the dominant element, large and centered. Dark navy
> background. Mint green accent on the number. Charlie Hills name bottom left.
> **Description:** A browser-based document editor is open to a page titled “Carousel Brief: The Engagement OS (466 Days to 100k).” The visible content is a structured brief with headings like Overview and Slide-by-Slide Brief, listing post topic, goals, slide count, dimensions, brand palette, and visual style. It appears to be a planning document for a social media carousel rather than the final design itself.


I also use Notion for team accountability. Claude checks all boards, finds tasks more than two days past due, and adds comments directly into the Notion pages.

![](https://substackcdn.com/image/fetch/$s_!3sYp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdca6d552-368a-4cd1-95d6-5b43b96b162e_2620x1172.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** CONTENT/STORIES CALENDAR
> 
> Charlie Hills 1d
> Daily check 11/03: 2 items need attention. Critical: None. Urgent: Generate Cinematic Video in NotebookLM (13/03, Video Feedback Needed), Anthropic Free Courses
> carousel (14/03, Needs Graphics). Full briefing sent via email.
> 
> Charlie Hills 1h
> Daily check 12/03: 4 items need attention. Critical: None. Urgent: "I fired my team and hired Claude 4.6" (15/03, Ready to Post). This Week: "Craziest ChatGPT Hack"
> (16/03, Editing), "Antigravity + Claude Code" (18/03, To Edit), "Claude in Chrome" (19/03, To Edit). 5 items missing priorities. Full briefing sent via email.
> 
> Add a comment...
> 
> Table
> Content Calendar
> Content Status Board
> Priority Board
> Tasks
> 3 more...
> 
> New
> **Description:** This is a screenshot of a content planning workspace titled “CONTENT/STORIES CALENDAR.” It shows comment-style updates from Charlie Hills about daily checks, urgent items, and scheduled content tasks. A navigation bar at the bottom includes views like Table, Content Calendar, Content Status Board, Priority Board, and Tasks, along with a New button.


**Gmail and Calendar**

Cowork reads your inbox, categorises emails, and labels messages. It reads your calendar and flags where you have focused work time between meetings.

> Look at my calendar for this week. Flag any days with back-to-back meetings and tell me where I have focused work time available.

![](https://substackcdn.com/image/fetch/$s_!giNJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58da2e50-47a0-410d-8bd0-841bb3162647_1862x1500.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Chat  Cowork  Code
> 
> Review calendar for meeting gaps
> 
> Look at my calendar for this week. Flag any days with back-to-back meetings
> and tell me where I have focused work time available.
> 
> Retrieved calendar events for March 9-13, 2026 ›
> 
> Here's your week at a glance (all times GMT):
> 
> MONDAY 09/03 Flamingo Fam (09:30-10:00), Posting Time (11:00-11:30), Gym/Lunch
> (12:00-14:30), 10M Views Club (15:30-16:00). Scattered but manageable. No true back-to-
> back situations.
> 
> TUESDAY 10/03 Posting Time (11:00-11:30), Lunch (12:00-13:00), Weekly Sync with Cory
> (15:00-15:30). Your lightest day. Big open morning before 11:00 and a solid 2-hour window
> from 13:00-15:00.
> 
> WEDNESDAY 11/03 (your busiest day) Posting Time (11:00-11:30), Gym/Lunch (12:00-
> 14:30), Speaking Practice (15:00-15:30), Funnel Clinic (16:00-17:00), Claude Workshop
> (19:00-20:00). Five events. The afternoon is chopped up with only 30-minute gaps between
> 14:30 and 17:00. This is your most fragmented day for focus work.
> 
> THURSDAY 12/03 (today) Posting Time (11:00-11:30), Charlie <> Utsav (13:00-13:30), Time
> Reply...
> **Description:** A desktop app chat interface is shown with a prompt asking to review a calendar for meeting gaps. The response summarizes calendar events for several days in March 2026 and highlights open focus-work windows and fragmented periods. A reply box and model selector are visible at the bottom, indicating an AI assistant conversation screen.


**Google Drive**

> Find the most recent document about \[PROJECT NAME\] in my Drive. Read it and tell me the three most important things I need to know.

---

### Feature 5: Plugins

![](https://substackcdn.com/image/fetch/$s_!MjC3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffad3de4-aa20-4a64-9a07-705bebab09dc_990x791.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Customize
> Skills
> Connectors
> Personal plugins
> Marketing
> Commands
> Connectors
> Skills
> Sales
> Legal
> Finance
> Marketing
> Update
> Customize
> Marketing
> Source
> Marketplace (Anthropic & Partners)
> Version
> 1.0.0
> Author
> Anthropic
> Description
> Create content, plan campaigns, and analyze performance across marketing channels. Maintain brand
> voice consistency, track competitors, and report on what's working.
> Commands
> Skills
> See all
> Use these shortcuts to trigger an entire workflow by name. Search your list of commands at any time by typing / in the chat
> window.
> Review content against your
> brand voice, style guide, a...
> /brand-review
> Generate a full campaign
> brief with objectives,...
> /campaign-plan
> Research competitors and
> generate a positioning and...
> /competitive-brief
> Draft blog posts, social
> media, email newsletters,...
> /draft-content
> Design and draft multi-email
> sequences for nurture flo...
> /email-sequence
> Build a marketing
> performance report with k...
> /performance-report
> Try asking...
> Draft a blog post with SEO optimization
> Plan a multi-channel campaign
> Review content against our brand voice
> Analyze our competitors' positioning and content gaps
> **Description:** A desktop app settings/customization page for a plugin or assistant named Marketing. The left sidebar lists sections like Skills, Connectors, and personal plugins, while the main panel shows plugin metadata, a description, and command cards. Buttons such as Update and Customize appear at the top, along with example prompts under “Try asking...”.


Without a plugin, Cowork is a capable generalist. Plugins make it a specialist.

Anthropic shipped 11 official plugins in January 2026. Productivity, Marketing, Sales, Finance, Data Analysis, Legal, Product Management, Customer Support, Enterprise Search, Biology Research, and more being added.

When the Legal plugin launched, Thomson Reuters dropped 16% in a single trading session. LegalZoom fell 20%. That is what happens when AI starts doing specialised work rather than drafting emails.

![Claude Crash Impact on Thomson Reuters + LexisNexis is Irrational –  Artificial Lawyer](https://substackcdn.com/image/fetch/$s_!tsVb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73728211-f3b4-4ff7-abd4-163b298ea68b_1024x792.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Thomson Reuters Corp
> TSE: TRI
> 
> 125.41 CAD
> -36.15 (-22.38%) ↓ past 5 days
> 3 Feb, 16:00 GMT-5 • Disclaimer
> 
> 1D 5D 1M 6M YTD 1Y 5Y Max
> 
> 160
> 140
> 120
> 100
> 
> 161.56 CAD Wed 28 Jan 09:30
> 29 Jan 30 Jan 2 Feb 3 Feb
> **Description:** A stock price chart interface for Thomson Reuters Corp (TSE: TRI) showing the current price and a 5-day performance view. The chart line trends downward sharply near the end, with the price displayed as 125.41 CAD and a red loss percentage. Tabs for different time ranges and a Follow button are visible, indicating a finance/market UI screenshot.


Claude Crash Impact on Thomson Reuters + LexisNexis is Irrational – Artificial Lawyer

To install one: click the “+” button in the Cowork chat bar, then click “Plugins.” Browse the library, click Install on the one that matches your role. Type “/” in any Cowork session to see the slash commands that plugin adds.

This is where the workflow from Features 1-3 pays off. Claude has your context files loaded. Apify has pulled your engagement data and trending content. AskUserQuestion has aligned the brief. The Marketing plugin executes it.

> /marketing:draft-content Write a LinkedIn post about \[TOPIC\]. Match the voice from my brand-voice.md file. Target \[AUDIENCE\]. Goal: \[WHAT I WANT PEOPLE TO DO\].

![](https://substackcdn.com/image/fetch/$s_!xtqj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F834f5f75-5db8-4649-ae8b-8677999b0657_1862x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Review daily tasks and plan
> 
> Chat  Cowork  Code
> 
> Linkedin post burn...
> 
> Cursor
> 
> /marketing:draft-content Write a LinkedIn
> post about burnout. Match the voice from
> my brand-voice.md file. Target B2B
> founders. Goal: inspire
> 
> I have your voice preferences from CLAUDE.md
> already loaded. Before I write this, a few quick
> questions:
> 
> 1. Is this for your personal LinkedIn (200k
> followers) or a client's page?
> 2. What angle on burnout? For example: you've
> experienced it personally, a framework for
> avoiding it, the myth of hustle culture, burnout
> as a signal to systemi
> 3. Any specific moment, story, or data point you
> 
> Reply...
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses.
> Give us feedback
> 
> 34% of founders are burned out right now.
> 
> And 82% have no support system for it.
> 
> I was one of them.
> 
> Two years ago I worked 14-hour days.
> I called it "dedication." It was bad systems.
> 
> Here is what changed everything for me:
> 
> 1. I stopped doing work AI could do. I
>    automated repurposing, scheduling, and first
>    drafts. That gave me back 3 hours a day.
> 2. I hired for everything except my voice. Gellei
>    runs IG. Ansh runs YouTube. ST runs
>    LinkedIn.
> 3. I blocked 2 hours every morning. No Slack.
>    No email. No calls.
> 4. I said no to 80% of calls. Most meetings are
>    someone else's priority.
> 
> The result was not "less work." It was better work
> with energy left over.
> 
> Burnout is not a badge of honour.
> **Description:** A split-screen desktop app interface shows a chat on the left and a generated LinkedIn post draft on the right. The left pane contains a prompt about writing a LinkedIn post on burnout and follow-up questions from the assistant, while the right pane displays the drafted post text. The top bar includes tabs like Chat, Cowork, and Code, indicating an AI writing workspace.


The plugin follows a proven structure rather than guessing. It writes the post in my voice, informed by today’s trends, built on two years of context, and formatted to my exact rules. The output is noticeably tighter than a raw prompt.

Once the post is written, I chain back to the Notion connector from Feature 3. Claude creates a carousel design brief and saves it as a new page in my content calendar. Post, brief, and visual direction in one session.

Other plugins worth installing:

> /productivity:start Let’s review what I need to accomplish today and set up my task list.

![](https://substackcdn.com/image/fetch/$s_!lNGM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13aec689-c9f7-4251-8b78-b6e8ee64518f_1862x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Review daily tasks and plan
> 
> Chat  Cowork  Code
> 
> Tasks · MD
> 
> Cursor
> 
> /productivity:start Let’s review what I need
> to accomplish today and set up my task
> list.
> 
> Read task management skill documentation file ›
> This is a fresh setup. Let me create the files and get
> you started.
> Created task management file and copied dashboard tem… ›
> Your productivity system is set up. TASKS.md and
> dashboard are ready in your working folder.
> Open your dashboard
> 
> Now, to make this useful, I’d need to learn your
> workplace shorthand. Where do you keep your
> project list? Could be
> 
> Reply…
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses.
> Give feedback
> 
> Tasks
> 
> Active
> 
> Posting Time - 11:00 GMT daily recurring
> Charlie <> Utsav - 13:00 GMT, recurring 1:1 with
> Utsav (Vislo co-founder)
> Inbound & Outbound Lead Generation
> masterclass - 17:00 GMT, The AI Creators Club on
> Zoom
> Joe x Charlie | Funnels Chat - 19:00 GMT,
> funnels partner call with Joe (Satori Funnels)
> Write script for "RIP Open Claw" - High
> Priority, Format 2 (AI News Reel), assigned to
> Gellei, needs script before production starts
> Review "Anthropic Free Courses" content -
> Needs Voice Over, post date 20/03, assigned to
> Gellei + Ansh Kumar
> 
> Waiting On
> 
> Content in production pipeline - Multiple items
> with Gellei and Ansh across Instagram/YouTube
> **Description:** A split-screen desktop app is shown with a chat/workspace panel on the left and a markdown task document on the right. The left side contains a conversation about setting up a productivity system and opening a dashboard, while the right side lists active tasks and a waiting-on section with checkbox items. The interface appears to be a productivity or task-management tool inside a macOS-style window.


> /data:explore I have uploaded a CSV in this folder. Give me a summary of what is in it, flag any anomalies, and suggest three analyses worth running.

![](https://substackcdn.com/image/fetch/$s_!B7dt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8ede3fc2-951a-4138-87a1-391b51276fd2_2470x1404.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** Analyze uploaded CSV data
> 
> /data:explore-data I have uploaded a CSV in this folder. Give
> me a summary of what is in it, flag any anomalies, and
> suggest three analyses worth running.
> 
> Let me find and explore the CSV file in your folder.
> Listed files in LinkedIn Data Export directory ›
> 
> There's also an .xlsx file that's 28KB, which is far more substantial than
> the tiny 87-byte CSV. The CSV only has 2 rows (total impressions and
> members reached). Let me check the Excel file for the real data.
> Updated todo list with data profiling and quality analysis tasks ›
> 
> Here's your data profile, Charlie.
> 
> Data Profile: LinkedIn Content Export
> 
> Reply...
> 
> Opus 4.6
> 
> Claude is AI and can make mistakes. Please double-check responses. Give us feedback
> 
> Chat  Cowork  Code
> 
> Linkedin analytics report · MD
> 
> Summary of day-of-week performance:
> 
> Day  Avg
> Impressions  Median
> Impressions  Avg
> ER  Known
> Posts
> 
> Monday  100,600  83,646  3.49%  8
> Tuesday  78,524  73,116  3.66%  4
> Wednesday  70,011  65,536  3.94%  5
> Thursday  71,926  57,926  3.89%  8
> Friday  91,173  65,627  3.59%  15
> Saturday  79,952  71,790  3.77%  12
> Sunday  88,424  80,462  3.67%  12
> 
> Recommendation: You are already posting on the right days for reach
> (Friday, weekend). If you want to improve engagement rate without
> sacrificing reach, consider adding a mid-week post (Tuesday or
> Wednesday) specifically targeting your core audience with higher-
> depth content. Your weekend content drives reach. Mid-week content
> drives loyalty.
> **Description:** This screenshot shows a split-screen AI workspace with a chat panel on the left and a markdown report on the right. The left side contains a prompt about analyzing uploaded CSV data and the assistant’s response about finding a LinkedIn data export, while the right side displays a table summarizing day-of-week LinkedIn performance and a recommendation paragraph. The interface includes tabs for Chat, Cowork, and Code, indicating an AI-assisted document or analysis environment.


One caveat: plugins load additional context into every session, which means they consume more of your monthly usage allocation. Install the ones relevant to your role and leave the others for when you need them.

---

### Feature 6: Scheduled Tasks

![](https://substackcdn.com/image/fetch/$s_!kFNJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fdc213e-ff9f-4592-8bb1-17ef383bf28a_1902x1324.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** All scheduled tasks
> 
> Daily social media briefing
> 
> Active
> Next run Tomorrow at 7:00
> 
> Run now
> 
> Description
> Scrape all pre-configured social media
> accounts across every platform using
> Apify actors and compile a daily
> trending content briefing.
> 
> Repeats
> Every day at 7:00
> 
> Always allowed
> Apify search-actors
> Apify call-actor
> 
> Instructions
> Run all my pre-configured Apify scraper actors across every platform
> (Instagram, LinkedIn, X/Twitter, TikTok, Threads, Facebook, YouTube).
> For each account, collect the most recent 5 posts including captions,
> engagement metrics (likes, comments, shares, saves, views), and any
> hashtags or keywords used.
> 
> For X/Twitter, scrape these profiles:
> 
> - https://x.com/minchoi
> - https://x.com/AnthropicAI
> - https://x.com/alex_prompter
> 
> History
> Today at 18:32
> 
> Today at 18:27
> **Description:** A task scheduling page titled “Daily social media briefing” is shown with an active status and a next run time of tomorrow at 7:00. The page includes a description, repeat schedule, allowed Apify actors, and a large instructions panel listing social platforms and X/Twitter profiles to scrape. A history section appears at the bottom with recent run times, and a “Run now” button is visible in the top right.


Every step so far requires you to be at your desk. Scheduled Tasks remove that.

You write instructions once. Cowork runs them on a timer, executes the work, and saves the output to your folder. You open your laptop in the morning and the work is already done.

I use two scheduled tasks every day.

**Task 1: Daily Content Briefing**

Every morning at 7am, Cowork scrapes 200+ profiles across LinkedIn, X, and Instagram using the Apify integration. It ranks posts by engagement, spots trending topics, and drops a structured briefing in my working folder.

![](https://substackcdn.com/image/fetch/$s_!Z8gc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f5bbcff-21d7-47a2-bebd-ff2ec466a915_1902x991.png)
> **Image OCR (auto):**
> **Type:** ui-screenshot
> **Text:** 6 Mar – Daily social media briefing
> 
> View your briefing
> 
> Here's the daily briefing for 06/03/2026. Data pulled from 212 LinkedIn posts, 30+ X/Twitter
> posts across key accounts, and 120 Instagram posts.
> 
> The three stories dominating today:
> 
> GPT-5.4 launched. Sam Altman dropped the announcement with 12.5K likes, OpenAI's
> post hit 22K likes. 1M context, native computer use, Codex integration. This is the dominant
> story on X and is spreading to LinkedIn fast.
> 
> The Anthropic Pentagon controversy is the week's biggest engagement story. Dario's
> statement on the Department of War hit 42,960 likes and 9,524 retweets on X. Massive
> comment count. OpenAI fired back on Instagram about guardrails. High-debate content all
> around.
> 
> Karpathy's coding agents post is still circulating with 37K likes: "coding agents basically
> didn't work before December." Julien Chaumond's local models post on LinkedIn (5K eng)
> and Sebastian Raschka's Qwen3.5 reimplementation (2.5K eng) confirm local AI is having a
> moment.
> 
> Top content opportunity for you today: Anna York's Claude + Semrush MCP post is
> getting strong early traction and it's fresh (6 hours old at scrape time). A marketing-specific
> MCP workflow post from you would ride that wave well. The briefing has 8 specific content
> ideas with rationale in section 7.
> 
> Daily social briefing 06 03 2026
> Document · MD
> 
> Open in Cursor
> 
> Reply...
> 
> Sonnet 4.6
> 
> 7. Content Ideas to Adapt for Your Channels
> 
> High-confidence picks (based on what's working right now):
> 
> 1. GPT-5.4 marketing angle — Take the 1M context window and reframe it for
> marketers. "1M tokens means Claude or GPT can now hold your entire year of email
> copy in one conversation. Here's what that changes."
> 2. AI is changing design — Lenny Rachitsky's Claude design lead interview is getting
> 7.5K+ combined eng. Angle for marketing: "Your brand's design process is 18 months
> behind. Here's what's replacing it."
> 3. MCP + existing tools workflow — Anna York's Claude + Semrush post is blowing up.
> You could do the same for marketing tools: Claude + GA4, Claude + Ahrefs, Claude +
> HubSpot. Specific, practical, show-don't-tell.
> 4. Contrarian SEO/visibility angle — "Ranking #1 is no longer winning" is a hook that's
> working. For you: "Your LinkedIn follower count no longer means what it used to.
> Here's the new metric."
> 5. Karpathy-style vibe post — Short, declarative, authority-driven. "AI changed content
> marketing more in the last 60 days than in the previous 3 years." No carousel. Just the
> claim + 3 specific examples.
> 6. Before/after agent workflow — Julien's local model post worked because of the clear
> before/after structure. Apply to a marketing workflow: "Before Claude agents: 4 hours
> on content briefs. After: 20 minutes. Here's the setup."
> 7. White-collar job displacement (engagement bait with substance) — Steve Nouri's
> post on Anthropic's displacement chart is hitting 1.7K eng. You have authority to go
> deeper on the marketing angle specifically. "Marketing jobs aren't safe. Neither is
> mine. Here's what I'm actually doing about it."
> 8. Instagram: Simple reaction post — @chatgpt's "All good now." got 78K eng. UGC-
> style, minimal caption, relatable AI moment. Record a quick screen video of an AI
> doing something surprisingly good in your workflow.
> 
> Briefing compiled 06/03/2026 | Sources: LinkedIn (212 posts, 68+ profiles), X/Twitter (30+
> posts, key AI accounts), Instagram (120 posts, 5 accounts)
> **Description:** A split-screen desktop view shows a document or chat-based briefing on the left and a markdown document preview on the right. The content is a daily social media briefing with paragraphs and a numbered list of content ideas. The interface includes document controls like “Open in Cursor,” a reply box, and a markdown file title at the top.


To set one up: go to Scheduled Tasks in the desktop app and click New Task. Write your instructions, set your schedule, and toggle “Always allowed” for any integrations the task needs to run without interruption.

The instructions I use for the briefing: