# Claude Code for GTM Operators
## Full Slide Deck + Speaker Notes

**Course:** Claude Code for GTM Operators
**Audience:** Agency operators, GTM engineers, AEs running campaigns at scale
**Format:** Each slide = visual description + speaker notes
**Companion repo:** github.com/LeadGrowGTM/claude-code-gtm

---

# INTRO

---

## Slide 0.1 — Title

**Visual:** Black background. Large text: "Claude Code for GTM Operators." Subtext: "The system behind agency-grade outbound." Repo link bottom right.

> **Speaker notes:** No intro. Just start. If you're watching this you already know what Claude Code is and you want to see it applied to real outbound work. That's what this is. Everything I show you here is running in production across 11 client campaigns right now.

---

## Slide 0.2 — Three things you will leave with

**Visual:** Three numbered items.
1. A working Claude Code GTM infrastructure
2. A companion repo — clone it once, adapt it forever
3. The headcount math to justify this to a client or your leadership

> **Speaker notes:** This isn't a tutorial. By the end you'll have the actual files — CLAUDE.md template, skills, agents, the enrichment waterfall script. Clone the repo now if you want to follow along. Link is on screen and in the description.

---

## Slide 0.3 — Three loops planted

**Visual:** Three callout boxes with timestamps (TBD).

- **Ch. 6:** "Cold company. No prep. Live campaign in under an hour."
- **Ch. 5:** "The enrichment waterfall that replaced most of our Clay spend."
- **Ch. 7:** "The headcount math. Two operators vs. six SDRs."

> **Speaker notes:** I'm planting three loops now so you know what to look forward to. Chapter 6 is the main event — I pick a company I've never touched, and we go from zero to a live campaign in under an hour. Timer on screen. No edits. Chapter 5 is the cost story. Chapter 7 is the business case.

---

## Slide 0.4 — Chapter map

**Visual:** Linear chapter progression with time estimates.

| Chapter | Title | Time |
|---------|-------|------|
| 1 | The Stack Replacement Thesis | 15 min |
| 2 | Foundation: CLAUDE.md | 20 min |
| 3 | Skills: SOPs That Run Forever | 35 min |
| 4 | Agents: Headcount Leverage | 25 min |
| 5 | The Enrichment Waterfall | 30 min |
| 6 | The Live GTM Build | 50 min |
| 7 | The Business Layer | 20 min |

> **Speaker notes:** Skip to whatever chapter is most relevant. Each one is standalone. If you're already running Claude Code and you just want to see the live build, jump to chapter 6. If you want the business case slides, that's chapter 7.

---

---

# CHAPTER 1 — THE STACK REPLACEMENT THESIS

---

## Slide 1.1 — Your current stack

**Visual:** Three tool logos side by side: Clay / N8n / Smartlead. Arrow pointing right: "= $X/month + 3 context switches per task."

> **Speaker notes:** If you're running a GTM agency right now you're probably paying for Clay, something like N8n or Make, and a sending platform. That stack works. I'm not going to tell you to rip it out. But I will show you where it breaks down and what you can replace.

---

## Slide 1.2 — What dies

**Visual:** Red X over each item.
- Zapier / basic automation logic
- Clay for standard enrichment (website scrape, LinkedIn, tech stack)
- Manual personalization workflows

> **Speaker notes:** Zapier is gone if you're serious about this. Clay's enrichment — specifically the stuff you can get from a company website, LinkedIn, and a tech stack tool — that's now a script you run once and own forever. Personalization at scale doesn't need a $800/month tool when you have a skill file that runs it on demand.

---

## Slide 1.3 — What survives

**Visual:** Green checkmark over each item.
- Apollo / data sources (you still need leads)
- Bison / Smartlead / Instantly (sending infra)
- Clay for complex signal-based workflows

> **Speaker notes:** Data sources survive. You still need Apollo or whatever list source you use — Claude Code doesn't generate leads out of thin air. Sending infra survives — Bison, Smartlead, Instantly. And Clay survives for genuinely complex signal-based workflows where you need its native integrations. Everything else is on the table.

---

## Slide 1.4 — What gets 10x'd

**Visual:** 10x multiplier graphic over three items.
- Research depth per company
- Personalization quality per email
- Workflow composition speed

