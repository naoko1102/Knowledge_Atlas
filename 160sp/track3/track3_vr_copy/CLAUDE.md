# CLAUDE.md

Read PROJECT_MEMORY.md before making implementation decisions.

## Mission

Build a professor-quality MVP for a web-based environmental psychology experiment authoring platform.

The target rooms are:

- Living Room
- Bedroom

The student-facing app must support:

1. Room selection
2. Parameter editing
3. Control condition creation
4. Treatment condition creation
5. Diff viewing
6. A-Frame/WebXR preview
7. Save/load

## Key Principle

This is not an Infinigen GUI.

Infinigen is used as an authoring-side asset generation pipeline.

The student-facing web app must still work even if Infinigen is unavailable or a generated asset is too large.

## Current Asset Policy

- Bedroom has a lightweight generated asset: renders/bedroom_parametric.glb
- Living Room currently uses a procedural A-Frame fallback because no lightweight GLB is available
- Asset status is documented in renders/asset_manifest.json

## Implementation Priority

1. aframe/viewer.html
2. index.html room picker
3. parameter editor
4. experiment builder
5. diff viewer
6. save/load
7. README/demo instructions

## Development Rules

- Keep implementation minimal.
- Prefer working demo over perfect architecture.
- Do not create a backend.
- Do not require Node or a build step unless explicitly requested.
- Serve locally with: python3 -m http.server 8000
- Do not run Infinigen from the student-facing UI.
- Do not modify unrelated files.
- Work in small commits.

## MVP Demo Workflow

The required demo workflow is:

1. Open index.html
2. Select Living Room or Bedroom
3. Adjust one parameter
4. Save current state as Control
5. Duplicate Control as Treatment
6. Change one parameter in Treatment
7. View the diff
8. Launch Control in A-Frame
9. Launch Treatment in A-Frame

If this workflow works, the MVP is successful.
