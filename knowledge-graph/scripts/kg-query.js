#!/usr/bin/env node

/**
 * kg-query.js - Knowledge graph search CLI
 *
 * Usage:
 *   bun knowledge-graph/scripts/kg-query.js search "cold email"
 *   bun knowledge-graph/scripts/kg-query.js search "cold email" --visibility team
 *   bun knowledge-graph/scripts/kg-query.js search "cold email" --repos leadgrow-hq,gtme-skills
 *   bun knowledge-graph/scripts/kg-query.js search "cold email" --visibility public --repos leadgrow-hq
 *
 * Visibility levels:
 *   --visibility public      Show only public entities
 *   --visibility team        Show team + public entities
 *   --visibility leadership  Show all entities (default)
 *
 * Federation:
 *   --repos repo1,repo2      Search entities.jsonl from multiple repos
 *                             Repos configured in knowledge-graph/federation.json
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = path.resolve(__dirname, '..', '..');
const ENTITIES_PATH = path.join(WORKSPACE_ROOT, 'knowledge-graph', 'entities.jsonl');
const INDEX_PATH = path.join(WORKSPACE_ROOT, 'knowledge-graph', 'index.json');
const FEDERATION_PATH = path.join(WORKSPACE_ROOT, 'knowledge-graph', 'federation.json');

// Visibility hierarchy: public < team < leadership
const VISIBILITY_LEVELS = { public: 0, team: 1, leadership: 2 };

function loadFederationConfig() {
  try {
    const content = fs.readFileSync(FEDERATION_PATH, 'utf8');
    return JSON.parse(content);
  } catch {
    return { repos: { 'leadgrow-hq': { path: '.', visibility_filter: null } } };
  }
}

function loadEntitiesFromFile(filePath) {
  if (!fs.existsSync(filePath)) return [];
  const lines = fs.readFileSync(filePath, 'utf8').trim().split('\n');
  return lines
    .filter((l) => l.trim())
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

function loadEntities(repoNames) {
  const federation = loadFederationConfig();

  // If no repos specified, use local only
  if (!repoNames || repoNames.length === 0) {
    return loadEntitiesFromFile(ENTITIES_PATH);
  }

  const allEntities = [];
  for (const repoName of repoNames) {
    const repoConfig = federation.repos[repoName];
    if (!repoConfig) {
      console.error(`Warning: repo "${repoName}" not found in federation.json, skipping.`);
      continue;
    }

    // Resolve path (relative to workspace root or absolute)
    let repoPath = repoConfig.path;
    if (repoPath === '.') {
      repoPath = WORKSPACE_ROOT;
    } else if (!path.isAbsolute(repoPath)) {
      repoPath = path.resolve(WORKSPACE_ROOT, repoPath);
    }

    const entitiesFile = path.join(repoPath, 'knowledge-graph', 'entities.jsonl');
    const entities = loadEntitiesFromFile(entitiesFile);

    // Apply repo-level visibility filter
    const visFilter = repoConfig.visibility_filter;
    for (const entity of entities) {
      // Tag entity with source repo for federated results
      entity._repo = repoName;

      if (visFilter) {
        const entityVis = entity.visibility || 'leadership';
        if (!visFilter.includes(entityVis)) continue;
      }
      allEntities.push(entity);
    }
  }

  return allEntities;
}

function filterByVisibility(entities, visibilityLevel) {
  if (!visibilityLevel || visibilityLevel === 'leadership') return entities;

  const maxLevel = VISIBILITY_LEVELS[visibilityLevel];
  if (maxLevel === undefined) {
    console.error(`Unknown visibility level: ${visibilityLevel}. Use: public, team, leadership`);
    process.exit(1);
  }

  return entities.filter((entity) => {
    const entityVis = entity.visibility || 'leadership';
    const entityLevel = VISIBILITY_LEVELS[entityVis] || 2;
    return entityLevel <= maxLevel;
  });
}

function scoreEntity(entity, query) {
  const lowerQuery = query.toLowerCase();
  // Also try hyphenated version for multi-word queries (e.g., "cold email" -> "cold-email")
  const hyphenated = lowerQuery.replace(/\s+/g, '-');
  const terms = lowerQuery.split(/\s+/).filter((t) => t.length > 1);
  let score = 0;

  if (entity.tags) {
    // Exact tag match (including hyphenated form) = 3 points
    if (entity.tags.some((tag) => tag === lowerQuery || tag === hyphenated)) {
      score += 3;
    }
    // Individual term tag matches = 1 point each
    for (const term of terms) {
      if (entity.tags.some((tag) => tag === term || tag.includes(term))) {
        score += 1;
      }
    }
  }

  // Trigger phrase match = 4 points (highest priority — exact intent signals)
  if (entity.triggers && entity.triggers.length > 0) {
    for (const trigger of entity.triggers) {
      const lowerTrigger = trigger.toLowerCase();
      // Full trigger contains query or query contains trigger
      if (lowerTrigger.includes(lowerQuery) || lowerQuery.includes(lowerTrigger)) {
        score += 4;
        break;
      }
      // Any term appears in a trigger phrase
      for (const term of terms) {
        if (lowerTrigger.includes(term)) {
          score += 1;
          break;
        }
      }
    }
  }

  // Description search = 2 points for phrase match, 1 for term match
  if (entity.description) {
    const lowerDesc = entity.description.toLowerCase();
    if (lowerDesc.includes(lowerQuery)) {
      score += 2;
    } else {
      let termHits = 0;
      for (const term of terms) {
        if (term.length >= 4 && lowerDesc.includes(term)) termHits++;
      }
      if (termHits >= 2) score += 1;
    }
  }

  // Name contains = 2 points
  if (entity.name && entity.name.toLowerCase().includes(lowerQuery)) {
    score += 2;
  }

  // ID contains any term = 1 point each
  if (entity.id) {
    const lid = entity.id.toLowerCase();
    for (const term of terms) {
      if (lid.includes(term)) score += 1;
    }
  }

  return score;
}

function search(query, opts) {
  const entities = loadEntities(opts.repos);

  if (entities.length === 0) {
    console.error('Error: no entities found. Run kg-index.js first, or check --repos config.');
    process.exit(1);
  }

  // Apply visibility filter
  const filtered = filterByVisibility(entities, opts.visibility);

  // Score and filter results
  const results = filtered
    .map((entity) => ({ entity, score: scoreEntity(entity, query) }))
    .filter((result) => result.score > 0)
    .sort((a, b) => b.score - a.score);

  if (results.length === 0) {
    console.log(`No results found for: ${query}`);
    if (opts.visibility && opts.visibility !== 'leadership') {
      console.log(`  (filtered to visibility: ${opts.visibility})`);
    }
    return;
  }

  // Group by type
  const byType = {};
  results.forEach(({ entity }) => {
    if (!byType[entity.type]) byType[entity.type] = [];
    byType[entity.type].push(entity);
  });

  // Display results
  const filterNote =
    opts.visibility && opts.visibility !== 'leadership' ? ` [visibility: ${opts.visibility}]` : '';
  const repoNote = opts.repos && opts.repos.length > 0 ? ` [repos: ${opts.repos.join(', ')}]` : '';
  console.log(
    `Search: "${query}" — ${results.length} result${results.length === 1 ? '' : 's'}${filterNote}${repoNote}\n`,
  );

  const typeLabels = {
    skill: 'SKILLS',
    case_study: 'CASE STUDIES',
    reference: 'REFERENCES',
    battlecard: 'BATTLECARDS',
    rule: 'RULES',
    learning: 'LEARNINGS',
    pattern: 'PATTERNS',
  };

  Object.entries(byType).forEach(([type, entities]) => {
    const label = typeLabels[type] || type.toUpperCase();
    console.log(`${label} (${entities.length})`);

    entities.forEach((entity) => {
      const repoTag = entity._repo && entity._repo !== 'leadgrow-hq' ? ` [${entity._repo}]` : '';
      console.log(`  ${entity.id} — ${entity.name}${repoTag}`);
      // Show description for better discovery context
      if (entity.description) {
        const desc =
          entity.description.length > 120
            ? entity.description.slice(0, 117) + '...'
            : entity.description;
        console.log(`    Desc: ${desc}`);
      }
      // Show trigger phrases when present (natural language entry points)
      if (entity.triggers && entity.triggers.length > 0) {
        console.log(`    Triggers: ${entity.triggers.slice(0, 4).join(' | ')}`);
      }
      console.log(`    Tags: ${entity.tags ? entity.tags.join(', ') : 'none'}`);
      console.log(`    Source: ${entity.source}`);
      console.log(
        `    Domain: ${entity.domain || 'unknown'} | Decay: ${entity.decay_class || 'unknown'} | Visibility: ${entity.visibility || 'unknown'}`,
      );
      console.log();
    });
  });
}

function parseArgs(args) {
  const opts = { visibility: null, repos: null };
  const positional = [];

  let i = 0;
  while (i < args.length) {
    if (args[i] === '--visibility' && i + 1 < args.length) {
      opts.visibility = args[i + 1];
      i += 2;
    } else if (args[i] === '--repos' && i + 1 < args.length) {
      opts.repos = args[i + 1]
        .split(',')
        .map((r) => r.trim())
        .filter(Boolean);
      i += 2;
    } else {
      positional.push(args[i]);
      i++;
    }
  }

  return { positional, opts };
}

function main() {
  const args = process.argv.slice(2);
  const { positional, opts } = parseArgs(args);

  if (positional.length === 0 || positional[0] !== 'search') {
    console.log(
      'Usage: bun knowledge-graph/scripts/kg-query.js search "query" [--visibility level] [--repos repo1,repo2]',
    );
    console.log('');
    console.log('Options:');
    console.log(
      '  --visibility public|team|leadership   Filter by visibility tier (default: leadership = all)',
    );
    console.log(
      '  --repos repo1,repo2                   Search across federated repos (see federation.json)',
    );
    process.exit(1);
  }

  const query = positional.slice(1).join(' ');
  if (!query) {
    console.log('Error: search query required');
    console.log(
      'Usage: bun knowledge-graph/scripts/kg-query.js search "query" [--visibility level] [--repos repo1,repo2]',
    );
    process.exit(1);
  }

  search(query, opts);
}

main();
