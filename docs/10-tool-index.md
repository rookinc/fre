# 10 Tool Index

Steward: SysOp

Status: Draft

## Purpose

This section indexes the Python tools in FRE.

Tools perform validation, generation, canonicalization, comparison, receipt
emission, gate preparation, profile pinning, reference runs, negative-control
runs, and audits.

A tool is capability. A contract or gate is authority. The SysOp must not run a
tool merely because it exists.

## Section scope

Owned scope:

- tools/audit_g900_bounce_negative_controls.py
- tools/audit_g900_bounce_reference.py
- tools/audit_g900_checkpoint.py
- tools/audit_g900_generator_target_congruence.py
- tools/audit_g900_native_generator_checkpoint.py
- tools/audit_g900_native_generator_execution.py
- tools/audit_g900_sibling_negative_control.py
- tools/audit_g900_target_canonicalization.py
- tools/audit_openfhe_execution.py
- tools/audit_openfhe_link_status.py
- tools/audit_openfhe_receipts.py
- tools/audit_reference_fixtures.py
- tools/canonicalize_g900_target.py
- tools/compare_g900_generator_target.py
- tools/emit_g900_status_receipt.py
- tools/emit_openfhe_receipts.py
- tools/generate_g900_kernel.py
- tools/generate_g900_sibling_control.py
- tools/pin_openfhe_executed_profile.py
- tools/prepare_openfhe_execution_gate.py
- tools/run_g900_bounce_negative_controls.py
- tools/run_g900_bounce_reference.py
- tools/validate_g900_payload.py
- docs/10-tool-index.md

Reference scope:

- contracts/
- schemas/
- fixtures/
- artifacts/json/
- artifacts/receipts/
- build/
- build-openfhe-link/
- $HOME/tmp/

## Tool rule

Before running any tool, the SysOp should identify:

- the admitting contract or gate
- allowed reads
- forbidden reads
- allowed writes
- runtime capture path
- expected artifact
- expected receipt
- expected audit
- claim boundary

If no authority admits the run, do not run the tool.

## Tool classes

The current tool classes are:

- G900 validators and emitters
- G900 constructors and comparators
- G900 bounce runners
- G900 audit tools
- OpenFHE preparation and profile tools
- OpenFHE receipt tools
- OpenFHE audit tools
- support mode reference audit tools

Some tools write committed artifacts. Some consume `$HOME/tmp/` runtime
captures. Some only prepare or pin authority surfaces. Check each tool before
use.

## G900 validators and emitters

### validate_g900_payload.py

Role: validate the G900 payload surface and write structural audit output.

Primary inputs:

- fixtures/g900/
- contracts/fre_g900_recursive_host_v0.1.json
- artifacts/json/fre_g900_payload_provenance_001.json

Primary output:

- artifacts/json/fre_g900_structural_audit_001.json

Boundary: validates structure; does not admit recursive hosting or transport.

### emit_g900_status_receipt.py

Role: emit the gated nonexecution G900 recursive-host unavailable receipt.

Primary inputs:

- schemas/fre_g900_recursive_host_receipt_v0.1.schema.json
- contracts/fre_g900_status_receipt_gate_v0.1.json
- contracts/fre_g900_recursive_host_v0.1.json
- artifacts/json/fre_g900_payload_provenance_001.json
- artifacts/json/fre_g900_structural_audit_001.json

Primary output:

- artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json

Boundary: emits unavailable status only; does not execute G900 or admit
recursive hosting.

## G900 constructors and comparators

### generate_g900_kernel.py

Role: construct the canonical G900 kernel from compact source fixtures.

Primary inputs:

- fixtures/g900/g15_slot_edges.csv
- fixtures/g900/g60_local_edges.csv
- fixtures/g900/carrier_signing_table.csv

Runtime capture:

- $HOME/tmp/fre_g900_native_generator_run_001.json

Boundary: must not read the flattened target.

### canonicalize_g900_target.py

Role: independently canonicalize the committed flat G900 target.

Primary input:

- fixtures/g900/x_sigma_edges.csv

Runtime capture:

- $HOME/tmp/fre_g900_target_canonicalization_001.json

Boundary: target canonicalization only; must not read generator source or result.

