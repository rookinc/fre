#!/usr/bin/env python3
"""Construct the six-toggle sibling G900 negative control."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID = "fre.g900.sibling_signing.negative_control.v0.1"
CANONICAL_DIGEST = "e261704922e6aa218126561bbf0d0b488d9eecd79b34fbeb08e66311e42bbd60"

INPUTS = {
    "g15": (
        "fixtures/g900/g15_slot_edges.csv",
        "7b94834d507cf2995ec6faf73e2e227a685d831894aa98f2647556d8b922b8f6",
    ),
    "g60": (
        "fixtures/g900/g60_local_edges.csv",
        "c700a185fab6a5f434da09b7acb716b96c76170774bee946af8ea907e4fe7f9f",
    ),
    "sibling": (
        "fixtures/g900/sibling_candidate_signing_table.csv",
        "8ad921c2af2f48e220e6c1c8a3a72aaecc64f56791bbfbd15b66f2211af11eba",
    ),
}


def locked_path(role):
    relative, expected = INPUTS[role]
    path = ROOT / relative
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError("input hash mismatch: " + role)
    return path


def read_pairs(path, left, right):
    with path.open("r", encoding="ascii", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = set()
    for row in rows:
        a, b = int(row[left]), int(row[right])
        if a == b:
            raise RuntimeError("loop in source pair")
        pair = (min(a, b), max(a, b))
        if pair in result:
            raise RuntimeError("duplicate source pair")
        result.add(pair)
    return result


def read_sibling(path):
    required = [
        "slot_a",
        "slot_b",
        "canonical_sign",
        "delta",
        "sibling_sign",
    ]
    with path.open("r", encoding="ascii", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != required:
            raise RuntimeError("sibling signing column mismatch")
        rows = list(reader)

    result = []
    support = set()
    seen = set()
    for row in rows:
        a = int(row["slot_a"])
        b = int(row["slot_b"])
        canonical = int(row["canonical_sign"])
        delta = int(row["delta"])
        sibling = int(row["sibling_sign"])
        if canonical not in (0, 1) or delta not in (0, 1):
            raise RuntimeError("non-binary signing value")
        if sibling != (canonical ^ delta):
            raise RuntimeError("sibling XOR relation failed")
        pair = (min(a, b), max(a, b))
        if pair in seen:
            raise RuntimeError("duplicate sibling carrier")
        seen.add(pair)
        result.append((pair[0], pair[1], sibling))
        if delta == 1:
            support.add(pair)
    return result, support


def edge(u, v):
    if u == v:
        raise RuntimeError("generated loop")
    return (min(u, v), max(u, v))


def main():
    slots = read_pairs(locked_path("g15"), "slot_u", "slot_v")
    local = read_pairs(locked_path("g60"), "local_u", "local_v")
    signing, delta_support = read_sibling(locked_path("sibling"))

    if len(slots) != 30 or len(local) != 120:
        raise RuntimeError("source cardinality mismatch")
    if len(signing) != 30 or len(delta_support) != 6:
        raise RuntimeError("sibling support cardinality mismatch")
    if {(a, b) for a, b, _ in signing} != slots:
        raise RuntimeError("sibling signing support differs from G15")

    internal = {
        edge(60 * slot + a, 60 * slot + b)
        for slot in range(15)
        for a, b in local
    }
    carrier = {
        edge(
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
    sibling_digest = hashlib.sha256(serialized).hexdigest()

    result = {
        "control_id": CONTROL_ID,
        "vertices": len(seen),
        "internal_edges": len(internal),
        "carrier_edges": len(carrier),
        "total_edges": len(edges),
        "degree_min": min(degree),
        "degree_max": max(degree),
        "connected": len(seen) == 900,
        "delta_support": len(delta_support),
        "canonical_edge_digest": CANONICAL_DIGEST,
        "sibling_edge_digest": sibling_digest,
        "distinct_from_canonical":
            sibling_digest != CANONICAL_DIGEST,
        "canonical_payload_read": False,
        "sibling_flat_target_read": False,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
