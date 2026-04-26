---
name: cold-email
description: Generate Step 1 + Step 2 cold email sequence from ICP research output.
  Use when user asks to write a cold email, sequence, or outreach copy for a company.
  Requires ICP research doc or company context.
---

# Cold Email Skill

Write a two-step outbound sequence grounded in research. No templates. Every sequence is built from the specific pain and signal in the research doc.

## Intake

Required before any output:
- ICP research doc (from `icp-research` skill) or equivalent company context
- Sender name and company
- Offer in one sentence (what you do, for who, what outcome)

## Quality Gates

Every email must pass before output:
- [ ] Subject line is under 8 words, no clickbait
- [ ] Step 1 body is under 100 words
- [ ] Step 2 body is under 75 words
- [ ] No links in either step
- [ ] Pain referenced is specific to this company — not a generic claim
- [ ] CTA is one question, not a pitch

## Output Format

```markdown
# [Company] — Outreach Sequence

## Step 1

**Subject:** [under 8 words]

[Body — under 100 words]

---

## Step 2 (send day 4-5 if no reply)

**Subject:** Re: [same subject]

[Body — under 75 words, different angle from Step 1]
```

## What Not To Do

- Don't open with "I noticed..." or "I came across your company..."
- Don't list features. Lead with the outcome or the pain.
- Don't include a calendar link in Step 1. The goal is a reply, not a booking.
- Don't write Step 2 as a guilt-trip bump. New angle only.
