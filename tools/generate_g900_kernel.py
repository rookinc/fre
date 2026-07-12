#!/usr/bin/env python3
"""Independent native constructor for the canonical FRE G900 kernel."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_ID = "fre.g900.native_generator.reference.v0.1"
CONTRACT_ID = "fre.g900.native_generator.v0.1"

INPUTS = {
    "g15": (
        "fixtures/g900/g15_slot_edges.csv",
        "7b94834d507cf2995ec6faf73e2e227a685d831894aa98f2647556d8b922b8f6",
    ),
    "g60": (
        "fixtures/g900/g60_local_edges.csv",
        "c700a185fab6a5f434da09b7acb716b96c76170774bee946af8ea907e4fe7f9f",
    ),
    "signing": (
        "fixtures/g900/carrier_signing_table.csv",
        "9b3cf812cc0f6d7b065666c81fa6d16fd3e3b8a98955c264709337c7f3e7efb7",
    ),
}


def locked_path(role):
    relative, expected = INPUTS[role]
    path = ROOT / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError("input hash mismatch: " + role)
    return path


def read_pairs(path, left, right):
    with path.open("r", encoding="ascii", newline="") as handle:
        rows = list(csv.DictReader(handle))
    pairs = set()
    for row in rows:
        a, b = int(row[left]), int(row[right])
        if a == b:
            raise RuntimeError("loop in source pair table")
        pairs.add((min(a, b), max(a, b)))
    if len(pairs) != len(rows):
        raise RuntimeError("duplicate source pair")
    return pairs


def read_signing(path):
    with path.open("r", encoding="ascii", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = []
    for row in rows:
        a, b, sign = int(row["slot_u"]), int(row["slot_v"]), int(row["sign"])
        if sign not in (0, 1):
            raise RuntimeError("sign outside {0,1}")
        law = "identity_x" if sign == 0 else "half_flip_x_plus_30_mod_60"
        if row["carrier_law"] != law or int(row["external_edge_count"]) != 60:
            raise RuntimeError("signing law mismatch")
        result.append((min(a, b), max(a, b), sign))
    if len(set(result)) != len(rows):
        raise RuntimeError("duplicate signed carrier")
    return result


def normalize(u, v):
    if u == v:
        raise RuntimeError("generated loop")
    return (min(u, v), max(u, v))


def generate():
    slots = read_pairs(locked_path("g15"), "slot_u", "slot_v")
    local = read_pairs(locked_path("g60"), "local_u", "local_v")
    signing = read_signing(locked_path("signing"))
    if len(slots) != 30 or len(local) != 120 or len(signing) != 30:
        raise RuntimeError("source cardinality mismatch")
    if {(a, b) for a, b, _ in signing} != slots:
        raise RuntimeError("signing support differs from G15")

    internal = {
        normalize(60 * slot + a, 60 * slot + b)
        for slot in range(15)
        for a, b in local
    }
    carrier = {
        normalize(
            60 * slot_a + alpha,
            60 * slot_b + ((alpha + 30 * sign) % 60),
        )
        for slot_a, slot_b, sign in signing
        for alpha in range(60)
    }
    if internal & carrier:
        raise RuntimeError("edge partitions overlap")
    edges = internal | carrier

    degree = [0] * 900
    adjacency = [set() for _ in range(900)]
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
        adjacency[u].add(v)
        adjacency[v].add(u)

    seen = {0}
    frontier = [0]
    while frontier:
        u = frontier.pop()
        for v in adjacency[u] - seen:
            seen.add(v)
            frontier.append(v)

    serialized = "".join(
        f"{u},{v}\n" for u, v in sorted(edges)
    ).encode("ascii")
    summary = {
        "generator_id": GENERATOR_ID,
        "contract_id": CONTRACT_ID,
        "target_read": False,
        "vertices": len(seen),
        "internal_edges": len(internal),
        "carrier_edges": len(carrier),
        "total_edges": len(edges),
        "degree_min": min(degree),
        "degree_max": max(degree),
        "connected": len(seen) == 900,
        "canonical_edge_digest": hashlib.sha256(serialized).hexdigest(),
    }
    return edges, summary


def main():
    _, summary = generate()
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
