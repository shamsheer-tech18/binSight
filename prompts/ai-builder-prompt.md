# Build prompt — BinSight web prototype

Use this as the input for an AI app builder (Vercel v0, Bolt, Lovable) or an AI coding assistant in VS Code. It reflects the current prototype in `/prototype`. Paste the whole block. For tools with a short input box, paste section 1–3 first, then send each page from section 5 as a follow-up message.

---

## 1. What to build

A clickable, desktop-first web prototype (1280 px wide) for **BinSight**, a weekly view for a university recycling lead. It shows which outdoor bins get contaminated, recommends one fix, records the change and proves whether it worked. Sample data only — no backend, no login, no real AI.

- Stack: React + TypeScript + Tailwind, one page per route, all data in one `data.ts` file.
- Font: Inter. Calm, light UI: white cards, light grey page background, green accent (#1f7a4d), thin grey borders, 10–12 px radius.
- Main navigation (top bar): **Overview · Change log · Summary**. Logo "BinSight" on the left.

## 2. Product rules (must hold on every page)

- Two kinds of numbers, always labelled:
  - **Sensor** = item count from the camera. Dashed border. A hint about where to look, never the official result.
  - **Audit** = weighed by hand. Solid border. The official result.
- Never mix sensor and audit numbers in one figure.
- Missing data shows **"No data"**, never 0%.
- Weeks run Sunday–Saturday. The weekly view updates every Monday.
- Hand audits are monthly on the 1st: Sep 1 (baseline), Oct 1, Nov 1. Next audit: **Tue Dec 1**.
- Today is **Mon Nov 23, 2026**. Latest week: **Sun Nov 15 – Sat Nov 21**.
- Reports are monthly for now: generated on the 1st and sent to the University Waste Management Office team. No weekly report.
- Station names start with a capital letter. One recommended fix at a time, always with evidence, a runner-up and a named owner.

## 3. Sample data

| Station | Role | Status | Story |
| --- | --- | --- | --- |
| A · Curry Student Center | Pilot (Big Belly) | Needs decision | Top problem items: coffee cups with liquid, food-soiled paper. Recommended fix: pair a trash bin next to recycling (owner: Grounds) |
| B · Snell Library | Pilot | Data quality low | Sign added Sep 16. Over 15% of readings uncertain (glare). Result: no real change, −2% vs comparison −4% |
| C · Centennial Walkway | Pilot | Result ready | Trash bin paired Sep 15. Audits 48% → 33% → 31%; comparison D 45% → 44% → 43%. −35% vs own baseline. Verdict: improved |
| D · ISEC Walkway | Comparison (unchanged) | Offline | Offline since Wed Nov 18. 7 days stored on the module; audits still count |

## 4. Shared components

- `StatusPill` (Needs decision · Result ready · Data quality low · Offline · On track) with an icon.
- `MetricCard` with `kind="sensor" | "audit"` (dashed vs solid border, small label "Sensor" / "Audit · Nov 1 · 42 kg").
- `StationBadge` (letter in a circle) + station name.
- `PriorityCard` (tinted background, small bin illustration, title, one line, CTA).
- `EvidenceList` (each line has a source: Sensor or Audit).

## 5. Pages

1. **Overview** (`/`) — Header "Overview" with a week picker (calendar dropdown, weeks Sun–Sat, latest = Nov 15–21). Legend chips: Sensor (dashed) · Audit (solid). Section **WEEKLY PRIORITIES**: two tinted cards — "Curry Student Center needs a decision" and "Centennial Walkway result is ready". Section **All Stations**: table with badge, station, this week's sensor %, latest audit % (date, kg), status pill, "See station" link. Note strip for Station B (data quality low). Footer: "Next audit: Tue Dec 1."
2. **Station detail** (`/station/a`) — Sensor accuracy check first. Wrong-bin % (sensor), contaminated % (audit), readings left out (uncertain, whole bags). Top problem items. Mistakes by hour (bar chart). CTA "See recommended fix".
3. **Recommendation** (`/station/a/fix`) — One fix, evidence with sources, confidence level, runner-up and 3rd option, owner (Grounds), how it will be checked. Buttons: Accept · I disagree, choose another option (asks why) · This can't be done (asks reason, then shows next option).
4. **Change log** (`/log`) — Form: station, type of change, date, owner, linked recommendation. Rules: a future date is refused with an error; logging a second change at a station already being measured shows a warning. After logging: follow-up audit dates and the change history table.
5. **Result — improved** (`/result/c`) — Station C vs comparison D at 3 audits (Sep 1, Oct 1, Nov 1) as a line or bar chart. Verdict "Improved", confidence. Guardrail: recyclables in trash did not increase. Events in the period. What BinSight learned (evidence, chosen fix, runner-up, verified). Buttons: Add to monthly report · Use this at Station A.
6. **Summary** (`/summary`) — Title "Monthly Report" with a month-year dropdown (Nov 2026, Oct 2026, Sep 2026). H1 "REPORT: 4 Stations", with a line under it: "Sent to: University Waste Management Office team · Monthly, on the 1st · Next report: Tue Dec 1". Box **REPORT SUMMARY** with 2 bullet points. Fixes proven / failed / pending; progress against targets; which data can be trusted; value vs cost (or "cost data missing" + Request cost data). Download PDF.

Edge-case pages (reachable from the Overview):

7. **Low confidence** (`/station/b`) — Sensor numbers hidden, no recommendation. Cause: glare. Last hand audit still shown. Buttons: Request a quick audit check · Ask BinSight team to fix the glare.
8. **Offline** (`/station/d`) — "No data, not 0%". Since Wed Nov 18; data stored on the module for 7 days; audits still work. Button: Ask Grounds to check the station.
9. **Result — no real change** (`/result/b`) — −2% vs −4%. Verdict "No real change". Suggests a different type of fix. Button: Add to next week's review.

Off the main navigation (installer and public):

10. **Install check** (`/install`) — 4-step tracker: mounted · camera sees only the bin (6 test images) · accuracy check · privacy approval. A test image that catches a hand is deleted and logged; the station must be re-tested.
11. **Hardware module** (`/hardware`) — Clip-in module, about 16 × 10 × 5 cm, 0.6 kg (estimates), downward camera with privacy shield.
12. **Station notice** (`/notice`) — The only thing at the bin: "This bin looks at what goes in. It never records you."

## 6. Done when

- Every page above is reachable by clicking; no dead links.
- Every number shows whether it is Sensor or Audit.
- No page shows 0% where data is missing.
- Dates match section 2 exactly.
