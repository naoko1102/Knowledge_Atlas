# Bedroom Asset Report

Hour 4 investigation for the Bedroom asset state, with later checkpoint updates.

## Checkpoint Update: 2026-06-12

Bedroom GLB loading is fixed in `aframe/viewer.html`.

Current viewer behavior:

- Loads `/renders/bedroom_parametric.glb` as the primary Bedroom runtime asset.
- Uses a root-relative asset path from the repo-root HTTP server.
- Preserves the imported GLB's authored transform.
- Centers and normalizes the preview through a wrapper entity instead of hard-scaling the model.
- Logs model bounds, mesh count, camera state, and fallback details.
- Keeps procedural Bedroom fallback for genuine load, timeout, or invalid-bounds failures.

Measured lightweight GLB contents:

| Metric | Value |
|---|---:|
| Scenes | 1 |
| Nodes | 20 |
| Meshes | 19 |
| Primitives | 19 |
| Materials | 8 |
| Vertices | 2,140 |
| Animations | 0 |
| Raw bounds min | `[-0.5, 0, -18.5]` |
| Raw bounds max | `[6, 2.7, -11]` |
| Raw dimensions | `[6.5, 2.7, 7.5]` |
| Raw center | `[2.75, 1.35, -14.75]` |
| Bounding sphere radius | about `5.14` |

The active local HTTP server returned `HTTP 200` for `/renders/bedroom_parametric.glb` with `Content-Length: 93136`.

Scope inspected:

- `renders/bedroom_parametric.glb`
- `renders/bedroom_default.gltf`
- `renders/_infinigen_bedroom_default/`
- `manifests/bedroom.manifest.json`
- `manifests/bedroom.roomspec.v2.json`
- `params/bedroom_default.json`

Application code was not modified.

## Environment Note

The default repo Python is:

```text
/opt/anaconda3/bin/python3
Python 3.12.4
```

That interpreter cannot import Infinigen.

Infinigen is available through the separate virtual environment:

```text
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python
```

That interpreter can import both:

```text
infinigen
infinigen_examples
```

## Executive Summary

Bedroom has real local source and runtime assets:

- A real source Blender file exists at `renders/_infinigen_bedroom_default/scene.blend`.
- A large binary glTF exists at `renders/bedroom_default.gltf`.
- A small browser-targeted GLB exists at `renders/bedroom_parametric.glb`.

The small GLB is a real GLB and is browser-sized, and the viewer now loads and frames it correctly. It is still not research-grade. Metadata and Blender/GLB inspection show it is a simplified parametric extraction: a small set of retained room-shell meshes plus added `KA_PARAM` furniture, not a full high-fidelity Bedroom export from the raw Infinigen scene.

Recommended current policy: keep the viewer's GLB-first behavior with procedural fallback, but treat `bedroom_parametric.glb` as an MVP runtime asset, not a final stimulus. For higher quality, rebuild from the local source `.blend` or regenerate with the Infinigen venv, then export and validate a browser-budgeted GLB.

## Commands Run

```bash
ls -lh renders/bedroom_parametric.glb renders/bedroom_default.gltf renders/_infinigen_bedroom_default/scene.blend manifests/bedroom.manifest.json manifests/bedroom.roomspec.v2.json params/bedroom_default.json
file renders/bedroom_parametric.glb renders/bedroom_default.gltf renders/_infinigen_bedroom_default/scene.blend
xxd -l 64 renders/bedroom_parametric.glb
head -c 240 renders/bedroom_default.gltf
find renders/_infinigen_bedroom_default -maxdepth 3 -type f -print
sed -n '1,220p' renders/bedroom_parametric.glb.meta.json
sed -n '1,160p' renders/bedroom_default.gltf.meta.json
sed -n '1,90p' renders/_infinigen_bedroom_default/pipeline_coarse.csv
sed -n '1,140p' renders/_infinigen_bedroom_default/polycounts.txt
git status --short --ignored renders/bedroom_parametric.glb renders/bedroom_default.gltf renders/_infinigen_bedroom_default/
git check-ignore -v renders/bedroom_parametric.glb renders/bedroom_default.gltf renders/_infinigen_bedroom_default/scene.blend
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python -c "import sys; print(sys.executable); import infinigen, infinigen_examples; print(infinigen.__file__); print(infinigen_examples.__file__)"
```

