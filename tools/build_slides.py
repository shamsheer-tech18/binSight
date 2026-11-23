import pathlib
import json, html
S = [
 ("Critical path","Entry","1 · Overview","01_overview",
  ["Monday: the weekly view for Sun Nov 15 – Sat Nov 21 is ready.","Two cards show what needs Marcus: Station A needs a decision; Station C has a result.","All Stations table: sensor count (dashed) vs hand audit (solid), with a status for each station."],
  "Can Marcus see what needs him this week in seconds? · FR-3.1, FR-3.2, US-07"),
 ("Critical path","Entry · state","1b · Choosing a week","02_overview_picker",
  ["The date picker lists Latest week, Week before, This month and Pilot so far.","Weeks run Sunday to Saturday."],
  "Weekly rhythm: view updated every Monday."),
 ("Critical path","Action → System response","2 · Station A detail","03_station_a",
  ["Trust badge first: the sensor passed its accuracy check.","38% wrong bin (sensor) vs 46% contaminated (audit, Nov 1).","Uncertain readings and whole-bag dumps are left out of the count.","Top problem items and the 12–2 pm peak lead to one recommended fix."],
  "Does the evidence make the problem clear? · FR-1.3, FR-1.4, FR-2.3, US-19, US-20"),
 ("Critical path","Decision","3 · Recommendation","04_rec",
  ["One fix: put a trash bin next to the Big Belly.","Each reason shows its source; the same fix worked at Station C.","Runner-up and 3rd option, owner (Grounds), how it will be checked.","Three choices: accept, disagree, or mark it can't be done."],
  "Does Marcus understand and trust the fix? · FR-4.1, FR-4.2, FR-4.3, US-08"),
 ("Critical path","Decision · challenge","3b · I disagree","05_rec_disagree",
  ["Marcus picks another fix and says why (e.g. a fire lane).","His choice, the runner-up and the reason are saved so recommendations improve."],
  "User can challenge the AI  and feed the learning record."),
 ("Critical path","Decision · recovery","3c · This can't be done","06_rec_cant",
  ["Marcus chooses a reason (no budget, Grounds can't, don't trust the data).","BinSight offers the next best option, or he decides later."],
  "No dead end when a fix isn't possible. · EC-6"),
 ("Critical path","Input","4 · Log a change","07_log_form",
  ["Station, type of change, date and owner.","Station D is blocked: it is the comparison station.","Change history shows past fixes and their results."],
  "Every result can be tied to one dated change. · FR-5.1, US-10"),
 ("Critical path","Input · error","4b · Date in the future","08_log_error",
  ["A future date is refused with a plain message."],
  "Invalid input handled clearly."),
 ("Critical path","Input · warning","4c · Second change at Station C","09_log_warn",
  ["Station C is still being measured.","Logging a second change makes both results 'can't be attributed'."],
  "One change at a time keeps results fair. · FR-5.2"),
 ("Critical path","Processing","4d · Logged, now measuring","10_log_done",
  ["Waiting for audits: sensor trends are not the result.","Follow-up audits on Tue Dec 1 and Fri Jan 1; verdict after both."],
  "Sets expectations while the system waits. · PRD Q-10 open"),
 ("Critical path","Outcome","5 · Result: it worked","11_result_c",
  ["Station C fell 35% vs 4% at the unchanged Station D (audits Sep 1 → Oct 1 → Nov 1).","Guardrail: recyclables in trash did not rise (21% → 20%).","'What BinSight learned' saves evidence, chosen fix, runner-up and verdict."],
  "Can Marcus tell whether a fix worked, fairly? · FR-5.3, US-11, US-23 · North Star"),
 ("Critical path","Outcome for the Waste Management Office","6 · Summary (monthly report)","12_summary",
  ["Monthly Report for November 2026, generated on the 1st and sent to the University Waste Management Office team.","Report summary, progress against targets, which data can be trusted.","Recommendation: continue to the Dec 1 audit; not ready to buy yet."],
  "Evidence the Waste Management Office can act on. · FR-7.1, US-15, US-21"),
 ("Critical path","Missing information → recovery","6b · Cost data requested","13_summary_req",
  ["Value vs cost can't be estimated without Facilities and Finance data.","One click requests it; the range will appear when it arrives."],
  "Missing-information state with a next step."),
 ("Failure states","Low confidence","F1 · Data unreliable (Station B)","14_lowconf",
  ["23% of readings uncertain (limit 15%): sensor numbers hidden, no recommendation.","Cause shown (afternoon glare); the Nov 1 hand audit still counts."],
  "System withholds a guess rather than mislead. · EC-1, FR-1.3, US-19"),
 ("Failure states","Low confidence · recovery","F1b · Audit check requested","15_lowconf_req",
  ["A quick hand check is booked with the SGA hand-sort team."],
  "Clear recovery path."),
 ("Failure states","Missing data","F2 · Station offline (Station D)","16_offline",
  ["No readings for 5 days: shown as 'no data', never 0%.","Data stored 7 days on the module; audits still valid; trend paused."],
  "A gap never looks like a clean week. · EC-4, FR-1.5, FR-3.2"),
 ("Failure states","Fix didn't work","F3 · Sign didn't help (Station B)","17_result_b",
  ["Station B −2% vs comparison −4%: no real change.","Suggests a different type of fix: put recycling first on the path."],
  "Failure leads to the next step, not a dead end. · EC-5, US-23"),
 ("Hardware + software","Installer view (not tested with the lead)","7 · Station check: fault","18_install_fault",
  ["4 steps: mounted, camera sees only the bin, accuracy check, approvals.","A hand appeared during a bag change: image deleted, fault logged, re-test."],
  "Privacy as a gate before any data is used. · FR-1.1, FR-2.2, FR-6.3"),
 ("Hardware + software","Installer view","7b · Station check: passed","19_install_pass",
  ["6 of 6 test images clear; sent to the privacy office.","The station stays on hand audits until approved."],
  "Hardware/software interaction required for hybrid products."),
 ("Hardware + software","Virtual prototype","8 · Module concept","20_hardware",
  ["Clip-on module under the lid of an existing bin (~16 × 10 × 5 cm, estimates).","Camera sees only inside the bin; item records only leave the module.","Who interacts: nobody new at the bin; installer and Marcus via software."],
  "Form, scale, key parts and connections."),
 ("Hardware + software","At the bin","9 · Privacy notice","21_notice",
  ["'This bin looks at what goes in. It never records you.'","The only thing people at the bin see."],
  "Zero added effort for Maya. · FR-6.1, US-24"),
]
def esc(s): return html.escape(s)
slides=[]
slides.append('''<section class="slide cover"><div class="covertag">Prototype walkthrough</div><h1>BinSight</h1><h2>Prototype journey: from a contamination finding to a proven fix</h2><p class="q"><b>Prototype question:</b> We are building this prototype to determine whether a campus recycling lead can go from a station-level contamination finding to choosing one fix and judging whether it worked, when the data shows uncertainty and gaps.</p><p class="note">Wireframes v1 · all numbers are sample data · AI output simulated (Wizard-of-Oz) · Mon Nov 23, 2026</p></section>''')
flow=["Overview","Station detail","Recommendation","Log a change","Result","Summary"]
stages=["Entry","System response","Decision","Input → processing","Outcome","Outcome for the Waste Management Office"]
boxes=''.join(f'<div class="fbox"><div class="fn">{i+1}</div><div class="ft">{esc(t)}</div><div class="fs">{esc(s)}</div></div>'+('<div class="arr">→</div>' if i<5 else '') for i,(t,s) in enumerate(zip(flow,stages)))
slides.append(f'''<section class="slide"><div class="top"><span class="tag">Journey map</span></div><h1 class="st">The critical path Marcus follows, plus the states that can go wrong</h1><div class="flow">{boxes}</div>
<div class="rows"><div class="rowbox"><h3>Failure, uncertainty and recovery</h3><p>F1 Data unreliable (Station B) · F2 Station offline (Station D) · F3 Fix didn't work (Station B) · plus input errors, a second-change warning, and missing cost data</p></div>
<div class="rowbox"><h3>Hardware + software (installer view)</h3><p>7 Station check (field-of-view test, accuracy check, privacy approval) · 8 Module concept · 9 Privacy notice at the bin</p></div>
<div class="rowbox"><h3>Rules on every screen</h3><p>Dashed border = sensor count (a hint) · solid border = hand audit (official result) · missing data = "No data", never 0% · weeks run Sun–Sat, updated Mondays · hand audits on the 1st of each month</p></div></div></section>''')
for n,(sec,stage,title,img,pts,tests) in enumerate(S, start=3):
    li=''.join(f'<li>{esc(p)}</li>' for p in pts)
    slides.append(f'''<section class="slide"><div class="top"><span class="tag">{esc(sec)}</span><span class="num">{n}</span></div><div class="body"><div class="txt"><div class="stage">{esc(stage)}</div><h1 class="st">{esc(title)}</h1><h3>What the user sees</h3><ul>{li}</ul><h3>What it tests</h3><p class="tests">{esc(tests)}</p></div><div class="img"><img src="../docs/screens/{img}.png"></div></div></section>''')
