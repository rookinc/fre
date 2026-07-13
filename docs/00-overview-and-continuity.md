# 00 Overview and Continuity

Steward: ED

Status: Draft

## Purpose

This section orients the Folded Receipt Envelope project.

It explains what FRE currently means, where the active continuity lives,
what boundaries are already declared, and where a SysOp should begin before
touching contracts, receipts, tools, fixtures, source code, or build outputs.

This section is intentionally high-level. Detailed authority belongs in the
contract documents. Detailed execution truth belongs in receipts and audits.

## Current name

FRE currently means Folded Receipt Envelope.

Older continuity language may refer to FRE as the Finite Receipt Engine. In
the current protocol framing, Folded Receipt Envelope is the preferred name.
Older language is treated as historical or operational language unless the ED
promotes it again by explicit decision.

## Working definition

A Folded Receipt Envelope is a bounded protocol packet that joins source
material, admission rules, execution limits, and receipt expectations in one
inspectable form.

The envelope does not make an action true.

The envelope makes the action accountable.

## Section scope

Owned scope:

- README.md
- fre_continuity.md
- notes/boundary.md
- notes/fre_local_milestone_progress_report_001.md
- docs/00-overview-and-continuity.md

Reference scope:

- contracts/
- schemas/
- artifacts/
- fixtures/
- include/
- src/
- tools/
- notes/
- CMakeLists.txt
- build/
- build-openfhe-link/

The reference scope is named here so the ED and SysOp can see the full project
surface. The individual files in those folders are documented in later sections.

## Project surface

The current repository surface contains:

- contracts
- schemas
- receipts
- audit artifacts
- fixtures
- reference implementation code
- OpenFHE backend code
- command-line tools
- checkpoint notes
- continuity notes
- build outputs

The intended future shape may change during repo reshuffling. Until then, this
document treats the current file tree as the active map.

## Active checkpoints

The current README records several active checkpoints:

- local OpenFHE support-mode throughline
- fail-closed G900 carrier checkpoint
- native G900 generator checkpoint
- G900 bounce checkpoint

The OpenFHE support-mode throughline completed one admitted local batch. The
encrypted outputs matched the plaintext reference for the admitted fixture set.
This remains local closure, not observational closure, production security, or
external truth.

The G900 work contains structural and receipt checkpoints. These checkpoints
record bounded carrier, generator, recursive-host, and bounce work. They do not
admit graph transport, recursive hosting, observational closure, physics,
geometry, force, or universal theorem claims.

## Boundary summary

The project boundary is conservative.

FRE may define public contracts, receipt schemas, operation names, source-class
identifiers, encoding declarations, tolerance declarations, verification status,
negative-control status, and claim-relative results permitted by contract.

FRE must not commit or expose runtime-only private body material such as secret
inputs, secret keys, ciphertexts, raw OpenFHE runtime objects, or undeclared
intermediate values.

FRE does not currently claim:

- production cryptographic security
- observational closure
- external truth
- physical interpretation
- global support-chamber closure
- recursive host admission
- unbounded backend adoption
- arbitrary support-register certification

## Steward roles

The ED stewards meaning, scope, continuity, claim language, and project
direction.

The SysOp stewards operational truth, contracts, gates, receipts, audits,
fixtures, tool execution, builds, and repository hygiene.

For now, these two roles are enough. New roles should not be invented until a
repeated responsibility clearly needs a separate steward.

## SysOp start point

A SysOp should begin each work session by reading:

1. fre_continuity.md
2. README.md
3. notes/boundary.md
4. the most relevant checkpoint note under notes/
5. the contract or gate for the intended action
6. the expected receipt schema
7. the relevant audit tool

The SysOp should not run an action merely because a tool exists. The action
must be admitted by a contract or gate.

## Documentation rule

Notes may guide action.

Contracts admit action.

Receipts record action.

Audits check action.

Continuity preserves orientation.

This overview does not admit new behavior. It only names the current map.
