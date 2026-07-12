#!/usr/bin/env python3
"""Record native-generator to flat-target G900 digest congruence."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = Path.home() / "tmp/fre_g900_generator_target_comparison_001.json"
ARTIFACT = ROOT / "artifacts/json/fre_g900_generator_target_congruence_audit_001.json"

LOCKS = {
    "contracts/fre_g900_generator_target_comparison_gate_v0.1.json":
        "43fcb31bb04234b39fad988bb1668742ff921adb96fbc1d804fce227a52061d9",
    "tools/compare_g900_generator_target.py":
        "6b302409dadba7bb77ef0386e88027d6189735097b202872e5f26d601e6bd211",
    "artifacts/json/fre_g900_native_generator_execution_audit_001.json":
        "b395d390d6f836b6aae9508c473251a4a72cce05f9d8fcad0e7c387b61c7dadb",
    "artifacts/json/fre_g900_target_canonicalization_audit_001.json":
        "e450c326271e3ff3a2656eeb5afb532dcb193e1f6d94b6cad2a224375648d52a",
}
CAPTURE_HASH = "3d9a9615521c05e216838968df176cab3bb1c997a2561b6990e876dfe1c30f03"
EDGE_DIGEST = "e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    observed = json.loads(CAPTURE.read_text(encoding="ascii"))
    checks = {
        "capture_hash_locked": digest(CAPTURE) == CAPTURE_HASH,
        "comparison_id_exact":
            observed.get("comparison_id")
            == "fre.g900.generator_target.digest_comparison.v0.1",
        "left_digest_locked":
            observed.get("left_digest") == EDGE_DIGEST,
        "right_digest_locked":
            observed.get("right_digest") == EDGE_DIGEST,
        "congruent": observed.get("congruent") is True,
        "tolerance_zero": observed.get("tolerance") == 0,
        "raw_payloads_not_read":
            observed.get("raw_payloads_read") is False,
        "runtime_captures_not_read":
            observed.get("runtime_captures_read") is False,
        "generator_not_rerun":
            observed.get("generator_rerun") is False,
        "target_not_recanonicalized":
            observed.get("target_recanonicalized") is False,
        "comparator_not_rerun_by_audit": True,
    }
    for path, expected in LOCKS.items():
        checks["binding_" + Path(path).stem] = (
            (ROOT / path).is_file()
            and digest(ROOT / path) == expected
        )

    audit_pass = all(checks.values())
    artifact = {
        "artifact_id":
            "fre.g900.generator_target.congruence_audit.001",
        "status":
            "native_generator_flat_target_digest_congruence_recorded",
        "bindings": {
            "comparison_capture_sha256": CAPTURE_HASH,
            "comparison_gate_sha256": LOCKS[
                "contracts/fre_g900_generator_target_comparison_gate_v0.1.json"
            ],
            "comparator_source_sha256": LOCKS[
                "tools/compare_g900_generator_target.py"
            ],
            "generator_audit_sha256": LOCKS[
                "artifacts/json/fre_g900_native_generator_execution_audit_001.json"
            ],
            "target_audit_sha256": LOCKS[
                "artifacts/json/fre_g900_target_canonicalization_audit_001.json"
            ],
        },
        "comparison": observed,
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "native_generator_reproduces_pinned_G900_"
            "canonical_edge_digest"
            if audit_pass else
            "generator_target_congruence_audit_failed"
        ),
        "claim_scope": {
            "claim": "canonical_edge_digest_congruence",
            "algorithm": "sha256",
            "canonical_serialization":
                "sorted normalized ASCII u,v followed by LF",
            "collision_resistance_assumption": True,
            "byte_for_byte_source_equality_claim": False,
            "recursive_host_claim": False,
            "universal_theorem_claim": False,
        },
        "boundary": {
            "negative_control_pending": True,
            "transport_cycle_executed": False,
            "independent_bridge_present": False,
            "recursive_host_admitted": False,
            "earned_recursive_host_receipt": False,
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
        "congruent": observed.get("congruent"),
        "verdict": artifact["verdict"],
    }, sort_keys=True))
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
