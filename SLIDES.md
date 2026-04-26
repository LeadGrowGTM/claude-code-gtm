# Claude Code for GTM Operators
## Full Slide Deck + Speaker Notes

**Course:** Claude Code for GTM Operators
**Audience:** Agency operators, GTM engineers, AEs running campaigns at scale
**Format:** Each slide = one clean idea + storyboard (visual direction) + speaker notes
**Companion repo:** github.com/LeadGrowGTM/claude-code-gtm

---

# INTRO

---

## Slide 0.1 — Title

**Storyboard:** Black background. Full-width white text: "Claude Code for GTM Operators." Below it, in smaller gray: "The system behind agency-grade outbound." Bottom-right corner, monospace: `github.com/LeadGrowGTM/claude-code-gtm`. Nothing else on screen. No gradients, no logos, no animation. Silence before speaking.

> **Speaker notes:** No intro. Just start. If you're watching this you already know what Claude Code is and you want to see it applied to real outbound work. That's what this is. Everything I show you here is running in production across 11 client campaigns right now.

---

## Slide 0.2 — Three things you will leave with

**Storyboard:** Dark background. Three numbered items reveal one at a time as you speak. Large numerals (1, 2, 3) in a muted accent color — not icons, not bullets. Each item is a single line of white text. No header. The list feels like a commitment, not a menu.

1. A working Claude Code GTM infrastructure
2. A companion repo — clone it once, adapt it forever
3. The headcount math to justify this to a client or your leadership

> **Speaker notes:** This isn't a tutorial. By the end you'll have the actual files — CLAUDE.md template, skills, agents, the enrichment waterfall script. Clone the repo now if you want to follow along. Link is on screen and in the description.

---

## Slide 0.3 — Four loops planted

**Storyboard:** Four horizontal cards, slightly staggered, on a dark background. Each card has a chapter number top-left and a single-line hook in quotes — large enough to read at a glance. The cards look like pinned notes or open loops. No timestamps yet (add in post). The visual says: "these are promises I'm going to keep." The fourth card (bonus) is slightly smaller or set apart visually — it's the cherry on top, not a core chapter.

- **Ch. 6:** "Cold company. No prep. Live campaign in under an hour."
- **Ch. 5:** "The enrichment waterfall that replaced most of our Clay spend."
- **Ch. 7:** "The headcount math. Two operators vs. six SDRs."
- **Bonus:** "If you do sales calls — stay for the last segment."

> **Speaker notes:** Four things I want you watching for. Chapter 6 is the main event — I pick a company I've never touched, and we go from zero to a live campaign in under an hour. Timer on screen. No edits. Chapter 5 is the cost story. Chapter 7 is the business case. And I'm closing the whole thing with something that's not about outbound at all — if you do sales calls, that last segment is worth staying for.

---

## Slide 0.4 — Chapter map

**Storyboard:** A horizontal timeline of seven chapters rendered as connected chevrons or sequential blocks. Chapter number and title on top, time estimate below each. The block for Chapter 6 is slightly larger or accented — it's the main event and the viewer should feel that. The rest of the chapters read as build-up to it.

| Chapter | Title | Time |
|---------|-------|------|
| 1 | The Stack Replacement Thesis | 15 min |
| 2 | Foundation: CLAUDE.md | 20 min |
| 3 | Skills: SOPs That Run Forever | 35 min |
| 4 | Agents: Headcount Leverage | 25 min |
| 5 | The Enrichment Waterfall | 30 min |
| **6** | **The Live GTM Build** | **50 min** |
| 7 | The Business Layer | 20 min |

> **Speaker notes:** The chapters build on each other — skip one and you'll feel it. Specifically: Chapter 3 (skills) is what makes the live build in Chapter 6 readable. If you jump straight to Chapter 6 without Chapter 3, you're watching a demo, not a blueprint. If you're already running Claude Code and want the cost argument, Chapter 5 and 7 are standalone. Everything else, watch in order. Here's where we're going — start with the thesis.

---

---

# CHAPTER 1 — THE STACK REPLACEMENT THESIS

---

## Slide 1.1 — Your current stack

**Storyboard:** Three tool logos side by side (Clay, N8n, Smartlead) in the center of a dark slide. Below them, a running dollar-sign total accumulates as you speak — or a static line: "$X/month + 3 context switches per task." The logos look like a familiar setup — the viewer nods. This is their current life.

> **Speaker notes:** If you're running a GTM agency right now you're probably paying for Clay, something like N8n or Make, and a sending platform. That stack works. I'm not going to tell you to rip it out. But I will show you where it breaks down and what you can replace.

---

## Slide 1.2 — What gets replaced

**Storyboard:** A clean list on a dark background. Each item appears with a red strikethrough drawn through it — no X icons, just the line. The strikethrough should feel decisive, not aggressive. The point isn't that these tools are bad — it's that these specific jobs no longer require them.

- ~~Zapier / basic automation logic~~
- ~~Clay for standard enrichment (website scrape, LinkedIn, tech stack)~~
- ~~Manual personalization workflows~~

> **Speaker notes:** Zapier is gone if you're serious about this. Clay's enrichment — specifically the stuff you can get from a company website, LinkedIn, and a tech stack tool — that's now a script you run once and own forever. Personalization at scale doesn't need a $800/month tool when you have a skill file that runs it on demand.

---

## Slide 1.3 — What survives

**Storyboard:** Same list format as 1.2, but green checkmarks instead of strikethroughs. The visual rhythm is intentional — same format, opposite signal. The viewer is calibrating. The message: this isn't a scorched-earth replacement, it's a surgical one.

- Apollo / data sources (you still need leads)
- Bison / Smartlead / Instantly (sending infra)
- Clay for complex signal-based workflows

