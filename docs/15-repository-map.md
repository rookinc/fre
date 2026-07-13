# 15 Repository Map

Steward: SysOp

Status: Draft

## Purpose

This section maps the FRE repository.

It exists to make sure every top-level file and folder has a documented role,
even while the repository is expected to be reshuffled later.

If a new top-level file or folder appears, assign it here or in a successor map.

## Section scope

Owned scope:

- .
- CMakeLists.txt
- README.md
- artifacts/
- artifacts/json/
- artifacts/receipts/
- build/
- build-openfhe-link/
- contracts/
- fixtures/
- fixtures/g900/
- fixtures/json/
- fre_continuity.md
- include/
- include/fre/
- notes/
- schemas/
- src/
- src/backends/
- src/backends/openfhe/
- src/cli/
- tests/
- tools/
- docs/
- docs/15-repository-map.md

## Root

The repository root contains the protocol source, public documentation,
contracts, schemas, fixtures, tools, artifacts, notes, source code, and local
build surfaces.

Root-level files:

- CMakeLists.txt
- README.md
- fre_continuity.md

Root-level folders:

- artifacts/
- build/
- build-openfhe-link/
- contracts/
- docs/
- fixtures/
- include/
- notes/
- schemas/
- src/
- tests/
- tools/

## CMakeLists.txt

Role: build declaration.

It defines the C++17 project, base reference targets, optional OpenFHE targets,
and CTest entries.

Primary documentation:

- docs/09-cli-build-and-test-surface.md

## README.md

Role: public orientation surface.

It introduces FRE, first target, architecture, current status, OpenFHE
throughline, and G900 checkpoints.

Primary documentation:

- docs/00-overview-and-continuity.md
- docs/11-notes-and-human-checkpoints.md

## fre_continuity.md

Role: SysOp continuity briefing.

It preserves operational state, mission, architecture, milestones, invariants,
priorities, and responsibilities.

Primary documentation:

- docs/00-overview-and-continuity.md
- docs/11-notes-and-human-checkpoints.md
- docs/13-sysop-runbook.md

## artifacts/

Role: committed evidence surface.

Subfolders:

- artifacts/json/
- artifacts/receipts/

Primary documentation:

- docs/03-receipts-and-schemas.md
- docs/04-audit-layer.md
- docs/12-artifact-index.md

## artifacts/json/

Role: JSON evidence artifacts.

Contains audit artifacts, provenance artifacts, checkpoint artifacts, execution
artifacts, link-status artifacts, and receipt-audit artifacts.

Primary documentation:

- docs/04-audit-layer.md
- docs/12-artifact-index.md

## artifacts/receipts/

Role: public receipt artifacts.

Contains G900 unavailable status receipt and support mode regularity receipts.

Primary documentation:

- docs/03-receipts-and-schemas.md
- docs/12-artifact-index.md

## build/

Role: generated base build directory.

Contains CMake cache, object files, executable outputs, library outputs, CTest
files, and test logs for the base reference build.

Primary documentation:

- docs/09-cli-build-and-test-surface.md

Boundary: generated operational evidence, not source authority.

## build-openfhe-link/

Role: generated OpenFHE-link build directory.

Contains CMake cache, object files, executable outputs, library outputs, CTest
files, and test logs for the OpenFHE-linked build.

Primary documentation:

- docs/08-openfhe-backend-boundary.md
- docs/09-cli-build-and-test-surface.md

Boundary: link capability is not execution authority.

## contracts/

Role: authority layer.

Contains contracts and gates for support mode, OpenFHE execution, G900 native
generator work, G900 recursive-host status, G900 target canonicalization,
G900 sibling controls, and G900 bounce work.

Primary documentation:

- docs/02-contracts-and-gates.md

## docs/

Role: structured documentation.

Contains the numbered documentation spine.

Primary documentation:

- docs/README.md once created
- docs/00-overview-and-continuity.md
- docs/15-repository-map.md

## fixtures/

Role: source, target, and control material.

Subfolders:

- fixtures/g900/
- fixtures/json/

Primary documentation:

- docs/05-fixtures-and-source-material.md

## fixtures/g900/

Role: G900 fixture family.

Contains G15 slot edges, G60 local edges, canonical carrier signing, flattened
target edges, sibling signing controls, and sibling target/control edges.

Primary documentation:

- docs/05-fixtures-and-source-material.md
- docs/07-g900-envelope-workflow.md

## fixtures/json/

Role: JSON fixture family.

Contains the support mode fixture set and folder placeholder.

Primary documentation:

- docs/05-fixtures-and-source-material.md
- docs/06-support-mode-reference-system.md

## include/

Role: public C++ header surface.

Subfolder:

- include/fre/

Primary documentation:

- docs/06-support-mode-reference-system.md
- docs/08-openfhe-backend-boundary.md
- docs/09-cli-build-and-test-surface.md

## include/fre/

Role: FRE public C++ API headers.

Contains support mode and OpenFHE boundary headers plus placeholder.

Primary documentation:

- docs/06-support-mode-reference-system.md
- docs/08-openfhe-backend-boundary.md

## notes/

Role: human-readable checkpoint and boundary notes.

Contains boundary note, milestone report, G900 checkpoint notes, and OpenFHE
throughline.

Primary documentation:

- docs/11-notes-and-human-checkpoints.md

## schemas/

Role: receipt schema layer.

Contains JSON schemas for support mode receipts and G900 recursive-host
receipts.

Primary documentation:

- docs/03-receipts-and-schemas.md

## src/

Role: implementation source.

Contains the plaintext support mode reference implementation, CLI programs, and
OpenFHE backend source.

Primary documentation:

- docs/06-support-mode-reference-system.md
- docs/08-openfhe-backend-boundary.md
- docs/09-cli-build-and-test-surface.md

## src/backends/

Role: backend implementation namespace.

Subfolder:

- src/backends/openfhe/

Primary documentation:

- docs/08-openfhe-backend-boundary.md
- docs/09-cli-build-and-test-surface.md

## src/backends/openfhe/

Role: OpenFHE backend implementation.

Contains backend status and support mode OpenFHE implementation plus placeholder.

Primary documentation:

- docs/08-openfhe-backend-boundary.md

## src/cli/

Role: command-line executable source.

Contains support reference CLI, OpenFHE status CLI, OpenFHE support mode smoke
CLI, and placeholder.

Primary documentation:

- docs/09-cli-build-and-test-surface.md

## tests/

Role: future test source folder.

Currently contains a placeholder.

CTest entries are currently declared in CMakeLists.txt rather than this folder.

Primary documentation:

- docs/09-cli-build-and-test-surface.md

## tools/

Role: operational Python tool surface.

Contains validators, generators, canonicalizers, comparators, emitters, gate
preparation tools, profile pinning tools, run tools, and audit tools.

Primary documentation:

- docs/10-tool-index.md

## Reshuffle rule

The repository may be reshuffled later.

When that happens:

1. Update this repository map.
2. Update docs/README.md.
3. Update section scopes in affected docs.
4. Keep contracts, receipts, audits, and artifact references stable or provide
   explicit migration notes.
5. Do not rewrite history by making old artifact paths appear as if they were
   always new paths.

## Boundary

This section maps the repository only.

It does not move files.

It does not modify contracts, receipts, artifacts, tools, fixtures, source, or
build outputs.

It does not admit execution.

It does not create production security, observational closure, external truth,
recursive-host admission, graph transport, physical interpretation, geometry,
force, or a universal theorem claim.
