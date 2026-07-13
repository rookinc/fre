# 12 Artifact Index

Steward: SysOp

Status: Draft

## Purpose

This section indexes FRE artifacts.

Artifacts are committed evidence surfaces. They include audits, provenance
records, execution summaries, link-status records, receipt audits, and public
receipts.

Artifacts are not all the same kind of truth. The SysOp must distinguish audit
artifacts from receipt artifacts, provenance artifacts, execution artifacts,
and checkpoint artifacts.

## Section scope

Owned scope:

- artifacts/json/fre_g900_bounce_negative_controls_audit_001.json
- artifacts/json/fre_g900_bounce_reference_audit_001.json
- artifacts/json/fre_g900_checkpoint_audit_001.json
- artifacts/json/fre_g900_generator_target_congruence_audit_001.json
- artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json
- artifacts/json/fre_g900_native_generator_execution_audit_001.json
- artifacts/json/fre_g900_payload_provenance_001.json
- artifacts/json/fre_g900_sibling_negative_control_audit_001.json
- artifacts/json/fre_g900_structural_audit_001.json
- artifacts/json/fre_g900_target_canonicalization_audit_001.json
- artifacts/json/fre_openfhe_durable_prefix_001.json
- artifacts/json/fre_openfhe_executed_profile_provenance_001.json
- artifacts/json/fre_openfhe_link_status_audit_001.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json
- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_002.json
- artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_10_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_20_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_10_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_20_001.json
- docs/12-artifact-index.md

Reference scope:

- contracts/
- schemas/
- fixtures/
- tools/
- notes/

## Artifact principle

Artifacts are committed memory.

They should be finite, inspectable, hashable, and tied to contracts, gates,
tools, fixtures, schemas, receipts, or runtime captures.

An artifact should not be treated as stronger than its own boundary. The
artifact verdict and the artifact boundary must be read together.

## Artifact folders

FRE currently has two artifact folders:

- artifacts/json/
- artifacts/receipts/

`artifacts/json/` contains audits, provenance records, checkpoint records,
execution summaries, and link-status records.

`artifacts/receipts/` contains public receipt artifacts.

## Provenance artifacts

Current provenance artifacts include:

- artifacts/json/fre_g900_payload_provenance_001.json
- artifacts/json/fre_openfhe_durable_prefix_001.json
- artifacts/json/fre_openfhe_executed_profile_provenance_001.json

These artifacts record source memory, durable toolchain state, or imported
profile provenance.

They do not automatically admit execution.

## Support mode reference artifacts

Current support mode reference artifacts include:

- artifacts/json/fre_support_mode_reference_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_002.json

These artifacts record plaintext reference behavior and contract rebinding.

They are reference-pipeline evidence, not OpenFHE execution receipts.

## OpenFHE artifacts

Current OpenFHE artifacts include:

- artifacts/json/fre_openfhe_link_status_audit_001.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json
- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json

The link-status audit records fail-closed OpenFHE linkage.

The execution audit records bounded local OpenFHE execution matching the
plaintext reference.

The receipt audit records schema-bound receipt congruence for the bounded local
batch.

## Support mode receipt artifacts

Current support mode receipt artifacts include:

- artifacts/receipts/fre_support_mode_receipt_regular_uniform_10_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_20_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_10_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_20_001.json

The two regular uniform receipts carry earned regularity true claims.

The two balanced exchange receipts carry unavailable regularity claims.

All four remain local-profile receipts with no production security or
observational closure claim.

## G900 structural artifacts

Current G900 structural artifacts include:

- artifacts/json/fre_g900_payload_provenance_001.json
- artifacts/json/fre_g900_structural_audit_001.json
- artifacts/json/fre_g900_checkpoint_audit_001.json

These artifacts record pinned payload provenance, structural validation, and a
fail-closed recursive-host checkpoint.

They do not admit recursive hosting.

## G900 native generator artifacts

Current G900 native generator artifacts include:

- artifacts/json/fre_g900_native_generator_execution_audit_001.json
- artifacts/json/fre_g900_target_canonicalization_audit_001.json
- artifacts/json/fre_g900_generator_target_congruence_audit_001.json
- artifacts/json/fre_g900_sibling_negative_control_audit_001.json
- artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json

Together these record generator execution, independent target
canonicalization, digest congruence, sibling negative control, and checkpoint
closure.

They establish bounded structural reproduction under the declared digest
discipline. They do not establish recursive hosting, graph transport,
observational closure, or graph non-isomorphism.

## G900 bounce artifacts

Current G900 bounce artifacts include:

- artifacts/json/fre_g900_bounce_reference_audit_001.json
- artifacts/json/fre_g900_bounce_negative_controls_audit_001.json

The positive reference audit records the one-shot plaintext bounce reference.

The negative-control audit records five rejected controls and no control
receipts.

These artifacts protect the rule that same-vertex return is not sufficient.

## G900 receipt artifacts

Current G900 receipt artifacts include:

- artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json

This is a nonexecution unavailable status receipt.

It is not a G900 execution receipt. It is not recursive-host admission.

## SysOp artifact check

Before relying on an artifact, the SysOp should check:

1. What kind of artifact is it?
2. Which contract, gate, schema, fixture, tool, or runtime capture produced it?
3. Does it have an artifact_id or receipt envelope_id?
4. Does it record audit_pass?
5. What verdict or claim status does it record?
6. What boundary remains false?
7. Does a later artifact depend on it?
8. Has any bound source file changed?

## Boundary

This section indexes artifacts only.

It does not create, modify, validate, or emit artifacts.

It does not rerun audits.

It does not emit receipts.

It does not promote unavailable claims to earned claims.

It does not create production security, observational closure, external truth,
recursive-host admission, graph transport, physical interpretation, geometry,
force, or a universal theorem claim.