> **Speaker notes:** Data sources survive. You still need Apollo or whatever list source you use — Claude Code doesn't generate leads out of thin air. Sending infra survives — Bison, Smartlead, Instantly. And Clay survives for genuinely complex signal-based workflows where you need its native integrations. Everything else is on the table.

---

## Slide 1.4 — What gets multiplied

**Storyboard:** Three items, each with a bold "10x" badge rendered like a multiplier chip or a price tag sticker in the corner — slightly tilted for energy. The items themselves are plain white text. The visual question it poses: "what's actually bottlenecking your output right now?" The answer is on screen.

- Research depth per company — **10x**
- Personalization quality per email — **10x**
- Workflow composition speed — **10x**

> **Speaker notes:** Research depth is the biggest one. What used to take an SDR 20 minutes per company — reading the website, pulling their recent news, checking job postings — now takes 45 seconds. Personalization quality goes up because you're working from actual research, not a template. And composing new workflows — building new sequences, new ICP angles — drops from days to hours.

---

## Slide 1.5 — The 4-layer architecture

**Storyboard:** A vertical stack of four clearly separated layers, each a distinct color block. The top layer (CLAUDE.md) is the widest and most prominent — it sits over everything. Below it, Rules, Skills, Agents stack in descending order. Each layer has its name on the left and a one-line description on the right. The diagram reads top-to-bottom: "this is the whole system." Let it sit on screen for a full 3 seconds before speaking — viewers need to map it.

```
┌─────────────────────────────────────────┐
│  CLAUDE.md         ← Operator brief     │  ← Loads every session
├─────────────────────────────────────────┤
│  Rules             ← Constraints        │  ← Prevent failures
├─────────────────────────────────────────┤
│  Skills            ← SOPs               │  ← Run forever
├─────────────────────────────────────────┤
│  Agents            ← Workers            │  ← Execute in parallel
└─────────────────────────────────────────┘
```

> **Speaker notes:** [Pause 3 seconds. Let the viewer read it.] This is the whole system in one diagram. CLAUDE.md at the top — loads every session, sets the operating mode. Rules below it — prevent the failure modes that cost you time on campaign work. Skills below that — your encoded SOPs, running correctly without re-prompting. Agents at the bottom — the workers who execute everything in parallel. Every chapter covers one layer. By chapter 5 you'll have all four running together. Before I go deep on each one — let me show you what this looks like running right now. [BRIEF LIVE MOMENT — open the terminal, show CLAUDE.md loading in a session, close. 60 seconds max. Proof before explanation.]

---

## Slide 1.6 — Clone the repo now

**Storyboard:** A dark terminal window centered on screen. A single command types out character by character: `git clone github.com/LeadGrowGTM/claude-code-gtm`. Nothing else. The typing animation is the visual. The viewer should feel a pull to pause the video and do it right now.

```bash
git clone github.com/LeadGrowGTM/claude-code-gtm
```

> **Speaker notes:** Clone the repo now. The companion repo mirrors the course chapter by chapter. Each folder has a README telling you what you're building and what the end state looks like. Chapter 6 has a before/ and after/ folder — diff them and you'll see exactly what 50 minutes with this system produces. One more thing: the repo also includes the knowledge graph scripts — `kg-query.js`, `kg-index.js`. Run the indexer once and the system can find its own skills from that point forward. That becomes useful as your library grows past 20 skills. Details in the tools/ folder. Chapter 2 is where you build the foundation — the document that loads at the start of every session.

---

---

# CHAPTER 2 — FOUNDATION: CLAUDE.md AS AN OPERATOR BRIEF

---

## Slide 2.1 — The claim

**Storyboard:** Single sentence, centered, large white type on black. No other elements. Two-line break for emphasis: "CLAUDE.md isn't a config file." — pause — "It's a permanent team member brief." The slide should feel like a provocation, not a definition. Let it sit.

> **Speaker notes:** Every new Claude Code session reads CLAUDE.md first. That makes it the most important document in your workspace. Most people treat it like a README — a few lines about what the project does. That's wrong. Write it like you're onboarding someone who will never forget what you write, never get tired, and reads it fresh every single time they start work.

---

## Slide 2.2 — The five sections

**Storyboard:** A dark terminal code block showing the five section headers in monospace. Each header is on its own line with a short description after the dash. They appear together, not one at a time — the viewer should scan them like a table of contents, not read them linearly. The visual question: "do you have all five?"

```
## Identity        — who Claude is in this context
## Workflow Style  — how to handle execution (ask vs act)
## Repos           — what directories exist and what they're for
## Work Routing    — where different types of work go
## Skill Discovery — how to find relevant skills
```

> **Speaker notes:** Five sections. Identity sets the operating mode — is this a cofounder? A meticulous analyst? An SDR? Workflow style is where you put execution preferences. Repos is the map of your workspace. Work routing tells it where to put different types of output. Skill discovery tells it how to find its own tools. That last one matters more as your skill library grows.

---

## Slide 2.3 — Identity: stop the filler

**Storyboard:** Syntax-highlighted code block on dark background. The four bullet lines inside "Core behaviors" are the focal point — slightly brighter or the surrounding text slightly dimmed. The viewer should be reading those four lines. Each one is a failure mode being closed. This isn't poetry — it's a behavioral spec.

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

## Slide 2.4 — Workflow style: kill the check-ins

**Storyboard:** A small code block, centered, with a single key sentence highlighted or underscored: "Execute the plan, show results, and only pause if something fails." The surrounding text is present for context but the highlighted line is what the viewer takes away. This is the sentence that changes the working rhythm.

```markdown
## Workflow Style

Don't ask for confirmation on every step during multi-step workflows.
Execute the plan, show results, and only pause if something fails
or is genuinely ambiguous.
```

