# Living Room Structure Notes

Regenerated scene inspected:

```text
renders/_infinigen_living_room_regen_test/scene.blend
```

Application code was not modified.

## Checkpoint Update: 2026-06-12

Blender/MCP inspection confirmed that current Infinigen exports are mostly static meshes. Individual object transforms are editable, but direct geometry edits are not topology-aware:

- Moving or scaling the ceiling does not automatically propagate to walls.
- Window and door assets do not automatically update their wall openings.
- Door/window relationship to a room may be spatial rather than name-prefixed.
- A shell-only Living Room GLB exists locally at `renders/living_room_shell.glb`, but it is not a complete validated runtime asset.

Implication: Blender MCP is useful for inspection, object selection, export collection assembly, and validation. It should not be treated as a complete parametric geometry solver unless a dedicated geometry-control layer updates all related shell/opening components together. Future geometry changes should likely follow:

```text
RoomSpec v2
-> Infinigen/regeneration or dedicated geometry-control layer
-> Blender cleanup/export
-> A-Frame bounds/visibility/navigation validation
```

## Summary

The regenerated Living Room scene has a usable structural naming pattern:

- `placeholders:room_shells` contains room shell placeholders such as `living-room_0/0`.
- `placeholders:room_meshes` contains matching meshed placeholders such as `living-room_0/0.meshed`.
- `unique_assets:room_wall`, `unique_assets:room_floor`, `unique_assets:room_ceiling`, and `unique_assets:room_exterior` contain room-specific geometry with the same room prefix.
- `unique_assets:windows` and `unique_assets:doors` contain factory-named assets without room prefixes, so they need spatial association against the Living Room shell.

This means Blender MCP can likely identify the Living Room shell and its core architectural geometry deterministically by name, then associate doors/windows by bounding-box overlap.

## Scene Collections of Interest

| Collection | Object Count | Purpose |
|---|---:|---|
| `placeholders` | 66 | High-level placeholder assets and child collections |
| `placeholders:room_shells` | 13 | One shell object per generated room |
| `placeholders:room_meshes` | 13 | Meshed room placeholders matching room shell names |
| `unique_assets` | 66 | Populated non-shell assets and child collections |
| `unique_assets:room_wall` | 13 | One wall mesh per room |
| `unique_assets:room_floor` | 13 | One floor mesh per room |
| `unique_assets:room_ceiling` | 13 | One ceiling mesh per room |
| `unique_assets:room_exterior` | 13 | One exterior/envelope mesh per room |
| `unique_assets:windows` | 44 | Window assets plus area/light helper objects |
| `unique_assets:doors` | 13 | Door assets |
| `skirting` | 2 | Shared skirting/support meshes |

## Room Shells and Room Meshes

`placeholders:room_shells` contains:

```text
living-room_0/0
bedroom_0/0
dining-room_0/0
hallway_0/0
kitchen_0/0
bathroom_0/0
bathroom_0/1
bedroom_0/1
bedroom_0/2
closet_0/0
bathroom_0/2
bathroom_0/3
closet_0/1
```

`placeholders:room_meshes` contains the same base names with `.meshed` suffix:

```text
living-room_0/0.meshed
bedroom_0/0.meshed
dining-room_0/0.meshed
...
```

The Living Room shell and meshed placeholder share the same bounding box:

| Object | Center | Dimensions | Bounding Box |
|---|---|---|---|
| `living-room_0/0` | `(6.5, 3.0, 1.433)` | `(9.0, 9.0, 2.866)` | `(2.0, -1.5, 0.0)` to `(11.0, 7.5, 2.866)` |
| `living-room_0/0.meshed` | `(6.5, 3.0, 1.433)` | `(9.0, 9.0, 2.866)` | `(2.0, -1.5, 0.0)` to `(11.0, 7.5, 2.866)` |

Interpretation:

- `living-room_0/0` is the logical room shell placeholder.
- `living-room_0/0.meshed` is the matching meshed room proxy.
- These are useful for selection, spatial bounds, and transform targets, but not sufficient alone for final GLB export.

## Mapping `living-room_0/0` to `unique_assets`

Core room architecture maps by name prefix.

| Room Role | Object | Collection | Notes |
|---|---|---|---|
| Shell placeholder | `living-room_0/0` | `placeholders:room_shells` | Primary logical room identifier |
| Meshed placeholder | `living-room_0/0.meshed` | `placeholders:room_meshes` | Same bounds as shell |
| Walls | `living-room_0/0.wall` | `unique_assets:room_wall` | Room-specific wall mesh |
| Floor | `living-room_0/0.floor` | `unique_assets:room_floor` | Room-specific floor mesh |
| Ceiling | `living-room_0/0.ceiling` | `unique_assets:room_ceiling` | Room-specific ceiling mesh |
| Exterior/envelope | `living-room_0/0.exterior` | `unique_assets:room_exterior` | Same outer bounds as shell |

