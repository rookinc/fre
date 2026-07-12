# G900 Native Generator Checkpoint 001

Status: structural reproduction recorded; recursive hosting remains closed

## Result

FRE can now reconstruct the canonical 900-state carrier from its compact
graph grammar instead of treating the flattened 3,600-edge table as the
only authority.

The native construction uses exactly three inputs:

- the 30 edges of G15 = L(Petersen);
- the 120 local edges of G60;
- the 30-edge canonical signing table.

It applies the vertex address

`vertex = 60 * slot + local`

and the signed carrier rule

`local -> local + 30 * sign mod 60`.

This produces 900 vertices, 1,800 internal G60-fiber edges, 1,800 signed
G15-carrier edges, and degree 8 at every vertex.

## Independent comparison

The native generator was frozen before its first execution. It was not
allowed to read the flattened G900 payload.

Its normalized edge pairs were sorted and serialized as ASCII `u,v`
records with LF endings. The resulting SHA-256 digest was:

`e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60`

A separately frozen target canonicalizer then read only the committed
flat payload. It could not read the generator source, runtime capture,
or generator audit.

The target canonicalizer produced the same canonical digest. A third
tool compared only the two locked audit artifacts. That comparison
passed with zero tolerance.

This is computational evidence that the compact product/signing law
reproduces the pinned carrier edge set under the declared canonical
serialization.

## Negative control

A sibling signing changed six G15 carrier signs while preserving the
same construction law.

The sibling graph still had:

- 900 vertices;
- 3,600 edges;
- degree 8 everywhere;
- one connected component.

Its canonical digest was:

`b7951eac5c82e49faeed6f3be342e2f0d546ae1bca90a22b4fc73edb79ed983c`

That digest differs from the canonical carrier digest. The comparison
therefore detects a small signing change even when coarse graph counts
remain unchanged.

This establishes fixed-label edge-set digest separation. It does not,
by itself, prove that the sibling graph is non-isomorphic to the
canonical graph.

## Why this matters

The G900 carrier is no longer only an imported table. It now has a
reproducible constructive grammar:

`G15 slots x G60 chambers + signed half-flip transport`.

The positive comparison shows reproducibility. The sibling control
shows sensitivity. Together they provide a stronger foundation for
binding a transport grammar to the carrier.

## Evidence

- Generator contract:
  `contracts/fre_g900_native_generator_v0.1.json`
- Generator execution audit:
  `artifacts/json/fre_g900_native_generator_execution_audit_001.json`
- Target canonicalization audit:
  `artifacts/json/fre_g900_target_canonicalization_audit_001.json`
- Generator-target congruence audit:
  `artifacts/json/fre_g900_generator_target_congruence_audit_001.json`
- Sibling negative-control audit:
  `artifacts/json/fre_g900_sibling_negative_control_audit_001.json`
- Checkpoint audit:
  `artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json`

## Current boundary

No 360 + 180 + 360 transport cycle has executed.

No independent inner-to-ambient bridge exists.

No vertex-local recursive-host instance is admitted.

No universal all-vertex theorem, graph non-isomorphism theorem,
observational closure, physical claim, or external-truth claim is made.

## Next phase

The next phase should predeclare the 900-phase bounce grammar as a
plaintext state machine. It should bind one oriented G15 edge, lift its
state through the G30 slip bit and G60 chamber lock, and preserve the
receipt-distinguished return state `I_t`.

Only after that reference trace is fixed should FRE construct an
independent inner and ambient environment for a one-vertex bridge probe.