### compare_g900_generator_target.py

Role: compare locked native-generator and flat-target digest artifacts.

Primary inputs:

- artifacts/json/fre_g900_native_generator_execution_audit_001.json
- artifacts/json/fre_g900_target_canonicalization_audit_001.json

Runtime capture:

- $HOME/tmp/fre_g900_generator_target_comparison_001.json

Boundary: compares locked audits; does not reopen either construction path.

### generate_g900_sibling_control.py

Role: construct the six-toggle sibling G900 negative control.

Primary inputs:

- fixtures/g900/g15_slot_edges.csv
- fixtures/g900/g60_local_edges.csv
- fixtures/g900/sibling_candidate_signing_table.csv

Runtime capture:

- $HOME/tmp/fre_g900_sibling_negative_control_001.json

Boundary: negative control only; not positive source material.

## G900 bounce runners

### run_g900_bounce_reference.py

Role: run one plaintext reference automaton for the admitted G900 bounce cycle.

Primary input:

- contracts/fre_g900_bounce_grammar_v0.1.json

Runtime capture:

- $HOME/tmp/fre_g900_bounce_reference_run_001.json

Boundary: plaintext reference trace only; not public recursive-host receipt.

### run_g900_bounce_negative_controls.py

Role: evaluate the five predeclared G900 bounce negative controls.

Primary input:

- contracts/fre_g900_bounce_negative_controls_v0.1.json

Runtime capture:

- $HOME/tmp/fre_g900_bounce_negative_controls_run_001.json

Boundary: negative-control evaluation only; rejected cases should not emit
control receipts.

## G900 audit tools

### audit_g900_bounce_reference.py

Role: record the one-shot plaintext G900 bounce reference.

Consumes:

- $HOME/tmp/fre_g900_bounce_reference_run_001.json

Writes:

- artifacts/json/fre_g900_bounce_reference_audit_001.json

### audit_g900_bounce_negative_controls.py

Role: audit the preserved one-shot G900 bounce negative-control capture.

Consumes:

- $HOME/tmp/fre_g900_bounce_negative_controls_run_001.attempted
- $HOME/tmp/fre_g900_bounce_negative_controls_run_001.json

Writes:

- artifacts/json/fre_g900_bounce_negative_controls_audit_001.json

### audit_g900_native_generator_execution.py

Role: record the locked first native G900 generator observation.

Consumes:

- $HOME/tmp/fre_g900_native_generator_run_001.json

Writes:

- artifacts/json/fre_g900_native_generator_execution_audit_001.json

### audit_g900_target_canonicalization.py

Role: record the independent canonical G900 target observation.

Consumes:

- $HOME/tmp/fre_g900_target_canonicalization_001.json

Writes:

- artifacts/json/fre_g900_target_canonicalization_audit_001.json

### audit_g900_generator_target_congruence.py

Role: record native-generator to flat-target G900 digest congruence.

Consumes:

- $HOME/tmp/fre_g900_generator_target_comparison_001.json

Writes:

- artifacts/json/fre_g900_generator_target_congruence_audit_001.json

### audit_g900_sibling_negative_control.py

Role: record the six-toggle sibling G900 negative control.

Consumes:

- $HOME/tmp/fre_g900_sibling_negative_control_001.json

Writes:

- artifacts/json/fre_g900_sibling_negative_control_audit_001.json

### audit_g900_native_generator_checkpoint.py

Role: audit the fail-closed native G900 generator checkpoint.

Consumes locked audit artifacts from generator execution, target
canonicalization, digest congruence, and sibling negative control.

Writes:

- artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json

### audit_g900_checkpoint.py

Role: audit the fail-closed G900 recursive-host checkpoint.

Consumes locked contract, provenance, structural audit, status gate, schema,
receipt, validator, and status emitter files.

Writes:

- artifacts/json/fre_g900_checkpoint_audit_001.json

## OpenFHE preparation and profile tools

### pin_openfhe_executed_profile.py

Role: pin executed OpenFHE profile provenance imported from the Aletheos adapter
surface.

Primary inputs include:

- external Aletheos OpenFHE adapter artifacts
- fixtures/json/fre_support_mode_fixture_set_v0.1.json

Primary output:

