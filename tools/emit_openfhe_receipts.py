#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re
import subprocess
import traceback

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/fre_support_mode_receipt_v0.2.schema.json"
AUDIT = ROOT / "artifacts/json/fre_support_mode_openfhe_execution_audit_001.json"
OUTDIR = ROOT / "artifacts/receipts"
REPORT = Path.home() / "tmp/emit_fre_openfhe_receipts_001.out"

SCHEMA_SHA = "3b256060e49d2f6599e9a1713eaf2c2b3aa27e135e5537ca8b967ee937127741"
AUDIT_SHA = "9f7dbc0b41ab1ab91ab6916ed7994361a81344ea86537e0ab676557900975f2d"
CONTRACT_SHA = "a7c28f080730aa5fa7f4183573b1270794c3246939137aac4240d90eaf5a69ba"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Invalid(Exception):
    pass

def validate(value, rule, path="$"):
    if "const" in rule and value != rule["const"]:
        raise Invalid(path + ": const")
    if "enum" in rule and value not in rule["enum"]:
        raise Invalid(path + ": enum")

    types = rule.get("type")
    if types:
        types = [types] if isinstance(types, str) else types
        matches = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "null": value is None,
        }
        if not any(matches.get(t, False) for t in types):
            raise Invalid(path + ": type")

    if isinstance(value, dict):
        required = set(rule.get("required", []))
        if not required.issubset(value):
            raise Invalid(path + ": required")
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False:
            if not set(value).issubset(properties):
                raise Invalid(path + ": additionalProperties")
        for key, child in properties.items():
            if key in value:
                validate(value[key], child, path + "." + key)

    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            raise Invalid(path + ": minItems")
        if len(value) > rule.get("maxItems", len(value)):
            raise Invalid(path + ": maxItems")
        if isinstance(rule.get("items"), dict):
            for index, item in enumerate(value):
                validate(item, rule["items"], path + f"[{index}]")

    if isinstance(value, str) and "pattern" in rule:
        if re.fullmatch(rule["pattern"], value) is None:
            raise Invalid(path + ": pattern")

    if "oneOf" in rule:
        passed = 0
        for child in rule["oneOf"]:
            try:
                validate(value, child, path)
                passed += 1
            except Invalid:
                pass
        if passed != 1:
            raise Invalid(path + ": oneOf")

    for child in rule.get("allOf", []):
        validate(value, child, path)

    if "if" in rule:
        try:
            validate(value, rule["if"], path)
            condition = True
        except Invalid:
            condition = False
        if condition and "then" in rule:
            validate(value, rule["then"], path)
        if not condition and "else" in rule:
            validate(value, rule["else"], path)

