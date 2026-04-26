# Chapter 2 — Foundation: CLAUDE.md as an Operator Brief

**Time:** 20 min | **Chapter goal:** Write the CLAUDE.md that makes every session coherent.

---

## What You're Building

Your `CLAUDE.md` — the single file that loads at the start of every Claude Code session. It's not documentation. It's a standing brief.

Rules in this folder: [`rules/`](./rules/) — the 7 behavioral constraints that go alongside it.

---

## Start Here

```bash
cp ../CLAUDE.md.template your-workspace/CLAUDE.md
```

Then customize the five sections:

### 1. Identity
Who Claude is in this context. Set the operating persona and name the failure modes you want to prevent.

```markdown
## Identity — Who You Are

You're not an assistant. You're [NAME]'s operator.

Your purpose: run outbound GTM for B2B SaaS clients.

Core behaviors:
- Lead with the answer. No filler.
- Read the file before asking. Come back with answers.
- Never hallucinate. If you don't know, say so.
- Default to action. Only ask when scope is genuinely ambiguous.
```

### 2. Workflow Style
One paragraph. How to handle multi-step tasks without constant confirmation requests.

### 3. Repos
A table mapping every directory to its purpose. Claude reads this to know where things live.

### 4. Work Routing
Where different types of work go. Campaign copy → `campaigns/`. Client research → `clients/`. Never leave this ambiguous.

### 5. Skill Discovery
How Claude finds its tools. Without this, it improvises instead of using the skills you've built.

```markdown
## Skill Discovery
Glob .claude/skills/*/SKILL.md
Grep "cold email" glob="**/skills/*/SKILL.md"
```

---

## The Rules

The 7 rules in `rules/` constrain behavior so you get predictable output:

| File | What it prevents |
|------|-----------------|
| `archive-safety.md` | Accidental deletes on client files |
| `ask-vs-act.md` | Constant confirmation requests |
| `context-and-tools.md` | Improvising when a skill exists |
| `file-conventions.md` | Files landing in wrong locations |
| `prompt-library.md` | Rebuilding prompts that already exist |
| `scope-before-execute.md` | Wrong-branch or wrong-client mistakes |
| `workflow.md` | Half-finished implementations |

You don't need all seven on day one. Start with `ask-vs-act.md` and `scope-before-execute.md`. Add the rest as you hit the problems they solve.

---

## End State

```
your-workspace/
├── CLAUDE.md           ← filled in, specific to your operation
└── .claude/
    └── rules/          ← at least ask-vs-act.md + scope-before-execute.md
```

---

## Next Chapter

[Chapter 3 →](../chapter-3-skills/README.md) — Build your first skills.
