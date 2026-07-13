# 13 SysOp Runbook

Steward: SysOp

Status: Draft

## Purpose

This section gives the operating procedure for FRE.

The SysOp keeps the Folded Receipt Envelope system honest in practice. The
SysOp checks contracts, runs only admitted actions, preserves private/public
boundaries, validates receipts, audits artifacts, and records continuity.

## Section scope

Owned scope:

- README.md
- fre_continuity.md
- contracts/
- schemas/
- artifacts/
- fixtures/
- include/
- src/
- tools/
- notes/
- CMakeLists.txt
- build/
- build-openfhe-link/
- docs/13-sysop-runbook.md

Reference scope:

- docs/00-overview-and-continuity.md
- docs/01-folded-receipt-envelope-model.md
- docs/02-contracts-and-gates.md
- docs/03-receipts-and-schemas.md
- docs/04-audit-layer.md
- docs/05-fixtures-and-source-material.md
- docs/06-support-mode-reference-system.md
- docs/07-g900-envelope-workflow.md
- docs/08-openfhe-backend-boundary.md
- docs/09-cli-build-and-test-surface.md
- docs/10-tool-index.md
- docs/11-notes-and-human-checkpoints.md
- docs/12-artifact-index.md

## Core rule

Capability is not authority.

A file can exist, a binary can build, and a tool can run without being admitted.

The SysOp must identify the admitting contract or gate before execution.

## Start of session

At the start of a FRE work session:

1. Read fre_continuity.md.
2. Read README.md.
3. Read notes/boundary.md.
4. Check git status.
5. Identify the current task.
6. Identify the relevant documentation section.
7. Identify the relevant contract, gate, receipt schema, fixture, tool, and
   audit artifact.
8. Confirm the boundary before running anything.

## Git check

Run a status check before editing or executing.

The SysOp should know:

- which files are untracked
- which files are modified
- which changes are from the current task
- whether generated build products changed
- whether unrelated changes should be left alone

Do not revert unrelated work unless explicitly directed.

## Contract and gate check

Before running a tool, check:

1. Which contract or gate admits this action?
2. What exact command is allowed?
3. What files may be read?
4. What files are forbidden?
5. What writes are allowed?
6. What is the maximum invocation count?
7. Where does runtime capture go?
8. May runtime capture be committed?
9. What receipt, audit, or artifact is expected?
10. Which claims remain false even if the run passes?

If any answer is missing, pause.

## Fixture check

Before using fixtures, check:

- Is this source material, target material, or control material?
- Does the gate admit this fixture read?
- Is the fixture hash-bound?
- Is the fixture certified or mixed-certification?
- Could this fixture leak the answer into the run?

Target fixtures and source fixtures must not be casually mixed.

## Build check

Before building:

- Confirm whether OpenFHE should be enabled.
- Confirm whether FRE_ENABLE_OPENFHE is ON or OFF.
- If OpenFHE is enabled, confirm FRE_OPENFHE_PREFIX.
- Treat build directories as generated operational evidence.
- Do not treat build outputs as source authority.

## Execution check

Before execution:

- Confirm the run is admitted.
- Confirm the command matches the gate.
- Confirm maximum invocation count.
- Confirm runtime capture path.
- Confirm private material rules.
- Confirm expected post-run audit.

After execution:

- Preserve the runtime capture.
- Do not commit runtime private body material.
- Run the expected audit if the protocol path requires it.
- Record failures without broadening the claim.

## Receipt check

Before emitting receipts:

- Confirm the receipt schema.
- Confirm the contract and gate.
- Confirm the execution audit or source event.
- Confirm claim status.
- Confirm privacy rules.
- Confirm closure class.
- Confirm boundary language.

After emitting receipts:

- Validate against schema.
- Run the receipt audit if required.
- Confirm earned versus unavailable claims.
- Confirm no private material was committed.

## Audit check

Before relying on an audit:

- Confirm the audit tool.
- Confirm the output artifact.
- Confirm locked hashes.
- Confirm audit_pass.
- Read the verdict.
- Read the boundary.
- Check whether a later artifact depends on this one.

An audit pass does not erase the boundary.

## Commit check

Before committing:

1. Inspect git status.
2. Stage only intended files.
3. Review staged diff.
4. Confirm no private body material is staged.
5. Confirm docs, contracts, receipts, artifacts, and notes do not overclaim.
6. Use a clear commit message.
7. Confirm final status after commit.

Do not include runtime captures, secret keys, ciphertexts, raw OpenFHE runtime
objects, or undeclared intermediate values.

## Stop conditions

Stop and ask for ED direction when:

- no contract or gate admits the requested action
- a forbidden read appears necessary
- a one-shot gate appears already consumed
- private body material would need to be committed
- a receipt claim would exceed its schema or source certification
- an audit fails
- a hash-bound file changed unexpectedly
- a note and contract disagree
- a proposed claim would imply observational closure, production security,
  recursive hosting, graph transport, physical interpretation, geometry, force,
  or a universal theorem without explicit admission

## Common safe outputs

Safe SysOp outputs include:

- inspect reports
- documentation drafts
- boundary notes
- contract drafts
- schema drafts
- audit reports
- receipt validation summaries
- git status summaries
- next-step checklists

Even safe outputs should preserve the public/private boundary.

## Private body rule

Do not commit:

- secret inputs
- secret keys
- ciphertexts
- raw OpenFHE runtime objects
- undeclared intermediate values

If unsure, treat the material as private body until a contract or ED decision
states otherwise.

## Public face rule

The public face may include:

- contracts
- schemas
- operation names
- source-class identifiers
- tolerance declarations
- claim-relative results
- verification status
- negative-control status
- boundary language

Public face material should be finite, inspectable, and bounded.

## End of session

At the end of a FRE work session:

1. Summarize what changed.
2. Summarize what was not changed.
3. State whether tests or audits were run.
4. State any untracked or modified files.
5. Record the next recommended step.
6. Preserve the boundary.

## Boundary

This runbook documents SysOp procedure only.

It does not admit execution.

It does not consume gates.

It does not emit receipts.

It does not run audits.

It does not create production security, observational closure, external truth,
recursive-host admission, graph transport, physical interpretation, geometry,
force, or a universal theorem claim.
