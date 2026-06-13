# Living Room Asset Report

Hour 3 investigation for the Living Room asset state, with later checkpoint updates.

## Checkpoint Update: 2026-06-12

Living Room Infinigen regeneration has now succeeded locally.

New local artifacts:

| Path | Size | Status |
|---|---:|---|
| `renders/_infinigen_living_room_regen_test/scene.blend` | about 1.0 GB | Real regenerated Blender source scene; local ignored heavy asset |
| `renders/_infinigen_living_room_regen_test/` | about 6.5 GB | Full local regeneration output directory; keep local/external |
| `renders/living_room_shell.glb` | 84 KB | Lightweight shell-only GLB export; useful evidence but not the reliable runtime path |

The original default Living Room files under `renders/_infinigen_living_room_default/` may still include LFS pointer artifacts from an earlier run, but that is no longer the only recovery path. The current reliable application runtime remains the procedural A-Frame Living Room preview. Do not switch Living Room runtime behavior to the shell GLB until it passes visual, navigation, scale, and room-completeness validation.

Scope inspected:

- `renders/`
- `assets/`
- `gallery/`
- `scans/`
- `manifests/`
- `params/`

Application code was not modified during the original Hour 3 report.

## Executive Summary

Original finding: no usable Living Room `.blend`, `.glb`, or `.gltf` asset was available in the checkout at the time of the Hour 3 investigation. The original default Living Room Blender files appeared as Git LFS pointer text files.

Current checkpoint finding: local regeneration succeeded and produced a real large `.blend` plus a small shell-only GLB. The current fallback policy should still remain: use the procedural A-Frame Living Room preview until a validated, complete, browser-budgeted GLB is produced.

## Commands Run

```bash
find renders -name "*.blend"
find renders -name "*.glb"
find renders -name "*.gltf"
find . -iname "*living*"
git lfs ls-files
```

Additional checks:

```bash
find assets -maxdepth 4 -type f -print
find gallery -maxdepth 4 -type f -print
find scans -maxdepth 4 -type f -print
find renders/_infinigen_living_room_default -maxdepth 3 -type f -print
git check-attr filter diff merge text -- renders/_infinigen_living_room_default/scene.blend renders/_infinigen_living_room_default/scene.blend1
git check-ignore -v renders/_infinigen_living_room_default/scene.blend renders/bedroom_parametric.glb renders/bedroom_default.gltf
which python3
python3 --version
python3 -c "import infinigen"
ls -ld /Users/naokoshibuya/Desktop/code/infinigen/venv
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python --version
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python -c "import infinigen; print(infinigen.__file__)"
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python -c "import infinigen_examples; print(infinigen_examples.__file__)"
```

## Files Found

### Render Files

| Path | Size | Type | Usability |
|---|---:|---|---|
| `renders/_infinigen_living_room_default/scene.blend` | 134 B | Git LFS pointer text | Not usable as a Blender source file |
| `renders/_infinigen_living_room_default/scene.blend1` | 134 B | Git LFS pointer text | Not usable as a Blender source file |
| `renders/_infinigen_living_room_default/pipeline_coarse.csv` | 989 B | Infinigen pipeline evidence | Useful metadata only |
| `renders/_infinigen_living_room_default/polycounts.txt` | 705 B | Mesh/polycount metadata | Useful metadata only |
| `renders/_infinigen_living_room_default/solve_state.json` | 64 KB | Infinigen solve metadata | Useful metadata only |
| `renders/_infinigen_living_room_default/optim_records.csv` | 64 KB | Optimization metadata | Useful metadata only |
| `renders/_infinigen_living_room_default/optim_records.png` | 14 KB | Diagnostic image | Useful metadata only |
| `renders/_infinigen_living_room_default/MaskTag.json` | 906 B | Metadata | Useful metadata only |
| `renders/_infinigen_living_room_default/assets/info.pickle` | 236 B | Metadata | Useful metadata only |

At the time of the original report, no Living Room `.glb` or `.gltf` file was found. A later local shell-only export now exists:

| Path | Size | Notes |
|---|---:|---|
| `renders/living_room_shell.glb` | 84 KB | Shell-only Living Room export; not currently the reliable runtime path |

For comparison, Bedroom assets exist locally:

| Path | Size | Notes |
|---|---:|---|
| `renders/bedroom_parametric.glb` | 91 KB | Bedroom only; not relevant to Living Room |
| `renders/bedroom_default.gltf` | 401 MB | Bedroom only; not relevant to Living Room |

