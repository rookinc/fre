# 04 Audit Layer

Steward: SysOp

Status: Draft

## Purpose

This section documents the FRE audit layer.

Audits check whether a Folded Receipt Envelope event held its declared
boundary. They inspect contracts, gates, runtime captures, receipts, fixtures,
source files, schemas, digests, and expected results.

An audit pass means the declared audit passed. It does not automatically
promote a broader claim.

## Section scope

Owned scope:

- tools/audit_g900_bounce_negative_controls.py
- tools/audit_g900_bounce_reference.py
- tools/audit_g900_checkpoint.py
- tools/audit_g900_generator_target_congruence.py
- tools/audit_g900_native_generator_checkpoint.py
- tools/audit_g900_native_generator_execution.py
- tools/audit_g900_sibling_negative_control.py
- tools/audit_g900_target_canonicalization.py
- tools/audit_openfhe_execution.py
- tools/audit_openfhe_link_status.py
- tools/audit_openfhe_receipts.py
- tools/audit_reference_fixtures.py
- artifacts/json/fre_g900_bounce_negative_controls_audit_001.json
- artifacts/json/fre_g900_bounce_reference_audit_001.json
- artifacts/json/fre_g900_checkpoint_audit_001.json
- artifacts/json/fre_g900_generator_target_congruence_audit_001.json
- artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json
- artifacts/json/fre_g900_native_generator_execution_audit_001.json
- artifacts/json/fre_g900_sibling_negative_control_audit_001.json
- artifacts/json/fre_g900_structural_audit_001.json
- artifacts/json/fre_g900_target_canonicalization_audit_001.json
- artifacts/json/fre_openfhe_link_status_audit_001.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json
- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_002.json
- docs/04-audit-layer.md

Reference scope:

- contracts/
- schemas/
- artifacts/receipts/
- fixtures/
- src/
- include/
- CMakeLists.txt
- build/
- build-openfhe-link/

## Audit principle

An audit is a bounded check.

It asks whether a specific declared event, artifact, or relationship satisfied
the declared conditions. It does not ask whether the whole research program is
true.

The SysOp should treat every audit as local unless the artifact explicitly
admits a wider scope.

## Common audit fields

Current audit artifacts are not all the same shape, but many include:

- artifact_id
- status
- verdict
- audit_pass
- bindings
- checks
- boundary
- claim_boundary
- run
- result
- receipt_policy

The field `audit_pass: true` means the audit's own checks passed. It does not
erase the boundary fields.

## Digest binding

Many audit tools lock expected file hashes.

This makes the audit layer a digest-binding layer as well as a logical check.
The audit may verify that the contract, gate, source tool, schema, fixture,
runtime capture, or previous artifact is exactly the version expected.

If a locked digest changes, the SysOp should not quietly rerun and overwrite the
audit. The changed file needs a new reason, new audit, or explicit repair path.

## Runtime captures

Some audits consume runtime captures from `$HOME/tmp/...`.

Those captures are operational evidence. They are usually not committed
directly. The audit decides what public artifact can be written into
`artifacts/json/`.

This preserves the split between runtime body and public face.

## Audit is not receipt

A receipt records an envelope event.

An audit checks whether an event, receipt, or artifact held its declared
boundary.

For example, the OpenFHE execution audit records that bounded encrypted outputs
matched the plaintext reference. The receipt audit then checks schema-bound
receipt congruence for the bounded local batch. These are connected but not the
same layer.

## Support mode audit family

The support mode audit family includes:

- tools/audit_reference_fixtures.py
- tools/audit_openfhe_link_status.py
- tools/audit_openfhe_execution.py
- tools/audit_openfhe_receipts.py
- artifacts/json/fre_support_mode_reference_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_002.json
- artifacts/json/fre_openfhe_link_status_audit_001.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json
- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json

The reference audits check the plaintext support-mode reference pipeline against
predeclared fixtures and contract revisions.

The OpenFHE link audit verifies a fail-closed linked target. It records that the
backend is available and linked, while crypto remains closed.

