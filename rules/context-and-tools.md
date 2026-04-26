# Context & Tools

## Before Any Task

1. **Spawn `smart-searcher` first** — find relevant skills, check if content exists. Always before committing Sonnet/Opus time to discovery work.
2. **Load skills if found** — read full SKILL.md; check for companion scripts in skill's `scripts/` folder
3. **Check MCP docs** if using an integration — `archive/mcp-docs/`
4. **Before creating any file** — check `.claude/rules/file-conventions.md` for routing rules

**Local files first, MCP servers last.** Client history, copy, research → local. Live data, external actions → MCP.

## Skill Locations

| Location | Scope |
|----------|-------|
| `.claude/skills/` | Universal skills for this workspace |
| `~/.claude/skills/` | Global skills available across all projects |
| `[domain]/skills/` | Domain-specific skills (outbound, content, research, data) |

```bash
# Find skills matching a task
bun knowledge-graph/scripts/kg-skill-graph.js --query "your task"
Glob .claude/skills/*/SKILL.md
bun knowledge-graph/scripts/kg-query.js search "topic"
```

## Context Priority (Highest First)

| Priority | Source | When to Load |
|----------|--------|-------------|
| P0 | `archive/campaigns/[client]/` — proven copy, conversion data | Always for campaign writing |
| P1 | `company/` — ICP, voice, messaging | Always for outbound content |
| P2 | Client `research/` — ICP research, market analysis | New copy or new market |
| P3 | Client `_master.md` — client overview, active campaigns | Start of any client work |
| P4 | `.claude/skills/` — SOPs, workflows | Load via skill execution |
| P5 | `archive/battlecards/` — competitor intel | Competitive positioning only |

**When results (P0) contradict research (P2), results win.**

## Workspace Context Tools

| Tool | What It Answers | Command |
|------|----------------|---------|
| **Knowledge Graph** | "Where is X? What relates to it?" | `bun knowledge-graph/scripts/kg-query.js search "topic"` |
| **smart-searcher agent** | "Does this file/skill exist?" | Spawn via Agent tool |

Use KG for finding skills, docs, and entity relationships.
Use smart-searcher for quick file existence checks and context loading.

## Tool Hierarchy

1. **Script** in `scripts/` or skill's `scripts/` — check first
2. **MCP server** — check `archive/mcp-docs/` for usage guide
3. **Manual** — only when no tool exists

When a tool breaks: fix the tool, update the skill with the learning. Never work around it.

**Tool placement:**
- Skill-specific → `skills/[skill]/scripts/`
- Reusable → `tools/`
- Shared utilities → `tools/shared-scripts/`

## Prompt Order (Cache Efficiency)

Static context (skills, voice, ICP, reference docs) always loads before dynamic inputs (user request, variable data). This preserves the cached prefix across repeated calls.
