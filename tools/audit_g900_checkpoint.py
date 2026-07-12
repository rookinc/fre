#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import subprocess
import traceback

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/json/fre_g900_checkpoint_audit_001.json"
REPORT = Path.home() / "tmp/audit_fre_g900_checkpoint_001.out"

LOCKS = {
    "contracts/fre_g900_recursive_host_v0.1.json":
        "8b8baa98a8d0252f7433f800a5c118c995dee7e078c55be5db787cade1b0d83c",
    "artifacts/json/fre_g900_payload_provenance_001.json":
        "c13bd8b4fc4901b0eb618b4918e77281a01dae1ba0f13ba5adbd9cc8170ce052",
    "artifacts/json/fre_g900_structural_audit_001.json":
        "e92dbcf6e14b83a7af81cca05da683f51633579fabe1781337a6d2664e8ad271",
    "contracts/fre_g900_status_receipt_gate_v0.1.json":
        "a7387dac27472247833007af42fca2ccedd0e1499a8aaae623ebc89f55f9f8b3",
    "schemas/fre_g900_recursive_host_receipt_v0.1.schema.json":
        "9f8ef85656d1536d71bf127f11986c547f16f603fe57543507416bdc4c07b0db",
    "artifacts/receipts/fre_g900_recursive_host_unavailable_v000_001.json":
        "29a951e2467a8e090859446b4e704b0ad8165a5d27272bf75a2b0279f1e9a312",
    "tools/validate_g900_payload.py":
        "b854e30cabe104776978f7f01f405190ce775a068512f7a630aa4ba9f6c827c7",
    "tools/emit_g900_status_receipt.py":
        "84f2cc2eb0660e5e2d626ec784eb86a0426050fd700a9f9fd9ebf95cbff6d7e8",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args):
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(
            "command failed: " + " ".join(args) + "\n"
            + (result.stdout + result.stderr)[-2500:]
        )
    return result.stdout

