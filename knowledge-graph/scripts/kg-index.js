/**
 * Knowledge Graph Indexer
 * Scans workspace markdown files and generates entity/relationship JSONL + index.json
 *
 * Usage:
 *   bun knowledge-graph/scripts/kg-index.js           # full rebuild
 *   bun knowledge-graph/scripts/kg-index.js --dry-run  # preview, don't write
 *   bun knowledge-graph/scripts/kg-index.js --stats    # counts only
 *
 * Zero dependencies — runs with Bun or Node.js.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { parseFrontmatter } = require('./lib/parse-frontmatter');

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const ROOT = path.resolve(__dirname, '..', '..');
const KG_DIR = path.resolve(__dirname, '..');
const TODAY = new Date().toISOString().slice(0, 10);

const STOP_WORDS = new Set([
  'the',
  'a',
  'an',
  'and',
  'or',
  'for',
  'with',
  'this',
  'that',
  'in',
  'on',
  'to',
  'of',
  'is',
  'are',
  'be',
  // Extended stop words for tag quality
  'when',
  'what',
  'how',
  'why',
  'where',
  'which',
  'who',
  'whom',
  'your',
  'our',
  'their',
  'its',
  'from',
  'into',
  'about',
  'after',
  'before',
  'between',
  'through',
  'during',
  'above',
  'below',
  'will',
  'would',
  'should',
  'could',
  'does',
  'have',
  'has',
  'had',
  'been',
  'being',
  'was',
  'were',
  'not',
  'but',
  'also',
  'just',
  'than',
  'then',
  'each',
  'every',
  'both',
  'more',
  'most',
  'much',
  'some',
  'such',
  'only',
  'very',
  'same',
  'here',
  'there',
  'part',
  'honest',
  'true',
  'false',
  'good',
  'well',
  'still',
  'over',
  // Domain-generic words that dilute tag quality
  'research',
  'client',
  'context',
  'master',
  'quick',
  'using',
  'create',
  'generate',
  'write',
  'dont',
  'overview',
  'folders',
  'local',
  'common',
  'based',
  'includes',
  'provides',
  'supports',
  'start',
  'guide',
  'steps',
  'rules',
  'section',
  'example',
  'format',
  'output',
  'input',
  'process',
  'system',
  'first',
  'current',
  'default',
  'specific',
  'available',
  'relevant',
  'existing',
]);

// Numeric/date patterns caught separately in tag extraction
const NOISE_PATTERN =
  /^\d+$|^\d{4}$|^v\d|^jan|^feb|^mar|^apr|^may|^jun|^jul|^aug|^sep|^oct|^nov|^dec/i;

const SYNONYM_MAP = {
  'e-mail': 'email',
  li: 'linkedin',
  'lead-gen': 'lead-generation',
  'lead-generation': 'lead-generation',
  leadgen: 'lead-generation',
  outbound: 'cold-email',
  'cold-email': 'cold-email',
  coldemail: 'cold-email',
  enrichment: 'enrich',
  enriching: 'enrich',
  'a-b': 'split-test',
  'ab-test': 'split-test',
  'split-test': 'split-test',
  linkedin: 'linkedin',
  'linked-in': 'linkedin',
  emailbison: 'bison',
  'email-bison': 'bison',
};

const DOMAIN_KEYWORDS = {
  outbound: [
    'cold-email',
    'campaign',
    'sequence',
    'deliverability',
    'list-building',
    'targeting',
    'personalization',
    'outbound',
    'email',
    'leads',
  ],
  content: [
    'linkedin',
    'newsletter',
    'youtube',
    'blog',
    'seo',
    'content-strategy',
    'hooks',
    'content',
    'writing',
    'post',
  ],
  methodology: [
    'icp',
    'voice',
    'messaging',
    'positioning',
    'offerings',
    'framework',
    'methodology',
    'thinking',
  ],
  competitive: [
    'apollo',
    'instantly',
    'smartlead',
    'objection',
    'differentiator',
    'competitor',
    'battlecard',
  ],
  operations: [
    'rule',
    'automation',
    'workflow',
    'sop',
    'file-storage',
    'archive',
    'operations',
    'git',
    'safety',
  ],
  clients: ['client', 'campaign', 'sequence', 'qualification', 'master', 'onboarding'],
  website: ['website', 'blog', 'landing-page', 'seo', 'page'],
};

const VOLATILE_SKILL_TAGS = new Set([
  'copy',
  'targeting',
  'enrichment',
  'list-building',
  'personalization',
]);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Normalise path to workspace-relative with forward slashes */
function relPath(absPath) {
  return path.relative(ROOT, absPath).replace(/\\/g, '/');
}

/** Read file safely, normalise CRLF to LF, return null on error */
function readSafe(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n');
  } catch {
    return null;
  }
}

/** Recursive directory walk returning absolute paths matching a test fn */
function walkDir(dir, testFn, results) {
  results = results || [];
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return results;
  }
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      walkDir(full, testFn, results);
    } else if (testFn(e.name, full)) {
      results.push(full);
    }
  }
  return results;
}

/** Find nearest git root by walking up from a directory */
function findGitRoot(dir) {
  let current = path.resolve(dir);
  while (current !== path.dirname(current)) {
    if (fs.existsSync(path.join(current, '.git'))) return current;
    current = path.dirname(current);
  }
  return null;
}

/** Get last git commit date for a file, or TODAY */
function gitDate(filePath) {
  try {
    const gitRoot = findGitRoot(path.dirname(filePath));
    if (!gitRoot) return TODAY;
    const relToGit = path.relative(gitRoot, filePath).replace(/\\/g, '/');
    const out = execSync(`git log --format=%aI -1 -- "${relToGit}"`, {
      cwd: gitRoot,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
    }).trim();
    return out ? out.slice(0, 10) : TODAY;
  } catch {
    return TODAY;
  }
}

