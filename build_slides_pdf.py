"""
Build presentation slides HTML from SLIDES.md.
Each slide = one 16:9 page. Speaker notes appear below.
Print via Chrome (Ctrl+P -> Save as PDF, No margins, A4 Landscape).
"""

import re
from pathlib import Path

SLIDES_MD = Path(r"C:\Users\mitch\Everything_CC\claude-code-gtm\SLIDES.md")
OUT_HTML  = Path(r"C:\Users\mitch\Everything_CC\claude-code-gtm\slides-presentation.html")

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Lora:ital,wght@0,400;1,400&family=Fira+Code:wght@400&display=swap');

:root {
  --bg:     #0f0f0e;
  --surface:#1a1a18;
  --cream:  #faf9f5;
  --dim:    rgba(250,249,245,0.55);
  --orange: #d97757;
  --green:  #7db87d;
  --gray:   #b0aea5;
  --rule:   rgba(250,249,245,0.15);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  background: #111;
  font-family: 'Poppins', Arial, sans-serif;
  color: var(--cream);
}

/* ── SLIDE WRAPPER ─────────────────────────────────────────────── */
.slide-page {
  width: 100%;
  page-break-after: always;
  margin-bottom: 0;
}

.slide-canvas {
  width: 100%;
  aspect-ratio: 16/9;
  background: var(--bg);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 6% 8%;
  overflow: hidden;
}

/* subtle texture line top */
.slide-canvas::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--orange);
  opacity: 0.6;
}

.slide-label {
  position: absolute;
  top: 18px; right: 24px;
  font-size: 9px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--gray);
  font-family: 'Fira Code', monospace;
}

/* ── LAYOUT TYPES ──────────────────────────────────────────────── */

/* Title-only: one big statement */
.layout-title .slide-canvas {
  align-items: center;
  text-align: center;
}

/* Split: left text / right content */
.layout-split .slide-canvas {
  flex-direction: row;
  gap: 6%;
}
.layout-split .slide-left { flex: 1; }
.layout-split .slide-right { flex: 1.2; }

/* Code: terminal feel */
.layout-code .slide-canvas {
  background: #0a0a09;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 5% 6%;
}

/* Centered content */
.layout-center .slide-canvas {
  align-items: center;
  text-align: center;
}

/* ── TYPOGRAPHY ────────────────────────────────────────────────── */
.slide-eyebrow {
  font-size: 1.1vw;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: 1.2vw;
  font-weight: 600;
}

.slide-headline {
  font-size: 4.8vw;
  line-height: 1.05;
  font-weight: 700;
  color: var(--cream);
  letter-spacing: -1px;
  margin-bottom: 1.5vw;
}

.slide-headline.xl {
  font-size: 6.5vw;
  letter-spacing: -2px;
}

.slide-sub {
  font-size: 1.5vw;
  color: var(--dim);
  font-family: 'Lora', Georgia, serif;
  font-style: italic;
  line-height: 1.5;
}

.slide-body {
  font-size: 1.4vw;
  color: var(--cream);
  line-height: 1.65;
}

.orange { color: var(--orange); }
.dim    { color: var(--dim); }
.green  { color: var(--green); }

/* ── RULE ──────────────────────────────────────────────────────── */
.slide-rule {
  width: 48px;
  height: 3px;
  background: var(--orange);
  margin: 1.5vw 0;
}

/* ── NUMBERED LIST ─────────────────────────────────────────────── */
.num-list { list-style: none; width: 100%; }
.num-list li {
  display: flex;
  align-items: baseline;
  gap: 1.2vw;
  padding: 0.8vw 0;
  border-bottom: 1px solid var(--rule);
  font-size: 1.5vw;
  color: var(--cream);
}
.num-list li:last-child { border-bottom: none; }
.num-list .n {
  font-size: 2.2vw;
  font-weight: 700;
  color: var(--orange);
  line-height: 1;
  flex-shrink: 0;
  width: 2.5vw;
}

/* ── BULLET LIST ───────────────────────────────────────────────── */
.bullet-list { list-style: none; width: 100%; }
.bullet-list li {
  padding: 0.7vw 0 0.7vw 1.8vw;
  border-bottom: 1px solid var(--rule);
  font-size: 1.5vw;
  color: var(--cream);
  position: relative;
}
.bullet-list li:last-child { border-bottom: none; }
.bullet-list li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--orange);
}
.bullet-list li.strike { color: var(--gray); text-decoration: line-through; }
.bullet-list li.check { color: var(--green); }
.bullet-list li.check::before { content: '✓'; color: var(--green); }

/* ── STAT GRID ─────────────────────────────────────────────────── */
.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2vw 4vw;
  width: 100%;
}
.stat-block { }
.stat-num {
  font-size: 5vw;
  font-weight: 700;
  color: var(--cream);
  line-height: 1;
  letter-spacing: -2px;
}
.stat-label {
  font-size: 1.1vw;
  color: var(--dim);
  font-family: 'Lora', Georgia, serif;
  font-style: italic;
  margin-top: 0.3vw;
}

/* ── TABLE ─────────────────────────────────────────────────────── */
.slide-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1.3vw;
}
.slide-table th {
  text-align: left;
  padding: 0.6vw 1vw;
  border-bottom: 1px solid var(--orange);
  font-size: 0.9vw;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--orange);
  font-weight: 600;
}
.slide-table td {
  padding: 0.7vw 1vw;
  border-bottom: 1px solid var(--rule);
  color: var(--cream);
  vertical-align: top;
}
.slide-table tr:last-child td { border-bottom: none; }
.slide-table .bold { font-weight: 700; color: var(--orange); }

/* ── CODE BLOCK ────────────────────────────────────────────────── */
.terminal {
  background: #0a0a09;
  border: 1px solid rgba(255,255,255,0.08);
  padding: 2vw 2.5vw;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 1.15vw;
  line-height: 1.65;
  color: #a8c8a8;
  width: 100%;
  overflow: hidden;
  border-radius: 4px;
}
.terminal .prompt { color: var(--orange); }
.terminal .comment { color: var(--gray); }

/* ── ARCHITECTURE DIAGRAM ──────────────────────────────────────── */
.arch-layers { width: 100%; }
.arch-layer {
  display: flex;
  align-items: center;
  padding: 1vw 1.5vw;
  margin-bottom: 0.5vw;
  background: var(--surface);
  border-left: 3px solid var(--orange);
  font-size: 1.2vw;
}
.arch-layer .layer-name {
  font-family: 'Fira Code', monospace;
  color: var(--orange);
  width: 12vw;
  font-weight: 600;
}
.arch-layer .layer-arrow { color: var(--gray); margin: 0 1vw; }
.arch-layer .layer-desc { color: var(--cream); }
.arch-layer .layer-tag {
  margin-left: auto;
  font-size: 0.9vw;
  color: var(--gray);
  font-style: italic;
  font-family: 'Lora', Georgia, serif;
}

/* ── QUOTE BLOCK ───────────────────────────────────────────────── */
.quote-block {
  border-left: 4px solid var(--orange);
  padding: 1.5vw 2vw;
  background: var(--surface);
  width: 100%;
}
.quote-text {
  font-size: 1.8vw;
  line-height: 1.5;
  color: var(--cream);
  font-family: 'Lora', Georgia, serif;
  font-style: italic;
}
.quote-meta {
  font-size: 1vw;
  color: var(--gray);
  margin-top: 1vw;
  font-style: normal;
  font-family: 'Poppins', Arial, sans-serif;
}

/* ── COMPARISON ────────────────────────────────────────────────── */
.compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5vw;
  width: 100%;
}
.compare-col {}
.compare-head {
  font-size: 0.9vw;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--orange);
  padding-bottom: 0.6vw;
  border-bottom: 1px solid var(--orange);
  margin-bottom: 0.8vw;
  font-weight: 600;
}
.compare-item {
  padding: 0.6vw 0;
  border-bottom: 1px solid var(--rule);
  font-size: 1.3vw;
  color: var(--cream);
}

/* ── WATERFALL ─────────────────────────────────────────────────── */
.waterfall { width: 100%; }
.wf-tier {
  background: var(--surface);
  border-left: 3px solid var(--orange);
  padding: 0.8vw 1.5vw;
  margin-bottom: 0.3vw;
  font-size: 1.2vw;
}
.wf-tier .tier-name { font-weight: 600; color: var(--orange); }
.wf-tier .tier-items { color: var(--dim); font-size: 1.05vw; margin-top: 0.2vw; }
.wf-arrow {
  text-align: center;
  color: var(--gray);
  font-size: 1.1vw;
  padding: 0.1vw 0;
}
.wf-arrow span { color: var(--dim); font-size: 0.9vw; font-style: italic; }

/* ── TOOL BLOAT SCATTER ────────────────────────────────────────── */
.tool-scatter {
  position: relative;
  width: 100%;
  height: 55%;
  margin-bottom: 2vw;
}
.tool-name {
  position: absolute;
  font-family: 'Poppins', Arial, sans-serif;
  color: rgba(176,174,165,0.7);
  font-weight: 600;
}

/* ── CHAPTER TITLE SLIDE ───────────────────────────────────────── */
.chapter-num {
  font-size: 8vw;
  font-weight: 700;
  color: rgba(217,119,87,0.15);
  position: absolute;
  right: 5%;
  bottom: 5%;
  line-height: 1;
  letter-spacing: -4px;
}

