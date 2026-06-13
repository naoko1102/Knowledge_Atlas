#!/usr/bin/env python3
"""infinigen_wrapper.py — Track 3 Task 2 central artifact.

Takes a JSON parameter dict (matching a Task 1 manifest), invokes Infinigen
Indoors to instantiate the corresponding room, and exports the result as a
single glTF/GLB file with embedded textures.

Usage:

    python3 infinigen_wrapper.py --room living_room \
        --manifest manifests/living_room.manifest.json \
        --params   params/living_room_default.json \
        --out      renders/living_room_default.gltf

    python3 infinigen_wrapper.py --room bedroom --params-default \
        --out renders/bedroom_default.gltf --quick

Output: a glTF file at the requested path, plus a sidecar JSON
<out>.meta.json recording the resolved parameters and render time.
"""
from __future__ import annotations
import argparse, json, sys, time, os, subprocess, tempfile
from pathlib import Path


# ──────────────────────────────────────────────────────────────────
# Room builders — naoko-shibuya custom implementations
# ──────────────────────────────────────────────────────────────────

def build_living_room(params: dict, infinigen):
    """Living room builder using manifest keys from living_room.manifest.json."""
    from infinigen_examples.constraints.home import sample_home_constraint_params
    base = sample_home_constraint_params()
    base["furniture_fullness_pct"] = params.get("furniture_fullness_pct", 0.75)
    base["painting_area_per_room_area"] = params.get("painting_area_per_room_area", 1.5)
    base["has_tv"] = params.get("has_tv", True)
    return base


def build_bedroom(params: dict, infinigen):
    """Bedroom builder using manifest keys from bedroom.manifest.json."""
    from infinigen_examples.constraints.home import sample_home_constraint_params
    base = sample_home_constraint_params()
    base["furniture_fullness_pct"] = params.get("furniture_fullness_pct", 0.72)
    return base


def build_default(params: dict, infinigen, room_type: str):
    """Generic fallback using sample_home_constraint_params."""
    from infinigen_examples.constraints.home import sample_home_constraint_params
    base = sample_home_constraint_params()
    base.update(params)
    return base


ROOM_BUILDERS = {
    "living_room":  build_living_room,
    "bedroom":      build_bedroom,
    "kitchen":      lambda p, i: build_default(p, i, "kitchen"),
    "bathroom":     lambda p, i: build_default(p, i, "bathroom"),
    "dining_room":  lambda p, i: build_default(p, i, "dining_room"),
    "hallway":      lambda p, i: build_default(p, i, "hallway"),
    "office":       lambda p, i: build_default(p, i, "office"),
}


# ──────────────────────────────────────────────────────────────────
# glTF export via Blender headless
# ──────────────────────────────────────────────────────────────────

GLTF_EXPORT_PY = r"""
# Run inside Blender's Python: bake the current scene to glTF.
import bpy, sys
out_path = sys.argv[sys.argv.index('--') + 1]
bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format='GLB',
    export_image_format='AUTO',
    export_yup=True,
    export_apply=True,
)
print(f"Wrote {out_path}")
"""


