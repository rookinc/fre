# 07 G900 Envelope Workflow

Steward: ED

Status: Draft

## Purpose

This section documents the G900-facing Folded Receipt Envelope workflow.

It explains the meaning of the G900 protocol path without replacing the
contract, audit, receipt, fixture, or tool documentation. The goal is to show
how the G900 pieces walk together while preserving the claim boundary.

## Section scope

Owned scope:

- notes/g900_bounce_checkpoint_001.md
- notes/g900_native_generator_checkpoint_001.md
- notes/g900_recursive_host_checkpoint_001.md
- artifacts/json/fre_g900_payload_provenance_001.json
- docs/07-g900-envelope-workflow.md

Reference scope:

- fixtures/g900/
- contracts/fre_g900_*.json
- schemas/fre_g900_recursive_host_receipt_v0.1.schema.json
- artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json
- artifacts/json/fre_g900_structural_audit_001.json
- artifacts/json/fre_g900_checkpoint_audit_001.json
- artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json
- artifacts/json/fre_g900_native_generator_execution_audit_001.json
- artifacts/json/fre_g900_target_canonicalization_audit_001.json
- artifacts/json/fre_g900_generator_target_congruence_audit_001.json
- artifacts/json/fre_g900_sibling_negative_control_audit_001.json
- artifacts/json/fre_g900_bounce_reference_audit_001.json
- artifacts/json/fre_g900_bounce_negative_controls_audit_001.json
- tools/validate_g900_payload.py
- tools/emit_g900_status_receipt.py
- tools/generate_g900_kernel.py
- tools/canonicalize_g900_target.py
- tools/compare_g900_generator_target.py
- tools/generate_g900_sibling_control.py
- tools/run_g900_bounce_reference.py
- tools/run_g900_bounce_negative_controls.py
- tools/audit_g900_*.py

## Workflow principle

The G900 workflow is a sequence of bounded envelopes.

Each envelope records what is admitted, what is observed, what is rejected, and
what remains unavailable.

The G900 workflow does not allow structural pressure to become authorization.
The controlling rules are:

- No receipts, no true.
- Pressure exists, but pressure is not authorization.

## Three G900 paths

The current G900 workflow has three major paths:

- recursive-host checkpoint
- native-generator checkpoint
- bounce checkpoint

The recursive-host path records a candidate/local-chart declaration and an
unavailable status receipt.

The native-generator path records that a compact grammar reproduces the pinned
G900 carrier digest under a declared canonicalization discipline.

The bounce path records a bounded plaintext reference automaton and five
negative controls.

These paths support each other, but none of them promotes the others into an
unearned claim.

## G900 carrier grammar

The G900 carrier is organized as:

- G15 slots
- G60 local chambers
- signed carrier edges
- half-flip transport across signed carrier edges

The address rule is:

`vertex = 60 * slot + local`

The signed carrier rule is:

`local -> local + 30 * sign mod 60`

The validated structural carrier has:

- 900 vertices
- 3600 edges
- degree 8
- one connected component

Each G900 vertex has four internal G60 edges and four G15 carrier edges.

## Recursive-host checkpoint

The recursive-host checkpoint is documented in:

- notes/g900_recursive_host_checkpoint_001.md

It records the signed half-flip G900 carrier kernel:

`K900 = (G15, G60, sigma, h)`

The checkpoint declares candidate local host language, but recursive hosting
remains unavailable.

The current receipt records:

- structural payload validated
- cycle not admitted
- cycle not executed
- independent environment absent
- bridge unavailable
- trace congruence unavailable
- recursive-host claim unavailable
- closure open

This is a candidate/local-chart declaration. It is not a recursive-host theorem
and not an ordinary induced-subgraph claim.

## Payload provenance

The payload provenance artifact is:

- artifacts/json/fre_g900_payload_provenance_001.json

It pins the source payload and records that the source files are present and
hash-locked.

Its status is source payload pinned, not yet structurally validated. Later
audits validate structural properties and checkpoint the fail-closed state.

Payload provenance is source memory. It is not admission, execution, or a
receipt by itself.

## Native-generator checkpoint

The native-generator checkpoint is documented in:

- notes/g900_native_generator_checkpoint_001.md

It records that FRE can reconstruct the canonical 900-state carrier from a
compact grammar rather than treating the flattened 3600-edge table as the only
authority.

