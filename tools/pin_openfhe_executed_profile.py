from pathlib import Path
import subprocess
import hashlib
import json
import re
import sys

HOME = Path.home()
FRE = Path(__file__).resolve().parents[1]
ALETHEOS = HOME / "dev/cori/research/aletheos"
ADAPTER = ALETHEOS / "adapters/openfhe"
PREFIX = HOME / "tmp/openfhe_build_probe/openfhe-local-install-fixed"

EXECUTION = (
    ALETHEOS
    / "artifacts/json/"
    "b32k_fre_fhe_openfhe_eval_mult_decrypt_verify_smoke_001.json"
)
COMPOSITE = (
    ALETHEOS
    / "artifacts/json/"
    "b32k_fre_fhe_openfhe_eval_mult_receipt_001.json"
)
SOURCE = (
    ADAPTER
    / "smokes/b32k_fre_openfhe_eval_mult_decrypt_verify_smoke_001.cpp"
)
INITIAL_PROFILE = (
    ADAPTER
    / "profiles/b32k_fre_openfhe_tiny_bgv_test_profile_001.json"
)
ADMISSION = ADAPTER / "receipts/eval_mult_admission_001.json"
FIXTURES = (
    FRE / "fixtures/json/fre_support_mode_fixture_set_v0.1.json"
)
VERSION_FILE = (
    PREFIX / "lib/OpenFHE/OpenFHEConfigVersion.cmake"
)
OUT = (
    FRE
    / "artifacts/json/fre_openfhe_executed_profile_provenance_001.json"
)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def vector(value):
    if isinstance(value, list):
        return [int(item) for item in value]
    if isinstance(value, str):
        return [
            int(item.strip())
            for item in value.split(",")
            if item.strip()
        ]
    raise TypeError(f"unsupported vector value: {value!r}")

