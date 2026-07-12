#!/usr/bin/env python3
"""Audit the fail-closed native G900 generator checkpoint."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/json/fre_g900_native_generator_checkpoint_audit_001.json"

LOCKS = {
    ".gitattributes":
        "f8cbc9348d04a505addbb20f32fc121b6508973ab8e6ca4aee3ebb1cf6762a79",
    "artifacts/json/fre_g900_native_generator_execution_audit_001.json":
        "b395d390d6f836b6aae9508c473251a4a72cce05f9d8fcad0e7c387b61c7dadb",
    "artifacts/json/fre_g900_target_canonicalization_audit_001.json":
        "e450c326271e3ff3a2656eeb5afb532dcb193e1f6d94b6cad2a224375648d52a",
    "artifacts/json/fre_g900_generator_target_congruence_audit_001.json":
        "237760733f0ff1a368016db1a1a073b11cc687bbaea4e2f6ca9620525d701541",
    "artifacts/json/fre_g900_sibling_negative_control_audit_001.json":
        "f785f8c1fde74b9dd0701ba54cd9e5a0b9b3269a650007ca6c17eb52d555146f",
}

CANONICAL = "e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60"
SIBLING = "b7951eac5c82e49faeed6f3be342e2f0d546ae1bca90a22b4fc73edb79ed983c"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_text(encoding="ascii"))


def main():
    checks = {}
    for path, expected in LOCKS.items():
        checks["hash_" + Path(path).stem] = (
            (ROOT / path).is_file()
            and digest(ROOT / path) == expected
        )

    policy = (ROOT / ".gitattributes").read_text(encoding="ascii")
    generator = load(
        "artifacts/json/fre_g900_native_generator_execution_audit_001.json"
    )
    target = load(
        "artifacts/json/fre_g900_target_canonicalization_audit_001.json"
    )
    congruence = load(
        "artifacts/json/fre_g900_generator_target_congruence_audit_001.json"
    )
    sibling = load(
        "artifacts/json/fre_g900_sibling_negative_control_audit_001.json"
    )

    generator_digest = generator["run"]["observed"][
        "canonical_edge_digest"
    ]
    target_digest = target["run"]["observed"][
        "canonical_edge_digest"
    ]
    sibling_digest = sibling["control"]["sibling_edge_digest"]

    checks.update({
        "byte_policy_exact":
            policy
            == (
                "# Preserve exact hash-pinned G900 payload bytes.\n"
                "fixtures/g900/*.csv -text\n"
            ),
        "generator_audit_pass": generator.get("audit_pass") is True,
        "target_audit_pass": target.get("audit_pass") is True,
        "congruence_audit_pass":
            congruence.get("audit_pass") is True,
        "sibling_audit_pass": sibling.get("audit_pass") is True,
        "generator_digest_locked":
            generator_digest == CANONICAL,
        "target_digest_locked": target_digest == CANONICAL,
        "positive_digest_congruent":
            generator_digest == target_digest,
        "congruence_result_true":
            congruence["comparison"]["congruent"] is True,
        "sibling_digest_locked":
            sibling_digest == SIBLING,
        "sibling_digest_distinct":
            sibling_digest != CANONICAL,
        "sibling_delta_support_six":
            sibling["control"]["delta_support"] == 6,
        "negative_control_passed":
            sibling["claim_scope"]["negative_control_passed"]
            is True,
        "nonisomorphism_not_claimed":
            sibling["claim_scope"]["graph_nonisomorphism_claim"]
            is False,
        "no_transport_cycle":
            not congruence["boundary"]["transport_cycle_executed"]
            and not sibling["boundary"]["transport_cycle_executed"],
        "no_independent_bridge":
            not congruence["boundary"]["independent_bridge_present"]
            and not sibling["boundary"]["independent_bridge_present"],
        "recursive_host_not_admitted":
            not congruence["boundary"]["recursive_host_admitted"]
            and not sibling["boundary"]["recursive_host_admitted"],
        "no_observational_closure":
            not congruence["boundary"]["observational_closure"]
            and not sibling["boundary"]["observational_closure"],
        "construction_not_rerun_by_checkpoint_audit": True,
        "raw_payloads_not_read_by_checkpoint_audit": True,
    })

    audit_pass = all(checks.values())
    artifact = {
        "artifact_id":
            "fre.g900.native_generator.checkpoint_audit.001",
        "status":
            "native_generator_checkpoint_recorded_fail_closed",
        "bindings": {
            path: {"sha256": value}
            for path, value in LOCKS.items()
        },
        "results": {
            "canonical_edge_digest": CANONICAL,
            "sibling_edge_digest": SIBLING,
            "positive_congruence": True,
            "negative_control_passed": True,
            "delta_support": 6,
        },
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "native_G900_generator_reproduces_pinned_carrier_"
            "and_sibling_control_separates"
            if audit_pass else
            "native_G900_generator_checkpoint_failed"
        ),
        "claim_scope": {
            "native_generator_reproduction":
                "canonical_edge_digest_congruence",
            "negative_control":
                "fixed_label_digest_separation",
            "graph_nonisomorphism_claim": False,
            "recursive_host_claim": False,
            "universal_theorem_claim": False,
        },
        "boundary": {
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
        "negative_control_passed": True,
        "positive_congruence": True,
        "verdict": artifact["verdict"],
    }, sort_keys=True))
    if not audit_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
