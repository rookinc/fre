# 09 CLI, Build, and Test Surface

Steward: SysOp

Status: Draft

## Purpose

This section documents the buildable and executable surface of FRE.

It covers the CMake targets, command-line programs, source layout, test surface,
and generated build directories.

A compiled binary is capability. A contract or gate is authority. The SysOp
must keep those separate.

## Section scope

Owned scope:

- CMakeLists.txt
- include/fre/.gitkeep
- include/fre/openfhe_backend_status.hpp
- include/fre/openfhe_support_mode.hpp
- include/fre/support_mode.hpp
- src/backends/openfhe/.gitkeep
- src/backends/openfhe/openfhe_backend_status.cpp
- src/backends/openfhe/openfhe_support_mode.cpp
- src/cli/.gitkeep
- src/cli/fre_openfhe_status.cpp
- src/cli/fre_openfhe_support_mode_smoke.cpp
- src/cli/fre_support_reference.cpp
- src/support_mode_reference.cpp
- tests/.gitkeep
- build/
- build-openfhe-link/
- docs/09-cli-build-and-test-surface.md

Reference scope:

- contracts/
- tools/
- artifacts/json/
- artifacts/receipts/
- docs/06-support-mode-reference-system.md
- docs/08-openfhe-backend-boundary.md

## Source layout

The source tree is currently organized as:

- include/
- src/
- tests/

The public headers live under:

- include/fre/

The reference and backend implementation files live under:

- src/
- src/backends/openfhe/
- src/cli/

The tests folder currently contains only a placeholder.

Placeholder `.gitkeep` files preserve empty or transitional folders. They do
not have protocol meaning beyond keeping the directory structure present.

## CMake surface

The build system is declared in:

- CMakeLists.txt

The project uses C++17.

The OpenFHE backend is controlled by:

- FRE_ENABLE_OPENFHE
- FRE_OPENFHE_PREFIX

`FRE_ENABLE_OPENFHE` defaults to OFF.

When OpenFHE is enabled, `FRE_OPENFHE_PREFIX` is required and must point to the
durable OpenFHE installation prefix.

## Core targets

The base support mode targets are:

- fre_reference
- fre_support_reference

`fre_reference` is the static library for the plaintext support mode reference
calculation.

`fre_support_reference` is the CLI executable for the plaintext reference
pipeline.

## OpenFHE targets

When OpenFHE is enabled, the build adds:

- fre_openfhe_backend
- fre_openfhe_status
- fre_openfhe_support_mode_smoke

`fre_openfhe_backend` is the static backend library.

`fre_openfhe_status` reports backend availability, link status, profile pinning,
profile admission, crypto permission, and boundary.

`fre_openfhe_support_mode_smoke` runs the bounded OpenFHE support mode smoke
surface when admitted by gate.

The existence of these targets does not admit execution. The relevant contract
or gate still controls authority.

## Base test surface

The base build currently records four CTest tests:

- fre_reference_regular
- fre_reference_nonuniform
- fre_reference_scale_control
- fre_reference_reject_bad_count

The latest scanned `build/Testing/Temporary/LastTest.log` shows all four tests
passing.

The tests check:

- K equals 0 and regular is true for uniform input
- K equals 72 and regular is false for a nonuniform input
- K equals 288 and regular is false for a scale-control input
- bad argument count is rejected

## OpenFHE-link test surface

The OpenFHE-link build currently records five CTest tests:

- fre_reference_regular
- fre_reference_nonuniform
- fre_reference_scale_control
- fre_reference_reject_bad_count
- fre_openfhe_link_status

The latest scanned `build-openfhe-link/Testing/Temporary/LastTest.log` shows
all five tests passing.

The OpenFHE link-status test expects:

- linked true
- profile_admitted false
- crypto_allowed false

That is a fail-closed status check. It verifies link status without admitting
crypto execution.

## Generated build directories

The current generated build directories are:

- build/
- build-openfhe-link/

They contain CMake caches, CTest files, object files, executables, libraries,
and test logs.

These directories are operational evidence and local build products. They are
not the primary source of protocol authority.

The scanned CTest logs include generated paths from an earlier or alternate
repository location under `research/fre`. Treat those paths as generated build
metadata, not as the current project root.

## CLI behavior

The active CLI surfaces are:

- fre_support_reference
- fre_openfhe_status
- fre_openfhe_support_mode_smoke

`fre_support_reference` emits plaintext support mode JSON.

`fre_openfhe_status` emits OpenFHE backend status JSON.

`fre_openfhe_support_mode_smoke` emits bounded OpenFHE batch JSON.

CLI output may become audit input, but a CLI run does not automatically become
a public receipt.

## SysOp procedure

Before building or running, the SysOp should check:

1. Is this a base build or an OpenFHE-enabled build?
2. Is `FRE_ENABLE_OPENFHE` intended to be ON or OFF?
3. If OpenFHE is enabled, is `FRE_OPENFHE_PREFIX` correct?
4. Which target is being built?
5. Which binary is being run?
6. Does a contract or gate admit the run?
7. Is this only a status check, a reference check, a smoke execution, or an
   audit input?
8. Are generated build paths stale after a repo move?
9. Should build outputs be treated as local evidence rather than source?

## Boundary

This section documents the CLI, build, and test surface only.

It does not build the project.

It does not run tests.

It does not run any CLI.

It does not admit OpenFHE execution.

It does not emit receipts.

It does not make generated build products authoritative over contracts,
schemas, receipts, audits, or source files.

It does not create production security, observational closure, external truth,
physical interpretation, recursive host admission, graph transport, geometry,
force, or a universal theorem claim.