The native construction uses:

- the 30 edges of G15 = L(Petersen)
- the 120 local edges of G60
- the 30-edge canonical signing table

It produces:

- 900 vertices
- 1800 internal G60-fiber edges
- 1800 signed G15-carrier edges
- degree 8 at every vertex

## Independent comparison

The native generator was frozen before its first execution and was not allowed
to read the flattened G900 target.

The target canonicalizer read only the committed flat payload and could not
read the generator source, runtime capture, or generator audit.

A comparison tool then compared only the two locked audit artifacts.

The result is canonical edge digest congruence.

This is evidence that the compact product/signing law reproduces the pinned
carrier edge set under the declared canonical serialization.

It is not recursive-host admission, graph transport execution, observational
closure, or a universal theorem claim.

## Sibling negative control

The sibling negative control changes six G15 carrier signs while preserving the
same construction law.

The sibling graph preserves coarse counts:

- 900 vertices
- 3600 edges
- degree 8 everywhere
- one connected component

Its fixed-label digest separates from the canonical carrier digest.

This protects the native-generator result from being only a gross-count match.

The sibling control does not prove graph non-isomorphism by itself.

## Bounce checkpoint

The bounce checkpoint is documented in:

- notes/g900_bounce_checkpoint_001.md

It records one bounded plaintext reference automaton for cycle `t=0`.

The declared phase grammar is:

- 360 outward symbolic ticks
- 180 turnaround symbolic ticks
- 360 return symbolic ticks

The formal measure is:

`360 + 180 + 360 = 900`

This is a symbolic grammar. It is not a physical-angle claim and not a time
claim.

## Positive bounce result

The positive bounce reference run completed exactly once.

It records:

- source vertex 0
- target vertex 90
- 900 transitions
- 901 states
- G30 slip bit
- persistent G60 chamber lock
- return to source vertex 0
- final automaton state distinct from initial state
- plaintext receipt candidate I_0

`I_0` is a plaintext reference-receipt candidate. It is not a public
recursive-host receipt.

## Bounce negative controls

The bounce workflow includes five predeclared negative controls:

- wrong_phase_total
- receiptless_return
- wrong_half_flip
- alternate_edge
- unlocked_return

All five were rejected for their predeclared reasons. No control receipt was
emitted.

This protects the central rule that return to the same vertex is not
sufficient.

## G900 tool path

The G900 workflow uses tools for separate responsibilities:

- validate_g900_payload.py validates the imported payload surface.
- emit_g900_status_receipt.py emits the nonexecution unavailable status receipt.
- generate_g900_kernel.py runs the native generator path.
- canonicalize_g900_target.py canonicalizes the flat target path.
- compare_g900_generator_target.py compares locked digest artifacts.
- generate_g900_sibling_control.py runs the sibling negative-control path.
- run_g900_bounce_reference.py runs the positive bounce reference.
- run_g900_bounce_negative_controls.py runs the bounce negative controls.
- audit_g900_*.py records bounded audit artifacts.

The tool path is intentionally separated. No single tool silently earns the
whole claim.

## Claim boundary

The G900 workflow currently does not claim or admit:

- graph-payload transport
- graph transport execution
- recursive-host admission
- earned recursive-host receipt
- independent bridge
- ambient trace
- observational closure
- external truth
- physical interpretation
- physical angle or time
- geometry claim
- force claim
- graph non-isomorphism claim
- universal theorem claim

The current achievements are structural, canonical, negative-control, and
plaintext-reference achievements under bounded contracts.

## ED and SysOp split

The ED stewards the G900 workflow meaning and claim language.

The SysOp stewards the contracts, gates, fixtures, tools, receipts, audits, and
hash-bound evidence.

If the workflow meaning changes, the ED should update this section and the
checkpoint notes. If an executable path changes, the SysOp should update the
contract, gate, audit, fixture, or tool documentation.

## Boundary

This section documents the G900 envelope workflow only.

It does not run a G900 tool.

It does not admit recursive hosting.

It does not emit a new G900 receipt.

It does not consume a one-shot gate.

It does not modify the payload.

It does not create graph transport, observational closure, external truth,
physical interpretation, geometry, force, graph non-isomorphism, or a universal
theorem claim.
