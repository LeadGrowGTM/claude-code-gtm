# Handoff — Next Session

## What this repo is
YouTube course: "Claude Code for GTM Operators" — companion repo at `github.com/LeadGrowGTM/claude-code-gtm`.

## State of the deck
`SLIDES.md` — 57 slides, complete with storyboards + speaker notes. Production-ready except for 13 placeholder numbers listed below.

`PRODUCTION.md` — slide-by-slide breakdown with loop tracker, edit flags, and pacing guide.

## One task for next session
Fill in the 13 placeholder numbers in SLIDES.md, then commit and push.

Mitch will provide the answers at the start of the session. Fill them in at the exact lines below using Edit tool.

---

## The 13 numbers — what to ask Mitch, what line to edit

| # | Slide | Placeholder | Ask Mitch for |
|---|-------|-------------|---------------|
| 1 | 1.1 storyboard | `$X/month` (combined stack cost) | Monthly spend: Clay + N8n/Make + sending tool combined |
| 2 | 5.5 table | `$X/credit` (Clay) | Clay enrichment credit cost on their plan |
| 3 | 5.5 table | `$Y/record` (FullEnrich) | FullEnrich cost per record — or confirm if they don't use it (delete row) |
| 4 | 5.6 table | `$X` (Clay-only, 1k records) | Actual cost per 1,000 records enriched in Clay |
| 5 | 5.6 table | `~$Y` (waterfall, 1k records) | Estimated waterfall cost per 1,000 records from enrich.js runs |
| 6 | 6.3 speaker notes | `[X] minutes` | Fill AFTER Ch.6 recording — exact elapsed time |
| 7 | 7.2 table | `$X each` (SDR) | What they'd pay per SDR/mo loaded (salary + benefits + tools) |
| 8 | 7.2 table | `$Y each` (Manager) | What a GTM manager costs/mo loaded |
| 9 | 7.2 table | `$Z/month` (tools) | What Clay + N8n + Smartlead costs at their client volume |
| 10 | 7.3 table | `$X each` (Operator) | What operators actually get paid at LeadGrow |
| 11 | 7.3 table | `$Y/month` (Bison) | Actual Bison subscription cost |
| 12 | 7.3 table | `$Z/month` (Data sources) | Apollo or list source monthly cost |
| 13 | 7.5 table | Revenue per client / CoD before / CoD after | Avg monthly retainer + old vs. new cost of delivery |

**Also resolve in session:**
- Slide 7.7: `X% lower cost per meeting` — rough % or "roughly half" with one supporting data point
- Slide 7.6: "Payback period: 90 days" — confirm this is defensible or adjust the number
- Bonus segment (B.1): Confirm Fireflies own call recordings vs. Hormozi reference (own recordings = stronger credibility)

---

## How to fill them in
Once Mitch gives the numbers, use Edit tool to replace each placeholder in SLIDES.md, then:
```bash
git add SLIDES.md && git commit -m "docs(slides): fill in real numbers — cost, headcount, margin"
git push origin main
```

## Repo location
`C:\Users\mitch\Everything_CC\claude-code-gtm\`
Remote: `github.com/LeadGrowGTM/claude-code-gtm`
Branch: `main`