/* ── SKILL FILE STRUCTURE ──────────────────────────────────────── */
.skill-tree { font-family: 'Fira Code', monospace; font-size: 1.2vw; }
.skill-tree .file { color: var(--cream); }
.skill-tree .section { color: var(--orange); }
.skill-tree .desc { color: var(--gray); }
.skill-tree .highlight { color: #f0c080; font-weight: 700; }

/* ── SPAWN PATTERN ─────────────────────────────────────────────── */
.spawn-compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2vw;
  width: 100%;
}
.spawn-col { }
.spawn-label {
  font-size: 0.85vw;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 0.4vw 0.8vw;
  margin-bottom: 0.5vw;
  font-weight: 600;
}
.spawn-label.wrong { background: #3d1f1f; color: #e07070; }
.spawn-label.right { background: #1f3d1f; color: #7db87d; }
.spawn-code {
  font-family: 'Fira Code', monospace;
  font-size: 1.05vw;
  line-height: 1.6;
  color: var(--dim);
  padding: 1vw;
  background: var(--surface);
}
.spawn-code .highlight { color: var(--green); }
.spawn-token {
  font-size: 1.6vw;
  font-weight: 700;
  margin-top: 0.8vw;
}
.spawn-token.bad { color: #e07070; }
.spawn-token.good { color: var(--green); }

/* ── SPEAKER NOTES AREA ────────────────────────────────────────── */
.notes-area {
  background: #222;
  padding: 2% 4%;
  border-top: 2px solid var(--orange);
}
.notes-area-label {
  font-size: 9px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: 8px;
  font-weight: 600;
}
.notes-area-text {
  font-family: 'Lora', Georgia, serif;
  font-size: 0.85vw;
  line-height: 1.6;
  color: rgba(250,249,245,0.7);
}

/* ── PRINT ─────────────────────────────────────────────────────── */
@media print {
  html, body { background: #000; }
  .slide-page { page-break-after: always; margin: 0; }
  @page { size: landscape; margin: 0; }
}
"""

# ── SLIDE DATA ────────────────────────────────────────────────────────────────
# Each slide is hand-crafted from the storyboard + content in SLIDES.md

def slide(num, title, canvas_html, notes, layout="default", chapter=None):
    chapter_badge = f'<div class="slide-label">{num}</div>' if num else ''
    ch_attr = f' data-chapter="{chapter}"' if chapter else ''
    return f"""
<div class="slide-page layout-{layout}"{ch_attr}>
  <div class="slide-canvas">
    {chapter_badge}
    {canvas_html}
  </div>
  <div class="notes-area">
    <div class="notes-area-label">Speaker Notes</div>
    <div class="notes-area-text">{notes}</div>
  </div>
</div>
"""

slides_html = []

# ── INTRO ─────────────────────────────────────────────────────────────────────

slides_html.append(slide("0.1", "Title", """
  <div style="width:100%; text-align:center;">
    <div class="slide-headline xl">Claude Code<br>for GTM Operators</div>
    <div class="slide-sub" style="text-align:center; margin-top:1vw;">The system behind agency-grade outbound</div>
    <div style="margin-top:2vw; font-family:'Fira Code',monospace; font-size:1vw; color:var(--gray);">github.com/LeadGrowGTM/claude-code-gtm</div>
  </div>
""", "No intro. Just start. If you're watching this you already know what Claude Code is.", "title"))

slides_html.append(slide("0.1b", "Proof of production", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Q1 Numbers</div>
    <div class="stat-grid">
      <div class="stat-block">
        <div class="stat-num">394</div>
        <div class="stat-label">calls booked for clients</div>
      </div>
      <div class="stat-block">
        <div class="stat-num">494K</div>
        <div class="stat-label">leads contacted</div>
      </div>
      <div class="stat-block">
        <div class="stat-num">5</div>
        <div class="stat-label">Claude Code implementations running</div>
      </div>
      <div class="stat-block">
        <div class="stat-num">$512K</div>
        <div class="stat-label">revenue for one client — their record</div>
      </div>
    </div>
  </div>
""", "These are the Q1 numbers from the system I'm about to show you. I'm not showing you a proof of concept. I'm showing you what's already running."))

slides_html.append(slide("0.2", "Three things you will leave with", """
  <div style="width:100%;">
    <div class="slide-eyebrow">By the end</div>
    <ol class="num-list">
      <li><span class="n">1</span><span>A working Claude Code GTM infrastructure</span></li>
      <li><span class="n">2</span><span>A companion repo — clone it once, adapt it forever</span></li>
      <li><span class="n">3</span><span>The headcount math to justify this to a client or your leadership</span></li>
    </ol>
  </div>
""", "This isn't a tutorial. By the end you'll have the actual files — CLAUDE.md template, skills, agents, the enrichment waterfall script. Clone the repo now if you want to follow along."))

slides_html.append(slide("0.3", "Four loops planted", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Watch for these</div>
    <ol class="num-list">
      <li><span class="n">6</span><span><span class="orange">"Cold company. No prep. Live campaign in under an hour."</span></span></li>
      <li><span class="n">5</span><span>"The enrichment waterfall that replaced most of our Clay spend."</span></li>
      <li><span class="n">7</span><span>"The headcount math. Two operators vs. six SDRs."</span></li>
      <li><span class="n">B</span><span class="dim">"If you do sales calls — stay for the last segment."</span></li>
    </ol>
  </div>
""", "Four things I want you watching for. Chapter 6 is the main event — I pick a company I've never touched, and we go from zero to a live campaign in under an hour. Timer on screen. No edits."))

slides_html.append(slide("0.1c", "Who This Is For", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Who this is for</div>
    <table class="slide-table">
      <thead><tr><th>Role</th><th>The pain</th><th>What changes</th></tr></thead>
      <tbody>
        <tr><td><strong>Founder / Solo</strong></td><td class="dim">You ARE the SDR. Research, write, send — manually.</td><td class="green">One operator, 11 clients. Research to live campaign under an hour.</td></tr>
        <tr><td><strong>Account Executive</strong></td><td class="dim">30% of your day is CRM logging, follow-ups, prep. None of it is selling.</td><td class="green">Call ends → transcript → CRM → follow-up drafted. You close.</td></tr>
        <tr><td><strong>VP of Sales</strong></td><td class="dim">Ramp takes 4 months. Playbook lives in your head.</td><td class="green">Encode the playbook as a skill. Every new rep executes at your best rep's level.</td></tr>
        <tr><td><strong>VP of Growth</strong></td><td class="dim">Every campaign starts from scratch. No intelligence from the last one.</td><td class="green">Reply data feeds the next campaign. Every cycle smarter than the last.</td></tr>
      </tbody>
    </table>
  </div>
""", "If you recognize yourself in one of these, stay. The founder problem is headcount. The AE problem is time. VP Sales is consistency. VP Growth is compounding."))

slides_html.append(slide("0.4", "Chapter map", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Course structure</div>
    <table class="slide-table">
      <thead><tr><th>Ch</th><th>Title</th><th>Time</th></tr></thead>
      <tbody>
        <tr><td>1</td><td>The Stack Replacement Thesis <span class="dim">+ Manual First + Git</span></td><td class="dim">25 min</td></tr>
        <tr><td>2</td><td>Foundation: CLAUDE.md <span class="dim">+ Hooks + Permission Model</span></td><td class="dim">30 min</td></tr>
        <tr><td>3</td><td>Skills: SOPs That Run Forever <span class="dim">+ Output Calibration</span></td><td class="dim">45 min</td></tr>
        <tr><td>4</td><td>Agents: Headcount Leverage <span class="dim">+ GSD + lg-runtime + Escape Hatch</span></td><td class="dim">40 min</td></tr>
        <tr><td>5</td><td>The Enrichment Waterfall</td><td class="dim">30 min</td></tr>
        <tr><td class="bold">6</td><td class="bold">The Live GTM Build</td><td class="orange bold">50 min ←</td></tr>
        <tr><td>7</td><td>The Business Layer <span class="dim">+ Skills Flywheel + PR Gatekeeper</span></td><td class="dim">35 min</td></tr>
        <tr><td>B</td><td>Bonus: Sales Call Prep</td><td class="dim">10 min</td></tr>
      </tbody>
    </table>
  </div>
""", "The chapters build on each other. Chapter 3 (skills) is what makes the live build in Chapter 6 readable. If you jump straight to 6, you're watching a demo, not a blueprint. Start with the argument — why does this stack exist? That's chapter 1."))

# ── CH 1 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("0.4b", "Full Course Map", """
  <div style="width:100%;">
    <div class="slide-eyebrow">YouTube chapter markers</div>
    <div class="terminal" style="font-size:0.9vw; line-height:1.55;">
<span style="color:var(--orange); font-weight:600;">INTRO</span>                                             0:00
  Proof of production / Who this is for               0:30

<span style="color:var(--orange); font-weight:600;">Ch. 1 — Stack Replacement Thesis</span>                  5:00
  Manual First · 4-layer arch · Mission Control
  Five Primitives · Git                               13:00

<span style="color:var(--orange); font-weight:600;">Ch. 2 — Foundation: CLAUDE.md</span>                    30:00
  Context Ladder · Permission Model · Hooks           35:00

<span style="color:var(--orange); font-weight:600;">Ch. 3 — Skills</span>                                   60:00
  Description Router · Six Patterns · Calibration
  7-Point Diagnostic                                  64:00

<span style="color:var(--orange); font-weight:600;">Ch. 4 — Agents</span>                                   90:00
  File Format · Spawn · Context Forking · Hygiene
  GSD · lg-runtime                                    95:00

<span style="color:var(--orange); font-weight:600;">Ch. 5 — Waterfall</span>                               130:00
<span style="color:var(--orange); font-weight:700; font-size:1vw;">Ch. 6 — LIVE GTM BUILD  ←</span>                       160:00
<span style="color:var(--orange); font-weight:600;">Ch. 7 — Business Layer</span>                          210:00
<span class="comment">— Timestamps approximate. Adjust during edit. —</span>
    </div>
  </div>
""", "[Pause 5 seconds — let viewers find their chapter. YouTube chapter markers source. Copy into video description after timestamps finalized in post. Not meant to be read aloud. Move immediately into Chapter 1.]"))

slides_html.append(slide("0.5", "Before You Start", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Setup — 5 minutes</div>
    <div class="terminal">
<span class="comment"># 1. Install</span>
npm install -g @anthropic-ai/claude-cli
<span class="comment"># or: brew install claude</span>

<span class="comment"># 2. Authenticate</span>
<span class="prompt">$</span> claude auth
<span class="comment"># → Opens browser → Anthropic login → back to terminal</span>

<span class="comment"># 3. First session</span>
<span class="prompt">$</span> cd your-workspace &amp;&amp; claude
<span class="comment"># → Reads CLAUDE.md → Ready</span>
    </div>
    <div class="slide-sub" style="margin-top:1.5vw;">VS Code / JetBrains extension optional but recommended for live editing.</div>
  </div>
""", "Install, auth, open. Under 5 minutes. Claude Code reads CLAUDE.md in your working directory — that's the first thing Chapter 2 builds. If you already have this running, skip ahead."))

slides_html.append(slide("1.1", "Your current stack", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Chapter 1 — The Stack Replacement Thesis</div>
    <div class="slide-headline">Your current stack</div>
    <div style="display:flex; gap:3vw; margin-top:2vw; align-items:center;">
      <div style="text-align:center; flex:1;">
        <div style="font-size:2.5vw; font-weight:700; color:var(--orange);">Clay</div>
        <div class="dim" style="font-size:1vw;">enrichment</div>
      </div>
      <div style="font-size:2vw; color:var(--gray);">+</div>
      <div style="text-align:center; flex:1;">
        <div style="font-size:2.5vw; font-weight:700; color:var(--orange);">N8n</div>
        <div class="dim" style="font-size:1vw;">automation</div>
      </div>
      <div style="font-size:2vw; color:var(--gray);">+</div>
      <div style="text-align:center; flex:1;">
        <div style="font-size:2.5vw; font-weight:700; color:var(--orange);">Smartlead</div>
        <div class="dim" style="font-size:1vw;">sending</div>
      </div>
      <div style="font-size:2vw; color:var(--gray);">+</div>
      <div style="text-align:center; flex:1; color:var(--gray);">
        <div style="font-size:2vw; font-weight:600;">7 more</div>
        <div style="font-size:1vw;">interfaces</div>
      </div>
    </div>
    <div style="margin-top:2.5vw; font-family:'Lora',serif; font-style:italic; font-size:1.4vw; color:var(--dim);">That stack works. But here's where it breaks down.</div>
  </div>
""", "If you're running a GTM agency right now you're probably paying for Clay, something like N8n or Make, and a sending platform. That stack works. I'm not going to tell you to rip it out. But I will show you where it breaks down."))

slides_html.append(slide("1.2", "What gets replaced", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Replaced</div>
    <ul class="bullet-list">
      <li class="strike">Zapier / basic automation logic</li>
      <li class="strike">Clay for standard enrichment (website scrape, LinkedIn, tech stack)</li>
      <li class="strike">Manual personalization workflows</li>
    </ul>
  </div>
""", "Zapier is gone if you're serious about this. Clay's enrichment — specifically the stuff you can get from a company website, LinkedIn, and a tech stack tool — that's now a script you run once and own forever."))

slides_html.append(slide("1.3", "What survives", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Survives</div>
    <ul class="bullet-list">
      <li class="check">Apollo / data sources (you still need leads)</li>
      <li class="check">Bison / Smartlead / Instantly (sending infra)</li>
      <li class="check">Clay for complex signal-based workflows</li>
    </ul>
  </div>
""", "Data sources survive. Sending infra survives. And Clay survives for genuinely complex signal-based workflows where you need its native integrations. Everything else is on the table."))

slides_html.append(slide("1.4", "What gets multiplied", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Multiplied</div>
    <ol class="num-list">
      <li><span class="n">10×</span><span>Research depth per company <span class="dim">— 20 min → 45 sec</span></span></li>
      <li><span class="n">10×</span><span>Personalization quality per email</span></li>
      <li><span class="n">10×</span><span>Workflow composition speed <span class="dim">— days → hours</span></span></li>
    </ol>
  </div>
""", "Research depth is the biggest one. What used to take an SDR 20 minutes per company now takes 45 seconds. Personalization quality goes up because you're working from actual research, not a template."))

slides_html.append(slide("1.4b", "Manual First", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The principle</div>
    <div class="spawn-compare">
      <div class="spawn-col">
        <div class="spawn-label wrong">Automate First</div>
        <div class="spawn-code">Prompt Claude<br>Hope it figures it out<br>Get fast garbage<br>Fix forever</div>
        <div class="spawn-token bad" style="font-size:1.1vw;">No expertise to encode.</div>
      </div>
      <div class="spawn-col">
        <div class="spawn-label right">Manual First</div>
        <div class="spawn-code">Do the work manually (5×)<br><span class="highlight">Notice the pattern</span><br>Notice the decisions<br>Write the skill<br>Validate on real data<br>Then automate<br>↓ Every run gets it right</div>
        <div class="spawn-token good" style="font-size:1.1vw;">Compounding from here.</div>
      </div>
    </div>
  </div>
""", "Most common failure: someone gets Claude Code, automates immediately, gets inconsistent output, gives up. You can't encode expertise you don't have yet. Do the work manually five times — you'll notice what you always check, what decisions you always make. Write those into the skill."))

slides_html.append(slide("1.5", "The 4-layer architecture", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The system</div>
    <div class="arch-layers">
      <div class="arch-layer" style="border-color:#f0c080; background: rgba(240,192,128,0.08);">
        <span class="layer-name" style="color:#f0c080;">CLAUDE.md</span>
        <span class="layer-arrow">←</span>
        <span class="layer-desc">Operator brief</span>
        <span class="layer-tag">Loads every session</span>
      </div>
      <div class="arch-layer">
        <span class="layer-name">Rules</span>
        <span class="layer-arrow">←</span>
        <span class="layer-desc">Constraints</span>
        <span class="layer-tag">Prevent failures</span>
      </div>
      <div class="arch-layer">
        <span class="layer-name">Skills</span>
        <span class="layer-arrow">←</span>
        <span class="layer-desc">SOPs</span>
        <span class="layer-tag">Run forever</span>
      </div>
      <div class="arch-layer">
        <span class="layer-name">Agents</span>
        <span class="layer-arrow">←</span>
        <span class="layer-desc">Workers</span>
        <span class="layer-tag">Execute in parallel</span>
      </div>
    </div>
  </div>
""", "This is the whole system in one diagram. CLAUDE.md at the top loads every session, sets the operating mode. Rules prevent failure modes. Skills are your encoded SOPs. Agents execute everything in parallel."))

slides_html.append(slide("1.5b", "Mission Control", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The mental model</div>
    <div class="terminal" style="font-size:1.1vw; line-height:1.9;">
<span style="color:var(--orange); font-weight:700;">You = Mission Control</span>
  Set objectives. Monitor. Intervene when needed.

<span style="color:var(--orange);">CLAUDE.md</span>  = Mission Brief + Rules of Engagement
<span style="color:var(--orange);">Terminal</span>    = Comms channel (how commands travel)
<span style="color:var(--orange);">IDE</span>         = Mission dashboard (visibility into what's running)
<span style="color:var(--orange);">Skills</span>      = SOPs the crew already knows cold
<span style="color:var(--orange);">Agents</span>      = Specialist crew with domain expertise
    </div>
    <div class="slide-sub" style="margin-top:1.5vw;">You're not coding. You're commanding.</div>
  </div>
""", "The mental model that changes everything: you're not a developer. You're Mission Control. Set objectives, monitor telemetry, intervene when something goes wrong. Trust is earned through demonstrated performance, not granted up front. Calibrate trust to evidence."))

slides_html.append(slide("1.5c", "Five Primitives", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The complete map</div>
    <table class="slide-table">
      <thead><tr><th>Primitive</th><th>What it does</th></tr></thead>
      <tbody>
        <tr><td class="bold" style="font-family:'Fira Code',monospace;">CLAUDE.md</td><td>Operator brief — loads every session, sets identity + routing</td></tr>
        <tr><td class="bold" style="font-family:'Fira Code',monospace;">Rules</td><td>Constraints — prevent specific failure modes from repeating</td></tr>
        <tr><td class="bold" style="font-family:'Fira Code',monospace;">Skills</td><td>SOPs — encode expert methodology, run on demand</td></tr>
        <tr><td class="bold" style="font-family:'Fira Code',monospace;">Agents</td><td>Workers — isolated execution, parallel throughput</td></tr>
        <tr><td class="bold" style="font-family:'Fira Code',monospace;">Hooks</td><td>Triggers — shell commands that fire on tool events</td></tr>
      </tbody>
    </table>
    <div class="slide-sub" style="margin-top:1.5vw;">Confused about what you're building? Come back to this slide.</div>
  </div>
""", "Five building blocks. Every chapter is one of these five. People who skip this mental model spend six months building the wrong primitive for every problem. Each chapter covers one layer."))

slides_html.append(slide("1.6", "Clone the repo", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Start here</div>
    <div class="terminal" style="text-align:left; margin:2vw auto; max-width:70%;">
      <span class="prompt">$</span> git clone github.com/LeadGrowGTM/claude-code-gtm
    </div>
    <div class="slide-sub" style="text-align:center; margin-top:1.5vw;">Chapter-by-chapter folders. Before/after diffs. Knowledge graph scripts.</div>
  </div>
""", "Clone the repo now. Each folder has a README telling you what you're building. Chapter 6 has before/ and after/ — diff them and you see exactly what 50 minutes produces.", "center"))

slides_html.append(slide("1.6b", "Git: Your Skills Are Code", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Version control the library</div>
    <div class="terminal">
<span class="comment"># Claude Code generates commits natively</span>
git commit -m <span style="color:var(--orange);">"feat(skills): add insider knowledge to cold-email"</span>

<span class="comment"># Skills library branches like any codebase</span>
main                        <span class="comment">← stable, pulled by the whole team</span>
feature/new-sequence-angle  <span class="comment">← operator's work in progress</span>
fix/qa-gate-tighten         <span class="comment">← under PR review</span>

<span class="comment"># Commit before any risky operation</span>
git add skills/ &amp;&amp; git commit -m <span style="color:var(--orange);">"checkpoint before campaign launch"</span>
    </div>
  </div>
""", "Everything in this system is markdown files — CLAUDE.md, rules, skills, agents, hooks. Markdown goes in git. Without version control: no rollback, no history, no team collaboration. Commit before any risky operation. It's your escape hatch."))

# ── CH 2 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("2.1", "CLAUDE.md — the claim", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Chapter 2 — Foundation</div>
    <div class="slide-headline" style="text-align:center;">CLAUDE.md isn't<br>a config file.</div>
    <div class="slide-rule" style="margin:1.5vw auto;"></div>
    <div class="slide-headline" style="text-align:center; color:var(--orange);">It's a permanent<br>team member brief.</div>
  </div>
""", "Every new Claude Code session reads CLAUDE.md first. Most people treat it like a README. Wrong. Write it like you're onboarding someone who will never forget what you write.", "title"))

slides_html.append(slide("2.2", "The five sections", """
  <div style="width:100%;">
    <div class="slide-eyebrow">CLAUDE.md structure</div>
    <div class="terminal">
<span style="color:var(--orange);">## Identity</span>        <span class="comment">— who Claude is in this context</span>
<span style="color:var(--orange);">## Workflow Style</span>  <span class="comment">— how to handle execution (ask vs act)</span>
<span style="color:var(--orange);">## Repos</span>           <span class="comment">— what directories exist and what they're for</span>
<span style="color:var(--orange);">## Work Routing</span>    <span class="comment">— where different types of work go</span>
<span style="color:var(--orange);">## Skill Discovery</span> <span class="comment">— how to find relevant skills</span>
    </div>
  </div>
""", "Five sections. Identity sets the operating mode. Workflow style is where you put execution preferences. Work routing tells it where to put different output. Skill discovery matters more as your library grows."))

slides_html.append(slide("2.2b", "The Context Ladder", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Context inherits upward</div>
    <div class="terminal">
<span style="color:var(--dim);">~/.claude/CLAUDE.md</span>         <span class="comment">← Global: your identity, universal rules</span>
<span style="color:var(--orange);">./CLAUDE.md</span>                  <span class="comment">← Workspace: repo map, integrations, routing</span>
<span style="color:var(--dim);">./leadgrow-hq/CLAUDE.md</span>      <span class="comment">← Project: company context, tools, commands</span>
<span style="color:var(--dim);">./clients/gtm-client-*/</span>      <span class="comment">← Client: per-client ICP, campaigns, history</span>

Each layer adds context. Most specific layer wins.
When Claude needs something outside current scope, it moves up.
    </div>
  </div>
""", "CLAUDE.md files layer like CSS inheritance. Write your identity once at global level. Company context lives once at project level. Client folders only contain client-specific overrides. Most specific layer wins — and when Claude can't find something, it moves up the ladder."))

slides_html.append(slide("2.3", "Identity: stop the filler", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Identity section</div>
    <div class="terminal">
<span class="comment">## Identity — Who You Are</span>

You're not an assistant. You're [NAME]'s operator.
Your purpose: run outbound GTM for B2B SaaS clients.

<span style="color:var(--orange);">Core behaviors:</span>
<span class="green">- Lead with the answer. No filler.</span>
<span class="green">- Read the file before asking. Come back with answers.</span>
<span class="green">- Never hallucinate. If you don't know, say so.</span>
<span class="green">- Default to action. Only ask when scope is ambiguous.</span>
    </div>
  </div>
""", "The identity section sets the persona and names the failure modes you want to prevent. 'Default to action' stops constant confirmation requests. These save 20 minutes per session."))

slides_html.append(slide("2.4", "Workflow style: kill the check-ins", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The line that changes everything</div>
    <div class="terminal">
<span class="comment">## Workflow Style</span>

Don't ask for confirmation on every step
during multi-step workflows.

<span style="color:var(--orange); font-size:1.3vw;">Execute the plan, show results, and only
pause if something fails or is genuinely ambiguous.</span>
    </div>
  </div>
""", "Without this line, Claude asks 'should I proceed?' after every step. With it, you give a task and come back to results. You're opting out of caution."))

slides_html.append(slide("2.4b", "Voice-to-Prompt", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Cut the friction</div>
    <div class="spawn-compare">
      <div class="spawn-col">
        <div class="spawn-label wrong">Typed</div>
        <div class="spawn-code">"write cold email for acme"</div>
        <div class="spawn-token bad" style="font-size:1.2vw;">Half the context missing.<br>Two correction turns wasted.</div>
      </div>
      <div class="spawn-col">
        <div class="spawn-label right">Dictated (30 sec)</div>
        <div class="spawn-code">"Two-step cold email for Acme Corp,<br>VP of Sales, just raised Series B,<br>Salesforce but no sequences tool,<br>use ICP pain angle, Step 1 &lt;80 words,<br><span class="highlight">Step 2 reframes — don't follow up</span>"</div>
        <div class="spawn-token good" style="font-size:1.2vw;">Full context. First draft usable.</div>
      </div>
    </div>
  </div>
""", "When you type, you abbreviate. When you dictate, you naturally give complete context. Operators who dictate prompts get higher-quality first drafts. The prompt is the brief — briefings spoken out loud are always more complete."))

slides_html.append(slide("2.5", "Work routing", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Work routing table</div>
    <table class="slide-table">
      <thead><tr><th>Work Type</th><th>Destination</th></tr></thead>
      <tbody>
        <tr><td>Cold email, campaigns</td><td class="orange">campaigns/</td></tr>
        <tr><td>ICP, voice, messaging</td><td class="orange">company/</td></tr>
        <tr><td>LinkedIn, content</td><td class="orange">content/</td></tr>
        <tr><td>Data tools, scripts</td><td class="orange">tools/</td></tr>
        <tr><td>Client-specific work</td><td class="orange">clients/[client-name]/</td></tr>
      </tbody>
    </table>
  </div>
""", "Routing matters because Claude will create files. Without routing instructions it guesses wrong half the time. Five minutes to write, saves you from hunting misplaced files indefinitely."))

slides_html.append(slide("2.6", "Rules: the two that matter", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Start with two</div>
    <div class="terminal">
.claude/rules/
<span style="color:var(--orange);">├── ask-vs-act.md          ← start here</span>
<span style="color:var(--orange);">├── scope-before-execute.md ← start here</span>
<span class="comment">├── workflow.md</span>
<span class="comment">├── file-conventions.md</span>
<span class="comment">├── context-and-tools.md</span>
<span class="comment">├── archive-safety.md</span>
<span class="comment">└── prompt-library.md</span>
    </div>
  </div>
""", "Seven rules in the repo. You don't need all seven on day one. Ask-vs-act and scope-before-execute change your daily work immediately. Add the others as you hit the problems they solve."))

slides_html.append(slide("2.6b", "Without the rule: the confirmation loop", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The default behavior</div>
    <div class="terminal" style="font-size:1.05vw;">
<span class="prompt">User:</span>  Build a cold email sequence for Acme Corp.

<span style="color:#e07070;">Claude: I'll start by researching Acme Corp. Should I proceed?</span>
<span class="prompt">User:</span>  Yes.
<span style="color:#e07070;">Claude: Research complete. Should I run the ICP research skill?</span>
<span class="prompt">User:</span>  Yes.
<span style="color:#e07070;">Claude: ICP score is 18/25. Should I write the sequence?</span>
<span class="prompt">User:</span>  Yes.
<span class="comment">...three more confirmations later</span>
    </div>
  </div>
""", "This is the default. Every step, a confirmation request. For a five-step task that takes 20 minutes, you're answering questions for the first 10. The ask-vs-act rule closes this in six lines."))

slides_html.append(slide("2.7", "Ask vs Act rule", """
  <div style="width:100%;">
    <div class="compare">
      <div class="compare-col">
        <div class="compare-head" style="color:#e07070; border-color:#e07070;">ASK first</div>
        <div class="compare-item">Destructive / irreversible action</div>
        <div class="compare-item">Scope ambiguous → wrong direction</div>
        <div class="compare-item">Genuinely unclear intent</div>
      </div>
      <div class="compare-col">
        <div class="compare-head" style="color:var(--green); border-color:var(--green);">ACT immediately</div>
        <div class="compare-item">User said build / create / implement</div>
        <div class="compare-item">Next step obvious from context</div>
        <div class="compare-item">Plan approved → execute, don't re-ask</div>
      </div>
    </div>
  </div>
""", "I'm going to show you this rule firing live. Watch what happens when I give a vague instruction — it doesn't ask a checklist, it states assumptions and moves. That behavior comes entirely from this rule file."))

slides_html.append(slide("2.7b", "Permission Escalation: Never Bypass", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Trust is earned, not granted</div>
    <div class="terminal">
Stage 1: Ask every edit          <span class="comment">← Start here. Always.</span>
  <span style="color:var(--dim);">↓ after seeing 10+ good decisions</span>
Stage 2: Approve bash once       <span class="comment">← Trust expands with evidence</span>
  <span style="color:var(--dim);">↓ after consistent output on known task types</span>
Stage 3: Trust within scope      <span class="comment">← Defined task, bounded context</span>

<span style="color:#e07070;">✗  Bypass permissions</span> <span class="comment">— you lose visibility, not just safety</span>
<span style="color:#e07070;">✗  Full auto mode on unfamiliar work</span> <span class="comment">— no telemetry, no escape hatch</span>
    </div>
  </div>
""", "Trust is earned, not granted. Start with Claude asking for approval on every edit — that's building the mental model. After 10 good decisions, expand. The two things you never do: bypass permissions and enable full auto mode on unfamiliar work. You lose visibility. You can't improve what you can't observe."))

slides_html.append(slide("2.7c", "Hooks: Automation That Fires Itself", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Events, not invocations</div>
    <div class="terminal" style="font-size:0.95vw;">
<span class="comment">// .claude/settings.json</span>
{
  <span style="color:var(--orange);">"hooks"</span>: {
    <span style="color:var(--orange);">"PostToolUse"</span>: [{
      <span style="color:var(--orange);">"matcher"</span>: <span style="color:var(--green);">"Write"</span>,
      <span style="color:var(--orange);">"hooks"</span>: [{ <span style="color:var(--orange);">"type"</span>: <span style="color:var(--green);">"command"</span>, <span style="color:var(--orange);">"command"</span>: <span style="color:var(--green);">"bun typecheck"</span> }]
    }],
    <span style="color:var(--orange);">"Stop"</span>: [{
      <span style="color:var(--orange);">"hooks"</span>: [{ <span style="color:var(--orange);">"type"</span>: <span style="color:var(--green);">"command"</span>, <span style="color:var(--orange);">"command"</span>: <span style="color:var(--green);">"powershell .claude/on-stop.ps1"</span> }]
    }]
  }
}
    </div>
    <div class="slide-sub" style="margin-top:1vw;">Events: PreToolUse / PostToolUse / Stop / Notification — set once, runs every session.</div>
  </div>
""", "Hooks are the automation layer of the automation layer. A hook fires automatically on a Claude Code event. Real examples: type-checker after every file write, Telegram notification when a long task finishes, logging hook for every tool call. Set them once — the behavior becomes structural."))

slides_html.append(slide("2.8", "Chapter close", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Foundation set</div>
    <ul class="bullet-list" style="text-align:left; max-width:60%; margin:2vw auto;">
      <li class="check">CLAUDE.md — operator brief written</li>
      <li class="check">Rules — ask-vs-act + scope-before-execute</li>
      <li class="check">Workspace — routing table in place</li>
    </ul>
    <div class="slide-sub" style="margin-top:2vw;">Next: Skills — the compound interest of this system.</div>
  </div>
""", "Foundation is set. The next chapter is where it gets interesting — skills. Every hour you spend writing a good skill gets paid back every time that skill runs.", "center"))

# ── CH 3 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("3.1", "Skills — the claim", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Chapter 3 — Skills</div>
    <div class="slide-headline xl" style="text-align:center;">Your best SDR's<br>playbook, encoded<br>in 40 lines.</div>
    <div class="slide-rule" style="margin:1.5vw auto;"></div>
    <div style="font-size:1.6vw; color:var(--orange); text-align:center;">Runs without them.</div>
  </div>
""", "A skill file is a constraint system. Not a tutorial, not a template — a constraint. It tells Claude exactly what inputs to expect, what format to output, what the failure modes are, and what the insider knowledge is.", "title"))

slides_html.append(slide("3.1b", "Skills UX: Institutionalized Expertise", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Without vs With</div>
    <table class="slide-table">
      <thead><tr><th>Without Skills</th><th>With Skills</th></tr></thead>
      <tbody>
        <tr><td>Write the prompt from memory each time</td><td class="green">/skill-name — one command</td></tr>
        <tr><td>Quality varies by how well you remembered it</td><td class="green">Same output spec every run</td></tr>
        <tr><td>No version history</td><td class="green">Versioned in git</td></tr>
        <tr><td>Can't share with team</td><td class="green">Team pulls the same skill</td></tr>
        <tr><td>Improve per session — no compounding</td><td class="green">Iterate once — all future runs benefit</td></tr>
      </tbody>
    </table>
  </div>
""", "The UX of skills is the difference between 'I know how to do this' and 'the system knows how to do this.' Without skills, quality degrades after a 14-hour day. With skills, you update the skill once and every future run gets the improvement. That's the compounding — not individual outputs, but what happens over 200 runs."))

slides_html.append(slide("3.2", "What a skill looks like", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Skill structure</div>
    <div class="terminal">
skills/cold-email/
└── SKILL.md
    ├── <span style="color:var(--dim);">## Define</span>            <span class="comment">← what this skill produces</span>
    ├── <span style="color:var(--dim);">## Uses</span>              <span class="comment">← when to call it</span>
    ├── <span style="color:var(--orange); font-weight:700;">## Insider Knowledge</span>  <span class="comment">← ← ← the moat</span>
    ├── <span style="color:var(--dim);">## Format</span>            <span class="comment">← exact output structure</span>
    └── <span style="color:var(--dim);">## Quality Gates</span>     <span class="comment">← what makes an output bad</span>
    </div>
  </div>
""", "Five sections. Most people write the first two and stop. The insider knowledge section and quality gates are where the actual leverage is — and they're the sections that take experience to write well."))

slides_html.append(slide("3.2b", "The Description Field Is Claude's Router", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Front-load the use case</div>
    <div class="terminal">
<span style="color:#e07070; font-weight:700;">WRONG:</span>
description: Code review tool

<span style="color:var(--green); font-weight:700;">RIGHT:</span>
description: Review code for bugs, security issues, and maintainability.
Use when reviewing pull requests, checking code quality, analyzing diffs,
or when user says "review", "PR", "code quality", or "check this."
Trigger keywords: review, PR, diff, quality, security.
    </div>
    <div class="slide-sub" style="margin-top:1vw;">Under 50 characters = invoked 3–5x less often. Write it like a dispatch rule, not a label.</div>
  </div>
""", "The description field is the single most important thing you write in a skill. Claude scans every skill's description before deciding which to invoke. Three things: what it does, when to use it, and three or more explicit trigger keywords. Front-load the use case in the first 250 characters."))

slides_html.append(slide("3.3", "The insider knowledge section", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The moat</div>
    <div class="terminal">
<span style="color:var(--orange);">## Insider Knowledge</span>

- Subject lines under 6 words outperform longer ones for this ICP
- Never open with "I" — open with them
- Step 2 should <span class="green">reframe</span>, not follow up
- Use single-brace variables: <span style="color:#f0c080;">{'{'}FIRST_NAME{'}'}, {'{'}COMPANY{'}'}, {'{'}PAIN_POINT{'}'}</span>
- No links. No attachments. One CTA max.
    </div>
  </div>
""", "This section is what makes your skill different from a generic prompt. It encodes what you've learned from running hundreds of campaigns. When you hire a new person, you onboard them. This is how you onboard Claude."))

slides_html.append(slide("3.3b", "Six Patterns: What Working Skills Have in Common", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Pre-flight checklist</div>
    <div class="terminal" style="font-size:0.95vw;">
Pattern 1: Description = routing document  <span class="comment">→ WHEN, not just WHAT. 3+ trigger keywords.</span>
Pattern 2: Directive, not conversational   <span class="comment">→ Imperative verbs. Numbered steps.</span>
Pattern 3: Explicit output format          <span class="comment">→ Define the structure. Same result every time.</span>
Pattern 4: Read first                      <span class="comment">→ Tell Claude to look before it acts.</span>
Pattern 5: Out of Scope section            <span class="comment">→ Name what the skill does NOT do.</span>
Pattern 6: Under 500 lines                 <span class="comment">→ Long skills lose focus. Split them.</span>
    </div>
  </div>
""", "These six patterns show up in 100% of skills that work — and are almost entirely absent from skills that don't. Pattern 3 (output format) is where most custom skills fail: they tell Claude what to do but not what the result should look like. Pattern 6 (under 500 lines) is a hard limit — every skill loads into context, and a 2000-line skill costs 5000+ tokens before doing anything."))

slides_html.append(slide("3.4", "Live: Build the cold-email skill", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Live build</div>
    <div class="terminal" style="text-align:left; display:inline-block; margin-top:2vw; padding:2vw 3vw;">
      <span style="color:var(--orange); font-size:1.5vw; font-weight:700;">[LIVE SEGMENT]</span>
      <div style="margin-top:1vw; color:var(--dim); font-size:1.1vw;">Building cold-email/SKILL.md from scratch.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show bad output before quality gates.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show good output after. The contrast is the point.</div>
    </div>
  </div>
""", "[LIVE SEGMENT — build each section, explain as you go. Show what a bad output looks like before adding the quality gates. Show good output after. Keep the pace fast — 12-15 minutes max. Don't read the code aloud line-by-line; talk about what each section is doing and why.]", "center"))

slides_html.append(slide("3.5", "Live: Run it on a real company", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Live run</div>
    <div class="terminal" style="text-align:left; display:inline-block; margin-top:2vw; padding:2vw 3vw;">
      <span style="color:var(--orange); font-size:1.5vw; font-weight:700;">[LIVE SEGMENT]</span>
      <div style="margin-top:1vw; color:var(--dim); font-size:1.1vw;">ICP research output → cold-email skill → sequence.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show generic output (no insider knowledge).</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show specific output (insider knowledge filled in).</div>
      <div style="margin-top:0.5vw; color:var(--orange); font-size:1.1vw;">Let silence sit while the viewer reads the output.</div>
    </div>
  </div>
""", "[LIVE SEGMENT — take one of the research outputs from the ICP research skill, feed it into cold-email. Show the output. Then show what happens without insider knowledge — generic. Then with it — specific. That contrast is the point. Let silence sit while the viewer reads.]", "center"))

slides_html.append(slide("3.5b", "Test Before Shipping", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The ritual</div>
    <div style="display:flex; align-items:center; gap:1vw; width:100%; margin-bottom:2vw;">
      <div style="flex:1; background:var(--surface); border-left:3px solid var(--orange); padding:1vw 1.2vw;">
        <div style="color:var(--orange); font-weight:700; font-size:1.2vw;">BUILD</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">All 5 sections</div>
      </div>
      <div style="color:var(--gray); font-size:1.5vw;">→</div>
      <div style="flex:1; background:var(--surface); border-left:3px solid var(--orange); padding:1vw 1.2vw;">
        <div style="color:var(--orange); font-weight:700; font-size:1.2vw;">REAL DATA</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">5 actual companies</div>
      </div>
      <div style="color:var(--gray); font-size:1.5vw;">→</div>
      <div style="flex:1; background:var(--surface); border-left:3px solid var(--orange); padding:1vw 1.2vw;">
        <div style="color:var(--orange); font-weight:700; font-size:1.2vw;">FIX</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">Until gates pass</div>
      </div>
      <div style="color:var(--gray); font-size:1.5vw;">→</div>
      <div style="flex:1; background:var(--surface); border-left:3px solid var(--green); padding:1vw 1.2vw;">
        <div style="color:var(--green); font-weight:700; font-size:1.2vw;">SHIP</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">Confident. Not hopeful.</div>
      </div>
    </div>
    <div class="quote-block">
      <div class="quote-text">"A skill that hasn't run on real data is a draft. Not a deliverable."</div>
    </div>
  </div>
""", "Build all 5 sections. Run on 5 actual companies — not invented examples. Fix where it breaks. 8/10 outputs passing gates without manual correction = deliverable. Below that = draft. Fast garbage is worse than slow correctness."))

slides_html.append(slide("3.6", "Quality gates", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Automated QA</div>
    <div class="terminal">
<span style="color:var(--orange);">## Quality Gates</span>

<span class="green">- [ ]</span> Subject line: under 8 words, not a question, not clickbait
<span class="green">- [ ]</span> Step 1 body: under 100 words
<span class="green">- [ ]</span> Step 2 body: under 80 words, different angle from Step 1
<span class="green">- [ ]</span> No links or attachments in either step
<span class="green">- [ ]</span> No "I hope this finds you well" or equivalent
<span class="green">- [ ]</span> One CTA max — one question, not a pitch
    </div>
  </div>
""", "Quality gates are the automated QA layer. Every time this skill runs, these constraints fire. You write them once from your list of things you've had to manually fix. Run the skill 10 times before you consider it done."))

slides_html.append(slide("3.6b", "Output Calibration: Three Failure Modes", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Fix upstream, not downstream</div>
    <div class="terminal" style="font-size:0.95vw;">
<span style="color:#e07070; font-weight:700;">Mode 1: Wrong direction</span>
  Claude misread the intent entirely
  Fix: CLAUDE.md or skill prompt is ambiguous <span class="comment">— rewrite it</span>

<span style="color:#d4a017; font-weight:700;">Mode 2: Right direction, bad quality</span>
  Claude understood but produced mediocre output
  Fix: Add one real example to the skill
       <span style="color:var(--green);">One example beats 500 words of instruction</span>

<span style="color:#b0b030; font-weight:700;">Mode 3: Can't tell if it's good</span>
  No quality standard defined <span class="comment">— nothing to check against</span>
  Fix: Define success criteria in the skill before running
       <span style="color:var(--dim);">"Good = reply rate &gt; 1%, subject &lt; 8 words, no links"</span>

<span style="color:var(--orange); font-weight:700;">Rule: Bad output is a skill authoring problem. Fix upstream.</span>
    </div>
  </div>
""", "Don't call it debugging — call it output calibration. The fix is almost never in Claude, it's in the skill. Wrong direction: fix the writing. Right direction, bad quality: add one concrete example — Claude pattern-matches faster from examples than from prose. Can't tell if it's good: you never defined what success looks like."))

slides_html.append(slide("3.7", "Skills trigger automatically", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Progressive disclosure</div>
    <table class="slide-table">
      <thead><tr><th>Trigger situation</th><th>Skill that loads</th></tr></thead>
      <tbody>
        <tr><td>Code edit / refactor / new file</td><td class="orange">engineering-discipline</td></tr>
        <tr><td>API error / raw content pasted</td><td class="orange">task-discipline</td></tr>
        <tr><td>Any work under clients/</td><td class="orange">client-discipline</td></tr>
      </tbody>
    </table>
    <div class="slide-sub" style="margin-top:1.5vw;">Open a client file → client-discipline loads automatically. You don't invoke it. The rule handles it.</div>
  </div>
""", "You don't load all the constraints all the time. You load the ones relevant to what you're doing right now. Keeps context lean, keeps the system fast."))

slides_html.append(slide("3.7b", "Why Your Skill Isn't Firing: The 7-Point Diagnostic", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Triage sheet</div>
    <div style="display:flex; gap:3vw; width:100%;">
      <div style="flex:1;">
        <div style="color:#e07070; font-weight:700; font-size:1.1vw; margin-bottom:0.8vw; font-family:'Fira Code',monospace;">DESCRIPTION FAILURES:</div>
        <div style="color:var(--dim); font-size:1vw; line-height:1.8;">□ Under 50 characters<br>□ No trigger keywords<br>□ No use case in first 250 chars</div>
      </div>
      <div style="flex:1;">
        <div style="color:#d4a017; font-weight:700; font-size:1.1vw; margin-bottom:0.8vw; font-family:'Fira Code',monospace;">CONTENT FAILURES:</div>
        <div style="color:var(--dim); font-size:1vw; line-height:1.8;">□ Conversational instead of directive<br>□ No output format specified<br>□ No "read first" step<br>□ Over 1000 lines</div>
      </div>
    </div>
    <div class="slide-sub" style="margin-top:1.5vw;">3+ of these = your skill is probably broken. Test: ask Claude without /invoking it manually — does it pick the right skill?</div>
  </div>
""", "Pull up your weakest skill — the one Claude never invokes. Run it through this list. If it fails three or more checks, that's your answer. The test at the bottom is the fastest diagnostic: ask Claude to do the thing without manually typing /skill-name. If it routes correctly, the description is working."))

slides_html.append(slide("3.8", "Skills — compound interest", """
  <div style="width:100%; text-align:center;">
    <div class="slide-headline xl" style="text-align:center;">Compound interest.</div>
    <div class="slide-rule" style="margin:1.5vw auto;"></div>
    <div style="font-size:1.8vw; color:var(--dim); text-align:center; font-family:'Lora',serif; font-style:italic;">30 minutes to write. Runs correctly forever.</div>
    <div class="slide-sub" style="margin-top:2vw; text-align:center;">Next: Agents — stop running one skill at a time.</div>
  </div>
""", "You spend 30 minutes writing a good skill, and it runs correctly every time for the rest of your agency's life. Fork the skills in the repo, fill in your insider knowledge.", "title"))

# ── CH 4 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("4.1", "Agents — the claim", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Chapter 4 — Agents</div>
    <div class="slide-headline xl" style="text-align:center;">1 operator<br>+ agents<br>= agency output</div>
  </div>
""", "An agent is an isolated worker you spawn. It has its own context window, its own tool access, and it runs independently. While you're in one conversation, three agents can be researching three different companies simultaneously.", "title"))

slides_html.append(slide("4.2", "Skills vs Agents", """
  <div style="width:100%;">
    <div class="compare">
      <div class="compare-col">
        <div class="compare-head">Skills</div>
        <div class="compare-item">SOPs — what to do</div>
        <div class="compare-item">Called with a task</div>
        <div class="compare-item">Constrain output format</div>
        <div class="compare-item">Run in your session</div>
      </div>
      <div class="compare-col">
        <div class="compare-head" style="color:var(--orange); border-color:var(--orange);">Agents</div>
        <div class="compare-item">Workers — who does it</div>
        <div class="compare-item">Spawned with a mission</div>
        <div class="compare-item">Constrain model and tools</div>
        <div class="compare-item">Run independently</div>
      </div>
    </div>
  </div>
""", "Mental model: skills are playbooks, agents are the people who run them. You spawn an agent when the task would burn too much of your main context to do yourself."))

slides_html.append(slide("4.3", "The three agents", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Agent roster</div>
    <div class="arch-layers">
      <div class="arch-layer" style="border-color:var(--green);">
        <span class="layer-name" style="color:var(--green);">smart-searcher</span>
        <span class="layer-arrow" style="color:var(--gray);">[Haiku]</span>
        <span class="layer-desc">Discovery — spawn first, always. Near-zero cost.</span>
        <span class="layer-tag">Always first</span>
      </div>
      <div class="arch-layer">
        <span class="layer-name">task-orchestrator</span>
        <span class="layer-arrow" style="color:var(--gray);">[Sonnet]</span>
        <span class="layer-desc">Route complex multi-step tasks</span>
      </div>
      <div class="arch-layer">
        <span class="layer-name">researcher</span>
        <span class="layer-arrow" style="color:var(--gray);">[Sonnet]</span>
        <span class="layer-desc">Company + market research, synthesis</span>
      </div>
    </div>
  </div>
""", "Three agents cover 90% of GTM work. Smart-searcher is Haiku — it costs almost nothing and finds whatever you need before you waste expensive model time."))

slides_html.append(slide("4.3b", "Building an Agent: The File Format", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Agent frontmatter</div>
    <div style="display:flex; gap:3vw; width:100%; align-items:flex-start;">
      <div style="flex:1.5;">
        <div class="terminal" style="font-size:0.95vw;">
---
<span style="color:var(--orange);">name</span>: cold-email-reviewer
<span style="color:var(--orange);">description</span>: Reviews cold email copy for ICP fit, tone, and CTA.
         Use after writing a sequence.
<span style="color:var(--orange);">tools</span>: Read, Grep, Glob
<span style="color:var(--orange);">model</span>: sonnet
---

You are a cold email QA reviewer. When invoked:
1. Read the sequence files
2. Check each email against the ICP in company/ICP.md
3. Flag any language that sounds like AI slop
        </div>
      </div>
      <div style="flex:1;">
        <table class="slide-table" style="font-size:0.95vw;">
          <thead><tr><th>Scope</th><th>Path</th></tr></thead>
          <tbody>
            <tr><td>Project</td><td class="orange">.claude/agents/</td></tr>
            <tr><td>Global</td><td class="orange">~/.claude/agents/</td></tr>
          </tbody>
        </table>
        <div class="slide-sub" style="margin-top:1vw;">If names conflict, project wins.</div>
      </div>
    </div>
  </div>
""", "An agent is just a Markdown file with frontmatter. Five fields: name, description, tools, model, and the prompt below the dashes. The description field is the most important line — Claude Code reads it to decide which agent to call. Write it like a dispatch rule. Project-level agents check into git and travel with the repo."))

slides_html.append(slide("4.4", "The spawn pattern", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The pattern that keeps context clean</div>
    <div class="spawn-compare">
      <div class="spawn-col">
        <div class="spawn-label wrong">✗ WRONG</div>
        <div class="spawn-code">Main reads files<br>→ understands<br>→ edits<br>→ reports</div>
        <div class="spawn-token bad">2,000+ tokens<br><span style="font-size:1vw; color:var(--gray);">on discovery alone</span></div>
      </div>
      <div class="spawn-col">
        <div class="spawn-label right">✓ RIGHT</div>
        <div class="spawn-code">Main spawns researcher()<br><span class="highlight">→ researcher reads &amp; edits</span><br>→ Main gets summary<br><span class="highlight">Main stays clean</span></div>
        <div class="spawn-token good">200 tokens<br><span style="font-size:1vw; color:var(--gray);">back to main</span></div>
      </div>
    </div>
  </div>
""", "This pattern is the single biggest context efficiency in the system. Every token your main session uses on file-reading is a token not available for actual work. Spawn, don't read."))

slides_html.append(slide("4.4b", "Context Forking: Inherit the Room", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Start blind vs. start knowing</div>
    <table class="slide-table">
      <thead><tr><th></th><th>Default</th><th>Fork</th></tr></thead>
      <tbody>
        <tr><td>Starting context</td><td class="dim">Blank</td><td class="green">Copy of parent at fork time</td></tr>
        <tr><td>Cache sharing</td><td class="dim">None</td><td class="green">Children 2-N ~10x cheaper on input</td></tr>
        <tr><td>Tool call isolation</td><td class="green">Yes</td><td class="green">Yes — still isolated</td></tr>
        <tr><td>Use when</td><td class="dim">Clean, independent research</td><td class="orange">Agent needs your accumulated context</td></tr>
      </tbody>
    </table>
    <div class="terminal" style="margin-top:1.5vw; font-size:0.95vw;">
<span class="comment"># Fork: agent inherits your full context at this moment</span>
export CLAUDE_CODE_FORK_SUBAGENT=1
<span class="comment"># Or fork a single spawn on demand</span>
/fork
    </div>
  </div>
""", "By default, a subagent starts with blank context. But if you've spent an hour building context — client brief, campaign history, targeting rules — you want the agent to start from THAT. Forking solves it. All forked subagents share your prompt cache prefix — every agent after the first costs ~10x less on input tokens."))

slides_html.append(slide("4.5", "Live: Three agents in parallel", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Live demo</div>
    <div class="terminal" style="text-align:left; display:inline-block; margin-top:2vw; padding:2vw 3vw;">
      <span style="color:var(--orange); font-size:1.5vw; font-weight:700;">[LIVE SEGMENT]</span>
      <div style="margin-top:1vw; color:var(--dim); font-size:1.1vw;">Spawn researcher on three companies simultaneously.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show results arriving. Synthesize into one brief.</div>
      <div style="margin-top:0.5vw; color:var(--orange); font-size:1.1vw;">Show the clock — three companies in the time it takes to do one manually.</div>
    </div>
  </div>
""", "[LIVE SEGMENT — spawn researcher on three different companies. While they run, explain what each one is doing. When results come back, show how the main session synthesizes them into a single campaign brief. Timing matters here — show the clock. Don't rush the silence while agents run.]", "center"))

slides_html.append(slide("4.5b", "Context Hygiene", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Long sessions degrade silently</div>
    <div class="terminal">
Session length → output quality:

  <span style="color:var(--green);">████████████████</span><span style="color:#d4a017;">▓▓▓▓</span><span style="color:#e07070;">░░░░░░</span>
  Start          /compact   Fresh session
  (sharp)        (mid-task)  (new task)

Rules:
  <span style="color:var(--orange);">/compact</span>   → mid-task when context is bloating, not between tasks
  <span style="color:var(--orange);">Fresh</span>      → any genuinely new task, especially after a complex one
  <span style="color:var(--orange);">HANDOFF.md</span> → write what you know before closing a session
    </div>
  </div>
""", "Long sessions produce worse output, and they don't announce it. By the time it's obvious, you've gotten 20 minutes of degraded output. Use /compact mid-task. Start fresh for new tasks. Before closing any session, write a HANDOFF.md — one paragraph. The session ends and context is gone. The file stays."))

slides_html.append(slide("4.5c", "The Escape Hatch", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Stopping Claude is a normal workflow move</div>
    <div style="display:flex; gap:3vw; width:100%;">
      <div style="flex:1;">
        <div style="color:var(--orange); font-weight:700; font-size:1.1vw; margin-bottom:0.8vw;">Signals Claude has gone sideways:</div>
        <ul class="bullet-list" style="font-size:1vw;">
          <li>Responses getting vague or circular</li>
          <li>Actions outside the stated scope</li>
          <li>Confident assertions it should be reading from a file</li>
          <li>Context thin — quality dropping</li>
        </ul>
      </div>
      <div style="flex:1;">
        <div style="color:var(--green); font-weight:700; font-size:1.1vw; margin-bottom:0.8vw;">When you see it:</div>
        <div class="terminal" style="font-size:1vw;">
<span style="color:#e07070;">Ctrl+C</span>  → escape

Diagnose:
  What was ambiguous?
  Did context run out?
  Was scope too wide?

Restart clean:
  Fresh session + tighter scope
  + one new guardrail
        </div>
      </div>
    </div>
  </div>
""", "The failure is pushing through when you can see it's gone sideways — that's how you get 20 minutes of bad output that's expensive to reverse. Ctrl+C, diagnose, restart with a tighter brief and one new guardrail. That guardrail is the most valuable one you'll write — it came from real failure, not a guess."))

slides_html.append(slide("4.5d", "Reading Claude's Telltales", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Early warning signals</div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1vw; width:100%;">
      <div style="background:var(--surface); border-left:3px solid #d4a017; padding:1vw 1.5vw;">
        <div style="color:#d4a017; font-weight:700; font-size:1.15vw;">⚠ Hedging language</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">"I believe" / "it seems likely" where it used to just answer</div>
      </div>
      <div style="background:var(--surface); border-left:3px solid #d4a017; padding:1vw 1.5vw;">
        <div style="color:#d4a017; font-weight:700; font-size:1.15vw;">⚠ Length drift</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">Shorter without getting denser — compressed, not concise</div>
      </div>
      <div style="background:var(--surface); border-left:3px solid #d4a017; padding:1vw 1.5vw;">
        <div style="color:#d4a017; font-weight:700; font-size:1.15vw;">⚠ Re-asking questions</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">Asking something you answered 2 turns ago → context loss</div>
      </div>
      <div style="background:var(--surface); border-left:3px solid #d4a017; padding:1vw 1.5vw;">
        <div style="color:#d4a017; font-weight:700; font-size:1.15vw;">⚠ Generalization slip</div>
        <div style="color:var(--dim); font-size:1vw; margin-top:0.3vw;">Specific ICP advice → generic GTM advice</div>
      </div>
    </div>
    <div style="margin-top:1.5vw; font-size:1.4vw; color:var(--cream);">Two of these together: <span class="orange">/compact</span> (mid-task) or start fresh. Don't push through.</div>
  </div>
""", "Claude doesn't announce when output quality drops. Read the telltales. Two signals together = intervene. The next 20 minutes will be worse than the last 20 if you push through."))

slides_html.append(slide("4.6", "How smart-searcher finds its tools", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Knowledge graph-backed discovery</div>
    <div class="terminal">
<span class="comment"># smart-searcher runs this internally before any task</span>
<span class="prompt">$</span> bun knowledge-graph/scripts/kg-skill-graph.js --query <span style="color:var(--green);">"write outbound sequence"</span>
<span style="color:var(--green);">→ skills/cold-email/SKILL.md</span>

<span class="comment"># Result: main session loads the right skill, not a generic prompt</span>
    </div>
    <div class="slide-sub" style="margin-top:1.5vw;">Index your workspace once with kg-index.js. From that point forward, smart-searcher finds the right skill for any task automatically.</div>
  </div>
""", "Smart-searcher doesn't guess what skill to load — it queries the knowledge graph first. You index your workspace once, and from that point forward, smart-searcher finds the right skill automatically. Once your library grows past 20 skills, you can't hold the full skill map in your head — the graph holds it for you."))

slides_html.append(slide("4.7", "Chapter close", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">One pattern</div>
    <div class="slide-headline xl" style="text-align:center;">Spawn,<br>don't read.</div>
    <div class="slide-sub" style="margin-top:2vw; text-align:center;">Next: The Enrichment Waterfall — agents + skills as a single pipeline.</div>
  </div>
""", "Three agents, one pattern. Always spawn smart-searcher first for discovery, task-orchestrator for complex routing, researcher for deep company work.", "title"))

slides_html.append(slide("4.7b", "GSD: Managing Multi-Phase Work", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Project lifecycle across sessions</div>
    <div class="terminal" style="font-size:0.95vw;">
Phase defined (goal + success criteria)
  <span style="color:var(--dim);">↓</span> <span style="color:var(--orange);">/gsd:plan-phase</span>
Detailed task breakdown with dependencies
  <span style="color:var(--dim);">↓</span> <span style="color:var(--orange);">/gsd:execute-phase</span>
Agents execute — tasks tracked in real time
  <span style="color:var(--dim);">↓</span> <span style="color:var(--orange);">/gsd:verify-work</span>
Goal-backward check: did we hit the goal?
<span style="color:#e07070;">(tasks completing ≠ goal achieved)</span>
  <span style="color:var(--dim);">↓</span> <span style="color:var(--orange);">/gsd:pause-work</span>
HANDOFF.md written — context preserved for next session
  <span style="color:var(--dim);">↓</span> <span style="color:var(--orange);">/gsd:resume-work</span>
Next session picks up exactly where you left off
    </div>
  </div>
""", "Skills and agents handle individual tasks. GSD handles the project. The critical distinction is the verify step: not 'did the tasks complete' but 'did we achieve the goal?' Those are different questions. Tasks can complete while the phase goal remains unmet. GSD enforces that distinction."))

slides_html.append(slide("4.7c", "lg-runtime: When Claude Can't Stay Awake", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Durable batch execution</div>
    <div class="compare">
      <div class="compare-col">
        <div class="compare-head" style="color:#e07070; border-color:#e07070;">Claude Code (interactive)</div>
        <div class="compare-item" style="color:var(--green);">Great for decisions, skill runs, human-in-the-loop</div>
        <div class="compare-item" style="color:#e07070;">Session-bounded — cuts off on long runs</div>
        <div class="compare-item" style="color:#e07070;">Can't queue 500 companies reliably</div>
      </div>
      <div class="compare-col">
        <div class="compare-head" style="color:var(--green); border-color:var(--green);">lg-runtime (Python/uv)</div>
        <div class="compare-item" style="color:var(--green);">Durable batch execution — runs while you sleep</div>
        <div class="compare-item" style="color:var(--green);">Resumable — picks up at record 247, not record 1</div>
        <div class="compare-item" style="color:var(--green);">Status logged — see what completed and what failed</div>
      </div>
    </div>
    <div style="margin-top:1.5vw; text-align:center; font-size:1.3vw; color:var(--orange); font-weight:600;">Claude Code (strategy + decisions) → lg-runtime (execution at volume)</div>
  </div>
""", "Claude Code is for interactive work — the back-and-forth, decisions, skill runs. When you need to enrich 500 companies overnight, Claude Code's session model becomes a constraint. lg-runtime runs durably. If it fails at record 247, it resumes from 247, not zero. They're different stages of the same pipeline."))

# ── CH 5 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("5.1", "The interface problem", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Chapter 5 — The Enrichment Waterfall</div>
    <div style="display:flex; align-items:center; gap:4vw; width:100%; margin-top:1vw;">
      <div style="flex:2;">
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.8vw; font-size:1.1vw; font-weight:600;">
          <span style="color:rgba(176,174,165,0.6);">Clay</span>
          <span style="color:rgba(176,174,165,0.5);">Apollo</span>
          <span style="color:rgba(176,174,165,0.55);">Instantly</span>
          <span style="color:rgba(176,174,165,0.45);">N8n</span>
          <span style="color:rgba(176,174,165,0.6);">Notion</span>
          <span style="color:rgba(176,174,165,0.4);">Sheets</span>
          <span style="color:rgba(176,174,165,0.5);">ChatGPT</span>
          <span style="color:rgba(176,174,165,0.45);">Sales Nav</span>
          <span style="color:rgba(176,174,165,0.55);">Slack</span>
          <span style="color:rgba(176,174,165,0.4); grid-column:span 2;">Loom</span>
        </div>
        <div style="font-size:2vw; color:var(--gray); margin-top:1vw; font-weight:300;">10 interfaces</div>
      </div>
      <div style="font-size:3vw; color:var(--orange);">→</div>
      <div style="flex:1; text-align:center;">
        <div class="terminal" style="display:inline-block; padding:1.5vw 2vw;">
          <span class="prompt">$</span> _
        </div>
        <div style="font-size:1vw; color:var(--dim); margin-top:0.8vw;">one terminal</div>
      </div>
    </div>
  </div>
""", "Count the tabs. Clay, Apollo, Instantly, N8n, Notion, Sheets, ChatGPT, Sales Nav, Slack, Loom. That's ten interfaces to run one outbound function. What Claude Code solves isn't any one of those tools. It's the interface tax on all of them."))

slides_html.append(slide("5.2", "The waterfall concept", """
  <div style="width:100%;">
    <div class="slide-eyebrow">How it works</div>
    <div class="waterfall">
      <div class="wf-tier">
        <div class="tier-name">Tier 1 — Free sources</div>
        <div class="tier-items">Company website · LinkedIn · Crunchbase · Google AI Mode</div>
      </div>
      <div class="wf-arrow">↓ <span>(only on miss)</span></div>
      <div class="wf-tier">
        <div class="tier-name">Tier 2 — Cheap APIs</div>
        <div class="tier-items">TechSight (free) · OpenWebNinja ($0.002/query)</div>
      </div>
      <div class="wf-arrow">↓ <span>(only on miss)</span></div>
      <div class="wf-tier">
        <div class="tier-name">Tier 3 — Paid fallback</div>
        <div class="tier-items">Clay native integrations (edge cases only)</div>
      </div>
      <div class="wf-arrow">↓</div>
      <div class="wf-tier" style="border-color:var(--green);">
        <div class="tier-name" style="color:var(--green);">Enriched record</div>
        <div class="tier-items">70-80% of records stop at Tier 1 or 2</div>
      </div>
    </div>
  </div>
""", "The waterfall only goes down when the tier above it fails. Most records get enriched in Tier 1 or Tier 2 — you only hit paid APIs for the harder cases."))

slides_html.append(slide("5.3", "Tier 1: Free", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Tier 1 — Zero cost</div>
    <table class="slide-table">
      <thead><tr><th>Source</th><th>What it returns</th></tr></thead>
      <tbody>
        <tr><td>Company website</td><td>What they do, who they sell to, key claims</td></tr>
        <tr><td>LinkedIn company page</td><td>Headcount, recent hires, job postings</td></tr>
        <tr><td>Crunchbase (public)</td><td>Funding date, round size, investors</td></tr>
        <tr><td>Google AI Mode</td><td>Recent news, announcements, events</td></tr>
      </tbody>
    </table>
    <div class="slide-sub" style="margin-top:1.5vw;">Website + LinkedIn alone covers 60% of what you need for personalization. At zero cost.</div>
  </div>
""", "The company website alone gets you 60% of what you need for personalization. LinkedIn gets you headcount signal and job postings. Together, these two cover most of your list at zero cost."))

slides_html.append(slide("5.4", "Tier 2: TechSight", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Tier 2 — Free tech stack detection</div>
    <div class="terminal">
<span class="prompt">$</span> techsight acmecorp.com

Tech stack detected:
  <span class="green">✓</span> Salesforce     <span class="comment">(CRM)</span>
  <span class="green">✓</span> HubSpot        <span class="comment">(Marketing)</span>
  <span class="green">✓</span> Outreach       <span class="comment">(Sales engagement)</span>
  <span class="green">✓</span> Segment        <span class="comment">(Analytics)</span>
  <span class="green">✓</span> Intercom       <span class="comment">(Support)</span>

Cost: <span class="green">$0.00</span>
    </div>
  </div>
""", "TechSight is a free CLI that detects tech stack from a domain. We built it in-house, it's open source. For GTM work, tech stack is one of the most valuable enrichment signals. Hits on 80% of domains."))

slides_html.append(slide("5.5", "Tier 3: Paid fallback", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Tier 3 — Edge cases only</div>
    <table class="slide-table">
      <thead><tr><th>Tool</th><th>Cost</th><th>When it fires</th></tr></thead>
      <tbody>
        <tr><td>OpenWebNinja</td><td class="orange">$0.002/query</td><td>Website thin, LinkedIn sparse</td></tr>
        <tr><td>Clay</td><td class="orange">$X/credit</td><td>Complex signal workflows — Clay's native integrations</td></tr>
      </tbody>
    </table>
    <div class="slide-sub" style="margin-top:1.5vw;">When you do hit Clay, you're calling it from the same terminal as everything else — not logging in to a separate interface.</div>
  </div>
""", "Tier 3 only fires on misses. For records where the website is thin and LinkedIn is sparse. The script handles fallback logic automatically. Most of your list never touches this tier."))

slides_html.append(slide("5.6", "Clay vs. Waterfall", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The full comparison</div>
    <table class="slide-table">
      <thead><tr><th></th><th>Clay-only</th><th>Waterfall</th></tr></thead>
      <tbody>
        <tr><td><strong>Interface</strong></td><td style="color:#e07070;">Separate UI, credit dashboard, workflow builder</td><td class="green">Same terminal as everything else</td></tr>
        <tr><td>1,000 records</td><td style="color:#e07070;">$X</td><td class="green">~$Y</td></tr>
        <tr><td>Data ownership</td><td class="dim">Platform-dependent</td><td class="green">Yours forever</td></tr>
        <tr><td>Iteration</td><td class="dim">Change in Clay UI</td><td class="green">Change the script</td></tr>
      </tbody>
    </table>
  </div>
""", "The interface row is the lead. Clay is great but it's a separate context. The waterfall runs from the same terminal as your research agents, sequence generator, and Bison upload. One interface. The cost difference is real, but the bigger gain is stopping the interface tax."))

slides_html.append(slide("5.7", "Live: Waterfall on real companies", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Live run</div>
    <div class="terminal" style="text-align:left; display:inline-block; margin-top:2vw; padding:2vw 3vw;">
      <span style="color:var(--orange); font-size:1.5vw; font-weight:700;">[LIVE SEGMENT]</span>
      <div style="margin-top:1vw; color:var(--dim); font-size:1.1vw;">Run enrich.js on 5 real domains.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show which tier each company hits.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Show one record where Tier 1 and 2 miss → Tier 3 fires.</div>
      <div style="margin-top:0.5vw; color:var(--orange); font-size:1.1vw;">Point out the cost column accumulating in real time.</div>
    </div>
  </div>
""", "[LIVE SEGMENT — run enrich.js from the repo on 5 real companies. Show which tier each one hits. Show the structured output. Show one record where Tier 1 and 2 miss and Tier 3 fires. Keep commentary minimal — let the output speak. Point out the cost column so the viewer sees it accumulating in real time.]", "center"))

slides_html.append(slide("5.8", "Chapter close", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Infrastructure complete</div>
    <ul class="bullet-list">
      <li class="check">CLAUDE.md — briefed</li>
      <li class="check">Rules — in place</li>
      <li class="check">Skills — encoded</li>
      <li class="check">Agents — standing by</li>
      <li class="check">Waterfall — running</li>
    </ul>
    <div style="margin-top:2vw; font-size:2vw; font-weight:700; color:var(--orange);">Chapter 6 is where all of it runs.</div>
  </div>
""", "That's the infrastructure layer — complete. Chapter 6 is the main event. No prep, no safety net. A company I've never researched, with a timer running."))

# ── CH 6 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("6.1", "Cold start declaration", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Chapter 6 — The Live GTM Build</div>
    <div style="font-family:'Fira Code',monospace; font-size:5vw; color:var(--cream); letter-spacing:-1px; margin:2vw 0;">stackbridge.io</div>
    <div class="slide-sub" style="text-align:center;">I've never looked at this company before. Timer starts now.</div>
  </div>
""", "This is the company. I've never looked at it before. Everything we've built in chapters 1 through 5 is already in place. Timer starts now.", "title"))

slides_html.append(slide("6.2", "What you're about to watch", """
  <div style="width:100%;">
    <div class="slide-eyebrow">The sequence — timer on screen</div>
    <ol class="num-list">
      <li><span class="n">1</span><span>Spawn researcher agent on the company</span></li>
      <li><span class="n">2</span><span>Run ICP research skill against the output</span></li>
      <li><span class="n">3</span><span>Run enrichment waterfall</span></li>
      <li><span class="n">4</span><span>Generate cold-email Step 1 + Step 2 from research</span></li>
      <li><span class="n">5</span><span>QA against quality gates</span></li>
      <li><span class="n">6</span><span>Upload to Bison via CLI</span></li>
      <li><span class="n">7</span><span>Set campaign live</span></li>
    </ol>
  </div>
""", "No setup, no warm-up. Everything you need to follow along is in the repo — the before/ folder is the starting state. The after/ folder is what this session produces."))

slides_html.append(slide("6.3", "Post-build debrief", """
  <div style="width:100%;">
    <div class="compare">
      <div class="compare-col" style="text-align:center;">
        <div class="compare-head" style="text-align:center;">Time elapsed</div>
        <div style="font-size:6vw; font-weight:700; color:var(--orange); line-height:1; margin-top:1vw;">[X]<br><span style="font-size:2vw; color:var(--dim);">minutes</span></div>
      </div>
      <div class="compare-col">
        <div class="compare-head">Session output</div>
        <ul class="bullet-list" style="margin-top:0.5vw;">
          <li class="check">Company research doc + ICP score</li>
          <li class="check">Two-step email sequence</li>
          <li class="check">Bison upload complete</li>
          <li class="check">Campaign live</li>
        </ul>
      </div>
    </div>
  </div>
""", "Fill [X] minutes after recording. Research to live campaign in [X] minutes. All from a company I'd never seen before. Diff before/ and after/ in the repo — that's the full session output in two minutes."))

slides_html.append(slide("6.3b", "Security Review: Ship Clean", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Run before every campaign launch</div>
    <div class="terminal" style="font-size:0.95vw;">
Pre-ship checklist — runs as a skill before every launch:

  <span style="color:var(--green);">✓</span>  .env is gitignored — no API keys in the repo
  <span style="color:var(--green);">✓</span>  Variables render correctly — {'{'}FIRST_NAME{'}'} not literally {'{'}FIRST_NAME{'}'}
  <span style="color:var(--green);">✓</span>  No links or attachments in cold outreach steps
  <span style="color:var(--green);">✓</span>  Daily send limit set — not uncapped
  <span style="color:var(--green);">✓</span>  Unsubscribe handling configured
  <span style="color:var(--green);">✓</span>  Dry-run reviewed — you've seen exactly what's launching

<span class="comment"># Invoke before every campaign launch:</span>
<span style="color:var(--orange);">/security-review</span>  →  flags any gate that fails, blocks launch until clear
    </div>
  </div>
""", "Run this before any campaign goes live — not as a mental checklist, as a skill that fires and tells you what failed. Six gates. A broken variable that sends 'Hi {FIRST_NAME}' to 500 people is a campaign you can't take back. An uncapped campaign can burn your domain in 48 hours. Run the skill, fix the failures, then launch."))

# ── CH 7 ───────────────────────────────────────────────────────────────────────

slides_html.append(slide("7.1", "The claim", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Chapter 7 — The Business Layer</div>
    <div class="slide-headline xl" style="text-align:center;">This isn't a<br>productivity hack.</div>
    <div class="slide-rule" style="margin:1.5vw auto;"></div>
    <div class="slide-headline" style="text-align:center; color:var(--orange);">It's what happens when<br>10 interfaces collapse into one.</div>
  </div>
""", "Every chapter before this was about building the system. This chapter is about what it's worth commercially. When the interface tax disappears, two things happen: your team moves faster, and you need less of them.", "title"))

slides_html.append(slide("7.2", "Traditional headcount model", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Traditional GTM agency — 10 clients</div>
    <table class="slide-table">
      <thead><tr><th>Role</th><th>Count</th><th>Monthly cost</th></tr></thead>
      <tbody>
        <tr><td>SDR</td><td>6–8</td><td class="dim">$X each</td></tr>
        <tr><td>Manager</td><td>1–2</td><td class="dim">$Y each</td></tr>
        <tr><td>Tools (Clay, N8n, etc.)</td><td>—</td><td class="dim">$Z/month</td></tr>
        <tr><td class="bold" style="border-top:1px solid var(--orange);">Total</td><td></td><td class="bold" style="border-top:1px solid var(--orange);">$$$</td></tr>
      </tbody>
    </table>
  </div>
""", "This is what a traditional 10-client GTM agency looks like on the cost side. That's your cost of delivery. That's what you're comparing against."))

slides_html.append(slide("7.3", "The operator model", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Operator model — 12 clients</div>
    <table class="slide-table">
      <thead><tr><th>Role</th><th>Count</th><th>Monthly cost</th></tr></thead>
      <tbody>
        <tr><td>Operator</td><td>2</td><td class="dim">$X each</td></tr>
        <tr><td>Claude Code</td><td>—</td><td class="green">$20/month</td></tr>
        <tr><td>Bison</td><td>—</td><td class="dim">$Y/month</td></tr>
        <tr><td>Data sources</td><td>—</td><td class="dim">$Z/month</td></tr>
        <tr><td class="bold" style="border-top:1px solid var(--green);">Total</td><td></td><td class="bold green" style="border-top:1px solid var(--green);">$$ (less)</td></tr>
      </tbody>
    </table>
    <div class="slide-sub" style="margin-top:1vw;"><span class="green">Clients served: 12. Output per campaign: higher.</span></div>
  </div>
""", "Two operators running this system can service 12 clients. I'm not estimating — that's what we're doing at LeadGrow right now. The output per campaign is higher because research is deeper and personalization isn't bottlenecked by SDR bandwidth."))

slides_html.append(slide("7.3b", "Speed Arbitrage", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Time compression</div>
    <table class="slide-table">
      <thead><tr><th>Task</th><th>Before</th><th>After</th><th>Compression</th></tr></thead>
      <tbody>
        <tr><td>Company research (one prospect)</td><td style="color:#e07070;">20 min / SDR</td><td class="green">45 sec</td><td class="orange">~27x</td></tr>
        <tr><td>Campaign: research → live</td><td style="color:#e07070;">2 days</td><td class="green">Under 1 hour</td><td class="orange">~16x</td></tr>
        <tr><td>New angle tested + validated</td><td style="color:#e07070;">2–3 weeks</td><td class="green">3 campaigns, 10 days</td><td class="orange">~2x cycles</td></tr>
      </tbody>
    </table>
    <div style="margin-top:2vw; font-size:1.8vw; font-weight:700; color:var(--cream);">This isn't efficiency. It's what becomes possible.</div>
  </div>
""", "Don't lead with cost savings. Lead with time compression — because it's what changes what's possible, not just what's cheaper. When research takes 45 seconds, you do research on companies you would have skipped. You test five angles instead of one. The throughput unlocks work that wasn't economically viable before."))

slides_html.append(slide("7.4", "What clients pay for", """
  <div style="width:100%; text-align:center;">
    <div style="font-size:1.1vw; color:var(--dim); margin-bottom:2vw; font-family:'Fira Code',monospace;">What you use: Claude Code + skills + agents + waterfall</div>
    <div style="width:80%; height:2px; background:var(--rule); margin:0 auto 2vw;"></div>
    <div style="font-size:2.5vw; font-weight:700; color:var(--cream);">What you charge for:</div>
    <div style="font-size:3vw; font-weight:700; color:var(--orange); margin-top:0.5vw;">Meetings booked.<br>Pipeline generated.</div>
  </div>
""", "Clients don't care what's in your stack. You're not selling 'AI-powered outbound' — you're selling a guaranteed number of qualified meetings per month at a margin your competitors can't match.", "center"))

slides_html.append(slide("7.5", "The margin restructure", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Before / After</div>
    <table class="slide-table">
      <thead><tr><th></th><th>Before</th><th>After</th></tr></thead>
      <tbody>
        <tr><td>Revenue per client</td><td class="dim">$X/mo</td><td class="dim">$X/mo</td></tr>
        <tr><td>Cost of delivery</td><td style="color:#e07070;">$Y/mo</td><td class="green">$Y × 0.4/mo</td></tr>
        <tr><td class="bold">Margin</td><td class="bold" style="color:#e07070;">Z%</td><td class="bold green">Z% × 2+</td></tr>
      </tbody>
    </table>
    <div class="slide-sub" style="margin-top:1.5vw;">Cost of delivery drops. Revenue per client stays or goes up. Margin restructures on both sides simultaneously.</div>
  </div>
""", "Use your real numbers if you're comfortable. The point is the multiplier — cost of delivery drops, capacity increases. That's not incremental improvement. That's structural."))

slides_html.append(slide("7.5b", "The Skills Flywheel", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Your IP compounds</div>
    <div class="terminal">
Client engagement
  → skill built or refined
    → library grows
      → next client: faster ramp, higher margin
        → Client engagement

<span style="color:var(--orange); font-weight:700;">Your competitors start from scratch every time.
You start from your last campaign.</span>
    </div>
    <div class="slide-sub" style="margin-top:1.5vw;">At team scale: the skills library is shared IP. When one operator improves a skill, everyone benefits on the next campaign. That's the moat.</div>
  </div>
""", "First client: you build the cold email skill. Tenth client: you run a version validated across nine engagements. Your competitors are starting from scratch every time — fresh prompts, fresh QA. You're starting from your last campaign. That gap compounds. The skills library is the moat — not 'we use Claude Code too.'"))

slides_html.append(slide("7.5c", "Claude as PR Gatekeeper", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Protecting the shared library</div>
    <div class="terminal" style="font-size:0.95vw;">
Operator writes new skill or updates existing one
  <span style="color:var(--dim);">↓</span>
Pull request opened
  <span style="color:var(--dim);">↓</span>
Claude reviews against standards:
  - Does it follow the SKILL.md template?
  - Is Insider Knowledge specific or generic?
  - Are Quality Gates defined and testable?
  - Has it been validated on real data?
  <span style="color:var(--dim);">↓</span>
  <span style="color:var(--green);">✓ Approved → merges to shared library</span>
  <span style="color:#e07070;">✗ Changes requested → operator revises</span>
    </div>
  </div>
""", "Every skill or agent change goes through a pull request. Claude reviews it before it merges. Not a human — Claude. It checks against the skill template, flags vague insider knowledge, verifies quality gates are testable, confirms the skill was validated on real data. One bad skill that produces garbage output poisons every operator on the team until someone notices. Claude as PR gatekeeper catches that before it merges."))

slides_html.append(slide("7.6", "The internal business case", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">For leadership / founders</div>
    <div class="quote-block" style="text-align:left; max-width:85%; margin:2vw auto;">
      <div class="quote-text">"Two operators with this system match the output of a 6-person SDR team at 40% of the cost."</div>
      <div class="quote-meta" style="margin-top:1.2vw; color:var(--orange);">Payback period: 90 days.</div>
    </div>
  </div>
""", "This is the framing for anyone pitching this internally. You're not pitching a tool. You're pitching a headcount restructure with a 90-day payback. Leadership doesn't need to know what Claude Code is.", "center"))

slides_html.append(slide("7.7", "The client-facing case", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">For AEs pitching clients</div>
    <div class="quote-block" style="text-align:left; max-width:85%; margin:2vw auto;">
      <div class="quote-text">"We're booking 20–30% more meetings per client than two years ago. Ramp time on new campaigns: two weeks, not six. Team size has gone down while output has gone up."</div>
      <div class="quote-meta">Powered by Claude Code infrastructure — they don't need to know what that means.</div>
    </div>
  </div>
""", "Clients need proof on two axes: output (more meetings) and speed (faster ramp). The 20-30% meetings stat is real — that's the LeadGrow number year-over-year. Lead with whichever matches what they're asking.", "center"))

slides_html.append(slide("7.8", "CTA: Three things to do next", """
  <div style="width:100%;">
    <div style="font-family:'Fira Code',monospace; font-size:1.3vw; color:var(--orange); margin-bottom:2vw; text-align:center;">github.com/LeadGrowGTM/claude-code-gtm</div>
    <ol class="num-list">
      <li><span class="n">1</span><span><span style="font-family:'Fira Code',monospace;">git clone github.com/LeadGrowGTM/claude-code-gtm</span></span></li>
      <li><span class="n">2</span><span>Start with <span style="font-family:'Fira Code',monospace; color:var(--orange);">chapter-2-foundation/CLAUDE.md.template</span> — fill in the five sections</span></li>
      <li><span class="n">3</span><span>Add your insider knowledge to the skill stubs — that's where your moat is</span></li>
    </ol>
  </div>
""", "That's the full stack. The insider knowledge is the only part only you can write. Everything else is infrastructure. Clone the repo, fill in your CLAUDE.md, write your insider knowledge into the skill stubs."))

# ── BONUS ─────────────────────────────────────────────────────────────────────

slides_html.append(slide("B.1", "Encoding sales training into a skill", """
  <div style="width:100%;">
    <div class="slide-eyebrow">Bonus — Sales Call Prep</div>
    <div class="compare">
      <div class="compare-col">
        <div class="compare-head">Training input</div>
        <div class="compare-item">Hormozi framework</div>
        <div class="compare-item">Your Fireflies call recordings</div>
        <div class="compare-item">SPIN Selling notes</div>
      </div>
      <div style="display:flex; align-items:center; font-size:2vw; color:var(--orange); padding:0 1vw;">→</div>
      <div class="compare-col">
        <div class="compare-head" style="color:var(--green); border-color:var(--green);">Pre-call brief</div>
        <div class="compare-item">Objections anticipated</div>
        <div class="compare-item">Discovery questions</div>
        <div class="compare-item">Opening move + close target</div>
      </div>
    </div>
    <div class="slide-sub" style="margin-top:1.5vw;">15 minutes to build the skill. 30 seconds to run before every call.</div>
  </div>
""", "The sales-call-prep skill takes a training source and a prospect brief and returns a pre-call sheet. Takes 15 minutes to build. Runs in 30 seconds before every call."))

slides_html.append(slide("B.2", "Live: Pre-call brief in 30 seconds", """
  <div style="width:100%; text-align:center;">
    <div class="slide-eyebrow" style="text-align:center;">Live run — bonus</div>
    <div class="terminal" style="text-align:left; display:inline-block; margin-top:2vw; padding:2vw 3vw;">
      <span style="color:var(--orange); font-size:1.5vw; font-weight:700;">[LIVE SEGMENT]</span>
      <div style="margin-top:1vw; color:var(--dim); font-size:1.1vw;">Paste in training content (Hormozi / Fireflies / SPIN Selling).</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Invoke sales-call-prep skill against a prospect.</div>
      <div style="margin-top:0.5vw; color:var(--dim); font-size:1.1vw;">Output: objections listed, discovery questions queued, opening move.</div>
      <div style="margin-top:0.5vw; color:var(--orange); font-size:1.1vw;">The output should be tight enough to read in 30 seconds before a call.</div>
    </div>
  </div>
""", "[LIVE SEGMENT — paste in training content, show the skill running, show the output. Keep this tight — 8-10 minutes. The point: skills aren't just for campaigns. Any repeatable expert task gets a skill file. The viewer should leave thinking about which expert task in their process gets encoded next.]", "center"))

# ── ASSEMBLE ──────────────────────────────────────────────────────────────────

all_slides = "\n".join(slides_html)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Claude Code for GTM Operators — Slides</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Lora:ital,wght@0,400;1,400&family=Fira+Code:wght@400&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{all_slides}
</body>
</html>
"""

OUT_HTML.write_text(html, encoding="utf-8")
print(f"Written: {OUT_HTML}")
print(f"Slides: {len(slides_html)}")
print(f"Size: {OUT_HTML.stat().st_size // 1024} KB")
