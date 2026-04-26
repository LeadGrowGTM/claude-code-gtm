#!/usr/bin/env node

/**
 * kg-skill-graph.js — Skill Graph Generator
 *
 * Builds a machine-readable skill graph from the knowledge graph, mapping:
 *   - Trigger phrases per skill (natural language → skill lookup)
 *   - Skill dependencies (which skills reference which)
 *   - Workflow chains (A → B → C sequences detected from skill bodies)
 *   - Alternative skills (same job, different approach)
 *   - Skill clusters by domain
 *
 * Usage:
 *   bun knowledge-graph/scripts/kg-skill-graph.js           # full rebuild
 *   bun knowledge-graph/scripts/kg-skill-graph.js --dry-run  # preview
 *   bun knowledge-graph/scripts/kg-skill-graph.js --query "write cold email"
 *
 * Output: knowledge-graph/skill-graph.json
 *
 * Design philosophy (Karpathy-style RAG):
 *   The skill graph is the "attention pattern" layer — it tells Claude
 *   which skills to co-load when any given skill is invoked. Like sparse
 *   attention, we only load high-signal neighbors, not all 76 skills.
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const KG_DIR = path.join(WORKSPACE_ROOT, 'knowledge-graph');
const ENTITIES_PATH = path.join(KG_DIR, 'entities.jsonl');
const RELS_PATH = path.join(KG_DIR, 'relationships.jsonl');
const SKILL_GRAPH_PATH = path.join(KG_DIR, 'skill-graph.json');

// ---------------------------------------------------------------------------
// Loaders
// ---------------------------------------------------------------------------

function loadEntities() {
  if (!fs.existsSync(ENTITIES_PATH)) return [];
  return fs
    .readFileSync(ENTITIES_PATH, 'utf8')
    .trim()
    .split('\n')
    .filter(Boolean)
    .map((l) => {
      try {
        return JSON.parse(l);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

function loadRelationships() {
  if (!fs.existsSync(RELS_PATH)) return [];
  return fs
    .readFileSync(RELS_PATH, 'utf8')
    .trim()
    .split('\n')
    .filter(Boolean)
    .map((l) => {
      try {
        return JSON.parse(l);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

function readSkillBody(sourcePath) {
  const fullPath = path.join(WORKSPACE_ROOT, sourcePath);
  try {
    return fs.readFileSync(fullPath, 'utf8');
  } catch {
    return '';
  }
}

// ---------------------------------------------------------------------------
// Workflow chain detection
// ---------------------------------------------------------------------------

/**
 * Detect "then use X" or "next: X" patterns in skill body text.
 * Returns array of skill IDs that this skill chains into.
 */
