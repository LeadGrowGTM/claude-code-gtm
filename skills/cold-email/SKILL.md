---
name: cold-email
description: Write cold outbound emails for a specific ICP. Accepts company context, pain points, and sequence position. Returns subject line + body ready for Bison upload.
---

# Cold Email

Write cold outbound email copy for B2B outreach campaigns.

## Define

A cold email skill that takes company context and ICP pain points and returns
a complete email: subject line + body. Sequence-position aware (step 1 vs step 2).

## Uses

- Generating initial outreach for a new campaign segment
- Rewriting underperforming sequences
- A/B variant generation

## Insider Knowledge

<!-- This is the moat. Fill this in after 10 real outputs. -->
<!-- What makes a cold email actually land for YOUR ICP? -->
<!-- Examples: -->
- Subject lines under 6 words outperform longer ones for this ICP
- Never open with "I" — open with them (observation about their company/role)
- Step 2 should reference step 1 but never beg — reframe, don't follow up
- Use single-brace variables: {FIRST_NAME}, {COMPANY}, {PAIN_POINT}
- No links. No attachments. One CTA max.

## Format

**Subject:** [under 6 words, no clickbait]

**Body:**
[opening observation — about them, not you]
[one-line bridge to the pain]
[your proof or mechanism — one sentence]
[CTA — specific, low-friction]

[Signature]

## Inputs Required

- Company name + website
- ICP role (who we're writing to)
- Core pain point / trigger
- Sequence step (1 or 2)
- Sender name + company

## Quality Gates

- No double-dash (--) or em-dash (—)
- No "I hope this finds you well" or equivalent
- Subject line: not a question, not clickbait
- Body: under 100 words for step 1, under 80 for step 2
