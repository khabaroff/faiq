## 2026-05-13T13:09:18+04:00

https://edatweets.substack.com/p/a-beginners-guide-to-claude-code

It's a snowy weekend in NYC (and half the East Coast, apparently). I successfully failed at going out for brunch, and after downgrading my HBO subscription (3 episodes into a series and 15 ads later) I decided that playing with Claude Code would be the most fun I can have on a snowy day (non-ironic).

**[Claude Code](https://code.claude.com/docs/en/overview) is Anthropic's tool that runs in your terminal and writes code for you**. While I do have a CS background, I haven’t coded in a while and always hated frontend work. So this is a good way to test what I can build.

![](https://substackcdn.com/image/fetch/$s_!L9QK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a1c35ca-c32c-457a-94fa-c80886f520e7_2076x1126.png)

*📧 PS: This post is too long for email, so you'll be getting a not-so-ideal user experience if you received this via email. I apologize in advance. It was supposed to be an email, but then I added screenshots. And then more screenshots.*

---

## Ok - but first, why should you care?

- If there’s ever a perfect time to learn this stuff, it’s now. Being early to new tech is the biggest advantage you can have.
- I’ve been using Claude Code at work and it’s genuinely helping me a lot. I built workflows that pull updates from different apps so I don’t have to check them one by one.
- If I can build a full-on app in a few hours without touching the code, you can too.

---

## Building a Packing List App (With Zero Lines of Code)

I have a company offsite in Costa Rica in 2 weeks. So for the purpose of this snowstorm vibe coding session, I’ll be building a packing list generator app.

### Part 1: Setup

First and foremost, Claude Code runs in your terminal. On Mac, just search "Terminal." On Windows, search "Command Prompt" or "PowerShell." I know it gives Mr. Robot vibes if you're not used to it, but I promise it's not that deep. You'll just be using it to have a chat with Claude.

#### 1: Download Claude Code

Head over to the [setup page](https://code.claude.com/docs/en/setup) to install Claude Code.

[To use Claude Code](https://code.claude.com/docs/en/setup#authentication), you need one of the following:

- **Claude Pro subscription** ($20/month)
- **Claude Max subscription** ($100/month or $200/month)
- **Anthropic API credits**

#### 2: Create a Project Folder

This is where all your project files will live. Open your terminal and type:

```markup
mkdir packing-list-app
cd packing-list-app
```

The first command creates the folder called `packing-list-app`, the second one opens it.

*(*`mkdir` *\= "make directory" which creates a folder.* `cd` *\= "change directory" which goes into that folder.)*

#### 3: Start Claude Code

In your terminal (while inside your project folder), type:

```markup
claude
```

This opens Claude Code in your project folder, when prompted, give access to the folder.

![](https://substackcdn.com/image/fetch/$s_!bPMS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F862c9292-e67a-40f5-a633-22dab1ff460f_1494x278.png)

You’re now ready!

### Part 2: Building the App (With Zero Lines of Code)

You'll be doing everything inside the terminal from now on. If you close your terminal, no worries — just open it again, use `cd` to navigate to your project folder, and type `claude` to enter Claude Code.

#### Step 1: Write a Clear Description

When you start Claude Code, you need to tell it what you want. **Be SUPER specific**.

In our case, the **Packing List Generator** will be a simple app that creates a packing checklist based on your trip details (destination, dates, activities).

**❌ Too vague (don’t do this):**

> “Make a packing list app.”

**✅ Better (do this instead):**

> “Make an app for a packing list generator. I want to input the destination, number of days, and what activities I’m doing (like beach, surfing, nice dinners). It should give me back a packing checklist with checkboxes so I can check off items I’ve packed. It should take into account the location and the weather during my travel dates. **”**

#### Step 2: Enter Plan Mode

Claude has a feature called [plan mode](https://code.claude.com/docs/en/common-workflows#use-plan-mode-for-safe-code-analysis), where it asks you questions and creates a plan before building anything. This allows you to clarify technical requirements, design preferences, or anything else before a single line of code is written.

**Let’s tell Claude our project and then enter Plan Mode:**

1. Type your description (from above).
2. **Press Shift+Tab twice to enter plan mode.**
3. Press **Enter**.
4. Answer the questions from this plan mode.

![](https://substackcdn.com/image/fetch/$s_!WvEL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6f1806d-90cd-41fa-b0a6-bcb749d984b9_1516x228.png)

It will keep asking questions until it has all the information it needs.

![](https://substackcdn.com/image/fetch/$s_!0gLr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7092076e-6583-4d00-8d96-cf9583d70c24_1292x328.png)

In Plan Mode, Claude will never write code automatically. It always asks first. It’s like you’re talking with a teammate here.

![](https://substackcdn.com/image/fetch/$s_!xjt4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F134411f0-cd3b-4521-895f-1e81783e8acc_1380x170.png)

After you’ve answered all the questions, Claude will create an implementation plan. **Read through the plan carefully.** If something doesn’t look right, tell Claude.

![](https://substackcdn.com/image/fetch/$s_!db6y!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F613198a7-19b5-493a-9486-6cb622fd4aba_1956x388.png)

#### Step 3: Let Claude Build

Once you’re ok with the plan, tell Claude to go ahead. Claude will now write the code, create files, and build your app. You can watch as it works.

![](https://substackcdn.com/image/fetch/$s_!q9h8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6a5c100-11c5-475c-8b8e-818f610f601d_1902x660.png)

#### Step 4: Test Your App

After Claude has written all the code, it might ask you to install any dependencies that are needed, and then tell you how to run the app.

![](https://substackcdn.com/image/fetch/$s_!DQWB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38912016-8c05-48ec-a101-b20446805288_1210x316.png)

Follow the instructions and head over to your app.

![](https://substackcdn.com/image/fetch/$s_!wThX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6d72c4c-97a2-4857-b208-2b18b0c97cb4_1726x1104.png)

Ok wow- here’s what Claude created:

![](https://substackcdn.com/image/fetch/$s_!2Ryv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c0a8c61-55fe-447b-9f84-22797b7f6072_1466x1102.png)

#### Step 5: Make changes (it’s not perfect)

After playing around with the app, I noticed some errors.

**Error1:** The weather API it used wasn’t fetching the data for the dates I wanted, apparently it only fetches for 16 days in advance. Claude added a fallback to a historical data API.

![](https://substackcdn.com/image/fetch/$s_!xDze!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad4c37e5-d53d-41e9-8406-28e16a32012b_1332x116.png)

![](https://substackcdn.com/image/fetch/$s_!sLdb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11ea9dbb-f913-4ec0-a260-161990a8dfee_1422x176.png)

Now, based on my dates, I have a full checklist!

![](https://substackcdn.com/image/fetch/$s_!VV-C!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2299d3ce-b5f2-4e3a-840b-b52eb8c6a049_1342x1150.png)

**Error2:** It made an error with the day calculation. While the date I put was 7 days, it showed as 2 days.

(I also asked Claude to add some emojis in this same message).

![](https://substackcdn.com/image/fetch/$s_!HjzP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb62cf9a9-4b92-45f7-bee1-517aca5d8624_1354x1036.png)

This is looking much prettier now and the days are calculated correctly.

**Error3:** It thinks I will bring 3 sunscreens? (I think this counts as an error 😋). While I do wear sunscreen every day, I will not be taking 3 sunscreens. So I told Claude to make the list more concise, and have an optional section for non-essentials.

![](https://substackcdn.com/image/fetch/$s_!N02b!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6fc313d-23e7-4532-87e0-f035ad71dc3f_1240x286.png)

#### Step 6: Ship it! 🚀

After playing around a bunch here is what I have now:

- dark mode
- extendable packing list (can click as a dropdown)
- the list is saved locally, so doesn’t go away when i refresh the page
- logo and new name
- footer
- UI updates

Here's the final result (the one you saw at the top):

![](https://substackcdn.com/image/fetch/$s_!n8Em!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad582377-8988-4544-b69d-a483c15afbfa_1724x1376.png)

Pretty happy with the optional items:

![](https://substackcdn.com/image/fetch/$s_!l-Gz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fa7e020-81c8-4113-95ca-4d835558177a_1246x806.png)

Claude also created a github repo and pushed the project, view it on my [GitHub](https://github.com/edakturk14/packing-list-app).

---

## End

**I went from a blank folder to a deployed app without writing a single line of code.** Not bad for a snow day. It took me around 1 hour to get something working, and then I spent 2-3 hours styling and playing around.

Important notes:

- **Be VERY specific.** The more detail, the better the results.
- **Use Plan Mode.** It forces you to think before building.
- **Ask questions.** Claude can explain anything it does or walkthrough the options before doing so.
- **Claude makes mistakes too.** What is perfect anyway?