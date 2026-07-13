# 11 Notes and Human Checkpoints

Steward: ED

Status: Draft

## Purpose

This section documents FRE's human-readable notes and checkpoint surfaces.

Notes preserve meaning, sequence, interpretation, and operational memory. They
help the ED and SysOp understand where the project is and why the next action
is bounded the way it is.

Notes may guide action. Contracts admit action. Receipts record action. Audits
check action.

## Section scope

Owned scope:

- README.md
- fre_continuity.md
- notes/boundary.md
- notes/fre_local_milestone_progress_report_001.md
- notes/g900_bounce_checkpoint_001.md
- notes/g900_native_generator_checkpoint_001.md
- notes/g900_recursive_host_checkpoint_001.md
- notes/openfhe_support_mode_throughline_001.md
- docs/11-notes-and-human-checkpoints.md

Reference scope:

- docs/
- contracts/
- schemas/
- artifacts/
- fixtures/
- tools/
- include/
- src/

## Note principle

A note is not an authority surface by itself.

A note can explain a contract, summarize an audit, preserve a boundary, or
describe a completed checkpoint. It should not silently admit a new execution,
change a claim boundary, or replace a receipt.

If a note and a contract disagree, the SysOp should pause and resolve the
conflict before running anything.

## README

The root README is the current public orientation surface.

It identifies FRE as a B32K Folded Receipt Envelope research implementation and
summarizes:

- first target
- architecture
- current status
- completed local OpenFHE throughline
- fail-closed G900 carrier checkpoint
- native G900 generator checkpoint
- G900 bounce checkpoint

The README is the front door. It should stay short enough to orient a reader
without becoming the full manual.

## Continuity

The continuity file is:

- fre_continuity.md

It is the SysOp continuity briefing. It preserves mission, current state,
architecture, completed milestones, invariants, priorities, and operating
responsibilities.

Current caution: this file uses older language that expands FRE as Finite
Receipt Engine. The current preferred expansion is Folded Receipt Envelope.
Treat the older phrase as historical or operational language unless the ED
promotes it again.

## Boundary note

The boundary note is:

- notes/boundary.md

It is the compact claim fence for the project.

It records:

- allowed project work
- private body material that must not be committed
- public face material that may be exposed
- claim boundaries

This note is a quick check before public writing, execution planning, or
repository reshuffling.

## Local milestone report

The local milestone report is:

- notes/fre_local_milestone_progress_report_001.md

It is the long-form history of the completed local OpenFHE support-mode
throughline.

It records the path from scaffold to bounded, contract-governed homomorphic
computation with public, schema-validated receipts.

It covers:

- research synthesis
- phase history
- implemented encrypted circuit
- observed execution
- receipt results
- evidence and privacy model
- engineering incidents and repairs
- current boundary
- milestone conclusion

This report is historical synthesis. It does not admit future execution.

## OpenFHE throughline note

The OpenFHE throughline note is:

- notes/openfhe_support_mode_throughline_001.md

It summarizes the completed local OpenFHE support-mode path.

It records that the encrypted pipeline and plaintext reference pipeline agreed
exactly on four admitted public fixtures:

- regular_uniform_10
- regular_uniform_20
- balanced_exchange_10
- balanced_exchange_20

It also records the claim split:

- two certified uniform fixtures earned regularity true
- two balanced exchange controls remained regularity unavailable

Its key boundary is that closure is local, not observational. No external truth,
production security, or physical claim is established.

## G900 recursive-host checkpoint note

The recursive-host checkpoint note is:

- notes/g900_recursive_host_checkpoint_001.md

It records the signed half-flip G900 carrier kernel:

`K900 = (G15, G60, sigma, h)`

It explains the baked-in structure, cycle grammar, recursive-host declaration,
current unavailable receipt, and boundary.

Its core meaning is that structural carrier validation exists, but recursive
hosting remains unavailable.

## G900 native-generator checkpoint note

The native-generator checkpoint note is:

- notes/g900_native_generator_checkpoint_001.md

It records the compact construction of the canonical 900-state carrier from:

- G15 edges
- G60 local edges
- canonical signing table

It explains the independent comparison path and sibling negative control.

Its core meaning is that native generator digest congruence was recorded, while
recursive hosting, graph transport, observational closure, graph
non-isomorphism, and universal theorem claims remain closed.

## G900 bounce checkpoint note

The bounce checkpoint note is:

- notes/g900_bounce_checkpoint_001.md

It records one bounded plaintext reference automaton for cycle `t=0`.

It summarizes:

- formal phase grammar 360 + 180 + 360 = 900
- positive reference result
- plaintext receipt candidate I_0
- five negative controls
- claim boundary

Its core meaning is that return to the same vertex is not sufficient. The
negative controls rejected as intended and no control receipt was emitted.

## How notes should be updated

When updating notes, preserve:

- contract IDs
- gate IDs
- artifact IDs
- receipt IDs
- hashes when they are part of the evidence
- exact boundary language
- unavailable versus earned distinction
- local versus observational closure distinction

Do not update notes in a way that makes a stronger claim than the underlying
contract, receipt, or audit permits.

## ED and SysOp split

The ED stewards human meaning, public orientation, continuity language, and
claim framing.

The SysOp stewards whether the notes still match contracts, receipts, audits,
fixtures, tools, and build evidence.

A note can say what the project means. The SysOp should verify whether the
system actually recorded it.

## Boundary

This section documents notes and human checkpoints only.

It does not modify any note other than this documentation file.

It does not admit execution.

It does not emit receipts.

It does not pass audits.

It does not promote historical language into current authority.

It does not create production security, observational closure, external truth,
recursive-host admission, graph transport, physical interpretation, geometry,
force, or a universal theorem claim.
