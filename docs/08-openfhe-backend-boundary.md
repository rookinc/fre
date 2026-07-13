# 08 OpenFHE Backend Boundary

Steward: SysOp

Status: Draft

## Purpose

This section documents the OpenFHE backend boundary in FRE.

OpenFHE performs cryptographic operations when an execution gate admits them.
FRE records what was admitted, executed, compared, receipted, and bounded.

The OpenFHE backend is not a blanket authority. Link status, profile
provenance, execution, receipt emission, and production security are separate
claims.

## Section scope

Owned scope:

- include/fre/openfhe_backend_status.hpp
- include/fre/openfhe_support_mode.hpp
- src/backends/openfhe/openfhe_backend_status.cpp
- src/backends/openfhe/openfhe_support_mode.cpp
- src/cli/fre_openfhe_status.cpp
- src/cli/fre_openfhe_support_mode_smoke.cpp
- notes/openfhe_support_mode_throughline_001.md
- artifacts/json/fre_openfhe_durable_prefix_001.json
- artifacts/json/fre_openfhe_executed_profile_provenance_001.json
- artifacts/json/fre_openfhe_link_status_audit_001.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json
- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json
- docs/08-openfhe-backend-boundary.md

Reference scope:

- CMakeLists.txt
- contracts/fre_support_mode_openfhe_execution_gate_v0.1.json
- contracts/fre_support_mode_regularity_v0.2.json
- schemas/fre_support_mode_receipt_v0.2.schema.json
- artifacts/receipts/
- fixtures/json/fre_support_mode_fixture_set_v0.1.json

## Boundary principle

Backend availability is not execution authority.

A linked backend can exist while crypto remains closed. A pinned profile can
exist while profile admission remains false. An execution can pass while
production security, observational closure, and physical claims remain false.

The gate decides what OpenFHE may do.

## Backend status API

The backend status API is declared in:

- include/fre/openfhe_backend_status.hpp

It defines:

- OpenFHEBackendStatus
- get_openfhe_backend_status

The status object records:

- backend_id
- backend_version
- install_prefix
- available
- linked
- profile_pinned
- profile_admitted
- crypto_allowed
- boundary

The current status implementation reports OpenFHE as available, linked, and
profile pinned, while profile admission and crypto permission remain false.

Its boundary is:

`link_only_profile_pinned_no_crypto`

## Backend status CLI

The backend status CLI is:

- src/cli/fre_openfhe_status.cpp

It prints the backend status as JSON.

This CLI is a status surface. It is not an execution surface for support mode
crypto.

## Durable prefix artifact

The durable prefix artifact is:

- artifacts/json/fre_openfhe_durable_prefix_001.json

It records a durable OpenFHE copy with source preserved.

Its boundary keeps crypto closed:

- no crypto context constructed
- no key generation
- no encryption
- no evaluation
- no decryption
- no FRE backend admission
- no receipt congruence
- no production security claim

The durable prefix is toolchain readiness, not backend adoption by itself.

## Executed profile provenance

The executed profile provenance artifact is:

- artifacts/json/fre_openfhe_executed_profile_provenance_001.json

It records a pinned executed EvalMult profile as imported evidence.

Its boundary keeps the profile from becoming automatic FRE authority:

- evidence import only
- openfhe backend not admitted
- profile not admitted to FRE
- no production security profile
- no receipt congruence
- no observational closure
- no physical claim

Profile provenance is not execution admission by itself.

## Link status audit

The link status audit is:

- artifacts/json/fre_openfhe_link_status_audit_001.json

Its verdict is:

- fail_closed_openfhe_link_target_verified_no_crypto

It records that the backend is available and linked, while crypto is not
allowed.

Its boundary preserves:

- link target only
- no crypto context
- no key generation
- no encryption
- no evaluation
- no decryption
- no FRE receipt emitted
- no profile admission
- no receipt congruence
- no production security
- no observational closure
- no physical claim

## Support mode OpenFHE API

The support mode OpenFHE API is declared in:

- include/fre/openfhe_support_mode.hpp

It defines:

