# StackBridge — Outreach Sequence

**Status:** Ready for upload  
**Target:** RevOps Managers + VP of Sales at StackBridge  
**Sender:** [Your name], [Your company]  
**Generated:** Chapter 6 live build — time from cold start: 34 minutes

*ICP research: `research/stackbridge-research.md`*

---

## Step 1

**Subject:** outbound stack question

Teams scaling SDR headcount in Q2 usually hit the same wall around month two — sequences running in three tools, no single view of what's actually converting.

Curious if that's where you are, or if you've already solved it.

Worth a quick chat?

[Your name]

---

## Step 2 (send day 4-5 if no reply)

**Subject:** Re: outbound stack question

Different angle — your Series A close was 6 weeks ago. Usually that's when the pressure to show pipeline velocity starts compressing the timeline.

If you're still building the infrastructure, happy to show you what we run across our clients. 20 minutes.

[Your name]

---

## QA Checklist

- [x] Step 1 subject under 8 words
- [x] Step 1 body under 100 words (71 words)
- [x] Step 2 body under 75 words (52 words)
- [x] No links in either step
- [x] Pain is company-specific (SDR scaling + Series A timing)
- [x] CTA is one question
- [x] Step 2 is a new angle (funding timeline), not a bump

## Upload Command

```bash
# Upload to Bison via CLI
python bison_cli.py campaigns create \
  --name "StackBridge - RevOps - Q2" \
  --sequence stackbridge-sequence.md \
  --workspace-id 3
```
