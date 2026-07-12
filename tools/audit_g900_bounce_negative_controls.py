#!/usr/bin/env python3
"""Audit the preserved one-shot G900 bounce negative-control capture."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MARKER = (
    Path.home()
    / "tmp/fre_g900_bounce_negative_controls_run_001.attempted"
)
CAPTURE = (
    Path.home()
    / "tmp/fre_g900_bounce_negative_controls_run_001.json"
)
ARTIFACT = (
    ROOT
    / "artifacts/json/fre_g900_bounce_negative_controls_audit_001.json"
)

MARKER_HASH = (
    "24b8430cb87ef91aa9afb5c94482f277ec674df9d455e13e6a1ef88ce6bc2059"
)
CAPTURE_HASH = (
    "dd7dc2d8f39703132360604171f9dd1b7ccc01801353502ff3ca26c33f2239f6"
)
LOCKS = {
    "contracts/fre_g900_bounce_grammar_v0.1.json":
        "80ac01520f3cc229425dd925a11efdda2c82d3a3fb8e9eead3fb424f86e66cfe",
    "artifacts/json/fre_g900_bounce_reference_audit_001.json":
        "63064b56d350a2c434c70ad9ab9a481f2d2633bcd26888f6625e04fbc4c04879",
    "contracts/fre_g900_bounce_negative_controls_v0.1.json":
        "5ba5491f131bd5ec4726aa83b80b6c0e19b8155d7a740519205bd04be2a1f140",
    "tools/run_g900_bounce_negative_controls.py":
        "ee58cbf554508841909f0bba46686ce57b75f03112c39b9d7014df8e9ba0facc",
    "contracts/fre_g900_bounce_negative_control_execution_gate_v0.1.json":
        "232c858ee264d5f15db42c8f19ce2c84c090faf35da9feb3890e4f9b8b424771",
}
EXPECTED_RESULTS = [
    {
        "accepted": False,
        "case_id": "wrong_phase_total",
        "matches_predeclared_result": True,
        "reason": "phase_partition_must_equal_360_180_360",
        "receipt_emitted": False,
    },
    {
        "accepted": False,
        "case_id": "receiptless_return",
        "matches_predeclared_result": True,
        "reason": "receipt_I_0_required_at_completion",
        "receipt_emitted": False,
    },
    {
        "accepted": False,
        "case_id": "wrong_half_flip",
        "matches_predeclared_result": True,
        "reason": "signed_half_flip_endpoint_mismatch",
        "receipt_emitted": False,
    },
    {
        "accepted": False,
        "case_id": "alternate_edge",
        "matches_predeclared_result": True,
        "reason": "oriented_edge_not_admitted_for_cycle_000",
        "receipt_emitted": False,
    },
    {
        "accepted": False,
        "case_id": "unlocked_return",
        "matches_predeclared_result": True,
        "reason": "G60_chamber_lock_must_persist",
        "receipt_emitted": False,
    },
]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    observed = json.loads(CAPTURE.read_text(encoding="ascii"))
    marker = json.loads(MARKER.read_text(encoding="ascii"))
    results = observed.get("results", [])

    checks = {
        "marker_hash_locked": digest(MARKER) == MARKER_HASH,
        "capture_hash_locked": digest(CAPTURE) == CAPTURE_HASH,
        "marker_run_id_exact":
            marker.get("run_id")
            == "fre.g900.bounce_negative_controls.run.001",
        "marker_command_exact":
            marker.get("command")
            == "python tools/run_g900_bounce_negative_controls.py",
        "marker_branch_main": marker.get("branch") == "main",
        "marker_head_locked":
            marker.get("head")
            == "6f3cf24ee6d2fff847a223104f43bff1231a69c3",
        "pipeline_id_exact":
            observed.get("pipeline_id")
            == "fre.g900.bounce_negative_controls.reference.v0.1",
        "contract_id_exact":
            observed.get("contract_id")
            == "fre.g900.bounce_negative_controls.v0.1",
        "suite_id_exact":
            observed.get("suite_id")
            == "fre.g900.bounce_negative_controls.suite.001",
        "case_count_five": observed.get("case_count") == 5,
        "rejected_count_five": observed.get("rejected_count") == 5,
        "accepted_count_zero": observed.get("accepted_count") == 0,
        "all_expected_rejections":
            observed.get("all_expected_rejections") is True,
        "results_exact": results == EXPECTED_RESULTS,
        "all_results_rejected":
            len(results) == 5
            and all(result.get("accepted") is False for result in results),
        "all_predeclared_results_match":
            len(results) == 5
            and all(
                result.get("matches_predeclared_result") is True
                for result in results
            ),
        "no_control_receipts":
            observed.get("control_receipts_emitted") is False
            and len(results) == 5
            and all(
                result.get("receipt_emitted") is False
                for result in results
            ),
        "same_vertex_not_sufficient":
            observed.get("same_vertex_is_not_sufficient") is True,
        "physical_claim_false":
            observed.get("physical_claim") is False,
        "negative_evaluator_not_rerun_by_audit": True,
    }
    for path, expected in LOCKS.items():
        checks["binding_" + Path(path).stem] = (
            (ROOT / path).is_file()
            and digest(ROOT / path) == expected
        )

    audit_pass = all(checks.values())
    artifact = {
        "artifact_id":
            "fre.g900.bounce_negative_controls.audit.001",
        "status":
            "five_predeclared_bounce_negative_controls_recorded",
        "bindings": {
            "marker_sha256": MARKER_HASH,
            "capture_sha256": CAPTURE_HASH,
            "grammar_contract_sha256": LOCKS[
                "contracts/fre_g900_bounce_grammar_v0.1.json"
            ],
            "positive_reference_audit_sha256": LOCKS[
                "artifacts/json/fre_g900_bounce_reference_audit_001.json"
            ],
            "negative_control_contract_sha256": LOCKS[
                "contracts/fre_g900_bounce_negative_controls_v0.1.json"
            ],
            "control_source_sha256": LOCKS[
                "tools/run_g900_bounce_negative_controls.py"
            ],
            "execution_gate_sha256": LOCKS[
                "contracts/fre_g900_bounce_negative_control_execution_gate_v0.1.json"
            ],
        },
        "run": {
            "run_id": "fre.g900.bounce_negative_controls.run.001",
            "maximum_invocations": 1,
            "negative_evaluator_rerun_by_audit": False,
            "marker": marker,
            "observed": observed,
        },
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "five_predeclared_bounce_negative_controls_rejected_without_receipts"
            if audit_pass
            else "bounce_negative_control_audit_failed"
        ),
        "receipt_policy": {
            "control_receipts_emitted": False,
            "public_recursive_host_receipt": False,
        },
        "claim_scope": {
            "automaton_sensitivity_controls_only": True,
            "same_vertex_is_not_sufficient": True,
            "graph_transport_execution_claim": False,
            "recursive_host_claim": False,
            "universal_all_vertex_claim": False,
        },
        "boundary": {
            "independent_bridge_present": False,
            "public_receipt_emitted": False,
            "recursive_host_admitted": False,
            "observational_closure": False,
            "physical_claim": False,
            "external_truth_claim": False,
        },
    }
    with ARTIFACT.open("x", encoding="ascii") as handle:
        handle.write(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n"
        )

    print(json.dumps({
        "artifact_id": artifact["artifact_id"],
        "audit_pass": audit_pass,
        "case_count": observed.get("case_count"),
        "rejected_count": observed.get("rejected_count"),
        "accepted_count": observed.get("accepted_count"),
        "verdict": artifact["verdict"],
    }, sort_keys=True))
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
