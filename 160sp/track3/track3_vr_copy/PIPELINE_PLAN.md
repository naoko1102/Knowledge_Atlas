# Pipeline Plan

Roadmap for moving VR Experiment Studio from the current functional MVP toward validated, higher-fidelity room assets.

## Current Findings

- VR Studio MVP is functional.
- Living Room and Bedroom procedural previews work.
- The Control/Treatment workflow, Diff Viewer, JSON persistence, and embedded A-Frame preview are implemented.
- Bedroom controls are now Bedroom-specific, and the Bedroom viewer loads the lightweight MVP GLB: `renders/bedroom_parametric.glb`.
- Bedroom GLB loading has been fixed with a root-relative asset URL, wrapper-based centering, bounds diagnostics, and camera framing. Procedural fallback remains available.
- Bedroom also has a local source `.blend`: `renders/_infinigen_bedroom_default/scene.blend`.
- Bedroom high-fidelity/intermediate exports exist locally, but the 401 MB assets are too large for ordinary browser/GitHub use without optimization.
- Living Room Infinigen regeneration succeeded.
- Regenerated Living Room output exists at `renders/_infinigen_living_room_regen_test/scene.blend`.
- The regenerated Living Room `scene.blend` is approximately `1.1 GB`.
- A lightweight `renders/living_room_shell.glb` exists locally, but it is shell-only and is not the reliable runtime path.
- Living Room pipeline evidence shows walls, floors, ceilings, windows, and doors were generated.
- Architectural shell elements exist: walls, floor, ceiling, windows, doors.
- Blender object transforms are editable.
- Blender direct-transform investigation found that current Infinigen exports are mostly static meshes. Directly moving a ceiling does not automatically propagate to walls, windows, doors, or openings.
- Future parametric geometry should likely use RoomSpec-driven regeneration or a dedicated geometry-control layer, followed by Blender cleanup/export and A-Frame validation.

Important caution:

- Procedural previews and raw Infinigen output are not yet research-grade or photorealistic stimuli.
- The current app should continue to preserve fallback behavior until exported GLBs pass validation.

## Phase 1: Current MVP

| Field | Details |
|---|---|
| Goal | Preserve the working browser-based experiment authoring MVP. |
| Inputs | `index.html`, `aframe/viewer.html`, current RoomSpec-inspired parameter subset, procedural A-Frame scenes, `bedroom_parametric.glb`, JSON/localStorage persistence. |
| Outputs | Students can select Living Room or Bedroom, edit parameters, save Control, duplicate Treatment, inspect diffs, receive confound warnings, and export/import JSON. |
| Risks | Regressing the working Control/Treatment/Diff flow; overclaiming asset realism; confusing legacy v1 params with the current UI subset. |
| Success criteria | MVP workflow remains stable; no app-code changes break preview, persistence, or diff behavior; documentation honestly states fallback and asset limitations. |

## Phase 2: Asset Recovery

| Field | Details |
|---|---|
| Goal | Inventory, recover, and validate available source assets before changing runtime behavior. |
| Inputs | `renders/_infinigen_living_room_regen_test/scene.blend`, `renders/_infinigen_bedroom_default/scene.blend`, existing Bedroom GLB/GLTF outputs, asset reports, pipeline metadata, polycount reports. |
| Outputs | Clear list of usable source `.blend` files, rejected/oversized intermediate files, candidate GLB exports, and per-room asset status. |
| Risks | Large files exceed browser/runtime budgets; regenerated source scenes contain unrelated rooms or terrain; exports may be poorly scaled, too heavy, or visually unsuitable; ignored render assets may not be reproducible from Git alone. |
| Success criteria | Each room has a documented source asset path, size, usability decision, blocker list, and next export action. No runtime switch occurs until a GLB passes validation. |

## Phase 3: Blender MCP Integration

| Field | Details |
|---|---|
| Goal | Use Blender MCP to inspect generated room assets, automate safe selection/export, and evaluate bounded edits without assuming direct transforms can preserve room topology. |
| Inputs | Valid `.blend` files, Blender object/collection inventory, identified room shell objects, RoomSpec variables that map to geometry or transforms. |
| Outputs | Documented MCP workflow for opening scenes, locating room objects, editing transforms, validating object bounds, and exporting candidate GLBs. |
| Risks | Wrong object selection; transforms break alignment between walls/windows/doors; direct edits affect static meshes without updating related openings; exported files look correct in Blender but fail in A-Frame. |
| Success criteria | MCP can reliably identify target room shell components, create validated export collections, and document which direct edits are unsafe. Any geometry-changing workflow either proves linked updates are preserved or routes back through RoomSpec/Infinigen regeneration. |

## Phase 4: RoomSpec v2 Expansion

| Field | Details |
|---|---|
| Goal | Expand from the current curated UI subset toward a fuller RoomSpec v2-driven authoring and regeneration model. |
| Inputs | `manifests/living_room.roomspec.v2.json`, `manifests/bedroom.roomspec.v2.json`, current hardcoded UI params, routing vocabulary (`live`, `cached`, `regeneration`), MCP edit findings. |
| Outputs | Parameter mapping table from RoomSpec v2 to runtime behavior: live preview update, cached asset variant, Blender inspection/export action, dedicated geometry-control action, or Infinigen regeneration. |
| Risks | Too many controls for beginner users; parameters without visible effects; UI/schema drift; claiming geometry changes that are only preview approximations. |
| Success criteria | A versioned mapping exists for each exposed parameter, including psychological construct, routing type, implementation status, and validation requirements. The student-facing UI remains beginner-friendly. |

## Phase 5: Photorealistic Pipeline

| Field | Details |
|---|---|
| Goal | Produce validated higher-fidelity assets suitable for future research-stimulus evaluation, without claiming current MVP assets are research-grade. |
| Inputs | Stable RoomSpec mappings, Infinigen venv, Blender/MCP export workflow, validated source `.blend` files, material/lighting cleanup requirements, browser performance budgets. |
| Outputs | Browser-budgeted GLBs for Living Room and Bedroom, asset validation reports, screenshots, performance notes, and fallback-safe runtime integration plan. |
| Risks | Photorealistic assets may exceed browser/WebXR budgets; material pipelines may not survive GLB export; visual realism may introduce uncontrolled confounds; research claims may require IRB/study validation beyond asset generation. |
| Success criteria | Assets load reliably in A-Frame, are correctly scaled, visually coherent, performant, documented, and explicitly validated before being presented as research-quality candidates. Procedural fallbacks remain available. |

## Immediate Recommended Next Steps

1. Open `renders/_infinigen_living_room_regen_test/scene.blend` in Blender or inspect it headlessly.
2. Identify Living Room shell objects, windows, doors, and object hierarchy.
3. Create a Bedroom/Living Room export validation checklist with exact pass/fail thresholds.
4. Treat `renders/living_room_shell.glb` as shell-only evidence; do not switch Living Room runtime to it until it passes visual and navigation validation.
5. Validate candidate GLBs in Blender first, then A-Frame.
6. Keep procedural fallbacks available even after candidate GLBs are introduced.

## Fallback Policy

The current procedural A-Frame scenes remain the safe runtime fallback.

Do not remove fallback scenes, claim photorealism, or claim research-grade stimuli until the asset pipeline produces validated GLBs with documented scale, performance, material, and visual-quality checks.
