# FRE OpenFHE support-mode throughline 001

Status: completed local closure

Checkpoint: `a7521e397e676e3deaf12c67c45e122260660c5d`

## Practical result

FRE now wraps one bounded OpenFHE computation in a predeclared,
auditable receipt path. FRE does not replace OpenFHE or make ciphertext
homomorphic. OpenFHE performs the cryptographic operations; FRE records
what was admitted, executed, compared, and allowed to become a claim.

For a six-coordinate support register `h`, the circuit computes:

- `S = sum(h_i)`
- `d_i = 6*h_i - S`
- `K = sum(d_i*d_i)`
- `computed_regular = (K == 0)`

The encrypted pipeline and plaintext reference pipeline agreed exactly
on all four admitted public fixtures.

| Fixture | S | d | K | Receipt claim |
| --- | ---: | --- | ---: | --- |
| regular_uniform_10 | 60 | 0,0,0,0,0,0 | 0 | regularity earned: true |
| regular_uniform_20 | 120 | 0,0,0,0,0,0 | 0 | regularity earned: true |
| balanced_exchange_10 | 60 | 6,-6,0,0,0,0 | 72 | regularity unavailable |
| balanced_exchange_20 | 120 | 12,-12,0,0,0,0 | 288 | regularity unavailable |

The two uniform fixtures are certified members of the declared
geometric source class. The two balanced exchanges are algebraic
negative controls only; their polynomial outputs are valid, but FRE
does not convert them into geometric regularity claims.

## Throughline

1. Contract v0.2 fixes the circuit, bounds, operations, and claim rules.
2. The execution gate admits one four-fixture local batch.
3. OpenFHE constructs the BGV context and runtime-only key material.
4. `Encrypt`, `EvalAdd`, and `EvalMult` compute `S`, `d`, and `K`.
5. `DecryptVerify` compares the results with the plaintext reference.
6. The execution audit binds the saved public output to source and binary hashes.
7. Four public receipts bind claims to that audit.
8. The receipt-set audit verifies the claim split and privacy boundary.

## Evidence map

- `contracts/fre_support_mode_regularity_v0.2.json`
- `contracts/fre_support_mode_openfhe_execution_gate_v0.1.json`
- `schemas/fre_support_mode_receipt_v0.2.schema.json`
- `artifacts/json/fre_support_mode_openfhe_execution_audit_001.json`
- `artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json`
- `artifacts/receipts/fre_support_mode_receipt_*_001.json`

## Boundary

This is a local test with OpenFHE 1.5.1, `HEStd_NotSet`, and a small
ring dimension. It is not a production-security demonstration.

No keys, ciphertexts, secret inputs, or OpenFHE runtime objects are
committed. The fixtures are public.

The one-shot execution gate has been consumed. Do not rerun
`fre_openfhe_support_mode_smoke` under the existing gate.

Closure is local, not observational. No external truth or physical
claim is established. Advancing beyond this point requires a new
predeclared contract and execution gate, preferably with independent
inputs and an independently operated verifier.
