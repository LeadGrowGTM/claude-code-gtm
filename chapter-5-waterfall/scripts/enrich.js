#!/usr/bin/env node
/**
 * Enrichment Waterfall
 * Tier 1: Free (website scrape, LinkedIn signals)
 * Tier 2: Cheap APIs (OpenWebNinja $0.002/query, TechSight free)
 * Tier 3: Paid fallbacks (configure in .env)
 *
 * Usage: node enrich.js <domain>
 *        node enrich.js --csv leads.csv --output enriched.csv
 */

import { readFileSync, writeFileSync } from 'fs';

const domain = process.argv[2];

if (!domain) {
  console.error('Usage: node enrich.js <domain>');
  console.error('       node enrich.js --csv leads.csv --output enriched.csv');
  process.exit(1);
}

async function enrichDomain(domain) {
  console.log(`\nEnriching: ${domain}`);
  const result = { domain, tier: null, data: {} };

  // ── TIER 1: Free sources ─────────────────────────────────────────────────

  // 1a. Website scrape
  try {
    const websiteData = await scrapeWebsite(domain);
    if (websiteData) {
      result.data.description = websiteData.description;
      result.data.icp_signals = websiteData.signals;
      result.tier = 1;
      console.log(`  ✓ Tier 1 (website): ${websiteData.description?.slice(0, 60)}...`);
    }
  } catch (e) {
    console.log(`  ✗ Tier 1 (website): ${e.message}`);
  }

  // 1b. TechSight — free tech stack detection
  try {
    const techStack = await runTechSight(domain);
    if (techStack?.length > 0) {
      result.data.tech_stack = techStack;
      result.tier = result.tier || 1;
      console.log(`  ✓ Tier 1 (TechSight): ${techStack.join(', ')}`);
    }
  } catch (e) {
    console.log(`  ✗ Tier 1 (TechSight): ${e.message}`);
  }

  // ── TIER 2: Cheap APIs ───────────────────────────────────────────────────

  if (!result.data.description || !result.data.tech_stack) {
    const openWebNinjaKey = process.env.OPENWEBNINJA_API_KEY;
    if (openWebNinjaKey) {
      try {
        const aiData = await queryOpenWebNinja(domain, openWebNinjaKey);
        if (aiData) {
          result.data.ai_summary = aiData;
          result.tier = 2;
          console.log(`  ✓ Tier 2 (OpenWebNinja): summary acquired`);
        }
      } catch (e) {
        console.log(`  ✗ Tier 2 (OpenWebNinja): ${e.message}`);
      }
    }
  }

  // ── TIER 3: Paid fallbacks ───────────────────────────────────────────────

  if (!result.tier) {
    // Add your paid enrichment API calls here
    // e.g., Clay, FullEnrich, Apollo
    console.log(`  → Tier 3: no free/cheap data found — route to paid enrichment`);
    result.tier = 3;
    result.data.needs_paid_enrichment = true;
  }

  return result;
}

// ── Source implementations ────────────────────────────────────────────────

async function scrapeWebsite(domain) {
  const url = `https://${domain}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; enrichbot/1.0)' },
    signal: AbortSignal.timeout(8000),
  });
  if (!res.ok) return null;
  const html = await res.text();

  // Extract meta description
  const descMatch = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)/i);
  const description = descMatch?.[1] || null;

  // Look for ICP signals in content
  const signals = [];
  const signalKeywords = ['B2B', 'SaaS', 'enterprise', 'startup', 'scale', 'outbound', 'sales', 'revenue'];
  for (const kw of signalKeywords) {
    if (html.toLowerCase().includes(kw.toLowerCase())) signals.push(kw);
  }

  return description ? { description, signals } : null;
}

async function runTechSight(domain) {
  // Requires techsight CLI installed: github.com/LeadGrowGTM/techsight
  const { execSync } = await import('child_process');
  try {
    const output = execSync(`techsight ${domain} --json`, { timeout: 10000 }).toString();
    const parsed = JSON.parse(output);
    return parsed.technologies || [];
  } catch {
    return null;
  }
}

async function queryOpenWebNinja(domain, apiKey) {
  // $0.002/query — Tier 2 only fires on Tier 1 miss
  const res = await fetch(
    `https://api.openwebninja.com/google-ai-mode/ai-mode?prompt=company overview for ${domain}`,
    { headers: { 'x-api-key': apiKey } }
  );
  if (!res.ok) return null;
  const data = await res.json();
  return data.answer || null;
}

// ── Main ──────────────────────────────────────────────────────────────────

const result = await enrichDomain(domain);

console.log('\n── Enrichment Result ──');
console.log(JSON.stringify(result, null, 2));
