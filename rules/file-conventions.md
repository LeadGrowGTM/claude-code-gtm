# File Naming Conventions

Consistent naming patterns for all file types in the workspace.

| Type        | Pattern                                      | Example                            |
| ----------- | -------------------------------------------- | ---------------------------------- |
| Skills      | `[skill-name]/SKILL.md` — always a folder    | `cold-email-v2/SKILL.md`           |
| Prompts     | `prompts/[name]/prompt.md` + `metadata.json` | `prompts/outbound-campaign-ideas/` |
| Tools       | `[action]_[target].py`                       | `create_proposal.py`               |
| MCP docs    | `[ServerName].md`                            | `EmailBison.md`                    |
| Client docs | `_master.md`                                 | Required in each client folder     |
| Commands    | `[name].md`                                  | `capture-learning.md`              |
| Rules       | `[name].md`                                  | `archive-safety.md`                |

**Never use vague names** like `utils.py`, `helper.md`, or `misc.md`.

## File Routing

### Company Knowledge (`leadgrow-hq/company/`)

| Content Type        | Destination                          |
| ------------------- | ------------------------------------ |
| ICP updates         | `leadgrow-hq/company/ICP.md`         |
| Voice/brand changes | `leadgrow-hq/company/voice-guide.md` |
| New case studies    | `leadgrow-hq/company/social-proof/`  |
| Operational docs    | `leadgrow-hq/company/methodology/`   |
| Messaging updates   | `leadgrow-hq/company/messaging.md`   |
| Offering changes    | `leadgrow-hq/company/offerings.md`   |

### GTM / Outbound

| Content Type             | Destination                            |
| ------------------------ | -------------------------------------- |
| Active campaign work     | `clients/gtm-client-[name]/`           |
| Campaign templates       | `leadgrow-hq/campaigns/templates/`     |
| Email sequences          | `clients/gtm-client-[name]/sequences/` |
| Lead lists               | Google Sheets (not local)              |
| Campaign reports         | `clients/gtm-client-[name]/reports/`   |
| Cross-client patterns    | `leadgrow-hq/campaigns/patterns/`      |
| LeadGrow's own campaigns | `leadgrow-hq/campaigns/leadgrow/`      |

### Content (`leadgrow-hq/content/`)

| Content Type                | Destination                               |
| --------------------------- | ----------------------------------------- |
| LinkedIn drafts             | `leadgrow-hq/content/drafts/linkedin/`    |
| Newsletter drafts           | `leadgrow-hq/content/drafts/newsletters/` |
| Content ideas               | `leadgrow-hq/content/ideas/backlog.md`    |
| Content atoms               | `leadgrow-hq/content/atoms/`              |
| Reference guides & patterns | `leadgrow-hq/content/libraries/`          |

### Skills, Agents & Commands

| Content Type                                    | Destination                                   |
| ----------------------------------------------- | --------------------------------------------- |
| Universal skills (all repos)                    | `.claude/skills/[skill]/SKILL.md`             |
| Universal agents (orchestration, model routing) | `.claude/agents/[agent].md`                   |
| LeadGrow-specific skills                        | `leadgrow-hq/.claude/skills/[skill]/SKILL.md` |
| LeadGrow-specific agents                        | `leadgrow-hq/.claude/agents/[agent].md`       |
| Domain skills (outbound, content, etc.)         | `lg-[domain]/skills/[skill]/SKILL.md`         |
| LeadGrow commands                               | `leadgrow-hq/.claude/commands/leadgrow/`      |
| Workspace rules                                 | `.claude/rules/`                              |
| Graduated prompts (LG-specific)                 | `leadgrow-hq/prompts/[name]/prompt.md`        |
| Graduated prompts (universal, future)           | `.claude/prompts/[name]/prompt.md`            |
| Prompt library tooling                          | `leadgrow-hq/tools/prompt-library/`           |

### Tools & Scripts

| Content Type           | Destination                           |
| ---------------------- | ------------------------------------- |
| Reusable scripts       | `leadgrow-hq/tools/[category]/`       |
| Data processing        | `leadgrow-hq/tools/csv-processing/`   |
| Skill-specific scripts | `lg-[domain]/skills/[skill]/scripts/` |

### Archive & Temporary

| Content Type                          | Destination                               |
| ------------------------------------- | ----------------------------------------- |
| Completed campaigns                   | `leadgrow-hq/archive/campaigns/[client]/` |
| Research docs                         | `leadgrow-hq/archive/research/`           |
| Competitor intel                      | `leadgrow-hq/archive/battlecards/`        |
| MCP documentation                     | `leadgrow-hq/archive/mcp-docs/`           |
| Temp files (API tests, CSVs, scratch) | `temp/` subfolders                        |

### Cloud Destinations

| Deliverable              | Service               |
| ------------------------ | --------------------- |
| Lead lists               | Google Sheets         |
| Proposals                | Website (leadgrow.ai) |
| LinkedIn/Twitter content | Typefully             |
| Email campaigns          | EmailBison            |
| Blog/web content         | Sanity CMS            |

**Key rules:** Never save to workspace root. Local files for processing, cloud for delivery. Archive, don't delete. temp/ is deletable.

## YAML Frontmatter

All skills and commands use YAML frontmatter for discovery.

```yaml
---
name: skill-name
description: What it does, when to use it, key capabilities
---
```

**Description best practices:**

- Include action verbs (analyze, create, extract)
- Include trigger scenarios (when user asks for X, when Y happens)
- Include keywords users would search for