> **Speaker notes:** Research depth is the biggest one. What used to take an SDR 20 minutes per company — reading the website, pulling their recent news, checking job postings — now takes 45 seconds. Personalization quality goes up because you're working from actual research, not a template. And composing new workflows — building new sequences, new ICP angles — drops from days to hours.

---

## Slide 1.5 — The 4-layer architecture

**Visual:** Stacked layer diagram.
```
┌─────────────────────────────┐
│         CLAUDE.md           │  ← Operator brief (permanent)
├─────────────────────────────┤
│           Rules             │  ← Behavioral constraints
├─────────────────────────────┤
│           Skills            │  ← SOPs that run forever
├─────────────────────────────┤
│           Agents            │  ← Workers you spawn
└─────────────────────────────┘
```

> **Speaker notes:** This is the whole system in one diagram. CLAUDE.md is the top — it's the brief that loads every session. Rules sit below that — they constrain behavior so you don't get hallucinated outputs on campaign copy. Skills are your encoded SOPs. Agents are the workers who run them. Every chapter covers one layer. By chapter 5 you'll have all four running together.

---

## Slide 1.6 — Repo intro

**Visual:** Terminal showing `git clone github.com/LeadGrowGTM/claude-code-gtm`

> **Speaker notes:** Clone the repo now. The companion repo mirrors the course chapter by chapter. Each folder has a README telling you what you're building, the files you need, and what the state should look like at the end. Chapter 6 has a before/ and after/ folder — you can diff them if you want to skip the build and just see the output.

---

---

# CHAPTER 2 — FOUNDATION: CLAUDE.md AS AN OPERATOR BRIEF

---

## Slide 2.1 — The claim

**Visual:** Single bold line centered: "CLAUDE.md isn't a config file. It's a permanent team member brief."

> **Speaker notes:** Every new Claude Code session reads CLAUDE.md first. That makes it the most important document in your workspace. Most people treat it like a README — a few lines about what the project does. That's wrong. Write it like you're onboarding someone who will never forget what you write, never get tired, and reads it fresh every single time they start work.

---

## Slide 2.2 — What goes in it

**Visual:** Five labeled sections with one-line descriptions.

```
## Identity       — who Claude is in this context
## Workflow Style — how to handle execution (ask vs act)
## Repos          — what directories exist and what they're for
## Work Routing   — where different types of work go
## Skill Discovery — how to find relevant skills
```

> **Speaker notes:** Five sections. Identity sets the operating mode — is this a cofounder? A meticulous analyst? An SDR? Workflow style is where you put execution preferences. Repos is the map of your workspace. Work routing tells it where to put different types of output. Skill discovery tells it how to find its own tools. That last one matters more as your skill library grows.

---

## Slide 2.3 — Code: Identity section

**Visual:** Code block, syntax highlighted.

```markdown
## Identity — Who You Are

You're not an assistant. You're [NAME]'s operator.

Your purpose: run outbound GTM for B2B SaaS clients.

Core behaviors:
- Lead with the answer. No filler.
- Read the file before asking. Come back with answers.
- Never hallucinate. If you don't know, say so.
- Default to action. Only ask when scope is genuinely ambiguous.
```

> **Speaker notes:** The identity section does two things: it sets the operating persona and it names the failure modes you want to prevent. "Default to action" stops the constant confirmation requests. "Read the file before asking" stops it from asking you questions it could answer by reading existing context. These sound like small things. They save 20 minutes per session.

---

## Slide 2.4 — Code: Workflow style

**Visual:** Code block.

```markdown
## Workflow Style

Don't ask for confirmation on every step during multi-step workflows.
Execute the plan, show results, and only pause if something fails
or is genuinely ambiguous.
```

> **Speaker notes:** This is the line that changes the most about how you work. Without it, Claude asks "should I proceed?" after every step. With it, you give a task and come back to results. For GTM work — building a campaign, running enrichment, writing a sequence — you want the latter.

---

## Slide 2.5 — Code: Work routing table

**Visual:** Code block with markdown table.

```markdown
## Work Routing

| Work Type | Destination |
|-----------|-------------|
| Cold email, campaigns | campaigns/ |
| ICP, voice, messaging | company/ |
| LinkedIn, content | content/ |
| Data tools, scripts | tools/ |
| Client-specific work | clients/[client-name]/ |
```