### Living Room Paths Found Outside Render Outputs

| Path | Size / Contents | Usability |
|---|---:|---|
| `assets/living_room/` | Empty directory | No usable asset |
| `gallery/living_room/` | Empty directory | No usable asset |
| `params/living_room_default.json` | 177 B | Legacy v1 parameter preset |
| `params/living_room_perturbed1.json` | 177 B | Legacy v1 parameter preset |
| `params/living_room_perturbed2.json` | 176 B | Legacy v1 parameter preset |
| `manifests/living_room.manifest.json` | 3.2 KB | Legacy v1 parameter manifest |
| `manifests/living_room.roomspec.v2.json` | 25 KB | RoomSpec v2 authoring manifest |

`scans/` contains only `.gitkeep`. No Living Room scan asset was found.

## Git LFS Pointer Status

`renders/_infinigen_living_room_default/scene.blend` contains:

```text
version https://git-lfs.github.com/spec/v1
oid sha256:610366e1d097515e30449b9389b2e06c91469f62fe5f65d6be03c358fc095dbb
size 136977701
```

`renders/_infinigen_living_room_default/scene.blend1` contains:

```text
version https://git-lfs.github.com/spec/v1
oid sha256:6699a2fdb4f3bb940a4b5b10269e5ac57a6445e6f9a377e8a769ef3090bee9ab
size 137599797
```

These files are not Blender binaries in the current checkout. They are pointer text files for two expected binary blobs of roughly 137 MB each.

Important Git finding:

- `git lfs ls-files` returned no files.
- No `.gitattributes` file was found.
- `git check-attr` reports no LFS filter configured for the Living Room `.blend` files.
- `.gitignore` ignores `*.blend`, `*.blend1`, `*.glb`, `*.gltf`, and all of `renders/`.
- `git status --ignored` shows render binaries/directories as ignored, not tracked.

This means the current checkout contains LFS pointer text locally, but Git LFS is not currently configured/tracking those files in this repository state.

## Prior Generation Evidence

`renders/_infinigen_living_room_default/pipeline_coarse.csv` shows a prior Infinigen run completed major stages:

- `solve_rooms`: ran
- `populate_assets`: ran
- `room_doors`: ran
- `room_windows`: ran
- `room_walls`: ran
- `room_floors`: ran
- `room_ceilings`: ran

`polycounts.txt` reports:

- Verts: `1,053,660`
- Faces: `1,175,368`
- Tris: `2,074,987`
- Blender version evidence: `4.2.0`

This supports the conclusion that a Living Room scene was generated in a prior environment, but the usable `.blend` payload is missing from this checkout.

## Required Determinations

### 1. Whether a usable Living Room `.blend` exists

**Original Hour 3 answer: No. Current checkpoint answer: Yes, locally, via regeneration.**

Only pointer-sized files exist:

- `renders/_infinigen_living_room_default/scene.blend`
- `renders/_infinigen_living_room_default/scene.blend1`

Both are Git LFS pointer text files, not usable Blender binaries.

However, regeneration later produced a real local source scene:

- `renders/_infinigen_living_room_regen_test/scene.blend`

This regenerated file is a heavy local ignored artifact and should not be committed directly.

### 2. Whether a usable Living Room `.glb` / `.gltf` exists

**Original Hour 3 answer: No. Current checkpoint answer: a shell-only GLB exists locally.**

The only discovered GLB/GLTF files are Bedroom assets:

- `renders/bedroom_parametric.glb`
- `renders/bedroom_default.gltf`

The current local shell export is:

- `renders/living_room_shell.glb` — 84 KB

This file should be treated as shell-only pipeline evidence until it passes A-Frame visual/navigation validation.

### 3. Whether any Living Room asset is only a Git LFS pointer

**Yes.**

Both Living Room Blender files are Git LFS pointer text:

- `renders/_infinigen_living_room_default/scene.blend`
- `renders/_infinigen_living_room_default/scene.blend1`

### 4. Whether `git lfs pull` could recover it

**Uncertain / unlikely in the current repository state without restoring LFS tracking metadata.**

The pointer text contains valid-looking LFS object IDs and expected blob sizes, so recovery may be possible if the remote LFS store still has those objects. However, this checkout does not currently advertise any LFS-tracked files:

- `git lfs ls-files` returned nothing.
- No `.gitattributes` file exists.
- `git check-attr` shows no LFS filter for the `.blend` paths.

