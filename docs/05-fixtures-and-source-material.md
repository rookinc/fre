# 05 Fixtures and Source Material

Steward: SysOp

Status: Draft

## Purpose

This section documents the fixture and source-material layer of FRE.

Fixtures are bounded public inputs or target materials used by contracts,
gates, tools, receipts, and audits. They are the material that an envelope may
fold around.

A fixture is not proof by itself. A fixture becomes part of a receipt-bearing
event only when a contract or gate admits its use and an audit or receipt
records the result.

## Section scope

Owned scope:

- fixtures/g900/carrier_signing_table.csv
- fixtures/g900/g15_slot_edges.csv
- fixtures/g900/g60_local_edges.csv
- fixtures/g900/sibling_candidate_signing_table.csv
- fixtures/g900/sibling_signing_delta.csv
- fixtures/g900/sibling_x_sigma_edges.csv
- fixtures/g900/x_sigma_edges.csv
- fixtures/json/.gitkeep
- fixtures/json/fre_support_mode_fixture_set_v0.1.json
- docs/05-fixtures-and-source-material.md

Reference scope:

- contracts/
- schemas/
- tools/
- artifacts/json/
- artifacts/receipts/

## Fixture principle

Fixtures are source material, target material, or control material.

The SysOp must keep those roles separate.

A source fixture can be read by a generator or reference pipeline when a gate
admits it.

A target fixture can be read by a canonicalizer or comparison path when a gate
admits it.

A control fixture can be used to test that a positive result is not being
overread.

A file's existence does not make it admissible for every tool. The gate decides
which fixture may be read.

## G900 fixture family

The G900 fixture family lives in:

- fixtures/g900/

It currently contains seven CSV files:

- carrier_signing_table.csv
- g15_slot_edges.csv
- g60_local_edges.csv
- sibling_candidate_signing_table.csv
- sibling_signing_delta.csv
- sibling_x_sigma_edges.csv
- x_sigma_edges.csv

These files support the G900 structural, generator, target, sibling-control,
and bounce workflows.

## G900 core source fixtures

The core G900 source fixtures are:

- fixtures/g900/g15_slot_edges.csv
- fixtures/g900/g60_local_edges.csv
- fixtures/g900/carrier_signing_table.csv

`g15_slot_edges.csv` contains 30 G15 slot edges.

`g60_local_edges.csv` contains 120 G60 local edges.

`carrier_signing_table.csv` contains 30 signed carrier rows. Each row records a
slot pair, sign, carrier law, and external edge count. The carrier laws include
identity and half-flip behavior.

Together these files are source material for the native G900 generator path
when the relevant gate admits them.

## G900 target fixture

The canonical flattened target fixture is:

- fixtures/g900/x_sigma_edges.csv

It contains 3600 target edges with columns for vertex ids, slot/local
coordinates, and edge kind.

The edge kinds include:

- internal_thalion_copy
- external_signed_carrier

This file is target material. It is intentionally forbidden to the native
generator execution gate, because the generator must not read the answer it is
trying to reproduce.

The target canonicalization gate may read this file when admitted.

## G900 sibling control fixtures

The sibling-control fixtures are:

- fixtures/g900/sibling_candidate_signing_table.csv
- fixtures/g900/sibling_signing_delta.csv
- fixtures/g900/sibling_x_sigma_edges.csv

`sibling_candidate_signing_table.csv` contains 30 rows comparing canonical
signs, deltas, and sibling signs.

`sibling_signing_delta.csv` contains 30 rows describing which signing entries
are unchanged and which participate in sibling delta support.

`sibling_x_sigma_edges.csv` contains 3600 sibling target/control edges.

These files are negative-control material. They help test whether gross graph
invariants can be preserved while the fixed-label digest separates from the
canonical positive target.

They are not positive generator source unless a future contract explicitly
promotes such a role.

## Support mode fixture family

The support mode fixture family currently lives in:

- fixtures/json/fre_support_mode_fixture_set_v0.1.json

The fixture set has:

- fixture_set_id: fre.support_mode.fixture_set.v0.1
- contract_id: fre.support_mode.regularity.v0.1
- receipt_schema: fre.support_mode.receipt.v0.1
- status: mixed_certification
- fixture count: 6

The fixture set includes both certified geometric fixtures and algebraic
controls.

A sample certified fixture is `regular_uniform_10`, with all six support
coordinates equal to 10, expected K equal to 0, and certification inside C_D.

## Mixed certification

The support mode fixture set is mixed certification.

That means not every fixture carries the same claim authority.

Certified fixtures may earn scoped geometric regularity claims when the
contract, gate, execution, comparison, receipt, and audit all support that
result.

Algebraic control fixtures may still compute correctly while leaving the
geometric regularity claim unavailable.

This distinction is why some support mode receipts are earned and others are
unavailable even when reference congruence is true.

## Placeholder fixture folder

The file:

- fixtures/json/.gitkeep

keeps the JSON fixture folder present in git.

It has no protocol meaning beyond preserving the directory structure.

## Fixture use by gates

Fixture access should be controlled by gates.

Examples:

- The native G900 generator gate may read G15, G60, and carrier signing source
  fixtures.
- The native G900 generator gate must not read the flattened target fixture.
- The target canonicalization gate may read the flattened target fixture.
- Sibling-control gates may read sibling-control fixture material.
- Support mode gates may read the declared public fixture set.

When a tool needs fixture access, the SysOp should inspect the gate before
running it.

## Fixture mutation rule

Fixtures should be treated as stable source material.

Changing a fixture may invalidate contracts, gates, audits, receipts, digests,
or notes. A fixture change should therefore be deliberate and receipted through
a new contract, revision, audit, or checkpoint.

Do not silently edit a fixture to make a later check pass.

## Fixture is not execution

Fixtures do not execute themselves.

A fixture can be well-formed, hash-bound, or structurally useful without
admitting a claim. Execution authority comes from a contract or gate. Public
truth comes from receipts and audits.

## Boundary

This section documents fixtures and source material only.

It does not modify fixtures.

It does not admit fixture reads for any tool.

It does not run a generator, canonicalizer, backend, or audit.

It does not promote target material into source material.

It does not promote sibling-control material into positive source material.

It does not create production security, observational closure, recursive host
admission, graph transport, external truth, physical interpretation, geometry,
force, or a universal theorem claim.
