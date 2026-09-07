# Claude Code for GTM Operators - Course Repo

YouTube course companion. 7 chapters covering Claude Code system design for GTM agencies.
Remote: `github.com/LeadGrowGTM/claude-code-gtm` | Branch: `main`
Category: projects/course

## Context

Full reference implementation for the "Claude Code for GTM Operators" YouTube course. 7 chapters covering system design for GTM agencies - from CLAUDE.md through enrichment waterfalls to business layer. Includes slide deck, speaker notes, and production guide.

## What This Is

A reference implementation, not a framework. Students clone once, adapt to their workspace.
Every chapter folder is self-contained - a README, working code, and concrete artifacts.

The thesis: Clay + N8n + Smartlead is three tools doing what one system should handle.
This repo shows what that one system looks like.

## Chapter Map

| Folder | Chapter | Artifact |
|--------|---------|----------|
| `chapter-1-foundation/` | Stack Replacement Thesis | Architecture mental model |
| `chapter-2-foundation/` | CLAUDE.md | Operator brief design |
| `chapter-3-skills/` | Skills | cold-email + icp-research skills |
| `chapter-4-agents/` | Agents | smart-searcher, researcher, task-orchestrator |
| `chapter-5-waterfall/` | Enrichment Waterfall | enrich.js pipeline |
| `chapter-6-live-build/` | Live GTM Build | before/ -> after/ diff |
| `chapter-7-business/` | Business Layer | delivery model + headcount math |

## Key Files

- `SLIDES.md` - Full slide deck (75 slides) with storyboards + speaker notes. Source of truth for course content. **13 placeholder numbers still need real values** - see `HANDOFF.md` for the list.
- `PRODUCTION.md` - Slide-by-slide breakdown: loop tracker, edit flags, pacing guide. Use for final edit pass.
- `HANDOFF.md` - Next session context. Start here if resuming work.
- `MILESTONES.md` - GTM Orchestrator v1->v4 evolution. Shows what the system becomes after 30 days of real client work.
- `CLAUDE.md.template` - What students copy to bootstrap their own workspace. Keep this lean and generic.
- `.continue-here.md` - Session bookmark. Update when pausing mid-work.

## Chapter 6 - Live Build Diff

The before/after folders show exactly what gets built during the live session:

```bash
# Quick diff - what changed
diff -rq chapter-6-live-build/before/ chapter-6-live-build/after/

# Full content diff
diff -r chapter-6-live-build/before/ chapter-6-live-build/after/

# In git
git diff HEAD -- chapter-6-live-build/before/ chapter-6-live-build/after/
```

`before/` = bare Claude Code install, no GTM infrastructure.
`after/` = rules + skills + research doc + two-email sequence, ready for Bison upload.

## Commands

```bash
# Enrichment waterfall
cd chapter-5-waterfall && npm install
node scripts/enrich.js

# Knowledge graph indexer
bun knowledge-graph/scripts/kg-index.js

# KG query
bun knowledge-graph/scripts/kg-query.js search "topic"

# Build course HTML (slides -> web)
python build_course_html.py

# Build slides PDF
python build_slides_pdf.py
```

## Skills in This Repo

| Skill | Path | Purpose |
|-------|------|---------|
| cold-email | `skills/cold-email/SKILL.md` | Generate cold email sequences from research |
| icp-research | `skills/icp-research/SKILL.md` | Run ICP research against a company |
| sales-call-prep | `skills/sales-call-prep/SKILL.md` | Prep for discovery/demo calls |

## Agents in This Repo

`agents/smart-searcher.md` - Haiku-powered file discovery. Spawn first before any Sonnet work.

## Adding New Content

**New chapter:** Add `chapter-N-[slug]/` with a `README.md` that follows the same format - what you build, key steps, code snippet if applicable.

**New skill:** Add to `skills/[skill-name]/SKILL.md`. Update chapter 3 README if it's demo material.

**Slide edits:** Edit `SLIDES.md` directly. Use `PRODUCTION.md` to track loop state and flag gaps. After filling placeholders:

```bash
git add SLIDES.md && git commit -m "docs(slides): fill in real numbers - cost, headcount, margin"
git push origin main
```

**Template changes:** `CLAUDE.md.template` is what students get. Keep it generic - no LeadGrow references, no internal tooling. Brackets around everything they need to replace.
