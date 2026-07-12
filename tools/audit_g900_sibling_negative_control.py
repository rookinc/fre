#!/usr/bin/env python3
"""Record the six-toggle sibling G900 negative control."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = Path.home() / "tmp/fre_g900_sibling_negative_control_001.json"
ARTIFACT = ROOT / "artifacts/json/fre_g900_sibling_negative_control_audit_001.json"

LOCKS = {
    "contracts/fre_g900_sibling_negative_control_execution_gate_v0.1.json":
        "421a72af3aabf257b73fbf4913088d14df52bb7df3b889c7ec947ceb9e260ca0",
    "tools/generate_g900_sibling_control.py":
        "0fd477ff9d6b16cec0d0907c75b4ea66319152b65a07b872f5a9ef91330d852b",
    "artifacts/json/fre_g900_generator_target_congruence_audit_001.json":
        "237760733f0ff1a368016db1a1a073b11cc687bbaea4e2f6ca9620525d701541",
}
CAPTURE_HASH = "1487593bfe1361c85139e8645d61d4b5e3b7f2d07e7acdbfe0293e6093fd9066"
CANONICAL = "e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60"
SIBLING = "b7951eac5c82e49faeed6f3be342e2f0d546ae1bca90a22b4fc73edb79ed983c"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    observed = json.loads(CAPTURE.read_text(encoding="ascii"))
    checks = {
        "capture_hash_locked": digest(CAPTURE) == CAPTURE_HASH,
        "control_id_exact":
            observed.get("control_id")
            == "fre.g900.sibling_signing.negative_control.v0.1",
        "vertices_900": observed.get("vertices") == 900,
        "internal_edges_1800":
            observed.get("internal_edges") == 1800,
        "carrier_edges_1800":
            observed.get("carrier_edges") == 1800,
        "total_edges_3600":
            observed.get("total_edges") == 3600,
        "degree_eight":
            observed.get("degree_min") == 8
            and observed.get("degree_max") == 8,
        "connected": observed.get("connected") is True,
        "delta_support_six":
            observed.get("delta_support") == 6,
        "canonical_digest_locked":
            observed.get("canonical_edge_digest") == CANONICAL,
        "sibling_digest_locked":
            observed.get("sibling_edge_digest") == SIBLING,
        "fixed_label_digest_separated":
            observed.get("distinct_from_canonical") is True
            and CANONICAL != SIBLING,
        "canonical_payload_not_read":
            observed.get("canonical_payload_read") is False,
        "sibling_target_not_read":
            observed.get("sibling_flat_target_read") is False,
        "control_not_rerun_by_audit": True,
    }
    for path, expected in LOCKS.items():
        checks["binding_" + Path(path).stem] = (
            (ROOT / path).is_file()
            and digest(ROOT / path) == expected
        )

    audit_pass = all(checks.values())
    artifact = {
        "artifact_id":
            "fre.g900.sibling_negative_control.audit.001",
        "status":
            "six_toggle_sibling_negative_control_recorded",
        "bindings": {
            "capture_sha256": CAPTURE_HASH,
            "execution_gate_sha256": LOCKS[
                "contracts/fre_g900_sibling_negative_control_execution_gate_v0.1.json"
            ],
            "control_source_sha256": LOCKS[
                "tools/generate_g900_sibling_control.py"
            ],
            "positive_congruence_audit_sha256": LOCKS[
                "artifacts/json/fre_g900_generator_target_congruence_audit_001.json"
            ],
        },
        "control": observed,
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "six_toggle_sibling_preserves_gross_invariants_"
            "and_separates_fixed_label_digest"
            if audit_pass else
            "sibling_negative_control_audit_failed"
        ),
        "claim_scope": {
            "negative_control_passed": audit_pass,
            "fixed_label_edge_set_digest_distinct": audit_pass,
            "graph_nonisomorphism_claim": False,
            "universal_cocycle_claim": False,
            "recursive_host_claim": False,
        },
        "boundary": {
            "flat_sibling_target_compared": False,
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
        "negative_control_passed":
            artifact["claim_scope"]["negative_control_passed"],
        "verdict": artifact["verdict"],
    }, sort_keys=True))
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
