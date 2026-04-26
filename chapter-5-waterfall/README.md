# Chapter 5 — The Enrichment Waterfall

**Time:** 30 min | **Chapter goal:** Replace Clay standard enrichment with a pipeline you own.

---

## What You're Building

`scripts/enrich.js` — a 3-tier enrichment waterfall that runs against any domain.

---

## The Tier Logic

```
Tier 1: Free       → website scrape, LinkedIn signals
Tier 2: Cheap APIs → OpenWebNinja ($0.002/query), TechSight (free)
Tier 3: Paid       → Apollo, Clearbit, or whatever you configure
```

Run Tier 1 first. If it produces enough signal, stop. Only escalate when the data quality is insufficient for the sequence. Most companies resolve at Tier 1 or 2.

**The math:** Tier 2 at $0.002/query vs. Clay at $0.05–0.15/row. At 500 companies/month, that's ~$1 vs. ~$50. The waterfall pays for itself in week one.

---

## Quick Start

```bash
cd chapter-5-waterfall

# Install deps
npm install

# Enrich a single domain
node scripts/enrich.js acme.com

# Enrich a CSV
node scripts/enrich.js --csv leads.csv --output enriched.csv
```

---

## Environment Setup

Copy and fill in `.env`:

```bash
cp ../env.example.txt .env
```

Required for Tier 2:
```
OPENWEBNINJA_API_KEY=your_key
```

Optional for Tier 3:
```
APOLLO_API_KEY=your_key
CLEARBIT_API_KEY=your_key
```

TechSight is free — no key needed. Repo: [LeadGrowGTM/techsight](https://github.com/LeadGrowGTM/techsight)

---

## Output Format

Each enriched company returns:

```json
{
  "domain": "acme.com",
  "tier": 1,
  "data": {
    "company_name": "Acme Corp",
    "description": "...",
    "tech_stack": ["HubSpot", "Salesforce", "Segment"],
    "employee_count": "51-200",
    "hiring_signals": ["SDR", "RevOps Manager"],
    "linkedin_url": "..."
  }
}
```

The `tier` field tells you how far the waterfall went — useful for auditing cost.

---

## Wiring to Claude Code

Once enriched, pass the output to the `icp-research` skill:

```
"Here's the enrichment data for acme.com: [paste JSON]. Run ICP research."
```

The skill scores ICP fit and surfaces the 1-2 pain points most relevant to your offer.

---

## End State

```
your-workspace/
├── CLAUDE.md
└── .claude/
    ├── rules/
    ├── skills/
    └── agents/
scripts/
└── enrich.js       ← runs standalone, no Claude needed
```

---

## Next Chapter

[Chapter 6 →](../chapter-6-live-build/README.md) — The main event. Cold company. No prep. Live campaign in under an hour.
