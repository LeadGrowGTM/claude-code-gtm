---
name: icp-research
description: Research a company and score ICP fit. Use when user asks to research a company,
  qualify a prospect, or assess ICP match before writing a sequence. Requires domain or company name.
---

# ICP Research Skill

Research a company and score ICP fit. Output is a structured research doc that feeds directly into the cold-email skill.

## Intake

Required before any output:
- Company domain or name
- Your ICP definition (or load from `company/ICP.md` if it exists)

## Research Sequence

Run in this order. Stop when you have enough signal for a personalized sequence.

1. **Website** — homepage, about, product pages. Extract: what they do, who they sell to, key claims.
2. **Job postings** — open SDR/AE/RevOps roles signal GTM investment and pain points.
3. **Tech stack** — run TechSight or check BuiltWith. Signals sophistication and existing tool overlap.
4. **LinkedIn** — headcount, growth rate, recent posts from founders/execs.
5. **News** — funding, launches, leadership changes. Triggers for outreach timing.

## ICP Scoring

Score 1-5 on each dimension:

| Dimension | Signal |
|-----------|--------|
| Company size | Employee count vs. your ICP range |
| GTM motion | Outbound vs. inbound signals in job postings |
| Tech alignment | Stack overlap with your ICP |
| Growth signal | Headcount growth or recent funding |
| Pain fit | Evidence of the pain your offer solves |

**Threshold:** Score >= 16/25 = qualify. Score < 12 = skip. 12-15 = judgment call.

## Output Format

```markdown
# [Company Name] — ICP Research

**Domain:** [domain]
**ICP Score:** [X/25]
**Verdict:** [Qualify / Skip / Judgment call]

## What They Do
[2-3 sentences]

## Who They Sell To
[ICP for their product]

## GTM Signals
- [Signal 1]
- [Signal 2]

## Tech Stack
[Key tools relevant to your offer]

## Pain Fit
[Specific evidence of the pain your offer solves]

## Best Angle
[The hook that should drive Step 1 of the sequence]
```

Pass this output to the `cold-email` skill to generate the sequence.
