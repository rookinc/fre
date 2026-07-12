#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import subprocess
import traceback

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/fre_support_mode_receipt_v0.2.schema.json"
EXEC_AUDIT = ROOT / "artifacts/json/fre_support_mode_openfhe_execution_audit_001.json"
RECEIPTS = ROOT / "artifacts/receipts"
OUT = ROOT / "artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json"
REPORT = Path.home() / "tmp/audit_fre_openfhe_receipts_001.out"

SCHEMA_SHA = "3b256060e49d2f6599e9a1713eaf2c2b3aa27e135e5537ca8b967ee937127741"
EXEC_SHA = "9f7dbc0b41ab1ab91ab6916ed7994361a81344ea86537e0ab676557900975f2d"
EMITTER_SHA = "3adc11119fb6ebf4d826fe6597238ca32e369a83e39827fb3223cd7787707f76"

EXPECTED = {
    "balanced_exchange_10": (
        "7fe1cb54e1cefa62db5cc6a85e72422083a30637ee17165c26ddb03e493906a4",
        False,
    ),
    "balanced_exchange_20": (
        "2230b6ab967ecde31753e2a7603e64c52efa47ca8196a536c68e221b6a710d9f",
        False,
    ),
    "regular_uniform_10": (
        "9fdb5d514c44430b14d710892b75061e454753ecb14549b4463ab064ce8cc08f",
        True,
    ),
    "regular_uniform_20": (
        "cbcf3ddaf3cfa8e429c6f56f7caaffe937a133fc1e3006dec19918b87b168078",
        True,
    ),
}

