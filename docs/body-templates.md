# Body Templates

Этот документ показывает, как должно выглядеть тело итоговых wiki-ready страниц в `guides/`.

Он нужен для двух вещей:

1. чтобы разработчики понимали target shape output;
2. чтобы prompts, processors и verify смотрели на один и тот же формат.

Полный schema contract:

- [docs/wiki-schema-for-guides.md](/Users/khabaroff/GOO_LIBARCH/guides/docs/wiki-schema-for-guides.md:1)

Примеры frontmatter:

- [docs/frontmatter-examples.md](/Users/khabaroff/GOO_LIBARCH/guides/docs/frontmatter-examples.md:1)

---

## 1. `article.md` template

Используется для:

- article
- youtube
- pdf
- note
- telegram-derived content позже

### Recommended structure

```markdown
# {Title}

## Summary
2-4 sentences explaining what the source is about and why it matters.

## Key Ideas
- idea 1
- idea 2
- idea 3

## Details
Main body of the processed material.
Use subsections when needed.

## Code and Commands
Preserve original code blocks, commands, prompts, config snippets, and URLs.

## Entities
- Entity 1
- Entity 2

## Concepts
- Concept 1
- Concept 2

## Related
- [[src-...]]
- [[ref-...]]

## Notes for Review
- Optional note about ambiguity, extraction weakness, or missing context.
```

---

## 2. `article.md` example for article URL

```markdown
# Prompting Best Practices

## Summary
This article explains practical prompt design patterns for LLM applications. It focuses on clearer task framing, output control, and techniques that make model behavior more reliable in production workflows.

## Key Ideas
- Put the most important instructions first.
- Specify the output format explicitly.
- Preserve examples and constraints close to the task.
- Separate role, goal, and input contract.

## Details
The article argues that prompt quality improves when the model receives a clear contract instead of vague conversational framing. It emphasizes that prompts should define the task, expected output shape, and failure conditions early.

The strongest practical recommendation is to make output requirements machine-checkable whenever possible. Instead of asking for “a good summary,” the source suggests naming the fields, sections, or JSON structure that the model must return.

Another recurring theme is prompt stability. Reusable prompts should isolate role, instructions, context, and output rules so they can be reviewed independently and updated without rewriting the full pipeline.

## Code and Commands
```text
Return valid JSON only.
```

```text
Use XML tags to separate instructions from input.
```

## Entities
- Anthropic
- Claude

## Concepts
- few-shot prompting
- structured prompts
- xml tags

## Related
- [[ref-2026-05-11-c3d4e5f6]]

## Notes for Review
- Source uses vendor-specific examples; some recommendations may not transfer equally across models.
```

---

## 3. `article.md` example for YouTube

```markdown
# Building Effective AI Agents

## Summary
This page is based on a video transcript about how agent systems should be designed in practice. It focuses on tool use, planning, context handling, and the tradeoff between flexibility and reliability.

## Key Ideas
- Agents need clear task boundaries.
- Tool use should be explicit and inspectable.
- Context growth becomes a reliability problem.
- Planning and execution should not be conflated blindly.

## Details
The speaker describes agents as operational systems rather than just long prompts. A useful agent is not defined by how much it can say, but by how predictably it can move through a task with tools and intermediate state.

The transcript repeatedly returns to the idea that uncontrolled context accumulation degrades performance. As sessions grow, the system needs summarization, pruning, or decomposition strategies to avoid confusion and token waste.

Another key point is that tool use should stay inspectable. If the system calls external tools, the operator should be able to understand what was called, why, and what came back.

## Code and Commands
```text
tool call -> inspect result -> decide next action
```

## Entities
- OpenAI

## Concepts
- tool calling
- planning
- context management

## Related
- [[ref-2026-05-11-c3d4e5f6]]

## Notes for Review
- Transcript quality may affect fine detail in examples and phrasing.
```

---

## 4. `reference.md` template

Используется для GitHub repo summary/reference.

### Recommended structure

```markdown
# {Repository Name}

## What It Is
1 short paragraph.

## Stack
- language / framework / runtime

## When To Use It
- use case 1
- use case 2

## Key Concepts
- concept 1
- concept 2

## Quick Start
Commands or setup steps when available.

## Caveats
Limitations, maturity concerns, missing docs, operational tradeoffs.

## Related
- [[src-...]]
- [[ref-...]]
```

---

## 5. `reference.md` example for GitHub repo

```markdown
# LangGraph

## What It Is
LangGraph is a framework for building stateful, graph-shaped LLM workflows. It is aimed at agent systems that need explicit steps, branching, retries, and checkpoint-like execution control.

## Stack
- Python
- LangChain ecosystem
- LLM workflow runtime

## When To Use It
- when a simple linear chain is no longer enough
- when an agent needs explicit state transitions
- when workflows require resumability or branching logic

## Key Concepts
- stateful workflows
- graph execution
- checkpoints
- node-based orchestration

## Quick Start
```bash
pip install langgraph
```

## Caveats
This is not the lightest possible abstraction. For very small pipelines, direct SDK calls and plain orchestration code may be simpler and easier to debug.

## Related
- [[src-2026-05-11-a1b2c3d4]]
```

---

## 6. `article.md` example for PDF or noisy extraction

Этот пример показывает, как должен выглядеть body, если материал частично грязный, но не потерян.

```markdown
# 5C Prompt Contracts

## Summary
This document appears to describe a structured framework for writing prompts as explicit contracts. The extraction is partially noisy, but the main framing around clarity, constraints, and reusable prompt structure is still visible.

## Key Ideas
- Prompt structure can be treated as a contract.
- Clear constraints reduce output ambiguity.
- Reusable prompt patterns improve consistency.

## Details
The source argues that prompts work better when they define expectations explicitly instead of relying on conversational intuition. The extracted text suggests a framework where task, context, constraints, and expected output are treated as separate design components.

Some sections of the PDF extraction are degraded, so fine distinctions between framework steps may need manual review. The overall direction is still usable.

## Code and Commands
No high-confidence code blocks were recovered from the extraction.

## Entities
- None identified with confidence

## Concepts
- prompt contracts
- instruction design

## Related
- [[src-2026-05-11-a1b2c3d4]]

## Notes for Review
- PDF extraction quality is weak in several sections.
- Re-run with a better extractor if this source becomes important.
```

---

## 7. Required body rules

These rules should be treated as part of the output contract:

1. Every `article.md` and `reference.md` must start with `# {Title}`.
2. `Summary` is required.
3. `Key Ideas` is required unless the source is too degraded to recover them.
4. `Code and Commands` is required for `article.md`, even if the section says none were confidently recovered.
5. `Entities` and `Concepts` should reflect frontmatter, not contradict it.
6. `Notes for Review` can be omitted only when there is nothing meaningful to flag.
7. The body must stay readable to a human, not just parseable by a machine.

---

## 8. Why this matters

Without a body template, two bad things happen:

1. the prompts drift into inconsistent shapes;
2. the verify layer can only check for shallow presence of files and fields.

With stable body templates:

- prompts have a concrete target;
- processors have a consistent render shape;
- verify can check sections, not just file existence;
- later agents can clean, connect, and rewrite pages more safely.