Recommended recovery check, if network access and the correct remote are available:

```bash
git lfs pull --include="renders/_infinigen_living_room_default/scene.blend"
git lfs pull --include="renders/_infinigen_living_room_default/scene.blend1"
```

If those commands do not replace the pointer files with ~137 MB Blender files, recover from the original environment, restore the LFS configuration, or regenerate.

### 5. Whether Infinigen regeneration is required

**No longer strictly required for first recovery, because Living Room regeneration has succeeded locally.**

Regeneration remains required for future RoomSpec-driven geometry variation and for producing a complete validated asset if the current shell-only export is insufficient.

Current default repo-shell Python check:

```text
/opt/anaconda3/bin/python3
Python 3.12.4
ModuleNotFoundError: No module named 'infinigen'
```

This only means the current Anaconda Python environment cannot see Infinigen.

Separate Infinigen virtual environment check:

```text
/Users/naokoshibuya/Desktop/code/infinigen/venv
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python
Python 3.11.15
/Users/naokoshibuya/Desktop/code/infinigen/venv/lib/python3.11/site-packages/infinigen/__init__.py
/Users/naokoshibuya/Desktop/code/infinigen/venv/lib/python3.11/site-packages/infinigen_examples/__init__.py
```

Conclusion: Infinigen is accessible through the separate virtual environment at:

```bash
/Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python
```

Local regeneration has since been verified through the separate Infinigen environment. Future regeneration remains subject to runtime dependencies, Blender integration, disk space, and successful export validation.

### 6. Recommended next action

Recommended order:

1. Keep the procedural Living Room preview as the reliable runtime path.
2. Treat `renders/_infinigen_living_room_regen_test/scene.blend` as the current local source for inspection/export.
3. Treat `renders/living_room_shell.glb` as shell-only evidence, not a complete runtime asset.
4. Validate the shell GLB in Blender and A-Frame: scale, orientation, bounding box, visibility, load time, and walkthrough usability.
5. If a complete room is needed, export a browser-budgeted GLB from the regenerated source scene with a target of 50 MB or less.
6. Only after validation, consider wiring the Living Room viewer path to load a GLB.
7. For geometry-changing parameters, prefer RoomSpec-driven regeneration or a dedicated geometry-control layer over direct static mesh transforms.

## Blocker

The original blocker was missing source geometry:

```text
Living Room source .blend files are Git LFS pointers, not actual Blender files.
No Living Room GLB/GLTF exists in the current checkout.
The default repo-shell Python cannot import Infinigen, but the separate Infinigen venv can.
```

Current checkpoint blocker:

```text
Living Room source geometry now exists locally after regeneration, but the available lightweight GLB is shell-only. The full regeneration output is too large for ordinary GitHub/browser use, and direct Blender transforms on static shell components do not automatically update related walls/windows/doors/openings.
```

## Recovery Plan

### Path A: Recover Existing Generated Source

1. Restore or recreate Git LFS tracking for Blender files if needed.
2. Run:

   ```bash
   git lfs pull --include="renders/_infinigen_living_room_default/scene.blend"
   git lfs pull --include="renders/_infinigen_living_room_default/scene.blend1"
   ```

3. Verify file sizes:

   - `scene.blend` should be approximately `136,977,701` bytes.
   - `scene.blend1` should be approximately `137,599,797` bytes.

4. Inspect in Blender.
5. Export `renders/living_room_default.glb`.
6. Validate in A-Frame before changing runtime policy.

### Path B: Regenerate

1. Use the separate Infinigen virtual environment:

   ```bash
   /Users/naokoshibuya/Desktop/code/infinigen/venv/bin/python
   ```

2. Generate Living Room from existing manifest/preset inputs or future RoomSpec v2 inputs.
3. Export GLB through Blender.
4. Validate GLB scale and quality.
5. Commit only validated, appropriately sized browser assets or document why assets remain external.

## Fallback Policy

Keep the current procedural A-Frame Living Room fallback as the active runtime policy until a validated GLB exists.

Do not:

- Claim the current Living Room is a real Infinigen GLB.
- Claim photorealism.
- Remove the procedural fallback.
- Change `index.html` or `aframe/viewer.html` until asset recovery/export validation is complete.

Current acceptable user-facing statement:

```text
Living Room currently uses a procedural A-Frame preview as the reliable runtime path. Local Infinigen regeneration and a shell-only GLB export exist, but they are not yet validated as complete browser runtime assets.
```