def main():
    required = [
        EXECUTION,
        COMPOSITE,
        SOURCE,
        INITIAL_PROFILE,
        ADMISSION,
        FIXTURES,
        VERSION_FILE,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing evidence: " + ", ".join(missing))

    execution = json.loads(EXECUTION.read_text(encoding="utf-8"))
    composite = json.loads(COMPOSITE.read_text(encoding="utf-8"))
    initial = json.loads(INITIAL_PROFILE.read_text(encoding="utf-8"))
    admission = json.loads(ADMISSION.read_text(encoding="utf-8"))
    fixture_set = json.loads(FIXTURES.read_text(encoding="utf-8"))
    source_text = SOURCE.read_text(encoding="utf-8")
    version_text = VERSION_FILE.read_text(
        encoding="utf-8",
        errors="replace"
    )

    version_match = re.search(
        r'set\s*\(PACKAGE_VERSION\s+"([^"]+)"',
        version_text
    )
    if not version_match:
        raise RuntimeError("OpenFHE package version not found")

    openfhe_version = version_match.group(1)
    actual_vector = vector(
        composite["verified_result"]["actual"]
    )

    selected_profile = {
        "profile_id": "fre.openfhe.bgv.evalmult.executed.v0.1",
        "source_profile_id":
            execution["smoke_status"]["profile_id"],
        "scheme": "BGVRNS",
        "plaintext_modulus": 65537,
        "multiplicative_depth": 2,
        "security_level": "HEStd_NotSet",
        "ring_dimension": 1024,
        "batch_size": 8,
        "openfhe_version": openfhe_version,
        "profile_class": "local_test_only",
        "status": "pinned_source_evidence_not_fre_admitted"
    }

    source_patterns = {
        "plaintext_modulus":
            r"SetPlaintextModulus\(65537\)",
        "multiplicative_depth":
            r"SetMultiplicativeDepth\(2\)",
        "security_level":
            r"SetSecurityLevel\(HEStd_NotSet\)",
        "ring_dimension":
            r"SetRingDim\(1024\)",
        "batch_size":
            r"SetBatchSize\(8\)",
        "eval_mult_keygen":
            r"EvalMultKeyGen\(",
        "eval_mult":
            r"EvalMult\(",
        "decrypt":
            r"Decrypt\("
    }

    source_checks = {
        key: re.search(pattern, source_text) is not None
        for key, pattern in source_patterns.items()
    }

    expected_values = []
    for fixture in fixture_set["fixtures"]:
        circuit = fixture["expected"]["circuit"]
        if circuit is None:
            continue
        expected_values.extend([circuit["S"], circuit["K"]])
        expected_values.extend(circuit["d"])

    max_expected_absolute = max(abs(value) for value in expected_values)
    signed_safe_bound = (
        selected_profile["plaintext_modulus"] - 1
    ) // 2

    source_commit_process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ALETHEOS,
        text=True,
        capture_output=True
    )
    if source_commit_process.returncode != 0:
        raise RuntimeError("could not resolve Aletheos source commit")
    source_commit = source_commit_process.stdout.strip()

    checks = {
        "execution_failures_empty":
            execution.get("failures") == [],
        "execution_scheme_bgv":
            execution["smoke_status"]["scheme"] == "BGVRNS",
        "execution_profile_is_repair":
            execution["smoke_status"]["profile_id"]
            == "b32k_fre_openfhe_tiny_bgv_eval_mult_profile_001_repair",
        "composite_failures_empty":
            composite.get("failures") == [],
        "composite_operation_evalmult":
            composite["operation"] == "EvalMult",
        "verified_result_exact":
            actual_vector == [10, 40, 90, 160, 0, 0, 0, 0],
        "source_parameters_exact":
            all(source_checks.values()),
        "openfhe_version_resolved":
            openfhe_version != "",
        "current_fixture_values_modulus_safe":
            max_expected_absolute < signed_safe_bound,
        "planned_ring_dimension_displaced":
            admission["planned_profile"]["ring_dimension"] == 2048
            and selected_profile["ring_dimension"] == 1024,
        "initial_depth_one_is_pre_evalmult":
            initial["multiplicative_depth"] == 1
            and selected_profile["multiplicative_depth"] == 2
    }

    pin_pass = all(checks.values())

    artifact = {
        "artifact_id":
            "fre.openfhe.executed_profile_provenance.001",
        "verdict": (
            "executed_evalmult_profile_pinned_not_admitted"
            if pin_pass
            else "executed_evalmult_profile_pin_failed"
        ),
        "pin_pass": pin_pass,
        "selection_rule": (
            "Successful execution receipt, successful composite receipt, "
            "and exact executed smoke source outrank plans, admissions, "
            "and earlier profile declarations."
        ),
        "source_project": {
            "path": str(ALETHEOS),
            "commit": source_commit,
            "install_prefix": str(PREFIX)
        },
        "selected_profile": selected_profile,
        "executed_operation_surface": [
            "KeyGen",
            "EvalMultKeyGen",
            "Encrypt",
            "EvalMult",
            "Decrypt"
        ],
        "verified_result": actual_vector,
        "parameter_conflicts_resolved": [
            {
                "field": "ring_dimension",
                "planned_value": 2048,
                "executed_value": 1024,
                "resolution": "executed_source_outranks_admission_plan"
            },
            {
                "field": "multiplicative_depth",
                "earlier_profile_value": 1,
                "executed_evalmult_value": 2,
                "resolution": "EvalMult_repair_profile_supersedes_add_profile"
            }
        ],
        "fixture_compatibility": {
            "fixture_set_id": fixture_set["fixture_set_id"],
            "max_expected_absolute": max_expected_absolute,
            "signed_safe_bound": signed_safe_bound,
            "modulus_wrap_expected": False
        },
        "source_hashes": {
            "execution_receipt_sha256": sha256(EXECUTION),
            "composite_receipt_sha256": sha256(COMPOSITE),
            "executed_smoke_source_sha256": sha256(SOURCE),
            "initial_profile_sha256": sha256(INITIAL_PROFILE),
            "evalmult_admission_sha256": sha256(ADMISSION),
            "fixture_set_sha256": sha256(FIXTURES),
            "openfhe_config_version_sha256": sha256(VERSION_FILE)
        },
        "checks": checks,
        "source_checks": source_checks,
        "boundary": {
            "evidence_import_only": True,
            "profile_admitted_to_fre": False,
            "production_security_profile": False,
            "openfhe_backend_admitted": False,
            "key_generation_performed_now": False,
            "encryption_performed_now": False,
            "evaluation_performed_now": False,
            "decryption_performed_now": False,
            "receipt_congruence_established": False,
            "observational_closure": False,
            "physical_claim": False
        }
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    print(json.dumps({
        "artifact_id": artifact["artifact_id"],
        "pin_pass": pin_pass,
        "verdict": artifact["verdict"],
        "selected_profile": selected_profile,
        "max_expected_absolute": max_expected_absolute,
        "signed_safe_bound": signed_safe_bound
    }, sort_keys=True))

    return 0 if pin_pass else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "pin_pass": False,
            "error": f"{type(exc).__name__}: {exc}"
        }), file=sys.stderr)
        raise SystemExit(2)
