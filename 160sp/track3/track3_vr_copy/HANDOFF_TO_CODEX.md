# HANDOFF_TO_CODEX.md

## Project

VR Experiment Studio
COGS 160 Track 3 — Environmental Psychology Experiment Authoring Platform

## Current Status

This project has moved from a basic Infinigen/Blender asset scaffold into a working MVP web application.

The MVP currently supports:

* Living Room / Bedroom selection
* Integrated A-Frame preview inside the main editor
* Parameter editing
* Live / Cached / Regeneration routing
* Control condition creation
* Treatment condition creation
* Diff Viewer
* Confound warning
* JSON download / upload
* localStorage restore
* Pop-out A-Frame viewer
* Collapsible Room Info HUD
* RoomSpec v2 Tier B parameter integration
* Bedroom-specific parameter controls
* Bedroom GLB loading and framing fix
* Improved Living Room procedural preview

## How To Run

From repo root:

```bash
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000
```

## Important Files

Read these first:

```text
README.md
PROJECT_MEMORY.md
DEMO_SCRIPT.md
renders/asset_manifest.json
index.html
aframe/viewer.html
manifests/
params/
```

## Current Architecture

```text
index.html
  -> Room Picker
  -> Parameter Editor
  -> Experiment Builder
  -> Diff Viewer
  -> Save / Load
  -> embedded iframe preview

aframe/viewer.html
  -> A-Frame runtime
  -> procedural Living Room fallback
  -> Bedroom GLB-first runtime / procedural fallback
  -> postMessage live updates
```

Infinigen is not run inside the browser.
Infinigen and Blender MCP are future authoring-side asset-generation tools.

## Current Parameter State

The current MVP started with 6 parameters per room.

It has now been expanded toward RoomSpec v2:

* Living Room: 13 parameters
* Bedroom: 14 parameters

Current supported parameter categories include:

* daylight
* wall warmth
* furniture density
* wall decoration
* TV presence
* ceiling height
* artificial light
* light color temperature
* window treatment
* exterior view
* floor material
* plant count
* clutter level

Bedroom controls are now Bedroom-specific. They include bed scale, pillow count, desk presence, night light, nightstand count, and other sleep-environment variables rather than Living Room-specific controls copied across rooms.

## Current Asset Status

### Living Room

Current status:

```text
Procedural A-Frame fallback
```

Current reliable runtime path remains the procedural A-Frame preview.

Local asset/pipeline status:

* Living Room Infinigen regeneration succeeded.
* Regenerated source scene exists at `renders/_infinigen_living_room_regen_test/scene.blend`.
* The regenerated `scene.blend` is about 1.0 GB and should remain local/external unless an asset-storage plan is chosen.
* `renders/living_room_shell.glb` exists locally as a small shell-only export.
* The shell GLB is not yet the default runtime scene and should not be treated as a complete validated Living Room asset.

The procedural preview has been improved with:

* windows
* window treatments
* exterior views
* wall art
* furniture density variations
* ceiling pendant
* clutter variety
* visible environmental changes

### Bedroom

Current status:

```text
bedroom_parametric.glb loads in the viewer
```

The Bedroom GLB path/framing issue has been fixed:

* Viewer uses `/renders/bedroom_parametric.glb`.
* The active local server returns HTTP 200 for that path.
* The viewer preserves the asset transform, centers it with a wrapper, frames the camera, and logs bounds diagnostics.
* Procedural fallback remains available for load, timeout, or invalid-bounds failures.

However, the Bedroom GLB is still not research-quality.

Known issues:

* not photorealistic
* not suitable for final parameter validation
* needs future Infinigen + Blender export cleanup
* larger Bedroom exports exist locally but are about 401 MB and too large for normal browser/GitHub use without optimization

## What Works

The following E2E workflow has been tested:

```text
Select Living Room
-> edit parameters
-> save as Control
-> duplicate as Treatment
-> modify Treatment
-> view Diff
-> see Confound Warning
-> Download JSON
-> Upload JSON
-> reload and restore state
```

