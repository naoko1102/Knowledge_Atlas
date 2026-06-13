# Verification Checklist

Current MVP verification status for VR Experiment Studio.

Status key:

- **Pass**: Confirmed by repository inspection or previously documented working flow.
- **Partial**: Implemented or documented, but needs live browser/runtime verification.
- **Fail**: Known not working.

## 1. Living Room Verification

| Item | Status | Notes |
|---|---|---|
| Room selection | Pass | `index.html` exposes a Living Room room card and initializes the Living Room parameter set. |
| All currently exposed parameters | Pass | The UI exposes 13 Living Room parameters and the editor/preview workflow is part of the current working MVP. |
| Embedded preview | Pass | Living Room preview routes to `aframe/viewer.html` in the embedded iframe and uses the reliable procedural A-Frame runtime path. |
| Pop-out viewer | Pass | `Pop Out Viewer` opens the same A-Frame viewer URL with encoded room parameters. |

### Living Room Parameters Currently Exposed

| Parameter | Status | Notes |
|---|---|---|
| Daylight Intensity | Partial | Live-routed; should update lighting through `postMessage`. |
| Wall Warmth | Partial | Live-routed; should update wall/sky color through `postMessage`. |
| Furniture Density | Partial | Cached-routed; should reload preview and alter furniture density. |
| Wall Decoration | Partial | Cached-routed; should reload preview and alter wall art levels. |
| Television Present | Partial | Cached-routed; should reload preview and show/hide TV. |
| Ceiling Height | Partial | Regeneration-routed; UI records value and shows note. Viewer shell can reflect value on reload, but this should not be overclaimed as real Infinigen regeneration. |
| Artificial Light | Partial | Live-routed; should update artificial fill light. |
| Light Color Temp. | Partial | Live-routed; should update light color. |
| Window Treatment | Partial | Cached-routed; should reload preview and alter window covering. |
| Exterior View | Partial | Cached-routed; should reload preview and alter sky/ground view colors. |
| Floor Material | Partial | Cached-routed; should reload preview and alter floor color/material proxy. |
| Plant Count | Partial | Cached-routed; should reload preview and alter plant count. |
| Clutter Level | Partial | Cached-routed; should reload preview and alter clutter bands. |

## 2. Bedroom Verification

| Item | Status | Notes |
|---|---|---|
| Room selection | Pass | `index.html` exposes a Bedroom room card and initializes the Bedroom parameter set. |
| GLB loading | Pass | `aframe/viewer.html` loads `/renders/bedroom_parametric.glb`; the active local server returned HTTP 200 with `Content-Length: 93136`. Viewer path, centering, and camera framing were fixed after the 404/path issue. |
| Fallback behavior | Pass | Viewer keeps explicit load-error, timeout, and invalid-bounds fallback paths to procedural Bedroom. |

### Bedroom Parameters Currently Exposed

| Parameter | Status | Notes |
|---|---|---|
| Daylight Intensity | Partial | Live-routed; should update lighting through `postMessage`. |
| Wall Warmth | Partial | Live-routed; should update wall/sky color through `postMessage`. |
| Desk Present | Pass | Cached-routed; records whether work furniture is present in the Bedroom condition. |
| Bed Scale | Partial | Cached-routed; should reload preview and affect procedural fallback bed scale. |
| Pillow Count | Partial | Cached-routed; should reload preview and affect procedural fallback pillow count. |
| Ceiling Height | Partial | Regeneration-routed; UI records value and shows note. Viewer shell can reflect value on reload in procedural fallback, but this is not real Infinigen regeneration. |
| Artificial Light | Partial | Live-routed; should update artificial fill light. |
| Light Color Temp. | Partial | Live-routed; should update light color. |
| Window Treatment | Partial | Cached-routed; affects lighting attenuation and should reload preview. |
| Exterior View | Partial | Cached-routed; affects sky/view color treatment. |
| Floor Material | Partial | Cached-routed; should reload preview and alter floor color/material proxy. |
| Night Light Present | Pass | Cached-routed; records light-at-night exposure as a Bedroom-specific sleep-environment variable. |
| Nightstand Count | Pass | Cached-routed; records bedside functional affordance/occupancy signal. |
| Clutter Level | Partial | Cached-routed; should reload preview and alter clutter bands. |

## 3. Experiment Workflow Verification

| Item | Status | Notes |
|---|---|---|
| Save as Control | Pass | Implemented in `saveAsControl()` and documented as part of the tested E2E flow. |
| Duplicate as Treatment | Pass | Implemented in `duplicateAsTreatment()` and documented as part of the tested E2E flow. |
| Diff Viewer | Pass | Implemented in `renderDiff()` with parameter-by-parameter comparison. |
| Confound Warning | Pass | `renderDiff()` shows a warning when more than one parameter differs between Control and Treatment. |

## 4. Persistence Verification

| Item | Status | Notes |
|---|---|---|
| JSON export | Pass | Implemented in `downloadExperiment()` and documented as part of the tested E2E flow. |
| JSON import | Pass | Implemented in `uploadExperiment()` and documented as part of the tested E2E flow. |
| localStorage restore | Pass | Implemented with `vr_studio_experiment` storage key and `DOMContentLoaded` restore. Documented as part of the tested E2E flow. |

## 5. Asset Verification

| Item | Status | Notes |
|---|---|---|
| Living Room procedural fallback | Pass | Current active path. `renders/asset_manifest.json` documents Living Room GLB as unavailable; `aframe/viewer.html` builds a procedural Living Room scene. |
| Living Room shell GLB status | Partial | `renders/living_room_shell.glb` exists locally as an ignored shell-only export. It is useful pipeline evidence but is not the reliable runtime path. |
| Bedroom GLB status | Pass | `renders/bedroom_parametric.glb` exists locally, is browser-sized, and is the current GLB-first Bedroom runtime asset. It is still not research-grade; procedural fallback remains available. |
| Bedroom high-fidelity/intermediate assets | Partial | `renders/bedroom_shell.glb` and `renders/bedroom_default.gltf` exist locally at about 401 MB each. They should remain local/external until optimized. |
| Infinigen regeneration pipeline | Pass | Living Room regeneration succeeded locally; the resulting `scene.blend` is about 1.0 GB and supports future export/validation work. |
| Blender direct-transform feasibility | Partial | Inspection found mostly static mesh outputs. Direct ceiling transforms do not propagate to walls/windows/doors, so future geometry edits need RoomSpec regeneration or a dedicated geometry-control layer. |

## Current Verification Gap

This checklist records the current MVP checkpoint. A live browser pass is still recommended before demo signoff:

1. Serve the repo with `python3 -m http.server 8000`.
2. Open `http://localhost:8000`.
3. Test Living Room parameter updates, embedded preview, and pop-out viewer.
4. Test Bedroom GLB load/fallback behavior.
5. Run Control/Treatment/Diff/Confound flow.
6. Test JSON export/import and reload-based localStorage restore.
