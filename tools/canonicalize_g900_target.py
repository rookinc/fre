#!/usr/bin/env python3
"""Independent canonicalizer for the committed flat G900 target."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "fixtures/g900/x_sigma_edges.csv"
TARGET_ID = "fre.g900.flattened_target.canonical.v0.1"
TARGET_RAW_SHA256 = "ea2679662f4322a9ea021fba1143c804ef73b1fae95f50c77ba76b7fe1092230"
REQUIRED_COLUMNS = [
    "u_vertex",
    "v_vertex",
    "u_slot",
    "u_local",
    "v_slot",
    "v_local",
    "kind",
]


def main():
    raw = TARGET.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TARGET_RAW_SHA256:
        raise RuntimeError("target raw hash mismatch")

    with TARGET.open("r", encoding="ascii", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise RuntimeError("target column mismatch")
        rows = list(reader)

    edges = set()
    vertices = set()
    kind_counts = {}

    for row in rows:
        u = int(row["u_vertex"])
        v = int(row["v_vertex"])
        us = int(row["u_slot"])
        ul = int(row["u_local"])
        vs = int(row["v_slot"])
        vl = int(row["v_local"])
        kind = row["kind"]

        if not (
            0 <= us < 15 and 0 <= vs < 15
            and 0 <= ul < 60 and 0 <= vl < 60
        ):
            raise RuntimeError("address outside declared range")
        if u != 60 * us + ul or v != 60 * vs + vl:
            raise RuntimeError("flat vertex address mismatch")
        if u == v:
            raise RuntimeError("loop in target")

        edge = (min(u, v), max(u, v))
        if edge in edges:
            raise RuntimeError("duplicate normalized target edge")
        edges.add(edge)
        vertices.update(edge)
        kind_counts[kind] = kind_counts.get(kind, 0) + 1

    if len(rows) != 3600 or len(edges) != 3600:
        raise RuntimeError("target edge cardinality mismatch")

    serialized = "".join(
        f"{u},{v}\n" for u, v in sorted(edges)
    ).encode("ascii")

    summary = {
        "target_id": TARGET_ID,
        "target_raw_sha256": TARGET_RAW_SHA256,
        "target_rows": len(rows),
        "normalized_edges": len(edges),
        "minimum_vertex": min(vertices),
        "maximum_vertex": max(vertices),
        "vertex_count": len(vertices),
        "kind_counts": dict(sorted(kind_counts.items())),
        "canonical_edge_digest":
            hashlib.sha256(serialized).hexdigest(),
        "generator_digest_read": False,
        "comparison_performed": False,
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