OPS = [
    "ContextGen", "KeyGen", "EvalMultKeyGen", "Encrypt",
    "EvalAdd", "EvalMult", "DecryptVerify",
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

try:
    if sha(SCHEMA) != SCHEMA_SHA:
        raise RuntimeError("schema hash lock failed")
    if sha(EXEC_AUDIT) != EXEC_SHA:
        raise RuntimeError("execution audit hash lock failed")
    if sha(ROOT / "tools/emit_openfhe_receipts.py") != EMITTER_SHA:
        raise RuntimeError("receipt emitter hash lock failed")

    schema = json.loads(SCHEMA.read_text())
    execution = json.loads(EXEC_AUDIT.read_text())
    execution_rows = {
        row["fixture_id"]: row for row in execution["fixture_results"]
    }

    expected_names = {
        "fre_support_mode_receipt_" + fixture_id + "_001.json"
        for fixture_id in EXPECTED
    }
    actual_names = {p.name for p in RECEIPTS.glob("*.json")}
    if actual_names != expected_names:
        raise RuntimeError("receipt file set is not exact")

    required_top = set(schema["required"])
    allowed_top = set(schema["properties"])
    records = []
    earned = 0
    unavailable = 0

    for fixture_id, (expected_sha, certified) in EXPECTED.items():
        path = RECEIPTS / (
            "fre_support_mode_receipt_" + fixture_id + "_001.json"
        )
        if sha(path) != expected_sha:
            raise RuntimeError("receipt hash failed: " + fixture_id)

        receipt = json.loads(path.read_text())
        if set(receipt) != required_top or set(receipt) != allowed_top:
            raise RuntimeError("top-level field set failed: " + fixture_id)
        if fixture_id not in execution_rows:
            raise RuntimeError("execution row missing: " + fixture_id)

        fixed = {
            "receipt_schema": "fre.support_mode.receipt.v0.2",
            "contract_id": "fre.support_mode.regularity.v0.2",
            "source_class": "six_support_register",
            "circuit_id": "support_mode_polynomial_v0.1",
        }
        for key, value in fixed.items():
            if receipt[key] != value:
                raise RuntimeError(key + " failed: " + fixture_id)

        if receipt["operation_names"] != OPS:
            raise RuntimeError("operation sequence failed: " + fixture_id)
        if receipt["gate"] != {
            "admitted": True,
            "reason": "predeclared_public_fixture_in_bounded_local_batch",
        }:
            raise RuntimeError("gate binding failed: " + fixture_id)

        comparison = receipt["comparison"]
        if (
            comparison["reference_congruence"] is not True
            or comparison["contract_sha256"] !=
                "a7c28f080730aa5fa7f4183573b1270794c3246939137aac4240d90eaf5a69ba"
            or comparison["execution_gate_id"] !=
                "fre.support_mode.openfhe_execution_gate.v0.1"
            or comparison["profile_id"] !=
                "fre.openfhe.bgv.evalmult.executed.v0.1"
            or comparison["rule"] != "exact_integer_equality"
            or comparison["tolerance"] != 0
        ):
            raise RuntimeError("comparison binding failed: " + fixture_id)

        if any(receipt["privacy"].values()):
            raise RuntimeError("privacy boundary failed: " + fixture_id)
        if receipt["closure"] != {
            "class": "local",
            "external_truth_claim": False,
        }:
            raise RuntimeError("closure failed: " + fixture_id)
        if receipt["controls"]["negative_controls_passed"] is not True:
            raise RuntimeError("control status failed: " + fixture_id)

        boundary = set(receipt["boundary"])
        required_boundary = {
            "fixture_id=" + fixture_id,
            "execution_audit_id=" + execution["artifact_id"],
            "execution_audit_sha256=" + EXEC_SHA,
            "no_observational_closure",
        }
        if not required_boundary.issubset(boundary):
            raise RuntimeError("audit boundary failed: " + fixture_id)

        row = execution_rows[fixture_id]
        if certified:
            if (
                receipt["input_certification"] !=
                    "certified_fixture_set_v0.1"
                or receipt["claim"] != {
                    "type": "regularity",
                    "status": "earned",
                    "result": True,
                }
                or row["K"] != 0
                or row["computed_regular"] is not True
            ):
                raise RuntimeError("earned claim failed: " + fixture_id)
            earned += 1
        else:
            if (
                receipt["input_certification"] != "unavailable"
                or receipt["claim"] != {
                    "type": "regularity",
                    "status": "unavailable",
                    "result": None,
                }
                or row["K"] <= 0
                or row["computed_regular"] is not False
            ):
                raise RuntimeError("control claim failed: " + fixture_id)
            unavailable += 1

        records.append({
            "fixture_id": fixture_id,
            "receipt_file": str(path.relative_to(ROOT)),
            "receipt_sha256": expected_sha,
            "claim_status": receipt["claim"]["status"],
            "reference_congruence": True,
        })

    checks = {
        "receipt_file_set_exact": True,
        "receipt_hashes_locked": True,
        "top_level_fields_exact": True,
        "execution_audit_bound": True,
        "all_seven_operations_exact": True,
        "earned_claim_count_two": earned == 2,
        "unavailable_claim_count_two": unavailable == 2,
        "negative_controls_passed": True,
        "private_material_absent": True,
        "local_closure_only": True,
        "external_truth_claim_false": True,
    }
    if not all(checks.values()):
        raise RuntimeError("receipt audit checks failed")

    artifact = {
        "artifact_id": "fre.support_mode.openfhe_receipt_audit.001",
        "audit_pass": True,
        "verdict":
            "schema_bound_receipt_congruence_for_bounded_local_batch",
        "schema_sha256": SCHEMA_SHA,
        "execution_audit_id": execution["artifact_id"],
        "execution_audit_sha256": EXEC_SHA,
        "receipt_count": len(records),
        "receipts": records,
        "checks": checks,
        "closure": {
            "class": "local",
            "observational": False,
            "external_truth_claim": False,
        },
    }
    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.rstrip()

    body = f"""== project ==
{ROOT}

== receipt audit tool ==
tools/audit_openfhe_receipts.py: created
sha256: {sha(Path(__file__))}

== receipt audit artifact ==
artifacts/json/fre_support_mode_openfhe_receipt_audit_001.json
artifact_id: {artifact["artifact_id"]}
verdict: {artifact["verdict"]}
sha256: {sha(OUT)}

== counts ==
receipts: {len(records)}
earned_regular_true: {earned}
regularity_unavailable: {unavailable}

== checks ==
audit_pass: True
receipt_file_set_exact: True
receipt_hashes_locked: True
execution_audit_bound: True
all_seven_operations_exact: True
claim_split_correct: True
private_material_absent: True
local_closure_only: True
external_truth_claim_false: True
crypto_executable_not_run: True

== git status ==
{status}

== boundary ==
The four-receipt set passed its independent audit.
Bounded local receipt congruence is recorded.
No crypto was rerun.
No observational closure.
No production security claim.
No external truth claim.
No commit.
No push.

next: build, test, commit, and push the bounded execution checkpoint
"""
except Exception as exc:
    body = f"""ERROR
{type(exc).__name__}: {exc}
{traceback.format_exc()}
NEXT
Return this OUT == receipt without closing Termux.
"""

report = "OUT ==\n\n" + body
REPORT.write_text(report)
subprocess.run(
    ["termux-clipboard-set"],
    input=report,
    text=True,
    check=False,
)
print(report)
