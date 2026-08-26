# FRE OpenFHE endpoint-projection conformance witness 001

## Status

openfhe_endpoint_projection_conformance_witness_established

## Purpose

Record the OpenFHE-side conformance witness for the bounded FRE principle
already exposed by the G900 endpoint-projection fibre witness.

No OpenFHE computation is executed here.

This artifact uses existing public handle receipts, packet receipts,
validation artifacts, refusal rules, and negative controls.

## Projection

Let h denote a registered public ciphertext-handle receipt state.

Define

    pi_payload_shape(h) = h.payload_shape

For the witnessed EvalMult handle family,

    pi_payload_shape(h_a)
      = pi_payload_shape(h_b)
      = pi_payload_shape(h_out)
      = packed_int64_8

The projection therefore forgets registered distinctions among the three
handle states.

## Retained distinctions

The fibre members retain distinct public provenance.

They have distinct handle identities and operation digests.

The EvalMult output also has a registered parent history

    [h_a, h_b]

while the two encrypted input handles have empty parent histories.

No ciphertext bytes are needed to observe these distinctions.

## Operational relevance

Existing FRE/Aletheos rules require the retained provenance.

The EvalMult packet template states that parent handles must bind the output
handle to the input handles.

The OpenFHE adapter boundary states that an output handle not bound to its
input handles and circuit digest must be refused.

Existing negative-control surfaces already record refusal for output-handle
and input-output-binding mismatches.

Thus the discarded information is not merely descriptive metadata.

It participates in FRE validation and refusal.

## Positive witness

The completed EvalMult packet has exact registered parent binding.

Its output handle names the same two input handles recorded by the packet.

The existing verification receipt also records verify_pass=true and exact
agreement between expected and actual result.

## Bounded conclusion

On the witnessed OpenFHE public receipt surface,

    payload-shape equality
        does not imply
    registered-handle equality

and

    payload-shape equality
        does not determine
    parent provenance.

Because FRE already requires that provenance for binding and refusal,

    payload-shape equality alone
        is insufficient for FRE congruence.

## Cross-domain FRE invariant

The G900 witness and the OpenFHE witness are not asserted to be equivalent
systems.

They instantiate the same bounded protocol principle:

    A lossy public projection cannot substitute for registered provenance
    when FRE decides congruence.

In G900, endpoint projection forgets phase, lock, and receipt history.

In OpenFHE, payload-shape projection forgets handle identity, operation
digest, and parent provenance.

In both cases, information discarded by the projection remains operationally
relevant to the receipt apparatus.

## Requirements

- R1_multiple_registered_states_share_payload_shape: true
- R2_public_registered_provenance_distinguishes_fibre_members: true
- R3_existing_FRE_rule_requires_handle_parent_binding: true
- R4_existing_negative_controls_refuse_binding_mismatch: true
- R5_positive_packet_has_exact_binding_and_verified_receipt: true

## Boundary

This is a conformance witness over existing evidence.

It does not execute OpenFHE.

It does not read ciphertext bytes.

It does not generate keys.

It does not encrypt, evaluate, or decrypt.

It does not establish equivalence between G900 and OpenFHE.

It does not establish a group action or group representation.

It does not establish a covering space or topological cover.

It does not establish the planned Paper 13 representation theorem.

It does not establish cryptographic security.

It does not make a physical claim.

## Keeper

The public shape may coincide. The receipt history still decides what the
coincidence means.

## Next gate

fre_projection_provenance_invariant_001
