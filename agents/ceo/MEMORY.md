# CEO — Memory Log

<!-- APPEND-ONLY. Never delete or edit past entries.
     Format: ## YYYY-MM-DD — Short title
     Then a brief note on what was decided, learned, or flagged. -->

## 2026-04-18 — Project initialized

Sipurima folder structure created. Root files, service files, and CEO agent files are live.
Rima confirmed: name spelling is רימה שניידרמן. Kids service defined as תיאטרון ילדים חוויתי.
Awaiting Rima's "go" to build remaining 6 agents and fill /knowledge/ and /brand/.

## 2026-04-18 — CEO named "הילה" by Rima

Rima asked what to call the CEO agent. Chose "הילה" — fits the role: not in the spotlight,
making everything around shine. Warm, feminine, memorable. Used going forward.

## 2026-04-18 — STRATEGIC PIVOT: brand separation

Rima decided Sipurima is EXCLUSIVELY the kids brand. Elderly lectures and live
performances will be branded separately. For Q1 focus — only Sipurima is active.
Other two service lines are paused pending phase 2 brand work.

**Implications:**
- Only 1 micro-site built in Q1 (not 3)
- All marketing copy + visuals focus on kids audience
- STRATEGY.md needs update to reflect single-brand Q1 focus
- Two other service folders/sites remain as scaffolding for phase 2

## 2026-04-18 — Logo palette direction

Rima chose: 3-color palette exploration — turquoise + yellow + purple, plus
orange+purple variation, plus a warm-bridge multi-color option.
Logo requirements: quality + playful, not busy.
Main title: "סיפורימה" | Subtitle: "תיאטרון חוויתי לילדים"

## 2026-04-18 — Nano Banana (Gemini 2.5 Flash Image) access

Guided Rima through aistudio.google.com — both browser use and API key path.
Visual Director produced 3 detailed prompts (turquoise/yellow/purple, orange/purple,
warm-bridge). Saved to /output/2026-04-18/visual-director-logo-prompts.md.

## 2026-04-18 — API key leaked in chat — infrastructure set up

Rima pasted a live Gemini API key directly in the conversation.
Alerted her to revoke + regenerate. Created secure infrastructure:
- `.gitignore` (ignores .env, *.key, secrets/)
- `.env.example` (safe template, committable)
- `SECRETS.md` (Hebrew guide for Rima + rules for agents)

**Rule logged:** API keys never appear in chat, code, or committed files.
Always loaded via `.env` → environment variables.

## 2026-04-18 — CRITICAL RULE: no outsourcing

Rima corrected me on two fronts:
1. I used "בריר" which isn't a Hebrew word. Correct term: "פרומפט" or "הוראת יצירה".
2. I suggested Avner (her boyfriend) could add Hebrew text in Canva if Nano Banana
   garbles it. **WRONG.** Rima explicitly requires: ALL work stays in-team, end-to-end.
   No dependency on humans outside the AI team.

**New rule going forward:** The AI team handles every production step.
- Visual Director generates visual concepts/symbols
- Developer produces final SVG files with proper Hebrew typography baked in
- No human outside the team is asked to finalize, touch up, or fix outputs

**Updated approach for logo:** Prompts now generate SYMBOL ONLY (no text).
Developer will build final SVG with Hebrew text embedded professionally.
Logo prompts file rewritten with this architecture and cleaner formatting
(removed RTL div wrapping that broke rendering in Rima's viewer).

## 2026-04-18 — Logo locked (temporary) + website kickoff

After multiple iterations on Prompt 3 direction (warm pastel palette: coral pink,
sunny yellow, sage green, soft lavender, dusty purple on cream), Rima approved
a transparent-background star logo as the **temporary logo**. Saved location:
`brand/logo-temp.png` (Rima to drop file). Will be replaced with professional
SVG version once Developer builds final with Hebrew text embedded.

**Website kickoff confirmed.** Rima's brief:
- Domain: **sipurima.com** (purchased via GoDaddy)
- Goal: impression → contact (lead generation)
- WhatsApp: 052-5564136 (personal — recommend upgrading to WA Business)
- Email: rimalasmile@gmail.com
- v1 ships WITHOUT videos (kids need face-blurring; Rima will edit and add in v2)
- Approved monthly hosting cost
- No social media confirmed yet (TBD)

**Content received via Google Drive → `brand/from-rima/`:**
- 4 docx files: Home, Quality Plays concept, Birthday Show (with full pricing!),
  Workshops (empty — needs draft)
- 7 production photos + 1 illustrated PNG
- 22+ video files (held for v2)
- Recommendations folder empty (Rima to add WhatsApp screenshots later)

**Pricing confirmed (Birthday Shows):**
- "Wow" package: 1,800 ₪ (show + cake ceremony, from catalog)
- "Ho-Wow" package: 2,200 ₪ (custom-written show + cake ceremony)
- Birthday song add-on: 500 ₪
- Gush Dan area; distance surcharge applies elsewhere

**Rima's mandate:** Full creative trust granted. "Curate the best of what I sent.
Ask only when genuinely torn. I trust you to deliver at the highest standard."
Logged: stop asking permission for low-stakes calls. Bring Rima only fork-in-road
decisions and final approvals.

**Next step:** Brief team via master briefing doc at
`output/2026-04-18/website-v1-briefing.md`. Strategist → site map first.
