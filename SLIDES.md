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

> **Speaker notes:** No intro. Just start. If you're watching this you already know what Claude Code is and you want to see it applied to real outbound work. That's what this is.

---

## Slide 0.1b — Proof of production

**Storyboard:** Dark background. Four numbers stacked vertically — large, white, no labels yet. They reveal one at a time as you speak, each with a short descriptor appearing beneath it in smaller gray text. The numbers do the work before you explain them. No charts, no logos, no color — just the math. The viewer should feel: "this person is operating at scale."

| | |
|--|--|
| **394** | calls booked for clients in Q1 |
| **494,000** | leads contacted |
| **5** | Claude Code implementations running |
| **$726,000** | revenue generated for one client — their record |

> **Speaker notes:** These are the Q1 numbers from the system I'm about to show you. 394 calls booked on behalf of clients. 494,000 leads contacted. Five Claude Code implementations across different agencies and operators. And one client who hit their record revenue quarter — $726,000 — powered entirely by this stack. I'm not showing you a proof of concept. I'm showing you what's already running.

---

## Slide 0.2 — Three things you will leave with

**Storyboard:** Dark background. Three numbered items reveal one at a time as you speak. Large numerals (1, 2, 3) in a muted accent color — not icons, not bullets. Each item is a single line of white text. No header. The list feels like a commitment, not a menu.

1. A working Claude Code GTM infrastructure
2. A companion repo — clone it once, adapt it forever
3. Your own tools integrated directly into Claude Code — one interface for everything
4. The headcount math to justify this to a client or your leadership

> **Speaker notes:** This isn't a tutorial. By the end you'll have the actual files — CLAUDE.md template, skills, agents, the enrichment waterfall script. And you'll know how to wire your own tools into that interface so you stop switching between five different dashboards. Clone the repo now if you want to follow along. Link is on screen and in the description.

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

## Slide 0.5 — Before You Start: Install, Auth, IDE

**Storyboard:** Three panels side by side on dark background. Panel 1 "Install" — one command. Panel 2 "Auth" — browser OAuth, one command. Panel 3 "IDE" — VS Code sidebar alongside terminal. Below all three: "5 minutes. Then you have a terminal and a dashboard." No GUI screenshots — just commands and panel labels. Viewers starting from zero pause here; everyone else skips ahead.

```bash
# 1. Install (pick one)
npm install -g @anthropic-ai/claude-cli
# or
brew install claude

# 2. Authenticate
claude auth
# → Opens browser → Anthropic login → Returns to terminal

# 3. IDE integration (optional but recommended)
# VS Code: install "Claude Code" extension

# 4. First session
cd your-workspace
claude
# → Reads CLAUDE.md → Ready
```

> **Speaker notes:** If you already have Claude Code running, skip ahead — this is for anyone starting from zero. Install via npm or brew, one command. Authentication is OAuth: `claude auth` opens a browser, you log in with your Anthropic account, and you're back in the terminal. The IDE integration gives you a sidebar alongside your terminal. For this course you need the terminal (primary interface) and VS Code if you want to follow the SKILL.md editing live. Under five minutes total. One thing to know: Claude Code reads the CLAUDE.md file in your working directory when it opens. That's the first thing Chapter 2 builds.

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

## Slide 1.7 — Git: The Four Things You Actually Need

**Storyboard:** Dark background. Four commands stacked vertically in a terminal block — each with a one-line plain-English comment above it. No diagrams, no branch trees. Just the four commands with what they do. Below all four, a single line: "That's it. Everything else is recoverable." The visual should feel like a cheat sheet, not a lecture.

```bash
# Save your work and send it to GitHub
git add . && git commit -m "what I did" && git push

# Pull someone else's changes (or your own from another machine)
git pull

# Stop tracking files you don't want in the repo
echo ".env" >> .gitignore   # API keys, secrets — never commit these
echo "node_modules/" >> .gitignore

# See what's changed before you commit
git status
git diff
```

**Why Git matters for this course:**
- Your CLAUDE.md, skills, and rules files live in Git — version controlled, shareable, recoverable
- Claude Code reads your repo state and uses `gh` to interact with GitHub directly
- Every chapter in the companion repo is a commit you can diff, roll back, or branch from

