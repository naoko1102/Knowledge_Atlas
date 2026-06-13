# VR Experiment Studio

**COGS 160 · Track 3 · Environmental Psychology in Virtual Interiors**

---

## Overview

VR Experiment Studio is a browser-based authoring tool that lets students design and compare environmental psychology experiments in virtual rooms. Students select a room, adjust environmental parameters, save a Control condition, create a Treatment condition, review the difference, and launch a WebXR walkthrough — all without writing code or running any generation pipeline.

This is a prototype built for the COGS 160 Track 3 project. The goal is a system where undergraduate researchers can produce reproducible virtual stimuli for perceptual and behavioral studies.

---

## Current MVP Features

| Feature | Status |
|---|---|
| Living Room and Bedroom selection | ✅ |
| Current parameter editor | ✅ Living Room: 13 parameters; Bedroom: 14 parameters |
| Integrated A-Frame preview inside the editor | ✅ |
| Live parameter editing (lights, warmth update instantly) | ✅ |
| Cached parameter editing (furniture/layout reloads preview) | ✅ |
| Control condition creation | ✅ |
| Treatment condition creation via duplication | ✅ |
| Diff Viewer (parameter-by-parameter comparison) | ✅ |
| Confound warning when more than one parameter differs | ✅ |
| Download experiment as JSON | ✅ |
| Upload experiment from JSON | ✅ |
| LocalStorage autosave and restore on page reload | ✅ |
| Pop Out Viewer (opens full A-Frame tab for a condition) | ✅ |
| Collapsible Room Info HUD in viewer | ✅ |
| Bedroom GLB loading and fallback | ✅ |

---

## Architecture

```
User Interface (index.html)
  └─ Experiment State (localStorage / JSON)
  └─ Parameter Editor → postMessage → A-Frame iframe (aframe/viewer.html)
                                    → iframe reload (cached params)
                                    → new tab (Pop Out / condition launch)
```

**A-Frame** (`aframe/viewer.html`) is the runtime preview layer. It renders procedural geometry using A-Frame primitives, or loads a pre-exported GLB when one is available. It accepts parameters via URL query string (base64-encoded JSON) and via `postMessage` for live updates.

**Infinigen** is an authoring-side asset generation tool — it does not run in the browser. The pipeline is: Infinigen → Blender GLB export → `renders/` → served as a static asset. When no GLB is available for a room, the viewer falls back to a procedural A-Frame scene built from box and plane primitives.

**No backend, no build step.** The entire application is static HTML/CSS/JS served by Python's built-in HTTP server.

## Current Parameter Model

The current MVP uses a curated RoomSpec v2 subset that is hardcoded in `index.html`.

| Room | Current UI Parameters | Notes |
|---|---:|---|
| Living Room | 13 | Tier A original controls plus Tier B lighting, window, material, plant, and clutter controls |
| Bedroom | 14 | Bedroom-specific controls covering sleep-environment, lighting, window, material, bed, desk, night light, nightstand, and clutter variables |

The richer RoomSpec v2 source manifests live in `manifests/living_room.roomspec.v2.json` and `manifests/bedroom.roomspec.v2.json`. The older flat manifests (`*.manifest.json`) and files in `params/*.json` are legacy v1 six-parameter presets retained for provenance and pipeline experiments; they are not the authoritative source for the current UI.

---

## Folder Structure

```
track3_vr_studio/
├── index.html                  Main editor UI (room picker, params, experiment builder, diff)
├── aframe/
│   └── viewer.html             A-Frame WebXR viewer (standalone and embedded iframe)
├── renders/
│   ├── asset_manifest.json     Documents Infinigen generation status per room
│   ├── bedroom_parametric.glb  Lightweight Infinigen-exported GLB for Bedroom (91 KB; force-add if committing runtime asset)
│   ├── living_room_shell.glb   Lightweight shell-only Living Room export (local/ignored unless intentionally force-added)
│   └── _infinigen_bedroom_default/   Raw Infinigen output (scene.blend, pipeline CSVs)
├── manifests/                  v1 manifests plus richer RoomSpec v2 authoring manifests
├── params/                     Legacy v1 six-parameter presets, not current UI source
├── experiments/
│   └── experiments.json        Placeholder experiment store
├── infinigen_wrapper.py        CLI wrapper for Infinigen generation (authoring side)
├── PROJECT_MEMORY.md           Project context and design decisions
└── CLAUDE.md                   Claude Code instructions for this repository
```

---

## How To Run

Clone the repository, then serve it over HTTP from the repo root:

```bash
python3 -m http.server 8000
```

Open in a browser:

```
http://localhost:8000
```

> **Do not open `index.html` directly as a `file://` URL.** The A-Frame iframe and `postMessage` communication require an HTTP origin.

No Node.js, no npm, no build step required.

---

## Demo Workflow

The following sequence exercises every current feature:

1. **Select Room** — click Living Room or Bedroom; A-Frame preview loads immediately in the right panel
2. **Edit Parameters** — move sliders; live params (daylight, warmth) update the preview in real time; cached params (furniture, bed scale) reload the preview after a short debounce; regeneration params (ceiling height) show an inline note
3. **Save Control** — click "Save as Control"; the Control condition card appears
4. **Duplicate Treatment** — click "Duplicate as Treatment"; Treatment card appears with identical params
5. **Modify Treatment** — adjust one parameter; the right panel preview updates
6. **Review Diff** — the Diff table below shows which parameters changed; a confound warning fires if more than one differs
7. **Open Viewer** — click "Pop Out ↗" on a condition card to open a full-tab A-Frame walkthrough with WASD navigation; or click "Pop Out Viewer ↗" in the right panel header for the current live state
8. **Save Experiment** — click "↓ Download JSON" to save the experiment file; "↑ Upload JSON" to restore it; the experiment also autosaves to localStorage and restores automatically on page reload

