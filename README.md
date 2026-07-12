# FRE

B32K Folded Receipt Envelope research implementation.

## First target

Evaluate the Project 39 Euclidean support-mode regularity and
scale-shape relations through an encrypted OpenFHE pipeline, compare
them with an independent plaintext reference pipeline, and export a
bounded public receipt.

## Architecture

- FRE Public Face: contracts, schemas, operation names, and boundaries
- FRE Private Body: secret inputs, keys, ciphertexts, and runtime objects
- FRE Receipt: claim-relative result, dependencies, and verification
- Reference Pipeline: independent plaintext calculation
- Comparator: predeclared receipt-congruence test

## Current status

Phase 0 scaffold only.

No OpenFHE backend is enabled.
No key generation, encryption, evaluation, or decryption is performed.
No cryptographic security theorem is claimed.
No global dodecahedral support-chamber test is claimed.
No physical interpretation is claimed.