Additional current working state:

```text
Select Bedroom
-> load bedroom_parametric.glb
-> edit Bedroom-specific controls
-> keep procedural fallback available if GLB validation fails
```

## Known Limitations

Do not overclaim the current implementation.

Current limitations:

* Not photorealistic
* Bedroom asset is not final
* Living Room is procedural fallback, not real Infinigen GLB
* Living Room shell GLB is shell-only and local/ignored
* Large Bedroom exports should remain local/external until optimized
* No participant data collection
* No behavioral data analysis
* No database/backend
* No live Infinigen regeneration in browser
* Current RoomSpec integration is partial
* Blender MCP is not integrated yet
* Direct Blender transforms are limited by static mesh exports; moving a ceiling does not automatically update walls/windows/doors/openings

## Immediate Next Tasks

### Task 1 — Verify Current State

Before writing new code:

1. Run the app locally.
2. Test Living Room parameters.
3. Test Control / Treatment / Diff.
4. Test JSON export/import.
5. Confirm no regression from latest Living Room preview changes.

### Task 2 — Commit Current Stable State

If tests pass:

```bash
git status
git add README.md DEMO_SCRIPT.md VERIFICATION_CHECKLIST.md PIPELINE_PLAN.md LIVING_ROOM_ASSET_REPORT.md BEDROOM_ASSET_REPORT.md LIVING_ROOM_STRUCTURE_NOTES.md HANDOFF_TO_CODEX.md aframe/viewer.html renders/asset_manifest.json
git add -f renders/bedroom_parametric.glb renders/bedroom_parametric.glb.meta.json
git commit -m "docs: checkpoint MVP asset pipeline status"
git push
```

Do not force-add `.blend`, `.gltf`, `bedroom_shell.glb`, or large regeneration directories.

### Task 3 — Start Asset Pipeline Planning

Create a plan for:

```text
RoomSpec v2
-> Infinigen/regeneration
-> Blender cleanup/export
-> A-Frame validation
```

Focus first on:

* Living Room
* Bedroom

### Task 4 — Living Room GLB Validation

Living Room source regeneration has succeeded. Next task is validation, not discovery.

Goal:

```text
Validate or rebuild a complete browser-budgeted Living Room GLB before replacing the procedural fallback.
```

### Task 5 — Bedroom Rebuild

Investigate why `bedroom_parametric.glb` is tiny and low quality.

Goal:

```text
Create a higher-quality browser-budgeted Bedroom GLB from Infinigen/Blender without using the 401 MB assets as the default runtime path.
```

### Task 6 — Blender MCP Feasibility

Do not start with full automation.

First document:

* what Blender file to open
* what objects exist
* what parameters can be edited
* what can be safely exported
* what should remain fallback for now
* where RoomSpec/regeneration is safer than direct static mesh transforms

## Future Roadmap

1. Refine RoomSpec v2 into a research-grade schema.
2. Expand parameters from 13/14 toward 38/39.
3. Map RoomSpec parameters to Infinigen controls.
4. Use Blender MCP for cleanup and controlled edits.
5. Export validated browser-budgeted GLB assets.
6. Add GLB runtime paths only after validation, while preserving procedural fallbacks.
7. Add asset validation reports.
8. Scale beyond Living Room and Bedroom.
9. Preserve experiment-authoring workflow.
10. Avoid adding participant-data collection until ethics/IRB planning exists.

## Rules For Codex

Before coding:

1. Read README.md, PROJECT_MEMORY.md, DEMO_SCRIPT.md, and this file.
2. Inspect index.html and aframe/viewer.html.
3. Summarize current state.
4. Ask before making large architectural changes.

Do not:

* run Infinigen from the browser
* add a backend unless explicitly requested
* claim photorealism
* delete fallback scenes
* remove Control/Treatment/Diff workflow
* modify many files at once without explanation

Prefer:

* small commits
* testable changes
* honest fallback behavior
* clear documentation
* preserving the working MVP
