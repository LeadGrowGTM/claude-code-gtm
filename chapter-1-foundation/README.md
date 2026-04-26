# Chapter 1 — The Stack Replacement Thesis

**Time:** 15 min | **Chapter goal:** Build the mental model before touching any files.

---

## What You're Building

Nothing yet. This chapter is architecture — understanding the 4-layer system before you wire it up.

```
┌─────────────────────────────┐
│         CLAUDE.md           │  ← Operator brief (loads every session)
├─────────────────────────────┤
│           Rules             │  ← Behavioral constraints
├─────────────────────────────┤
│           Skills            │  ← SOPs that run forever
├─────────────────────────────┤
│           Agents            │  ← Workers you spawn
└─────────────────────────────┘
```

Each layer compounds. Rules make skills predictable. Skills make agents useful. CLAUDE.md makes the whole thing coherent across sessions.

---

## The Stack Decision

What gets replaced:

| Old tool | Replaced by | Reason |
|----------|-------------|--------|
| Zapier / Make | Claude Code workflows | No context window, no memory, no iteration |
| Clay (standard enrichment) | enrich.js + TechSight | Own the pipeline, pay once |
| Manual personalization | cold-email skill | Runs from research, not templates |

What survives:

- **Apollo / data sources** — you still need leads
- **Bison / Smartlead** — sending infra stays
- **Clay for signal-based workflows** — complex enrichment with native integrations

---

## Key Mental Shift

Clay processes one cell at a time. Claude Code processes a company — reads the website, checks job postings, pulls tech stack, synthesizes an ICP fit score — in one pass. The output isn't a row in a spreadsheet. It's a research doc that drives the sequence.

That difference in fidelity is why personalization quality improves, not just speed.

---

## Next Chapter

[Chapter 2 →](../chapter-2-foundation/README.md) — Build your CLAUDE.md operator brief.
