# Claude Code for GTM Operators

The companion repo for the course. Every chapter has a folder. Clone once, adapt forever.

**Course:** [YouTube link]
**Audience:** Agency operators, GTM engineers, AEs running campaigns at scale

---

## The Thesis

Clay + N8n + Smartlead is three tools doing what one system should handle.
This repo is that system — built on Claude Code, running in production.

---

## Chapter Map

| Folder | Chapter | What you build |
|--------|---------|----------------|
| `chapter-1-foundation/` | Stack Replacement Thesis | Architecture mental model |
| `chapter-2-foundation/` | CLAUDE.md | Your operator brief |
| `chapter-3-skills/` | Skills | cold-email + icp-research skills |
| `chapter-4-agents/` | Agents | smart-searcher, researcher, task-orchestrator |
| `chapter-5-waterfall/` | Enrichment Waterfall | enrich.js pipeline |
| `chapter-6-live-build/` | Live GTM Build | before/ → after/ diff |
| `chapter-7-business/` | Business Layer | delivery model + headcount math |

---

## Quick Start

```bash
git clone https://github.com/LeadGrowGTM/claude-code-gtm
cd claude-code-gtm

# Start here — copy and customize
cp CLAUDE.md.template your-workspace/CLAUDE.md

# Install enrichment waterfall deps
cd chapter-5-waterfall && npm install

# Run knowledge graph indexer
bun knowledge-graph/scripts/kg-index.js
```

---

## Tool Index

| Tool | Repo | Use case |
|------|------|---------|
| Bison CLI | [LeadGrowGTM/bison-cli](https://github.com/LeadGrowGTM/bison-cli) | EmailBison campaign management |
| TechSight | [LeadGrowGTM/techsight](https://github.com/LeadGrowGTM/techsight) | Free tech stack detection (Tier 1 waterfall) |
| GSD Plugin | [get-shit-done](https://github.com/anthropics/claude-code-skill-template) | Planning system used throughout |
| youtube-transcript | [badlogic/pi-skills](https://github.com/badlogic/pi-skills/tree/main/youtube-transcript) | Transcript fetching |

---

## What's In Here

```
claude-code-gtm/
├── CLAUDE.md.template        ← Start here
├── .env.example
├── SLIDES.md                 ← Full slide deck with speaker notes
├── rules/                    ← 7 behavioral constraint files
├── agents/                   ← smart-searcher, task-orchestrator, researcher
├── skills/                   ← cold-email, icp-research, sales-call-prep + more
├── knowledge-graph/scripts/  ← kg-query.js, kg-index.js, kg-skill-graph.js
├── chapter-[1-7]-*/          ← Per-chapter files and READMEs
└── tools/                    ← Links to open-source CLIs
```

---

## License

MIT. Fork it, adapt it, run it.
