# FRE G900 endpoint-projection fibre witness 001

## Status

endpoint_projection_fibre_witness_established

## Purpose

Record the smallest currently earned FRE statement that endpoint identity does
not determine registered-state identity.

The witness is derived from the already completed G900 plaintext bounce
reference and its negative controls. No new G900 execution is performed here.

## Projection

Let a registered state be written schematically as

    s = (v, phase, edge, slip, chamber_lock, receipt_history, ...)

Define the endpoint projection

    pi_vertex(s) = v

The projection intentionally forgets registered information other than the
endpoint vertex.

## Witness

The reference bounce returns to its source vertex after 900 transitions.

The returned registered state nevertheless retains:

- phase_tick = 900
- G30_slip_bit = 0
- G60_chamber_lock = 1
- receipt_state = I_0

The source and returned states therefore have the same endpoint projection
while the audited reference explicitly records that they are not the same final
automaton state.

Thus, on the witnessed registered-state set,

    s != t
    pi_vertex(s) = pi_vertex(t)

and therefore pi_vertex is non-injective on that witnessed set.

## Operational relevance

The fibre distinction is not merely descriptive.

The negative-control family records that same vertex is not sufficient.
In particular:

- receiptless_return is refused because receipt I_0 is required at completion.
- unlocked_return is refused because the G60 chamber lock must persist.

The grammar independently records both cases as non-congruent.

Therefore information discarded by pi_vertex participates in FRE congruence
and refusal.

The stronger bounded statement earned here is:

    endpoint equality does not imply receipt congruence

## Fibre language

For this artifact, fibre means only the inverse-image set

    pi_vertex^-1(v)

of registered states sharing endpoint v.

No topological or geometric structure is inferred from the word fibre.

## Requirements

- R1_reference_returns_to_source: true
- R2_returned_state_retains_registered_distinction: true
- R3_same_vertex_negative_control_rule_present: true
- R4_endpoint_sharing_controls_reject_or_fail_congruence: true
- R5_rejection_depends_on_nonendpoint_registered_information: true
- R6_private_crypto_body_not_required_for_witness: true

## Boundary

This artifact establishes one bounded endpoint-projection witness.

It does not establish a group action.

It does not establish a group representation.

It does not establish a covering space or topological cover.

It does not establish a cryptographic security theorem.

It does not admit recursive hosting or graph transport.

It does not establish observational closure or external truth.

It does not make a physical claim.

It does not establish a universal theorem for every possible G900 state.

## Keeper

A returned endpoint does not erase the receipt history that earned the return.

## Next gate

fre_openfhe_endpoint_projection_conformance_scout_001
