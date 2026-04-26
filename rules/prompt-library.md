# Prompt Library: Check Before Generating

Before generating structured output inline via API call (campaign ideas, pain analysis, enrichment fields, classification), check `leadgrow-hq/prompts/_catalog.md` for a graduated prompt targeting that task.

## Why

Graduated prompts were optimized for cost and quality on a specific model through the anneal loop. They hit 92%+ accuracy on validation data. Inline generation on Opus is more expensive and less tested than using the graduated prompt on its target model.

## When This Applies

- You're about to call an LLM API with a hand-written system prompt for a task that looks like it could have a graduated prompt
- You're building a skill or pipeline that generates structured output
- A user asks for output that matches a prompt's description in the catalog

## What To Do

1. Check `leadgrow-hq/prompts/_catalog.md` for a matching prompt
2. If found: read `prompts/[name]/metadata.json` for the input schema and target model
3. Use the graduated prompt via API call to the target model (usually a cheap model like gpt-5-nano)
4. If not found: generate inline as normal, and consider whether the task is worth annealing later

## Prompt Library Convention

Any repo can have a `prompts/` directory following this structure:

```
prompts/
  _catalog.md                    <- auto-generated index
  [prompt-name]/
    prompt.md                    <- the graduated prompt text
    metadata.json                <- model, scores, inputs, outputs
    examples/                    <- real outputs for review
```

Regenerate catalog: `bun leadgrow-hq/tools/prompt-library/generate-catalog.ts`