Blender background inspections:

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python-expr "<import and inspect renders/bedroom_parametric.glb>"
/Applications/Blender.app/Contents/MacOS/Blender --background renders/_infinigen_bedroom_default/scene.blend --python-expr "<inspect scene objects and collections>"
```

## Files Found

### Main Bedroom Assets

| Path | Size | Type | Usability |
|---|---:|---|---|
| `renders/bedroom_parametric.glb` | 91 KB / 93,136 bytes | Real binary glTF 2.0 GLB | Browser-sized MVP asset; not research-grade |
| `renders/bedroom_default.gltf` | 401 MB / 420,044,764 bytes | Binary glTF 2.0 despite `.gltf` extension | Too large for practical browser runtime use |
| `renders/bedroom_shell.glb` | 401 MB / 420,044,764 bytes | Large high-fidelity/intermediate GLB | Too large for normal browser/GitHub use without optimization |
| `renders/_infinigen_bedroom_default/scene.blend` | 373 MB | Real Blender 4.03 file | Usable source file for inspection/re-export |
| `renders/_infinigen_bedroom_default/scene.blend1` | 381 MB | Blender backup/source file | Potential backup source |

### Supporting Bedroom Render Files

| Path | Size | Type | Usability |
|---|---:|---|---|
| `renders/_infinigen_bedroom_default/pipeline_coarse.csv` | 990 B | Infinigen pipeline evidence | Useful metadata |
| `renders/_infinigen_bedroom_default/polycounts.txt` | 705 B | Mesh/polycount metadata | Useful metadata |
| `renders/_infinigen_bedroom_default/solve_state.json` | 87 KB | Infinigen solve metadata | Useful metadata |
| `renders/_infinigen_bedroom_default/optim_records.csv` | 62 KB | Optimization metadata | Useful metadata |
| `renders/_infinigen_bedroom_default/optim_records.png` | 15 KB | Diagnostic image | Useful metadata |
| `renders/_infinigen_bedroom_default/MaskTag.json` | 1.1 KB | Metadata | Useful metadata |
| `renders/_infinigen_bedroom_default/assets/info.pickle` | Small metadata file | Metadata | Useful metadata |

### Bedroom Manifests and Params

| Path | Size | Role |
|---|---:|---|
| `manifests/bedroom.manifest.json` | 3.0 KB | Legacy v1 six-parameter manifest |
| `manifests/bedroom.roomspec.v2.json` | 25 KB | Broader RoomSpec v2 Bedroom authoring manifest |
| `params/bedroom_default.json` | 168 B | Legacy v1 default preset |

## Git Tracking Status

Bedroom render outputs are local ignored artifacts:

```text
!! renders/_infinigen_bedroom_default/
!! renders/bedroom_default.gltf
!! renders/bedroom_parametric.glb
```

`.gitignore` ignores:

```text
renders/
*.blend
*.blend1
*.glb
*.gltf
```

So the current source and binary assets exist on this machine, but they are not tracked as regular Git files.

## Required Determinations

### 1. What Bedroom assets exist

Bedroom has:

- `renders/_infinigen_bedroom_default/scene.blend`
- `renders/_infinigen_bedroom_default/scene.blend1`
- `renders/bedroom_default.gltf`
- `renders/bedroom_parametric.glb`
- metadata under `renders/_infinigen_bedroom_default/`
- v1 and v2 Bedroom manifests under `manifests/`
- legacy v1 Bedroom default params under `params/`

### 2. File sizes

Key sizes:

- `bedroom_parametric.glb`: 91 KB / 93,136 bytes
- `bedroom_default.gltf`: 401 MB / 420,044,764 bytes
- `scene.blend`: 373 MB
- `scene.blend1`: 381 MB
- `bedroom.manifest.json`: 3.0 KB
- `bedroom.roomspec.v2.json`: 25 KB
- `bedroom_default.json`: 168 B

### 3. Whether `bedroom_parametric.glb` is a real GLB and browser-usable

**Yes, with quality caveats.**

`file` reports:

```text
renders/bedroom_parametric.glb: glTF binary model, version 2, length 93136 bytes
```

The header begins with the expected GLB magic:

```text
glTF
```

Blender imports the file successfully. Background inspection found:

- Mesh objects: `20`
- Total scene objects: `23`
- Imported dimensions: approximately `(7.0, 19.5, 3.7)`
- Example mesh names:
  - `bedroom_0/0.ceiling`
  - `bedroom_0/0.exterior`
  - `bedroom_0/0.floor`
  - `bedroom_0/0.wall`
  - `KA_PARAM_bed_frame`
  - `KA_PARAM_blanket`
  - `KA_PARAM_chair`
  - `KA_PARAM_desk_top`
  - `KA_PARAM_mattress`
  - `KA_PARAM_nightstand`
  - `KA_PARAM_pillow_1`
  - `KA_PARAM_pillow_2`
  - `KA_PARAM_plant_leaf_1`
  - `KA_PARAM_plant_pot_1`

Browser usability:

- Size is browser-friendly.
- Format is valid GLB.
- It is now used for MVP preview loading.
- It has fixed path loading, wrapper centering, camera framing, and fallback diagnostics in `aframe/viewer.html`.
- It still needs visual review for navigation comfort, material appearance, and participant-visible quality before any research-stimulus claim.

### 4. Why `bedroom_parametric.glb` is only about 91 KB

The GLB is small because it is not a full raw Infinigen scene export.

`renders/bedroom_parametric.glb.meta.json` describes a cleanup/export process:

- `removed_other_rooms`: `true`
- Retained a small set of room shell objects:
  - `bedroom_0/0.ceiling`
  - `bedroom_0/0.exterior`
  - `bedroom_0/0.floor`
  - `bedroom_0/0.wall`
- Added simple parametric furniture:
  - bed
  - pillows
  - nightstand
  - desk
  - chair
  - plant
  - area light

Likely cause of low-quality/small GLB:

- The export intentionally stripped the large Infinigen scene down to a small curated subset.
- Many detailed Infinigen assets/materials were omitted.
- Simple `KA_PARAM` objects were added for controllability and low file size.
- This made the asset fast and lightweight, but reduced realism and research validity.

### 5. Whether `bedroom_default.gltf` is too large for browser use

**Yes.**

`bedroom_default.gltf` is 401 MB / 420,044,764 bytes. It is also reported by `file` as binary glTF 2.0 despite the `.gltf` extension.

This is too large for the current static browser MVP:

- slow initial load
- high memory pressure
- likely poor WebXR performance
- hard to serve/share/commit safely
- likely includes unoptimized full-scene geometry and materials

It should be treated as an intermediate export or diagnostic artifact, not the runtime asset.

### 6. Whether a source `.blend` exists locally

**Yes.**

`renders/_infinigen_bedroom_default/scene.blend` exists locally and is a real Blender file:

```text
Blender3D, saved as 64-bits little endian with version 4.03
```

Blender background inspection loaded it successfully:

- Total objects: `182`
- Mesh objects: `156`
- Infinigen marker object: `infinigen.__version__='1.19.1'`
- Room objects include:
  - `living-room_0/0`
  - `bathroom_0/0`
  - `bedroom_0/0`
  - `dining-room_0/0`
  - `kitchen_0/0`

Pipeline evidence:

- `populate_assets`: ran
- `room_doors`: ran
- `room_windows`: ran
- `room_walls`: ran
- `room_floors`: ran
- `room_ceilings`: ran

`polycounts.txt` reports:

- Verts: `3,060,018`
- Faces: `3,936,391`
- Tris: `6,048,050`
- Objects: `1/94`
- Blender version evidence: `4.2.0`

### 7. Whether Bedroom should use GLB, fallback, or regeneration

Recommended policy by use case:

| Use Case | Recommended Runtime |
|---|---|
| Current MVP demo | Use `bedroom_parametric.glb`; keep procedural fallback |
| Browser performance testing | Use `bedroom_parametric.glb` because it is small |
| Research-quality stimulus validation | Rebuild/export a better GLB from `scene.blend` or regenerate |
| If GLB fails scale/load/material checks | Use procedural fallback |
| If exact parameter changes require new geometry | Regenerate through Infinigen/Blender pipeline |

The current viewer policy should remain GLB-first with fallback. Do not remove the fallback.

### 8. Recommended rebuild path using the Infinigen venv if needed

Preferred order:

1. Inspect the existing source `.blend`.
2. Try to extract a better Bedroom-only GLB from the existing `.blend`.
3. If source extraction cannot produce a usable result, regenerate with the Infinigen venv.

Venv interpreter:

```bash
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python
```

Potential regeneration command shape:

```bash
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python -m infinigen_examples.generate_indoors \
  --output_folder renders/_infinigen_bedroom_rebuild \
  --seed 42 \
  -t coarse populate
