# G900 Bounce Checkpoint 001

## Scope

This checkpoint records one bounded plaintext reference automaton for the
current cycle `t=0`. One oriented signed carrier edge is used: vertex `0` to
vertex `90`.

The phase grammar is:

- 360 outward symbolic ticks;
- 180 turnaround symbolic ticks; and
- 360 return symbolic ticks.

The resulting trace has 900 transitions and 901 states. These counts are a
symbolic grammar. They are not a physical-angle claim and not a time claim.

## Positive reference result

The positive reference run completed exactly once.

- `G30` records the slip bit.
- `G60` preserves the chamber lock.
- The trace returns to source vertex `0` after 900 transitions.
- The final automaton state is distinct from the initial state because the
  chamber lock persists and receipt state `I_0` exists.
- `I_0` is only a plaintext reference-receipt candidate. It is not a public
  recursive-host receipt.

Locked positive evidence:

- runtime capture SHA-256:
  `0bbca88737e20904fbba9cef76e1a9e76eeb78a1bc3c9f0a0586a4ea3c1d71de`
- trace SHA-256:
  `841e7bec36225dd83a069f252f41bab206e3d21be2d04dad4ae41b33717fe467`
- `I_0` SHA-256:
  `1ee381695c107e5f28f43940348504fad6fb9c363fbfc29711143e7226b7a446`
- positive audit artifact SHA-256:
  `63064b56d350a2c434c70ad9ab9a481f2d2633bcd26888f6625e04fbc4c04879`

## Five negative controls

The five-case negative-control suite also completed exactly once. Every case
was rejected for its predeclared reason, no control receipt was emitted, and
return to the same vertex was explicitly insufficient.

| Case | Mutation | Predeclared rejection reason |
| --- | --- | --- |
| `wrong_phase_total` | 899 total ticks | `phase_partition_must_equal_360_180_360` |
| `receiptless_return` | source return without `I_0` | `receipt_I_0_required_at_completion` |
| `wrong_half_flip` | target vertex `89` | `signed_half_flip_endpoint_mismatch` |
| `alternate_edge` | target vertex `270` | `oriented_edge_not_admitted_for_cycle_000` |
| `unlocked_return` | final `G60` lock is zero | `G60_chamber_lock_must_persist` |

Observed suite result:

- case count: 5;
- rejected count: 5;
- accepted count: 0;
- all expected rejections: true;
- every `receipt_emitted` value: false;
- `same_vertex_is_not_sufficient`: true;
- `control_receipts_emitted`: false; and
- `physical_claim`: false.

Locked negative evidence:

- runtime capture SHA-256:
  `dd7dc2d8f39703132360604171f9dd1b7ccc01801353502ff3ca26c33f2239f6`
- negative-control audit artifact SHA-256:
  `cf01428ed0c43ce5a488eab737074658ad22ed13e91b4052406fa3485f5bfb44`

The one-shot markers and runtime captures remain under `~/tmp`. They are
preserved evidence and are not repository publication files.

## Claim boundary

This checkpoint does not claim or admit:

- graph-payload transport;
- an independent bridge;
- a public host receipt;
- recursive-host admission;
- a universal all-vertex result;
- observational closure;
- an external truth claim;
- a physical-angle or time interpretation; or
- a graph non-isomorphism theorem.

The earlier generator-target congruence and sibling fixed-label negative
control remain bounded results. This bounce checkpoint does not broaden them.