> **Speaker notes:** This is the line that changes the most about how you work. Without it, Claude asks "should I proceed?" after every step. With it, you give a task and come back to results. For GTM work — building a campaign, running enrichment, writing a sequence — you want the latter. The default behavior is cautious. You're opting out of caution.

---

## Slide 2.5 — Work routing: tell it where things go

**Storyboard:** A clean markdown table on dark background. Two columns: "Work Type" and "Destination." The destinations are in monospace — they look like real file paths because they are. The viewer realizes: every time Claude creates a file, it checks this table first. The visual communicates a system that knows where everything belongs.

```markdown
## Work Routing

| Work Type                | Destination             |
|--------------------------|-------------------------|
| Cold email, campaigns    | campaigns/              |
| ICP, voice, messaging    | company/                |
| LinkedIn, content        | content/                |
| Data tools, scripts      | tools/                  |
| Client-specific work     | clients/[client-name]/  |
```

> **Speaker notes:** Routing matters because Claude will create files. Without routing instructions it guesses — and it'll guess wrong half the time. This table costs you five minutes to write and saves you from hunting down misplaced files indefinitely. Every new workspace, write the routing table first.

---

## Slide 2.6 — Rules: the two that matter for GTM

**Storyboard:** A dark terminal showing a file tree: `.claude/rules/` with seven files beneath it, but two are visually highlighted or marked — `ask-vs-act.md` and `scope-before-execute.md`. The other five are dimmed or smaller. The visual says: there are seven, and two of them run your daily workflow. Start here.

```
.claude/rules/
├── ask-vs-act.md          ← start here
├── scope-before-execute.md ← start here
├── workflow.md
├── file-conventions.md
├── context-and-tools.md
├── archive-safety.md
└── prompt-library.md
```

> **Speaker notes:** Seven rules in the repo. You don't need all seven on day one. The two that change your daily work immediately are ask-vs-act and scope-before-execute. Ask-vs-act defines when Claude should just do the thing vs. when it should stop and confirm — without it, you're answering confirmation questions every two minutes. Scope-before-execute stops it from charging ahead on the wrong client folder or the wrong branch. Add the others as you hit the problems they solve. Before I show you ask-vs-act firing in a session — let me show you what happens without it.

---

## Slide 2.6b — Without the rule: the confirmation loop

**Storyboard:** A Claude Code terminal screenshot or short screen recording showing the failure mode — Claude asking "Should I proceed?" after every step of a simple task. Three confirmation requests in a row before any actual output. The visual is intentionally tedious to look at. The viewer feels the friction before the fix.

```
User: Build a cold email sequence for Acme Corp.

Claude: I'll start by researching Acme Corp. Should I proceed?
User: Yes.
Claude: Research complete. Should I now run the ICP research skill?
User: Yes.
Claude: ICP score is 18/25. Should I write the sequence?
User: Yes.
...
```

> **Speaker notes:** This is the default. Every step, a confirmation request. For a five-step task that takes 20 minutes, you're answering questions for the first 10 of them. The ask-vs-act rule closes this in six lines of markdown. Watch what changes.

---

## Slide 2.7 — Rules in action: ask-vs-act

**Storyboard:** Split screen. Left side: the ask-vs-act rule file, highlighted cleanly. Right side: a Claude Code terminal session where the rule is visibly firing — Claude states assumptions and proceeds instead of asking a confirmation question. The left side explains the rule; the right side proves it works. The split should be 40/60 left/right so the session output has more room.

```markdown
# Ask vs Act
Default to action. Only ask when the answer genuinely
changes what you build.

ACT (no confirmation needed):
- User said build/create/implement — start
- Next step is obvious from context — do it

ASK (pause first):
- Destructive or irreversible action
- Scope would send you the wrong direction
```

> **Speaker notes:** I'm going to show you this rule firing live. Watch what happens when I give a vague instruction — it doesn't ask a checklist of questions, it states assumptions and moves. That behavior comes entirely from this rule file. Without it, you'd spend the first two minutes of every task answering clarifying questions. With it, you give a direction and come back to a result.

---

## Slide 2.8 — Chapter close

**Storyboard:** Single large text: "Foundation set." Below it in smaller gray: CLAUDE.md / Rules / Workspace map — three items listed like a checklist, all checked. Bottom of the slide: a forward arrow and "Chapter 3: Skills →" in muted text. Clean chapter-close energy. The viewer knows where they stand and what's next.

> **Speaker notes:** Foundation is set. CLAUDE.md is your brief, rules are your constraints, and your workspace has a map. The next chapter is where it gets interesting — skills. Skills are the reason this system compounds. Every hour you spend writing a good skill gets paid back every time that skill runs. We're going to build two of them live.

---

---

# CHAPTER 3 — SKILLS: SOPs THAT RUN FOREVER

---

## Slide 3.1 — The claim

**Storyboard:** Single bold sentence on dark background, centered: "Your best SDR's playbook, encoded in 40 lines. Runs without them." Let it sit for two beats before speaking. The word "forever" isn't on the slide — it should live in the viewer's head as the implication.

> **Speaker notes:** A skill file is a constraint system. Not a tutorial, not a template — a constraint. It tells Claude exactly what inputs to expect, what format to output, what the failure modes are, and most importantly, what the insider knowledge is. That last section is where two years of campaign learning lives.

---

## Slide 3.2 — What a skill looks like

**Storyboard:** A file tree on the left: `skills/cold-email/SKILL.md`. On the right, the SKILL.md structure shown as five labeled sections stacked vertically. Each section name is on a colored left-border block — like a document outline. The key section, "Insider Knowledge," has a slightly brighter border or a subtle highlight. The visual says: there's structure here, and one part of the structure is the real moat.