/** Kebab-case a string */
function kebab(str) {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9-\s]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

/** Normalise a single tag token */
function normTag(t) {
  let tag = kebab(t.trim());
  if (SYNONYM_MAP[tag]) tag = SYNONYM_MAP[tag];
  // Filter numeric/date noise
  if (NOISE_PATTERN.test(tag)) return '';
  return tag;
}

/** Extract H1 from markdown */
function extractH1(content) {
  const m = content.match(/^#\s+(.+)/m);
  return m ? m[1].trim() : null;
}

/** Extract H2/H3 headings from markdown as keyword tags */
function extractHeadingTags(content) {
  const tags = [];
  const re = /^#{2,3}\s+(.+)/gm;
  let m;
  while ((m = re.exec(content)) !== null) {
    const heading = m[1].trim();
    // First check for existing hyphenated-phrases (keep as-is)
    const hyphPhrases = heading.match(/[a-zA-Z]+-[a-zA-Z]+(?:-[a-zA-Z]+)*/g);
    if (hyphPhrases) {
      for (const hp of hyphPhrases) {
        const n = normTag(hp);
        if (n && n.length > 2 && !STOP_WORDS.has(n)) tags.push(n);
      }
    }
    // Then extract individual meaningful words (4+ chars, not stop words)
    const words = heading.replace(/[^a-zA-Z0-9\s-]/g, '').split(/\s+/);
    for (const w of words) {
      const n = normTag(w);
      if (n && n.length >= 4 && !STOP_WORDS.has(n)) tags.push(n);
    }
  }
  return tags;
}

/** Filter and clamp tags: min 2, max 7, remove stop words */
function clampTags(tags, fallbackTokens) {
  let unique = [...new Set(tags.filter((t) => t && t.length > 1 && !STOP_WORDS.has(t)))];
  // pad if under 2
  if (unique.length < 2 && fallbackTokens) {
    for (const t of fallbackTokens) {
      const n = normTag(t);
      if (n && n.length > 1 && !STOP_WORDS.has(n) && !unique.includes(n)) unique.push(n);
      if (unique.length >= 2) break;
    }
  }
  // trim if over 7 — keep first 7 (most specific come first from extraction order)
  if (unique.length > 7) unique = unique.slice(0, 7);
  return unique;
}

/** Assign domain from tags, fallback to folder path */
function assignDomain(tags, sourcePath) {
  const scores = {};
  for (const [domain, keywords] of Object.entries(DOMAIN_KEYWORDS)) {
    scores[domain] = tags.filter((t) => keywords.includes(t)).length;
  }
  const best = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
  if (best && best[1] > 0) return best[0];

  // Fallback: derive from folder path
  const p = sourcePath.toLowerCase();
  if (p.includes('campaigns/') || p.includes('campaigns/patterns/')) return 'outbound';
  if (p.includes('content/') || p.includes('content-library/')) return 'content';
  if (p.includes('company/methodology/') || p.includes('company/')) return 'methodology';
  if (p.includes('battlecard') || p.includes('archive/battlecards/')) return 'competitive';
  if (p.includes('tools/') || p.includes('automation/')) return 'operations';
  if (p.includes('clients/')) return 'clients';
  if (p.includes('website/') && !p.includes('company/website/')) return 'website';
  return 'operations';
}

/** Assign decay class based on type and tags */
function assignDecay(type, tags) {
  if (type === 'pattern' || type === 'learning') return 'volatile';
  if (['reference', 'rule', 'case_study', 'battlecard'].includes(type)) return 'durable';
  if (type === 'skill') {
    for (const t of tags) {
      if (VOLATILE_SKILL_TAGS.has(t)) return 'volatile';
    }
    return 'durable';
  }
  return 'durable';
}

/** Parse simple YAML (key: value, key: [list], key:\n  - items) — enough for taxonomy */
function parseSimpleYaml(content) {
  const result = {};
  const lines = content.split('\n');
  let currentKey = null;
  for (const line of lines) {
    if (line.trim() === '' || line.trim().startsWith('#')) continue;
    const kvMatch = line.match(/^(\w[\w_]*):\s*(.+)/);
    const blockMatch = line.match(/^(\w[\w_]*):\s*$/);
    const listMatch = line.match(/^\s+-\s+(.+)/);
    if (kvMatch && !kvMatch[2].startsWith('"')) {
      result[kvMatch[1]] = kvMatch[2].trim();
      currentKey = null;
    } else if (blockMatch) {
      currentKey = blockMatch[1];
      result[currentKey] = [];
    } else if (listMatch && currentKey && Array.isArray(result[currentKey])) {
      result[currentKey].push(listMatch[1].replace(/#.*$/, '').trim());
    }
  }
  return result;
}

/** Extract metric values from a markdown table under ## Summary */
function extractSummaryMeta(content) {
  const meta = {};
  const summaryMatch = content.match(
    /## Summary[\s\S]*?\n\|[\s\S]*?\n\|[-|\s]+\n([\s\S]*?)(?=\n---|\n##|$)/,
  );
  if (!summaryMatch) return meta;
  const rows = summaryMatch[1].trim().split('\n');
  for (const row of rows) {
    const cells = row
      .split('|')
      .map((c) => c.trim())
      .filter(Boolean);
    if (cells.length >= 2) {
      const key = cells[0].replace(/\*\*/g, '').trim().toLowerCase();
      const val = cells[1].replace(/\*\*/g, '').trim();
      if (key.includes('revenue')) meta.revenue = val;
      if (key.includes('timeframe')) meta.timeframe = val;
    }
  }
  return meta;
}

/** Extract tags from skill description */
function tagsFromDescription(desc) {
  if (!desc) return [];
  const tags = [];
  // Split on commas, "and", semicolons
  const parts = desc.split(/[,;]+|(?:\band\b)/i);
  for (const part of parts) {
    // Extract hyphenated phrases
    const hyphMatch = part.match(/[a-z]+-[a-z]+(?:-[a-z]+)*/gi);
    if (hyphMatch) tags.push(...hyphMatch.map(normTag));
    // Extract quoted terms
    const quotMatch = part.match(/"([^"]+)"/g);
    if (quotMatch) tags.push(...quotMatch.map((q) => normTag(q.replace(/"/g, ''))));
    // Single meaningful words (5+ chars)
    const words = part.trim().split(/\s+/);
    for (const w of words) {
      const n = normTag(w);
      if (n.length >= 5 && !STOP_WORDS.has(n)) tags.push(n);
    }
  }
  return tags;
}

/** Extract additional tags from "Use when" and "Triggers:" sections in skill body */
function tagsFromSkillBody(body) {
  const tags = [];
  const triggerMatch = body.match(/(?:Use when|Triggers?:)([\s\S]*?)(?:\n##|\n---|\n\n\n|$)/i);
  if (triggerMatch) {
    const lines = triggerMatch[1].split('\n');
    for (const line of lines) {
      const cleaned = line.replace(/^[\s*-]+/, '').trim();
      if (cleaned.length > 3 && cleaned.length < 80) {
        const words = cleaned.split(/\s+/);
        for (const w of words) {
          const n = normTag(w);
          if (n.length >= 4 && !STOP_WORDS.has(n)) tags.push(n);
        }
      }
    }
  }
  return tags;
}

// ---------------------------------------------------------------------------
// Scanners — each returns an array of entity objects
// ---------------------------------------------------------------------------

function scanSkills() {
  const entities = [];
  // Scan skills from lg-* plugins, leadgrow-hq, and workspace root.
  // Order matters: first occurrence wins dedup, so plugin repos take priority
  // over leadgrow-hq copies (plugins are the canonical home now).
  const lgSkillsDir = path.join(ROOT, 'leadgrow-hq', '.claude', 'skills');
  const rootSkillsDir = path.join(ROOT, '.claude', 'skills');
  const scanDirs = [];

  // lg-* plugin repo skills (canonical source — scanned first to win dedup)
  const pluginRepos = ['lg-outbound', 'lg-content', 'lg-research', 'lg-data', 'lg-website'];
  for (const repo of pluginRepos) {
    const pluginSkillsDir = path.join(ROOT, repo, 'skills');
    if (fs.existsSync(pluginSkillsDir)) scanDirs.push(pluginSkillsDir);
  }

  // leadgrow-hq skills (legacy — skills not yet migrated to plugins still live here)
  if (fs.existsSync(lgSkillsDir)) scanDirs.push(lgSkillsDir);
  const lgUniversalDir = path.join(lgSkillsDir, 'universal');
  if (fs.existsSync(lgUniversalDir)) scanDirs.push(lgUniversalDir);

  // Root workspace skills
  if (fs.existsSync(rootSkillsDir)) scanDirs.push(rootSkillsDir);

  for (const dir of scanDirs) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name === 'universal') continue; // skip universal dir itself, handled separately
      const skillFile = path.join(dir, entry.name, 'SKILL.md');
      if (!fs.existsSync(skillFile)) continue;

      const rel = relPath(skillFile);
      const content = readSafe(skillFile);
      if (!content) continue;

      const { frontmatter, body } = parseFrontmatter(content);
      const parentDir = entry.name;
      const id = `skill:${parentDir}`;
      const name = frontmatter.name || parentDir;
      const descTags = tagsFromDescription(frontmatter.description);
      const bodyTags = tagsFromSkillBody(body);
      const fileTokens = parentDir.split('-');
      const tags = clampTags([...descTags, ...bodyTags], fileTokens);
      const domain = frontmatter.domain || assignDomain(tags, rel);
      const decay = assignDecay('skill', tags);

      // Extract description and triggers for richer search + skill graph
      const description = frontmatter.description
        ? typeof frontmatter.description === 'string'
          ? frontmatter.description.replace(/^\s*\|\s*/, '').trim()
          : ''
        : '';
      const triggers = Array.isArray(frontmatter.triggers)
        ? frontmatter.triggers.map((t) => String(t).trim()).filter(Boolean)
        : [];
      const tool = frontmatter.tool || null;

      entities.push({
        id,
        type: 'skill',
        name,
        description,
        source: rel,
        domain,
        tags,
        triggers,
        status: 'canonical',
        decay_class: decay,
        created: TODAY,
        last_validated: gitDate(skillFile),
        confidence: 1.0,
        meta: tool ? { tool } : {},
      });
    }
  }
  return entities;
}

function scanCaseStudies() {
  const entities = [];
  const dir = path.join(ROOT, 'leadgrow-hq', 'company', 'social-proof');
  let files;
  try {
    files = fs.readdirSync(dir);
  } catch {
    return entities;
  }

  for (const f of files) {
    if (!f.endsWith('.md')) continue;
    if (f === '_index.md' || f.startsWith('aggregate-')) continue;
    const filePath = path.join(dir, f);
    const content = readSafe(filePath);
    if (!content) continue;

    const slug = f.replace(/\.md$/, '');
    const id = `case-study:${slug}`;
    const name = extractH1(content) || slug;
    const headingTags = extractHeadingTags(content);
    const meta = extractSummaryMeta(content);

    // Extract meaningful tags: slug tokens first (most descriptive), then headings
    const slugTokens = slug.split('-').filter((t) => !/^\d+$/.test(t)); // exclude pure numbers
    // Also extract keywords from Summary table values and campaign body
    const bodyKeywords = [];
    const summaryMatch = content.match(/## Summary[\s\S]*?(?=\n##|$)/);
    if (summaryMatch) {
      const valueWords = summaryMatch[0].match(/\|\s*\*?\*?([^|*]+)\*?\*?\s*\|/g);
      if (valueWords) {
        for (const v of valueWords) {
          const cleaned = v.replace(/[|*]/g, '').trim();
          for (const w of cleaned.split(/\s+/)) {
            const n = normTag(w);
            if (n.length >= 4 && !STOP_WORDS.has(n) && !/^\d+$/.test(n) && !/^[\d,.%$]+$/.test(w)) {
              bodyKeywords.push(n);
            }
          }
        }
      }
    }
    // Prioritize slug tokens (industry, scale), body keywords, then headings
    const tags = clampTags(
      [...slugTokens.map(normTag), ...bodyKeywords, ...headingTags],
      slugTokens,
    );
    const domain = assignDomain(tags, relPath(filePath));

    entities.push({
      id,
      type: 'case_study',
      name,
      source: relPath(filePath),
      domain,
      tags,
      status: 'canonical',
      decay_class: 'durable',
      created: TODAY,
      last_validated: gitDate(filePath),
      confidence: 1.0,
      meta,
    });
  }
  return entities;
}

function scanReferences() {
  const entities = [];
  const sources = [];

  // company/*.md — exclude mitch-personal-interests.md, skip directories
  const companyDir = path.join(ROOT, 'leadgrow-hq', 'company');
  try {
    const entries = fs.readdirSync(companyDir, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isFile() || !e.name.endsWith('.md')) continue;
      if (e.name === 'mitch-personal-interests.md') continue;
      sources.push(path.join(companyDir, e.name));
    }
  } catch {
    /* skip */
  }

  // company/operations/*.md — exclude campaigns/ and list-building/ subdirs
  const opsDir = path.join(ROOT, 'leadgrow-hq', 'company', 'operations');
  try {
    const entries = fs.readdirSync(opsDir, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isFile() || !e.name.endsWith('.md')) continue;
      sources.push(path.join(opsDir, e.name));
    }
  } catch {
    /* skip */
  }

  // company/content-library/*.md — exclude examples/ subdir (was projects/content/libraries/)
  const libDir = path.join(ROOT, 'leadgrow-hq', 'company', 'content-library');
  try {
    const entries = fs.readdirSync(libDir, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isFile() || !e.name.endsWith('.md')) continue;
      sources.push(path.join(libDir, e.name));
    }
  } catch {
    /* skip */
  }

  // company/methodology/*.md — methodology reference entities
  const methDir = path.join(ROOT, 'leadgrow-hq', 'company', 'methodology');
  try {
    const entries = fs.readdirSync(methDir, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isFile() || !e.name.endsWith('.md')) continue;
      sources.push(path.join(methDir, e.name));
    }
  } catch {
    /* skip */
  }

  // company/hiring/**/*.md — hiring reference entities (recursive)
  const hiringDir = path.join(ROOT, 'leadgrow-hq', 'company', 'hiring');
  const hiringFiles = walkDir(hiringDir, (name) => name.endsWith('.md'));
  for (const f of hiringFiles) sources.push(f);

  // company/customer-success/**/*.md — CS methodology reference entities (recursive)
  const csDir = path.join(ROOT, 'leadgrow-hq', 'company', 'customer-success');
  const csFiles = walkDir(csDir, (name) => name.endsWith('.md'));
  for (const f of csFiles) sources.push(f);

  // company/social-proof/aggregate-2025-stats.md
  const aggFile = path.join(
    ROOT,
    'leadgrow-hq',
    'company',
    'social-proof',
    'aggregate-2025-stats.md',
  );
  if (fs.existsSync(aggFile)) sources.push(aggFile);

  for (const filePath of sources) {
    const content = readSafe(filePath);
    if (!content) continue;
    const slug = path.basename(filePath, '.md');
    const id = `reference:${slug}`;
    const name = extractH1(content) || slug;
    const headingTags = extractHeadingTags(content);
    const fileTokens = slug.split('-');
    const tags = clampTags(headingTags, fileTokens);
    const domain = assignDomain(tags, relPath(filePath));

    entities.push({
      id,
      type: 'reference',
      name,
      source: relPath(filePath),
      domain,
      tags,
      status: 'canonical',
      decay_class: 'durable',
      created: TODAY,
      last_validated: gitDate(filePath),
      confidence: 1.0,
      meta: {},
    });
  }
  return entities;
}

function scanBattlecards() {
  const entities = [];
  const dir = path.join(ROOT, 'leadgrow-hq', 'archive', 'battlecards');
  let files;
  try {
    files = fs.readdirSync(dir);
  } catch {
    return entities;
  }

  for (const f of files) {
    if (!f.endsWith('.md') || f === 'README.md') continue;
    const filePath = path.join(dir, f);
    const content = readSafe(filePath);
    if (!content) continue;

    const slug = f.replace(/\.md$/, '');
    const id = `battlecard:${slug}`;
    const name = extractH1(content) || slug;
    const headingTags = extractHeadingTags(content);
    const competitorTag = normTag(slug);
    const tags = clampTags([competitorTag, 'battlecard', ...headingTags], slug.split('-'));
    const domain = 'competitive';

    entities.push({
      id,
      type: 'battlecard',
      name,
      source: relPath(filePath),
      domain,
      tags,
      status: 'canonical',
      decay_class: 'durable',
      created: TODAY,
      last_validated: gitDate(filePath),
      confidence: 1.0,
      meta: {},
    });
  }
  return entities;
}

function scanRules() {
  const entities = [];
  const seenIds = new Set();
  // Scan both workspace root and leadgrow-hq rules (root takes priority)
  const rootRulesDir = path.join(ROOT, '.claude', 'rules');
  const lgRulesDir = path.join(ROOT, 'leadgrow-hq', '.claude', 'rules');

  for (const dir of [rootRulesDir, lgRulesDir]) {
    let files;
    try {
      files = fs.readdirSync(dir);
    } catch {
      continue;
    }

    for (const f of files) {
      if (!f.endsWith('.md')) continue;
      const filePath = path.join(dir, f);
      const content = readSafe(filePath);
      if (!content) continue;

      const slug = f.replace(/\.md$/, '');
      const id = `rule:${slug}`;
      if (seenIds.has(id)) continue; // root rules take priority
      seenIds.add(id);
      const name = extractH1(content) || slug;
      const headingTags = extractHeadingTags(content);
      const fileTokens = slug.split('-');
      const tags = clampTags([...headingTags, ...fileTokens.map(normTag)], fileTokens);

      entities.push({
        id,
        type: 'rule',
        name,
        source: relPath(filePath),
        domain: 'operations',
        tags,
        status: 'canonical',
        decay_class: 'durable',
        created: TODAY,
        last_validated: gitDate(filePath),
        confidence: 1.0,
        meta: {},
      });
    }
  }
  return entities;
}

function scanLearnings() {
  const entities = [];
  // Scan both leadgrow-hq and workspace root memory directories
  const lgMemoryDir = path.join(ROOT, 'leadgrow-hq', '.claude', 'memory');
  const rootMemoryDir = path.join(ROOT, '.claude', 'memory');

  for (const memoryDir of [lgMemoryDir, rootMemoryDir]) {
    let files;
    try {
      files = fs.readdirSync(memoryDir);
    } catch {
      continue;
    }

    for (const f of files) {
      if (!f.startsWith('learnings-') || !f.endsWith('.md')) continue;
      const filePath = path.join(memoryDir, f);
      const content = readSafe(filePath);
      if (!content) continue;

      // Extract project name from filename: learnings-gtm.md → gtm
      const projName = f.replace(/^learnings-/, '').replace(/\.md$/, '');

      // Parse ### YYYY-MM-DD - Title blocks under ## Unpromoted
      const unpromotedMatch = content.match(/## .*Unpromoted([\s\S]*?)(?=\n## |$)/i);
      if (!unpromotedMatch) continue;
      const section = unpromotedMatch[1];
      const blockRe = /### (\d{4}-\d{2}-\d{2})\s*-\s*(.+)/g;
      let m;
      while ((m = blockRe.exec(section)) !== null) {
        const date = m[1];
        const title = m[2].trim();
        const slug = kebab(title);
        if (!slug) continue;
        const id = `learning:${date}-${slug}`;
        const tags = clampTags(slug.split('-').map(normTag), [projName]);
        const domain = assignDomain(tags, relPath(filePath));

        entities.push({
          id,
          type: 'learning',
          name: title,
          source: relPath(filePath),
          domain,
          tags,
          status: 'emergent',
          decay_class: 'volatile',
          created: date,
          last_validated: date,
          confidence: 1.0,
          meta: {},
        });
      }
    }
  }
  return entities;
}

function scanPatterns() {
  const entities = [];
  const dir = path.join(ROOT, 'leadgrow-hq', 'campaigns', 'patterns');
  let files;
  try {
    files = fs.readdirSync(dir);
  } catch {
    return entities;
  }

  for (const f of files) {
    if (!f.endsWith('.md') || f === 'README.md') continue;
    const filePath = path.join(dir, f);
    const content = readSafe(filePath);
    if (!content) continue;

    const slug = f.replace(/\.md$/, '');
    const id = `pattern:${slug}`;
    const name = extractH1(content) || slug;
    const headingTags = extractHeadingTags(content);
    const fileTokens = slug.split('-');
    const tags = clampTags([...fileTokens.map(normTag), ...headingTags], fileTokens);
    const domain = assignDomain(tags, relPath(filePath));

    entities.push({
      id,
      type: 'pattern',
      name,
      source: relPath(filePath),
      domain,
      tags,
      status: 'emergent',
      decay_class: 'volatile',
      created: TODAY,
      last_validated: gitDate(filePath),
      confidence: 1.0,
      meta: {},
    });
  }
  return entities;
}

function scanClients() {
  const entities = [];
  const clientsDir = path.join(ROOT, 'clients');
  let clientDirs;
  try {
    clientDirs = fs.readdirSync(clientsDir, { withFileTypes: true });
  } catch {
    return entities;
  }

  for (const entry of clientDirs) {
    if (!entry.isDirectory() || !entry.name.startsWith('gtm-client-')) continue;
    const clientDir = path.join(clientsDir, entry.name);
    const clientSlug = entry.name.replace('gtm-client-', '');

    // Index _master.md as reference
    const masterFile = path.join(clientDir, '_master.md');
    if (fs.existsSync(masterFile)) {
      const content = readSafe(masterFile);
      if (content) {
        const name = extractH1(content) || `${clientSlug} — Client Overview`;
        const headingTags = extractHeadingTags(content);
        const tags = clampTags([clientSlug, 'client', 'master', ...headingTags], [clientSlug]);
        entities.push({
          id: `client:${clientSlug}`,
          type: 'reference',
          name,
          source: relPath(masterFile),
          domain: 'clients',
          tags,
          status: 'canonical',
          decay_class: 'durable',
          created: TODAY,
          last_validated: gitDate(masterFile),
          confidence: 1.0,
          meta: {},
        });
      }
    }

    // Index sequences/*.md as patterns
    const seqDir = path.join(clientDir, 'sequences');
    try {
      const seqFiles = fs.readdirSync(seqDir);
      for (const f of seqFiles) {
        if (!f.endsWith('.md') || f === 'README.md') continue;
        const filePath = path.join(seqDir, f);
        const content = readSafe(filePath);
        if (!content) continue;
        const slug = f.replace(/\.md$/, '');
        const name = extractH1(content) || slug;
        const tags = clampTags(
          [clientSlug, 'sequence', 'campaign', ...slug.split('-').map(normTag)],
          [clientSlug],
        );
        entities.push({
          id: `client-seq:${clientSlug}-${slug}`,
          type: 'pattern',
          name,
          source: relPath(filePath),
          domain: 'clients',
          tags,
          status: 'canonical',
          decay_class: 'volatile',
          created: TODAY,
          last_validated: gitDate(filePath),
          confidence: 1.0,
          meta: {},
        });
      }
    } catch {
      /* no sequences dir */
    }

    // Index research/*.md as references
    const resDir = path.join(clientDir, 'research');
    try {
      const resFiles = fs.readdirSync(resDir);
      for (const f of resFiles) {
        if (!f.endsWith('.md') || f === 'README.md') continue;
        const filePath = path.join(resDir, f);
        const content = readSafe(filePath);
        if (!content) continue;
        const slug = f.replace(/\.md$/, '');
        const name = extractH1(content) || slug;
        const tags = clampTags(
          [clientSlug, 'research', ...slug.split('-').map(normTag)],
          [clientSlug],
        );
        entities.push({
          id: `client-research:${clientSlug}-${slug}`,
          type: 'reference',
          name,
          source: relPath(filePath),
          domain: 'clients',
          tags,
          status: 'canonical',
          decay_class: 'durable',
          created: TODAY,
          last_validated: gitDate(filePath),
          confidence: 1.0,
          meta: {},
        });
      }
    } catch {
      /* no research dir */
    }
  }
  return entities;
}

// ---------------------------------------------------------------------------
// Visibility Assignment
// ---------------------------------------------------------------------------

const VISIBILITY_RULES = [
  { pattern: /^leadgrow-hq\/archive\/battlecards\//, visibility: 'leadership' },
  { pattern: /^leadgrow-hq\/automation\//, visibility: 'leadership' },
  { pattern: /^leadgrow-hq\/campaigns\/patterns\//, visibility: 'leadership' },
  { pattern: /^leadgrow-hq\/company\/social-proof\//, visibility: 'public' },
  { pattern: /^leadgrow-hq\/company\//, visibility: 'team' },
  { pattern: /^leadgrow-hq\/\.claude\/skills\//, visibility: 'team' },
  { pattern: /^leadgrow-hq\/\.claude\/rules\//, visibility: 'team' },
  { pattern: /^leadgrow-hq\/\.claude\/memory\//, visibility: 'team' },
  { pattern: /^leadgrow-hq\/content\//, visibility: 'team' },
  { pattern: /^leadgrow-hq\/tools\//, visibility: 'team' },
  { pattern: /^leadgrow-hq\/website\//, visibility: 'team' },
  { pattern: /^clients\//, visibility: 'leadership' },
  { pattern: /^website\//, visibility: 'public' },
  { pattern: /^\.claude\/skills\//, visibility: 'team' },
  { pattern: /^\.claude\/rules\//, visibility: 'team' },
  { pattern: /^\.claude\/memory\//, visibility: 'team' },
  { pattern: /^lg-outbound\/skills\//, visibility: 'team' },
  { pattern: /^lg-content\/skills\//, visibility: 'team' },
  { pattern: /^lg-research\/skills\//, visibility: 'team' },
  { pattern: /^lg-data\/skills\//, visibility: 'team' },
  { pattern: /^lg-website\/skills\//, visibility: 'team' },
];

function assignVisibility(sourcePath) {
  for (const rule of VISIBILITY_RULES) {
    if (rule.pattern.test(sourcePath)) return rule.visibility;
  }
  // Default: leadership (most restrictive)
  return 'leadership';
}

// ---------------------------------------------------------------------------
// Relationship Detection
// ---------------------------------------------------------------------------

function detectRelationships(entities) {
  const rels = [];
  const entityMap = new Map();
  const contentCache = new Map();

  for (const e of entities) entityMap.set(e.id, e);

  function getContent(entity) {
    if (contentCache.has(entity.id)) return contentCache.get(entity.id);
    const content = readSafe(path.join(ROOT, entity.source)) || '';
    contentCache.set(entity.id, content);
    return content;
  }

  // Strategy 1: File path references
  // Match full source path or last 2 path segments (e.g. "skills/cold-email-v2").
  // Bare filenames like "SKILL.md" are too generic and create false positives.
  for (const entity of entities) {
    const content = getContent(entity);
    for (const target of entities) {
      if (entity.id === target.id) continue;
      const srcParts = target.source.split('/');
      const shortRef = srcParts.slice(-2).join('/'); // e.g. "cold-email-v2/SKILL.md"
      const fileRef = srcParts[srcParts.length - 1]; // e.g. "ICP.md"
      // Skip generic filenames that match too broadly
      const genericNames = new Set(['SKILL.md', 'README.md', '_master.md', 'learnings.md']);
      const useFileRef = fileRef.length > 5 && !genericNames.has(fileRef);
      if (
        content.includes(target.source) ||
        (shortRef.length > 10 && content.includes(shortRef)) ||
        (useFileRef && content.includes(fileRef))
      ) {
        rels.push({
          from: entity.id,
          to: target.id,
          rel: 'depends_on',
          created: TODAY,
          last_validated: TODAY,
          confidence: 1.0,
          evidence: `References ${target.source}`,
          source: 'auto',
        });
      }
    }
  }

  // Strategy 2: Skill name cross-refs (skip short/common names to avoid false positives)
  const COMMON_WORDS = new Set([
    'research',
    'newsletter',
    'blog',
    'content',
    'proposal',
    'interview',
    'landing',
  ]);
  const skills = entities.filter((e) => e.type === 'skill');
  for (const skill of skills) {
    const fmName = skill.name;
    if (!fmName || fmName.length < 8) continue;
    // Skip names that are common English words
    if (COMMON_WORDS.has(fmName.toLowerCase())) continue;
    for (const other of entities) {
      if (other.id === skill.id) continue;
      const content = getContent(other);
      if (content.includes(fmName)) {
        // Avoid duplicates from strategy 1
        const exists = rels.some(
          (r) => r.from === other.id && r.to === skill.id && r.rel === 'depends_on',
        );
        if (!exists) {
          rels.push({
            from: other.id,
            to: skill.id,
            rel: 'depends_on',
            created: TODAY,
            last_validated: TODAY,
            confidence: 0.8,
            evidence: `Mentions skill name "${fmName}"`,
            source: 'auto',
          });
        }
      }
    }
  }

  // Strategy 3: Case study technique overlap (2+ shared tags with a skill)
  const caseStudies = entities.filter((e) => e.type === 'case_study');
  for (const cs of caseStudies) {
    for (const skill of skills) {
      const overlap = cs.tags.filter((t) => skill.tags.includes(t));
      if (overlap.length >= 2) {
        rels.push({
          from: cs.id,
          to: skill.id,
          rel: 'validates',
          created: TODAY,
          last_validated: TODAY,
          confidence: 0.7,
          evidence: `Shared tags: ${overlap.join(', ')}`,
          source: 'auto',
        });
      }
    }
  }

  // Strategy 4: Client entity hierarchy (client-research/client-seq → client)
  const clientEntities = entities.filter((e) => e.id.startsWith('client:'));
  for (const client of clientEntities) {
    const slug = client.id.replace('client:', '');
    for (const e of entities) {
      if (e.id === client.id) continue;
      if (e.id.startsWith(`client-research:${slug}-`) || e.id.startsWith(`client-seq:${slug}-`)) {
        rels.push({
          from: e.id,
          to: client.id,
          rel: 'depends_on',
          created: TODAY,
          last_validated: TODAY,
          confidence: 1.0,
          evidence: `Belongs to client ${slug}`,
          source: 'auto',
        });
      }
    }
  }

  return rels;
}

/** Filter universal deps: entities appearing in >60% of all relationships */
function filterUniversalDeps(rels, entities) {
  const targetCounts = {};
  for (const r of rels) {
    targetCounts[r.to] = (targetCounts[r.to] || 0) + 1;
  }
  const threshold = rels.length * 0.6;
  const universalDeps = [];
  for (const [id, count] of Object.entries(targetCounts)) {
    if (count > threshold) universalDeps.push(id);
  }
  const filtered = rels.filter((r) => !universalDeps.includes(r.to));
  return { filtered, universalDeps };
}

// ---------------------------------------------------------------------------
// Health Checks
// ---------------------------------------------------------------------------

function runHealthChecks(entities, relationships) {
  const health = {
    needs_research: [],
    contradictions: [],
    broken_refs: [],
    orphans: [],
    disconnected: [],
    tag_collisions: [],
  };

  // 1. Broken references — entity source doesn't exist on disk
  for (const e of entities) {
    const fullPath = path.join(ROOT, e.source);
    if (!fs.existsSync(fullPath)) {
      health.broken_refs.push(e.id);
    }
  }

  // 2. Orphan files — SKILL.md and case study files not in entities
  const entitySources = new Set(entities.map((e) => e.source));
  // Scan both skill directories for orphan SKILL.md files
  const skillsBases = [
    path.join(ROOT, 'leadgrow-hq', '.claude', 'skills'),
    path.join(ROOT, '.claude', 'skills'),
    path.join(ROOT, 'lg-outbound', 'skills'),
    path.join(ROOT, 'lg-content', 'skills'),
    path.join(ROOT, 'lg-research', 'skills'),
    path.join(ROOT, 'lg-data', 'skills'),
    path.join(ROOT, 'lg-website', 'skills'),
  ];
  for (const skillsBase of skillsBases) {
    const allSkills = walkDir(skillsBase, (name) => name === 'SKILL.md');
    for (const sk of allSkills) {
      const rel = relPath(sk);
      if (!entitySources.has(rel)) {
        health.orphans.push(rel);
      }
    }
  }
  const csDir = path.join(ROOT, 'leadgrow-hq', 'company', 'social-proof');
  try {
    for (const f of fs.readdirSync(csDir)) {
      if (!f.endsWith('.md') || f === '_index.md' || f.startsWith('aggregate-')) continue;
      const rel = relPath(path.join(csDir, f));
      if (!entitySources.has(rel)) health.orphans.push(rel);
    }
  } catch {
    /* skip */
  }

  // 3. Tag collisions — skill pairs with >50% tag overlap
  const skills = entities.filter((e) => e.type === 'skill');
  for (let i = 0; i < skills.length; i++) {
    for (let j = i + 1; j < skills.length; j++) {
      const a = skills[i],
        b = skills[j];
      const shared = a.tags.filter((t) => b.tags.includes(t));
      const minLen = Math.min(a.tags.length, b.tags.length);
      if (minLen > 0 && shared.length / minLen > 0.5) {
        health.tag_collisions.push(`${a.id} <-> ${b.id} (${shared.join(', ')})`);
      }
    }
  }

  // 4. Disconnected entities — 0 relationships
  const connected = new Set();
  for (const r of relationships) {
    connected.add(r.from);
    connected.add(r.to);
  }
  for (const e of entities) {
    if (!connected.has(e.id)) health.disconnected.push(e.id);
  }

  // 5. Decay check — volatile entities with last_validated >60 days ago
  const sixtyDaysAgo = new Date(Date.now() - 60 * 86400000).toISOString().slice(0, 10);
  for (const e of entities) {
    if (e.decay_class === 'volatile' && e.last_validated < sixtyDaysAgo) {
      health.needs_research.push(e.id);
    }
  }

  return health;
}

// ---------------------------------------------------------------------------
// Index Builder
// ---------------------------------------------------------------------------

function buildIndex(entities, relationships, universalDeps, health) {
  const byType = {};
  const byDomain = {};
  const byTag = {};
  const byVisibility = {};

  for (const e of entities) {
    if (!byType[e.type]) byType[e.type] = [];
    byType[e.type].push(e.id);
    if (!byDomain[e.domain]) byDomain[e.domain] = [];
    byDomain[e.domain].push(e.id);
    for (const t of e.tags) {
      if (!byTag[t]) byTag[t] = [];
      byTag[t].push(e.id);
    }
    const vis = e.visibility || 'leadership';
    if (!byVisibility[vis]) byVisibility[vis] = [];
    byVisibility[vis].push(e.id);
  }

  return {
    by_type: byType,
    by_domain: byDomain,
    by_tag: byTag,
    by_visibility: byVisibility,
    universal_deps: universalDeps,
    health,
    stats: {
      entities: entities.length,
      relationships: relationships.length,
      last_indexed: new Date().toISOString(),
    },
  };
}

// ---------------------------------------------------------------------------
// Manual Relationship Preservation
// ---------------------------------------------------------------------------

function loadManualRelationships() {
  const relFile = path.join(KG_DIR, 'relationships.jsonl');
  const content = readSafe(relFile);
  if (!content) return [];
  const manual = [];
  for (const line of content.split('\n')) {
    if (!line.trim()) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.source === 'manual') manual.push(obj);
    } catch {
      /* skip malformed */
    }
  }
  return manual;
}

// ---------------------------------------------------------------------------
// Output
// ---------------------------------------------------------------------------

function formatStats(entities, relationships, health) {
  const byType = {};
  const byVisibility = {};
  for (const e of entities) {
    byType[e.type] = (byType[e.type] || 0) + 1;
    const vis = e.visibility || 'unknown';
    byVisibility[vis] = (byVisibility[vis] || 0) + 1;
  }

  const autoCount = relationships.filter((r) => r.source === 'auto').length;
  const manualCount = relationships.filter((r) => r.source === 'manual').length;

  const typeBreakdown = [
    `${byType.skill || 0} skills`,
    `${byType.case_study || 0} case studies`,
    `${byType.reference || 0} references`,
    `${byType.battlecard || 0} battlecards`,
    `${byType.rule || 0} rules`,
    `${byType.learning || 0} learnings`,
    `${byType.pattern || 0} patterns`,
  ].join(', ');

  const visBreakdown = [
    `${byVisibility.leadership || 0} leadership`,
    `${byVisibility.team || 0} team`,
    `${byVisibility.public || 0} public`,
  ].join(', ');

  return [
    'Knowledge Graph Stats:',
    `  Entities: ${entities.length} (${typeBreakdown})`,
    `  Visibility: ${visBreakdown}`,
    `  Relationships: ${relationships.length} (${autoCount} auto, ${manualCount} manual)`,
    `  Health: ${health.broken_refs.length} broken refs, ${health.orphans.length} orphans, ${health.tag_collisions.length} tag collisions, ${health.disconnected.length} disconnected`,
  ].join('\n');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const statsOnly = args.includes('--stats');

  // Scan all entity types
  const rawEntities = [
    ...scanSkills(),
    ...scanCaseStudies(),
    ...scanReferences(),
    ...scanBattlecards(),
    ...scanRules(),
    ...scanLearnings(),
    ...scanPatterns(),
    ...scanClients(),
  ];

  // Deduplicate entities by ID — first occurrence wins
  // (leadgrow-hq skills scan first, so they take priority over universal/ and root copies)
  const seenIds = new Set();
  const entities = [];
  for (const e of rawEntities) {
    if (!seenIds.has(e.id)) {
      seenIds.add(e.id);
      entities.push(e);
    }
  }

  // Assign visibility tier to each entity based on source path
  for (const entity of entities) {
    entity.visibility = assignVisibility(entity.source);
  }

  // Detect relationships
  const autoRels = detectRelationships(entities);
  const manualRels = loadManualRelationships();
  const allRels = [...autoRels, ...manualRels];

  // Filter universal deps
  const { filtered: finalRels, universalDeps } = filterUniversalDeps(allRels, entities);
  // Re-add manual rels that might have been filtered
  const outputRels = [...finalRels];
  for (const mr of manualRels) {
    if (!outputRels.some((r) => JSON.stringify(r) === JSON.stringify(mr))) {
      outputRels.push(mr);
    }
  }

  // Health checks
  const health = runHealthChecks(entities, outputRels);

  // Build index
  const index = buildIndex(entities, outputRels, universalDeps, health);

  // Output
  if (statsOnly) {
    console.log(formatStats(entities, outputRels, health));
    return;
  }

  if (dryRun) {
    console.log('[DRY RUN] Would write 3 files to knowledge-graph/\n');
    console.log(formatStats(entities, outputRels, health));
    console.log('\nSample entities:');
    const byType = {};
    for (const e of entities) {
      if (!byType[e.type]) byType[e.type] = [];
      byType[e.type].push(e);
    }
    for (const [type, items] of Object.entries(byType)) {
      console.log(`\n  ${type} (${items.length}):`);
      for (const item of items.slice(0, 3)) {
        console.log(`    ${item.id} — ${item.name} [${item.tags.join(', ')}]`);
      }
      if (items.length > 3) console.log(`    ... and ${items.length - 3} more`);
    }
    return;
  }

  // Write entities.jsonl
  const entitiesPath = path.join(KG_DIR, 'entities.jsonl');
  fs.writeFileSync(entitiesPath, entities.map((e) => JSON.stringify(e)).join('\n') + '\n', 'utf8');

  // Write relationships.jsonl
  const relsPath = path.join(KG_DIR, 'relationships.jsonl');
  fs.writeFileSync(
    relsPath,
    outputRels.map((r) => JSON.stringify(r)).join('\n') + (outputRels.length ? '\n' : ''),
    'utf8',
  );

  // Write index.json
  const indexPath = path.join(KG_DIR, 'index.json');
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n', 'utf8');

  console.log(formatStats(entities, outputRels, health));
  console.log(`\nWritten to:`);
  console.log(`  ${relPath(entitiesPath)}`);
  console.log(`  ${relPath(relsPath)}`);
  console.log(`  ${relPath(indexPath)}`);
}

main();