function detectWorkflowNext(body, allSkillIds) {
  const next = [];
  const patterns = [
    /then (?:use|run|apply|load|invoke)\s+["']?([a-z][a-z0-9-]+)["']?/gi,
    /next[,:]?\s+(?:use|run|apply|load)\s+["']?([a-z][a-z0-9-]+)["']?/gi,
    /after (?:this|running|completing)[,:]?\s+(?:use|run|apply|load)\s+["']?([a-z][a-z0-9-]+)["']?/gi,
    /→\s*["']?([a-z][a-z0-9-]+)["']?/g,
    /step \d+[:.]\s+["']?([a-z][a-z0-9-]+)["']?/gi,
  ];

  for (const pattern of patterns) {
    let m;
    while ((m = pattern.exec(body)) !== null) {
      const candidate = m[1].toLowerCase().trim();
      const skillId = `skill:${candidate}`;
      if (allSkillIds.has(skillId) && !next.includes(skillId)) {
        next.push(skillId);
      }
    }
  }
  return next;
}

/**
 * Detect "use X first" or "requires X" patterns — prerequisite skills.
 */
function detectPrerequisites(body, allSkillIds) {
  const prereqs = [];
  const patterns = [
    /(?:use|run|load|apply)\s+["']?([a-z][a-z0-9-]+)["']?\s+first/gi,
    /requires?\s+["']?([a-z][a-z0-9-]+)["']?/gi,
    /after (?:running|using|applying)\s+["']?([a-z][a-z0-9-]+)["']?/gi,
    /build(?:ing)? on\s+["']?([a-z][a-z0-9-]+)["']?/gi,
  ];

  for (const pattern of patterns) {
    let m;
    while ((m = pattern.exec(body)) !== null) {
      const candidate = m[1].toLowerCase().trim();
      const skillId = `skill:${candidate}`;
      if (allSkillIds.has(skillId) && !prereqs.includes(skillId)) {
        prereqs.push(skillId);
      }
    }
  }
  return prereqs;
}

// ---------------------------------------------------------------------------
// Alternative skill detection (Jaccard similarity on tags)
// ---------------------------------------------------------------------------

function jaccardSimilarity(a, b) {
  const setA = new Set(a);
  const setB = new Set(b);
  const intersection = [...setA].filter((t) => setB.has(t)).length;
  const union = new Set([...setA, ...setB]).size;
  return union === 0 ? 0 : intersection / union;
}

function findAlternatives(skill, allSkills, threshold = 0.35) {
  return allSkills
    .filter((s) => s.id !== skill.id && s.domain === skill.domain)
    .map((s) => ({
      id: s.id,
      similarity: jaccardSimilarity(skill.tags || [], s.tags || []),
    }))
    .filter((r) => r.similarity >= threshold)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 3)
    .map((r) => r.id);
}

// ---------------------------------------------------------------------------
// Trigger index builder
// ---------------------------------------------------------------------------

/**
 * Build a reverse lookup: trigger phrase → [skill_id, ...]
 * Used by Claude to find the right skill from natural language.
 */
function buildTriggerIndex(skills) {
  const index = {};
  for (const skill of skills) {
    if (!skill.triggers || skill.triggers.length === 0) continue;
    for (const trigger of skill.triggers) {
      const key = trigger.toLowerCase().trim();
      if (!index[key]) index[key] = [];
      if (!index[key].includes(skill.id)) {
        index[key].push(skill.id);
      }
    }
  }
  return index;
}

// ---------------------------------------------------------------------------
// Workflow chain builder (A → B → C)
// ---------------------------------------------------------------------------

/**
 * Build explicit workflow chains by traversing "next" relationships.
 * Returns named workflows found in skill bodies.
 *
 * Example: "cold email workflow" = situation-targeting → cold-email-v2 → email-campaign-setup
 */
function buildWorkflowChains(skills, skillNodes) {
  const chains = {};

  // Defined workflow sequences based on domain knowledge
  const knownWorkflows = {
    'cold-email-pipeline': {
      description: 'Full cold email pipeline from ICP to live campaign',
      steps: [
        'skill:situation-targeting',
        'skill:cold-email-v2',
        'skill:email-campaign-setup',
        'skill:email-campaign-analyze',
      ],
    },
    'content-pipeline': {
      description: 'Content creation from transcript to published post',
      steps: ['skill:pull-transcript', 'skill:linkedin-content', 'skill:push-content'],
    },
    'client-onboarding': {
      description: 'New client setup and campaign launch',
      steps: [
        'skill:icp-qualification',
        'skill:situation-targeting',
        'skill:campaign-copywriting',
        'skill:email-campaign-setup',
      ],
    },
    'campaign-review': {
      description: 'Review campaign performance and optimize',
      steps: [
        'skill:email-campaign-analyze',
        'skill:cross-client-ground-truth',
        'skill:campaign-state-of-market',
      ],
    },
    'lead-enrichment': {
      description: 'Build and enrich a lead list for outreach',
      steps: [
        'skill:discolike-discovery',
        'skill:csv-merge-dedupe',
        'skill:waterfall-enrich',
        'skill:cold-email-v2',
      ],
    },
    'proposal-pipeline': {
      description: 'From discovery call to sent proposal',
      steps: ['skill:pull-transcript', 'skill:proposal-from-transcript', 'skill:create-proposal'],
    },
    'playbook-generation': {
      description: 'Build a market takeover playbook for a client',
      steps: [
        'skill:scrape-website',
        'skill:spider-llm',
        'skill:company-research',
        'skill:situation-targeting',
      ],
    },
  };

  // Validate that referenced skills exist
  const skillIdSet = new Set(skills.map((s) => s.id));
  for (const [name, workflow] of Object.entries(knownWorkflows)) {
    const validSteps = workflow.steps.filter((id) => skillIdSet.has(id));
    if (validSteps.length >= 2) {
      chains[name] = {
        description: workflow.description,
        steps: validSteps,
        // Mark any gaps where the skill doesn't exist
        missing_steps: workflow.steps.filter((id) => !skillIdSet.has(id)),
      };
    }
  }

  return chains;
}

// ---------------------------------------------------------------------------
// Domain cluster builder
// ---------------------------------------------------------------------------

function buildDomainClusters(skills) {
  const clusters = {};
  for (const skill of skills) {
    const domain = skill.domain || 'operations';
    if (!clusters[domain]) clusters[domain] = [];
    clusters[domain].push({
      id: skill.id,
      name: skill.name,
      description: skill.description || '',
      triggers: skill.triggers || [],
      source: skill.source,
    });
  }
  return clusters;
}

// ---------------------------------------------------------------------------
// Main graph builder
// ---------------------------------------------------------------------------

function buildSkillGraph(entities, relationships) {
  const skills = entities.filter((e) => e.type === 'skill');
  const allSkillIds = new Set(skills.map((s) => s.id));

  // Build per-skill nodes
  const nodes = {};
  for (const skill of skills) {
    const body = readSkillBody(skill.source);

    // Dependencies from relationships (skill → reference/skill)
    const deps = relationships
      .filter((r) => r.from === skill.id && r.rel === 'depends_on')
      .map((r) => ({ id: r.to, confidence: r.confidence || 1.0, evidence: r.evidence || '' }))
      .filter((d) => !d.id.startsWith('client-')); // skip noisy client-specific deps

    // What validates this skill (case studies)
    const validatedBy = relationships
      .filter((r) => r.to === skill.id && r.rel === 'validates')
      .map((r) => r.from);

    // Detect workflow chains in body text
    const workflowNext = detectWorkflowNext(body, allSkillIds);
    const prerequisites = detectPrerequisites(body, allSkillIds);

    // Find alternative skills (same domain, high tag overlap)
    const alternatives = findAlternatives(skill, skills);

    nodes[skill.id] = {
      id: skill.id,
      name: skill.name,
      description: skill.description || '',
      domain: skill.domain || 'operations',
      source: skill.source,
      triggers: skill.triggers || [],
      tags: skill.tags || [],
      dependencies: deps.slice(0, 10), // cap to reduce noise
      workflow_next: workflowNext,
      prerequisites,
      alternatives,
      validated_by: validatedBy,
      visibility: skill.visibility || 'team',
      decay_class: skill.decay_class || 'durable',
      last_validated: skill.last_validated || '',
    };
  }

  // Build trigger index (reverse lookup: phrase → skill IDs)
  const triggerIndex = buildTriggerIndex(skills);

  // Build workflow chains
  const workflowChains = buildWorkflowChains(skills, nodes);

  // Build domain clusters
  const domainClusters = buildDomainClusters(skills);

  // Compute hub skills (most connected)
  const connectionCount = {};
  for (const r of relationships) {
    connectionCount[r.from] = (connectionCount[r.from] || 0) + 1;
    connectionCount[r.to] = (connectionCount[r.to] || 0) + 1;
  }
  const hubSkills = Object.entries(connectionCount)
    .filter(([id]) => id.startsWith('skill:'))
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([id, count]) => ({ id, connections: count }));

  return {
    version: '1.0.0',
    generated: new Date().toISOString(),
    stats: {
      total_skills: skills.length,
      skills_with_triggers: skills.filter((s) => s.triggers && s.triggers.length > 0).length,
      total_trigger_phrases: Object.keys(triggerIndex).length,
      workflow_chains: Object.keys(workflowChains).length,
      domains: Object.keys(domainClusters).length,
    },
    // Primary lookup: skill ID → full node data
    nodes,
    // Reverse lookup: trigger phrase → skill IDs
    trigger_index: triggerIndex,
    // Named workflow sequences
    workflow_chains: workflowChains,
    // Skills grouped by domain
    domain_clusters: domainClusters,
    // Most-connected skills (likely entry points)
    hub_skills: hubSkills,
  };
}

// ---------------------------------------------------------------------------
// Query mode — find skill from natural language
// ---------------------------------------------------------------------------

function queryGraph(query, graph) {
  const lowerQuery = query.toLowerCase();
  const terms = lowerQuery.split(/\s+/).filter((t) => t.length > 2);
  const results = [];

  // 1. Exact trigger match
  for (const [phrase, skillIds] of Object.entries(graph.trigger_index)) {
    if (phrase.includes(lowerQuery) || lowerQuery.includes(phrase)) {
      for (const id of skillIds) {
        results.push({ id, score: 10, matched_on: `trigger: "${phrase}"` });
      }
    }
  }

  // 2. Term-based trigger match
  for (const [phrase, skillIds] of Object.entries(graph.trigger_index)) {
    const hits = terms.filter((t) => phrase.includes(t)).length;
    if (hits >= 2) {
      for (const id of skillIds) {
        if (!results.find((r) => r.id === id)) {
          results.push({ id, score: hits * 2, matched_on: `trigger terms in: "${phrase}"` });
        }
      }
    }
  }

  // 3. Description match
  for (const [id, node] of Object.entries(graph.nodes)) {
    if (!results.find((r) => r.id === id)) {
      const desc = node.description.toLowerCase();
      const hits = terms.filter((t) => desc.includes(t)).length;
      if (hits >= 2 || desc.includes(lowerQuery)) {
        results.push({ id, score: hits, matched_on: 'description' });
      }
    }
  }

  // 4. Tag match
  for (const [id, node] of Object.entries(graph.nodes)) {
    if (!results.find((r) => r.id === id)) {
      const tagHits = (node.tags || []).filter((t) =>
        terms.some((term) => t.includes(term)),
      ).length;
      if (tagHits >= 1) {
        results.push({ id, score: tagHits, matched_on: 'tags' });
      }
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, 8);
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const queryArg = args.indexOf('--query');

  // Load data
  const entities = loadEntities();
  const relationships = loadRelationships();

  if (entities.length === 0) {
    console.error('No entities found. Run kg-index.js first.');
    process.exit(1);
  }

  // Build graph
  const graph = buildSkillGraph(entities, relationships);

  // Query mode
  if (queryArg >= 0 && args[queryArg + 1]) {
    const query = args.slice(queryArg + 1).join(' ');
    const results = queryGraph(query, graph);
    console.log(`\nSkill lookup: "${query}"\n`);
    if (results.length === 0) {
      console.log('No matching skills found.');
    } else {
      for (const r of results) {
        const node = graph.nodes[r.id];
        console.log(`  ${r.id} (score: ${r.score}, matched: ${r.matched_on})`);
        console.log(`    ${node.description.slice(0, 100)}`);
        if (node.triggers.length > 0) {
          console.log(`    Triggers: ${node.triggers.slice(0, 3).join(' | ')}`);
        }
        console.log();
      }
    }
    return;
  }

  // Stats / dry run
  if (dryRun) {
    console.log('[DRY RUN] Skill graph preview:\n');
    console.log(`  Total skills: ${graph.stats.total_skills}`);
    console.log(`  Skills with triggers: ${graph.stats.skills_with_triggers}`);
    console.log(`  Total trigger phrases: ${graph.stats.total_trigger_phrases}`);
    console.log(`  Workflow chains: ${graph.stats.workflow_chains}`);
    console.log('\nWorkflow chains:');
    for (const [name, chain] of Object.entries(graph.workflow_chains)) {
      console.log(`  ${name}: ${chain.steps.join(' → ')}`);
    }
    console.log('\nHub skills (most connected):');
    for (const h of graph.hub_skills.slice(0, 5)) {
      console.log(`  ${h.id} (${h.connections} connections)`);
    }
    console.log('\nTrigger index sample:');
    const triggerSample = Object.entries(graph.trigger_index).slice(0, 10);
    for (const [phrase, ids] of triggerSample) {
      console.log(`  "${phrase}" → ${ids.join(', ')}`);
    }
    return;
  }

  // Write skill-graph.json
  fs.writeFileSync(SKILL_GRAPH_PATH, JSON.stringify(graph, null, 2) + '\n', 'utf8');
  console.log('Skill graph written to knowledge-graph/skill-graph.json');
  console.log(`  ${graph.stats.total_skills} skills`);
  console.log(`  ${graph.stats.total_trigger_phrases} trigger phrases`);
  console.log(`  ${graph.stats.workflow_chains} workflow chains`);
  console.log(`\nUsage:`);
  console.log(`  bun knowledge-graph/scripts/kg-skill-graph.js --query "write cold email"`);
  console.log(`  bun knowledge-graph/scripts/kg-skill-graph.js --dry-run`);
}

main();
