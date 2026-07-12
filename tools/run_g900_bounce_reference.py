#!/usr/bin/env python3
"""Plaintext reference automaton for one FRE G900 bounce cycle."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/fre_g900_bounce_grammar_v0.1.json"
CONTRACT_HASH = "80ac01520f3cc229425dd925a11efdda2c82d3a3fb8e9eead3fb424f86e66cfe"
PIPELINE_ID = "fre.g900.bounce_reference.v0.1"


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_contract():
    raw = CONTRACT.read_bytes()
    if digest_bytes(raw) != CONTRACT_HASH:
        raise RuntimeError("bounce contract hash mismatch")
    value = json.loads(raw.decode("ascii"))
    if value.get("contract_id") != "fre.g900.bounce_grammar.v0.1":
        raise RuntimeError("bounce contract id mismatch")
    return value


def state_at(t, tick):
    if not 0 <= tick <= 900:
        raise RuntimeError("phase tick outside 0..900")

    if tick == 0:
        segment = "initial"
        step = 0
        vertex_role = "source"
        direction = "outward"
    elif tick <= 360:
        segment = "outward"
        step = tick
        vertex_role = "target" if tick == 360 else "edge_interior"
        direction = "outward"
    elif tick <= 540:
        segment = "turnaround"
        step = tick - 360
        vertex_role = "target"
        direction = "return" if tick == 540 else "turning"
    else:
        segment = "return"
        step = tick - 540
        vertex_role = "source" if tick == 900 else "edge_interior"
        direction = "returned" if tick == 900 else "return"

    slip_bit = 1 if 360 <= tick < 900 else 0
    chamber_lock = 1 if tick >= 540 else 0
    receipt_state = "I_0" if tick == 900 else "absent"

    return {
        "cycle_t": t,
        "phase_tick": tick,
        "segment": segment,
        "segment_step": step,
        "vertex_role": vertex_role,
        "direction": direction,
        "G30_slip_bit": slip_bit,
        "G60_chamber_lock": chamber_lock,
        "receipt_state": receipt_state,
    }


def build_trace(contract):
    t = contract["cycle"]["t"]
    states = [state_at(t, tick) for tick in range(901)]

    encoded = "".join(
        canonical(state) + "\n" for state in states
    ).encode("ascii")
    trace_sha256 = digest_bytes(encoded)

    receipt_body = {
        "grammar_contract_id": contract["contract_id"],
        "cycle_t": t,
        "oriented_edge": contract["oriented_edge"],
        "phase_partition": [360, 180, 360],
        "trace_sha256": trace_sha256,
        "prior_receipt_sha256": None,
    }
    receipt_sha256 = digest_bytes(
        canonical(receipt_body).encode("ascii")
    )

    counts = {
        "initial": sum(s["segment"] == "initial" for s in states),
        "outward": sum(s["segment"] == "outward" for s in states),
        "turnaround":
            sum(s["segment"] == "turnaround" for s in states),
        "return": sum(s["segment"] == "return" for s in states),
    }

    checks = {
        "state_count_901": len(states) == 901,
        "transition_count_900":
            states[-1]["phase_tick"] - states[0]["phase_tick"]
            == 900,
        "segment_counts_exact":
            counts
            == {
                "initial": 1,
                "outward": 360,
                "turnaround": 180,
                "return": 360,
            },
        "target_reached_at_360":
            states[360]["vertex_role"] == "target",
        "lock_set_at_540":
            states[540]["G60_chamber_lock"] == 1,
        "source_returned_at_900":
            states[900]["vertex_role"] == "source",
        "slip_involution_closed":
            states[0]["G30_slip_bit"] == 0
            and states[360]["G30_slip_bit"] == 1
            and states[900]["G30_slip_bit"] == 0,
        "lock_persists_on_return":
            all(
                state["G60_chamber_lock"] == 1
                for state in states[540:]
            ),
        "receipt_only_at_completion":
            all(
                state["receipt_state"] == "absent"
                for state in states[:900]
            )
            and states[900]["receipt_state"] == "I_0",
        "return_state_distinct":
            states[0] != states[900],
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError("trace checks failed: " + ", ".join(failed))

    return {
        "pipeline_id": PIPELINE_ID,
        "contract_id": contract["contract_id"],
        "cycle_id": contract["cycle"]["cycle_id"],
        "cycle_t": t,
        "phase_measure": contract["cycle"]["phase_measure"],
        "transition_count": 900,
        "state_count": len(states),
        "segment_state_counts": counts,
        "source_vertex":
            contract["oriented_edge"]["source"]["vertex"],
        "target_vertex":
            contract["oriented_edge"]["target"]["vertex"],
        "trace_sha256": trace_sha256,
        "receipt_id": "I_0",
        "receipt_sha256": receipt_sha256,
        "final_state": states[-1],
        "checks": checks,
        "physical_claim": False,
    }


def main():
    result = build_trace(load_contract())
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
