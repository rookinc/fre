#!/usr/bin/env python3
"""Record the independent canonical G900 target observation."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = Path.home() / "tmp/fre_g900_target_canonicalization_001.json"
ARTIFACT = ROOT / "artifacts/json/fre_g900_target_canonicalization_audit_001.json"

LOCKS = {
    "contracts/fre_g900_target_canonicalization_gate_v0.1.json":
        "699e209a580ef7750255963188e7753c2ef7d205c453487c55b53bcdd511476b",
    "tools/canonicalize_g900_target.py":
        "f0d87e92ce330539c8603cce7a0ae3a40ed4cb29db592a7c2b90f89f7c2d5bef",
    "fixtures/g900/x_sigma_edges.csv":
        "ea2679662f4322a9ea021fba1143c804ef73b1fae95f50c77ba76b7fe1092230",
}
CAPTURE_HASH = "6b1219278273fff451cf3b72489145a3c9227a21048f0c3385c39a82741e5b56"

EXPECTED = {
    "target_id": "fre.g900.flattened_target.canonical.v0.1",
    "target_raw_sha256":
        "ea2679662f4322a9ea021fba1143c804ef73b1fae95f50c77ba76b7fe1092230",
    "target_rows": 3600,
    "normalized_edges": 3600,
    "minimum_vertex": 0,
    "maximum_vertex": 899,
    "vertex_count": 900,
    "kind_counts": {
        "external_signed_carrier": 1800,
        "internal_thalion_copy": 1800,
    },
    "canonical_edge_digest":
        "e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60",
    "generator_digest_read": False,
    "comparison_performed": False,
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    checks = {
        "capture_hash_locked":
            CAPTURE.is_file() and digest(CAPTURE) == CAPTURE_HASH,
        "target_canonicalizer_not_rerun": True,
        "generator_result_not_read": True,
        "comparison_not_performed": True,
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
            "fre.g900.target_canonicalization.audit.001",
        "status":
            "independent_target_canonicalization_recorded_comparison_pending",
        "bindings": {
            "capture_sha256": CAPTURE_HASH,
            "canonicalization_gate_sha256": LOCKS[
                "contracts/fre_g900_target_canonicalization_gate_v0.1.json"
            ],
            "canonicalizer_source_sha256": LOCKS[
                "tools/canonicalize_g900_target.py"
            ],
            "target_raw_sha256": LOCKS[
                "fixtures/g900/x_sigma_edges.csv"
            ],
        },
        "run": {
            "run_id": "fre.g900.target_canonicalization.run.001",
            "maximum_invocations": 1,
            "canonicalizer_rerun_by_audit": False,
            "observed": observed,
        },
        "checks": checks,
        "audit_pass": audit_pass,
        "verdict": (
            "flat_G900_target_independently_canonicalized_"
            "generator_comparison_pending"
            if audit_pass else
            "target_canonicalization_audit_failed"
        ),
        "boundary": {
            "generator_result_read": False,
            "generator_digest_compared": False,
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
