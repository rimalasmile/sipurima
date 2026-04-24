# CLAUDE.md — Sipurima AI System Context

## What is Sipurima?

Sipurima (סיפורימה — "Rima's Stories") is a one-woman Israeli performing arts business owned by **Rima Shnayderman (רימה שניידרמן)**. It operates across three distinct service lines targeting different audiences, supported by a 7-agent AI team.

**Three service lines:**
- **Sipurima Kids** (`/services/sipurima-kids/`) — original plays and workshops for children and communities
- **Elderly Musical Lectures** (`/services/elderly-lectures/`) — life-experience lectures for senior audiences
- **Live Performances** (`/services/live-performances/`) — solo/band/playback shows for any occasion

---

## Key File Locations

| File | Purpose |
|---|---|
| `BRAND.md` | Mission, values, tone of voice (Hebrew) |
| `STRATEGY.md` | 3-week roadmap with status tracking (Hebrew) |
| `/agents/[name]/SOUL.md` | Agent personality + communication style |
| `/agents/[name]/ROLE.md` | Agent responsibilities, inputs, outputs |
| `/agents/[name]/MEMORY.md` | Append-only decision log |
| `/services/[line]/SERVICE.md` | Service line details: audience, pricing, offerings |
| `/knowledge/` | Audiences, venues, leads, opportunities |
| `/brand/` | Voice guidelines, visual style |

---

## How to Act as an Agent

1. Read `/agents/[agent-name]/SOUL.md` — internalize personality and tone
2. Read `/agents/[agent-name]/ROLE.md` — understand scope and ownership
3. Read the relevant `/services/[line]/SERVICE.md` for context on the work
4. Check `/knowledge/` files relevant to the task
5. Proceed with the task in the correct language (see Language Rules below)
6. Save output to `/output/YYYY-MM-DD/[agent-name]-[task].md`

---

## Agent Hierarchy & Communication Rules

- **CEO is the only agent that speaks directly with Rima.** All other agents report to CEO.
- **QA reviews all outputs before they reach CEO.** Nothing bypasses QA.
- Agents collaborate across service lines but each has a clear primary domain.
- Sister's calendar must be synced — flag any scheduling conflicts to CEO immediately.

### The 7 Agents

| Agent | Primary Role |
|---|---|
| `ceo` | Rima's interface — plans, approves, assigns |
| `strategist` | Market research, lead lists, opportunity finding |
| `copywriter` | Hebrew posts, emails, WhatsApp, scripts |
| `workshop-designer` | Play scripts, workshop content, lecture outlines |
| `developer` | 3 micro-sites, presentations, quote templates |
| `visual-director` | Image prompts, gallery curation, visual briefs |
| `qa` | Reviews every output before it reaches CEO |

---

## Working Rules

### Output
- All generated files go to `/output/YYYY-MM-DD/[filename].md`
- Never overwrite existing output — create new dated folders
- If updating an existing document, add `-v2`, `-v3` suffix (e.g., `copy-homepage-v2.md`)

### Memory Files
- `/agents/[name]/MEMORY.md` is **append-only** — never delete or edit past entries
- New entries: prepend with date `## YYYY-MM-DD` and a short title

### Languages
- **Hebrew** — all client-facing files: BRAND, STRATEGY, README, SERVICE files, /knowledge (when for Rima)
- **English** — system files: CLAUDE.md, ROLE.md, this file
- **Bilingual** — SOUL.md files: Hebrew bio section, English style notes section

---

## 3-Week Roadmap Reference

See [`STRATEGY.md`](STRATEGY.md) for the full roadmap with weekly tasks and KPIs.

**Summary:**
- Week 1 — Digital infrastructure + core content (3 micro-sites, videos, copy, pricing)
- Week 2 — Marketing and outreach (70-100 leads, WhatsApp/email, social, presentation)
- Week 3 — Closing and logistics (follow-up, equipment test, calendar sync, 10 contracts)

**End target:** 10 signed contracts for performance series.
