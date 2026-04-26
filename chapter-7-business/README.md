# Chapter 7 — The Business Layer

**Time:** 20 min | **Chapter goal:** Understand what this system does to your cost of delivery and how to talk about it.

---

## What's Here

- [`delivery-model.md`](./delivery-model.md) — headcount math, pricing models, margin analysis
- [`client-onboarding-template/`](./client-onboarding-template/) — drop-in template for onboarding new clients into the system

---

## The Core Claim

This isn't a productivity hack. It's a cost-of-delivery restructure.

Traditional 10-client GTM agency:
- 6-8 SDRs ($X each/month)
- 1-2 managers ($Y each/month)
- Tool stack (Clay, N8n, Smartlead) = $Z/month

Operator model running this system:
- 2 operators
- Claude Code ($20/month)
- Bison + data sources

**Same client count. Higher output per campaign. Lower headcount cost.**

The math is in `delivery-model.md`. Run the numbers against your own P&L.

---

## Making the Case to a Client

When a client asks "why Claude Code instead of a traditional SDR team," the answer isn't "it's faster." The answer is:

1. **Research depth** — Every company gets 10-15 minutes of research, not 60 seconds of template-filling. The sequence reflects what you actually know about them.
2. **Zero degradation** — An SDR's output quality drops on Friday afternoon. This doesn't.
3. **Iteration speed** — When a sequence underperforms, you rewrite it in 20 minutes with the same research context. No rebriefing.

The objection you'll hear: "Is the copy good enough?" The answer is: load `chapter-6-live-build/after/campaigns/stackbridge-sequence.md` and show them.

---

## Client Onboarding

When you close a new client, run through [`client-onboarding-template/`](./client-onboarding-template/) to configure the workspace:

1. Fill in `_master.md` with client context
2. Set ICP parameters
3. Load any existing campaign data
4. Configure Bison workspace

Takes about 90 minutes the first time, 30 minutes once you've done it a few times.

---

## End State

You now have the full system:

```
your-workspace/
├── CLAUDE.md                    ← operator brief
├── .claude/
│   ├── rules/                   ← 3-7 constraints
│   ├── skills/                  ← cold-email, icp-research, sales-call-prep
│   └── agents/                  ← smart-searcher, researcher
├── scripts/
│   └── enrich.js                ← enrichment waterfall
├── clients/
│   └── [client]/                ← per-client workspace
└── knowledge-graph/scripts/     ← kg-query.js, kg-index.js
```

Clone once. Adapt forever.
