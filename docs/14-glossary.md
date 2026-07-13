# 14 Glossary

Steward: ED

Status: Draft

## Purpose

This section defines FRE vocabulary.

The glossary exists so ED language, SysOp procedure, contracts, receipts,
audits, tools, notes, and public explanations do not drift apart.

## Section scope

Owned scope:

- README.md
- fre_continuity.md
- notes/
- docs/
- contracts/
- schemas/
- artifacts/
- fixtures/
- include/
- src/
- tools/
- docs/14-glossary.md

## FRE

FRE currently means Folded Receipt Envelope.

Older language may expand FRE as Finite Receipt Engine. In the current protocol
framing, Folded Receipt Envelope is preferred.

## Folded Receipt Envelope

A bounded protocol packet that joins source material, admission rules,
execution limits, and receipt expectations in one inspectable form.

The envelope does not make an action true. The envelope makes the action
accountable.

## Fold

To pack bounded source material into an inspectable protocol shape.

Folded material may include fixtures, operation names, source-class identifiers,
tolerances, public inputs, target identifiers, or comparison rules.

## Seal

The authority attached to an envelope.

In FRE, the seal is usually a contract or gate.

## Contract

A document that declares bounded protocol meaning, claim limits, source class,
comparison rule, receipt policy, or execution boundary.

A contract says what the envelope means.

## Gate

A document that admits a specific action under a contract boundary.

A gate usually declares allowed command, allowed reads, forbidden reads, writes,
maximum invocation count, runtime capture path, and output expectations.

A gate says what may run.

## Admission

Permission for an action to proceed under a declared contract or gate.

Admission should be explicit and narrow.

## Rejection

A contract-level refusal.

Rejection is often the correct result. Negative controls, missing authority,
bad input, or forbidden reads should reject.

## Bounce

The return of a non-admitted or non-conforming envelope without granting the
requested claim.

A bounce can be informative, but it does not earn the claim.

## Receipt

A finite public memory of an envelope event.

A receipt records what happened under a declared contract, gate, comparison,
privacy rule, closure class, and boundary.

A receipt is not a global theorem by itself.

## Schema

A closed shape rule for a receipt or other structured artifact.

Schemas prevent undeclared fields from silently changing public meaning.

## Audit

A bounded check that verifies whether an event, artifact, receipt, fixture,
tool output, or digest relationship held its declared boundary.

An audit pass means the audit passed. It does not erase the boundary.

## Fixture

Public source material, target material, or control material used by a
contract, gate, tool, receipt, or audit.

A fixture is not proof by itself.

## Source material

Material that may be folded into an admitted computation or declaration.

Source material must not be confused with target material.

## Target material

Material used as a target, comparison surface, or canonicalization input.

A target should not be read by a generator unless a gate explicitly admits it.

## Control material

Material used to test that a positive result is not being overread.

Negative-control material should not be silently promoted to positive source
material.

## Payload

A structured body of source or target data used by a protocol path.

In G900, payload often refers to the pinned carrier or related fixture surface.

## Canonicalization

A deterministic normalization step that creates a stable comparison form.

For G900 target work, canonicalization turns edge material into a locked digest
surface.

## Digest

A hash value used to bind a file, runtime capture, canonical form, or artifact.

A matching digest can establish identity under the declared serialization. It
does not automatically establish a broader theorem.

## Runtime capture

Operational evidence written during an admitted run, often under `$HOME/tmp/`.

Runtime capture is not automatically public artifact material.

## Public face

The material FRE may expose publicly.

Examples include contracts, schemas, operation names, source-class identifiers,
tolerance declarations, claim-relative results, verification status,
negative-control status, and boundary language.

## Private body

Material that must not be committed or exposed.

Examples include secret inputs, secret keys, ciphertexts, raw OpenFHE runtime
objects, and undeclared intermediate values.

## Closure

The declared scope of completion for a result.

Current examples include local closure and open closure.

Local closure is not observational closure.

## Observational closure

A stronger claim that the result closes against an external observation
boundary.

Current FRE artifacts do not claim observational closure.

## External truth

A claim that the protocol result establishes truth outside its declared
boundary.

Current FRE artifacts do not claim external truth.

## Support mode

The six-coordinate support-register calculation used in the Project 39
regularity path.

The reference calculation computes S, d, K, and regular.

## Support register

A six-coordinate support input.

In the reference system, support coordinates must be positive integers.

## Regularity

The support-mode claim associated with K equal to zero for certified source
material.

Without source certification, the same polynomial may compute while the
geometric regularity claim remains unavailable.

## OpenFHE backend

The OpenFHE implementation surface used for bounded encrypted support-mode
computation when admitted by gate.

Backend linkage is not backend admission. Execution is not production security.

## OpenFHE status

The report of backend availability, link status, profile pinning, profile
admission, crypto permission, and boundary.

## G900

The 900-state signed half-flip carrier surface used in the G900 workflow.

Current G900 work is bounded by structural, canonical, receipt, and audit
claims. It does not admit recursive hosting or graph transport.

## G15

The 15-slot graph used in the G900 carrier grammar.

The current notes identify it as L(Petersen).

## G60

The 60-local chamber graph used in the G900 carrier grammar.

## Half-flip

The signed carrier rule that shifts local coordinate by 30 modulo 60 when the
sign requires it.

## Recursive host

A candidate/local-chart declaration for reading completed inner G900 structure
as an outer vertex.

Current FRE records recursive-host status as unavailable.

## Transport

A stronger action or relation claim than current G900 structural checkpoints
admit.

Current G900 artifacts do not admit graph transport execution.

## Bounce grammar

The symbolic G900 phase grammar:

`360 + 180 + 360 = 900`

It is a formal symbolic measure, not a physical-angle or time claim.

## Receipt candidate I_0

The plaintext reference receipt candidate from the G900 bounce checkpoint.

It is not a public recursive-host receipt.

## Negative control

A test expected to reject, separate, or withhold a claim.

Negative controls protect positive results from being overread.

## ED

Executive Director.

The ED stewards meaning, scope, continuity, claim language, and project
direction.

## SysOp

System Operator.

The SysOp stewards operational truth, contracts, gates, fixtures, tools,
receipts, audits, builds, and repository hygiene.

## Boundary

The explicit limit on what a document, artifact, receipt, audit, contract, or
tool result claims.

Boundary language is part of the truth surface.

## Boundary

This glossary defines language only.

It does not admit execution.

It does not emit receipts.

It does not run audits.

It does not promote claims.

It does not create production security, observational closure, external truth,
recursive-host admission, graph transport, physical interpretation, geometry,
force, or a universal theorem claim.