> **Speaker notes:** Git is how you don't lose work. Four commands cover 90% of what you'll do in this course. `git add . && git commit && git push` saves and syncs. `git pull` gets changes. `.gitignore` keeps secrets out of GitHub — your `.env` file with API keys should always be in there, day one. And `git status` tells you what changed before you commit. One thing that matters here specifically: your CLAUDE.md and skill files are assets now. Treat them like code. Commit them. When you update your insider knowledge section, commit that. When a skill breaks, you can roll back to the last working version. Claude Code can also use `gh` commands directly to create repos, open PRs, and view issues without you touching a browser. If you're brand new to Git, clone the companion repo and the habit will build naturally.

---

## Slide 1.7b — GitHub Issues as Your Ops Backlog

**Storyboard:** A split screen. Left: a clean GitHub Issues list — three open issues with short, specific titles ("cold-email skill breaking on single-founder companies", "add LinkedIn scrape to Tier 1 waterfall", "test ICP research skill on 10 new accounts"). Right: a terminal running `gh issue list` showing the same issues. The message: your ops backlog and your code live in the same place. No Notion, no sticky notes.

```bash
# View open issues from the terminal
gh issue list

# Create an issue without leaving Claude Code
gh issue create --title "cold-email skill breaks on solo founders" \
                --body "Step 2 output generic when no team signals present"

# Close an issue when the fix ships
gh issue close 12
```

> **Speaker notes:** GitHub Issues are how you track what's broken, what needs building, and what's next — without a separate tool. Claude Code can read your issues list and create new ones from the terminal. Practical use: when you notice a skill failing a quality gate consistently, file an issue with the exact failure mode. When you build the fix, close it in the same commit message with "fixes #12". Your ops backlog and your codebase live in one place. That's the compounding benefit of running everything through one interface.

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

## Slide 2.4b — Voice-to-Prompt: Cut the Friction

**Storyboard:** Dark background. Left: phone with microphone active — "30 sec, dictated." Right: terminal with a complete, fully-contextualized prompt. Arrow connecting them. Two examples below — one typed (terse, incomplete) vs. one dictated (complete, full context). Contrast makes the quality difference obvious without commentary.

```
Typed: "write cold email for acme"

Dictated: "Write a two-step cold email for Acme Corp targeting their VP of Sales.
           They just raised a Series B, using Salesforce but no sequences tool.
           Use the pain angle from the ICP research file. Step 1 under 80 words,
           Step 2 reframes — don't follow up. Single brace variables."

Same time investment. Very different output quality.
```

> **Speaker notes:** The activation energy for a good prompt is friction. When you type, you abbreviate. You leave out context. Claude makes assumptions, you spend two turns correcting. When you dictate — phone speech-to-text, WhisperFlow, or any dictation tool — you naturally speak in complete sentences and give Claude the full picture in one shot. Operators who dictate prompts consistently get higher-quality first-draft output. The prompt is the brief. A briefing spoken out loud is always more complete than one typed on a keyboard while distracted. Try it for one session.

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

## Slide 3.5b — Test Before Shipping

**Storyboard:** Four boxes connected left to right: BUILD → REAL DATA → FIX → SHIP. Below each: BUILD: "30 min of focus"; REAL DATA: "5 actual companies — not invented examples"; FIX: "Until quality gates pass consistently"; SHIP: "Confident. Not hopeful." Below the flow in large type: "A skill that hasn't run on real data is a draft. Not a deliverable."

```
The ritual — every new skill, every time:

  BUILD      Write all 5 sections
    ↓
  REAL DATA  Run on 5 actual companies from your list
    ↓
  FIX        Find where it breaks. Update quality gates. Re-run.
    ↓
  SHIP       Now it's a deliverable. Not before.

"A skill that hasn't run on real data is a draft.
 Fast garbage is worse than slow correctness."
```

> **Speaker notes:** The ritual that separates usable skills from dangerous ones: test before shipping. Build the skill — all five sections. Run it on five actual companies from a real list. Not invented examples. Real companies. See where it breaks. Fix the quality gates. Run it again. A skill that passes on invented examples and fails on real data isn't done. Consistency is the bar: 8 out of 10 outputs passing all quality gates without manual correction. Below that — still a draft. A skill that produces garbage half the time is a liability, not an asset. Test before shipping.

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