Measured Living Room architectural assets:

| Object | Center | Dimensions | Bounding Box |
|---|---|---|---|
| `living-room_0/0.wall` | `(6.5, 3.0, 1.433)` | `(9.0, 9.0, 2.663)` | `(2.0, -1.5, 0.101)` to `(11.0, 7.5, 2.765)` |
| `living-room_0/0.floor` | `(6.551, 3.0, 0.101)` | `(8.899, 9.0, 0.0)` | `(2.101, -1.5, 0.101)` to `(11.0, 7.5, 0.101)` |
| `living-room_0/0.ceiling` | `(6.5, 3.0, 2.775)` | `(8.797, 8.797, 0.0)` | `(2.101, -1.399, 2.775)` to `(10.899, 7.399, 2.775)` |
| `living-room_0/0.exterior` | `(6.5, 3.0, 1.433)` | `(9.0, 9.0, 2.866)` | `(2.0, -1.5, 0.0)` to `(11.0, 7.5, 2.866)` |

Conclusion:

`living-room_0/0` maps to `unique_assets` through deterministic object names:

```text
living-room_0/0.wall
living-room_0/0.floor
living-room_0/0.ceiling
living-room_0/0.exterior
```

This is the safest first-pass export set for the architectural shell.

## Windows and Doors

Windows and doors do not use the `living-room_0/0` name prefix.

They are factory-named:

```text
WindowFactory(...).spawn_asset(...)
GlassPanelDoorFactory(...).spawn_asset(...)
LiteDoorFactory(...).spawn_asset(...)
```

Candidate Living Room windows found by bounding-box overlap with the Living Room shell:

| Candidate | Center | Dimensions |
|---|---|---|
| `WindowFactory(42300).spawn_asset(6)` | `(9.89, 1.148, 1.472)` | `(1.094, 0.136, 1.083)` |
| `WindowFactory(42300).spawn_asset(7)` | `(10.899, 1.803, 1.472)` | `(0.055, 0.991, 1.078)` |
| `WindowFactory(42300).spawn_asset(20)` | `(8.399, -0.735, 1.472)` | `(0.075, 1.092, 1.086)` |

Candidate Living Room doors found by bounding-box overlap with the Living Room shell:

| Candidate | Center | Dimensions |
|---|---|---|
| `GlassPanelDoorFactory(3240805).spawn_asset(1)` | `(5.69, 3.696, 1.405)` | `(2.19, 1.947, 2.607)` |
| `GlassPanelDoorFactory(3240805).spawn_asset(10)` | `(10.9, 3.237, 1.405)` | `(1.956, 1.281, 2.607)` |
| `LiteDoorFactory(5607973).spawn_asset(0)` | `(7.371, 7.99, 1.16)` | `(1.773, 1.475, 2.118)` |
| `LiteDoorFactory(5607973).spawn_asset(2)` | `(2.218, 7.296, 1.16)` | `(1.801, 1.802, 2.118)` |
| `GlassPanelDoorFactory(875692).spawn_asset(3)` | `(11.008, 6.853, 1.329)` | `(1.704, 1.43, 2.648)` |
| `GlassPanelDoorFactory(875692).spawn_asset(12)` | `(5.14, -0.926, 1.329)` | `(1.692, 1.412, 2.648)` |

Important caution:

- Bounding-box overlap is a starting heuristic, not a final truth source.
- Some overlapping doors may belong to adjacent rooms or shared openings.
- Window/door association should be confirmed visually or by portal/cutter relationship before export.

## How a Single Room Can Be Isolated

Recommended isolation layers:

1. **Room identity**
   - Select the target shell: `living-room_0/0`.
   - Use its bounding box as the spatial reference.

2. **Core architectural geometry**
   - Include deterministic name-mapped assets:
     - `living-room_0/0.wall`
     - `living-room_0/0.floor`
     - `living-room_0/0.ceiling`
     - `living-room_0/0.exterior`

3. **Openings**
   - Candidate windows and doors should be selected from `unique_assets:windows` and `unique_assets:doors`.
   - Use bounding-box overlap/intersection with the shell.
   - Prefer objects touching or near shell boundaries over objects merely inside the XY bounds.
   - Validate visually.

4. **Optional trim/supports**
   - `skirting` appears shared, not room-prefixed.
   - Include only if it can be clipped or confirmed to belong to the Living Room.

5. **Movable/interior assets**
   - Placeholder assets in `placeholders` and `unique_assets` are not room-prefixed.
   - Associate by spatial containment within the Living Room bounding box, then validate manually.
   - Do not include all `unique_assets` wholesale.

## Blender MCP Identification Strategy

Blender MCP should identify room-specific geometry in this order:

