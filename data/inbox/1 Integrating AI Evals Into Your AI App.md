## 2026-04-19T21:18:05+04:00

https://www.decodingai.com/p/integrating-ai-evals-into-your-ai-app

### The holistic guide: From optimization to production monitoring

*Welcome to the **[AI Evals & Observability series](https://www.decodingai.com/t/ai-evals-and-observability)**: A 7-part journey from shipping AI apps to systematically improving them. Made by busy people. For busy people.*

🧐 Everyone says you need AI evals. Few explain how to actually build them and answer questions such as…

How do we avoid creating evals that waste our time and resources? How do we build datasets and design evaluators that matter? How do we adapt them for RAG?...and most importantly, how do we stop “vibe checking” and leverage evals to actually track and optimize our app?

*This 7-article series breaks it all down from first principles:*

1. **Integrating AI Evals Into Your AI App** ← *You are here*
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

By the end, you’ll know how to integrate AI evals that actually track and improve the performance of your AI product. No vibe checking required!

**Let’s get started.**

---

Understanding where AI Evals and Observability fit into the broader scheme of things can be daunting. It certainly was for me. At first, it was confusing because you can use AI evals in so many places within your application. Also, everyone seemed to have a different definition.

But it does not have to be that complicated. With this article, we want to finally connect the dots on where AI Evals fit in your AI app holistically.

But first, let’s understand WHY AI Evals are so essential.

A few months ago, I had to completely rewrite **Brown**, a writer agent I built as one of the capstone projects for my [Agentic AI Engineering course](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31). The first version worked but was slow and expensive. So, I redesigned the architecture from scratch.

Immediately, I hit a wall. How do I know this new version is at least as good as the old one? I had spent months fine-tuning the original and could not afford to lose that progress silently.

That is when AI evals saved me. I wrote evaluators that scored the agent on dimensions tied to our actual business requirements. With those evals, every code change generated a clear signal indicating whether I was on track. Without them, the rewrite would have been a coin flip.

You likely shipped the first version of your app. You got this far by *“vibe checking”* if the app works fine. Up to this point, everything is fine.

However, once you start adding new features, you realize old features break. Once you start having real users, they interact with the app in unexpected ways. If you have only 10 users, vibe checking works.

But as this scales, you get overwhelmed. You try to improve current features, and it is incredibly hard to tell if your changes have any effect. Manually managing all of this is a living hell.

💡 *The solution is a structured way of measuring how well your app performs. This is known as AI Evals.*

**In this article, we will cover:**

1. A holistic view of the AI Evals lifecycle.
2. How to use evals for optimization during development.
3. How to use evals for regression testing in CI pipelines.
4. How to monitor production quality using sampling.
5. Common misconceptions regarding guardrails and benchmarks.
6. The recommended tech stack for implementing this system.

![](https://substackcdn.com/image/fetch/$s_!Y_0d!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e3e3f14-390a-4fcf-b449-d41b3e050fd8_1200x1075.png)

Image 1: The holistic view of AI Evals within the AI application development lifecycle.

*Before digging into the article, a quick word from our sponsor, Opik.* ↓

---

## Opik: Open-Source Observability for Your Multimodal AI Agents (Sponsored)

This ***AI Evals & Observability series*** is brought to you by ***[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)***, the LLMOps open-source platform used by Uber, Netflix, Etsy, and more.

We’re proud to partner with a tool we actually use daily across our open-source courses and real-world AI products. Why? *Because it makes evaluating multimodal AI apps as easy as evaluating text ones.*

![](https://substackcdn.com/image/fetch/$s_!DvE9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc89e180b-7253-4edd-91d3-5ef78afccff7_3020x1516.png)

Monitoring traces that contain generated videos, such as when using OpenAI Sora. Learn more about monitoring multimodal traces with Opik or about hooking Opik to OpenAI Sora.

*AI apps are no longer just text-in, text-out.* They process images, generate videos, parse PDFs, and more. Monitoring and evaluating all of that used to be painful. With Opik, it’s not. Here is why we love it:

- **Trace everything** — Opik renders images, videos and PDFs directly inside your traces. No more guessing what your model actually saw or generated. We use this daily, and it changed how we debug multimodal pipelines.
- **Zero-friction multimodal evals** — Add image URLs or upload files directly in the UI, then run LLM-as-a-Judge evaluations on them. Opik auto-detects vision-capable models (GPT-4o, Claude 3+, Gemini) and warns you if the model doesn’t support vision.
- **Video generation? Traced automatically** — Wrap your OpenAI client in one line, and Opik tracks the full Sora workflow: creation, polling, download, and logs the generated video as an attachment. Full visibility, minimal setup. [Guide here](https://www.comet.com/docs/opik/integrations/openai#video-generation-sora?utm_source=newsletter&utm_medium=partner&utm_campaign=paul).

[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) is fully open-source and works with custom code or most AI frameworks. You can also use the managed version for free (with 25K spans/month on their generous free tier). *Learn more about evaluating multimodal traces:*

↓ *Now, let’s move back to the article.*

---

## The Holistic View of AI Evals

At their heart, AI Evals are systematic data analytics on your LLM application. You look at the data flowing through your app, create metrics for what matters, and use those metrics to measure what is happening. This allows you to iterate, experiment, and improve with confidence rather than guess [\[1\]](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [\[2\]](https://hamel.dev/blog/posts/evals-faq/).

Without evals, every prompt change is a coin flip. With them, you have a concrete feedback signal to iterate against [\[3\]](https://youtube.com/watch?v=BsWxPI9UM4c&si=Zn5CgOvM_uqtTrF6).

In this article, we will focus on the *where*, *when*, *why*, and *what*. In future articles from the series, we will focus on the *how*. There are ***three core scenarios** where AI Evals play a central role*:

1. **Optimization:** During development, we use evals to measure and optimize current or new features.
2. **Regression:** During development, when changing the code, we use evals to ensure our changes do not break previous features. This is conceptually similar to classic software tests.
3. **Production Monitoring:** In production, we use evals to detect potential performance issues caused by unexpected user behavior or drift.

Beyond these three, two complementary signals round out the picture. We touch on them briefly later, but they are not the focus of this article:

1. **User Feedback:** These are direct signals from users that bypass all our predefined datasets and evaluation strategies. They are the most valuable signal you can get.
2. **A/B Testing:** This ensures new code changes perform as expected, tested on real user behavior rather than predefined datasets.

This is illustrated in Image 1, which maps these concepts to the development lifecycle.

![](https://substackcdn.com/image/fetch/$s_!Y_0d!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e3e3f14-390a-4fcf-b449-d41b3e050fd8_1200x1075.png)

Image 1: The holistic view of AI Evals within the AI application development lifecycle.

Now that we have the big picture, let’s dig deeper into each of the three core scenarios, starting with optimization.

## Using Evals for Optimization

The first major use case for AI Evals is optimizing your application on a specific feature during development.

To keep costs under control and run tests multiple times during development, we run the AI evals only on a *subset* of the dataset that targets the feature we want to optimize. This is usually triggered manually by the developer while testing new code.

![](https://substackcdn.com/image/fetch/$s_!ChCe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7176d199-2fb7-484d-9590-a07e1a631dc7_1200x773.gif)

Image 2: Evaluate one feature at a time during optimization.

This makes development guided by concrete numbers that can be measured against a baseline, rather than just vibe-checking.

Suppose you have a customer support bot and you want to improve how it handles refund requests. You do not run your evals on the entire dataset, which may also cover shipping questions, account issues, and technical support. Instead, you filter your evals dataset down to just the refund-related examples and iterate on that subset.

You tweak the prompt, run the evals, check if your “refund accuracy” metric improved compared to the baseline, tweak again, and repeat. This keeps each cycle fast and cheap, so you can iterate multiple times in a single session [\[4\]](https://www.oreilly.com/radar/evals-are-not-all-you-need/).

![](https://substackcdn.com/image/fetch/$s_!GmAN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcba3b70-a65a-4fca-9b71-d656112e2376_1200x1047.png)

Image 3: A flowchart detailing the iterative process of using AI Evals for optimization during development.

But what happens when your optimization work accidentally breaks something that was already working? That is where regression testing comes in.

## Using Evals for Regression

Regression testing is used to catch potential errors introduced by your new changes before they reach production. Unlike optimization, which focuses on a subset, regression testing runs on the **whole evaluation dataset**.

This typically happens within the CI pipeline. Because running AI Evals on the entire dataset is costly (some evaluators rely on LLM calls to grade outputs), we try to avoid running them on every single commit, as we do with standard software tests. A common approach is to run this suite when you think you are “done” with your feature, right before merging the feature branch, to ensure you are not introducing new bugs.

![](https://substackcdn.com/image/fetch/$s_!giir!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0ebc005-6ff0-4d5d-97bf-98602b1a1bd1_1200x796.png)

Image 4: Evaluate all the features when computing regression scores.

Continuing the customer support bot example: after you optimized refund handling during the optimization phase, you now want to merge your changes. Before merging, your CI pipeline runs the full eval suite. This includes refunds, shipping questions, account issues, and escalation scenarios.

This catches regressions. Maybe your prompt change for refunds accidentally made the bot worse at routing shipping complaints to the right team. If any metric drops below the baseline threshold, the pipeline fails and blocks the merge until you fix it. This is similar to how Anthropic’s Claude Code team and Bolt’s AI team run separate eval suites for quality benchmarking and regression testing on each change [\[1\]](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

![](https://substackcdn.com/image/fetch/$s_!20y0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb7c58f2-f6eb-400c-958a-a36da6161c5a_1200x1019.png)

Image 5: A flowchart illustrating how AI Evals are used for regression testing within the CI pipeline, emphasizing an automated, pre-merge process on the entire dataset.

Optimization and regression testing happen during development, but what about after you deploy? Let’s look at how AI Evals work in production.

## Using Evals for Production Monitoring

Production monitoring is similar to regression testing, but instead of running it offline on your AI Evals dataset, we aim to catch issues in the production environment using live traces tracked by your LLMOps platform. The final scope is to identify potential pitfalls in our system and generate alarms or warnings.

To keep costs under control, we apply smart live sampling techniques within your LLMOps platform (e.g., [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)). You rarely want to evaluate 100% of production traffic with an LLM judge. Instead, you use:

- **Random sampling:** Evaluate a fixed percentage of all traces (e.g., 5-10%) to get an unbiased baseline of overall quality.
- **Stratified sampling:** Divide traces into meaningful subgroups (by feature, user segment, query type) and sample from each proportionally, ensuring no critical category is overlooked.
- **Signal-based sampling:** Prioritize traces that show suspicious signals. These include long exchanges, repeated questions, user frustration indicators (thumbs-down, drop-offs from your user feedback pipe), low confidence scores, or anomalous latency/cost spikes. These are the highest-value traces to review.

You should run these as soon as practical. This can be near real-time or on a batch schedule (e.g., nightly), depending on risk tolerance and cost.

Suppose your customer support bot is live with thousands of conversations per day. Even with a 95% success rate, that still amounts to dozens of failures daily. That is far too many to review manually. Your LLMOps platform samples a percentage of live traces and automatically runs evaluators on them. For instance, you might check if the bot hallucinated a return policy that does not exist or if it escalated appropriately when the user was frustrated.

These evaluators flag problematic traces and feed dashboards that track failure rates over time. When you see a spike, you catch it within hours instead of waiting for user complaints to pile up. Perhaps a new product launch causes questions the bot wasn’t trained on [\[5\]](https://humanloop.com/blog/why-your-product-needs-evals).

![](https://substackcdn.com/image/fetch/$s_!h8bx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ac7959f-6130-4759-af62-8917c3437323_1200x918.png)

Image 6: A flowchart depicting the process of AI Evals for production monitoring on live traffic.

Beyond evaluators, you have two complementary signals. **User Feedback** (thumbs-up/down, comments) is the most valuable quality signal because it reflects real satisfaction, not proxy metrics. **A/B Testing** validates that improvements measured offline actually hold up under real user behavior by routing traffic to different variants.

Now that we understand where and when to run AI Evals, let’s clear up some common misconceptions that trip up most teams.

## Looking at Common Misconceptions

There are three major areas where terminology gets confusing: guardrails, benchmarks, and software tests.

### Guardrails vs. Evaluators

Guardrails run on the inputs and outputs of the LLM or other components of your AI app. These should be very fast to avoid adding extra latency. Their role is to flag inputs/outputs as valid or not, or mask sensitive data. Evaluators, on the other hand, are used to compute metrics on your AI app components.

While you can use evaluators as guardrails if they detect adherence to business outcomes, this is the exception, not the rule. Evaluators are usually designed for accuracy rather than low latency.

For example, a **guardrail** in your customer support bot checks every user message in real time. If the user pastes a credit card number, the guardrail masks it instantly. On the output side, another guardrail blocks any response that promises a refund above a certain threshold. These must run in milliseconds.

An **evaluator** runs after the fact (or offline on sampled traces). It measures whether the bot’s refund responses are actually accurate, helpful, and aligned with company policy. The evaluator can take seconds or even minutes per trace because it is not in the user’s critical path.

### App Evaluators vs. LLM Evaluators

**App Evaluators** measure your whole app as a unit (LLM calls + everything around them). They focus on ensuring the performance of your business use case.

**LLM Evaluators** measure only the performance of the LLM itself, rarely considering your business use case. Popular benchmarks like the LLM arena evaluate only the LLM in isolation. That is why benchmarks are deceiving and should never be your only criterion when picking an LLM. They are often a marketing strategy for foundational model companies.

Examples like Chatbot Arena (LMSYS) or MMLU tell you which LLM is “generally smarter.” But they say nothing about whether that LLM will handle your specific refund policy correctly, escalate frustrated users at the right moment, or respect your company’s tone of voice. You need app-level evaluators grounded in your business use case, not generic benchmark scores [\[4\]](https://www.oreilly.com/radar/evals-are-not-all-you-need/).

### Evaluator vs. Classic Software Tests

When running evaluators as regression tests, they are conceptually similar to classic software tests. Their purpose is to ensure everything still works after you change the code. However, the implementation is vastly different.

Classic software tests are deterministic. For a given state of the database and a given input, you almost always get the same output. It is also much cheaper and easier to run because the code itself is cheap to run, and the outputs are structured and easy to validate.

AI Evaluators must assess the quality of LLM calls operating in a non-deterministic environment, often with unstructured data. Instead of writing unit and integration test cases, AI evals cases are operated as eval datasets, reflecting the AI-centric approach.

With a clear mental model of what AI Evals are and aren’t, let’s look at the tools you need to put this into practice.

## So What Is the Tech Stack?

To run AI Evals effectively, you need two core tool families: an annotation tool and an LLMOps platform.

First, **should you build a custom annotation tool or use an off-the-shelf tool?** Since your data is always custom, we recommend building the annotation tool from scratch. With current AI coding tools such as Claude Code, Cursor, or Lovable, doing this is extremely easy. You want to make annotation effortless, adding zero resistance to how your data is displayed. As your data is custom, no pre-defined tool can do that perfectly for you. Most LLMOps platforms will have a feature around this, but a custom lightweight tool often wins on speed and usability.

Second, you need an **LLMOps platform**. Our favorite vendor is **[Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul)**. It is what we recommend and use in all our products. It is open source, constantly updated with new features, works out of the box with popular LLM APIs and AI Frameworks, and offers a generous freemium plan.

![](https://substackcdn.com/image/fetch/$s_!ulUk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe694c3e3-3ada-4393-99c6-bbc515ec4041_2984x1841.png)

Image 7: Tracking multimodal traces with Opik.

Other strong options include **LangSmith**, which is best for the LangChain ecosystem, and **LangFuse**, another solid open-source alternative. We have also heard good things about Braintrust and Arize.

The reality is that most of the time, you should pick the best tool for your current setup. We use Opik, but most of these tools have overlapping features. Choose the one that best fits your ecosystem and connections.

## Next Steps

AI Evals are not optional. They are a structured, repeatable way to ensure your AI app actually works, both during development and in production.

Now that we understand the *where*, *when*, *why*, and *what* of AI Evals, the [next article](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis) will focus on the *how*. Specifically, we will dive into how to gradually build an evals dataset.

Also, remember that this article is part of a **[7-piece series on AI Evals & Observability](https://www.decodingai.com/t/ai-evals-and-observability)**. **Here is what’s ahead:**

1. **Integrating AI Evals Into Your AI App** ← *You just finished this one*
2. [Build an AI Evals Dataset from Scratch](https://www.decodingai.com/p/build-an-ai-evals-dataset-with-error-analysis)
3. [Generate Synthetic Datasets for AI Evals](https://www.decodingai.com/p/generate-synthetic-datasets-for-ai-evals)
4. [How to Design Evaluators](https://www.decodingai.com/p/how-to-design-ai-evaluators-that-catch-failures)
5. [How to Evaluate the Evaluator](https://www.decodingai.com/p/how-to-evaluate-the-evaluator-validate-llm-judge)
6. [RAG Evaluation: The Only 6 Metrics You Need](https://www.decodingai.com/p/rag-evaluation-6-metrics-framework)
7. [Lessons from 6 Months of Evals on a Production AI Companion](https://www.decodingai.com/p/behind-the-scenes-of-ai-observability)

See you next Tuesday.

[Paul Iusztin](https://www.pauliusztin.ai/)

---

*What’s your opinion? Do you agree, disagree, or is there something I missed?*

---

*Enjoyed the article? The most sincere compliment is to share our work.*

---

## Go Deeper

**Go from zero to production-grade AI agents** with the [Agentic AI Engineering self-paced course](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31). Built in partnership with [Towards AI](https://academy.towardsai.net/courses/agent-engineering?ref=b3ab31).

Across **34 lessons** (articles, videos, and a lot of code), you’ll design, build, evaluate, and deploy production-grade AI agents end to end. By the final lesson, you’ll have **built a multi-agent system** and a **capstone project** where you apply everything you’ve learned on your own.

*Three portfolio projects and a certificate to showcase in interviews. Plus a Discord community where you have direct access to other industry experts and me.*

Rated 4.9/5 ⭐️ by 290+ early students — *“Every AI Engineer needs a course like this.”*

*Not ready to commit?* We also prepared a free 6-day email course to reveal the ***6 critical mistakes that silently destroy agentic systems.** [Get the free email course.](https://email-course.towardsai.net/?ref=b3ab31)*

---

*Thanks again to [Opik](https://www.comet.com/site/?utm_source=newsletter&utm_medium=partner&utm_campaign=paul) for sponsoring the series and keeping it free!*

![Opik Banner](https://substackcdn.com/image/fetch/$s_!oSDm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26c21863-4ee6-4026-91c7-74650eb16dac_3168x792.png)

Try Opik for free here (25k spans/month free)

**If you want to monitor, evaluate and optimize your AI workflows and agents:**

---

## References

1. Anthropic. (n.d.). Demystifying evals for AI agents. Anthropic. [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
2. Husain, H. (n.d.). LLM Evals: Everything You Need to Know (Evals FAQ). Hamel’s Blog. [https://hamel.dev/blog/posts/evals-faq/](https://hamel.dev/blog/posts/evals-faq/)
3. Lenny’s Podcast. (n.d.). Why AI evals are the hottest new skill for product builders | Hamel Husain & Shreya Shankar. YouTube. [link](https://www.youtube.com/watch?v=BsWxPI9UM4c)
4. Reganti, A. N., & Badam, K. (2025, January 28). Evals Are NOT All You Need. O’Reilly. [https://www.oreilly.com/radar/evals-are-not-all-you-need/](https://www.oreilly.com/radar/evals-are-not-all-you-need/)
5. Habib, R. (2024, March 14). Why Your AI Product Needs Evals with Hamel Husain. Humanloop Blog. [https://humanloop.com/blog/why-your-product-needs-evals](https://humanloop.com/blog/why-your-product-needs-evals)

---

## Images

If not otherwise stated, all images are created by the author.