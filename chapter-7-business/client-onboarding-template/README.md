# Client Onboarding Template

Use this when closing a new client. Creates their workspace and loads context into the system.

**Time:** 30-90 minutes depending on how much client context exists.

---

## Step 1 — Create client directory

```bash
mkdir -p clients/[client-name]/{research,campaigns,sequences,reports}
cp client-onboarding-template/_master.md clients/[client-name]/_master.md
```

## Step 2 — Fill in `_master.md`

Required fields:
- Company name + domain
- ICP definition (title, company size, vertical)
- Offer in one sentence
- Sending domain + sender name
- Current tools (CRM, MAP, data source)

## Step 3 — Load existing campaign data (if any)

If they've run outbound before:
```
"Here's copy from [client]'s previous sequences: [paste]. Analyze what was working, what wasn't. Save to clients/[client]/research/historical-campaigns.md"
```

## Step 4 — Configure Bison workspace

```bash
python bison_cli.py workspace set --id [workspace-id]
python bison_cli.py campaigns list  # verify connection
```

## Step 5 — First ICP research pass

Pick 3-5 companies from their target list and run the `icp-research` skill on each. This calibrates the ICP score against their actual targets, not hypothetical ones.

---

## Files in This Template

- `_master.md` — client brief (fill in per client)

---