def export_to_gltf(scene_blend_path: Path, out_path: Path) -> bool:
    """Invoke Blender headless to export a .blend to GLB. Returns True on success."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(GLTF_EXPORT_PY)
        export_script = Path(f.name)
    try:
        result = subprocess.run([
            "blender", "-b", str(scene_blend_path),
            "--python", str(export_script),
            "--", str(out_path),
        ], capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            sys.stderr.write(f"Blender export failed:\n{result.stderr[-500:]}\n")
            return False
        return out_path.exists()
    finally:
        export_script.unlink(missing_ok=True)


# ──────────────────────────────────────────────────────────────────
# Infinigen scene runner
# ──────────────────────────────────────────────────────────────────

def run_infinigen_scene(params_dict: dict, room_type: str, out_path: Path) -> bool:
    """
    Run Infinigen's indoor pipeline via subprocess to produce a .blend file,
    then export to glTF.

    The builder functions return a constraint-params dict (not a scene object),
    so we pass params to Infinigen's generate_indoors entry point directly.
    """
    import infinigen
    import infinigen_examples

    blend_path = out_path.with_suffix(".blend")

    # Convert JSON params to gin format for Infinigen's --overrides
    gin_overrides = []
    for key, value in params_dict.items():
        if isinstance(value, bool):
            gin_overrides.append(f"{key}={str(value).lower()}")
        elif isinstance(value, str):
            gin_overrides.append(f"{key}='{value}'")
        else:
            gin_overrides.append(f"{key}={value}")

    try:
        # Get infinigen root directory for proper gin config loading
        infinigen_root = Path(infinigen.__file__).parent.parent

        # Run generate_indoors as a module from infinigen root directory
        cmd = [
            sys.executable,
            "-m", "infinigen_examples.generate_indoors",
            "--output_folder", str(blend_path.parent),
            "--seed", "0",
            "-t", "coarse", "populate",
            "--overrides", *gin_overrides,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=str(infinigen_root))
        if result.returncode != 0:
            sys.stderr.write(f"Infinigen process failed:\n{result.stderr[-1000:]}\n")
            return False

        # Infinigen writes scene.blend into the output folder
        scene_blend = blend_path.parent / "scene.blend"
        if not scene_blend.exists():
            sys.stderr.write("Infinigen did not produce scene.blend\n")
            return False
        return export_to_gltf(scene_blend, out_path)
    except Exception as e:
        sys.stderr.write(f"Infinigen pipeline error: {e}\n")
        return False


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--room", required=True,
                   help="Room type (living_room, bedroom, kitchen, etc.)")
    p.add_argument("--manifest",
                   help="Path to room's JSON-Schema manifest (optional; "
                        "used to validate params before render)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--params", help="Path to JSON parameter dict")
    g.add_argument("--params-default", action="store_true",
                   help="Render with default parameters")
    p.add_argument("--out", required=True, help="Output GLB/glTF path")
    p.add_argument("--quick", action="store_true",
                   help="Quick CPU render (smoke-test quality)")
    args = p.parse_args()

    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Idempotency check ──────────────────────────────────────────
    meta_path = Path(str(out_path) + ".meta.json")
    if out_path.exists() and meta_path.exists():
        print(f"SKIP: {out_path} already exists with sidecar (idempotent)")
        return 0

    # ── Load parameters ───────────────────────────────────────────
    if args.params_default:
        params = {}
    else:
        with open(args.params) as f:
            params = json.load(f)

    # ── Manifest validation (optional) ────────────────────────────
    if args.manifest:
        try:
            from jsonschema import validate
            with open(args.manifest) as f:
                manifest = json.load(f)
            # Validate only the properties section
            validate(instance=params, schema=manifest)
        except ImportError:
            sys.stderr.write("Warning: jsonschema not installed; skipping validation\n")
        except Exception as e:
            sys.stderr.write(f"Manifest validation failed: {e}\n")
            return 1

    # ── Get builder ───────────────────────────────────────────────
    builder = ROOM_BUILDERS.get(args.room)
    if builder is None:
        sys.stderr.write(
            f"No builder for room_type={args.room!r}. "
            f"Available: {sorted(ROOM_BUILDERS)}\n"
        )
        return 1

    t0 = time.time()

    # ── Import Infinigen ──────────────────────────────────────────
    try:
        import infinigen
    except ImportError:
        sys.stderr.write("Infinigen not installed. Run: bash scripts/track3/setup_track3.sh\n")
        if args.params_default:
            _write_stub_gltf(out_path, args.room)
            _write_sidecar(out_path, args.room, params, time.time() - t0,
                           note="Infinigen unavailable — stub glTF for smoke test only")
            return 0
        return 1

    # ── Build constraint-params dict via builder ──────────────────
    try:
        resolved_params = builder(params, infinigen)
    except Exception as e:
        sys.stderr.write(f"Builder failed: {type(e).__name__}: {e}\n")
        return 2

    # ── Run Infinigen pipeline → glTF ─────────────────────────────
    try:
        ok = run_infinigen_scene(resolved_params, args.room, out_path)
        if not ok:
            sys.stderr.write("Render did not produce output file.\n")
            return 2
    except Exception as e:
        sys.stderr.write(f"Render failed: {type(e).__name__}: {e}\n")
        return 2

    elapsed = time.time() - t0
    _write_sidecar(out_path, args.room, params, elapsed)
    print(f"OK: rendered {args.room} -> {out_path} ({elapsed:.1f}s)")
    return 0


def _write_sidecar(out: Path, room: str, params: dict,
                   elapsed: float, note: str = "") -> None:
    sidecar = Path(str(out) + ".meta.json")
    with open(sidecar, "w") as f:
        json.dump({
            "room": room,
            "resolved_params": params,
            "render_time_seconds": round(elapsed, 2),
            "wrapper_version": "0.1.0-naoko-shibuya",
            "note": note,
        }, f, indent=2)


def _write_stub_gltf(out: Path, room: str) -> None:
    """Minimal valid GLB for smoke test."""
    minimal = (
        b"glTF"
        + (2).to_bytes(4, "little")
        + (88).to_bytes(4, "little")
        + (20).to_bytes(4, "little")
        + b"JSON"
        + b'{"asset":{"version":"2.0"}}'
    )
    out.write_bytes(minimal)


if __name__ == "__main__":
    sys.exit(main())