> **Speaker notes:** Routing matters because Claude will create files. Without routing instructions it guesses — and it'll guess wrong half the time. This table costs you five minutes to write and saves you from hunting down misplaced files indefinitely. Every new workspace, write the routing table first.

---

## Slide 2.6 — The rules system

**Visual:** File tree showing `.claude/rules/` with 7 files listed.

```
.claude/rules/
├── ask-vs-act.md
├── workflow.md
├── file-conventions.md
├── scope-before-execute.md
├── context-and-tools.md
├── archive-safety.md
└── prompt-library.md
```

> **Speaker notes:** Rules are behavioral constraints that load alongside CLAUDE.md. Think of them as the employee handbook. The ones that matter most for GTM work are ask-vs-act and scope-before-execute. Ask-vs-act defines when Claude should just do the thing vs. when it should stop and confirm. Scope-before-execute stops it from charging ahead on the wrong branch or the wrong client. All seven are in the repo.

---

## Slide 2.7 — Live: ask-vs-act rule

**Visual:** Split screen — left: the rule file content. Right: Claude Code session showing it actually applying the rule.

```markdown
# Ask vs Act
Default to action. Only ask when the answer genuinely
changes what you build.

## ASK (design decisions)
- Scope is ambiguous and wrong direction wastes significant work
- Destructive or irreversible action

## ACT (operational steps)
- The user just told you to build/create/implement — start
- The next step is obvious from context — do it
```

> **Speaker notes:** I'm going to show you this rule firing live. Watch what happens when I give a vague instruction — it doesn't ask a checklist of questions, it states assumptions and moves. That behavior comes entirely from this rule file. Without it, you'd spend the first two minutes of every task answering clarifying questions.

---

## Slide 2.8 — Chapter close + open loop

**Visual:** Chapter summary. One planted loop highlighted.

> **Speaker notes:** Foundation is set. CLAUDE.md is your brief, rules are your constraints, and your workspace has a map. The next chapter is where it gets interesting — skills. Skills are the reason this system compounds. Every hour you spend writing a good skill gets paid back every time that skill runs. We're going to build two of them live.

---

---

# CHAPTER 3 — SKILLS: SOPs THAT RUN FOREVER

---

## Slide 3.1 — The claim

**Visual:** Single bold line: "Your best SDR's playbook, encoded in 40 lines. Runs without them."

> **Speaker notes:** A skill file is a constraint system. Not a tutorial, not a template — a constraint. It tells Claude exactly what inputs to expect, what format to output, what the failure modes are, and most importantly, what the insider knowledge is. That last section is where two years of campaign learning lives.

---

## Slide 3.2 — What a skill IS

**Visual:** SKILL.md structure diagram — 5 sections labeled.

```
skills/cold-email/
└── SKILL.md
    ├── ## Define     ← what this skill produces
    ├── ## Uses       ← when to call it
    ├── ## Insider Knowledge  ← the moat
    ├── ## Format     ← exact output structure
    └── ## Quality Gates  ← what makes an output bad
```

> **Speaker notes:** The folder structure matters. Every skill lives in its own folder so you can add scripts, examples, and reference docs alongside it. The SKILL.md itself has five sections. Most people write the first two and stop. The insider knowledge section and quality gates are where the actual leverage is — and they're the sections that take experience to write well.

---

## Slide 3.3 — The insider knowledge section

**Visual:** Code block showing insider knowledge from cold-email skill.

```markdown
## Insider Knowledge

- Subject lines under 6 words outperform longer ones for this ICP
- Never open with "I" — open with them
- Step 2 should reframe, not follow up
- Use single-brace variables: {FIRST_NAME}, {COMPANY}, {PAIN_POINT}
- No links. No attachments. One CTA max.
```

> **Speaker notes:** This section is what makes your skill different from a generic prompt. Anyone can write "write me a cold email." The insider knowledge section encodes what you've learned from running hundreds of campaigns — what actually works for your specific ICP. When you hire a new person, you onboard them. This is how you onboard Claude to your campaigns.

---

## Slide 3.4 — Live: Build cold-email skill from scratch

**Visual:** Screen recording — VS Code, building SKILL.md file section by section.

> **Speaker notes:** [LIVE SEGMENT — no scripted notes. Build each section, explain as you go. Show what a bad output looks like before adding the quality gates. Show what a good output looks like after. Keep the pace fast — this should take 12-15 minutes max.]

---

