#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re
import subprocess
import traceback

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    ROOT / "schemas/fre_g900_recursive_host_receipt_v0.1.schema.json"
)
GATE_PATH = ROOT / "contracts/fre_g900_status_receipt_gate_v0.1.json"
OUT = (
    ROOT / "artifacts/receipts/"
    "fre_g900_recursive_host_unavailable_v000_001.json"
)
REPORT = Path.home() / "tmp/emit_fre_g900_status_receipt_001.out"

LOCKS = {
    "contracts/fre_g900_recursive_host_v0.1.json":
        "8b8baa98a8d0252f7433f800a5c118c995dee7e078c55be5db787cade1b0d83c",
    "artifacts/json/fre_g900_payload_provenance_001.json":
        "c13bd8b4fc4901b0eb618b4918e77281a01dae1ba0f13ba5adbd9cc8170ce052",
    "artifacts/json/fre_g900_structural_audit_001.json":
        "e92dbcf6e14b83a7af81cca05da683f51633579fabe1781337a6d2664e8ad271",
    "schemas/fre_g900_recursive_host_receipt_v0.1.schema.json":
        "9f8ef85656d1536d71bf127f11986c547f16f603fe57543507416bdc4c07b0db",
    "contracts/fre_g900_status_receipt_gate_v0.1.json":
        "a7387dac27472247833007af42fca2ccedd0e1499a8aaae623ebc89f55f9f8b3",
}

