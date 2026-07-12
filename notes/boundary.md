# FRE project boundary

## Allowed project work

- define public contracts and receipt schemas
- implement an independent plaintext reference evaluator
- add certified finite fixtures and negative controls
- implement an OpenFHE backend behind an explicit build gate
- compare decrypted results against reference receipts
- preserve failure receipts and unresolved boundaries

## Private body

The following remain runtime-only and must not be committed:

- secret inputs
- secret keys
- ciphertexts
- raw OpenFHE runtime objects
- undeclared intermediate values

## Public face

The public surface may expose:

- contract and circuit identifiers
- admitted operation names
- source-class identifiers
- encoding and tolerance declarations
- claim-relative results permitted by the contract
- verification and negative-control status

## Claim boundary

The scaffold does not admit an OpenFHE backend, prove cryptographic
security, certify arbitrary support registers as members of C_D,
establish a folding-compiler optimum, or make a physical claim.