## Slide 3.5 — Live: Run it on a real company

**Visual:** Claude Code terminal — running the cold-email skill against a real company.

> **Speaker notes:** [LIVE SEGMENT — take one of the research outputs from the ICP research skill, feed it into cold-email. Show the output. Then show what happens when you haven't filled in the insider knowledge section yet — the output is generic. Then show it with the section filled in. That contrast is the point.]

---

## Slide 3.6 — The quality gates section

**Visual:** Code block.

```markdown
## Quality Gates

- No double-dash or em-dash in output
- No "I hope this finds you well" or equivalent
- Subject line: not a question, not clickbait
- Body: under 100 words for step 1, under 80 for step 2
```

> **Speaker notes:** Quality gates are the automated QA layer. Every time this skill runs, these constraints fire. You write them once from your list of "things I've had to manually fix." After 10 outputs you'll know exactly what gates to add. Before you've seen failure modes, you can't write them — that's why you run the skill 10 times before you consider it done.

---

## Slide 3.7 — The workflow rule trigger

**Visual:** Excerpt from workflow.md rule — the guardrail trigger table.

```markdown
| Trigger situation | Skill to invoke |
|------------------|-----------------|
| Code edit / refactor / new file | engineering-discipline |
| API error / raw content pasted | task-discipline |
| Any work under clients/ | client-discipline |
```

> **Speaker notes:** Rules can also trigger skills. This table in workflow.md tells Claude: after a code edit, invoke the engineering-discipline skill. After touching a client folder, invoke client-discipline. It's a progressive disclosure system — you don't load all the constraints all the time, you load the ones relevant to what you're doing. This keeps context lean and the system fast.

---

## Slide 3.8 — Chapter close

**Visual:** Summary — skills built, skills in repo.

> **Speaker notes:** Skills are the compound interest of this system. You spend 30 minutes writing a good skill, and it runs correctly every time for the rest of your agency's life. The ICP research and cold-email skills are in the repo. Fork them, fill in your insider knowledge, and they become your skills. Next chapter: agents. That's how you run 10 skills at once.

---

---

# CHAPTER 4 — AGENTS: ONE OPERATOR, AGENCY OUTPUT

---

## Slide 4.1 — The claim

**Visual:** Simple equation: "1 operator + agents = agency-level throughput"

> **Speaker notes:** An agent is an isolated worker you spawn. It has its own context window, its own tool access, and it runs independently. While you're in one conversation, three agents can be researching three different companies simultaneously. That's not a demo feature — that's how I run research across 11 client campaigns without a research team.

---

## Slide 4.2 — Skills vs Agents

**Visual:** Two-column comparison.

| Skills | Agents |
|--------|--------|
| SOPs — what to do | Workers — who does it |
| Called with a task | Spawned with a mission |
| Constrain output format | Constrain model and tools |
| Run in your session | Run independently |

> **Speaker notes:** The mental model: skills are playbooks, agents are the people who run them. You can run a skill yourself or you can spawn an agent to run it. You spawn an agent when the task would burn too much of your main context to do yourself — multi-file research, long enrichment runs, anything where you need parallel execution.

---

## Slide 4.3 — The three agents in the repo

**Visual:** Three agent cards with model, purpose, and when to use.

```
smart-searcher    [Haiku]   Discovery — always spawn first
task-orchestrator [Sonnet]  Route complex multi-step tasks
researcher        [Sonnet]  Company + market research, synthesis
```

> **Speaker notes:** Three agents cover 90% of GTM work. Smart-searcher is Haiku — it costs almost nothing and finds whatever file or skill you need before you waste expensive model time. Task-orchestrator routes complex jobs and picks the right agent for each piece. Researcher does the deep company work — reads websites, pulls signals, synthesizes into a structured brief.

---

## Slide 4.4 — The spawn pattern

**Visual:** Two code blocks side by side — wrong vs right.

```
WRONG:
Main reads files → understands → edits → reports
(burns 2,000+ tokens on discovery)

RIGHT:
Main spawns researcher("research Acme Corp")
→ researcher reads/edits
→ Main gets 200-token summary
```

> **Speaker notes:** This pattern is the single biggest context efficiency in the system. Every token your main session uses on file-reading is a token not available for actual work. Spawn cheap agents for discovery, get back a summary, proceed. Your main session stays clean. I've been running sessions for 4-6 hours on complex campaigns without hitting context limits because of this pattern.

---

## Slide 4.5 — Live: Three agents in parallel

**Visual:** Screen — three agent spawns running simultaneously, showing research output arriving from each.

> **Speaker notes:** [LIVE SEGMENT — spawn researcher on three different companies. While they run, explain what each one is doing. When results come back, show how the main session synthesizes them into a single campaign brief. Timing matters here — show the clock. Three companies researched in the time it would take to do one manually.]

---

## Slide 4.6 — The knowledge graph

**Visual:** KG architecture diagram — entities.jsonl → SKILLS.md catalog → kg-query.js.

```bash
# Find everything related to "cold email"
bun knowledge-graph/scripts/kg-query.js search "cold email"

# Find skills for a task
bun knowledge-graph/scripts/kg-skill-graph.js --query "write outbound sequence"
```

> **Speaker notes:** The knowledge graph is what makes the system self-aware. Instead of telling Claude where everything is in every session, you index your workspace once and query it. Smart-searcher uses this first before globbing files. As your skill library grows past 20 skills, this becomes essential — you can't hold the map in your head, so the system holds it for you.

---

## Slide 4.7 — Chapter close

**Visual:** Agent roster summary.

> **Speaker notes:** Three agents, one pattern. Always spawn smart-searcher first for discovery, task-orchestrator for complex routing, researcher for deep company work. The pattern: spawn, not read. Next chapter is the enrichment waterfall — where agents and skills combine into a pipeline that runs end-to-end.

---

---

# CHAPTER 5 — THE ENRICHMENT WATERFALL

---

## Slide 5.1 — The Clay problem

**Visual:** Clay pricing screenshot (or representative numbers). Monthly cost at scale.

> **Speaker notes:** Clay is a great product. I'm not saying it isn't. But when you're running 11 client campaigns and each one has a 1,000-lead list, you're paying for enrichment on 11,000 records a month. A lot of that enrichment is stuff you can get for free — company website data, LinkedIn signals, tech stack detection. The waterfall is how you get that for almost nothing.

---

## Slide 5.2 — The waterfall concept

**Visual:** Waterfall flow diagram — three tiers.

```
Tier 1: Free sources
  ↓ (miss) 
Tier 2: Cheap APIs ($0.002/query)
  ↓ (miss)
Tier 3: Paid fallbacks (Clay, FullEnrich)
  ↓
Enriched record
```

> **Speaker notes:** The waterfall only goes down when the tier above it fails. Most records get enriched in Tier 1 or Tier 2 — you only hit paid APIs for the harder cases. In practice that means 70-80% of your enrichment runs at near-zero cost. The paid tier exists for edge cases, not as the default.

---

## Slide 5.3 — Tier 1: Free sources

**Visual:** Source list with what each returns.

| Source | Data returned | Cost |
|--------|--------------|------|
| Company website | Description, ICP signals, tech mentions | Free |
| LinkedIn company page | Headcount, recent hires, job postings | Free (rate limits) |
| Google AI Mode | Summaries, news, recent events | $0.002/query |
| Crunchbase (public) | Funding, founding date | Free |

> **Speaker notes:** The company website alone gets you 60% of what you need for personalization — what they do, how they position it, what pain points they surface publicly. LinkedIn gets you the headcount signal and job postings, which tell you whether they're actively investing in the function you're selling into. Together, these two sources cover most of your list.

---

## Slide 5.4 — Tier 2: TechSight

**Visual:** TechSight CLI demo — terminal showing tech stack detection output.

```bash
techsight acmecorp.com
# → Salesforce, HubSpot, Outreach, Chrome extensions...
```

> **Speaker notes:** TechSight is a free CLI that detects tech stack from a domain. We built it in-house and it's open source — link in the repo. For GTM work, tech stack is one of the most valuable enrichment signals. If they're using Salesforce but no outreach tool, that's a gap. If they're on HubSpot with no sequences, that's a gap. TechSight runs at zero cost and hits on 80% of domains.

---

## Slide 5.5 — Tier 3: Paid fallbacks

**Visual:** API cost comparison table.

| Tool | Cost | Use case |
|------|------|---------|
| Clay | $X/credit | Complex signal workflows |
| OpenWebNinja | $0.002/query | AI-mode search results |
| FullEnrich | $Y/record | Contact data completion |

> **Speaker notes:** Tier 3 only fires on misses. If you've gotten what you need from Tier 1 and 2, you don't call Tier 3. For records where the website is thin and LinkedIn is sparse — usually smaller companies, early-stage startups — that's when you hit the paid APIs. The script handles the fallback logic automatically.

---

## Slide 5.6 — Cost comparison

**Visual:** Side-by-side table — Clay-only vs waterfall for 1,000 records.

| | Clay-only | Waterfall |
|--|---------|---------|
| 1,000 records | $X | ~$Y |
| Enrichment fields | Standard | Custom |
| Ownership | Platform-dependent | Yours forever |

> **Speaker notes:** [Use real numbers here from your actual Clay spend vs. waterfall runs. The ownership line is the sleeper argument — once you've built the waterfall, you own the logic. You're not dependent on Clay changing their pricing or their data sources. That's an infrastructure argument, not a cost argument.]

---

## Slide 5.7 — Live: Waterfall on real companies

**Visual:** Screen — running the enrichment script on 5 companies, showing output.

> **Speaker notes:** [LIVE SEGMENT — run enrich.js from the repo on 5 real companies. Show which tier each one hits. Show the structured output. Show one record where Tier 1 and 2 miss and Tier 3 fires. Keep commentary minimal — let the output speak.]

---

## Slide 5.8 — Chapter close + Chapter 6 tease

**Visual:** Loop callout: "That's the infrastructure. Chapter 6 is where it runs."

> **Speaker notes:** Waterfall is live. Chapter 6 is where all of this comes together — CLAUDE.md, rules, skills, agents, waterfall — on a company I've never researched, with a timer running. No prep, no safety net. That's next.

---

---

# CHAPTER 6 — THE LIVE GTM BUILD

---

## Slide 6.1 — Cold start declaration

**Visual:** Single slide. Timer visible. Company domain shown for the first time.

"Starting now. [domain]. Never looked at this company before."

> **Speaker notes:** No setup. Everything we've built in chapters 1-5 is already in place. I'm going to research this company, qualify the ICP fit, run enrichment, write a two-email sequence, upload to Bison, and launch a campaign. Timer is running. I'll narrate what I'm doing and why as I go.

[SWITCH TO FULL SCREEN — 50 MINUTES LIVE]

Sequence:
1. Spawn researcher agent on the company
2. Run ICP research skill against the output
3. Run enrichment waterfall
4. Generate cold-email Step 1 + Step 2 from research
5. QA against quality gates
6. Upload to Bison via CLI
7. Set campaign live

---

## Slide 6.2 — Post-build debrief

**Visual:** Timer result. Summary of what was built.

> **Speaker notes:** That's the system. Research to live campaign in [X] minutes. The before/ and after/ folders in the repo show exactly what changed — you can diff them if you want to see the full state. Next chapter is the business layer — what this does to your cost of delivery and how to talk about it with clients.

---

---

# CHAPTER 7 — THE BUSINESS LAYER

---

## Slide 7.1 — The claim

**Visual:** Single bold line: "This isn't a productivity hack. It's a cost-of-delivery restructure."

> **Speaker notes:** Every chapter before this was about building the system. This chapter is about what the system is worth commercially. Not as a tool you sell — as infrastructure that changes your margin. There are two audiences for this chapter: operators who want to understand their own economics, and anyone who needs to make a business case to leadership or a client.

---

## Slide 7.2 — Traditional agency headcount model

**Visual:** Org chart. 10 clients, 6-8 SDRs, 1-2 managers.

| Role | Count | Monthly cost |
|------|-------|-------------|
| SDR | 6-8 | $X each |
| Manager | 1-2 | $Y each |
| Tools (Clay, N8n, etc.) | — | $Z/month |
| **Total** | | **$$$** |

> **Speaker notes:** This is what a traditional 10-client GTM agency looks like on the cost side. Six to eight SDRs handling list building, enrichment, sequence writing, and campaign management. One or two managers. Plus tool costs. That's your cost of delivery. That's what you're comparing against.

---

## Slide 7.3 — The operator model

**Visual:** Same format but restructured.

| Role | Count | Monthly cost |
|------|-------|-------------|
| Operator | 2 | $X each |
| Claude Code | — | $20/month |
| Bison | — | $Y/month |
| Data sources | — | $Z/month |
| **Total** | | **$$ (less)** |

**Clients served: 12. Output per campaign: higher.**

> **Speaker notes:** Two operators running this system can service 12 clients. I'm not estimating — that's what we're doing at LeadGrow right now. The output per campaign is higher because the research is deeper and the personalization isn't bottlenecked by SDR bandwidth. Your cost of delivery drops, your capacity goes up, and your margin goes up on both sides.

---

## Slide 7.4 — What clients pay for

**Visual:** Clear separation: "What you use" vs "What you charge for."

```
What you use: Claude Code + skills + agents + waterfall
What you charge for: meetings booked, pipeline generated
```

> **Speaker notes:** Clients don't care what's in your stack. They care about meetings and pipeline. You're not selling "AI-powered outbound" — you're selling a guaranteed number of qualified meetings per month, with a system that can deliver it at a margin your competitors can't match. The tool is internal infrastructure. The output is what gets priced.

---

## Slide 7.5 — Margin restructure

**Visual:** Before/after margin calculation (representative numbers).

| | Before | After |
|--|--------|-------|
| Revenue per client | $X | $X |
| Cost of delivery | $Y | $Y × 0.4 |
| Margin | Z% | Z% × 2+ |

> **Speaker notes:** [Use your real numbers here if you're comfortable. If not, use representative ranges. The point is the multiplier — cost of delivery drops, revenue per client stays the same or goes up because you can deliver more. That's the margin restructure.]

---

## Slide 7.6 — The leadership business case

**Visual:** One-slide version of the argument.

**For internal teams / agencies pitching leadership:**
> "Two operators with this system match the output of a 6-person SDR team at 40% of the cost. Payback period: 90 days."

**For AEs pitching clients:**
> "Our delivery model runs on Claude Code infrastructure. That's why our cost per meeting booked is X% lower than our competitors and our ramp time on new campaigns is two weeks, not six."

> **Speaker notes:** These are the two framings depending on who you're talking to. Internal teams need the headcount math and payback period. Clients need the output comparison and the ramp time. Neither needs to know what Claude Code is. They need to know what the system produces.

---

## Slide 7.7 — CTA + what's next

**Visual:** Repo link large. Three things to do.

1. `git clone github.com/LeadGrowGTM/claude-code-gtm`
2. Start with `chapter-2-foundation/CLAUDE.md.template`
3. Add your insider knowledge to the skill stubs

Also linking:
- Bison CLI: `github.com/LeadGrowGTM/bison-cli`
- TechSight: [link]
- GSD Plugin: [link]

> **Speaker notes:** Clone the repo, start with the CLAUDE.md template, and fill in your insider knowledge in the skill stubs. Those three steps get you from zero to a working system. The bison-cli repo is linked if you're using Bison. TechSight is free and the link's in the tools folder. If you build something with this, share it — I read everything. Links in the description.

---

---

# BONUS — SALES CALL PREP (Hormozi loop close)

---

## Slide B.1 — Encoding sales training into a skill

**Visual:** Hormozi content on left, sales-call-prep skill on right.

> **Speaker notes:** Earlier I said I'd show you how to take any sales training and encode it into a skill that makes you better on calls. Here's that. The sales-call-prep skill in the repo takes a training source — could be a Hormozi transcript, your own Fireflies call recordings, SPIN Selling notes — and a prospect brief, and returns a pre-call sheet. Objections, discovery questions, opening move, close target. Takes 15 minutes to build. Runs in 30 seconds before every call.

---

## Slide B.2 — Live: Load Hormozi, prep for a discovery call

**Visual:** Screen — loading sales training content, running the skill against a prospect.

> **Speaker notes:** [LIVE SEGMENT — paste in training content, show the skill running, show the output. Keep this tight — 8-10 minutes. The point is demonstrating that skills aren't just for campaigns. Any repeatable expert task gets a skill file.]

---

*END OF DECK*

---

## PRODUCTION NOTES

- **Chapter 6 pacing:** Don't rush. Let silence sit when the agent is thinking. The audience needs to see it's real.
- **Code slides:** Use a dark theme. Font size 18+ so it reads on compressed video.
- **Live segments:** No re-takes on Chapter 6. Everything else can be edited.
- **Timestamps:** Add final timestamps after recording, not before.
- **Repo link:** Pin it to the first comment. Add it to the description. Reference it at least once per chapter.
