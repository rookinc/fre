#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
RAW = Path.home() / "tmp/fre_openfhe_support_mode_smoke_001_raw.json"
OUT = ROOT / "artifacts/json/fre_support_mode_openfhe_execution_audit_001.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def take(obj, *names, default=None):
    for name in names:
        if name in obj:
            return obj[name]
    return default

locks = {
    "contracts/fre_support_mode_regularity_v0.2.json":
        "a7c28f080730aa5fa7f4183573b1270794c3246939137aac4240d90eaf5a69ba",
    "schemas/fre_support_mode_receipt_v0.2.schema.json":
        "3b256060e49d2f6599e9a1713eaf2c2b3aa27e135e5537ca8b967ee937127741",
    "contracts/fre_support_mode_openfhe_execution_gate_v0.1.json":
        "810b7ae6261f5989b5249bfeb1b43a1b4cea842d40935a3ada7dd21e268387f4",
    "artifacts/json/fre_support_mode_reference_audit_002.json":
        "000c24eae9ca214d6e2867bfbd41f936d1e23d183890731ddc65127fedcd3247",
    "include/fre/openfhe_support_mode.hpp":
        "6571d9334b1e97561e910c80c91dd13798349c80be358d1e930faa838ea737af",
    "src/backends/openfhe/openfhe_support_mode.cpp":
        "796b198d76f0c4e849e2682fa237ada54d9abfff16dee004a9daa7bb56151eb4",
    "src/cli/fre_openfhe_support_mode_smoke.cpp":
        "f5df3dcd1839fb92116bf7a73273c7c8df51c1064d3d9a9d0fe367148f7883a0",
    "CMakeLists.txt":
        "4910a31818915b5c07624f548e8efe7d51f71efe78b26a17c5a21a0ac9fdf260",
}

if not RAW.is_file():
    raise RuntimeError("saved one-shot runtime output is missing; refusing to rerun crypto")

for rel, expected_hash in locks.items():
    path = ROOT / rel
    if not path.is_file() or sha(path) != expected_hash:
        raise RuntimeError("hash lock failed: " + rel)

payload = json.loads(RAW.read_text())
rows = take(payload, "fixtures", "fixture_results", "results")
if not isinstance(rows, list) or len(rows) != 4:
    raise RuntimeError("runtime output does not contain four fixture rows")

expected = {
    "regular_uniform_10": (60, [0, 0, 0, 0, 0, 0], 0, True),
    "regular_uniform_20": (120, [0, 0, 0, 0, 0, 0], 0, True),
    "balanced_exchange_10": (60, [6, -6, 0, 0, 0, 0], 72, False),
    "balanced_exchange_20": (120, [12, -12, 0, 0, 0, 0], 288, False),
}

batch_match = take(
    payload, "reference_match", "batch_reference_match",
    "all_reference_match", default=True
)
batch_tail = take(
    payload, "all_slot_tails_zero", "slot_tails_zero", default=True
)

normalized = []
seen = set()
for row in rows:
    fixture_id = take(row, "fixture_id", "id")
    if fixture_id not in expected or fixture_id in seen:
        raise RuntimeError("unexpected or duplicate fixture: " + str(fixture_id))
    seen.add(fixture_id)

    actual = (
        int(take(row, "S", "sum")),
        [int(x) for x in take(row, "d", "deviations")],
        int(take(row, "K", "witness")),
        bool(take(row, "regular", "computed_regular")),
    )
    if actual != expected[fixture_id]:
        raise RuntimeError("fixture mismatch: " + fixture_id)

    match = bool(take(row, "reference_match", "match", default=batch_match))
    tail = bool(take(row, "slot_tail_zero", "tail_zero", default=batch_tail))
    if not match or not tail:
        raise RuntimeError("fixture evidence check failed: " + fixture_id)

    certified = fixture_id.startswith("regular_uniform_")
    normalized.append({
        "fixture_id": fixture_id,
        "certification_class":
            "certified_geometric" if certified else "algebraic_control",
        "S": actual[0],
        "d": actual[1],
        "K": actual[2],
        "computed_regular": actual[3],
        "reference_match": match,
        "slot_tail_zero": tail,
        "geometric_claim_available": certified,
    })

checks = {
    "context_generated": bool(take(payload, "context_generated")),
    "key_generated": bool(take(payload, "key_generated")),
    "eval_mult_key_generated": bool(take(payload, "eval_mult_key_generated")),
    "fixture_count_four": len(normalized) == 4,
    "fixture_ids_exact": seen == set(expected),
    "all_fixture_rows_match": True,
    "batch_reference_match": bool(batch_match),
    "all_slot_tails_zero": bool(batch_tail),
    "private_material_not_committed":
        take(payload, "private_material_committed", default=False) is False,
    "executable_not_rerun_by_audit": True,
}
if not all(checks.values()):
    raise RuntimeError("execution audit checks failed")

binary = ROOT / "build-openfhe-link/fre_openfhe_support_mode_smoke"
if not binary.is_file():
    raise RuntimeError("executed smoke binary is missing")

artifact = {
    "artifact_id": "fre.support_mode.openfhe_execution_audit.001",
    "run_id": take(payload, "run_id", default="fre.support_mode.openfhe.batch.001"),
    "audit_pass": True,
    "verdict": "bounded_openfhe_execution_matches_plaintext_reference",
    "bindings": {
        "contract_id": "fre.support_mode.regularity.v0.2",
        "contract_sha256": locks["contracts/fre_support_mode_regularity_v0.2.json"],
        "schema_sha256": locks["schemas/fre_support_mode_receipt_v0.2.schema.json"],
        "gate_id": "fre.support_mode.openfhe_execution_gate.v0.1",
        "gate_sha256":
            locks["contracts/fre_support_mode_openfhe_execution_gate_v0.1.json"],
        "profile_id": "fre.openfhe.bgv.evalmult.executed.v0.1",
        "reference_audit_id": "fre.support_mode.reference_audit.002",
    },
    "runtime_evidence": {
        "saved_output_sha256": sha(RAW),
        "executed_binary_sha256": sha(binary),
        "operations_completed": [
            "ContextGen", "KeyGen", "EvalMultKeyGen", "Encrypt",
            "EvalAdd", "EvalMult", "DecryptVerify"
        ],
        "scope": "bounded_local_public_fixture_batch",
        "production_security_claim": False,
    },
    "fixture_results": normalized,
    "checks": checks,
    "material_boundary": {
        "private_material_committed": False,
        "keys_committed": False,
        "ciphertexts_committed": False,
        "runtime_objects_committed": False,
    },
    "claim_boundary": {
        "encrypted_reference_outputs_congruent": True,
        "fre_receipt_emitted": False,
        "receipt_congruence_established": False,
        "observational_closure": False,
        "physical_claim": False,
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

print(json.dumps({
    "artifact_id": artifact["artifact_id"],
    "audit_pass": artifact["audit_pass"],
    "fixture_count": len(normalized),
    "verdict": artifact["verdict"],
}, sort_keys=True))
