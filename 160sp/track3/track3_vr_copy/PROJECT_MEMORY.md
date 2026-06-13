# PROJECT MEMORY

## Project Name

COGS 160 Track 3 VR Studio

---

## Context

This repository is a focused implementation extracted from a larger UCSD COGS 160 Track 3 project.

The original Track 3 effort explored procedural room generation using Infinigen and Blender.

However, the actual course objective is not procedural generation itself.

The goal is to build a system that allows undergraduate students to create environmental psychology experiments in virtual interiors.

---

## Problem Statement

Students with little or no VR development experience should be able to:

1. Select a room.
2. Modify room variables.
3. Create a Control condition.
4. Create one or more Treatment conditions.
5. Compare conditions.
6. Run conditions in WebXR.

The system should support reproducible virtual stimuli.

---

## Current Scope

This repository focuses ONLY on:

* Living Room
* Bedroom

These were the originally assigned room types.

Do not expand scope unless explicitly requested.

---

## Project Vision

This is NOT:

* an Infinigen GUI
* a Blender GUI
* a procedural generation research project
* a CAD tool
* an architectural design application

This IS:

A web-based experiment authoring platform.

Students should never need to understand:

* Infinigen
* Blender
* procedural generation
* JSON schemas

The interface should remain beginner-friendly.

---

## Core User Flow

Student opens the application.

↓

Selects:

* Living Room
  or
* Bedroom

↓

Modifies environmental variables.

↓

Saves current state as Control.

↓

Duplicates Control into Treatment.

↓

Changes one variable.

↓

System displays changed variables.

↓

Student compares conditions.

↓

Student launches condition in A-Frame/WebXR.

---

## MVP Definition

The MVP is complete when a student can:

1. Select Living Room or Bedroom.
2. Modify parameters.
3. Save a Control condition.
4. Create a Treatment condition.
5. See parameter differences.
6. Load the room in A-Frame.
7. Save and reload experiments.

---

## Room Parameters

### Live Parameters

Can update immediately.

Examples:

* Brightness
* Warmth

### Cached Variant Parameters

Switch between pre-generated assets.

Examples:

* Furniture Density
* Plant Count

### Regeneration Parameters

Require asset regeneration.

Examples:

* Ceiling Height
* Room Dimensions
* Room Shape
* Window Count

The system must never fake geometry changes.

---

## Architecture

Student UI

↓

Room Catalog

↓

Room Definition

↓

Parameter Editor

↓

Experiment Builder

↓

Diff Viewer

↓

A-Frame Runtime

↓

Save / Load

---

## Experiment Model

Each experiment contains:

* exactly one Control condition
* one or more Treatment conditions

Each condition stores:

* room id
* parameter values
* metadata
* asset reference

---

## Diff System

The system should identify:

* changed variables
* unchanged variables
* possible confounds

Example:

Control

Brightness = 50

Treatment

Brightness = 70

Output:

Changed Variables:
✓ Brightness

No Confounds

---

## Runtime

Canonical runtime:

A-Frame + WebXR

Minimum support:

* desktop browser
* WASD movement
* room loading
* condition loading

Optional:

* VR headset support

---

## Infinigen

Infinigen is NOT the product.

Infinigen is a backend asset-generation tool.

Current repository includes:

* manifests
* parameter files
* Infinigen wrapper
* generated room assets

Use these when useful.

However:

The MVP must remain functional even if Infinigen generation is unavailable.

---

## Existing Repository Assets

Current repository already contains:

* manifests/
* params/
* infinigen_wrapper.py
* living room definitions
* bedroom definitions

Review these before creating new files.

Reuse whenever possible.

Avoid duplicate definitions.

---

## Immediate Goal

Deadline: Tomorrow at 1:00 PM.

Deliver a working MVP demonstrating:

* Living Room
* Bedroom
* Room Picker
* Parameter Editor
* Control/Treatment workflow
* Diff Viewer
* A-Frame Viewer
* Save/Load

Prioritize functionality over visual polish.

---

## Development Rules

Before writing code:

1. Inspect repository structure.
2. Reuse existing files.
3. Explain planned changes.
4. Then implement.

Always prefer:

working MVP

over

perfect architecture.

---

## Success Criteria

By demo time, the following workflow must work:

Select Living Room

↓

Adjust Brightness

↓

Save as Control

↓

Duplicate as Treatment

↓

Change Brightness

↓

View Diff

↓

Launch Control

↓

Launch Treatment

↓

Compare Conditions

If this workflow works, the MVP is successful.
