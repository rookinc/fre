# 02 Contracts and Gates

Steward: SysOp

Status: Draft

## Purpose

This section documents the authority layer of FRE.

Contracts and gates decide what a Folded Receipt Envelope may admit, reject,
compare, canonicalize, execute, or emit. They are the seal on the envelope.

The central rule is simple:

If no contract or gate admits an action, FRE rejects it.

## Section scope

Owned scope:

- contracts/fre_g900_bounce_grammar_v0.1.json
- contracts/fre_g900_bounce_negative_control_execution_gate_v0.1.json
- contracts/fre_g900_bounce_negative_controls_v0.1.json
- contracts/fre_g900_bounce_reference_execution_gate_v0.1.json
- contracts/fre_g900_generator_target_comparison_gate_v0.1.json
- contracts/fre_g900_native_generator_execution_gate_v0.1.json
- contracts/fre_g900_native_generator_v0.1.json
- contracts/fre_g900_recursive_host_v0.1.json
- contracts/fre_g900_sibling_negative_control_execution_gate_v0.1.json
- contracts/fre_g900_sibling_negative_control_gate_v0.1.json
- contracts/fre_g900_status_receipt_gate_v0.1.json
- contracts/fre_g900_target_canonicalization_gate_v0.1.json
- contracts/fre_support_mode_openfhe_execution_gate_v0.1.json
- contracts/fre_support_mode_regularity_v0.1.json
- contracts/fre_support_mode_regularity_v0.2.json
- docs/02-contracts-and-gates.md

Reference scope:

- schemas/
- artifacts/
- fixtures/
- tools/
- notes/
- src/
- include/

## Contract versus gate

A contract declares a bounded protocol meaning.

A gate admits a specific action under a contract boundary.

In practice, a contract may define a computation, grammar, target, claim
boundary, source class, or comparison rule. A gate usually declares one narrow
execution path: command, reads, forbidden reads, invocation count, runtime
capture, and output expectations.

Contracts answer:

- What does this envelope mean?
- What is in scope?
- What is out of scope?
- What claim is forbidden?
- What comparison or receipt is expected?

Gates answer:

- What exact command may run?
- Which files may it read?
- Which files must it not read?
- How many times may it run?
- Where does runtime capture go?
- May runtime capture be committed?
- What output must be checked later?

## Authority fields

Important authority fields include:

- contract_id
- gate_id
- version
- status
- purpose
- admission
- permissions
- bindings
- claim_boundary
- boundary
- allowed_command
- allowed_data_reads
- allowed_reads
- forbidden_data_reads
- forbidden_reads
- allowed_project_writes
- maximum_invocations
- runtime_capture
- runtime_capture_may_commit
- predeclared_output_requirements

Not every contract uses every field. The SysOp should read the actual file
before running any action.

## Status language

Many gates say `admitted_not_executed`.

That status records the pre-run authority state. It means the gate admits a
future action, not that the action has already happened.

After execution, truth should move into runtime capture, receipts, artifacts,
and audits. The contract or gate should not be silently reinterpreted as an
execution receipt.

## Invocation discipline

Many current gates use:

- maximum_invocations: 1
- allowed_project_writes: []
- runtime_capture_may_commit: false

This is deliberate.

The run is narrow. The project tree is protected. Runtime material usually
lands in `$HOME/tmp/...` and is not automatically public. A later audit decides
what public artifact, if any, can be committed.

## Read discipline

Several gates explicitly separate allowed reads from forbidden reads.

This prevents leakage between construction paths. For example, a generator run
may be allowed to read source fixtures while forbidden from reading the target
edge table. A target canonicalization run may be allowed to read the target
while forbidden from reading generator inputs. A comparison gate may be allowed
to read completed audits while forbidden from reopening either construction
path.

This separation is part of the proof discipline of the repository. It keeps a
result from being earned by accidentally reading the answer.

## Claim boundaries

Claim boundaries are authority fields.

They are not commentary.

When a contract states that physical_claim is false, observational_closure is
false, recursive_host_claim is false, or universal_theorem_claim is false, that
is part of the envelope seal.

A passed execution or audit must not promote a forbidden claim unless a later
contract explicitly admits that promotion.

## Support mode contract family

