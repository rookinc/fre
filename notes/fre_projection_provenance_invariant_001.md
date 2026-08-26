# FRE projection-provenance invariant 001

## Status

projection_provenance_invariant_established

## Purpose

Abstract the common bounded protocol structure established independently by
the committed G900 and OpenFHE projection witnesses.

No G900 execution is performed here.

No OpenFHE execution is performed here.

No cryptographic private body is read.

## Formal schema

Let X be a registered FRE state space.

Let Y be a public projection space.

Let

    pi: X -> Y

be a public projection.

Let

    ~_FRE

denote the relevant registered protocol congruence relation.

The witnessed form is

    exists x,x' in X

such that

    pi(x) = pi(x')

while

    not(x ~_FRE x').

Equivalently,

    public projection equality
        does not imply
    registered protocol congruence.

## G900 instance

The committed G900 witness uses

    pi_vertex(s) = s.vertex

The reference bounce returns to the same endpoint while retaining registered
phase, chamber-lock, and receipt distinctions.

Existing negative controls show that the forgotten distinctions participate
in FRE congruence and refusal.

## OpenFHE instance

The committed OpenFHE witness uses

    pi_payload_shape(h) = h.payload_shape

Three registered handle states share the same payload-shape projection.

Their handle identities, operation digests, and parent histories remain
distinct.

Existing FRE binding and refusal rules depend on those distinctions.

## Invariant

The two systems are not asserted to be equivalent.

What they establish jointly is the bounded FRE protocol invariant:

    A lossy public projection cannot substitute for registered provenance
    when FRE decides congruence.

The important object is therefore not merely the public projected value.

The protocol state also contains registered provenance whose relevance
survives projection.

## Fibre interpretation

For a public value y in Y, define the set-theoretic fibre

    pi^-1(y) = {x in X : pi(x) = y}.

The current witnesses establish that at least one such fibre may contain
states that are distinct under FRE congruence.

Therefore a projection fibre is not automatically a congruence class.

That distinction is now the central structural frontier.

## Requirements

- R1_both_source_witnesses_pass: true
- R2_both_sources_define_explicit_lossy_projections: true
- R3_both_projections_are_noninjective_on_witnessed_sets: true
- R4_projection_equality_does_not_imply_FRE_congruence: true
- R5_discarded_provenance_is_operationally_relevant: true
- R6_no_new_execution_required: true
- R7_no_physical_claim_imported: true
- R8_no_G900_OpenFHE_equivalence_imported: true

## What is earned

- public projection equality does not imply registered protocol congruence
- a public projection may be noninjective over operationally distinct registered states
- registered provenance may remain FRE-relevant after public projection coordinates coincide
- FRE congruence is not determined by the witnessed public projection alone
- G900 and OpenFHE provide two bounded instances of the same projection-provenance schema

## What is not earned

This artifact does not establish that every FRE projection has this property.

It does not establish a universal FRE theorem.

It does not establish equivalence between G900 and OpenFHE.

It does not establish a group action.

It does not establish a group representation.

It does not establish a fibre group.

It does not establish a covering space, bundle, or topological cover.

It does not establish the planned Paper 13 representation theorem.

It does not establish cryptographic security.

It does not make a physical claim.

## Next structural question

The next question is no longer whether projection fibres can contain
operationally distinct registered states.

They can, on the two witnessed surfaces.

The next question is:

    What, if any, algebraic structure organizes the retained distinctions
    inside a witnessed FRE projection fibre?

That question must be answered from existing registered transitions,
composition laws, admissibility relations, or receipt-preserving maps.

Group structure must not be assumed merely because a fibre exists.

## Keeper

Projection may forget provenance. FRE congruence may not.

## Next gate

fre_projection_fibre_structure_scout_001