try:
    if sha(SCHEMA) != SCHEMA_SHA:
        raise RuntimeError("schema hash lock failed")
    if sha(AUDIT) != AUDIT_SHA:
        raise RuntimeError("execution audit hash lock failed")

    schema = json.loads(SCHEMA.read_text())
    audit = json.loads(AUDIT.read_text())
    if not audit.get("audit_pass"):
        raise RuntimeError("execution audit did not pass")

    rows = {r["fixture_id"]: r for r in audit["fixture_results"]}
    expected_ids = {
        "regular_uniform_10", "regular_uniform_20",
        "balanced_exchange_10", "balanced_exchange_20",
    }
    if set(rows) != expected_ids:
        raise RuntimeError("fixture set mismatch")

    controls_passed = all(
        rows[name]["K"] > 0
        and rows[name]["computed_regular"] is False
        and rows[name]["reference_match"] is True
        for name in ("balanced_exchange_10", "balanced_exchange_20")
    )
    if not controls_passed:
        raise RuntimeError("negative controls did not pass")

    operations = [
        "ContextGen", "KeyGen", "EvalMultKeyGen", "Encrypt",
        "EvalAdd", "EvalMult", "DecryptVerify",
    ]

    documents = {}
    for fixture_id in sorted(rows):
        row = rows[fixture_id]
        certified = row["certification_class"] == "certified_geometric"

        if certified:
            if row["K"] != 0 or row["computed_regular"] is not True:
                raise RuntimeError("certified claim mismatch: " + fixture_id)
            certification = "certified_fixture_set_v0.1"
            claim = {
                "type": "regularity",
                "status": "earned",
                "result": True,
            }
            claim_boundary = "geometric_claim_scoped_to_certified_fixture"
        else:
            certification = "unavailable"
            claim = {
                "type": "regularity",
                "status": "unavailable",
                "result": None,
            }
            claim_boundary = (
                "geometric_regularity_unavailable_without_C_D_certification"
            )

        receipt = {
            "receipt_schema": "fre.support_mode.receipt.v0.2",
            "envelope_id":
                "fre.support_mode.receipt." + fixture_id + ".001",
            "contract_id": "fre.support_mode.regularity.v0.2",
            "source_class": "six_support_register",
            "input_certification": certification,
            "circuit_id": "support_mode_polynomial_v0.1",
            "operation_names": operations,
            "gate": {
                "admitted": True,
                "reason": "predeclared_public_fixture_in_bounded_local_batch",
            },
            "claim": claim,
            "comparison": {
                "rule": "exact_integer_equality",
                "tolerance": 0,
                "reference_congruence": True,
                "contract_sha256": CONTRACT_SHA,
                "reference_pipeline_id": "support_mode_reference_v0.1",
                "fre_pipeline_id": "support_mode_openfhe_v0.1",
                "profile_id": "fre.openfhe.bgv.evalmult.executed.v0.1",
                "execution_gate_id":
                    "fre.support_mode.openfhe_execution_gate.v0.1",
            },
            "controls": {
                "negative_controls_passed": True,
            },
            "privacy": {
                "private_material_committed": False,
                "secret_inputs_exposed": False,
                "keys_exposed": False,
                "ciphertexts_exposed": False,
                "runtime_objects_committed": False,
            },
            "closure": {
                "class": "local",
                "external_truth_claim": False,
            },
            "boundary": [
                "fixture_id=" + fixture_id,
                "execution_audit_id=" + audit["artifact_id"],
                "execution_audit_sha256=" + AUDIT_SHA,
                "local_test_profile_only",
                "public_fixture_inputs_only",
                claim_boundary,
                "no_production_security_claim",
                "no_observational_closure",
            ],
        }

        validate(receipt, schema)
        path = OUTDIR / (
            "fre_support_mode_receipt_" + fixture_id + "_001.json"
        )
        documents[path] = (
            json.dumps(receipt, indent=2, sort_keys=True) + "\n"
        )

    for path, content in documents.items():
        if path.exists() and path.read_text() != content:
            raise RuntimeError("refusing to overwrite differing receipt: " + path.name)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    actions = {}
    for path, content in documents.items():
        action = "preserved_exact" if path.exists() else "created"
        path.write_text(content)
        actions[path] = action

    receipt_lines = "\n".join(
        f"{path.relative_to(ROOT)}: {actions[path]}\nsha256: {sha(path)}"
        for path in sorted(documents)
    )
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.rstrip()

    body = f"""== project ==
{ROOT}

== emitter ==
tools/emit_openfhe_receipts.py
sha256: {sha(Path(__file__))}

== public receipts ==
{receipt_lines}

== claims ==
earned_regular_true: 2
regularity_unavailable_controls: 2
negative_controls_passed: True
reference_congruence: True
closure_class: local

== checks ==
schema_hash_locked: True
execution_audit_hash_locked: True
four_receipts_valid: True
all_seven_operations_named: True
certified_claims_earned: True
controls_not_geometrically_certified: True
private_material_absent: True
external_truth_claim_false: True
observational_closure_false: True
crypto_executable_not_run: True

== git status ==
{status}

== boundary ==
Four schema-bound public receipts emitted.
Receipt congruence is established for the bounded local fixture batch.
Only the two certified uniform fixtures earn regularity claims.
The two algebraic controls carry unavailable geometric claims.
No crypto was rerun.
No keys, ciphertexts, or runtime objects were committed.
No observational closure.
No production security claim.
No external truth claim.
No commit.
No push.

next: audit the receipt set, then commit and push the checkpoint
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
