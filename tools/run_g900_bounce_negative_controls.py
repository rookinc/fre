#!/usr/bin/env python3
"""Evaluate the five predeclared G900 bounce negative controls."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/fre_g900_bounce_negative_controls_v0.1.json"
CONTRACT_HASH = "5ba5491f131bd5ec4726aa83b80b6c0e19b8155d7a740519205bd04be2a1f140"
PIPELINE_ID = "fre.g900.bounce_negative_controls.reference.v0.1"


def load_contract():
    raw = CONTRACT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONTRACT_HASH:
        raise RuntimeError("negative-control contract hash mismatch")
    value = json.loads(raw.decode("ascii"))
    if value.get("contract_id") != (
        "fre.g900.bounce_negative_controls.v0.1"
    ):
        raise RuntimeError("negative-control contract id mismatch")
    return value


def evaluate(case):
    case_id = case["case_id"]
    mutation = case["mutation"]

    if case_id == "wrong_phase_total":
        accepted = (
            mutation["outward"] == 360
            and mutation["turnaround"] == 180
            and mutation["return"] == 360
            and mutation["total"] == 900
        )
        reason = (
            "accepted"
            if accepted
            else "phase_partition_must_equal_360_180_360"
        )

    elif case_id == "receiptless_return":
        accepted = (
            mutation["final_vertex"] == 0
            and mutation["final_lock"] == 1
            and mutation["final_receipt_state"] == "I_0"
        )
        reason = (
            "accepted"
            if accepted
            else "receipt_I_0_required_at_completion"
        )

    elif case_id == "wrong_half_flip":
        expected_local = (
            mutation["local_from"] + 30
        ) % 60
        expected_vertex = (
            60 * mutation["slot_to"] + expected_local
        )
        accepted = (
            mutation["local_to"] == expected_local
            and mutation["target_vertex"] == expected_vertex
        )
        reason = (
            "accepted"
            if accepted
            else "signed_half_flip_endpoint_mismatch"
        )

    elif case_id == "alternate_edge":
        admitted = {
            "slot_from": 0,
            "local_from": 0,
            "slot_to": 1,
            "local_to": 30,
            "target_vertex": 90,
        }
        accepted = all(
            mutation.get(key) == value
            for key, value in admitted.items()
        )
        reason = (
            "accepted"
            if accepted
            else "oriented_edge_not_admitted_for_cycle_000"
        )

    elif case_id == "unlocked_return":
        accepted = (
            mutation["final_vertex"] == 0
            and mutation["final_slip_bit"] == 0
            and mutation["final_lock"] == 1
            and mutation["final_receipt_state"] == "I_0"
        )
        reason = (
            "accepted"
            if accepted
            else "G60_chamber_lock_must_persist"
        )

    else:
        raise RuntimeError("unknown negative-control case")

    return {
        "case_id": case_id,
        "accepted": accepted,
        "reason": reason,
        "matches_predeclared_result":
            accepted == case["expected_accepted"]
            and reason == case["expected_reason"],
        "receipt_emitted": False,
    }


def main():
    contract = load_contract()
    cases = contract["suite"]["cases"]
    results = [evaluate(case) for case in cases]
    rejected = sum(not result["accepted"] for result in results)
    accepted = sum(result["accepted"] for result in results)

    summary = {
        "pipeline_id": PIPELINE_ID,
        "contract_id": contract["contract_id"],
        "suite_id": contract["suite"]["suite_id"],
        "case_count": len(results),
        "rejected_count": rejected,
        "accepted_count": accepted,
        "all_expected_rejections":
            rejected == 5
            and accepted == 0
            and all(
                result["matches_predeclared_result"]
                for result in results
            ),
        "same_vertex_is_not_sufficient": True,
        "control_receipts_emitted": False,
        "results": results,
        "physical_claim": False,
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