The OpenFHE execution audit records the bounded local execution matching the
plaintext reference.

The OpenFHE receipt audit records schema-bound receipt congruence for the
bounded local batch.

Support mode audit boundaries preserve:

- no production security claim
- no physical claim
- no observational closure
- no unbounded OpenFHE backend adoption
- no receipt congruence until the receipt audit establishes it

## G900 structural and checkpoint audits

The G900 structural/checkpoint audit family includes:

- tools/audit_g900_checkpoint.py
- tools/audit_g900_native_generator_checkpoint.py
- artifacts/json/fre_g900_structural_audit_001.json
- artifacts/json/fre_g900_checkpoint_audit_001.json
- artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json

These audits record fail-closed structural checkpoints.

They validate structural carrier or generator conditions while preserving the
boundary that recursive host admission, transport execution, observational
closure, and universal theorem claims remain false.

## G900 native generator audits

The G900 native generator audit family includes:

- tools/audit_g900_native_generator_execution.py
- tools/audit_g900_target_canonicalization.py
- tools/audit_g900_generator_target_congruence.py
- tools/audit_g900_sibling_negative_control.py
- artifacts/json/fre_g900_native_generator_execution_audit_001.json
- artifacts/json/fre_g900_target_canonicalization_audit_001.json
- artifacts/json/fre_g900_generator_target_congruence_audit_001.json
- artifacts/json/fre_g900_sibling_negative_control_audit_001.json

This family separates generator execution, target canonicalization, digest
comparison, and sibling negative control.

The generator execution audit records locked primitives and expected G900
invariants before target comparison.

The target canonicalization audit records the flat G900 target independently.

The congruence audit records native-generator to flat-target canonical digest
congruence.

The sibling negative control audit records that a six-toggle sibling preserves
gross invariants while separating the fixed-label digest.

The boundary remains structural. These audits do not admit recursive hosting,
transport execution, observational closure, or external truth.

## G900 bounce audits

The G900 bounce audit family includes:

- tools/audit_g900_bounce_reference.py
- tools/audit_g900_bounce_negative_controls.py
- artifacts/json/fre_g900_bounce_reference_audit_001.json
- artifacts/json/fre_g900_bounce_negative_controls_audit_001.json

The reference audit records the one-shot plaintext G900 bounce reference.

The negative-control audit records that all five predeclared bounce negative
controls were rejected without receipts.

This family protects the claim boundary that return to the same vertex is not
sufficient. It does not admit graph transport execution, recursive hosting,
observational closure, public receipt emission, or a physical claim.

## Audit pass interpretation

When an audit passes, read both the verdict and the boundary.

Examples:

- `bounded_openfhe_execution_matches_plaintext_reference` means the bounded
  execution matched the plaintext reference under the declared local profile.
- `schema_bound_receipt_congruence_for_bounded_local_batch` means the receipt
  set passed the schema-bound receipt audit.
- `native_generator_reproduces_pinned_G900_canonical_edge_digest` means digest
  congruence was recorded, not recursive host admission.
- `five_predeclared_bounce_negative_controls_rejected_without_receipts` means
  the negative controls rejected as intended.

The verdict is the result. The boundary is the fence around the result.

## SysOp audit procedure

Before relying on an audit, the SysOp should check:

1. Which tool produced the audit?
2. Which artifact did it write?
3. Which contracts, gates, schemas, fixtures, tools, or captures were hash-bound?
4. Was `audit_pass` true?
5. What exact verdict was recorded?
6. What checks passed?
7. Which boundary or claim_boundary fields remain false?
8. Does a later audit depend on this artifact?
9. Is the audit local, structural, receipt-level, or checkpoint-level?
10. Has any bound file changed since the audit?

## Boundary

This section documents the audit layer only.

It does not run an audit.

It does not modify audit artifacts.

It does not validate receipts.

It does not emit receipts.

It does not consume any gate.

It does not promote structural validation to recursive host admission.

It does not promote local OpenFHE execution to production security.

It does not create observational closure, external truth, physical
interpretation, geometry, force, transport execution, or a universal theorem
claim.
