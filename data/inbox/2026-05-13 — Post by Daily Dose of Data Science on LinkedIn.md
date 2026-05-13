## 2026-05-13T14:51:51+04:00

https://www.linkedin.com/feed/update/urn:li:activity:7458735024272588800/

The anatomy of a Claude prompt:  
  
(how to go from mediocre to great outputs)  
  
The difference between a mediocre Claude output and a great one almost always comes down to how you structure your prompt. Not the specific words. Just a clear, repeatable structure.  
  
Here's how a well-built Claude prompt breaks down into 8 building blocks, each doing one job:  
  
1\. Role  
  
Tell Claude who it is before telling it what to do.  
"You are a \[ROLE\] with expertise in \[DOMAIN\]. Your tone should be \[TONE\]. Your audience is \[AUDIENCE\]."  
A "senior backend engineer" writes differently than a "technical copywriter," and Claude picks up on that distinction immediately.  
  
2\. Task  
  
State what you want and what success looks like, in the same breath.  
"I need you to \[SPECIFIC TASK\] so that \[SUCCESS CRITERIA\]."  
The "so that" part is what people skip, and it's the part that matters. It gives Claude a way to evaluate its own output.  
  
3\. Context  
  
Wrap supporting material in XML tags like <context> and paste your documents, data, or background inside.  
Put long documents at the top of your prompt and your actual query at the end. Anthropic's testing shows this can improve response quality by up to 30%.  
  
4\. Examples  
  
Provide 3-5 input/output pairs covering normal AND edge cases. Wrap them in <examples> tags so Claude doesn't confuse them with instructions.  
If your example has a quirk you didn't intend, Claude will replicate it. So make sure every example models the behavior you actually want.  
  
5\. Thinking  
  
For anything requiring reasoning or multi-step logic, ask Claude to think before answering.  
"Think through this step by step. Use <thinking> tags for your reasoning. Put only your final answer in <answer> tags."  
This separates messy reasoning from clean output.  
  
6\. Constraints  
  
"Never \[thing to avoid\]. Always \[thing to ensure\]. If you are about to break a rule, stop and tell me."  
That last line is underrated. It turns Claude into a collaborator instead of a blind executor.  
  
7\. Output Format  
  
"Return your response as \[JSON / markdown / table / prose\]. Use this exact structure: \[template\]."  
If you want JSON, show the schema. If you want a table, define the columns. The more specific you are, the less reformatting afterward.  
  
8\. Prefill  
  
API-specific but powerful. Pre-fill the start of Claude's response to skip preamble and lock in the format. No "Sure, I'd be happy to help!" opening, just clean output from the first token.  
  
Here's the thing people get wrong about prompting: they think it's about finding the right words. It's actually about giving Claude the right structure.