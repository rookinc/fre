# 06 Support Mode Reference System

Steward: SysOp

Status: Draft

## Purpose

This section documents the plaintext support mode reference system.

The reference system is the independent local calculation that OpenFHE results
are compared against. It is intentionally small, deterministic, and public.

The reference system is not the OpenFHE backend. It does not perform key
generation, encryption, evaluation, or decryption.

## Section scope

Owned scope:

- include/fre/support_mode.hpp
- src/support_mode_reference.cpp
- src/cli/fre_support_reference.cpp
- tools/audit_reference_fixtures.py
- artifacts/json/fre_support_mode_reference_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_002.json
- docs/06-support-mode-reference-system.md

Reference scope:

- CMakeLists.txt
- contracts/fre_support_mode_regularity_v0.1.json
- contracts/fre_support_mode_regularity_v0.2.json
- fixtures/json/fre_support_mode_fixture_set_v0.1.json
- schemas/fre_support_mode_receipt_v0.1.schema.json
- schemas/fre_support_mode_receipt_v0.2.schema.json
- artifacts/receipts/

## Reference principle

The reference pipeline exists so FRE has an independent plaintext baseline.

The baseline should be:

- small
- deterministic
- inspectable
- contract-bound
- fixture-audited
- separate from OpenFHE execution

The OpenFHE path may match the reference. The reference path does not inherit
OpenFHE authority, and OpenFHE does not define the reference truth.

## Public API

The public reference API is declared in:

- include/fre/support_mode.hpp

The API defines:

- `kSupportCoordinateCount`
- `SupportRegister`
- `SupportModeResult`
- `is_positive_support_register`
- `evaluate_support_mode`

`kSupportCoordinateCount` is 6.

`SupportRegister` is an array of six signed 64-bit integers.

`SupportModeResult` contains:

- `S`
- `d`
- `K`
- `regular`

## Reference calculation

The reference calculation is implemented in:

- src/support_mode_reference.cpp

The calculation accepts a positive six-coordinate support register.

It computes:

- `S = sum(h_i)`
- `d_i = 6*h_i - S`
- `K = sum(d_i*d_i)`
- `regular = (K == 0)`

Nonpositive support coordinates are rejected.

The implementation uses wider internal arithmetic and explicit narrowing checks
to avoid silently accepting overflow.

## CLI surface

The command-line reference executable is implemented in:

- src/cli/fre_support_reference.cpp

The executable is:

- fre_support_reference

It requires exactly six support coordinates.

On success, it emits JSON containing:

- pipeline_id: support_mode_reference_v0.1
- source_class: six_support_register
- S
- d
- K
- regular

On bad argument count or invalid input, it rejects rather than manufacturing a
result.

## Build targets

The reference build surface is declared in:

- CMakeLists.txt

The relevant targets are:

- fre_reference
- fre_support_reference

`fre_reference` is the static library containing the reference calculation.

`fre_support_reference` is the command-line executable linked against the
reference library.

The CMake test surface includes reference tests for:

- regular input
- nonuniform input
- scale control
- bad argument count

## Contract relationship

The reference system is tied to the support mode regularity contracts:

- contracts/fre_support_mode_regularity_v0.1.json
- contracts/fre_support_mode_regularity_v0.2.json

Both contracts preserve the same support mode polynomial:

- `S = sum(h_i)`
- `d_i = 6*h_i - S`
- `K = sum(d_i*d_i)`
- `K = 36*sigma^2`

The comparison rule is exact integer equality with tolerance 0.

The v0.2 contract rebinding does not change the reference math.

## Fixture relationship

The reference system is audited against:

- fixtures/json/fre_support_mode_fixture_set_v0.1.json

The fixture set contains six rows with mixed certification.

Some rows are certified geometric fixtures. Some rows are algebraic controls.
The reference calculation can compute both, but the claim boundary differs by
fixture kind and certification.

## Reference audit 001

The first reference audit is:

- artifacts/json/fre_support_mode_reference_audit_001.json

Its verdict is:

- plaintext_reference_matches_predeclared_fixtures

It records:

- pipeline_id: support_mode_reference_v0.1
- fixture_set_id: fre.support_mode.fixture_set.v0.1
- six fixture rows
- fixture count check
- hash binding check
- certified claim count check
- algebraic control count check
- rejected control count check
- scale relation check

Its boundary preserves:

- reference pipeline only
- no OpenFHE backend admission
- no key generation
- no encryption
- no evaluation
- no decryption
- no receipt emitted
- no observational closure
- no physical claim

## Reference audit 002

The second reference audit is:

- artifacts/json/fre_support_mode_reference_audit_002.json

Its verdict is:

- plaintext_reference_rebound_to_contract_v0.2

It records that the reference pipeline was rebound to the v0.2 support mode
contract while preserving the reference math, comparison rule, receipt quotient,
tolerance, operation surface, and fixture expectations.

Its boundary preserves:

- reference pipeline only
- no OpenFHE execution
- no receipt emitted
- no observational closure
- no physical claim

## Relationship to receipts

The reference system does not itself emit public receipts.

It produces plaintext reference outputs and audit artifacts. Receipt emission is
a separate layer handled by receipt tooling, schemas, execution audits, and
receipt audits.

This separation matters. A reference match can support a later receipt, but the
reference audit is not the receipt.

## Relationship to OpenFHE

The OpenFHE path must compare against the reference path.

The reference path does not prove OpenFHE security. It only provides the
plaintext result that OpenFHE output should match under the admitted local
profile.

When OpenFHE output matches the reference, the result is still bounded by the
execution gate, receipt schema, receipt audit, and claim boundary.

## SysOp procedure

Before using the support mode reference system, the SysOp should check:

1. Is the intended input exactly six coordinates?
2. Are all coordinates positive integers?
3. Which contract version is being compared against?
4. Which fixture row or source class is in scope?
5. Is the fixture certified or only an algebraic control?
6. Has the reference audit passed?
7. Is OpenFHE involved, or is this reference-only?
8. Is a receipt expected, or only an audit artifact?
9. Which claim boundaries remain false?

## Boundary

This section documents the plaintext support mode reference system only.

It does not run the reference executable.

It does not admit new fixtures.

It does not emit receipts.

It does not run OpenFHE.

It does not perform key generation, encryption, evaluation, or decryption.

It does not create production security, observational closure, external truth,
physical interpretation, global support-chamber closure, or a universal theorem
claim.
