# Chapter 4 — Agents: Headcount Leverage

**Time:** 25 min | **Chapter goal:** Understand when to spawn agents and wire up the smart-searcher.

---

## What You're Building

One agent to start: [`smart-searcher`](./agents/smart-searcher.md) — the discovery agent that finds relevant skills and context before burning Sonnet/Opus time.

---

## What an Agent Is

An agent is a subagent with a specific role, tool access, and model. You spawn it with a task; it runs independently and returns a result.

The key insight: agents preserve main context. The main session stays clean. The agent does the expensive reading, the main session gets a 200-token summary.

```
Wrong:  Main reads 10 files → understands → edits → reports  (burns 2000+ tokens)
Right:  Main spawns agent → agent reads/edits → Main gets summary (200 tokens)
```

---

## Agent Roster

| Agent | Model | Use For |
|-------|-------|---------|
| `smart-searcher` | Haiku | Discovery, file search — always first |
| `lg-researcher` | Sonnet | Company research, synthesis |
| `task-orchestrator` | Sonnet | Route complex multi-step tasks |

Start with `smart-searcher` only. Add `lg-researcher` when you're doing regular company research. Add `task-orchestrator` when your tasks span 5+ files.

---

## The smart-searcher Pattern

Before any task that involves finding context — existing copy, a skill, a client file — spawn smart-searcher first.

```
Main: "Research StackBridge.io for ICP fit"
 ↓
Main spawns smart-searcher: "Find ICP research skill and any existing StackBridge files"
 ↓
smart-searcher returns: skill path + no existing files
 ↓
Main spawns lg-researcher with correct skill loaded
```

This pattern stops you from rewriting research that already exists and ensures the right skill gets loaded before any work starts.

---

## When to Use Agents

| Task | Use Agent? |
|------|-----------|
| Research a company (10+ files) | Yes |
| Follow a plan phase | Yes |
| New skill with examples | Yes |
| Single-line config change | No |
| Quick rename | No |

---

## End State

```
your-workspace/
├── CLAUDE.md
└── .claude/
    ├── rules/
    ├── skills/
    └── agents/
        └── smart-searcher.md
```

---

## Next Chapter

[Chapter 5 →](../chapter-5-waterfall/README.md) — The enrichment waterfall that replaced most of our Clay spend.
