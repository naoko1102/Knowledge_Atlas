# Demo Script — VR Experiment Studio
**COGS 160 · Track 3 · Environmental Psychology in Virtual Interiors**
Estimated time: 3–5 minutes

---

## Before You Start

- Server running: `python3 -m http.server 8000`
- Browser open to: `http://localhost:8000`
- Browser zoom at 100%, window wide enough to show both panels
- Clear localStorage if you want a clean slate: DevTools → Application → Local Storage → Clear

---

## 1 — Select Living Room *(~20 s)*

> **Click the Living Room card.**

**Say:**
"This is the experiment authoring interface. On the left, you have the editor. On the right, a live A-Frame preview loads automatically the moment you select a room — no separate button to click."

**What to show:**
- The room card highlights in blue when selected
- The right panel transitions from the placeholder to the A-Frame viewer
- The orange procedural-preview banner appears at the top of the viewer — point to it briefly

**Say:**
"The banner tells us we're looking at the reliable procedural A-Frame path for the Living Room. A regenerated Living Room source scene and shell export exist locally, but the shell is not the default runtime asset yet. The interface is honest about that. The Bedroom now loads its lightweight generated GLB first and still keeps a procedural fallback if loading or bounds validation fails."

---

## 2 — Adjust Parameters *(~40 s)*

> **Move the Daylight Intensity slider.**

**Say:**
"Every parameter has a routing label. Daylight Intensity is marked Live — watch the preview."

**What to show:**
- Drag the slider slowly from left to right — the room visibly brightens in the iframe in real time, no reload
- Drag Wall Warmth — sky and wall colour shift from cool blue-grey to warm amber in real time

**Say:**
"Live parameters update through a postMessage channel to the embedded A-Frame viewer — no page reload, no round-trip to a server."

> **Move the Furniture Density slider.**

**Say:**
"Furniture Density is Cached — it requires rebuilding the procedural scene. Watch for the brief reload."

**What to show:**
- Drag to a high value — the iframe reloads after a short debounce; more furniture appears

**Say:**
"Cached and Regeneration parameters are honest labels. Cached means we switch between pre-generated variants. Regeneration — like Ceiling Height — means a new Infinigen run would be needed. We record the value in the experiment, we show the difference in the diff, but we don't pretend the preview updated when it didn't."

> **Point to the Ceiling Height param — do not move it yet.**

**Say:**
"We'll come back to that when we look at confound detection."

---

## 3 — Live Preview Updates *(already covered above — use this beat to let the room settle)*

> **Collapse the Room Info HUD in the preview panel by clicking the × button, or note it is already collapsed.**

**Say:**
"The HUD in the viewer is collapsible. In the embedded view it defaults to collapsed so it doesn't block your view of the room. Click the pill to bring it back — it shows the condition label, asset source, and current parameter values."

> **Click the Room Info pill to expand it briefly, then collapse again.**

---

## 4 — Save as Control *(~15 s)*

> **Set parameters to a baseline you like. Click "Save as Control".**

**Say:**
"I've set a calm, moderately lit room. I'll save this as the Control condition."

**What to show:**
- The Control card appears below the buttons
- The editing banner at the top of the left panel shows "Editing: Control"
- The right panel header updates to "Editing Control · Living Room"

**Say:**
"The Control card shows the current room's parameter values. This state is also autosaved to localStorage — if I reload the page right now, everything comes back."

---

## 5 — Duplicate as Treatment *(~15 s)*

> **Click "Duplicate as Treatment".**

**What to show:**
- Treatment card appears alongside Control
- Both cards show identical values
- The editing indicator switches to Treatment
- The diff section appears at the bottom — currently shows "No changes detected"

**Say:**
"Treatment starts as an exact copy of Control. The diff is live — it updates every time I move a slider."

---

## 6 — Change One Parameter *(~20 s)*

> **Move the Daylight Intensity slider noticeably — e.g. from 0.60 to 0.90.**

**What to show:**
- The preview brightens in real time
- The value display next to the slider turns blue (indicating it differs from default)
- The Treatment card's Daylight Intensity value updates immediately

**Say:**
"I've increased daylight intensity in the Treatment. This is now a valid single-variable manipulation — one independent variable, everything else held constant."

---

## 7 — Show Diff Viewer *(~25 s)*

> **Scroll down to the Diff table.**

**What to show:**
- One highlighted row — Daylight Intensity — with Control value on the left and Treatment value on the right
- "Changed" badge on that row
- The green notice: "1 parameter changed. No confounds detected."

