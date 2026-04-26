# Scope Before Execute

Before executing any task that touches files, state scope, target, and done-state. Don't infer from "obvious" context — say assumptions out loud.

## Pattern

1. State assumptions before starting:
   - **Scope** — which client or project this applies to
   - **Target** — which branch or directory changes go to
   - **Output** — what format the deliverable should be in
2. Proceed immediately after stating assumptions unless corrected
3. If scope shifts mid-task, re-state before continuing

## Don't

- Silently assume scope from vague context
- Ask a checklist of questions — state and move
- Default to main branch without confirming on non-trivial changes
