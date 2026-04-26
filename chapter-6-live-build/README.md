# Chapter 6 — The Live GTM Build

**Time:** 50 min | **Chapter goal:** Watch (or diff) a cold company go from zero to live campaign.

---

## What Happens

I pick a company I've never researched. Timer starts. No prep, no edits.

Sequence:
1. Spawn researcher agent on the company
2. Run ICP research skill against the output
3. Run enrichment waterfall
4. Generate cold-email Step 1 + Step 2 from research
5. QA against quality gates
6. Upload to Bison via CLI
7. Set campaign live

Everything in chapters 1-5 is already in place. This chapter is where it runs together.

---

## The Before/After Diff

Don't want to watch the full 50 minutes? Diff the folders:

```bash
# See everything that changed during the live session
diff -rq before/ after/

# See full content of what was built
diff -r before/ after/
```

Or in git:
```bash
git diff HEAD -- chapter-6-live-build/before/ chapter-6-live-build/after/
```

### Before state
`before/` contains a workspace with Claude Code installed but no GTM infrastructure yet — no rules, no skills, no agents. Just a bare CLAUDE.md.

### After state
`after/` contains everything the live session produced:
- Rules added (ask-vs-act, archive-safety, scope-before-execute)
- Skills created (icp-research, cold-email)
- Company research doc
- Two-email sequence ready for upload

---

## Key Things to Watch

**Research quality:** The researcher agent reads the website, job postings, and any available signals. Watch how much context it surfaces in one pass vs. what a manual SDR would catch.

**Skill invocation:** When the ICP research skill runs, notice how it doesn't need re-prompting. The SKILL.md intake requirements pull exactly what's needed.

**Speed:** The bottleneck isn't writing — it's thinking. The sequence is done before you'd finish reading the first SDR's draft.

---

## Next Chapter

[Chapter 7 →](../chapter-7-business/README.md) — The headcount math. What this does to your cost of delivery.