**Say:**
"The diff table shows every parameter side by side. One row is highlighted. The system confirms: no confounds. This is the clean experimental design we want — one IV manipulated, everything else identical."

> **Point at the Control and Treatment cards.**

**Say:**
"A researcher can hand this diff to a supervisor or IRB and say: here is exactly what changed between conditions, and here is proof nothing else did."

---

## 8 — Show Confound Warning *(~20 s)*

> **Move a second slider — e.g. Wall Warmth from 0.50 to 0.80.**

**What to show:**
- A second row highlights in the diff table
- The notice immediately turns orange: "⚠️ Possible confound: 2 parameters differ from Control."

**Say:**
"The moment I change a second variable, the system flags a confound. This is immediate feedback for students who might not realise they've introduced a confounding variable. The diff is still fully visible — they can see exactly which parameters diverged and decide whether to revert one."

> **Revert Wall Warmth back to its Control value.**

**Say:**
"Reverting one brings us back to a clean single-variable design."

---

## 9 — Export JSON *(~20 s)*

> **Click "↓ Download JSON" in the top-right header.**

**What to show:**
- Browser downloads a file named something like `experiment_living_room_2026-06-10.json`

**Say:**
"The entire experiment state downloads as a JSON file — both conditions, all parameter values, the active editing context. This is the unit of scientific record for this tool. A student submits this file with their lab report."

> **Open the file in a text editor briefly if possible, or just describe it.**

**Say:**
"It's plain JSON — readable, versionable, and portable. A future system could feed it directly into an Infinigen regeneration pipeline or a study management platform."

---

## 10 — Import JSON *(~20 s)*

> **Click "↑ Upload JSON", select the file you just downloaded.**

**What to show:**
- The experiment state restores exactly
- A toast appears: "Experiment loaded from experiment_living_room_…json"
- The iframe reloads with the correct parameters
- Both condition cards appear with correct values
- The diff table is correct

**Say:**
"Upload restores the full state — room selection, both conditions, which condition was being edited, the diff. localStorage does this automatically on every page reload, but the JSON file is the durable, shareable artefact."

---

## 11 — Future Roadmap *(~45 s)*

> **No clicks needed. Talk to the screen.**

**Say:**
"What you've seen is the MVP — it works, the workflow is real, and the runtime is honest about which assets are procedural and which are generated. Let me describe where this goes."

**Pause on the viewer panel.**

**Say:**
"The architecture is already set up for generated assets. The Bedroom loads a 91 KB Infinigen-derived GLB and frames it in A-Frame, but it is still an MVP asset, not a research-grade stimulus. The Living Room still uses the procedural path at runtime. Local regeneration has succeeded and a shell-only GLB exists, but it needs validation before replacing the fallback."

**Say:**
"The next layer is the generation pipeline. We have broader RoomSpec v2 manifests, with parameters mapped to psychological constructs and citations. The current interface exposes a curated subset — 13 Living Room parameters and 14 Bedroom-specific parameters. When a student changes Ceiling Height, that value is stored. The system knows it requires regeneration. A future authoring step would call Infinigen from a RoomSpec, clean up and export the scene in Blender, validate the bounding box and polygon budget, and then test the GLB in A-Frame."

**Say:**
"We're also looking at Blender MCP — the Blender Model Context Protocol server — for inspection and export automation. The current investigation found that direct transforms on static meshes are risky: moving a ceiling does not automatically propagate to walls, windows, and doors. So geometry changes should probably come from RoomSpec-driven regeneration or a dedicated geometry-control layer, not one-off mesh edits."

**Say:**
"The student-facing interface doesn't change. They still see this same editor. They still get a clean diff and a JSON file. The quality of the preview improves as the asset pipeline matures — but the experimental workflow is already the right shape."

---

## Close

**Say:**
"The core claim of this prototype is: a student with no VR development experience can design a valid single-variable environmental psychology experiment, generate a reproducible diff, and export a documented experimental record — in under five minutes, in a browser, with no code."

> **Point at the diff table.**

**Say:**
"That's what this is for."

---

## Fallback Notes

| If… | Then… |
|---|---|
| iframe doesn't load | Reload the page; check that `python3 -m http.server 8000` is running |
| localStorage restores old state | DevTools → Application → Local Storage → Delete key `vr_studio_experiment` → reload |
| Confound warning doesn't clear | Revert the second slider to exactly match the Control value |
| Download doesn't trigger | Check browser pop-up blocker; allow downloads from localhost |
| Room Info pill click does nothing | Check that viewer is served over HTTP (not file://); hard-reload the iframe |