1. Find `placeholders:room_shells`.
2. Locate exact object name `living-room_0/0`.
3. Read its world-space bounding box.
4. Select deterministic room-prefixed geometry:
   - `living-room_0/0.meshed`
   - `living-room_0/0.wall`
   - `living-room_0/0.floor`
   - `living-room_0/0.ceiling`
   - `living-room_0/0.exterior`
5. Search `unique_assets:windows` and `unique_assets:doors` for objects whose world bounding boxes intersect or touch the shell boundary.
6. Optionally search `unique_assets` and `placeholders` for furniture/decor objects whose bounding-box centers fall inside the shell bounds.
7. Put selected objects into a temporary export collection, for example:

   ```text
   KA_EXPORT_living_room_0_0
   ```

8. Export only that collection after visual validation.

Recommended MCP guardrails:

- Never select all of `unique_assets`.
- Never select all of `placeholders`.
- Treat shared collections (`skirting`, `door_base_elements`, terrain, rocks, nature backdrop) as opt-in only.
- Record every selected object path/name in an export manifest before export.
- Run a bounding-box sanity check on the export collection.

## Export Strategy for a Single Room

### Pass 1: Shell-Only Export

Goal:

Create the smallest validated Living Room architectural GLB.

Include:

```text
living-room_0/0.wall
living-room_0/0.floor
living-room_0/0.ceiling
living-room_0/0.exterior
```

Maybe include:

```text
living-room_0/0.meshed
```

Only include `.meshed` if it contributes visible geometry and does not duplicate the wall/floor/ceiling/exterior meshes.

Exclude:

```text
terrain
rocks
nature_backdrop
all non-room-prefixed unique_assets
all other rooms
all placeholder factories not validated as inside Living Room
```

Success criteria:

- GLB is valid.
- Room scale matches the source shell.
- Floor, walls, ceiling, and exterior are visible in Blender and A-Frame.
- File size is browser-feasible.

### Pass 2: Openings Export

Goal:

Add Living Room windows and doors.

Include:

- Window candidates that touch/intersect Living Room shell boundaries.
- Door candidates confirmed to belong to Living Room openings.

Success criteria:

- Openings align with walls.
- No duplicate or adjacent-room doors appear in the room.
- Door/window transforms remain editable.

### Pass 3: Furnished Export

Goal:

Add validated furniture/decor assets.

Selection rule:

- Include objects whose bounding-box centers are inside the Living Room shell and whose visual role is appropriate.
- Validate each object manually or through screenshot review.

Success criteria:

- Export is navigable.
- No unrelated room objects are included.
- Asset quality is acceptable for MVP preview, while still not overclaiming research-grade realism.

## Likely MCP-Editable Parameters

Based on the structure, these may be feasible after object mapping:

| Parameter | Candidate MCP Edit Target | Risk |
|---|---|---|
| Ceiling height | `living-room_0/0.ceiling`, `living-room_0/0.wall`, `living-room_0/0.exterior` | Wall/window/door alignment can break |
| Room dimensions | Shell, meshed proxy, wall/floor/ceiling/exterior meshes | Non-uniform scaling may distort openings/materials |
| Window position | Candidate `WindowFactory(...).spawn_asset(...)` objects plus wall openings/cutters | Window mesh can detach from wall opening |
| Door position | Candidate `DoorFactory(...).spawn_asset(...)` objects plus wall openings/cutters | Door can detach from portal/opening |

Observed checkpoint limitation:

Direct ceiling transforms do not propagate to the rest of the architectural shell. Treat the table above as an identification map, not a promise that isolated object transforms can safely implement RoomSpec geometry parameters.

Before editing:

- Identify cutter/portal relationships for windows and doors.
- Confirm whether edits should move only visible assets or also wall openings.
- Work on a copy of the `.blend`.

## Open Questions

1. Which candidate door/window objects are actually connected to `living-room_0/0` versus adjacent rooms?
2. Are portal cutters preserved in a way that maps openings back to rooms?
3. Should `living-room_0/0.meshed` be exported, or only the `unique_assets:room_*` meshes?
4. Can skirting be isolated per room, or does it need clipping/rebuild?
5. Are furniture/decor objects spatially reliable enough to select by containment?

## Recommended Next Step

Create a non-destructive Blender/MCP selection test:

1. Open a copy of `renders/_infinigen_living_room_regen_test/scene.blend`.
2. Select the deterministic shell set:
   - `living-room_0/0.wall`
   - `living-room_0/0.floor`
   - `living-room_0/0.ceiling`
   - `living-room_0/0.exterior`
3. Add candidate windows/doors from boundary-overlap checks.
4. Move the selection into `KA_EXPORT_living_room_0_0`.
5. Export a test GLB.
6. Validate in Blender and then in A-Frame before changing app runtime code.
