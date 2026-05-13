## 2026-05-12T09:53:39+04:00

https://artificialcorner.com/p/claude-notebooklm

### Connect NotebookLM to Claude Cowork to build reports, infographics, dashboards, and custom apps. All powered by your own notebooks.

Most people use [NotebookLM](https://artificialcorner.com/p/notebooklm) and [Claude Cowork](https://artificialcorner.com/p/cowork) separately.

NotebookLM to do research or get answers grounded in their documents. Cowork for building a report, infographic, dashboard, and apps without coding.

Connect them, and you get something unique. Tools built on your own data. The research layer and the build layer finally talk to each other.

Nobody does this. Everyone should.

In this guide, you’ll learn:

- How to connect NotebookLM to Claude Cowork
- Use Case 1: Turn spreadsheets into infographics your CEO will read
- Use Case 2: Build a personal language tutor app before your next trip abroad
- Use Case 3: Spy on competitor content and extract what’s working

### What does connecting NotebookLM and Claude Cowork solve?

Two things.

**One. Your data becomes the source of truth.**

NotebookLM grounds every answer in the sources you upload. Every claim traces back to a citation you can click.

Cowork normally runs on training data. Useful, but can be generic. Connect it to NotebookLM and Cowork now reasons from your sources. Your internal docs or your research.

**Two. Static knowledge becomes a working tool.**

NotebookLM alone stays “ *ask and read.*” You open it, type a question, read the answer, and close the tab.

Cowork turns that same knowledge into an app you operate. An artifact or infographic creator. Something you use every week, not a tab you forget.

Build once. Run forever.

![](https://substackcdn.com/image/fetch/$s_!IOff!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3975bc5b-472f-444b-9e03-28138993c2a2_1942x1310.png)

### How to connect NotebookLM and Claude Cowork

![](https://substackcdn.com/image/fetch/$s_!KfL9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b0cb954-80f7-460c-bd20-051a10fe411c_1360x742.png)

There is no official connector.

What works is this repo: [github.com/teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py).

Unofficial, but powerful.

#### Step 1: Install NotebookLM-py

Run this prompt in Cowork:

```markup
Install this skill :https://github.com/teng-lin/notebooklm-py
I want to use it via CLI
```

Let it work. The progress bar shows up in the top right.

![](https://substackcdn.com/image/fetch/$s_!RMjR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3b7f824-5dbb-499c-8de0-839a25fa3043_2368x1020.png)

#### Step 2: Turn it into a Skill

Next prompt:

> I want to drive this on Claude Cowork because I’ll turn it into a skill and do whatever is needed.

Cowork starts building.

Watch the progress bar on the top right, walk through the checklist.

![](https://substackcdn.com/image/fetch/$s_!hCm5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1a0c444-9a52-466d-9993-432c0e8bb2f1_2368x1702.png)

#### Step 3: Auth

Cowork cannot log into Google from the sandbox.

You log in on your Mac and hand the session back.

![](https://substackcdn.com/image/fetch/$s_!TdJO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f81f863-3998-4fa2-b489-e4fd2f896be4_2368x1702.png)

Open your terminal.

**New to the terminal?**

The terminal is a simple text window where you type commands instead of clicking buttons. Do not panic, you only need it once for this setup.

**On Mac:** Press `Cmd + Space`, type `Terminal`, hit Enter.

![](https://substackcdn.com/image/fetch/$s_!_pQ4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2942213-36e3-4f64-9aa3-6b8891f4be67_1280x906.png)

**On Windows:** Press the Windows key, type `PowerShell`, hit Enter.

A black or white window opens. That’s it.

![](https://substackcdn.com/image/fetch/$s_!jT5A!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb88b145a-1208-4c90-9a37-0a820d8f5462_1382x714.png)

[Reference](https://www.digitalcitizen.life/simple-questions-what-powershell-what-can-you-do-it/)

Paste the command below:

```markup
notebooklm login
```

A browser window opens. Log in with your Google account.

Wait until the NotebookLM homepage loads.

![](https://substackcdn.com/image/fetch/$s_!dKMo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bb18b8c-b8b9-4355-965a-32dc040f2c7a_2368x1702.png)

Go back to the terminal.

Press Enter.

![](https://substackcdn.com/image/fetch/$s_!_4Cf!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F281dae98-bf5f-46af-a01d-1cd41d6a0010_1132x362.png)

The terminal prints the path to your `storage_state.json`.

![](https://substackcdn.com/image/fetch/$s_!iFUJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F993ef443-6363-494c-896e-60d21bdc98d8_1132x416.png)

Copy it. Paste it back into Cowork:

```markup
Authentication saved to: /Users/learnai/.notebooklm/storage_state.json
```

Done! Cowork now has your credentials.

![](https://substackcdn.com/image/fetch/$s_!3RPd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfc008d0-a2a9-46d1-8555-a1ef62b70cad_2374x1664.png)

> **Note:** If Cowork cannot reach the file, ask Claude Code to copy-paste the auth file into your working folder.

#### Step 4: Testing

Time to test the skill. Type /notebooklm

![](https://substackcdn.com/image/fetch/$s_!RPy7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8407fef3-a8a6-4e50-b9a2-8d583a79b0f9_1798x712.png)

Ask it to list your previous notebooks.

![](https://substackcdn.com/image/fetch/$s_!hffv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7178426c-5b3f-4b32-9176-832a8665f0ce_2446x1692.png)

Mine pulled 120 notebooks from October 2024 through today.

![](https://substackcdn.com/image/fetch/$s_!FBRi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21625fac-57df-4059-9d30-cb13c032e20c_2366x1148.png)

Fair warning, I am a pretty heavy NotebookLM user.

Let’s see my favorite use cases:

### Use Case 1: Turn Ugly Spreadsheets Into Infographics Your CEO Will Actually Read

You know the drill.

You have a messy CSV.

Three different date formats in one column. Somebody’s initials in row 857 for no reason.

Your CEO drops a message: “Give me a summary by Friday.”

You spend three hours in Excel building pivot tables. Another hour picking a chart template that does not look like 2008. You created an infographic. Your CEO opens it, scrolls for four seconds, and closes it.

Nobody reads it.

Here is the version that works.

#### Step 1. Upload the spreadsheet to NotebookLM

Drop the CSV in as a source. NotebookLM parses the data, finds the patterns, and flags the anomalies.

You did not write a single formula.

Takes under a minute.

I’m using [this data](https://www.kaggle.com/datasets/ronnykym/online-store-sales-data) as an example, r *etail sales data from an online store.*

Here is how my NotebookLM looks after uploading this data.

![](https://substackcdn.com/image/fetch/$s_!7lXg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c345951-35a5-464f-b015-e4b171cf9b1f_3440x1788.png)

#### Step 2. Ask NotebookLM what matters

Paste this:

```markup
What are the five most important insights in this data? 
Ignore noise. Focus on what a non-technical executive would care about.
Each insight should be one sentence.
```

NotebookLM returns grounded answers.

Every insight traces back to specific rows. Click the citation, and see exactly where the number came from.

![](https://substackcdn.com/image/fetch/$s_!hUFx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F812535b3-62ad-4657-8def-2ff453a0567f_3450x1802.png)

You now have the story before you have touched a design tool.

#### Step 3. Trigger the NotebookLM skill in Cowork

Open a new Cowork session. Trigger the skill:

```markup
/notebooklm Reach this notebook: European Export Sales Registry 2019-2020
```

Cowork now has read access to every source and every insight NotebookLM found.

![](https://substackcdn.com/image/fetch/$s_!l_Ak!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa36319fa-3489-4d3a-94c1-c55d4a548302_2378x1298.png)

#### Step 4. Give Cowork the build command

Paste this:

```markup
Build a web app that pulls the top five insights from the notebook 
and renders each one as a visual element. 

Let the user pick a style: minimal, corporate, or playful. 
Each style should have its own color palette, typography, and layout. 

Add a PNG export button.
```

After pasting, it started talking with the notebookLM.

![](https://substackcdn.com/image/fetch/$s_!2Wsy!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d66fc60-dc3f-4f14-af68-3b28ff170ef4_854x238.png)

You can see the conversation from the NotebookLM.

![](https://substackcdn.com/image/fetch/$s_!Ptqn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ebb3742-e1cb-49c4-8c57-2ca91e86f3a1_3414x1796.png)

After getting the insights, it is now building the app.

![](https://substackcdn.com/image/fetch/$s_!Q0vK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F967542cd-8bd9-43d0-9d4e-0274bfa0ef6f_1118x448.png)

And it is done.

![](https://substackcdn.com/image/fetch/$s_!5TAG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c6e75b9-1b6f-4b6f-92de-4469d8dafc8e_2444x1786.png)

#### Step 5. Export and ship

Click “corporate.”

Your five insights render as a clean one-page infographic

![](https://substackcdn.com/image/fetch/$s_!0yhU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1686dfa-8617-466d-b360-4b6efef35fa0_1630x3374.png)

Or minimal.

![](https://substackcdn.com/image/fetch/$s_!8C1X!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06bf7c40-abdf-4ad6-892e-416f7528856e_1630x2558.png)

Or playful.

![](https://substackcdn.com/image/fetch/$s_!KauB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9570abd-cc01-49a1-aa3b-011a05efb14f_1630x2642.png)

### Use Case 2: Build a Personal Language Tutor App Before Your Next Trip Abroad

You booked a flight to Barcelona. Three weeks out. You know ten Spanish words. Five of them are food.

Duolingo teaches you sentences nobody says. Google Translate is fine at the airport, but useless at dinner.

You don’t need another language app. You need a tutor who knows your trip: The neighborhood you are staying in, the phrases locals actually use, etc.

We’ll build a tutor with NotebookLM and Cowork.

#### Step 1. Let NotebookLM research your trip

Open NotebookLM. Create a new notebook. Name it `barcelona-trip-tutor`.

Click “Discover sources.” Switch on **Deep Research**. Paste this:

```markup
Research everything a first-time traveler needs to know about 
Barcelona for a trip in [MONTH/YEAR]. Focus on:

- Neighborhood guides for staying in Eixample, Gothic Quarter, 
  and Gracia
- Top 20 restaurants and tapas bars across different price points 
  (include addresses and what to order)
- Metro and bus system basics (which lines tourists actually use)
- Cultural etiquette Spanish people care about but tourists miss 
  (meal times, tipping, greeting)
- Common scams targeting tourists and how to avoid them
- Day trips within 1 hour of Barcelona (Montserrat, Sitges, Girona)
- Typical Spanish phrases locals use daily that tourists do not know
- Seasonal context: weather, festivals, crowds for [MONTH]

Prioritize sources from local bloggers and expat guides 
over generic travel sites.
```

After pasting this notebookLM, import the sources and here your notebook is ready.

![](https://substackcdn.com/image/fetch/$s_!5hQ0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1010da8d-4d44-46fa-a855-4338be66c2ce_3432x1798.png)

#### Step 2. Ask NotebookLM to build the curriculum

Sanity-check first. Ask the notebook: “Which neighborhood am I staying in, and what are three phrases I will need there?” If the answer pulls from the research you asked for, you are good.

Then paste the curriculum prompt:

```markup
Based on the sources in this notebook, build me a 14-day 
Spanish crash course for my Barcelona trip.

Each day should cover:
- Five new phrases I will actually use on this specific trip
- Context for where and when I would use them 
  (hotel, tapas bar, metro, taxi)
- Pronunciation in plain English (not IPA)
- One cultural note about using that phrase

Prioritize phrases relevant to my hotel neighborhood, 
my restaurant bookings, and getting around the city.

Include Catalan variants where locals in Barcelona would 
appreciate hearing it (Catalonia has its own language alongside Spanish).

Skip greetings I already know like “hola” and “gracias.”
```

NotebookLM returns a 14-day plan grounded in your actual trip. Not generic Spanish. Your Spanish.

Here it is.

 <video controls=""><source src="https://artificialcorner.com/api/v1/video/upload/890edb41-1a7f-4375-ac6a-b8d3a6db9de7/src?override_publication_id=1867166&amp;type=hls" type="application/x-mpegURL"> <source src="https://artificialcorner.com/api/v1/video/upload/890edb41-1a7f-4375-ac6a-b8d3a6db9de7/src?override_publication_id=1867166&amp;type=mp4" type="video/mp4"></video>

#### Step 3. Trigger the NotebookLM skill in Cowork

Open a new Cowork session:

```markup
/notebooklm Reach this notebook: barcelona-trip-tutor
```

And here it connects.

![](https://substackcdn.com/image/fetch/$s_!IrF8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb2068d2-1c09-4d60-a7e1-23ba623341d6_2392x866.png)

Cowork now has your trip context and your curriculum.

#### Step 4. Build the tutor app

Paste this:

```markup
Build an artifact called “Barcelona Tutor” with three sections:

1. TODAY’S LESSON

   Show today’s five phrases with pronunciation and context.

   Mark a phrase as “learned” with a checkbox.

   Progress bar shows how many phrases I have learned this week.

2. QUICK DRILL

   Flashcard mode. Show the English phrase, I guess the Spanish.

   Tap to flip. Rate myself (easy/medium/hard).

   Hard cards come back tomorrow. Easy ones disappear.

3. TRIP SCENARIOS

   Pre-built roleplays for: hotel check-in, ordering tapas, 

   taking the metro, asking for directions.

   I pick a scenario, the app shows me the likely script 

   with my phrases highlighted.

Pull all phrases, pronunciations, and cultural notes 

from the connected NotebookLM notebook.
```

And click on “Create” when it asks.

![](https://substackcdn.com/image/fetch/$s_!d_hq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64a0ea14-f489-4a49-adf7-923f908e9827_2412x1676.png)

Here is your app.

 <video controls=""><source src="https://artificialcorner.com/api/v1/video/upload/e2f5f961-3cef-487c-a595-61176cb67c58/src?override_publication_id=1867166&amp;type=hls" type="application/x-mpegURL"> <source src="https://artificialcorner.com/api/v1/video/upload/e2f5f961-3cef-487c-a595-61176cb67c58/src?override_publication_id=1867166&amp;type=mp4" type="video/mp4"></video>

Three tabs, one live app, built in ten minutes.

**Today’s Lesson** feeds me five phrases I will actually use in Barcelona.

**Quick Drill** turns them into flashcards with spaced repetition, so hard cards come back tomorrow, and easy ones get out of my way.

**Trip Scenarios** drops me into real roleplays, asking for directions in the Gothic Quarter, ordering tapas, checking into the hotel, with my own phrases highlighted in the script.

Every word traces back to the NotebookLM notebook I built in Step 1. Grounded curriculum, personal context, zero generic Duolingo energy.

### Use Case 3: Spy on Competitor Content and Extract What’s Actually Working

Every writer stares at the same question on Monday morning.

What should I write this week?

You scroll through three competitor Substacks. You read ten articles. You try to reverse-engineer what made their viral posts hit. You take messy notes. You forget half of them by Wednesday. You end up guessing anyway.

Twenty hours a month, gone. Pattern recognition done by vibes.

Here is the version that works.

#### Step 1. Collect competitor URLs into one place

Pick three to five writers in your niche.

Grab the URLs of their last free articles. ( to get the tone)

Fastest way: open their Substack archive page, scroll to the bottom, and copy the list.

Here are my articles.

```markup
1- NotebookLM Prompts for Students 

↳ http://gencay.substack.com/p/notebooklm-prompts-for-studying

2- NotebookLM Prompts to Beat 99%

↳  https://gencay.substack.com/p/10-notebooklm-prompts-that-put-you

3- Free 2026 AI Learning Path

↳ https://gencay.substack.com/p/how-to-learn-ai-in-2026-without-spending

4- Run Claude Code Locally (Free)

↳ https://gencay.substack.com/p/how-to-run-claude-code-locally-100

5- Claude Code Source Code Leaked

↳ http://gencay.substack.com/p/claude-code-source-code-free

6- Claude Code + Telegram

↳ https://gencay.substack.com/how-to-connect-claude-code-with-telegram

7- 7 Hidden Claude Features

↳ https://gencay.substack.com/p/claude-hidden-features-guide

8- ChatGPT → Claude: 5 Surprises

↳ https://gencay.substack.com/p/5-surprises-that-hit-you-when-you

9- Claude Cowork: What Actually Works

↳ https://gencay.substack.com/p/i-tested-all-claude-cowork-features

10- Claude for Content Creation

↳ https://gencay.substack.com/p/the-developer-tool-thats-quietly

11- OpenClaw Better Than 99%

↳ https://gencay.substack.com/p/how-to-use-openclaw-better-than-99

12- Clawdbot Setup (Cheapest + Secure): 

↳ https://gencay.substack.com/p/clawdbotopenclaw-cheapest-most-secure

13- Hire a Free AI Employee (Clawdbot): 

↳ https://gencay.substack.com/p/how-i-hired-a-free-ai-employee-clawdbot
```

#### Step 2. Upload to NotebookLM

Create a new NotebookLM notebook.

Select a web search and use this prompt with the links above.

```markup
Analyze the following Substack articles as competitor intelligence.

Extract:

* Tone of voice (writing style, pacing, personality)
* Hook patterns (how each article starts)
* Content structure (sections, flow, formatting)
* Title patterns (what makes them clickable)
* CTA strategies (how they drive engagement like restacks, clicks)
* Common topics and positioning
* What makes these posts perform well

Then:

* Identify repeatable patterns across all articles
* Highlight the top 5 strategies I should reuse
* Suggest 5 new article ideas based on these patterns
* Rewrite one viral-style post using these insights

Articles: [pasted from step-1]
```

And make sure to select “Deep research”.

![](https://substackcdn.com/image/fetch/$s_!u3uN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff0f1cc3-700a-4c07-a106-888bd0c1cf6f_1452x1416.png)

#### Step 3. Ask NotebookLM to find the patterns

Step 2 triggered the scrape.

Now that the sources are indexed, we go deeper. Open the notebook chat and paste this

```markup
Analyze all sources in this notebook. Find patterns across the articles.

Return:
1. Top 10 headline formulas (with example headlines for each)
2. Top 5 hook patterns used in the first 200 words
3. Most common article length (words)
4. Most common CTA placements and wording
5. Topics that appear in more than 3 articles

For every claim, cite the specific article it came from.
```

NotebookLM returns grounded patterns.

Every insight traces back to a real article.

Here it is.

![](https://substackcdn.com/image/fetch/$s_!vUkg!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39455b2a-59e3-451e-b293-29d080cfb4d1_3450x1800.png)

#### Step 4. Trigger the NotebookLM skill in Cowork

Open a new Cowork session:

```markup
/notebooklm Reach this notebook: LearnAIWithMe: The Complete Guide to Mastering AI Workflows
```

Point it at the notebookLM you just trained.

![](https://substackcdn.com/image/fetch/$s_!VjXJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe166ac82-81ed-4965-aaba-b8a07a8e74a8_1680x1178.png)

#### Step 5. Build an Artifact

Next, paste this:

```markup
Connect to my NotebookLM notebook <Paste name of your notebooklm>
Build an artifact called “Content Spy Dashboard” with four sections:

1. HEADLINE FORMULAS
   Show the top 10 formulas with usage count. 
   Click any formula to see example headlines that use it.

2. HOOK PATTERNS  
   Show top 5 hook patterns with one-line descriptions. 
   Click to expand and see real examples from competitor articles.

3. TOPIC HEATMAP
   Grid view. Rows = topics. Columns = competitors. 
   Cell shows how many articles each competitor wrote on that topic.

4. GAP FINDER
   List topics the competitors cover often but your niche could 
   approach differently. NotebookLM should suggest angles.

Add a “Generate Draft” button at the bottom. 
When I click it, the app picks a winning formula + a gap topic 
and drafts a headline + opening paragraph in my voice.

Save my past 10 articles as reference for voice matching.
```

Cowork builds.

It queries NotebookLM.(Cowork side)

![](https://substackcdn.com/image/fetch/$s_!B4SU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F310ed02f-e1dc-4af9-bd5d-a7ff7130f555_1604x490.png)

See how it is talking with NotebookLM.

![](https://substackcdn.com/image/fetch/$s_!k0Ts!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b929553-88e7-43c9-a6bf-ec63e20a325a_3452x1804.png)

You can follow the progress from here.

![](https://substackcdn.com/image/fetch/$s_!iN-V!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4303e03-fc4d-4dfa-89ed-dd096cd63f6c_2488x1788.png)

Allow this.

![](https://substackcdn.com/image/fetch/$s_!6HTs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffab6a8e6-6ddc-4837-bab1-29e571b316c5_1526x606.png)

And finished, let’s test it.

#### Step 6. Test the Artifact

Here’s what it looks like.

 <video controls=""><source src="https://artificialcorner.com/api/v1/video/upload/4b70a262-9ad3-4718-9717-5b0212f1500a/src?override_publication_id=1867166&amp;type=hls" type="application/x-mpegURL"> <source src="https://artificialcorner.com/api/v1/video/upload/4b70a262-9ad3-4718-9717-5b0212f1500a/src?override_publication_id=1867166&amp;type=mp4" type="video/mp4"></video>

Cowork built this in under ten minutes.

Eleven of my own articles are indexed as the competitive corpus.

Headline formulas, hook patterns, topic heatmap, gap finder, and a draft generator — all live, all clickable.

The “Generate Draft” button at the bottom is the kicker.

It picks a winning formula, pairs it with a gap topic, and drafts a headline plus opening paragraph in my voice.

From competitive research to the first draft in one click.

> **AI News:** Artifacts recently became available in Cowork.

### Final Thoughts

Most people treat NotebookLM and Cowork as two different drawers.

Research goes in one. The building goes in the other.

They never open both at the same time. That is the mistake.

Connect them, and the math changes. Your sources become the ground. Your apps inherit that ground.

---

Don’t forget to subscribe to [LearnAIWithMe](https://www.learnwithmeai.com/), a newsletter focused on practical AI tutorials for people who’d rather replace than be replaced by AI.