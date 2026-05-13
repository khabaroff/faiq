---
title: As We May Work
slug: 2026-04-12-as-we-may-work
source_url: https://taylorpearson.substack.com/p/as-we-may-work?r=llvd&utm_medium=ios&triedRedirect=true
source_type: article
fetched_at: 2026-05-13
lang: en
---

In July 1945, as World War II was drawing to a close, Vannevar Bush published an essay in The Atlantic Monthly that would set the trajectory for personal computing, hypertext, and the internet. Bush was the director of the Office of Scientific Research and Development where he had coordinated the work of the Manhattan Project and 6,000 American scientists during the war. As the wartime effort was coming to an end, he asked: what should scientists work on next?

His answer: the growing crisis of human knowledge.

![](https://substackcdn.com/image/fetch/$s_!lLhe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae1391c8-f63b-481a-82d0-8b88b1d033e8_1280x1064.png)

“There is a growing mountain of research,” Bush wrote. “But there is increased evidence that we are being bogged down today as specialization extends. The investigator is staggered by... conclusions which he cannot find time to grasp, much less to remember.”

We were still using the same retrieval methods from centuries past: alphabetical indexes and hierarchical filing systems. Bush marveled at the infrastructure of mass production that had been built out in the war effort with vacuum tubes “made by the hundred million, tossed about in packages, plugged into sockets.”

Bush proposed a machine he called the “memex” — a desk-sized device that would combine lower level technologies to achieve a higher level of organized knowledge (like human memory processes). The memex could store all of a person’s books, records, and communications on microfilm and allow them to build connections that would lead to new discoveries.

![](https://substackcdn.com/image/fetch/$s_!a_c2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94df8329-3ee2-4788-b324-e9dedc088b48_1266x1034.png)

Bush illustrated with a scenario: A researcher is studying why the Turkish bow was superior to the English longbow in the Crusades. He pulls up an encyclopedia article, finds a related passage in a history book, ties them together. He branches off into textbooks on elasticity, tables of physical constants. He adds his own handwritten notes. He builds a “trail of his interest through the maze of materials available to him.”

![](https://substackcdn.com/image/fetch/$s_!OBMq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7099a459-8b63-4948-a0c7-14f8616e8b67_1254x1194.png)

Bush’s essay inspired the people who built the digital age. Ted Nelson cited it when developing hypertext. Doug Engelbart, who invented the mouse and demonstrated hyperlinks in 1968, called it a primary influence.

Bush saw how technology generally, and computing specifically, was going to alter the way in which we worked. In 1945, most work involved making things or moving things: the factory, the farm, and the warehouse were where work happened.

Today, 80 years later, many people’s work looks kind of like operating a Memex. It involves sitting at a desk manipulating symbols: writing memos, updating spreadsheets, sending emails, and, of course, sitting in meetings about the memos, spreadsheets and emails while online shopping in another browser tab.

There was no word to described this until Peter Drucker coined the term “knowledge worker” in 1959. Knowledge work is manipulating symbols — words, numbers, formulas, diagrams — such that the output changes what happens in the world. A project plan determines what gets built. A financial model determines where capital gets allocated. A legal brief determines who pays whom.

Our world adapted to this new mode of working. Factories needed to be near raw materials or transport. Knowledge work just needs a desk and a screen and so our physical world was reshaped. We got the office park, the cubicle farm, and eventually the laptop on the kitchen table during COVID. The path from “high school → factory” became “college → cubicle” and the rust belt was supplanted by the sunbelt.

We shape our tools, then our tools shape us.

I have been reflecting on Bush’s essay as I’ve started to use a new technological tool: Claude Code. While “Code” is in the name, Claude Code is better thought of as the leader in a new category of tools for manipulating information broadly.

Code is one type of information, but project plans, legal documents, spreadsheets, and standard operating procedures are all information. In fairness to the creators, “Claude Knowledge Work” doesn’t have quite the same ring to it, but that’s the way to think about it.

I wrote a book in 2016 called *[The End of Jobs](https://www.amazon.com/End-Jobs-Meaning-9-5-ebook/dp/B010L8SYRG/)* which suggested that the combination of global competition and what I broadly called “machines” was going to come to knowledge work in the 2020s in the same way that automation and globalization came to blue-collar work in the 2000s and 2010s.[^1] Claude Code, and the broader product category it represents, feels like an inflection point in that journey.

At the risk of being hyperbolic, Claude Code is the ChatGPT moment repeated. It is the leading product in a new era of AI. If you do knowledge work of any sort, you need to understand what it is and how it works. Claude Code, and the product category it represents, will become the primary tool most knowledge workers use to do their work.[^2]

2025 was the year where AI became a key part of most software engineers’ workflows. “Vibe Coding” went mainstream. When we look back, I think 2026 is going to be an inflection point year where AI did the same for large swaths of knowledge work, beginning an era I’ve been calling freestyle work.

If not on the level of importance of the personal computer, it is at least on the level of the browser. If you are a knowledge worker: marketer, salesperson, writer, developer, designer, project manager, investor, etc. then understanding what it is and how it works is going to be pretty important going forward.

This essay is the result of my attempt to figure that out for myself, as one of a class of people that consider themselves non-technical knowledge workers.

## The Limitations of Chat-Based AI

To understand Claude Code, it’s worth starting with what current AI models actually are and how they work.

All the currently popular AI models are a type of AI known as large language models (LLMs). LLMs are next-token predictors. Given a sequence of text (the “context window”), they use statistical models to predict what comes next.

The models learned these patterns by reading essentially all the text on the internet and embedding them in their weightings. When you ask an LLM to complete a sentence that starts with “the dog is,” you’re likely to get a logical and coherent ending.[^3]

![](https://substackcdn.com/image/fetch/$s_!Zxx0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff745681c-89ad-40aa-a73f-e5677b6b759b_978x368.png)

What’s astonishing about LLMs is that given three paragraphs about your business, your market, and your resources, the same next most likely word prediction process often produces something that reads like incredibly savvy strategic advice. It’s as if auto-complete chugged four Red Bulls, went Super Saiyan, and got access to the nuclear codes.

ChatGPT made LLMs mainstream in late 2022 by creating a chat-based interface to interact with these models and doing some specialized training to have it act more like a helpful assistant than merely auto-complete.

In a sense, LLMs are a societal-level memex. Trained on huge amounts of human text, they embody a vast web of associative trails through statistical relationships learned during training. The Turkish bow connects implicitly to the physics of elasticity and to the history of the Crusades. Those connections exist in the model’s weights.

When you chat with an LLM, you’re embarking on a choose-your-own-adventure through humanity’s collective knowledge. Ask about Turkish bows, branch into physics. Ask about HVAC, branch into building science, then contractor negotiation, then your city’s climate. The “selection by association” Bush imagined is now here at a societal scale.

However, chat-based LLMs like Claude, ChatGPT and Gemini suffer two broad limitations.

1. Their lack of long-term memory.
2. Their inability to do things rather than merely provide instructions.

The models themselves lack the equivalent of long-term memory. You can write or paste text into a chat window and the model will respond based on what is in that window, but it can’t remember anything between conversations. Each session starts fresh.

The societal memex doesn’t know *you*. If you want to ask it questions about your job or business or life, it has lots of general knowledge but no specifics. It knows about HVAC or construction practices in general, but not your house, your budget, or your project history. It knows everything ever written in an MBA textbook, but relatively little about your company.

Talking with AI has historically felt like talking to someone who was always having their first day on the job. Their background was impressive: They had the equivalent of a PhD in mathematics, physics, and history. But, they don’t really know anything about your specific situation.

Context windows are growing, but they’ll always be finite.[^4]

The frontier AI companies (Google, OpenAI, and Anthropic) are obviously aware and trying to find solutions. ChatGPT introduced Custom GPTs in late 2023, allowing you to upload documents and instructions relevant to a specific task. Claude Projects and Gemini Gems followed in 2024. These were attempts to give the models more persistent memory by allowing you to store relevant files.

My usage pattern, which seems typical for other non-technical users, was to create Custom GPTs/Projects/Gems for different life or work areas:

- One for health information that would have relevant information to my health
- One as a business adviser for certain parts of my job.
- One as a home cooking assistant with my recipe and dietary preferences

This allowed you to embed persistent context relevant to these projects.

![](https://substackcdn.com/image/fetch/$s_!CGHE!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95ae9b80-b1d8-4d73-9a9b-87a642902c25_928x1357.png)

This helped, but you were still uploading static snapshots. The model couldn’t engage in “on the job learning.” It couldn’t update its own knowledge, couldn’t write notes to itself, and couldn’t accumulate learning over time. It could read, but it couldn’t remember. It was reliant on your ability to constantly update it.

In practice, this meant constant and tedious maintenance. Imagine you set up a business adviser project with your pricing, client list, and how you structure engagements. As soon as a client churns or your structure evolves, you have to dig through the reference documents to find it and update it.

Multiply that across several projects and you’re spending real time just keeping the AI updated on the current status of projects. Worse, the projects couldn’t talk to each other. The cooking assistant didn’t know about the dietary notes in the health project. The business adviser doesn’t know about a vacation that will take you offline for a week.

It was like having an army of extremely specialized contractors. They were good at what they did, but there was huge coordination overhead keeping them all up to speed on what was going on. The transaction and coordination costs were so high that it often was still more efficient to just do it yourself.

## 50 First Chats

This inability to learn is a major issue for making AI useful at knowledge work. No matter how qualified someone is, they’re rarely very useful or helpful their first day on the job. There’s always a lot of specific knowledge in any company.

Dwarkesh Patel has called this the fundamental bottleneck. “The lack of continual learning is a huge, huge problem,” he wrote. The reason humans are useful isn’t mainly raw intelligence, it’s the ability to “build up context, interrogate their own failures, and pick up small improvements and efficiencies as they practice a task.”

In their current form, chat-based LLMs can’t do that.

They also are limited in the sense that they are, well, chatbots. I spent a couple weeks last year fixing and improving a spreadsheet that tracked an investment portfolio’s performance.

The workflow was that I would copy sections or formulas out of the spreadsheet into the LLM chat, ask it questions and then copy things out of the chat and into the spreadsheet.

I am probably a 4/10 Excel user. I know enough to get around but am not highly proficient. Being able to use LLMs for this kind of task has been a huge benefit to me, but the copy/pasting was pretty tedious and I found myself often wishing it could just fix the spreadsheet itself.

Enter stage left: Claude Code.

## Claude Code Can Write Its Own Memory

Claude Code is a command-line interface (CLI) tool, meaning it can use the command line on your computer. Practically, this means it can do anything on your computer that you can do: It can read, create, and edit files on your computer, not just generate text in a chat window.

Compared with web-based chat apps, that’s a key difference: Claude Code can read and write files. You can think of it as scaffolding that sits on top of the AI model’s general blob of intelligence.

![](https://substackcdn.com/image/fetch/$s_!gUXx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd1e6e22-3e2b-4342-b1a9-ecf3c73dc6f4_2230x1164.png)

One of the obvious (and most widely used) versions of that is to ask it to write software.

But, it can write anything including notes about what it did and why.

I have a set of instructions (called a Skill file in Claude Code) to help me write a monthly newsletter. The AI model uses the instructions in this file like someone at your company might use a standard operating procedure.

![](https://substackcdn.com/image/fetch/$s_!ijaq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd46af2b-edb8-4498-beac-fcf23c2ac5e5_1312x906.png)

I asked it to write a newsletter based on a topic I gave it. The output was OK, but it did some things I didn’t like: it jumped straight into editorializing from my notes.

I went back and edited what it said and asked it to “Compare my version to the version you drafted and update your skill to do it more in my style next time.”

With no other prompting, it drafted the following and added it to the newsletter file in the appropriate place:

![](https://substackcdn.com/image/fetch/$s_!Bv5n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c3d6511-5e69-4898-893b-2738e20f76b9_1386x832.png)

These are all patterns and preferences in my writing that wouldn’t have occurred to me explicitly to state but when reflected back to me like this, are all accurate reflections of my style.

This looks a whole lot like how someone on their first day of a job writing a newsletter for me might take notes (explicitly or implicitly) to do it more in line with the way I want next time.

When an AI can read and write files, it gains the ability to write its own memory and, with memory, the capacity for learning.

It is comparable to how companies use internal training or standard operating procedures. The next time I ask it to write a newsletter, it will look at the notes it took from last time and insert that into the context to use for the task.

If you haven’t used Claude Code or a similar tool before and this all sounds a bit abstract, here’s a short demo.

 <video controls=""><source src="https://taylorpearson.substack.com/api/v1/video/upload/b13516bb-c1cc-4b30-8e85-2d250bc5cfda/src?override_publication_id=25729&amp;type=hls" type="application/x-mpegURL"> <source src="https://taylorpearson.substack.com/api/v1/video/upload/b13516bb-c1cc-4b30-8e85-2d250bc5cfda/src?override_publication_id=25729&amp;type=mp4" type="video/mp4"></video>

While the Claude model itself is the ‘intelligence’ — it reads, writes, and reasons. Claude Code is the harness around it: the files it can access, the tools it can use, and the rules it follows.

On top of Claude Code itself sits personal scaffolding that you can customize. Skills are perhaps the best example. You can create a skill with instructions for how to write a newsletter, close the monthly books, or format a client proposal.

![](https://substackcdn.com/image/fetch/$s_!ScW_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdac74d9-4096-4998-86e2-a3e7c80f8bde_2078x1722.png)

These are all just text files on your computer that any LLM can read and use. The analogy to how knowledge workers work should be pretty obvious.

![](https://substackcdn.com/image/fetch/$s_!l5wM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbf7e3e6-ec2a-4b81-99b0-e85ce151dc7b_1300x1278.png)

Imagine you hire a marketer who spent five years doing email campaigns for a sunglasses brand. She knows how to write subject lines, segment lists, and structure a launch sequence — that’s her general training, the equivalent of the model’s weights.

But when she starts at a snack bar company, she doesn’t know your brand voice, your product launch calendar, or that your audience responds better to nutrition science than lifestyle imagery.

You give her brand guidelines, a style doc, and the last six months of campaign performance. That’s the context-specific ‘harness’ — that shapes her general skills into something useful in that particular situation.

She then has the ability to improve and shape those over time. Claude Code can do the same. You could copy in your last ten newsletters and their performance then use Claude Code to analyze which ones performed better or worse and what you could learn going forward.

There is still judgement required in overseeing it and the models still make mistakes, but everyone I know who has tried using it for similar tasks has been shocked at the quality of the results.

But its ability to write its own memory isn’t the whole breakthrough. Claude Code has memory *within a composable environment*.

## A Castle Made of Legos

Claude Code uses the terminal on your computer to do its work. The terminal is built on a 50-year-old design philosophy, Unix, which has some simple principles:

> 1. Make each program do one thing well.
> 2. Expect the output of every program to become the input to another.
> 3. Write programs to handle text streams, because that is a universal interface.

Unix is built so it can pipe the output of one command into another, combining simple pieces into complex workflows — like Lego bricks versus a single molded toy.

Claude Code inherits this philosophy: it reads files, writes files, calls other tools, and passes text between them. It uses small tools, composed together, to create capabilities that no single tool has.

Watching Claude Code work you can see this philosophy in action — the tools it’s calling are shown in bold: Read, Glob, and Web Fetch. Each of these commands is simple: Read a file, search for another file on my computer (Glob), and then read a webpage.

These are small, simple commands for an LLM to execute.

![](https://substackcdn.com/image/fetch/$s_!sFEK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea6ea296-b364-4b1f-9ceb-94df58f6e548_1438x1376.png)

What makes them powerful is that they are composable and can be chained together. The model (Claude) is able to use these tools from the harness (Claude Code) in sequence to produce a complex output like writing a newsletter.

Because of this design philosophy, you can always add new tools, and they immediately work with everything else.

Skills can call other skills inside themselves. If you have a branding guide, the newsletter skill might call the branding guide towards the end to do all the formatting and layout.

Tools also aren’t limited to your local files. Any piece of software that has an API (which is pretty much all software at this point like Gmail, Google Calendar, Slack, your CRM) can be used.[^5]

It can check your calendar, pull up recent emails, update a spreadsheet or mark a task as completed in Asana. Each new connection works with everything else. Data from one tool can be routed into another tool or used to create a file.

The seemingly simple technical ability to have filesystem and command line access results in something remarkable: an AI that can read files, write files, search across documents, chain tools together, and build on its own previous work. It has memory and it has the ability to extend itself into any use case that can be described in text and done on a computer.

Claude Code can, in principle, do anything we would describe as knowledge work: manipulating symbols, be they words, numbers, formulas, or diagrams. In practice, it is not (yet) able to do everything well and the question of when/if it will be able to do different parts of knowledge work is obviously important (a topic for a future essay).

## The Emergent Operating System

This design creates emergent possibilities where new capabilities can arise that weren’t designed in advance. Here’s an example of how it played out for me.

Because I knew that Claude’s context was wiped at the end of each chat session, I asked Claude Code to write a summary of what happened into a “workbench” file associated with that project — what got done, decisions made, open questions. This is a habit I’ve done manually for a long time as a way to easily pick up where I left off on a project. It was easy to ask Claude Code to write it for me instead by using our chat history.

After a few days, I realized the daily entries across all my projects could roll up into a single daily summary. So I told Claude to summarize what got done in project-level workbenches and add it to a daily log file (e.g. YYYY-MM-DD) at the end of each chat session.

When I started doing my weekly review and planning, I already had seven daily summaries sitting there. I told Claude to compare those daily reports to the weekly plan, checking what I said I’d focus on versus what I actually did, flag the gaps, and give me a report.

With that report, it was straightforward to see how my time lined up with my goals without doing the tedious cross-referencing myself. And if I decide to reprioritize, I can tell Claude to update my quarterly goals right there. Because it has access to tools like my Google Calendar, it can check whether I actually have time for what I’m planning.

You can see how this might be extended in other ways. If you send a weekly update to your team, it would be easy to ask Claude to reformat your internal version for a team audience: you could use a skill that adds more context for people who aren’t in your head all day and removes personal plans you have for the week.

You could review the weekly reports once a month or once a quarter as part of planning on those cadences. If everyone on your team did them, you could roll them all up to send a client a report of all the things you got done for them that week.

If you wanted to build this workflow in traditional software, you’d spend most of your time on plumbing — defining data schemas, matching field types between systems, writing code to parse one format and convert it to another. The weekly review app needs to read from the daily notes app, which means their data structures have to line up. Add a goals tracker and now three systems need to agree on how they pass information around.

Because AI works with natural language, that integration layer largely disappears. The process of turning seven daily notes into a weekly summary is simply a line in a file that says, “Condense these seven daily notes down into a weekly summary.” The goals audit is just a line that says “compare what got done to what I planned.” [^6]

Each piece took a few minutes to set up because the building blocks were already there and they integrate using natural language. As AI researcher Andrej Karpathy memorably put it: the hottest programming language is now English.

![](https://substackcdn.com/image/fetch/$s_!qEoc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81ce33ee-f04a-4a68-980a-e0a74c818fc8_895x363.png)

We’re still in the early days of figuring out what this looks like. Claude Code uses structures like commands, hooks and skills that are first attempts at the form factor. I don’t know that the current Claude Code form factor is the right or final form that CLI tools will take, but the capability for knowledge workers to use Claude Code for non-technical work is already here, if not widely distributed.

To be sure, there are issues. Unlike software, which is purely deterministic, today’s AI models are probabilistic next-token generators. That means when you tell them to follow a 10-step process, sometimes they just decide to skip step 7. Everyone using AI at scale is running into this issue and building workarounds.

The models also exhibit what AI researcher Ethan Mollick and colleagues call the “jagged frontier:” the observation that AI capability doesn’t map to human intuitions about task difficulty. Models that models that [outperform doctors at medical diagnosis](https://arxiv.org/pdf/2412.10849) still [fail at simple visual puzzles](https://www.nytimes.com/interactive/2025/03/26/business/ai-smarter-human-intelligence-puzzle.html), and systems that [win gold medals in international math competitions](https://simonwillison.net/2025/Jul/19/openai-gold-medal-math-olympiad/) [can't reliably run a vending machine](https://www.anthropic.com/research/project-vend-2) (a topic for a future essay).

It will improve as the underlying models get better, the tooling gets better, and we learn to architect and use these systems. The emerging skill of structuring your workflows and knowledge so you can use Claude Code and AI tools like it effectively is going to be an imporant differentiator in the coming years.

## A Tool for Work

Bush’s vision was to make a tool for thought: a common record of humanity’s knowledge more accessible, better linked, more navigable. LLMs have, to a large extent, become that common record. They’re trained on the bulk of human text, and when you interact with one, you’re navigating a vast associative web of everything humanity has written down.

Claude Code adds two layers on top of that.

First, the personal layer. On top of the societal memex sits your own knowledge base — your projects, your preferences, your history, your way of working. Claude Code helps create, organize, and structure this. It reads your unstructured voice memos and files them where they belong. It watches how you edit its drafts and updates its own notes.[^7]

Second, you can *make things* with that knowledge. Not just retrieve it, not just link it, but produce new forms of knowledge work. Software appears to have been particularly amenable to this tooling because:

1. There is a lot of training data on the internet for what constitutes good software
2. Software is more amenable to tests and evaluations by a computer than other forms of knowledge work.
3. The frontier labs have invested heavily in additional model training to make it good at software development

Having said all that, software is the canary in the coal mine. The labs are going to turn their focus to other forms of knowledge work and I expect rapid progress there this year. The compounding chain of drafting a newsletter or going from workbench notes to weekly reviews are examples of a more general capacity for knowledge work that is only going to improve. How should we, as knowledge workers, think about this?

## Our Freestyle Future

In his book, *Average Is Over*, Tyler Cowen proposed that the future of work would look something like freestyle chess. In freestyle chess, human-machine teams compete against each other. The computer suggests moves; the human decides whether to accept, reject, or explore alternatives. Historically, the best freestyle chess teams weren’t the strongest chess players or the most powerful computers, but the best combination of the two.

In 2005, a team called ZackS won a major freestyle tournament by beating an opponent that included Vladimir Dobrov, a grandmaster. ZackS turned out to be two twenty-something guys in New Hampshire: Zackary Stephen, a database administrator with a statistics degree, and Steven Cramton, a soccer coach and snowboarding instructor. Stephen’s chess rating was 1,381; Cramton’s was 1,685. If Cramton played Dobrov head-to-head, the grandmaster would be expected to win 99% of the time.

But, with machines as partners, the amateurs dominated the experts.

Chess Grandmaster Gary Kasparov put it this way: “A weak human player plus machine plus a better process is superior, not only to a very powerful machine, but most remarkably, to a strong human player plus machine plus an inferior process.”

He also said something revealing: “I exclude myself from this category because I’m not a very good operator. I’m a great chess player. A great operator does not have to be necessarily a very strong player.”

The skill of directing the machine is different from the skill of playing chess.

The amateurs had better intuitive judgment about when to trust the machine, when to override it, and which processes to employ. Being good at freestyle chess isn’t knowing chess (though that’s a component); it’s knowing how to direct the collaboration with the machine.

The people who won freestyle chess tournaments might accept 95% of the machine’s suggestions. The skill is understanding the 5% where you override it — knowing the jagged frontier and when your own judgment should take over.

What he described in chess is now emerging in knowledge work. We are entering an era of *freestyle work.* It’s a human-AI collaboration where the machine proposes and the human disposes. Claude Code suggests an edit; I accept or reject. It drafts a contractor proposal; I revise and send. The skill isn’t domain expertise alone. It’s knowing how to direct the AI, when to push back, and how to structure the collaboration.

This is my first piece of writing where I used Claude Code and I’ll use that as an example of how knowledge work processes might evolve.

AI is incredibly good at certain components of writing: It’s a phenomenal research assistant and copy editor.

It’s a good brainstorming partner for when I’m stuck on something and need to talk through it though I often find it frames things too narrowly.

It is a crappy writer. It doesn’t quite seem to “get” the piece in the same way I do, or what it’s trying to achieve. The wording it uses still sounds like AI slop to me no matter what I put in the skills file.

My writing process conformed to this and looked something like this:

**1\. Voice dump → cleanup (50% AI / 50% human)**

I start by dictating raw thoughts. Rambling, stream of consciousness, whatever comes out. That’s my half. Then AI cleans it up to read smoothly while preserving my exact wording. No rewriting, no AI voice. Just making dictation readable.

**2\. Structural edit (30% AI / 70% human)**

This is the most collaborative phase. The goal is getting the argument and narrative into the right order: what’s the throughline, what sections exist, what goes where.

AI is useful for moving big blocks around in the draft and proposing structures, and as a brainstorming buddy when I’m stuck. Even when it gives bad ideas, having something to react to is faster than staring at a blank page for me.

It tends to converge on too-narrow or too-obvious framings if I don’t push back. This phase requires heavy back-and-forth: I mostly drive here and the AI is doing a lot of copy/pasting type work as well as serving as a sounding board.

**3\. De-AI-ify pass (100% AI / 0% human)**

This is basically a filter for AI voice. It strips out “delve into,” “it’s worth noting,” “landscape,” unnecessary hedging, false enthusiasm, hollow transitions, etc. Some of this residue seemed to creep in during the structural edit.

**4\. Rewrite and research (20% AI / 80% human)**

I rewrite the whole piece in my own voice, section by section. AI is useful for research: finding sources, getting precise numbers, filling factual gaps, etc. It’s also still good as a brainstorming partner when I’m stuck on a section.

The prose and argument are mine and (so far) seem to require very heavy-handed re-writes of what came out of the structural edit.

This phase is iterative and usually takes me 2-3 passes at least. A section might go through several rounds of writing, researching, rewriting. This is probably 70-80% of the time that went into this piece.

**5\. Copy edit (80% AI / 20% human)**

Finally, I do an interactive copy editing pass. AI flags issues one by one (grammar, consistency, clarity, word choice) and I approve or reject. It’s good at catching mechanical issues I’d miss after staring at the same paragraphs for hours. I have final say on anything that touches voice or style.

I suspect this workflow is what a lot of knowledge work is going to start to look like over the next year or two: a human/AI collaboration with each doing the part they have a comparative advantage in. Figuring out where and how to insert AI into your workflows should be a major focus of any knowledge worker right now.

There are real differences between coding and knowledge work worth flagging.

Coding is more amenable to tests and evals than most knowledge work. Even though the models are getting smarter, one big advantage in coding is that the AI can just try stuff over and over and over until it meets some success criteria.

Lots of projects don’t have clear feedback loops. One of the first projects I decided to manage in Claude Code was replacing an HVAC system and ductwork in my (old) house.

Replacing an HVAC system is expensive and you can’t just keep trying stuff and throwing out what doesn’t work in the way you can with software.

A lot of knowledge work shares this: Negotiating a contract, choosing a market to enter, deciding how to restructure a team, picking an investment thesis — these all have feedback loops measured in months or years, not seconds. The more complex the domain and the longer the feedback loop, the more the work depends on judgment that can’t be cheaply verified.

It is naive and lazy to take either extreme of “the real world is messy, AI won’t be able to figure it out.” or “humans will be useless and all the jobs are going away.” The truth is something in the middle.

The frontier of what AI models can do will keep shifting. The job is to shift with it. Historically we’ve talked about this through the lens of prompting, but the more powerful part unlocked by Claude Code is starting to think about how you structure your information and how to work with the models to get things done.

## As We May Work

Eighty years ago, Vannevar Bush looked at the technology of his day — vacuum tubes made by the millions, tossed about in packages — and saw the outlines of what was coming. He imagined a tool that would store all of a person’s knowledge and retrieve it by association rather than alphabetical index. We built pieces of his vision over decades: hyperlinks, search engines, digital notes. The associative retrieval he imagined feels like it finally fully arrived with large language models.

CLI tools like Claude Code push beyond what Bush imagined: from tools for thought to tools for work. This makes this technology wave fundamentally different from the most recent ones in our lifetime.

Mobile and Social were primarily tools for consumption and distribution: you scrolled, shared, and reacted. The defining act was consumptive. CLI tools like Claude Code are productive. They are tools for *making things*. You direct, you judge, you structure, you build. It’s more of a workshop than a megaphone.[^8]

While most of the discussion around AI has been around it accelerating and replacing existing work (which it will), the more interesting and exciting possibility is that it unlocks new forms of making and doing.

When I wrote my book, *The End of Jobs*, I never would have gotten a publishing deal — I had no audience, no credentials, no platform. Self-publishing tools made it worth trying anyway. My expectation was to sell maybe a thousand copies. I ended up selling tens of thousands, which was a delightful surprise and changed my life. The book only exists because the technology made it worth attempting. AI will enable new forms of creative endeavor: art, business models, and products that simply didn’t make economic sense or weren’t possible previously. We shape our tools, then our tools shape us.

---

*Sources:*

- Vannevar Bush, “As We May Think,” The Atlantic Monthly, July 1945 (reprinted in Life Magazine, September 1945)
- Dwarkesh Patel, “Why I don’t think AGI is right around the corner,” June 2025
- Noah Brier, “The Magic of Claude Code,” Alephic, September 2025
- Daniel Miessler, “Building a Personal AI Infrastructure (PAI),” [danielmiessler.com](https://danielmiessler.com/blog/personal-ai-infrastructure)
- Andrew Wilkinson on *AI & I* podcast with Dan Shipper, “Opus 4.5 Changed How Andrew Wilkinson Works and Lives,” Every, January 2026. [every.to](https://every.to/podcast/opus-4-5-changed-how-andrew-wilkinson-works-and-lives)
- Dan Shipper, “How I Use Claude Code to Ship Like a Team of Five,” Every, 2025
- Doug O’Laughlin, “The Death of Software 2.0 (A Better Analogy!),” Fabricated Knowledge, January 2026. [fabricatedknowledge.com](https://www.fabricatedknowledge.com/p/the-death-of-software-20-a-better)

[^1]: I am not claiming that in any meaningful sense, I called AI. I did not know what a LLM was until 2022 like most of the rest of you.

[^2]: Claude Code is probably most accurately referred to as an “agentic CLI tool.” CLI = command line interface and agentic = do things. Essentially, it can do things using the command line on your computer. Because the term is so niche, I’m going to simply refer to Claude Code itself — the equivalent of saying “Windows” rather than “operating system” for clarity. Broadly, the tools in this category include Claude Code (Anthropic), Codex (OpenAI), and OpenCode. I’m sure there will be others and we’ll settle on a term at some point.

[^3]: Though, because they are statistical models rather than deterministic scripts, you will not always get the same response

![](https://substackcdn.com/image/fetch/$s_!i211!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3261d666-a36c-4790-a221-c91d058447d3_981x379.png)

[^4]: Even as context windows expand to hundreds of thousands of tokens, research has shown that LLMs perform best on information near the beginning or end of the window, with significantly degraded performance on information in the middle (Liu et al., “Lost in the Middle,” 2023). A model with a million-token context window may still miss the key detail buried on page 47 of a 200-page document

[^5]: The exact way this happens will likely evolve, the point is just that you can, from your Claude Code interface, interact with all these tools. Many expose APIs, which are just structured ways for programs to read and write data to those services. A standard developed by Anthropic called MCP (Model Context Protocol) lets Claude Code connect to these APIs as tools and there are also more tools offering their own command line interfaces (CLIs).

[^6]: As anyone who has worked with these tools will tell you, you still need a lightweight schema — it’s just informal. If your daily notes drift in format or your file naming gets inconsistent, the summarization breaks down the same way a traditional integration would. However the friction is at least an order of magnitude lower.

[^7]: Really, this too was a part of Bush’s vision - the memex was meant to be a personal tool and not a global one where researchers could make new discoveries, not just traverse everything that was known.

[^8]: There will, of course, be a group of people who decide to hook a megaphone up to the workshop and AI sloppification will continue until morale improves.