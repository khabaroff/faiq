# ALF Corpus Candidates

## 1. evals-theory/1 — Integrating AI Evals Into Your AI App

- **Path:** /Users/khabaroff/DEV/alf/evals-theory/1 Integrating AI Evals Into Your AI App.md
- **Source type:** article
- **Why useful:** Real article from the ALF evals-theory series — covers practical AI evaluation. Tests article fetch + rewrite pipeline end-to-end.
- **Risk notes:** Filename contains spaces; URL encoding in shell/cmd may need quoting.

## 2. _task/ARCHITECTURE.md

- **Path:** /Users/khabaroff/DEV/alf/_task/ARCHITECTURE.md
- **Source type:** reference
- **Why useful:** Long (626 lines) technical architecture doc with code diagrams, LangGraph workflow, prompt patterns. Good stress-test for chunking and reference output format.
- **Risk notes:** Contains pre-existing frontmatter which may conflict or double-parse.

## 3. pages/wiki/llm.md

- **Path:** /Users/khabaroff/DEV/alf/pages/wiki/llm.md
- **Source type:** note
- **Why useful:** Wiki page with structured frontmatter (tags, provenance, aliases, confidence). Tests how the pipeline handles already-structured wiki content from another system.
- **Risk notes:** Russian/YAML frontmatter; may need non-ASCII handling verification.