The support mode family currently includes:

- contracts/fre_support_mode_regularity_v0.1.json
- contracts/fre_support_mode_regularity_v0.2.json
- contracts/fre_support_mode_openfhe_execution_gate_v0.1.json

The regularity contracts declare the support-mode polynomial comparison. The
v0.1 contract begins with the backend disabled. The v0.2 contract extends the
predeclared model to a linked but crypto-closed OpenFHE profile state.

The OpenFHE execution gate admits one bounded local public fixture batch. Its
scope includes selected fixture IDs, rejected pre-gate fixture IDs, admitted
operations, receipt policy, failure conditions, and explicit production
boundaries.

This family does not claim production cryptographic security, external truth,
physical interpretation, global support-chamber closure, or an unbounded
OpenFHE backend.

## G900 recursive host family

The recursive host family currently includes:

- contracts/fre_g900_recursive_host_v0.1.json
- contracts/fre_g900_status_receipt_gate_v0.1.json

The recursive host contract records a candidate structure while keeping
recursive host admission closed.

The status receipt gate admits a narrow nonexecution status receipt. Its
boundary states that an unavailable status receipt is not a G900 execution
receipt, not recursive-host admission, not transport execution, not
observational closure, and not a physical claim.

## G900 native generator family

The native generator family currently includes:

- contracts/fre_g900_native_generator_v0.1.json
- contracts/fre_g900_native_generator_execution_gate_v0.1.json
- contracts/fre_g900_target_canonicalization_gate_v0.1.json
- contracts/fre_g900_generator_target_comparison_gate_v0.1.json
- contracts/fre_g900_sibling_negative_control_gate_v0.1.json
- contracts/fre_g900_sibling_negative_control_execution_gate_v0.1.json

This family separates construction, target canonicalization, comparison, and
negative control work.

The native generator contract declares structural reconstruction from G15,
G60, signing data, and half-flip rules without reading the flattened G900
target during generation.

The target canonicalization gate admits independent target normalization.

The comparison gate compares locked digests without reopening construction
paths.

The sibling negative control gates admit a separate sibling signing control and
require digest separation from the positive construction.

The family boundary remains structural. It does not create a recursive host
theorem, observational closure, physical claim, or universal theorem claim.

## G900 bounce family

The bounce family currently includes:

- contracts/fre_g900_bounce_grammar_v0.1.json
- contracts/fre_g900_bounce_negative_controls_v0.1.json
- contracts/fre_g900_bounce_reference_execution_gate_v0.1.json
- contracts/fre_g900_bounce_negative_control_execution_gate_v0.1.json

The bounce grammar declares one receipt-bearing 360 + 180 + 360 symbolic bounce
over a single oriented signed G15 carrier edge lifted into G900.

The reference execution gate admits one plaintext reference run.

The negative controls contract and execution gate test that return to the
source vertex is not enough by itself. Phase, edge, slip, chamber lock, and
receipt distinctions must not collapse into an unearned claim.

The bounce family does not admit graph transport execution, recursive host
closure, observational closure, physical interpretation, external truth, or a
universal all-vertex result.

## Negative controls

Negative controls are first-class contract work.

A negative control is not a nuisance. It protects the positive result from
being overread.

Current negative-control examples include:

- G900 bounce negative controls
- G900 sibling negative controls
- support mode rejected pre-gate fixtures

A successful negative control often rejects, separates, or withholds a receipt.
That is a valid outcome when the contract expects it.

## SysOp procedure

Before running a tool, the SysOp should check:

1. Which contract or gate admits this action?
2. What exact command is allowed?
3. What files may be read?
4. What files are forbidden?
5. What writes are allowed?
6. What is the maximum invocation count?
7. Where does runtime capture go?
8. May runtime capture be committed?
9. What receipt, artifact, or audit is expected afterward?
10. Which claims remain forbidden even if the run passes?

If any answer is missing, pause and add or repair the contract before running
the action.

## Boundary

This section documents contracts and gates only.

It does not admit a new run.

It does not consume any one-shot gate.

It does not emit a receipt.

It does not pass an audit.

It does not promote recursive hosting, graph transport, observational closure,
production security, external truth, physical interpretation, geometry, force,
or a universal theorem claim.