> **Speaker notes:** An agent is an isolated worker you spawn. It has its own context window, its own tool access, and it runs independently. While you're in one conversation, three agents can be researching three different companies simultaneously. That's not a demo feature — 394 calls booked in Q1, 494,000 leads contacted, five implementations running across different operators. No research team. This chapter is also what makes the enrichment waterfall in Chapter 5 viable at scale — without agents coordinating the pipeline, you'd be running it one company at a time.

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

## Slide 4.5d — Reading Claude's Telltales

**Storyboard:** Four indicators in a 2x2 grid — amber dashboard warnings, not red alarms. Each: signal name in orange, concrete example in gray. Signals: Hedging Language, Length Drift, Re-asking Questions, Generalization Slip. Below: "Two of these together = /compact or restart. Don't wait for the third." Clinical, not alarming — these are early, readable signals.

```
Claude doesn't announce when output quality drops.
You have to read the telltales.

  ⚠ Hedging language    "I believe" / "it seems likely" (was specific before)
  ⚠ Length drift        Shorter without getting denser
  ⚠ Re-asking           Asking something you answered 2 turns ago
  ⚠ Generalization      Specific ICP advice → generic GTM advice

Two together: /compact (mid-task) or start fresh (new task)
Don't push through. Next 20 min will be worse than last 20.
```

> **Speaker notes:** Claude doesn't tell you when it's running out of context. Four signals to watch for: hedging language increases — it says "I believe" where it used to just answer. Response length shrinks without getting more concise. It re-asks questions you already answered — context loss in real time. Specifics slip into generics — tailored ICP advice starts sounding like a blog post. When you see two of these together: /compact mid-task to preserve progress, or start fresh for a new task. Don't push through hoping it self-corrects. The next 20 minutes of output will be worse. Cut it early.

---

## Slide 4.5e — Skill vs. Automation vs. Agentic Automation

**Storyboard:** Three columns on dark background, each a distinct block. Header row: "Skill", "Automation", "Agentic Automation." Four comparison rows below: Who triggers it, What it handles, Where it lives, Example. The columns read left to right as increasing autonomy — the visual should feel like a spectrum, not three random options. The viewer should finish reading and immediately know which column their next build belongs in.

| | Skill | Automation | Agentic Automation |
|--|-------|------------|-------------------|
| **Triggered by** | You, in a session | Event or schedule | Event, schedule, or another agent |
| **Handles** | Ambiguity, judgment calls | Deterministic steps only | Ambiguity + multi-step decisions |
| **Lives in** | Claude Code | N8n / Make / Zapier | Claude Code (scheduled or triggered) |
| **Example** | Write cold email from research | Push enriched lead to Bison on webhook | Research company → score ICP → write sequence → upload → notify if score > 18 |

> **Speaker notes:** Three tools, three different jobs. A skill handles ambiguity — you invoke it when there's judgment involved, context to read, output that varies. An automation runs a fixed sequence: trigger fires, steps execute, done. Deterministic. If the logic is purely IF-THEN, it's an automation and N8n is fine. The third column is where this gets interesting: agentic automation combines Claude's judgment with the autonomy of a scheduled trigger. A nightly agent that pulls yesterday's new leads, scores ICP fit, writes sequences for anything above 18, and uploads them — that's not a skill you invoke, and it's not a simple automation. It's a worker running a shift. The question for every new workflow you're about to build: which column does this belong in? Pick the simplest option that handles the ambiguity level of the task.

---

## Slide 4.5f — The Karpathy Auto-Research Loop

**Storyboard:** A circular loop diagram on dark background — six labeled stages connected by arrows going clockwise. The loop reads like a gear system: each stage feeds the next. In the center of the circle, two words: "Gets better." Beneath the loop, two concrete real-world examples shown as compact before/after blocks. The visual message: this isn't a one-time setup. It's a system that improves itself.

```
  Domain Research
        ↓
  Heuristics Library
        ↓
  Warm-Start Protocol  →  [Gets better]
        ↓
  Artifact Inspection
        ↓
  Parallel Readiness
        ↓
  Exploration Budget
        ↑_____________
```

**Example 1 — Tool integration:**
> Before: TechSight runs as a separate CLI you paste results from.
> After: TechSight is wired directly into Claude Code. Research agent calls it automatically. One interface.

**Example 2 — Sequence quality loop:**
> Before: Write sequence → review manually → tweak → repeat.
> After: Write sequence → score against quality gates → auto-iterate on failures → ship when gates pass. No manual review pass.

> **Speaker notes:** Andrej Karpathy documented this pattern for LLM optimization: the loop itself isn't complicated, what determines whether it actually improves is what you feed into it and how you steer it. Six failure modes kill 80% of loops before they compound. Blind start — you skip domain research and the LLM has no vocabulary. Rewrite churn — it rewrites from scratch every iteration instead of building on what worked. Cold restart — no warm-start protocol, so each run ignores prior wins. Metric blindness — score goes up but output gets worse because you're measuring the wrong thing. Premature parallelism — you parallelize before the single-agent loop is stable. Greedy lock-in — it always takes the better option and never explores, so it local-maxes. The practical version for GTM: wire your tools in so Claude calls them directly, then let the quality gates do the review pass. Stop doing the work a loop can do.

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

## Slide 5.1 — The interface problem

**Storyboard:** Ten tool names scattered across a dark screen in different font sizes — Clay, Apollo, Instantly, N8n, Notion, Google Sheets, ChatGPT, Sales Nav, Slack, Loom. All slightly overlapping, slightly chaotic. A single arrow pointing right. Then: one terminal cursor, blinking. Nothing else. The visual is the argument.

> **Speaker notes:** Count the tabs. Clay for enrichment. Apollo or ZoomInfo for list building. Instantly or Smartlead for sending. N8n for automation. Notion or Google Docs for research and SOPs. Sheets for reporting. ChatGPT for copy. Sales Nav for prospecting. Slack for handoffs. Loom to train the SDRs who run all of it. That's ten interfaces to run one outbound function. Every switch has a cost — not just the subscription, but the context switch, the handoff, the thing that falls through the gap between tools. What Claude Code actually solves isn't any one of those tools. It's the interface tax on all of them. One terminal. Everything routes through it. That's what this chapter is about.

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

**Storyboard:** A small two-row table: tool name, cost per query, and when it fires. The "When it fires" column tells the story — conditional, not default. A subtle "(edge cases only)" note at the bottom reinforces this.

| Tool | Cost | When it fires |
|------|------|---------------|
| OpenWebNinja | $0.002/query | Website thin, LinkedIn sparse |
| Clay | $X/credit | Complex signal workflows requiring Clay's native integrations |

> **Speaker notes:** Tier 3 only fires on misses. For records where the website is thin and LinkedIn is sparse — usually smaller companies, early-stage startups — that's when you hit the paid APIs. The script handles the fallback logic automatically. Most of your list never touches this tier. And when it does hit Clay, that's intentional — Clay's native integrations for complex signal work are genuinely useful. The difference is you're calling Clay from one interface, not running your whole operation inside it.

---

## Slide 5.6 — Clay vs. waterfall: the full comparison

**Storyboard:** A side-by-side table with two columns: "Clay-only" and "Waterfall." Four rows. Same dark background, same clean format. The "Interface" row is new and sits at the top — it's the lead. Cost comes second. Ownership and iteration speed follow. The visual tells the operator this isn't just a cost arbitrage — it's a workflow consolidation.

| | Clay-only | Waterfall |
|--|---------|---------|
| Interface | Separate UI, credit dashboard, workflow builder | Same terminal as everything else |
| 1,000 records | $X | ~$Y |
| Data ownership | Platform-dependent | Yours forever |
| Iteration | Change in Clay UI | Change the script |

> **Speaker notes:** The interface row is the lead. Clay is a great product — but it's a separate context. You're logging in, managing credits, building workflows in its own builder, then handing off to your sending tool, then handing off again. The waterfall runs from the same terminal as your research agents, your sequence generator, your Bison upload. One interface. The cost difference is real — Clay's enrichment at scale can run $500 to $1,500 a month depending on your volume and plan. The waterfall runs most of that at near-zero. But the bigger gain is that you stopped paying the interface tax.

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

**Storyboard:** Single bold sentence, centered on black: "This isn't a productivity hack." Line break. "It's what happens when 10 interfaces collapse into one." Two sentences, two lines, large type. Let it sit. The viewer who's been nodding along since Chapter 1 should feel this land.

> **Speaker notes:** Every chapter before this was about building the system. This chapter is about what it's worth commercially. Not as a tool you sell — as infrastructure that changes how you operate. When the interface tax disappears, two things happen: your team moves faster, and you need less of them to produce the same output. That's not an efficiency gain. That's a structural change. Two audiences: operators who want to understand their own economics, and anyone making a business case to leadership or a client.

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

**Storyboard:** Same quote box format as 7.6, different framing. Client-facing — tone shifts from internal efficiency to competitive differentiation. Three claims visible: meetings booked, ramp time, output velocity. These are the numbers clients actually ask about. Make them prominent.

> **For AEs pitching clients:**

"Our delivery model runs on Claude Code infrastructure. We're booking 20-30% more meetings per client than we were two years ago, our ramp time on new campaigns is two weeks not six, and our team size has gone down while output has gone up."

> **Speaker notes:** Clients need proof on two axes: output (are they getting more meetings?) and speed (how fast can you get campaigns live?). Neither requires them to understand what Claude Code is. You're telling them what the system produces, not what it runs on. The 20-30% meetings stat is real — that's the LeadGrow number year-over-year. The two-week ramp is real. The team shrinking 50% while output increased — that's the structural argument. You can lead with whichever stat matches what they're asking about.

---

## Slide 7.8 — GTM Orchestrator: the live system

**Storyboard:** A five-stage pipeline flow, left to right, dark background. Each stage is a labeled box with a one-line description below it. Connector arrows between them. The last box — "Offer: free campaign" — is highlighted in orange or accent color to signal the close. This isn't a concept slide. It's a wiring diagram for a system that's running.

```
[Signal-Led DB]  →  [Weekly Hire Monitor]  →  [Relevancy Assessment]  →  [Permissionless Value Drop]  →  [3-Step Sequence]
 Initial company      New hires at target        Role → ICP match           "Here are 10 companies          Email 1+2: signal intel
 list from signal     companies detected          Company bucketing           actively hiring [role]          Email 3: free campaign
 database             weekly, auto-flagged        by fit score               that match your ICP"            offer, one slot
```

> **Speaker notes:** This is the GTM Orchestrator. Here's how it runs. We start with a signal-led database — a curated list of companies that match the startup's ICP. Once a week, the system checks for new hires at those companies. Not all hires — we run a relevancy assessment first. The question is: what roles, when filled, signal that this company is the right buyer right now for the startup we're running campaigns for? When a company trips that signal, it gets bucketed and queued for research. The output is a permissionless value drop — "here are ten companies in your space actively hiring for [role], we think three of them are your best Q3 targets, here's why." No pitch. Just signal. The CTA at the end of the sequence isn't "book a call" — it's "we're offering one company a free signal-led campaign this quarter, want us to run yours?" Lower volume. Higher reply rate. The free campaign offer sits in email three, not email one. By the time they see it, they've already gotten value twice.

---

## Slide 7.9 — CTA: Three things to do next

**Storyboard:** The repo link large and centered: `github.com/LeadGrowGTM/claude-code-gtm`. Below it, three numbered steps. Clean, actionable, no fluff. The viewer should be able to pause, screenshot this, and have everything they need to start. Links to Bison CLI and TechSight below the steps in smaller monospace.

1. `git clone github.com/LeadGrowGTM/claude-code-gtm`
2. Start with `chapter-2-foundation/CLAUDE.md.template` — fill in the five sections
3. Add your insider knowledge to the skill stubs — that's where your moat is

Additional tools:
- Bison CLI: `github.com/LeadGrowGTM/bison-cli`
- TechSight: open source, link in `tools/README.md`
- Feynman skill (installable): `github.com/LeadGrowGTM/feynman-skill`
- context-os (workspace OS patterns): `github.com/jacob-dietle/context-os`

> **Speaker notes:** That's the full stack. CLAUDE.md briefs the system. Rules prevent the failure modes. Skills encode what you know. Agents multiply your throughput. The waterfall cuts your data cost. And the business model restructures your margin — same clients, half the headcount cost, higher output per campaign. That's not a demo — that's what's running at LeadGrow right now. Three things to do with it: clone the repo, fill in your CLAUDE.md, and write your insider knowledge into the skill stubs. The insider knowledge is the only part only you can write. Everything else is infrastructure. Two bonus repos worth bookmarking: the Feynman skill teaches any concept using the Feynman Technique — install it in your workspace and it fires automatically when you say "teach me X." context-os by Jacob Dietle is a workspace OS pattern repo that complements everything in this course. If you build something with this, share it. Links in the description.

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
