from pathlib import Path
import subprocess
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/fre_support_mode_regularity_v0.1.json"
SCHEMA = ROOT / "schemas/fre_support_mode_receipt_v0.1.schema.json"
FIXTURES = ROOT / "fixtures/json/fre_support_mode_fixture_set_v0.1.json"
BINARY = ROOT / "build/fre_support_reference"
OUT = ROOT / "artifacts/json/fre_support_mode_reference_audit_001.json"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    required = [CONTRACT, SCHEMA, FIXTURES, BINARY]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("missing required files: " + ", ".join(missing))

    fixture_set = json.loads(FIXTURES.read_text(encoding="utf-8"))
    contract_sha = sha256(CONTRACT)
    schema_sha = sha256(SCHEMA)
    fixture_sha = sha256(FIXTURES)

    hash_binding_pass = (
        fixture_set["contract_sha256"] == contract_sha
        and fixture_set["receipt_schema_sha256"] == schema_sha
    )

    rows = []
    observed = {}

    for fixture in fixture_set["fixtures"]:
        fixture_id = fixture["fixture_id"]
        expected = fixture["expected"]
        command = [str(BINARY)] + [str(value) for value in fixture["h"]]

        process = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True
        )

        row = {
            "fixture_id": fixture_id,
            "kind": fixture["kind"],
            "expected_well_typed": expected["well_typed"],
            "returncode": process.returncode,
            "circuit_match": None,
            "claim_boundary_match": None,
            "rejection_match": None,
            "observed": None,
            "pass": False
        }

        if expected["well_typed"]:
            try:
                result = json.loads(process.stdout)
            except json.JSONDecodeError:
                result = None

            circuit_match = (
                process.returncode == 0
                and result is not None
                and result.get("pipeline_id")
                    == "support_mode_reference_v0.1"
                and result.get("source_class")
                    == "six_support_register"
                and result.get("S") == expected["circuit"]["S"]
                and result.get("d") == expected["circuit"]["d"]
                and result.get("K") == expected["circuit"]["K"]
                and result.get("regular")
                    == (expected["circuit"]["K"] == 0)
            )

            claim_expected = expected["claim"]
            if claim_expected["status"] == "earned":
                claim_boundary_match = (
                    result is not None
                    and result.get("regular")
                        == claim_expected["result"]
                )
            else:
                claim_boundary_match = (
                    claim_expected["status"] == "unavailable"
                    and claim_expected["result"] is None
                )

            row["circuit_match"] = circuit_match
            row["claim_boundary_match"] = claim_boundary_match
            row["observed"] = result
            row["pass"] = circuit_match and claim_boundary_match

            if result is not None:
                observed[fixture_id] = result

        else:
            rejection_match = (
                process.returncode != 0
                and process.stdout.strip() == ""
                and expected["claim"]["status"] == "rejected"
                and expected["claim"]["result"] is None
            )
            row["rejection_match"] = rejection_match
            row["pass"] = rejection_match

        rows.append(row)

    left = observed.get("balanced_exchange_10")
    right = observed.get("balanced_exchange_20")

    scale_relation_pass = (
        left is not None
        and right is not None
        and right["S"] == 2 * left["S"]
        and right["d"] == [2 * value for value in left["d"]]
        and right["K"] == 4 * left["K"]
    )

    checks = {
        "hash_binding_pass": hash_binding_pass,
        "fixture_count_six": len(rows) == 6,
        "all_fixture_rows_pass":
            all(row["pass"] for row in rows),
        "certified_claim_count_two":
            sum(
                row["claim_boundary_match"] is True
                and row["kind"] == "admitted_geometric"
                for row in rows
            ) == 2,
        "algebraic_control_count_two":
            sum(
                row["kind"].startswith("algebraic_")
                and row["pass"]
                for row in rows
            ) == 2,
        "rejected_control_count_two":
            sum(
                row["kind"] == "rejected_control"
                and row["pass"]
                for row in rows
            ) == 2,
        "scale_relation_pass": scale_relation_pass
    }

    audit_pass = all(checks.values())

    artifact = {
        "artifact_id": "fre.support_mode.reference_audit.001",
        "verdict": (
            "plaintext_reference_matches_predeclared_fixtures"
            if audit_pass
            else "plaintext_reference_fixture_mismatch"
        ),
        "audit_pass": audit_pass,
        "pipeline_id": "support_mode_reference_v0.1",
        "fixture_set_id": fixture_set["fixture_set_id"],
        "source_hashes": {
            "contract_sha256": contract_sha,
            "receipt_schema_sha256": schema_sha,
            "fixture_set_sha256": fixture_sha,
            "reference_header_sha256":
                sha256(ROOT / "include/fre/support_mode.hpp"),
            "reference_source_sha256":
                sha256(ROOT / "src/support_mode_reference.cpp"),
            "reference_cli_sha256":
                sha256(ROOT / "src/cli/fre_support_reference.cpp")
        },
        "checks": checks,
        "rows": rows,
        "boundary": {
            "reference_pipeline_only": True,
            "fre_receipt_emitted": False,
            "openfhe_backend_admitted": False,
            "key_generation_performed": False,
            "encryption_performed": False,
            "evaluation_performed": False,
            "decryption_performed": False,
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

    summary = {
        "artifact_id": artifact["artifact_id"],
        "audit_pass": audit_pass,
        "verdict": artifact["verdict"],
        "fixture_count": len(rows),
        "passed_count": sum(row["pass"] for row in rows)
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if audit_pass else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            json.dumps({
                "audit_pass": False,
                "error": f"{type(exc).__name__}: {exc}"
            }),
            file=sys.stderr
        )
        raise SystemExit(2)
