# FRE Documentation

FRE means Folded Receipt Envelope.

This directory contains the structured documentation spine for the FRE protocol
repository. It is intended for ED and SysOp use.

## Reading order

1. 00-overview-and-continuity.md
2. 01-folded-receipt-envelope-model.md
3. 02-contracts-and-gates.md
4. 03-receipts-and-schemas.md
5. 04-audit-layer.md
6. 05-fixtures-and-source-material.md
7. 06-support-mode-reference-system.md
8. 07-g900-envelope-workflow.md
9. 08-openfhe-backend-boundary.md
10. 09-cli-build-and-test-surface.md
11. 10-tool-index.md
12. 11-notes-and-human-checkpoints.md
13. 12-artifact-index.md
14. 13-sysop-runbook.md
15. 14-glossary.md
16. 15-repository-map.md

## Steward split

ED stewards:

- meaning
- continuity
- claim language
- workflow framing
- glossary
- public orientation

SysOp stewards:

- contracts
- gates
- schemas
- fixtures
- receipts
- artifacts
- audits
- tools
- builds
- repository coverage

## Core rule

Capability is not authority.

A file can exist, a binary can build, and a tool can run without being admitted.
Contracts and gates admit action. Receipts record action. Audits check action.

## Documentation boundary

These documents do not admit new behavior.

They do not emit receipts, run audits, consume one-shot gates, or promote any
claim beyond the underlying contracts, receipts, and artifacts.
