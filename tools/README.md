# Tools

Open-source CLIs and utilities referenced in the course.

| Tool | Repo | Use case | Cost |
|------|------|---------|------|
| **Bison CLI** | [LeadGrowGTM/bison-cli](https://github.com/LeadGrowGTM/bison-cli) | EmailBison campaign management — list upload, sequence setup, campaign launch | Free (requires Bison account) |
| **TechSight** | [LeadGrowGTM/techsight](https://github.com/LeadGrowGTM/techsight) | Tech stack detection from domain — used in enrichment waterfall Tier 1 | Free |
| **GSD Plugin** | [get-shit-done](https://github.com/anthropics/claude-code-skill-template) | Planning system used throughout the course for phase management | Free |
| **youtube-transcript** | [badlogic/pi-skills](https://github.com/badlogic/pi-skills/tree/main/youtube-transcript) | Fetch YouTube transcripts for research | Free |

## Install

```bash
# Bison CLI
git clone https://github.com/LeadGrowGTM/bison-cli
pip install -e bison-cli

# TechSight
git clone https://github.com/LeadGrowGTM/techsight
pip install -e techsight

# youtube-transcript
cd tools/youtube-transcript && npm install
```