```
skills/cold-email/
└── SKILL.md
    ├── ## Define              ← what this skill produces
    ├── ## Uses                ← when to call it
    ├── ## Insider Knowledge   ← ← ← the moat
    ├── ## Format              ← exact output structure
    └── ## Quality Gates       ← what makes an output bad
```

> **Speaker notes:** The folder structure matters. Every skill lives in its own folder so you can add scripts, examples, and reference docs alongside it. The SKILL.md itself has five sections. Most people write the first two and stop. The insider knowledge section and quality gates are where the actual leverage is — and they're the sections that take experience to write well.

---

## Slide 3.3 — The insider knowledge section

**Storyboard:** A syntax-highlighted code block. The section heading "## Insider Knowledge" is prominent. Each bullet beneath it is a specific, non-obvious rule — not generic advice. The viewer should read these and think "this is specific to someone who's run a lot of campaigns." The contrast with a generic prompt is implicit.

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

## Slide 3.4 — Live: Build the cold-email skill

**Storyboard:** Full-screen terminal — VS Code with SKILL.md open, building each section from scratch. No slide overlay. The screen is the slide. Keep the font large (18pt minimum). This is a live segment — the pace and narration carry it.

> **Speaker notes:** [LIVE SEGMENT — build each section, explain as you go. Show what a bad output looks like before adding the quality gates. Show what a good output looks like after. The contrast is the point. Keep the pace fast — this should take 12-15 minutes max. Don't read the code aloud line-by-line; talk about what each section is doing and why.]

---

## Slide 3.5 — Live: Run it on a real company

**Storyboard:** Claude Code terminal — the skill invocation and the output. Show the full output on screen, scroll slowly. If possible, annotate live what the insider knowledge section changed. No slide overlay. The output quality speaks for itself.

> **Speaker notes:** [LIVE SEGMENT — take one of the research outputs from the ICP research skill, feed it into cold-email. Show the output. Then show what happens when you haven't filled in the insider knowledge section yet — the output is generic. Then show it with the section filled in. That contrast is the point. Let silence sit while the viewer reads the output.]

---

## Slide 3.6 — Quality gates: automated QA

**Storyboard:** A code block showing the Quality Gates section. Each gate is a single checkable line — they look like a CI checklist. The visual question: "what would you have to manually review otherwise?" The answer is: all of this. These gates replace a review pass.

```markdown
## Quality Gates

- [ ] Subject line: under 8 words, not a question, not clickbait
- [ ] Step 1 body: under 100 words
- [ ] Step 2 body: under 80 words, different angle from Step 1
- [ ] No links or attachments in either step
- [ ] No "I hope this finds you well" or equivalent
- [ ] One CTA max — one question, not a pitch
```

> **Speaker notes:** Quality gates are the automated QA layer. Every time this skill runs, these constraints fire. You write them once from your list of "things I've had to manually fix." After 10 outputs you'll know exactly what gates to add. Before you've seen failure modes, you can't write them — that's why you run the skill 10 times before you consider it done.

---

## Slide 3.7 — Skills trigger based on what you're doing

**Storyboard:** A small table showing three situation → skill triggers. Left column: the situation (slightly dimmer, italicized). Right column: the skill that auto-loads (monospace, bright). Below the table, one concrete example in plain text: "Open a file in clients/ → client-discipline loads automatically." The visual communicates: you don't have to remember which playbook to use — the system loads the right one based on context.

```markdown
| Trigger situation                | Skill that loads        |
|----------------------------------|-------------------------|
| Code edit / refactor / new file  | engineering-discipline  |
| API error / raw content pasted   | task-discipline         |
| Any work under clients/          | client-discipline       |
```

Example: open `clients/acme-corp/sequences/step1.md` → client-discipline loads automatically, pulling client-specific copy standards and campaign rules into context.

> **Speaker notes:** Here's the concrete version: when I open anything inside the clients/ folder, the workflow rule fires and loads client-discipline. That skill contains the copy standards, the QA rules, and the campaign guard-rails for client work. I don't invoke it manually — I just open the file. The rule handles it. This is the progressive disclosure pattern — you don't load all the constraints all the time. You load the ones relevant to what you're doing right now. Keeps context lean, keeps the system fast.

---

## Slide 3.8 — Chapter close

**Storyboard:** A single sentence centered: "Compound interest." Below it in smaller text: "30 minutes to write. Runs correctly forever." Below that, a list of the skills now in the repo. Forward arrow at the bottom: "Chapter 4: Agents →" The viewer should leave this chapter feeling like they've planted something that will pay dividends.

> **Speaker notes:** Skills are the compound interest of this system. You spend 30 minutes writing a good skill, and it runs correctly every time for the rest of your agency's life. The ICP research and cold-email skills are in the repo. Fork them, fill in your insider knowledge, and they become your skills. Right now we've been running one skill at a time. Agents are how you stop doing that — next chapter, we run 10 in parallel.

---

---

# CHAPTER 4 — AGENTS: ONE OPERATOR, AGENCY OUTPUT

---

## Slide 4.1 — The claim

**Storyboard:** A simple equation, centered on dark background, large type: "1 operator + agents = agency-level throughput." No decoration. Let the math land. The viewer should feel the implication: the bottleneck isn't headcount anymore.

> **Speaker notes:** An agent is an isolated worker you spawn. It has its own context window, its own tool access, and it runs independently. While you're in one conversation, three agents can be researching three different companies simultaneously. That's not a demo feature — that's how I run research across 11 client campaigns without a research team. This chapter is also what makes the enrichment waterfall in Chapter 5 viable at scale — without agents coordinating the pipeline, you'd be running it one company at a time.

---

## Slide 4.2 — Skills vs Agents: the mental model

**Storyboard:** Two columns, clearly labeled "Skills" and "Agents." Each column has four rows — the rows are parallel comparisons. The typography should feel like a scorecard. The viewer reads across each row and builds the mental model: one is the playbook, one is the player. No icons, no color beyond contrast.

| Skills | Agents |
|--------|--------|
| SOPs — what to do | Workers — who does it |
| Called with a task | Spawned with a mission |
| Constrain output format | Constrain model and tools |
| Run in your session | Run independently |

> **Speaker notes:** The mental model: skills are playbooks, agents are the people who run them. You can run a skill yourself or you can spawn an agent to run it. You spawn an agent when the task would burn too much of your main context to do yourself — multi-file research, long enrichment runs, anything where you need parallel execution.

---

## Slide 4.3 — The three agents

**Storyboard:** Three horizontal agent cards stacked vertically. Each card has: agent name (large, left), model in brackets (small, muted), and a one-line purpose (right). The "smart-searcher" card is at the top with a subtle indicator — it's always first. The visual reads like an org chart of three people with clearly different roles.

```
smart-searcher    [Haiku]   Discovery — spawn first, always
task-orchestrator [Sonnet]  Route complex multi-step tasks
researcher        [Sonnet]  Company + market research, synthesis
```

> **Speaker notes:** Three agents cover 90% of GTM work. Smart-searcher is Haiku — it costs almost nothing and finds whatever file or skill you need before you waste expensive model time. Task-orchestrator routes complex jobs and picks the right agent for each piece. Researcher does the deep company work — reads websites, pulls signals, synthesizes into a structured brief.

---

## Slide 4.4 — The spawn pattern

**Storyboard:** Two code blocks side by side. Left block labeled "WRONG" in red — shows the main session doing all the work. Right block labeled "RIGHT" in green — shows the main session spawning and receiving a summary. A token count under each: "2,000+ tokens" vs "200 tokens." The visual teaches the pattern through contrast. The numbers tell the whole story.

```
WRONG:
Main reads files → understands → edits → reports
2,000+ tokens on discovery alone

RIGHT:
Main spawns researcher("research Acme Corp")
→ researcher reads and edits
→ Main gets 200-token summary
Main session stays clean
```

> **Speaker notes:** This pattern is the single biggest context efficiency in the system. Every token your main session uses on file-reading is a token not available for actual work. Spawn cheap agents for discovery, get back a summary, proceed. I've been running sessions for 4-6 hours on complex campaigns without hitting context limits because of this pattern. Spawn, don't read.

---

## Slide 4.5 — Live: Three agents in parallel

**Storyboard:** Full-screen Claude Code terminal. Show three spawns happening, then results arriving. No slide overlay. The viewer should see agents running and returning. Narrate the clock — "that's three companies in the time it would take to do one manually."

> **Speaker notes:** [LIVE SEGMENT — spawn researcher on three different companies. While they run, explain what each one is doing. When results come back, show how the main session synthesizes them into a single campaign brief. Timing matters here — show the clock. Three companies researched in the time it would take to do one manually. Don't rush the silence while agents run.]

---

## Slide 4.6 — How smart-searcher finds its tools

**Storyboard:** A flow diagram: smart-searcher spawns → queries knowledge graph → returns the right skill path → main session proceeds. Two terminal lines showing the query and the result. The visual is: smart-searcher isn't guessing — it's querying an index. One idea: the agent knows where things are because the system holds the map.

```bash
# smart-searcher runs this internally before any task
bun knowledge-graph/scripts/kg-skill-graph.js --query "write outbound sequence"
# → skills/cold-email/SKILL.md

# Result: main session loads the right skill, not a generic prompt
```

> **Speaker notes:** Smart-searcher doesn't guess what skill to load — it queries the knowledge graph first. You index your workspace once with kg-index.js, and from that point forward, smart-searcher finds the right skill for any task automatically. Once your library grows past 20 skills, this is what keeps the system coherent — you can't hold the full skill map in your head, so the graph holds it for you. Run the indexer from the repo's knowledge-graph/scripts/ folder. It reindexes in under a minute.

---

## Slide 4.7 — Chapter close

**Storyboard:** Three-row summary. Each row: agent name on left, one-line role on right. Below all three, a single rule in large text: "Spawn, don't read." Forward arrow: "Chapter 5: The Enrichment Waterfall →" The chapter close should feel like a standing operating procedure has just been established.

> **Speaker notes:** Three agents, one pattern. Always spawn smart-searcher first for discovery, task-orchestrator for complex routing, researcher for deep company work. The pattern is simple: spawn, don't read. Chapter 5 is where agents and skills combine into a single pipeline — researcher pulls company data, smart-searcher loads the ICP skill, the waterfall enriches, cold-email writes the sequence. All of it without you switching context. That's next.

---

---

# CHAPTER 5 — THE ENRICHMENT WATERFALL

---

## Slide 5.1 — The Clay problem

**Storyboard:** A stark cost-per-record number, large and centered. Below it, a multiplication: "× 11,000 records/month" — and the result. Nothing else. No logos, no screenshots. The number does the work. The viewer either recognizes this as their life, or as what they're avoiding.

> **Speaker notes:** Clay is a great product. I'm not saying it isn't. But when you're running 11 client campaigns and each one has a 1,000-lead list, you're paying for enrichment on 11,000 records a month. Standard Clay enrichment — website scrape, LinkedIn pull, tech stack — runs somewhere between $0.05 and $0.15 per record depending on your plan and which providers you hit. At 11,000 records, that's $550 to $1,650 a month just for the data layer. And you don't own any of it — if Clay changes pricing or a provider drops out, you start over. The waterfall runs the same enrichment for a fraction of that. Most records at near-zero cost. The math is in slide 5.6. [FILL IN YOUR ACTUAL MONTHLY CLAY SPEND BEFORE RECORDING — use real numbers.]

---

## Slide 5.2 — The waterfall concept

**Storyboard:** A vertical waterfall flow diagram. Three tiers stacked with downward arrows between them. Each tier is a horizontal block: "Tier 1: Free" / "Tier 2: Cheap APIs ($0.002/query)" / "Tier 3: Paid fallback." A downward arrow labeled "(miss)" connects each tier — you only drop to the next tier when the one above fails. At the bottom: "Enriched record." The visual reads: most records stop at Tier 1. The paid tier is the exception.

```
Tier 1: Free sources
  ↓ (only on miss)
Tier 2: Cheap APIs ($0.002/query)
  ↓ (only on miss)
Tier 3: Paid fallbacks
  ↓
Enriched record
```

> **Speaker notes:** The waterfall only goes down when the tier above it fails. Most records get enriched in Tier 1 or Tier 2 — you only hit paid APIs for the harder cases. In practice that means 70-80% of your enrichment runs at near-zero cost. The paid tier exists for edge cases, not as the default.

---

## Slide 5.3 — Tier 1: Free

**Storyboard:** Two columns: "Source" and "What you get from it." Four rows. Clean table on dark background — monospace for the source names, plain text for the returns. The viewer scans this like a checklist. The subtext is: "you could do all of this manually — the waterfall just does it in 45 seconds."

| Source | What it returns |
|--------|----------------|
| Company website | What they do, who they sell to, key claims |
| LinkedIn company page | Headcount, recent hires, job postings |
| Crunchbase (public) | Funding date, round size, investors |
| Google AI Mode | Recent news, announcements, events |

> **Speaker notes:** The company website alone gets you 60% of what you need for personalization — what they do, how they position it, what pain points they surface publicly. LinkedIn gets you the headcount signal and job postings, which tell you whether they're actively investing in the function you're selling into. Together, these two sources cover most of your list at zero cost.

---

## Slide 5.4 — Tier 2: TechSight

**Storyboard:** A dark terminal window centered on screen. The command `techsight acmecorp.com` runs and outputs a clean tech stack list: Salesforce, HubSpot, Outreach, etc. Simple, specific output. The viewer immediately understands the use case — and they understand that this is free.

```bash
$ techsight acmecorp.com

Tech stack detected:
  ✓ Salesforce (CRM)
  ✓ HubSpot (Marketing)
  ✓ Outreach (Sales engagement)
  ✓ Segment (Analytics)
  ✓ Intercom (Support)

Cost: $0.00
```

> **Speaker notes:** TechSight is a free CLI that detects tech stack from a domain. We built it in-house and it's open source — link in the repo. For GTM work, tech stack is one of the most valuable enrichment signals. If they're using Salesforce but no outreach tool, that's a gap. If they're on HubSpot with no sequences, that's a gap. TechSight runs at zero cost and hits on 80% of domains.

---

## Slide 5.5 — Tier 3: When free doesn't cover it

**Storyboard:** A small three-row table: tool name, cost per query, and when it fires. The "When it fires" column tells the story — each row says "on miss from Tier 2." The visual point is that Tier 3 is conditional, not default. A subtle "(edge cases only)" note at the bottom reinforces this.

| Tool | Cost | When it fires |
|------|------|---------------|
| OpenWebNinja | $0.002/query | Website thin, LinkedIn sparse |
| Clay | $X/credit | Complex signal workflows |
| FullEnrich | $Y/record | Contact data completion needed |

> **Speaker notes:** Tier 3 only fires on misses. If you've gotten what you need from Tier 1 and 2, you don't call Tier 3. For records where the website is thin and LinkedIn is sparse — usually smaller companies, early-stage startups — that's when you hit the paid APIs. The script handles the fallback logic automatically. Most of your list never touches this tier.

---

## Slide 5.6 — The cost comparison

**Storyboard:** A side-by-side table with two columns: "Clay-only" and "Waterfall." Three rows: cost per 1,000 records, enrichment ownership, and iteration speed. The numbers should be real (fill in from actual spend). The "Ownership" row is the sleeper argument — colored differently to draw attention. The visual tells the operator: this is a build-vs-rent decision.

| | Clay-only | Waterfall |
|--|---------|---------|
| 1,000 records | $X | ~$Y |
| Data ownership | Platform-dependent | Yours forever |
| Iteration | Change in Clay UI | Change the script |

> **Speaker notes:** Use real numbers from your actual Clay spend vs. waterfall runs. The ownership row is the sleeper argument — once you've built the waterfall, you own the logic. You're not dependent on Clay changing their pricing or their data sources. That's an infrastructure argument, not a cost argument. The script is yours. The data is yours.

---

## Slide 5.7 — Live: Waterfall on real companies

**Storyboard:** Full-screen terminal. Run `enrich.js` on five real domains, show the output for each, and note which tier each one hit. No slide overlay. The tier result for each company is the interesting data — show it clearly.

> **Speaker notes:** [LIVE SEGMENT — run enrich.js from the repo on 5 real companies. Show which tier each one hits. Show the structured output. Show one record where Tier 1 and 2 miss and Tier 3 fires. Keep commentary minimal — let the output speak. Point out the cost column in the output so the viewer sees it accumulating in real time.]

---

## Slide 5.8 — Chapter close + Chapter 6 tease

**Storyboard:** A single horizontal bar across the slide, dividing it. Above the bar: a checklist of what's been built (CLAUDE.md, Rules, Skills, Agents, Waterfall) — all checked. Below the bar, in larger text: "Chapter 6 is where it runs." The visual divides the build from the test. Everything above the line is infrastructure. Below the line is the proof.

> **Speaker notes:** That's the infrastructure layer — complete. CLAUDE.md briefed, rules in place, skills encoded, agents standing by, waterfall running. Chapter 6 is where all of it comes together on a company I've never researched, with a timer running. No prep, no safety net. That's next.

---

---

# CHAPTER 6 — THE LIVE GTM BUILD

---

## Slide 6.1 — Cold start declaration

**Storyboard:** Black screen. A domain appears in the center — large white monospace text. Nothing else. No timer yet, no company logo, no context. Just: `stackbridge.io` (or whatever domain you use). Let it sit for one beat before speaking. The domain appearing is the starting gun.

> **Speaker notes:** This is the company. I've never looked at it before. Everything we've built in chapters 1 through 5 is already in place. Right now I'm going to research this company, qualify ICP fit, run enrichment, write a two-step sequence, upload to Bison, and set a campaign live. Timer starts now.

---

## Slide 6.2 — What you're about to watch

**Storyboard:** A numbered sequence list on dark background — seven steps, each on its own line. The steps appear all at once, not one at a time. A timer in the corner (or noted as "timer visible on screen"). The viewer reads the list and understands the scope of the next 50 minutes. This is the contract being made.

The build sequence:
1. Spawn researcher agent on the company
2. Run ICP research skill against the output
3. Run enrichment waterfall
4. Generate cold-email Step 1 + Step 2 from research
5. QA against quality gates
6. Upload to Bison via CLI
7. Set campaign live

> **Speaker notes:** That's the sequence. No setup, no warm-up. Everything you need to follow along is in the repo — the before/ folder in chapter-6 is the starting state. The after/ folder is what this session produces. If you want to diff them, run: `diff -r chapter-6-live-build/before chapter-6-live-build/after`

[SWITCH TO FULL SCREEN — 50 MINUTES LIVE]

---

## Slide 6.3 — Post-build debrief

**Storyboard:** Two-column result card. Left: "Time elapsed" with the actual timer result in large type. Right: a checklist of everything produced — research doc, ICP score, two-step sequence, Bison upload. Both columns are green/confirmed. The visual is a receipt. It says: this is what 50 minutes with this system produces.

> **Speaker notes:** Research to live campaign in [X] minutes — fill this in with the real time after recording. Before I move on, here's what the session actually produced: one company research doc with ICP score, one two-step email sequence that passed all quality gates, one Bison upload, one live campaign. All from a company I'd never seen before that session. The before/ and after/ folders in the repo show exactly what changed — every file that was created, the full state diff. Diff them and you'll see the whole session output in two minutes. That's the system. The next chapter is about what it's worth commercially — what this does to your cost of delivery, and the two ways to make that case depending on who you're talking to.

---

---

# CHAPTER 7 — THE BUSINESS LAYER

---

## Slide 7.1 — The claim

**Storyboard:** Single bold sentence, centered on black: "This isn't a productivity hack." Line break. "It's a cost-of-delivery restructure." Two sentences, two lines, large type. The word "productivity" should feel almost dismissive — the viewer who's been thinking "AI efficiency tool" needs to recalibrate. Let the slide sit.

> **Speaker notes:** Every chapter before this was about building the system. This chapter is about what the system is worth commercially. Not as a tool you sell — as infrastructure that changes your margin. Two audiences for this chapter: operators who want to understand their own economics, and anyone who needs to make a business case to leadership or a client.

---

## Slide 7.2 — Traditional headcount model

**Storyboard:** A clean cost table on dark background. Roles on the left, headcount in the middle, monthly cost on the right. A bold "Total" row at the bottom with a number that should make the viewer wince slightly. This is the baseline — the thing being compared against. No editorializing, just the math.

| Role | Count | Monthly cost |
|------|-------|-------------|
| SDR | 6-8 | $X each |
| Manager | 1-2 | $Y each |
| Tools (Clay, N8n, etc.) | — | $Z/month |
| **Total** | | **$$$** |

> **Speaker notes:** This is what a traditional 10-client GTM agency looks like on the cost side. Six to eight SDRs handling list building, enrichment, sequence writing, and campaign management. One or two managers. Plus tool costs. That's your cost of delivery. That's what you're comparing against. Fill in real numbers from your market if you have them.

---

## Slide 7.3 — The operator model

**Storyboard:** Same table format as 7.2 — same columns, same structure. But now the headcount is 2, the tool costs are dramatically lower, and the total is a fraction of the previous slide. Below the table: "Clients served: 12. Output per campaign: higher." The visual contrast between 7.2 and 7.3 is the argument. Same format, different numbers.

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

**Storyboard:** Two lines, separated by a horizontal rule in the center of the slide. Above: "What you use: Claude Code + skills + agents + waterfall" in smaller, dimmer text. Below: "What you charge for: meetings booked. Pipeline generated." in larger, brighter text. The visual hierarchy says: the tool is invisible. The output is what's priced.

```
What you use:
  Claude Code + skills + agents + waterfall

─────────────────────────────────────────

What you charge for:
  Meetings booked. Pipeline generated.
```

> **Speaker notes:** Clients don't care what's in your stack. They care about meetings and pipeline. You're not selling "AI-powered outbound" — you're selling a guaranteed number of qualified meetings per month, with a system that can deliver it at a margin your competitors can't match. The tool is internal infrastructure. The output is what gets priced. Never lead with the tech in a client conversation.

---

## Slide 7.5 — The margin restructure

**Storyboard:** A before/after table with three rows: Revenue per client, Cost of delivery, and Margin. The "Before" column shows a baseline margin. The "After" column shows cost of delivery dropping significantly and margin expanding. Use real numbers if comfortable; representative ranges otherwise. The margin row should be the focal point — highlight it or bold it.

| | Before | After |
|--|--------|-------|
| Revenue per client | $X/mo | $X/mo |
| Cost of delivery | $Y/mo | $Y × 0.4/mo |
| **Margin** | **Z%** | **Z% × 2+** |

> **Speaker notes:** Use your real numbers here if you're comfortable sharing them. If not, use representative ranges. The point is the multiplier — cost of delivery drops, revenue per client stays the same or goes up because you can take on more clients. The margin restructure happens on both sides simultaneously. That's not incremental improvement. That's a structural change.

---

## Slide 7.6 — The internal business case

**Storyboard:** A single quote box, styled like a formal slide proposal. Bold text: "Two operators with this system match the output of a 6-person SDR team at 40% of the cost." Below that, smaller: "Payback period: 90 days." The framing is internal — this is the slide for a leadership deck. No company branding, no sales tone. Just the math, stated cleanly.

> **For internal teams / agencies pitching leadership:**

"Two operators with this system match the output of a 6-person SDR team at 40% of the cost. Payback period: 90 days."

> **Speaker notes:** This is the framing for anyone pitching this internally — to a founder, a VP, a board. You're not pitching a tool. You're pitching a headcount restructure with a 90-day payback. That's a capex argument with a clear ROI timeline. Leadership doesn't need to know what Claude Code is. They need the model, the cost, and the payback period.

---

## Slide 7.7 — The client-facing case

**Storyboard:** Same quote box format as 7.6, different framing. This one is client-facing — the tone shifts from internal efficiency to competitive differentiation. Two key claims: cost per meeting booked vs. competitors, and ramp time (two weeks vs. six). These are the two numbers clients actually ask about. Make them prominent.

> **For AEs pitching clients:**

"Our delivery model runs on Claude Code infrastructure. That's why our cost per meeting booked is lower than our competitors and our ramp time on new campaigns is two weeks, not six."

> **Speaker notes:** This is the client framing. They need two things: proof that the output is better (cost per meeting), and proof that it's faster (ramp time). Neither requires them to understand what Claude Code is. You're telling them what the system produces, not what it runs on. Fill in your real cost-per-meeting numbers before using this in a sales conversation.

---

## Slide 7.8 — CTA: Three things to do next

**Storyboard:** The repo link large and centered: `github.com/LeadGrowGTM/claude-code-gtm`. Below it, three numbered steps. Clean, actionable, no fluff. The viewer should be able to pause, screenshot this, and have everything they need to start. Links to Bison CLI and TechSight below the steps in smaller monospace.

1. `git clone github.com/LeadGrowGTM/claude-code-gtm`
2. Start with `chapter-2-foundation/CLAUDE.md.template` — fill in the five sections
3. Add your insider knowledge to the skill stubs — that's where your moat is

Additional tools:
- Bison CLI: `github.com/LeadGrowGTM/bison-cli`
- TechSight: open source, link in `tools/README.md`

> **Speaker notes:** That's the full stack. CLAUDE.md briefs the system. Rules prevent the failure modes. Skills encode what you know. Agents multiply your throughput. The waterfall cuts your data cost. And the business model restructures your margin — same clients, half the headcount cost, higher output per campaign. That's not a demo — that's what's running at LeadGrow right now. Three things to do with it: clone the repo, fill in your CLAUDE.md, and write your insider knowledge into the skill stubs. The insider knowledge is the only part only you can write. Everything else is infrastructure. If you build something with this, share it. Links in the description.

---

---

# BONUS — SALES CALL PREP (Hormozi loop close)

---

## Slide B.1 — Encoding sales training into a skill

**Storyboard:** Split screen. Left: a Hormozi framework excerpt or a page from SPIN Selling — whatever training you're using. Right: the sales-call-prep SKILL.md structure. A dotted arrow connects them. The visual says: training input goes in, pre-call brief comes out. The loop is the payoff — this is the thing you teased in the intro.

> **Speaker notes:** Earlier I said I'd show you how to take any sales training and encode it into a skill that makes you better on calls. Here's that. The sales-call-prep skill in the repo takes a training source — could be a Hormozi transcript, your own Fireflies call recordings, SPIN Selling notes — and a prospect brief, and returns a pre-call sheet. Objections, discovery questions, opening move, close target. Takes 15 minutes to build. Runs in 30 seconds before every call.

---

## Slide B.2 — Live: Pre-call brief in 30 seconds

**Storyboard:** Full-screen Claude Code terminal. Paste in training content, invoke the skill against a prospect, show the output: a structured pre-call sheet with objections listed, discovery questions queued, and an opening move. The output should be tight enough to read in 30 seconds before a call. That's the visual proof.

> **Speaker notes:** [LIVE SEGMENT — paste in training content, show the skill running, show the output. Keep this tight — 8-10 minutes. The point is demonstrating that skills aren't just for campaigns. Any repeatable expert task gets a skill file. The viewer should leave thinking about which expert task in their process gets encoded next.]

---

*END OF DECK*

---

## PRODUCTION NOTES

- **Dark background throughout.** Every slide. No gradient backgrounds, no stock photos.
- **Font size:** Code slides: 18pt minimum so it reads on compressed video. Body text: 22pt+.
- **Chapter 6 pacing:** Don't rush. Let silence sit when the agent is thinking. The audience needs to see it's real.
- **Live segments:** No re-takes on Chapter 6. Everything else can be edited. Mark live segments in the edit so the editor knows not to cut them for pacing.
- **Timestamps:** Add final chapter timestamps after recording, not before. Pin them to the first YouTube comment.
- **Repo link:** Pin it to the first comment. Add it to the description. Reference it at least once per chapter — not every slide.
- **The insider knowledge section:** When you show the cold-email skill live, pause long enough for viewers to screenshot it. That section is the most shareable moment in the deck.
