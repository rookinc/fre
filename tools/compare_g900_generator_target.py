#!/usr/bin/env python3
"""Compare the two independently recorded canonical G900 digests."""

from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEFT = (
    ROOT
    / "artifacts/json/fre_g900_native_generator_execution_audit_001.json"
)
RIGHT = (
    ROOT
    / "artifacts/json/fre_g900_target_canonicalization_audit_001.json"
)

LEFT_HASH = "b395d390d6f836b6aae9508c473251a4a72cce05f9d8fcad0e7c387b61c7dadb"
RIGHT_HASH = "e450c326271e3ff3a2656eeb5afb532dcb193e1f6d94b6cad2a224375648d52a"


def load_locked(path, expected_hash):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise RuntimeError("audit artifact hash mismatch")
    return json.loads(raw.decode("ascii"))


def main():
    left = load_locked(LEFT, LEFT_HASH)
    right = load_locked(RIGHT, RIGHT_HASH)

    if left.get("audit_pass") is not True:
        raise RuntimeError("left audit did not pass")
    if right.get("audit_pass") is not True:
        raise RuntimeError("right audit did not pass")

    left_digest = left["run"]["observed"]["canonical_edge_digest"]
    right_digest = right["run"]["observed"]["canonical_edge_digest"]

    if not (
        isinstance(left_digest, str)
        and isinstance(right_digest, str)
        and len(left_digest) == 64
        and len(right_digest) == 64
    ):
        raise RuntimeError("canonical digest shape mismatch")

    result = {
        "comparison_id":
            "fre.g900.generator_target.digest_comparison.v0.1",
        "left_artifact_id": left["artifact_id"],
        "right_artifact_id": right["artifact_id"],
        "algorithm": "sha256",
        "rule": "exact_lowercase_hex_string_equality",
        "tolerance": 0,
        "left_digest": left_digest,
        "right_digest": right_digest,
        "congruent": left_digest == right_digest,
        "raw_payloads_read": False,
        "runtime_captures_read": False,
        "generator_rerun": False,
        "target_recanonicalized": False,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
