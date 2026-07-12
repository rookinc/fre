#!/usr/bin/env python3
"""Record the one-shot plaintext G900 bounce reference."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = Path.home() / "tmp/fre_g900_bounce_reference_run_001.json"
ARTIFACT = ROOT / "artifacts/json/fre_g900_bounce_reference_audit_001.json"

LOCKS = {
    "contracts/fre_g900_bounce_grammar_v0.1.json":
        "80ac01520f3cc229425dd925a11efdda2c82d3a3fb8e9eead3fb424f86e66cfe",
    "contracts/fre_g900_bounce_reference_execution_gate_v0.1.json":
        "9a9644ebeb939740b830f149e2086ae90e16e0cee7c5e22fcfbdd3b8e5d695d8",
    "tools/run_g900_bounce_reference.py":
        "2d3c78d6ebe199bc394d980bfb413a31f55fb153c795e670e8d7525ab1074af3",
    "artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json":
        "4b755358bde7e3407693d33b88ca7c0c4aff9e0ba4436331f99e3b7254ae16a5",
}
CAPTURE_HASH = "0bbca88737e20904fbba9cef76e1a9e76eeb78a1bc3c9f0a0586a4ea3c1d71de"
TRACE_HASH = "841e7bec36225dd83a069f252f41bab206e3d21be2d04dad4ae41b33717fe467"
RECEIPT_HASH = "1ee381695c107e5f28f43940348504fad6fb9c363fbfc29711143e7226b7a446"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    observed = json.loads(CAPTURE.read_text(encoding="ascii"))
    final = observed.get("final_state", {})
    internal = observed.get("checks", {})

    checks = {
        "capture_hash_locked": digest(CAPTURE) == CAPTURE_HASH,
        "pipeline_id_exact":
            observed.get("pipeline_id")
            == "fre.g900.bounce_reference.v0.1",
        "contract_id_exact":
            observed.get("contract_id")
            == "fre.g900.bounce_grammar.v0.1",
        "cycle_t_zero": observed.get("cycle_t") == 0,
        "phase_measure_exact":
            observed.get("phase_measure") == "360+180+360=900",
        "states_901": observed.get("state_count") == 901,
        "transitions_900":
            observed.get("transition_count") == 900,
        "source_zero_target_ninety":
            observed.get("source_vertex") == 0
            and observed.get("target_vertex") == 90,
        "trace_hash_locked":
            observed.get("trace_sha256") == TRACE_HASH,
        "receipt_id_I0": observed.get("receipt_id") == "I_0",
        "receipt_hash_locked":
            observed.get("receipt_sha256") == RECEIPT_HASH,
        "return_to_source":
            final.get("phase_tick") == 900
            and final.get("vertex_role") == "source",
        "slip_closed": final.get("G30_slip_bit") == 0,
        "chamber_lock_persisted":
            final.get("G60_chamber_lock") == 1,
        "receipt_present":
            final.get("receipt_state") == "I_0",
        "all_internal_checks_pass":
            bool(internal) and all(internal.values()),
        "physical_claim_false":
            observed.get("physical_claim") is False,
        "reference_not_rerun_by_audit": True,
    }
    for path, expected in LOCKS.items():
        checks["binding_" + Path(path).stem] = (
            (ROOT / path).is_file()
            and digest(ROOT / path) == expected
        )

    audit_pass = all(checks.values())
    artifact = {
        "artifact_id":
            "fre.g900.bounce_reference.audit.001",
        "status":
            "plaintext_900_transition_bounce_reference_recorded",
        "bindings": {
            "capture_sha256": CAPTURE_HASH,
            "grammar_contract_sha256": LOCKS[
                "contracts/fre_g900_bounce_grammar_v0.1.json"
            ],
            "execution_gate_sha256": LOCKS[
                "contracts/fre_g900_bounce_reference_execution_gate_v0.1.json"
            ],
            "reference_source_sha256": LOCKS[
                "tools/run_g900_bounce_reference.py"
            ],
            "native_generator_checkpoint_sha256": LOCKS[
                "artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json"
            ],
        },
        "run": {
            "run_id": "fre.g900.bounce_reference.run.001",
            "maximum_invocations": 1,
            "reference_rerun_by_audit": False,
            "observed": observed,
        },
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "900_transition_reference_bounce_returns_to_source_"
            "with_receipt_distinguished_state"
            if audit_pass else
            "bounce_reference_audit_failed"
        ),
        "receipt": {
            "receipt_id": "I_0",
            "trace_sha256": TRACE_HASH,
            "receipt_sha256": RECEIPT_HASH,
            "classification": "reference_receipt_candidate",
            "public_recursive_host_receipt": False,
        },
        "claim_scope": {
            "plaintext_reference_trace": True,
            "same_final_vertex": True,
            "same_final_automaton_state": False,
            "graph_transport_execution_claim": False,
            "recursive_host_claim": False,
            "universal_all_vertex_claim": False,
        },
        "boundary": {
            "graph_payload_read": False,
            "independent_bridge_present": False,
            "recursive_host_admitted": False,
            "public_receipt_emitted": False,
            "observational_closure": False,
            "physical_claim": False,
            "external_truth_claim": False,
        },
    }
    ARTIFACT.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps({
        "artifact_id": artifact["artifact_id"],
        "audit_pass": audit_pass,
        "receipt_id": artifact["receipt"]["receipt_id"],
        "trace_sha256": TRACE_HASH,
        "verdict": artifact["verdict"],
    }, sort_keys=True))
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
