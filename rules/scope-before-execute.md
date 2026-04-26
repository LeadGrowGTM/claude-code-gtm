# Scope Before Execute

Before executing any task that touches files, confirm scope, target, and done-state. Don't infer from "obvious" context — state assumptions explicitly.

## Pattern

Wrong-approach friction comes from charging ahead with confident but incorrect assumptions about scope, branch, or output format. The fix is stating assumptions upfront, not asking questions.

## DO

1. Before starting, state (don't ask) your assumptions on:
   - **Scope** — which client/repo this applies to (global vs client-specific)
   - **Target** — which branch changes go to
   - **Output** — what format/length the deliverable should be
2. Proceed immediately after stating assumptions unless corrected
3. Mid-task, if scope shifts or becomes ambiguous, pause and re-state before continuing

## DON'T

- Silently assume scope from vague context and charge ahead
- Ask a checklist of questions and wait — state and move
- Treat "lean" as obvious (could mean less output, stripped architecture, minimal code)
- Default to `main` branch without confirming on non-trivial changes
- Skip this checkpoint just because the task "seems obvious"