class Invalid(Exception):
    pass

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(value, rule, path="$"):
    if isinstance(rule, bool):
        if rule is False:
            raise Invalid(path + ": forbidden")
        return

    if "const" in rule and value != rule["const"]:
        raise Invalid(path + ": const")
    if "enum" in rule and value not in rule["enum"]:
        raise Invalid(path + ": enum")

    declared = rule.get("type")
    if declared:
        declared = [declared] if isinstance(declared, str) else declared
        matches = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "integer": (
                isinstance(value, int) and not isinstance(value, bool)
            ),
            "null": value is None,
        }
        if not any(matches.get(item, False) for item in declared):
            raise Invalid(path + ": type")

    if isinstance(value, dict):
        required = set(rule.get("required", []))
        if not required.issubset(value):
            raise Invalid(path + ": required")

        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False:
            if not set(value).issubset(properties):
                raise Invalid(path + ": additionalProperties")

        for name, child in properties.items():
            if name in value:
                validate(value[name], child, path + "." + name)

    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            raise Invalid(path + ": minItems")
        if len(value) > rule.get("maxItems", len(value)):
            raise Invalid(path + ": maxItems")

        prefix = rule.get("prefixItems", [])
        for index, child in enumerate(prefix):
            if index < len(value):
                validate(value[index], child, path + f"[{index}]")

        items = rule.get("items")
        if items is False and len(value) > len(prefix):
            raise Invalid(path + ": items")
        if isinstance(items, dict):
            for index in range(len(prefix), len(value)):
                validate(value[index], items, path + f"[{index}]")

    if isinstance(value, str):
        if "pattern" in rule:
            if re.fullmatch(rule["pattern"], value) is None:
                raise Invalid(path + ": pattern")
        if len(value) < rule.get("minLength", 0):
            raise Invalid(path + ": minLength")

    if isinstance(value, int) and not isinstance(value, bool):
        if value < rule.get("minimum", value):
            raise Invalid(path + ": minimum")
        if value > rule.get("maximum", value):
            raise Invalid(path + ": maximum")

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
    for rel, expected in LOCKS.items():
        path = ROOT / rel
        if not path.is_file() or sha(path) != expected:
            raise RuntimeError("hash lock failed: " + rel)

    schema = json.loads(SCHEMA_PATH.read_text())
    gate = json.loads(GATE_PATH.read_text())

    expected_envelope = (
        "fre.g900.recursive_host.unavailable.v000.001"
    )
    if (
        gate["status"] !=
            "one_unavailable_status_receipt_admitted_not_emitted"
        or gate["scope"]["envelope_id"] != expected_envelope
        or gate["permissions"][
            "emit_exact_nonexecution_status_receipt"
        ] is not True
        or gate["permissions"]["emit_any_other_receipt"] is not False
    ):
        raise RuntimeError("status receipt gate is not exact")

    receipt = {
        "receipt_schema": "fre.g900.recursive_host.receipt.v0.1",
        "envelope_id": expected_envelope,
        "contract_id": "fre.g900.recursive_host.v0.1",
        "contract_sha256": LOCKS[
            "contracts/fre_g900_recursive_host_v0.1.json"
        ],
        "kernel": {
            "kernel_id": "fre.g900.signed_half_flip_carrier.v0.1",
            "structural_audit_id": "fre.g900.structural_audit.001",
            "structural_audit_sha256": LOCKS[
                "artifacts/json/fre_g900_structural_audit_001.json"
            ],
            "vertices": 900,
            "edges": 3600,
            "degree": 8,
            "G15_vertices": 15,
            "G30_vertices": 30,
            "G60_vertices": 60
        },
        "cycle": {
            "cycle_id": "fre.g900.cycle.probe.000",
            "t": 0,
            "phase_word": [
                "W_out", "X_out", "Y_out", "Z_out", "I_t",
                "Z_return", "Y_return", "X_return", "W_return"
            ],
            "outbound_measure": 360,
            "bounce_measure": 180,
            "return_measure": 360,
            "total_measure": 900,
            "measure_class":
                "formal_cycle_measure_not_physical_angle",
            "receipt_id": expected_envelope,
            "admitted": False,
            "trace_preserved": False
        },
        "gate": {
            "contract_predeclared": True,
            "structural_payload_validated": True,
            "recursive_host_event_admitted": False,
            "reason":
                "structural_payload_validated_independent_bridge_missing"
        },
        "host": {
            "outer_slot": 0,
            "outer_local": 0,
            "outer_vertex": 0,
            "address_law_checked": True,
            "host_boundary_id": "fre.g900.host.v000",
            "inner_graph_id":
                "fre.g900.signed_half_flip_carrier.v0.1",
            "inner_embedding_declared": True,
            "outer_projection_declared": True,
            "projection_target_matches_outer_vertex": True,
            "ordinary_induced_subgraph_claim": False,
            "unbounded_material_recursion_claim": False
        },
        "bridge": {
            "environment_id": None,
            "environment_distinct_from_host": None,
            "independent": None,
            "cycle_through_environment": None,
            "realization_map_id": None,
            "inner_trace_sha256": None,
            "ambient_trace_sha256": None,
            "receipt_congruence": None
        },
        "controls": {
            "sibling_signing_checked": True,
            "sibling_switching_class_distinct": True,
            "independent_bridge_negative_control_passed": None,
            "circular_justification": False
        },
        "claim": {
            "type": "vertex_local_recursive_host_admission",
            "scope": "one_outer_vertex_instance",
            "status": "unavailable",
            "result": None
        },
        "privacy": {
            "private_material_committed": False,
            "secret_inputs_exposed": False,
            "runtime_objects_committed": False
        },
        "closure": {
            "class": "open",
            "external_truth_claim": False,
            "physical_claim": False,
            "production_security_claim": False,
            "universal_recursive_host_theorem_claim": False
        },
        "boundary": [
            "authorized_by="
            "fre.g900.nonexecution_status_receipt_gate.v0.1",
            "status_receipt_not_execution_receipt",
            "structural_validation_not_recursive_host_admission",
            "independent_bridge_missing",
            "distinct_environment_missing",
            "ambient_trace_missing",
            "no_receipts_no_true",
            "pressure_exists_but_pressure_is_not_authorization",
            "no_observational_closure"
        ]
    }

    validate(receipt, schema)

    if receipt["host"]["outer_vertex"] != (
        receipt["host"]["outer_slot"] * 60
        + receipt["host"]["outer_local"]
    ):
        raise RuntimeError("outer address law failed")
    if receipt["cycle"]["total_measure"] != (
        receipt["cycle"]["outbound_measure"]
        + receipt["cycle"]["bounce_measure"]
        + receipt["cycle"]["return_measure"]
    ):
        raise RuntimeError("cycle measure law failed")

    encoded = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if OUT.exists() and OUT.read_text() != encoded:
        raise RuntimeError("refusing to overwrite differing receipt")

    action = "preserved_exact" if OUT.exists() else "created"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(encoded)

    git_status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.rstrip()

    body = f"""== project ==
{ROOT}

== status receipt emitter ==
tools/emit_g900_status_receipt.py: created
sha256: {sha(Path(__file__))}

== gated nonexecution receipt ==
artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json
action: {action}
envelope_id: {receipt["envelope_id"]}
sha256: {sha(OUT)}

== instance ==
outer_address: slot=0 local=0 vertex=0
cycle_t: 0
phase_measure: 360+180+360=900
cycle_admitted: False
trace_preserved: False
event_admitted: False

== result ==
claim_type: vertex_local_recursive_host_admission
claim_status: unavailable
claim_result: null
closure_class: open

== bridge ==
environment_id: null
independent: null
inner_trace_sha256: null
ambient_trace_sha256: null
receipt_congruence: null

== checks ==
gate_hash_locked: True
schema_hash_locked: True
schema_validation_passed: True
exact_gated_envelope: True
outer_address_law_passed: True
cycle_measure_law_passed: True
sibling_control_recorded: True
earned_claim_false: True
universal_theorem_claim_false: True
transport_cycle_not_executed: True

== git status ==
{git_status}

== boundary ==
The exact gated unavailable-status receipt was emitted.
This is not a G900 execution receipt.
No transport cycle executed.
No independent bridge or ambient trace exists.
No recursive-host instance was admitted.
No earned or universal recursive-host claim.
Closure remains open.
No build.
No crypto.
No commit.
No push.

next: audit and document the fail-closed G900 checkpoint
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
