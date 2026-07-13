# 01 Folded Receipt Envelope Model

Steward: ED

Status: Draft

## Purpose

This section defines the core FRE model.

FRE means Folded Receipt Envelope. A Folded Receipt Envelope is a bounded
protocol packet that carries source material, admission rules, execution
limits, and receipt expectations in one inspectable form.

This model is conceptual, but it is not decorative. It is the rule language
that keeps the repository from treating capability as authority.

## Envelope principle

An envelope does not make an action true.

An envelope makes an action accountable.

A valid envelope tells the SysOp what is being folded, what authority admits
or rejects it, what may run, what must stay private, what receipt should be
emitted, and what audit should check afterward.

## Lifecycle

The basic lifecycle is:

1. Fold
2. Seal
3. Admit or reject
4. Run if admitted
5. Bounce if rejected
6. Emit receipt
7. Audit
8. Preserve continuity

Each step has a different responsibility. Confusing those steps is the main
failure mode FRE is designed to prevent.

## Fold

To fold is to pack bounded source material into an inspectable protocol shape.

The folded material may include fixtures, operation names, source-class
identifiers, tolerances, public inputs, target identifiers, or declared
comparison rules.

Folded material must not include private runtime body material unless the
contract explicitly allows it and the repository boundary permits it.

In the current repository, fold material may come from:

- fixtures/
- contracts/
- schemas/
- selected public artifacts
- declared operation names
- declared source-class identifiers

## Seal

To seal is to attach authority.

The seal is normally a contract or gate. It states what is allowed, what is
forbidden, what the maximum invocation count is, what receipt is expected, and
what rejection means.

In the current repository, seals live primarily in:

- contracts/

A seal is not a receipt. A seal gives or denies permission. A receipt records
what happened under that permission.

## Admit

To admit is to let an action proceed under a declared contract or gate.

Admission should be narrow. It should say exactly what action is allowed, which
inputs are in scope, how many times the action may run, and what output or
receipt is expected.

If admission is unclear, the action should not run.

## Reject

To reject is to refuse an action under the contract boundary.

Rejection is not failure in the ordinary sense. In FRE, rejection is often the
correct result. Negative controls are expected to reject. Missing authority
should reject. Private material exposure should reject.

A good rejection preserves the boundary.

## Run

To run is to perform an admitted action.

Running may involve a reference implementation, a backend adapter, a CLI tool,
or a validation script. Running should not silently expand the claim.

In the current repository, run surfaces include:

- src/
- include/
- tools/
- build/
- build-openfhe-link/

The existence of a runnable tool does not admit the action. The contract or
gate admits the action.

## Bounce

To bounce is to return a non-admitted or non-conforming envelope without
granting the requested claim.

A bounce may still be informative. It can show that a negative control was
rejected, that a recursive host was unavailable, or that a requested action had
no valid admission path.

Bounce behavior is especially important in the G900 work, where same-vertex
return or structural resemblance must not become an unearned transport,
recursive-host, observational, physical, geometric, or force claim.

## Receipt

A receipt is the public memory of an envelope event.

A receipt records the result that the contract permits the system to expose.
It should be finite, inspectable, schema-shaped where applicable, and tied to
the boundary that admitted or rejected the event.

In the current repository, receipt material lives in:

- artifacts/receipts/
- schemas/
- selected artifacts/json/ files

A receipt is not a theorem by itself. A receipt says that a bounded event was
recorded under a declared protocol shape.

## Audit

An audit checks whether the envelope event held its boundary.

Audits may check schemas, fixtures, receipt contents, contract expectations,
negative controls, digest matches, link status, or execution congruence.

In the current repository, audit logic and audit outputs live in:

- tools/audit_*.py
- artifacts/json/*audit*.json

An audit pass means the declared audit passed. It does not automatically promote
a broader claim.

## Continuity

Continuity preserves the operational memory of the project.

Continuity should record what is current, what is historical, what is blocked,
what has been admitted, what has been consumed, and what must not be broken.

In the current repository, continuity material lives in:

- fre_continuity.md
- notes/
- docs/

## Public face and private body

FRE separates the public face from the private body.

The public face may include contracts, schemas, operation names, source-class
identifiers, tolerance declarations, claim-relative results, verification
status, and negative-control status.

The private body must not be committed or exposed. It includes secret inputs,
secret keys, ciphertexts, raw backend runtime objects, and undeclared
intermediate values.

The envelope exists partly to keep those two surfaces from being confused.

## Stewardship

The ED stewards the meaning of the envelope model, the claim boundary, and the
language used to explain FRE.

The SysOp stewards operational truth: contracts, gates, tools, fixtures,
receipts, audits, builds, and repository hygiene.

The ED may define what the organization intends. The SysOp verifies what the
system actually admitted, ran, rejected, receipted, and audited.

## Current model boundary

This section defines the model language only.

It does not admit new execution.

It does not promote an OpenFHE backend.

It does not admit recursive hosting.

It does not create a graph transport claim.

It does not create observational closure.

It does not make a physical, geometric, force, or universal theorem claim.