try:
    for rel, expected in LOCKS.items():
        path = ROOT / rel
        if not path.is_file() or sha(path) != expected:
            raise RuntimeError("pre-audit hash lock failed: " + rel)

    run(["python", "tools/validate_g900_payload.py"])
    run(["python", "tools/emit_g900_status_receipt.py"])

    for rel, expected in LOCKS.items():
        if sha(ROOT / rel) != expected:
            raise RuntimeError("post-rerun hash changed: " + rel)

    contract = json.loads(
        (ROOT / "contracts/fre_g900_recursive_host_v0.1.json").read_text()
    )
    structural = json.loads(
        (ROOT / "artifacts/json/"
         "fre_g900_structural_audit_001.json").read_text()
    )
    gate = json.loads(
        (ROOT / "contracts/"
         "fre_g900_status_receipt_gate_v0.1.json").read_text()
    )
    receipt = json.loads(
        (ROOT / "artifacts/receipts/"
         "fre_g900_recursive_host_unavailable_v000_001.json").read_text()
    )
    provenance = json.loads(
        (ROOT / "artifacts/json/"
         "fre_g900_payload_provenance_001.json").read_text()
    )

    bridge_values = list(receipt["bridge"].values())
    checks = {
        "contract_candidate_not_admitted":
            contract["status"] ==
            "predeclared_recursive_host_candidate_not_admitted",
        "structural_audit_pass":
            structural["audit_pass"] is True,
        "G15_L_Petersen":
            structural["graphs"]["G15"]["graph_class"] ==
            "L(Petersen)",
        "G900_vertices_900":
            structural["graphs"]["G900"]["vertices"] == 900,
        "G900_edges_3600":
            structural["graphs"]["G900"]["edges"] == 3600,
        "G900_degree_eight":
            structural["graphs"]["G900"]["degree"] == 8,
        "canonical_cocycle_nontrivial":
            structural["signing"]["nontrivial_cocycle"] is True,
        "sibling_delta_support_six":
            structural["signing"]["sibling_delta_support"] == 6,
        "seven_payload_files_pinned":
            len(provenance["files"]) == 7,
        "source_commit_unavailable_recorded":
            provenance["source"]["source_commit_available"] is False,
        "one_status_receipt_gate":
            gate["scope"]["receipt_count"] == 1,
        "event_gate_closed":
            gate["permissions"]["admit_G900_event"] is False,
        "cycle_not_admitted":
            receipt["cycle"]["admitted"] is False,
        "trace_not_claimed":
            receipt["cycle"]["trace_preserved"] is False,
        "claim_unavailable":
            receipt["claim"]["status"] == "unavailable"
            and receipt["claim"]["result"] is None,
        "bridge_fields_null":
            all(value is None for value in bridge_values),
        "closure_open":
            receipt["closure"]["class"] == "open",
        "universal_theorem_false":
            receipt["closure"][
                "universal_recursive_host_theorem_claim"
            ] is False,
        "external_truth_false":
            receipt["closure"]["external_truth_claim"] is False,
        "existing_tracked_files_unchanged":
            run(["git", "diff", "--name-only"]).strip() == "",
    }

    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise RuntimeError("checkpoint checks failed: " + ", ".join(failed))

    artifact = {
        "artifact_id": "fre.g900.fail_closed_checkpoint_audit.001",
        "audit_pass": True,
        "verdict":
            "G900_carrier_baked_in_recursive_host_not_admitted",
        "bindings": {
            rel: expected for rel, expected in sorted(LOCKS.items())
        },
        "structural_result": {
            "G15": "L(Petersen)",
            "G30": "signed_2_lift_slip_layer",
            "G60": "locked_chamber_layer",
            "G900": {
                "vertices": 900,
                "edges": 3600,
                "degree": 8,
                "connected": True
            },
            "canonical_signing": {
                "zero_edges": 15,
                "one_edges": 15,
                "nontrivial_cocycle": True
            },
            "sibling_control": {
                "delta_support": 6,
                "switching_class_distinct": True
            }
        },
        "status_receipt": {
            "envelope_id": receipt["envelope_id"],
            "outer_vertex": 0,
            "cycle_t": 0,
            "phase_measure": "360+180+360=900",
            "claim_status": "unavailable",
            "claim_result": None,
            "closure": "open"
        },
        "checks": checks,
        "boundary": {
            "structural_carrier_validated": True,
            "recursive_host_instance_admitted": False,
            "independent_bridge_present": False,
            "transport_cycle_executed": False,
            "earned_claim_emitted": False,
            "universal_theorem_claim": False,
            "observational_closure": False,
            "external_truth_claim": False
        }
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    status = run(["git", "status", "--short"]).rstrip()
    if any(
        line and not line.startswith("?? ")
        for line in status.splitlines()
    ):
        raise RuntimeError("tracked project file unexpectedly changed")

    body = f"""== project ==
{ROOT}

== checkpoint audit tool ==
tools/audit_g900_checkpoint.py: created
sha256: {sha(Path(__file__))}

== checkpoint audit ==
artifacts/json/fre_g900_checkpoint_audit_001.json
artifact_id: {artifact["artifact_id"]}
verdict: {artifact["verdict"]}
sha256: {sha(OUT)}

== structural state ==
G15: L(Petersen)
G30: signed_2_lift_slip_layer
G60: locked_chamber_layer
G900: vertices=900 edges=3600 degree=8 connected=True
canonical_signing: zero=15 one=15 nontrivial=True
sibling_delta_support: 6

== receipt state ==
envelope_id: {receipt["envelope_id"]}
outer_vertex: 0
cycle_t: 0
phase_measure: 360+180+360=900
claim_status: unavailable
closure: open

== checks ==
audit_pass: True
structural_validator_rerun: True
status_receipt_validator_rerun: True
seven_payload_files_pinned: True
existing_tracked_files_unchanged: True
recursive_host_instance_admitted: False
independent_bridge_present: False
transport_cycle_executed: False
earned_claim_emitted: False
universal_theorem_claim: False
observational_closure: False

== git status ==
{status}

== boundary ==
The fail-closed G900 checkpoint passed its audit.
The signed half-flip carrier is baked into FRE.
Recursive hosting remains a declared but unavailable claim.
No transport cycle or recursive-host event executed.
No independent bridge exists.
No earned or universal claim.
No build.
No crypto.
No commit.
No push.

next: document and publish the fail-closed G900 checkpoint
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
