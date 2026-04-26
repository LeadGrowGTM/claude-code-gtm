# Workflow & Execution

## Task Execution

**Plan mode** for ANY non-trivial task (3+ steps or architectural decisions). If something goes sideways mid-task, STOP and re-plan — don't keep pushing.

**Core principles:**

- **Simplicity first** — make every change as simple as possible; minimal code impact. If you write 200 lines and it could be 50, rewrite it before moving on.
- **Root causes only** — no temporary fixes, no workarounds; find and fix the actual problem
- **Surgical changes** — every changed line must trace directly to the user's request. Match existing code style, even if you'd do it differently. Clean up imports/variables YOUR changes orphaned, but don't touch pre-existing dead code unless asked.
- **Verify before done** — never mark complete without proving it works; diff behavior, run tests, check logs

## Guardrail Skill Triggers

Situational discipline rules live in the `lg-guardrails` plugin as progressive-disclosure skills. They are NOT always loaded — load the matching skill when any of these situations apply:

| Trigger situation                                                       | Skill to invoke          |
| ----------------------------------------------------------------------- | ------------------------ |
| Code edit finished / refactor / rename / large file / commit / new file | `engineering-discipline` |
| Building automation-pipeline-tool / API error / raw content pasted      | `task-discipline`        |
| Any work under `clients/gtm-client-*/` or on a named client             | `client-discipline`      |

Each skill's SKILL.md is a lean index; read only the specific reference file inside `references/` that matches the situation. Do NOT load references eagerly — the whole point is selective loading.

## When to Use Agents

Agents preserve main context — use them for multi-file work:

| Task                      | Use Agent? |
| ------------------------- | ---------- |
| Multi-file implementation | Yes        |
| Following a plan phase    | Yes        |
| New feature with tests    | Yes        |
| Single-line fix           | No         |
| Quick config change       | No         |

**Pattern — spawn, don't read:**

```
Wrong: Main reads files → understands → edits → reports (burns 2000+ tokens)
Right: Main spawns agent("implement X") → agent reads/edits → Main gets 200-token summary
```

**Trigger words:** implement, build, create feature, follow the plan, do phase X, use implementation agents

## Agent Roster

| Agent               | Model  | Use For                                                   |
| ------------------- | ------ | --------------------------------------------------------- |
| `smart-searcher`    | Haiku  | Discovery, file search, context loading — ALWAYS first    |
| `task-orchestrator` | Sonnet | Route complex/ambiguous multi-step tasks                  |
| `lg-researcher`     | Sonnet | Market research, competitor analysis, workspace synthesis |
| `lg-reviewer`       | Sonnet | Content QA, voice + ICP review                            |
| `lg-writer`         | Opus   | LeadGrow-voice content with full company context          |

## Subagent Coordination with Tasks

For multi-session or multi-agent work, use Claude Code native Tasks:

- Create a named task list (e.g., `client-teachaid`, `leadgrow-content`)
- Pass task list ID to subagents via environment
- Subagents update shared tasks as they complete work
- Use `Ctrl+T` to view task list in terminal

**Use Tasks when:** multi-step implementation, spawning coordinated subagents, work spans sessions.
**Skip Tasks when:** single quick fix, simple config change, purely conversational.

## Verification

Before starting, reframe the task as verifiable success criteria:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

Before calling any task complete:

1. Check if expected directories/files exist
2. Check logs for errors
3. Run the failing command manually to see actual output
4. Only then edit code — don't assume what failed
5. **Run project-specific checks** — invoke the `engineering-discipline` skill and read `references/verify-after-edit.md` for type-checker/linter requirements per project type

## Deep Refactor Mode

Default behavior is minimal-impact: simplest fix, smallest change. That's correct for most tasks.

For deep refactors where the user explicitly wants architectural fixes, apply the senior dev standard: **"What would a senior, perfectionist dev reject in code review? Fix all of it."** Only when explicitly asked for deep work — triggered by words like "refactor the architecture", "fix this properly", "don't be lazy", "production-grade".

## Self-Improvement

After any user correction → capture the learning via `/leadgrow:capture-learning`. Write rules that prevent the same mistake. Review learnings at session start for the relevant project.

## 80/20 Chunking

For complex tasks: identify the 3 most critical items that deliver 80% of the value. Complete those first, then reassess. Plans with 10+ steps get broken into chunks of 3-5, each independently verifiable.

## Session Kickoff

For any multi-step task (3+ steps), create a TodoWrite checklist before executing.

- Order items by impact — highest-value work ships first even if session ends early
- Check off each item immediately when done (don't batch completions)
- If spawning agents, track what each agent owns in the checklist
- The checklist makes remaining work obvious if context compresses or session ends

This complements 80/20 Chunking: chunk first, then checklist the chunks.