- artifacts/json/fre_openfhe_executed_profile_provenance_001.json

Boundary: profile provenance only; not FRE backend admission by itself.

### prepare_openfhe_execution_gate.py

Role: prepare the OpenFHE support mode execution gate.

Primary inputs:

- contracts/fre_support_mode_regularity_v0.1.json
- contracts/fre_support_mode_regularity_v0.2.json
- schemas/fre_support_mode_receipt_v0.2.schema.json
- fixtures/json/fre_support_mode_fixture_set_v0.1.json
- artifacts/json/fre_support_mode_reference_audit_001.json
- artifacts/json/fre_support_mode_reference_audit_002.json
- artifacts/json/fre_openfhe_executed_profile_provenance_001.json
- artifacts/json/fre_openfhe_durable_prefix_001.json
- artifacts/json/fre_openfhe_link_status_audit_001.json

Primary output:

- contracts/fre_support_mode_openfhe_execution_gate_v0.1.json

Boundary: prepares admission surface; does not execute crypto by itself.

## OpenFHE receipt tools

### emit_openfhe_receipts.py

Role: emit schema-bound public receipts from the bounded OpenFHE execution
audit.

Primary inputs:

- schemas/fre_support_mode_receipt_v0.2.schema.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json

Primary outputs:

- artifacts/receipts/fre_support_mode_receipt_regular_uniform_10_001.json
- artifacts/receipts/fre_support_mode_receipt_regular_uniform_20_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_10_001.json
- artifacts/receipts/fre_support_mode_receipt_balanced_exchange_20_001.json

Boundary: emits public receipts without rerunning crypto.

## OpenFHE audit tools

### audit_openfhe_link_status.py

Role: audit OpenFHE link status and fail-closed backend boundary.

Primary inputs:

- artifacts/json/fre_openfhe_executed_profile_provenance_001.json
- artifacts/json/fre_openfhe_durable_prefix_001.json
- build-openfhe-link/

Primary output:

- artifacts/json/fre_openfhe_link_status_audit_001.json

Boundary: link status only; no crypto allowed.

### audit_openfhe_execution.py

Role: audit the bounded OpenFHE support mode smoke execution.

Consumes:

- $HOME/tmp/fre_openfhe_support_mode_smoke_001_raw.json

Writes:

- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json

Boundary: records execution-reference congruence; receipt congruence belongs to
the receipt audit.

### audit_openfhe_receipts.py

Role: audit the emitted OpenFHE support mode receipt set.

Primary inputs:

- schemas/fre_support_mode_receipt_v0.2.schema.json
- artifacts/json/fre_support_mode_openfhe_execution_audit_001.json
- artifacts/receipts/
- tools/emit_openfhe_receipts.py

Primary output:

- artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json

Boundary: receipt-set audit only; does not rerun crypto.

## Support mode reference audit tool

### audit_reference_fixtures.py

Role: audit the plaintext support mode reference executable against the
predeclared fixture set.

Primary inputs:

- contracts/fre_support_mode_regularity_v0.1.json
- schemas/fre_support_mode_receipt_v0.1.schema.json
- fixtures/json/fre_support_mode_fixture_set_v0.1.json
- build/fre_support_reference

Primary output:

- artifacts/json/fre_support_mode_reference_audit_001.json

Boundary: reference pipeline only; no OpenFHE backend admission.

## Runtime capture rule

Runtime captures under `$HOME/tmp/` are operational evidence.

They should not be treated as committed public artifacts unless a contract,
gate, and audit explicitly allow that transition.

## SysOp procedure

Before running a tool, the SysOp should check:

1. What class of tool is this?
2. What contract or gate admits the run?
3. What files does it read?
4. What files is it forbidden to read?
5. Does it write a runtime capture or committed artifact?
6. Is it allowed to write into the project tree?
7. Does it rerun a computation or only audit existing evidence?
8. Does it emit a receipt?
9. What boundary remains false after it succeeds?

## Boundary

This section indexes tools only.

It does not run any tool.

It does not prepare a gate.

It does not emit a receipt.

It does not run an audit.

It does not admit OpenFHE execution, G900 transport, recursive hosting,
observational closure, production security, external truth, physical
interpretation, geometry, force, or a universal theorem claim.