css='''@page{size:1920px 1080px;margin:0}body{margin:0;font-family:Inter,system-ui,sans-serif;color:#1F1F1F}
.slide{width:1920px;height:1080px;box-sizing:border-box;padding:48px 64px;background:#FFFFFF;page-break-after:always;overflow:hidden;position:relative}
.cover{background:#F4F4F2;display:flex;flex-direction:column;justify-content:center;padding:0 160px}
.covertag{font-size:26px;color:#555}.cover h1{font-size:120px;margin:12px 0 0}.cover h2{font-size:44px;font-weight:500;margin:8px 0 48px;color:#1F4FB8}
.q{font-size:30px;line-height:1.45;max-width:1500px;background:#fff;border:2px solid #1F1F1F;border-radius:12px;padding:28px 36px;margin:0}.note{font-size:22px;color:#555;margin-top:32px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}.tag{font-size:20px;font-weight:600;color:#1F4FB8;background:#E3EBFA;padding:6px 16px;border-radius:999px}.num{font-size:20px;color:#777}
.body{display:flex;gap:48px;height:920px}.txt{flex:0 0 520px}.stage{font-size:22px;color:#555;text-transform:uppercase;letter-spacing:.04em}
h1.st{font-size:44px;margin:8px 0 28px;line-height:1.15}.txt h3{font-size:22px;color:#555;margin:24px 0 10px;text-transform:uppercase;letter-spacing:.04em}
.txt ul{margin:0;padding-left:26px;font-size:25px;line-height:1.45}.txt li{margin-bottom:12px}.tests{font-size:23px;line-height:1.45;margin:0;padding:16px 20px;background:#F4F4F2;border-left:none;border-radius:8px}
.img{flex:1;display:flex;align-items:flex-start;justify-content:center;background:#F4F4F2;border-radius:12px;padding:20px;box-sizing:border-box}.img img{max-width:100%;max-height:880px;object-fit:contain;border:1px solid #D4D4CF;border-radius:6px;background:#fff}
.flow{display:flex;align-items:stretch;gap:12px;margin:24px 0 40px}.fbox{flex:1;border:2px solid #1F4FB8;border-radius:12px;padding:20px;background:#fff}.fn{font-size:22px;color:#1F4FB8;font-weight:700}.ft{font-size:28px;font-weight:700;margin:6px 0}.fs{font-size:20px;color:#555}.arr{align-self:center;font-size:40px;color:#1F4FB8}
.rows{display:flex;flex-direction:column;gap:20px}.rowbox{border:1px solid #D4D4CF;border-radius:12px;padding:20px 28px;background:#F4F4F2}.rowbox h3{margin:0 0 6px;font-size:26px}.rowbox p{margin:0;font-size:23px;line-height:1.45}'''
open(str(pathlib.Path(__file__).resolve().parent/'slides.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(slides)}</body></html>')
print(len(slides))
