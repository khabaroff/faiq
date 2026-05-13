## 2026-05-13T13:21:43+04:00

https://charliehills.substack.com/p/claude-cowork?r=llvd&utm_medium=ios&triedRedirect=true

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

Cowork does not carry memory between sessions the way claude.ai does. Every new session starts fresh. But you control what it reads at the start.

When you open a session, select the folder you want to work from. Cowork reads every file inside it. If you have a client folder with their brand voice, past posts, contact list, and working notes, all of that loads as context the moment you start. You do not need to re-explain anything.

This is the workaround for Cowork’s missing cross-session memory. Your files are the memory. The better your files, the less you repeat yourself.

Type /memory-management in any session to check what context is loaded. You can see which files Cowork has read, verify it has the right information, and spot gaps before you start working. Five seconds of checking saves you from realising halfway through a task that Cowork is missing half the brief.

![](https://substackcdn.com/image/fetch/$s_!mxbe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92f0b4e9-a2c0-4648-8efe-b617409f536a_2470x1404.png)

The next step is the one that changes your output quality.

Create a folder called “Claude Context” with three files inside it.

“about-me.md” covers who you are, your role, and what good work looks like in your context. “brand-voice.md” covers how you write, your phrases, your tone, what sounds wrong to you. “working-style.md” covers how you want Claude to behave. Questions before it starts or not. Short or long outputs. Which formats.

![](https://substackcdn.com/image/fetch/$s_!i2BA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37756aa2-9d9d-4b4d-bc07-cd8e60d4a117_1628x772.png)

Save them as.md files. These compound over time. Refine them weekly and the output tightens with each session.

If you followed last week’s guide, you already have a profile.md built from your full ChatGPT history. Drop it into this folder alongside your other context files. It gives Cowork deep context on day one.

If you have not done the migration yet, start there. It takes 20 minutes and gives you a structured profile covering your writing style, frameworks, projects, and preferences.

Cowork can access unlimited files in your granted folders. Projects in claude.ai cap at 20 files. If you need deep context on a client, put everything in a local folder and point Cowork at it.

Your first prompt after selecting this folder:

> Read all the files in this folder completely. Then give me a summary of what you know about me, how I work, and what context you have access to.

This forces Claude to absorb your context before starting anything. It also tells you immediately if your context files are written well enough.

![](https://substackcdn.com/image/fetch/$s_!pLsJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84413bf8-523e-4ce4-bcb5-3360f46a50d4_1976x1574.png)

---

### Feature 2: Instructions

Instructions are standing orders you write once. They load automatically at the start of every Cowork session. No re-explaining yourself.

Global instructions apply everywhere. Folder instructions apply when you select a specific local folder. With both set up properly, Claude starts every session already knowing your name, your role, your output defaults, and your communication preferences.

How to set them up. Go to Settings > Cowork in the desktop app. Click “Edit” next to Global Instructions. Write what you want Claude to always know.

![](https://substackcdn.com/image/fetch/$s_!hiTa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F497c65ad-d4c3-418d-a57a-7d317c45ff64_986x787.png)

What to include: your name, role, and what you do. Communication preferences. Output defaults like “always save documents as.docx unless I say otherwise.” Working style preferences. Things to avoid.

Folder instructions work the same way but per project. Each client folder gets its own brief that loads automatically. Full context, every time. I’m setting this up for every client at my agency. One folder per client, one set of instructions, and every team member working from the same context.

After setting global instructions, open a new session and test it:

> Before we start any work, tell me what you know about me, how I like to work, and any standing preferences you are aware of.

![](https://substackcdn.com/image/fetch/$s_!xOVD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7051eb86-1680-4523-8ea1-6f2f3932b8b6_986x787.png)

If Claude reflects your instructions back accurately, you are ready. If something is missing, fix it now.

Your context files and instructions are not set-and-forget. After every session where Claude produces something good, ask yourself if the context files need updating. New client? Add them to your about-me.md. Refined your tone? Update brand-voice.md. Changed your output preferences? Edit working-style.md.

You can also update memory mid-session. Type /memory-management and add new information directly. If you’ve landed a new client, changed your posting schedule, or shifted your content strategy, add it there. It loads into the current session immediately and persists in your files for the next one.

![](https://substackcdn.com/image/fetch/$s_!dPKa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33420550-6942-4fea-8bc7-0706928d5014_2470x1404.png)

The rule is simple. If you find yourself re-explaining something to Claude, it belongs in a file.

Your context files give Claude your history. Your instructions give Claude your rules. Both load before you type a single message. Now we need data.

---

### Feature 3: AskUserQuestion

![](https://substackcdn.com/image/fetch/$s_!If9_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae8e194a-1582-4b23-8dc2-68c0cc0bdb83_1347x761.png)

Every other AI tool guesses when your task is unclear. Confidently. Then gives you polished output that answers the wrong question.

Cowork stops and generates a form instead. Structured questions with multiple-choice options. You iterate until you and Claude are aligned, then it executes.

I showed this to my team and it was the thing that made them reconsider ChatGPT. Claude gives you actual clickable options rather than forcing you to prompt your way to clarity. It breaks your request into subtasks, shows you the plan, and then executes step by step. ChatGPT charges ahead with assumptions. Claude asks first.

Use this as your default opener for any non-trivial task:

> I want to \[YOUR TASK\] so that \[WHAT GOOD LOOKS LIKE\]. First, read all uploaded files completely before responding. DO NOT start executing yet. Ask me clarifying questions to refine the approach. Only begin work once we have aligned.

![](https://substackcdn.com/image/fetch/$s_!uUrY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4237b20c-5647-4f92-837a-5d7ca73d2044_990x791.png)

Try it once and you will stop writing long, engineered prompts from scratch. Context compounds. Prompt engineering depreciates.

The richer your about-me files, brand voice docs, and working style instructions, the better every output gets without extra work in the conversation. Anthropic is building the prompting layer into the tool itself. What scales is your context files, not your prompts.

---

### Feature 4: Connectors

Link your tools once and Claude references live data from them mid-session. Over 50 integrations available. Slack, Google Drive, Google Calendar, Notion, Figma, Asana, Apify, ClickUp, and more. Free on all plans.

You can also build custom MCP connectors. MCP stands for Model Context Protocol. An API connects one app to one other app. MCP connects one LLM to any app through the same standard. Anything with an API key can become a connector.

To connect: go to Settings > Connectors in Claude Desktop. Browse the directory, click a connector, authenticate, done. You only do this once.

![](https://substackcdn.com/image/fetch/$s_!cWyK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F778da554-69db-4746-858a-9f8e0a29a919_986x787.png)

**Apify (Social Scraping)**

Apify scrapes data from any website. I connected it and asked Claude to pull my last 30 LinkedIn posts, rank them by engagement, and give me a full breakdown.

> Use Apify to scrape my last 30 LinkedIn posts. Rank them by engagement. Give me a full breakdown.

![](https://substackcdn.com/image/fetch/$s_!Joyb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83b9722a-1dd1-4acb-a93a-ec79eebe7b15_2470x1404.png)

Claude returned the top post with exact likes, comments, and shares. An analysis of why each post performed. The topic, the format, the posting time. It identified which posts were carousels versus text-only, which surprised me because I didn’t expect it to detect format from scraped data.

The output reads like a strategy report. Content themes, underperforming formats, posting patterns. This is what my custom model Stanley does, rebuilt inside Claude with one prompt.

I ran six accounts through the same process for competitor analysis. Claude compared engagement rates, top-performing posts, trending topics, and content angles across all six.

Some data was off. One follower count was wrong by about 50k. Another account didn’t appear in the ranking at all. The directional analysis and pattern identification were solid. For client work, you verify the numbers, but the structure and insights save hours.

> Use Apify to scrape the last 20 posts from \[competitor 1\], \[competitor 2\], \[competitor 3\]. Compare engagement rates, top content themes, and formats. Give me strategic recommendations.

![](https://substackcdn.com/image/fetch/$s_!mow4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6118ce9-4468-43d4-a39b-2e496715c6b4_2470x1404.png)

This is step one of my daily workflow. That comes in Feature 4.

Here is what this looks like in practice.

**Slack Triage**

I asked Cowork to search my Slack DMs and surface anything I had not responded to, ordered by priority. It found unread threads and compiled a full summary.

> Search my Slack messages from the last 7 days and give me a summary of anything I need to follow up on. Organise by urgency.

![](https://substackcdn.com/image/fetch/$s_!woR8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a8f6997-86d3-437e-bca2-99f6db5e667f_1976x1500.png)

That’s work I used to hand off to a VA. Now it takes one prompt.

**Notion Integration**

After Claude writes a LinkedIn post, I ask it to create a carousel design brief and save it as a new page in Notion. Slide-by-slide breakdown with my caption included. The design team picks it up without me writing a separate brief.

> Connect to Notion. Create a carousel design brief based on this post. Include a slide-by-slide breakdown and save it as a new page in my content calendar.

![](https://substackcdn.com/image/fetch/$s_!xLgJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff15e737f-8797-4d36-a48c-74e4489005ac_1638x1712.png)

I also use Notion for team accountability. Claude checks all boards, finds tasks more than two days past due, and adds comments directly into the Notion pages.

![](https://substackcdn.com/image/fetch/$s_!3sYp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdca6d552-368a-4cd1-95d6-5b43b96b162e_2620x1172.png)

**Gmail and Calendar**

Cowork reads your inbox, categorises emails, and labels messages. It reads your calendar and flags where you have focused work time between meetings.

> Look at my calendar for this week. Flag any days with back-to-back meetings and tell me where I have focused work time available.

![](https://substackcdn.com/image/fetch/$s_!giNJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58da2e50-47a0-410d-8bd0-841bb3162647_1862x1500.png)

**Google Drive**

> Find the most recent document about \[PROJECT NAME\] in my Drive. Read it and tell me the three most important things I need to know.

---

### Feature 5: Plugins

![](https://substackcdn.com/image/fetch/$s_!MjC3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffad3de4-aa20-4a64-9a07-705bebab09dc_990x791.png)

Without a plugin, Cowork is a capable generalist. Plugins make it a specialist.

Anthropic shipped 11 official plugins in January 2026. Productivity, Marketing, Sales, Finance, Data Analysis, Legal, Product Management, Customer Support, Enterprise Search, Biology Research, and more being added.

When the Legal plugin launched, Thomson Reuters dropped 16% in a single trading session. LegalZoom fell 20%. That is what happens when AI starts doing specialised work rather than drafting emails.

![Claude Crash Impact on Thomson Reuters + LexisNexis is Irrational –  Artificial Lawyer](https://substackcdn.com/image/fetch/$s_!tsVb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73728211-f3b4-4ff7-abd4-163b298ea68b_1024x792.png)

Claude Crash Impact on Thomson Reuters + LexisNexis is Irrational – Artificial Lawyer

To install one: click the “+” button in the Cowork chat bar, then click “Plugins.” Browse the library, click Install on the one that matches your role. Type “/” in any Cowork session to see the slash commands that plugin adds.

This is where the workflow from Features 1-3 pays off. Claude has your context files loaded. Apify has pulled your engagement data and trending content. AskUserQuestion has aligned the brief. The Marketing plugin executes it.

> /marketing:draft-content Write a LinkedIn post about \[TOPIC\]. Match the voice from my brand-voice.md file. Target \[AUDIENCE\]. Goal: \[WHAT I WANT PEOPLE TO DO\].

![](https://substackcdn.com/image/fetch/$s_!xtqj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F834f5f75-5db8-4649-ae8b-8677999b0657_1862x1404.png)

The plugin follows a proven structure rather than guessing. It writes the post in my voice, informed by today’s trends, built on two years of context, and formatted to my exact rules. The output is noticeably tighter than a raw prompt.

Once the post is written, I chain back to the Notion connector from Feature 3. Claude creates a carousel design brief and saves it as a new page in my content calendar. Post, brief, and visual direction in one session.

Other plugins worth installing:

> /productivity:start Let’s review what I need to accomplish today and set up my task list.

![](https://substackcdn.com/image/fetch/$s_!lNGM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13aec689-c9f7-4251-8b78-b6e8ee64518f_1862x1404.png)

> /data:explore I have uploaded a CSV in this folder. Give me a summary of what is in it, flag any anomalies, and suggest three analyses worth running.

![](https://substackcdn.com/image/fetch/$s_!B7dt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8ede3fc2-951a-4138-87a1-391b51276fd2_2470x1404.png)

One caveat: plugins load additional context into every session, which means they consume more of your monthly usage allocation. Install the ones relevant to your role and leave the others for when you need them.

---

### Feature 6: Scheduled Tasks

![](https://substackcdn.com/image/fetch/$s_!kFNJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fdc213e-ff9f-4592-8bb1-17ef383bf28a_1902x1324.png)

Every step so far requires you to be at your desk. Scheduled Tasks remove that.

You write instructions once. Cowork runs them on a timer, executes the work, and saves the output to your folder. You open your laptop in the morning and the work is already done.

I use two scheduled tasks every day.

**Task 1: Daily Content Briefing**

Every morning at 7am, Cowork scrapes 200+ profiles across LinkedIn, X, and Instagram using the Apify integration. It ranks posts by engagement, spots trending topics, and drops a structured briefing in my working folder.

![](https://substackcdn.com/image/fetch/$s_!Z8gc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f5bbcff-21d7-47a2-bebd-ff2ec466a915_1902x991.png)

To set one up: go to Scheduled Tasks in the desktop app and click New Task. Write your instructions, set your schedule, and toggle “Always allowed” for any integrations the task needs to run without interruption.

The instructions I use for the briefing: