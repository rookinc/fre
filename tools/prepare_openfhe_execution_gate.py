from pathlib import Path
import subprocess
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT_V1 = ROOT / "contracts/fre_support_mode_regularity_v0.1.json"
CONTRACT_V2 = ROOT / "contracts/fre_support_mode_regularity_v0.2.json"
SCHEMA_V2 = ROOT / "schemas/fre_support_mode_receipt_v0.2.schema.json"
FIXTURES = ROOT / "fixtures/json/fre_support_mode_fixture_set_v0.1.json"
BASE_REFERENCE_AUDIT = (
    ROOT / "artifacts/json/fre_support_mode_reference_audit_001.json"
)
REFERENCE_AUDIT_V2 = (
    ROOT / "artifacts/json/fre_support_mode_reference_audit_002.json"
)
PROFILE = (
    ROOT
    / "artifacts/json/fre_openfhe_executed_profile_provenance_001.json"
)
DURABLE = (
    ROOT / "artifacts/json/fre_openfhe_durable_prefix_001.json"
)
LINK_AUDIT = (
    ROOT / "artifacts/json/fre_openfhe_link_status_audit_001.json"
)
GATE = (
    ROOT / "contracts/fre_support_mode_openfhe_execution_gate_v0.1.json"
)

PARENT_COMMIT = "3cc24b5eb1db7eb07841b17fe8bd7381e8a0f6e6"

EXPECTED_HASHES = {
    "contract_v1":
        "25622e5185cd1289f28e51157d9236d13fc5ddaf863097522ac46b6d9e4ccda6",
    "contract_v2":
        "a7c28f080730aa5fa7f4183573b1270794c3246939137aac4240d90eaf5a69ba",
    "schema_v2":
        "3b256060e49d2f6599e9a1713eaf2c2b3aa27e135e5537ca8b967ee937127741",
    "fixtures":
        "bb7a62eb248a0ee47de9a6e46e69e778c015d415544d5cdce5591faa964a1f2d",
    "base_reference_audit":
        "07b1c0c4b3f7d93363d020eb4b8846916d51e98c072817719269cd07c160e615",
    "profile":
        "77a78f5741268dd64bf61212d4ef8d694449199f47751886458f6af225557359",
    "durable":
        "d76fa197a0b46bd44f34c18343b1adf1faf0ac9e1ebd14adf7f8cd2b992fbac7",
    "link_audit":
        "8ea2500a8284caa1ac33152f6cfe7505b074c5aff2c8ad27780ea6ca5fe71ac2"
}

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd):
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True
    )
    text = (p.stdout + p.stderr).rstrip()
    if p.returncode != 0:
        raise RuntimeError(
            f"command failed rc={p.returncode}: {' '.join(cmd)}\n{text[:2200]}"
        )
    return text

def main():
    required = [
        CONTRACT_V1,
        CONTRACT_V2,
        SCHEMA_V2,
        FIXTURES,
        BASE_REFERENCE_AUDIT,
        PROFILE,
        DURABLE,
        LINK_AUDIT,
    ]

    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing required files: " + ", ".join(missing))

    run(["python", "tools/audit_reference_fixtures.py"])
    run(["python", "tools/audit_openfhe_link_status.py"])

    paths = {
        "contract_v1": CONTRACT_V1,
        "contract_v2": CONTRACT_V2,
        "schema_v2": SCHEMA_V2,
        "fixtures": FIXTURES,
        "base_reference_audit": BASE_REFERENCE_AUDIT,
        "profile": PROFILE,
        "durable": DURABLE,
        "link_audit": LINK_AUDIT,
    }

    actual_hashes = {
        name: sha256(path)
        for name, path in paths.items()
    }

    hash_checks = {
        name: actual_hashes[name] == EXPECTED_HASHES[name]
        for name in EXPECTED_HASHES
    }

    if not all(hash_checks.values()):
        failed = [
            name for name, ok in hash_checks.items() if not ok
        ]
        raise RuntimeError("binding hash mismatch: " + ", ".join(failed))

    ancestor = subprocess.run(
        [
            "git", "merge-base", "--is-ancestor",
            PARENT_COMMIT, "HEAD"
        ],
        cwd=ROOT,
        text=True,
        capture_output=True
    )
    if ancestor.returncode != 0:
        raise RuntimeError("link checkpoint is not an ancestor of HEAD")

    contract_v1 = json.loads(
        CONTRACT_V1.read_text(encoding="utf-8")
    )
    contract_v2 = json.loads(
        CONTRACT_V2.read_text(encoding="utf-8")
    )
    schema_v2 = json.loads(
        SCHEMA_V2.read_text(encoding="utf-8")
    )
    fixture_set = json.loads(
        FIXTURES.read_text(encoding="utf-8")
    )
    base_audit = json.loads(
        BASE_REFERENCE_AUDIT.read_text(encoding="utf-8")
    )
    profile = json.loads(
        PROFILE.read_text(encoding="utf-8")
    )
    durable = json.loads(
        DURABLE.read_text(encoding="utf-8")
    )
    link_audit = json.loads(
        LINK_AUDIT.read_text(encoding="utf-8")
    )

    well_typed_ids = [
        item["fixture_id"]
        for item in fixture_set["fixtures"]
        if item["expected"]["well_typed"]
    ]
    rejected_ids = [
        item["fixture_id"]
        for item in fixture_set["fixtures"]
        if not item["expected"]["well_typed"]
    ]

    schema_operations = set(
        schema_v2["properties"]["operation_names"]
        ["items"]["enum"]
    )
    contract_operations = set(
        contract_v2["required_operations"]
    )

    reference_checks = {
        "base_reference_audit_pass":
            base_audit["audit_pass"] is True,
        "all_six_base_rows_pass":
            len(base_audit["rows"]) == 6
            and all(row["pass"] for row in base_audit["rows"]),
        "formulas_unchanged":
            contract_v2["circuit"]["formulas"]
            == contract_v1["circuit"]["formulas"],
        "receipt_quotient_unchanged":
            contract_v2["comparison"]["receipt_quotient"]
            == contract_v1["comparison"]["receipt_quotient"],
        "comparison_rule_unchanged":
            contract_v2["comparison"]["comparison_rule"]
            == contract_v1["comparison"]["comparison_rule"],
        "tolerance_unchanged":
            contract_v2["comparison"]["tolerance"]
            == contract_v1["comparison"]["tolerance"] == 0,
        "reference_pipeline_unchanged":
            contract_v2["pipelines"]["reference"]["pipeline_id"]
            == contract_v1["pipelines"]["reference"]["pipeline_id"],
        "well_typed_fixture_set_exact":
            well_typed_ids
            == contract_v2["source"]["admitted_fixture_ids"],
        "rejected_fixture_set_exact":
            rejected_ids
            == contract_v2["source"]["rejected_fixture_ids"],
        "schema_contract_binding":
            schema_v2["properties"]["comparison"]
            ["properties"]["contract_sha256"]["const"]
            == EXPECTED_HASHES["contract_v2"],
        "schema_operation_surface_exact":
            schema_operations == contract_operations
    }

    reference_audit_pass = all(reference_checks.values())

    reference_audit = {
        "artifact_id": "fre.support_mode.reference_audit.002",
        "verdict": (
            "plaintext_reference_rebound_to_contract_v0.2"
            if reference_audit_pass
            else "plaintext_reference_v0.2_binding_failed"
        ),
        "audit_pass": reference_audit_pass,
        "pipeline_id": "support_mode_reference_v0.1",
        "contract_binding": {
            "contract_id": contract_v2["contract_id"],
            "contract_sha256": actual_hashes["contract_v2"],
            "superseded_contract_id": contract_v1["contract_id"],
            "superseded_contract_sha256":
                actual_hashes["contract_v1"]
        },
        "receipt_schema_binding": {
            "receipt_schema": "fre.support_mode.receipt.v0.2",
            "receipt_schema_sha256": actual_hashes["schema_v2"]
        },
        "fixture_binding": {
            "fixture_set_id": fixture_set["fixture_set_id"],
            "fixture_set_sha256": actual_hashes["fixtures"]
        },
        "base_audit_binding": {
            "artifact_id": base_audit["artifact_id"],
            "artifact_sha256":
                actual_hashes["base_reference_audit"]
        },
        "checks": reference_checks,
        "rows": base_audit["rows"],
        "boundary": {
            "reference_pipeline_only": True,
            "contract_revision_changes_reference_math": False,
            "openfhe_execution_performed": False,
            "fre_receipt_emitted": False,
            "receipt_congruence_established": False,
            "observational_closure": False,
            "physical_claim": False
        }
    }

    REFERENCE_AUDIT_V2.parent.mkdir(parents=True, exist_ok=True)
    REFERENCE_AUDIT_V2.write_text(
        json.dumps(reference_audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    gate_checks = {
        "reference_audit_v2_pass":
            reference_audit_pass,
        "profile_pin_pass":
            profile["pin_pass"] is True,
        "durable_copy_ready":
            durable["copy_ready"] is True,
        "link_audit_pass":
            link_audit["audit_pass"] is True,
        "backend_available":
            link_audit["backend_status"]["available"] is True,
        "backend_linked":
            link_audit["backend_status"]["linked"] is True,
        "current_crypto_closed":
            link_audit["backend_status"]["crypto_allowed"] is False,
        "all_operations_receiptable":
            schema_operations == contract_operations,
        "multiplicative_depth_two":
            contract_v2["execution_model"]
            ["multiplicative_depth_required"] == 2,
        "modulus_safe":
            contract_v2["execution_model"]
            ["fixture_max_expected_absolute"]
            < contract_v2["execution_model"]["signed_safe_bound"],
        "no_rotations_required":
            contract_v2["execution_model"]["ciphertext_layout"]
            ["rotations_required"] is False,
        "public_fixture_batch_only":
            len(well_typed_ids) == 4
    }

    gate_pass = all(gate_checks.values())

    gate = {
        "gate_id":
            "fre.support_mode.openfhe_execution_gate.v0.1",
        "status": (
            "next_bounded_local_smoke_admitted_not_executed"
            if gate_pass
            else "execution_gate_blocked"
        ),
        "gate_pass": gate_pass,
        "execution_allowed_for_next_packet": gate_pass,
        "parent_checkpoint_commit": PARENT_COMMIT,
        "bindings": {
            "contract_id": contract_v2["contract_id"],
            "contract_sha256": actual_hashes["contract_v2"],
            "receipt_schema":
                "fre.support_mode.receipt.v0.2",
            "receipt_schema_sha256": actual_hashes["schema_v2"],
            "fixture_set_id": fixture_set["fixture_set_id"],
            "fixture_set_sha256": actual_hashes["fixtures"],
            "reference_audit_id": reference_audit["artifact_id"],
            "reference_audit_sha256": sha256(REFERENCE_AUDIT_V2),
            "profile_id":
                profile["selected_profile"]["profile_id"],
            "profile_sha256": actual_hashes["profile"],
            "durable_prefix_artifact_id": durable["artifact_id"],
            "durable_prefix_sha256": actual_hashes["durable"],
            "link_audit_id": link_audit["artifact_id"],
            "link_audit_sha256": actual_hashes["link_audit"]
        },
        "admitted_scope": {
            "scope": "one_local_public_fixture_batch",
            "fixture_ids": well_typed_ids,
            "pre_gate_rejected_fixture_ids": rejected_ids,
            "coordinate_min": 1,
            "coordinate_max": 22,
            "public_test_data_only": True,
            "production_data_allowed": False,
            "production_security_claim": False
        },
        "profile": contract_v2["execution_model"],
        "admitted_operations": contract_v2["required_operations"],
        "receipt_policy": {
            "receipt_schema":
                "fre.support_mode.receipt.v0.2",
            "receipt_emitted_only_after_reference_comparison":
                True,
            "public_receipt_exports_claim_only": True,
            "decrypted_fixture_values_remain_verification_data":
                True,
            "secret_keys_committed": False,
            "ciphertext_material_committed": False,
            "runtime_objects_committed": False,
            "failure_receipt_required_on_gate_or_comparison_failure":
                True
        },
        "failure_conditions": [
            "fixture outside admitted batch",
            "coordinate outside declared bounds",
            "profile or prefix binding mismatch",
            "unexpected operation requested",
            "reference comparison mismatch",
            "negative control failure",
            "receipt schema failure",
            "private runtime material selected for commit"
        ],
        "checks": gate_checks,
        "boundary": {
            "admission_artifact_only": True,
            "current_runtime_profile_admitted": False,
            "profile_admission_effective_on_next_packet": gate_pass,
            "crypto_execution_performed_now": False,
            "crypto_context_constructed_now": False,
            "key_generation_performed_now": False,
            "encryption_performed_now": False,
            "evaluation_performed_now": False,
            "decryption_performed_now": False,
            "fre_receipt_emitted": False,
            "receipt_congruence_established": False,
            "observational_closure": False,
            "production_security_claim": False,
            "physical_claim": False
        }
    }

    GATE.parent.mkdir(parents=True, exist_ok=True)
    GATE.write_text(
        json.dumps(gate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    print(json.dumps({
        "reference_audit_id": reference_audit["artifact_id"],
        "reference_audit_pass": reference_audit_pass,
        "gate_id": gate["gate_id"],
        "gate_pass": gate_pass,
        "execution_allowed_for_next_packet":
            gate["execution_allowed_for_next_packet"],
        "fixture_count": len(well_typed_ids),
        "operation_count": len(contract_operations)
    }, sort_keys=True))

    return 0 if reference_audit_pass and gate_pass else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "gate_pass": False,
            "error": f"{type(exc).__name__}: {exc}"
        }), file=sys.stderr)
        raise SystemExit(2)
