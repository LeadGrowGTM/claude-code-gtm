---
name: icp-research
description: Research a company and score ICP fit. Takes company name/URL, returns structured fit report with trigger signals, pain hypothesis, and recommended sequence angle.
---

# ICP Research

Research a target company and return a structured ICP fit report.

## Define

Takes a company name + URL. Returns: industry, size estimate, tech stack signals,
ICP fit score (1-10), primary pain hypothesis, and recommended outreach angle.

## Uses

- Pre-campaign qualification
- Live enrichment during list building
- Deciding which sequence angle to use

## Insider Knowledge

<!-- Fill in after 10 real runs — what signals actually predict good fit? -->
- Headcount 20-200 = sweet spot for outbound-heavy GTM
- Job postings for "SDR", "BDR", "sales development" = active pipeline investment
- No CRM listed on their stack = likely using spreadsheets = high pain
- Series A-B = growth pressure, limited headcount, strong use case
- Tech stack: if they use Salesforce but no outreach tool = gap = angle

## Format

**Company:** [name]
**Website:** [url]
**Industry:** [industry]
**Headcount:** [estimate]
**Tech Stack Signals:** [what you found]

**ICP Fit Score:** [1-10]
**Fit Rationale:** [2 sentences — why this score]

**Primary Pain Hypothesis:** [the thing they're most likely struggling with]
**Recommended Angle:** [what your first email should lead with]
**Red Flags:** [anything that should disqualify or deprioritize]

## Sources to Check

1. Company website (About, Careers, Product pages)
2. LinkedIn company page (headcount, job postings, recent hires)
3. G2/Capterra reviews (if applicable — what customers say)
4. TechSight for tech stack: `techsight [domain]`