```

Then export from Blender to a browser-budgeted GLB:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b renders/_infinigen_bedroom_rebuild/scene.blend \
  --python-expr "import bpy; bpy.ops.export_scene.gltf(filepath='renders/bedroom_rebuild.glb', export_format='GLB', export_apply=True, export_yup=True)"
```

This command shape should be adapted after inspecting the generated scene and isolating the Bedroom room/object set.

## Blender Inspection Recommendation

Open or inspect `renders/_infinigen_bedroom_default/scene.blend` before regenerating.

Inspection goals:

1. Locate `bedroom_0/0` and determine which objects belong to the bedroom.
2. Identify whether high-detail bedroom furniture exists in the source scene or whether the raw generation lacks usable bedroom furnishings.
3. Determine whether other rooms, animals, plants, exterior, cameras, and placeholders can be safely removed.
4. Check object scale and coordinate orientation before export.
5. Check material count, texture references, and unsupported material extensions.
6. Decide whether to preserve raw Infinigen meshes or rebuild simplified but better-quality parametric furniture.
7. Export a test GLB and inspect it in Blender before using it in A-Frame.

## Export Validation Checklist

Before replacing or relying on any Bedroom GLB:

| Check | Target |
|---|---|
| File format | Valid GLB 2.0 |
| File size | Prefer under 50 MB for browser MVP |
| Scene isolation | Bedroom only; no unrelated rooms or placeholder objects |
| Scale | Walkthrough-scale room; camera at human height feels correct |
| Orientation | Floor horizontal, gravity/up axis correct in A-Frame |
| Bounding box | Nonzero and plausible dimensions |
| Navigation | WASD movement works without starting inside walls/furniture |
| Materials | No missing textures; no extreme black/white/transparent surfaces |
| Lighting | Visible under viewer lights without baked-light dependency |
| Polycount | Low enough for browser/WebXR performance |
| Load time | Acceptable over local static server |
| Fallback | Procedural fallback remains available if load fails |

## Fallback Policy

Keep the current procedural Bedroom fallback.

The current `bedroom_parametric.glb` is acceptable as an MVP runtime loading target, but it should not be described as research-grade or photorealistic.

Do not:

- Claim the current Bedroom GLB is final.
- Remove fallback behavior.
- Use `bedroom_default.gltf` directly in the browser runtime.
- Replace `bedroom_parametric.glb` with the 401 MB high-fidelity/intermediate assets as the default browser asset without optimization and validation.

Current acceptable user-facing statement:

```text
Bedroom has a lightweight GLB available and loading for MVP preview, but it is not research-grade. The viewer keeps a procedural fallback for load, bounds, or quality issues.
```