---

## Asset Status

| Room | Asset | Source | Notes |
|---|---|---|---|
| Bedroom | `renders/bedroom_parametric.glb` (91 KB) | Infinigen + Blender headless export | Current GLB-first Bedroom runtime asset; not research-grade, and the viewer may fall back procedurally if loading or bounds validation fails |
| Living Room | Procedural A-Frame fallback | Built from primitives at runtime | Current reliable runtime path |
| Living Room shell | `renders/living_room_shell.glb` (84 KB, local ignored asset) | Infinigen regeneration + Blender export | Shell-only export; useful pipeline evidence, not wired as the default runtime scene |
| Bedroom high-fidelity/intermediate exports | `renders/bedroom_shell.glb` / `renders/bedroom_default.gltf` (about 401 MB each) | Infinigen + Blender export | Too large for normal browser/GitHub use; keep local or external until optimized |

The Living Room fallback is intentional. It is a workable proxy for development and demos but is not a substitute for a validated generated asset.

The Bedroom GLB is small enough to serve statically (91 KB). The viewer now loads it through `/renders/bedroom_parametric.glb`, preserves the authored asset transform, centers it through a preview wrapper, logs bounds/camera diagnostics, and keeps the procedural Bedroom fallback for genuine load or bounds failures. It is useful evidence that the asset pipeline can export browser-sized GLB files, but it is not a research-grade environment.

Living Room Infinigen regeneration has been verified locally. The regenerated source scene is large (about 1.0 GB for `scene.blend`, with a larger output directory) and should remain local/external unless a deliberate asset-storage plan is chosen. Blender inspection found mostly static mesh exports; direct ceiling transforms do not automatically propagate to walls, windows, and doors. Future geometry variation should therefore flow through RoomSpec-driven regeneration or a dedicated geometry-control layer rather than ad hoc direct mesh transforms.

---

## Known Limitations

- **Curated parameter subset.** The current UI exposes 13 Living Room parameters and 14 Bedroom parameters from a broader RoomSpec v2 direction. This is enough for an MVP demo but not yet a complete research schema.
- **Not photorealistic.** The procedural fallback scenes use colored A-Frame primitives. The Bedroom GLB is a raw Infinigen output without material refinement.
- **No participant data collection.** There is no mechanism to record participant responses, timing, or gaze data.
- **No automated Infinigen regeneration from the browser.** Regeneration parameters (e.g. ceiling height) are recorded in the experiment state and shown in the diff, but changing them does not trigger a new Infinigen run. That step remains a manual authoring-side operation.
- **Static mesh limitations.** Current Blender/Infinigen exports are mostly static meshes. Directly transforming one shell component can break alignment with related walls, windows, doors, or openings.
- **Limited room coverage.** Only Living Room and Bedroom are implemented.
- **Desktop-only layout.** The two-panel UI assumes a wide screen (≥ 900 px). No mobile breakpoint.
- **Pointer lock in iframe requires a click.** The embedded A-Frame preview requires one click inside the panel before WASD mouse-look activates. This is a browser security constraint; the Pop Out window does not have this restriction.

---

## Future Roadmap

The following items represent the intended evolution of this system beyond the current MVP:

1. **Research-grade RoomSpec schema** — a formal, versioned parameter schema that maps directly to Infinigen/Blender generation arguments and supports study pre-registration
2. **Expanded environmental parameters** — move beyond the current 13/14-parameter curated subset toward a fuller room specification with window count, material reflectance, plant species, color temperature, spatial layout, and other controlled variables
3. **RoomSpec-driven regeneration pipeline** — map RoomSpec v2 values to Infinigen/regeneration inputs, Blender cleanup/export steps, and A-Frame validation checks
4. **Better Living Room and Bedroom generation** — refine Blender export scripts, add material cleanup, tune scale/framing, and create browser-budgeted GLBs
5. **Blender MCP integration** — use the Blender Model Context Protocol server to automate GLB export and validation steps from within the authoring workflow
6. **Higher-fidelity asset workflow** — baked lighting, PBR materials, and optimised mesh LODs suitable for later perception-study validation
7. **Additional room types** — office, lab, outdoor courtyard, and other environments relevant to environmental psychology research
8. **Asset validation and export checks** — automated bounding-box, polygon count, and material sanity checks before a GLB is committed to `renders/`

---

## Development Notes

- Serve from repo root, not from a subdirectory, so root-relative viewer assets (`/renders/bedroom_parametric.glb`) and `aframe/viewer.html` resolve correctly.
- `.gitignore` intentionally ignores `.blend`, `.gltf`, `.glb`, and `renders/`. Small runtime assets such as `renders/bedroom_parametric.glb` must be intentionally force-added if the GitHub checkpoint needs them.
- All application state lives in `index.html` as plain JS variables. There is no framework.
- `aframe/viewer.html` is deliberately standalone — it can be opened directly with URL parameters and does not depend on `index.html` being loaded.
- `postMessage` communication uses `window.location.origin` as the target origin; both pages must share the same HTTP origin.
- See `PROJECT_MEMORY.md` for the original project context and design rationale.
