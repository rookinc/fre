#!/usr/bin/env python3
"""Record the locked first native G900 generator observation."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = Path.home() / "tmp/fre_g900_native_generator_run_001.json"
ARTIFACT = ROOT / "artifacts/json/fre_g900_native_generator_execution_audit_001.json"

LOCKS = {
    "contracts/fre_g900_native_generator_v0.1.json":
        "be609a89f694eff192cbc0ee7edda255f9efe930c33c6146ab0ae57ebebc0282",
    "contracts/fre_g900_native_generator_execution_gate_v0.1.json":
        "705ef4aa1c07f21a01c75240aaf9830177b62229b6173597a3492b2cc1f59a23",
    "tools/generate_g900_kernel.py":
        "f695b4ce6eee5a5bfde7ec2373ceb5511b758e0cf6ef9d02e5e2d8782e59f6a7",
}
CAPTURE_HASH = "256f3424fe17a55a5165e6a144bc32350510eb3b41a962acd51cc64a319361db"

EXPECTED = {
    "generator_id": "fre.g900.native_generator.reference.v0.1",
    "contract_id": "fre.g900.native_generator.v0.1",
    "target_read": False,
    "vertices": 900,
    "internal_edges": 1800,
    "carrier_edges": 1800,
    "total_edges": 3600,
    "degree_min": 8,
    "degree_max": 8,
    "connected": True,
    "canonical_edge_digest":
        "e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60",
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    checks = {
        "capture_hash_locked":
            CAPTURE.is_file() and digest(CAPTURE) == CAPTURE_HASH,
        "generator_not_rerun": True,
        "flattened_target_not_read": True,
        "sibling_inputs_not_read": True,
    }
    for path, expected in LOCKS.items():
        checks["binding_" + Path(path).stem] = (
            (ROOT / path).is_file()
            and digest(ROOT / path) == expected
        )

    observed = json.loads(CAPTURE.read_text(encoding="utf-8"))
    for key, expected in EXPECTED.items():
        checks["observed_" + key] = observed.get(key) == expected

    audit_pass = all(checks.values())
    artifact = {
        "artifact_id":
            "fre.g900.native_generator.execution_audit.001",
        "status":
            "native_generator_observation_recorded_target_not_compared",
        "bindings": {
            "capture_sha256": CAPTURE_HASH,
            "generator_contract_sha256": LOCKS[
                "contracts/fre_g900_native_generator_v0.1.json"
            ],
            "execution_gate_sha256": LOCKS[
                "contracts/fre_g900_native_generator_execution_gate_v0.1.json"
            ],
            "generator_source_sha256": LOCKS[
                "tools/generate_g900_kernel.py"
            ],
        },
        "run": {
            "run_id": "fre.g900.native_generator.run.001",
            "maximum_invocations": 1,
            "generator_rerun_by_audit": False,
            "observed": observed,
        },
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "locked_primitives_generated_expected_G900_invariants_"
            "target_comparison_pending"
            if audit_pass else
            "native_generator_execution_audit_failed"
        ),
        "boundary": {
            "flattened_target_compared": False,
            "negative_control_executed": False,
            "transport_cycle_executed": False,
            "recursive_host_admitted": False,
            "earned_receipt_emitted": False,
            "observational_closure": False,
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
        "canonical_edge_digest":
            observed.get("canonical_edge_digest"),
        "verdict": artifact["verdict"],
    }, sort_keys=True))
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
