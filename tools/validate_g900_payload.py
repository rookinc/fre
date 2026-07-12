#!/usr/bin/env python3
from pathlib import Path
from collections import deque
import csv
import hashlib
import json
import subprocess
import traceback

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures/g900"
OUT = ROOT / "artifacts/json/fre_g900_structural_audit_001.json"
REPORT = Path.home() / "tmp/validate_fre_g900_payload_001.out"

LOCKS = {
    "contracts/fre_g900_recursive_host_v0.1.json":
        "8b8baa98a8d0252f7433f800a5c118c995dee7e078c55be5db787cade1b0d83c",
    "artifacts/json/fre_g900_payload_provenance_001.json":
        "c13bd8b4fc4901b0eb618b4918e77281a01dae1ba0f13ba5adbd9cc8170ce052",
    "fixtures/g900/carrier_signing_table.csv":
        "9b3cf812cc0f6d7b065666c81fa6d16fd3e3b8a98955c264709337c7f3e7efb7",
    "fixtures/g900/g15_slot_edges.csv":
        "7b94834d507cf2995ec6faf73e2e227a685d831894aa98f2647556d8b922b8f6",
    "fixtures/g900/g60_local_edges.csv":
        "c700a185fab6a5f434da09b7acb716b96c76170774bee946af8ea907e4fe7f9f",
    "fixtures/g900/x_sigma_edges.csv":
        "ea2679662f4322a9ea021fba1143c804ef73b1fae95f50c77ba76b7fe1092230",
    "fixtures/g900/sibling_candidate_signing_table.csv":
        "8ad921c2af2f48e220e6c1c8a3a72aaecc64f56791bbfbd15b66f2211af11eba",
    "fixtures/g900/sibling_signing_delta.csv":
        "e75263b7e4de2b9c491b36b81e36674131c5f658842976b75da8e3303e146a50",
    "fixtures/g900/sibling_x_sigma_edges.csv":
        "13dbc8023eee15f8367d9d3309d60f2c447ac24c8ae5c43c71994705a562b425",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(name):
    with (FIX / name).open(newline="") as handle:
        return list(csv.DictReader(handle))

def edge(a, b):
    a, b = int(a), int(b)
    if a == b:
        raise RuntimeError("loop encountered")
    return (a, b) if a < b else (b, a)

def adjacency(edges, count):
    adj = [set() for _ in range(count)]
    for a, b in edges:
        if not (0 <= a < count and 0 <= b < count):
            raise RuntimeError("vertex outside declared range")
        adj[a].add(b)
        adj[b].add(a)
    return adj

def distances(adj, start):
    dist = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def shell_vector(adj, start):
    dist = distances(adj, start)
    if -1 in dist:
        raise RuntimeError("graph is disconnected")
    return [dist.count(i) for i in range(max(dist) + 1)]

def isomorphic(a, b):
    if len(a) != len(b):
        return False
    mapping = {}
    used = set()

    def search():
        if len(mapping) == len(a):
            return True

        unmapped = [u for u in range(len(a)) if u not in mapping]
        u = max(
            unmapped,
            key=lambda x: sum(n in mapping for n in a[x])
        )

        for v in range(len(b)):
            if v in used or len(a[u]) != len(b[v]):
                continue
            if any(
                ((x in a[u]) != (mapping[x] in b[v]))
                for x in mapping
            ):
                continue

            mapping[u] = v
            used.add(v)
            if search():
                return True
            used.remove(v)
            del mapping[u]
        return False

    return search()

def petersen_line_graph():
    p_edges = set()
    for i in range(5):
        p_edges.add(edge(i, (i + 1) % 5))
        p_edges.add(edge(i, i + 5))
        p_edges.add(edge(i + 5, 5 + ((i + 2) % 5)))

    p_edges = sorted(p_edges)
    line_edges = set()
    for i in range(len(p_edges)):
        for j in range(i + 1, len(p_edges)):
            if set(p_edges[i]) & set(p_edges[j]):
                line_edges.add((i, j))
    return adjacency(line_edges, 15)

def is_coboundary(graph_edges, values):
    adj = {}
    for a, b in graph_edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    phi = {}
    for start in adj:
        if start in phi:
            continue
        phi[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                expected = phi[u] ^ values[edge(u, v)]
                if v in phi and phi[v] != expected:
                    return False
                if v not in phi:
                    phi[v] = expected
                    queue.append(v)
    return True

try:
    for rel, expected in LOCKS.items():
        path = ROOT / rel
        if not path.is_file() or sha(path) != expected:
            raise RuntimeError("hash lock failed: " + rel)

    g15_rows = rows("g15_slot_edges.csv")
    g15 = {edge(r["slot_u"], r["slot_v"]) for r in g15_rows}
    if len(g15_rows) != 30 or len(g15) != 30:
        raise RuntimeError("G15 edge count or uniqueness failed")

    a15 = adjacency(g15, 15)
    if {len(x) for x in a15} != {4}:
        raise RuntimeError("G15 degree failed")
    if {tuple(shell_vector(a15, i)) for i in range(15)} != {
        (1, 4, 8, 2)
    }:
        raise RuntimeError("G15 shell structure failed")
    if not isomorphic(a15, petersen_line_graph()):
        raise RuntimeError("G15 is not isomorphic to L(Petersen)")

    g60_rows = rows("g60_local_edges.csv")
    g60 = {edge(r["local_u"], r["local_v"]) for r in g60_rows}
    if len(g60_rows) != 120 or len(g60) != 120:
        raise RuntimeError("G60 edge count or uniqueness failed")

    a60 = adjacency(g60, 60)
    if {len(x) for x in a60} != {4}:
        raise RuntimeError("G60 degree failed")
    if {tuple(shell_vector(a60, i)) for i in range(60)} != {
        (1, 4, 8, 16, 24, 6, 1)
    }:
        raise RuntimeError("G60 shell structure failed")

    sign_rows = rows("carrier_signing_table.csv")
    sigma = {}
    for r in sign_rows:
        e = edge(r["slot_u"], r["slot_v"])
        value = int(r["sign"])
        if e not in g15 or value not in (0, 1):
            raise RuntimeError("canonical signing failed")
        if int(r["external_edge_count"]) != 60:
            raise RuntimeError("carrier multiplicity failed")
        if value == 1 and "half_flip" not in r["carrier_law"]:
            raise RuntimeError("half-flip carrier law failed")
        if value == 0 and "identity" not in r["carrier_law"]:
            raise RuntimeError("identity carrier law failed")
        sigma[e] = value

    if len(sigma) != 30 or is_coboundary(g15, sigma):
        raise RuntimeError("canonical cocycle nontriviality failed")

    internal = {
        edge(i * 60 + a, i * 60 + b)
        for i in range(15)
        for a, b in g60
    }
    carrier = {
        edge(
            i * 60 + a,
            j * 60 + (a if sigma[edge(i, j)] == 0 else (a + 30) % 60)
        )
        for i, j in g15
        for a in range(60)
    }
    expected_g900 = internal | carrier

    if (
        len(internal) != 1800
        or len(carrier) != 1800
        or len(expected_g900) != 3600
    ):
        raise RuntimeError("constructed G900 count failed")

    payload_rows = rows("x_sigma_edges.csv")
    payload_edges = set()
    kinds = {"internal": 0, "carrier": 0}
    for r in payload_rows:
        u = int(r["u_vertex"])
        v = int(r["v_vertex"])
        us, ul = int(r["u_slot"]), int(r["u_local"])
        vs, vl = int(r["v_slot"]), int(r["v_local"])
        if u != us * 60 + ul or v != vs * 60 + vl:
            raise RuntimeError("G900 address law failed")
        payload_edges.add(edge(u, v))
        key = "internal" if r["kind"].startswith("internal") else "carrier"
        kinds[key] += 1

    if (
        len(payload_rows) != 3600
        or payload_edges != expected_g900
        or kinds != {"internal": 1800, "carrier": 1800}
    ):
        raise RuntimeError("canonical G900 edge payload failed")

    a900 = adjacency(payload_edges, 900)
    if {len(x) for x in a900} != {8}:
        raise RuntimeError("G900 degree failed")
    if -1 in distances(a900, 0):
        raise RuntimeError("G900 connectedness failed")

    sibling_rows = rows("sibling_candidate_signing_table.csv")
    sibling = {
        edge(r["slot_a"], r["slot_b"]): int(r["sibling_sign"])
        for r in sibling_rows
    }
    delta_rows = rows("sibling_signing_delta.csv")
    delta = {
        edge(r["slot_a"], r["slot_b"]): int(r["delta"])
        for r in delta_rows
    }

    if set(sibling) != g15 or set(delta) != g15:
        raise RuntimeError("sibling signing domain failed")
    if any(delta[e] != (sigma[e] ^ sibling[e]) for e in g15):
        raise RuntimeError("sibling delta equation failed")

    delta_support = sum(delta.values())
    if delta_support == 0 or is_coboundary(g15, delta):
        raise RuntimeError("sibling switching-class control failed")

    sibling_carrier = {
        edge(
            i * 60 + a,
            j * 60 + (
                a if sibling[edge(i, j)] == 0 else (a + 30) % 60
            )
        )
        for i, j in g15
        for a in range(60)
    }
    expected_sibling = internal | sibling_carrier

    sibling_payload = {
        edge(
            int(r["slot_a"]) * 60 + int(r["local_a"]),
            int(r["slot_b"]) * 60 + int(r["local_b"])
        )
        for r in rows("sibling_x_sigma_edges.csv")
    }

    if (
        len(expected_sibling) != 3600
        or sibling_payload != expected_sibling
        or sibling_payload == payload_edges
    ):
        raise RuntimeError("sibling graph negative control failed")

    checks = {
        "payload_hashes_locked": True,
        "G15_is_L_Petersen": True,
        "G15_vertices_15": len(a15) == 15,
        "G15_edges_30": len(g15) == 30,
        "G15_degree_four": True,
        "G60_vertices_60": len(a60) == 60,
        "G60_edges_120": len(g60) == 120,
        "G60_degree_four": True,
        "G60_shell_vector_exact": True,
        "canonical_cocycle_nontrivial": True,
        "half_flip_fixed_point_free_involution": all(
            (a + 30) % 60 != a
            and ((a + 30) % 60 + 30) % 60 == a
            for a in range(60)
        ),
        "G900_vertices_900": len(a900) == 900,
        "G900_edges_3600": len(payload_edges) == 3600,
        "G900_degree_eight": True,
        "G900_connected": True,
        "canonical_edge_law_exact": True,
        "sibling_control_distinct": True,
        "sibling_switching_class_distinct": True,
        "recursive_host_admitted": False,
        "independent_bridge_present": False,
    }

    if not all(v for k, v in checks.items() if k not in {
        "recursive_host_admitted", "independent_bridge_present"
    }):
        raise RuntimeError("structural checks failed")

    artifact = {
        "artifact_id": "fre.g900.structural_audit.001",
        "audit_pass": True,
        "verdict":
            "signed_half_flip_G900_payload_structurally_validated_not_recursively_admitted",
        "contract_id": "fre.g900.recursive_host.v0.1",
        "contract_sha256": LOCKS[
            "contracts/fre_g900_recursive_host_v0.1.json"
        ],
        "provenance_sha256": LOCKS[
            "artifacts/json/fre_g900_payload_provenance_001.json"
        ],
        "graphs": {
            "G15": {
                "vertices": 15,
                "edges": 30,
                "degree": 4,
                "graph_class": "L(Petersen)",
                "shell_vector": [1, 4, 8, 2]
            },
            "G60": {
                "vertices": 60,
                "edges": 120,
                "degree": 4,
                "diameter": 6,
                "shell_vector": [1, 4, 8, 16, 24, 6, 1]
            },
            "G900": {
                "vertices": 900,
                "edges": 3600,
                "degree": 8,
                "connected": True,
                "internal_edges": 1800,
                "carrier_edges": 1800
            }
        },
        "signing": {
            "zero_edges": sum(v == 0 for v in sigma.values()),
            "one_edges": sum(v == 1 for v in sigma.values()),
            "nontrivial_cocycle": True,
            "sibling_delta_support": delta_support,
            "sibling_switching_class_distinct": True
        },
        "checks": checks,
        "boundary": {
            "structural_graph_identity_validated": True,
            "recursive_host_theorem_validated": False,
            "independent_bridge_present": False,
            "G900_execution_admitted": False,
            "G900_receipt_emitted": False,
            "observational_closure": False,
            "external_truth_claim": False
        }
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    git_status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.rstrip()

    body = f"""== project ==
{ROOT}

== structural validator ==
tools/validate_g900_payload.py: created
sha256: {sha(Path(__file__))}

== structural audit ==
artifacts/json/fre_g900_structural_audit_001.json
artifact_id: {artifact["artifact_id"]}
verdict: {artifact["verdict"]}
sha256: {sha(OUT)}

== canonical graphs ==
G15: vertices=15 edges=30 degree=4 class=L(Petersen)
G60: vertices=60 edges=120 degree=4 diameter=6
G900: vertices=900 edges=3600 degree=8 connected=True

== edge partition ==
internal_G60_fiber_edges: 1800
signed_G15_carrier_edges: 1800

== signing ==
zero_edges: {artifact["signing"]["zero_edges"]}
one_edges: {artifact["signing"]["one_edges"]}
canonical_cocycle_nontrivial: True
sibling_delta_support: {delta_support}
sibling_switching_class_distinct: True

== checks ==
audit_pass: True
payload_hashes_locked: True
canonical_edge_law_exact: True
half_flip_involution: True
negative_control_distinct: True
recursive_host_admitted: False
independent_bridge_present: False

== git status ==
{git_status}

== boundary ==
The 900-state signed half-flip carrier is structurally validated.
The sibling signing passed as a distinct negative control.
No recursive-host theorem is admitted.
No independent bridge is present.
No transport cycle executed.
No G900 receipt emitted.
No build.
No crypto.
No commit.
No push.
No observational closure.

next: add the fail-closed G900 recursive-host receipt schema
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
