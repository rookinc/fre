# 03 Receipts and Schemas

Steward: SysOp

Status: Draft

## Purpose

This section documents the receipt and schema layer of FRE.

Receipts are the public memory of Folded Receipt Envelope events. Schemas define
the closed shape that a valid receipt must satisfy.

A receipt does not make a global claim true. A receipt records a bounded event
under a declared contract, gate, comparison rule, privacy rule, closure class,
and boundary.

## Section scope

Owned scope:

- schemas/fre_g900_recursive_host_receipt_v0.1.schema.json
- schemas/fre_support_mode_receipt_v0.1.schema.json
- schemas/fre_support_mode_receipt_v0.2.schema.json
- artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_10_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_20_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_10_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_20_001.json
- docs/03-receipts-and-schemas.md

Reference scope:

- contracts/
- artifacts/json/
- tools/audit_openfhe_receipts.py
- tools/emit_openfhe_receipts.py
- tools/emit_g900_status_receipt.py

## Schema principle

Schemas are the shape law for receipts.

The current schemas use closed JSON shapes with `additionalProperties: false`.
That means a receipt must stay inside the declared structure. Extra fields are
not casually accepted.

This matters because a receipt is a public claim surface. Undeclared fields can
smuggle meaning, authority, or private material into public output.

## Current schema families

The current schema families are:

- support mode receipt schema v0.1
- support mode receipt schema v0.2
- G900 recursive host receipt schema v0.1

The support mode schemas shape regularity receipts for the support-mode
polynomial pipeline.

The G900 recursive host schema shapes nonexecution or future recursive-host
receipts, with strict conditions around bridge, host, claim, closure, privacy,
and boundary.

## Common receipt fields

Important receipt fields include:

- receipt_schema
- envelope_id
- contract_id
- contract_sha256
- source_class
- input_certification
- circuit_id
- operation_names
- gate
- claim
- comparison
- controls
- privacy
- closure
- boundary

Not every receipt family uses every field. The SysOp should inspect the schema
before treating a receipt as valid.

## Claim statuses

FRE receipts distinguish earned claims from unavailable or rejected claims.

For support mode receipts:

- `earned` carries a boolean result.
- `unavailable` carries a null result.
- `rejected` carries a null result.

The distinction is important. A successful computation can still produce an
unavailable claim when the source boundary required for that claim is missing.

## Support mode receipt family

The current support mode receipt files are:

- artifacts/receipts/fre_support_mode_receipt_regular_uniform_10_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_20_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_10_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_20_001.json

All four receipts are tied to:

- contract_id: fre.support_mode.regularity.v0.2
- circuit_id: support_mode_polynomial_v0.1
- execution gate: fre.support_mode.openfhe_execution_gate.v0.1
- rule: exact_integer_equality
- tolerance: 0
- reference_congruence: true
- negative_controls_passed: true

The regular uniform receipts have earned regularity claims:

- regular_uniform_10 has claim status `earned` with result true.
- regular_uniform_20 has claim status `earned` with result true.

The balanced exchange receipts have unavailable regularity claims:

- balanced_exchange_10 has claim status `unavailable` with result null.
- balanced_exchange_20 has claim status `unavailable` with result null.

The difference is source certification. The regular uniform receipts are scoped
to certified fixtures. The balanced exchange receipts remain algebraic controls
without geometric regularity certification.

## Support mode receipt boundary

The support mode receipts are local test profile receipts.

Their boundaries include:

- public fixture inputs only
- local test profile only
- no production security claim
- no observational closure

For earned regular uniform receipts, the geometric claim is scoped to the
certified fixture.

For unavailable balanced exchange receipts, geometric regularity is unavailable
without C_D certification.

## G900 recursive host receipt family

The current G900 recursive host receipt is:

- artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json

It is tied to:

- contract_id: fre.g900.recursive_host.v0.1
- gate: fre.g900.nonexecution_status_receipt_gate.v0.1
- claim type: vertex_local_recursive_host_admission
- claim status: unavailable
- claim result: null
- closure class: open

This receipt records unavailability. It is not a G900 execution receipt. It is
not recursive host admission. It is not observational closure.

## G900 recursive host boundary

The G900 unavailable receipt includes boundaries such as:

- status receipt not execution receipt
- structural validation not recursive host admission
- independent bridge missing
- distinct environment missing
- ambient trace missing
- no receipts no true
- pressure exists but pressure is not authorization
- no observational closure

This language is part of the receipt truth. It should not be removed when the
receipt is summarized.

## Privacy

Receipts are public memory, not private body dumps.

Receipt schemas and receipt artifacts should preserve the public/private split.
They may expose public operation names, public source classes, claim-relative
results, comparison status, closure status, and boundary language.

They must not expose secret inputs, secret keys, ciphertexts, raw backend
runtime objects, or undeclared intermediate values.

## Closure

Receipts should name closure honestly.

Current support mode receipts use local closure. They do not claim external
truth or observational closure.

The current G900 recursive host receipt uses open closure. It records that the
bridge and admission requirements are not satisfied.

Closure labels are not decoration. They prevent bounded results from being
promoted into larger claims.

## Receipt validation

The SysOp should validate receipts against their schemas before relying on
them.

A valid receipt should satisfy:

1. The schema accepts the shape.
2. The contract_id matches the intended contract.
3. The gate field matches the admitted action.
4. The claim status matches the source boundary.
5. The comparison field matches the predeclared rule.
6. The controls field records required negative-control status.
7. The privacy field preserves the public/private split.
8. The closure field does not overclaim.
9. The boundary field remains intact.

## Receipt is not audit

A receipt records an event.

An audit checks whether the event and its artifacts held their declared
boundary.

The two surfaces should be connected, but they are not the same thing.

## Boundary

This section documents receipts and schemas only.

It does not emit a new receipt.

It does not validate a receipt.

It does not pass an audit.

It does not admit execution.

It does not promote unavailable claims to earned claims.

It does not create production security, observational closure, external truth,
recursive host admission, physical interpretation, geometry, force, or a
universal theorem claim.
