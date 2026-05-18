# Chapter 3 — Skills: SOPs That Run Forever

**Time:** 35 min | **Chapter goal:** Write your first two skills and understand the lifecycle.

---

## What You're Building

Two skills in `skills/`:

| Skill | What it does |
|-------|-------------|
| [`cold-email/`](./skills/cold-email/SKILL.md) | Generate Step 1 + Step 2 sequences from research input |
| [`icp-research/`](./skills/icp-research/SKILL.md) | Research a company and score ICP fit |

Plus `sales-call-prep/` — a third skill for pre-call intelligence briefings.

---

## What a Skill Is

A skill is a markdown file that replaces a standing instruction you'd otherwise repeat every session. Once it's in `skills/`, Claude finds it automatically.

```
skills/
└── cold-email/
    └── SKILL.md      ← The skill
```

The SKILL.md has three parts:
1. **YAML frontmatter** — name + description for discovery
2. **Intake** — what inputs are required before any output is generated
3. **Output format** — exactly what gets produced and how

---

## The Lifecycle

```
USE → LOG friction (GitHub Issues) → REVIEW weekly → IMPROVE (branch + PR) → RELEASE
```

Skills degrade if you don't run them against real data. The first time a skill hits a real edge case, file a GitHub Issue with the exact failure. That's your improvement backlog.

---

## Writing Your First Skill

Start with the task you repeat most. For most GTM operators that's "write a cold email from research." The prompt you run manually today becomes the skill file you invoke tomorrow.

Pattern:
```markdown
---
name: cold-email
description: Generate Step 1 + Step 2 email sequence from company research. 
  Triggered when user asks to write a cold email, sequence, or outreach copy.
---

## Intake
Required before any output:
- Company name + domain
- ICP fit assessment (from icp-research skill or manual input)
- Key pain or trigger

## Output
Step 1: Subject + body (under 100 words)
Step 2: Follow-up (under 60 words, different angle)
```

---

## End State

```
your-workspace/
├── CLAUDE.md
└── .claude/
    ├── rules/
    └── skills/
        ├── cold-email/SKILL.md
        ├── icp-research/SKILL.md
        └── sales-call-prep/SKILL.md
```

---

---

## Bonus: Install a Pre-Built Skill

The Feynman skill is a ready-to-install example of a non-GTM skill that shows how skills generalize. It teaches any concept using the Feynman Technique — you explain first, Claude probes your gaps, then delivers a calibrated explanation calibrated to your level. Also outputs HTML concept explainers for dashboards and reports.

```bash
mkdir -p .claude/skills/feynman/references
curl -sL https://raw.githubusercontent.com/LeadGrowGTM/feynman-skill/main/SKILL.md \
  -o .claude/skills/feynman/SKILL.md
curl -sL https://raw.githubusercontent.com/LeadGrowGTM/feynman-skill/main/references/concept-guide.md \
  -o .claude/skills/feynman/references/concept-guide.md
curl -sL https://raw.githubusercontent.com/LeadGrowGTM/feynman-skill/main/references/html-template.md \
  -o .claude/skills/feynman/references/html-template.md
```

Then: `feynman pipeline velocity` — Claude will ask your familiarity level and run the technique.

Repo: `github.com/LeadGrowGTM/feynman-skill`

---

## Next Chapter

[Chapter 4 →](../chapter-4-agents/README.md) — Add agents for multi-step tasks.