- OpenFHEFixtureResult
- OpenFHEBatchResult
- run_openfhe_support_mode_batch

A fixture result records:

- fixture_id
- S
- d
- K
- regular
- slot_tail_zero
- decrypt_verified
- reference_match

A batch result records:

- run_id
- gate_id
- profile_id
- gate_admitted
- context_generated
- key_generated
- eval_mult_key_generated
- fixtures
- all_reference_match
- all_slot_tails_zero
- private_material_committed

## Support mode OpenFHE implementation

The implementation lives in:

- src/backends/openfhe/openfhe_support_mode.cpp

The admitted local batch uses four public fixtures:

- regular_uniform_10
- regular_uniform_20
- balanced_exchange_10
- balanced_exchange_20

The implementation computes the same support mode quantities as the plaintext
reference path:

- S
- d
- K
- regular

It uses packed plaintext slots and checks that unused slot tails remain zero
after decrypt verification.

## Support mode smoke CLI

The OpenFHE support mode smoke CLI is:

- src/cli/fre_openfhe_support_mode_smoke.cpp

It prints the admitted batch result as JSON.

This executable is an execution surface only when the OpenFHE execution gate
admits it. It should not be run merely because the binary exists.

## Execution gate

The OpenFHE execution gate is:

- contracts/fre_support_mode_openfhe_execution_gate_v0.1.json

It admits one bounded local public fixture batch.

The admitted operations are:

- ContextGen
- KeyGen
- EvalMultKeyGen
- Encrypt
- EvalAdd
- EvalMult
- DecryptVerify

The admitted scope is public test data only. Production data is not allowed.
Production security is not claimed.

The receipt policy keeps ciphertext material, runtime objects, and secret keys
out of the committed public surface.

## Execution audit

The OpenFHE execution audit is:

- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json

Its verdict is:

- bounded_openfhe_execution_matches_plaintext_reference

It records that all four fixture rows matched the plaintext reference, all slot
tails were zero, and private material was not committed.

It also records that receipt congruence was not established at this layer. That
belongs to the receipt audit.

## Receipt audit

The OpenFHE receipt audit is:

- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json

Its verdict is:

- schema_bound_receipt_congruence_for_bounded_local_batch

It records four receipts:

- two earned claims
- two unavailable claims

The closure remains local. External truth and observational closure remain
false.

## Throughline

The throughline note is:

- notes/openfhe_support_mode_throughline_001.md

It summarizes the practical path:

1. Contract v0.2 fixes the circuit, bounds, operations, and claim rules.
2. The execution gate admits one four-fixture local batch.
3. OpenFHE constructs runtime-only key material.
4. Encrypt, EvalAdd, and EvalMult compute S, d, and K.
5. DecryptVerify compares results with the plaintext reference.
6. The execution audit binds saved public output to source and binary hashes.
7. Four public receipts bind claims to that audit.
8. The receipt-set audit verifies the claim split and privacy boundary.

## Private material boundary

The OpenFHE path must not commit:

- secret inputs
- secret keys
- ciphertexts
- raw OpenFHE runtime objects
- undeclared intermediate values

The public surface may record operation names, fixture IDs, comparison status,
claim status, closure status, hashes, and boundary language.

## SysOp procedure

Before running OpenFHE work, the SysOp should check:

1. Is the backend merely linked, or is execution admitted?
2. Which gate admits the action?
3. Is the fixture batch exactly the admitted public batch?
4. Are production data and production security claims excluded?
5. Are secret keys, ciphertexts, and runtime objects excluded from commits?
6. Is the expected output a runtime capture, audit artifact, receipt, or all
   three?
7. Has the plaintext reference audit passed?
8. Does the receipt audit establish receipt congruence?
9. Which claims remain false even if execution passes?

## Boundary

This section documents the OpenFHE backend boundary only.

It does not run OpenFHE.

It does not admit a new backend action.

It does not construct a crypto context.

It does not generate keys.

It does not encrypt, evaluate, decrypt, or verify.

It does not emit a receipt.

It does not claim production security, observational closure, external truth,
physical interpretation, global support-chamber closure, or a universal theorem
claim.
