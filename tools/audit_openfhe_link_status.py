from pathlib import Path
import subprocess
import hashlib
import platform
import json
import re
import sys

HOME = Path.home()
ROOT = Path(__file__).resolve().parents[1]
ARCH = platform.machine() or "unknown"
PREFIX = (
    HOME
    / f"dev/cori/toolchains/openfhe-1.5.1-termux-{ARCH}"
)
BUILD = ROOT / "build-openfhe-link"

PROFILE = (
    ROOT
    / "artifacts/json/fre_openfhe_executed_profile_provenance_001.json"
)
DURABLE = (
    ROOT
    / "artifacts/json/fre_openfhe_durable_prefix_001.json"
)
OUT = (
    ROOT
    / "artifacts/json/fre_openfhe_link_status_audit_001.json"
)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd):
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True
    )
    text = (p.stdout + p.stderr).rstrip()
    if p.returncode != 0:
        raise RuntimeError(
            f"command failed rc={p.returncode}: {' '.join(cmd)}\n{text[:2200]}"
        )
    return text

def main():
    required = [
        PROFILE,
        DURABLE,
        ROOT / "CMakeLists.txt",
        ROOT / "include/fre/openfhe_backend_status.hpp",
        ROOT / "src/backends/openfhe/openfhe_backend_status.cpp",
        ROOT / "src/cli/fre_openfhe_status.cpp",
    ]

    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("missing required files: " + ", ".join(missing))
    if not PREFIX.is_dir():
        raise RuntimeError(f"durable prefix missing: {PREFIX}")

    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    durable = json.loads(DURABLE.read_text(encoding="utf-8"))

    run([
        "cmake", "-S", ".", "-B", str(BUILD),
        "-DBUILD_TESTING=ON",
        "-DFRE_ENABLE_OPENFHE=ON",
        f"-DFRE_OPENFHE_PREFIX={PREFIX}"
    ])
    run(["cmake", "--build", str(BUILD)])
    ctest = run([
        "ctest", "--test-dir", str(BUILD), "--output-on-failure"
    ])

    status_text = run([str(BUILD / "fre_openfhe_status")])
    status = json.loads(status_text)

    dynamic = run([
        "readelf", "-d", str(BUILD / "fre_openfhe_status")
    ])

    dependencies = []
    for row in dynamic.splitlines():
        if "(NEEDED)" not in row:
            continue
        match = re.search(r"\[([^]]+)\]", row)
        if match:
            dependencies.append(match.group(1))

    checks = {
        "five_tests_passed":
            "100% tests passed" in ctest
            and "out of 5" in ctest,
        "backend_available":
            status["available"] is True,
        "backend_linked":
            status["linked"] is True,
        "profile_pinned":
            status["profile_pinned"] is True,
        "profile_not_admitted":
            status["profile_admitted"] is False,
        "crypto_not_allowed":
            status["crypto_allowed"] is False,
        "boundary_link_only":
            status["boundary"]
            == "link_only_profile_pinned_no_crypto",
        "durable_prefix_exact":
            status["install_prefix"] == str(PREFIX),
        "pke_dependency_present":
            "libOPENFHEpke.so.1" in dependencies,
        "binfhe_dependency_present":
            "libOPENFHEbinfhe.so.1" in dependencies,
        "core_dependency_present":
            "libOPENFHEcore.so.1" in dependencies,
        "durable_copy_ready":
            durable["copy_ready"] is True,
        "source_profile_not_admitted":
            profile["boundary"]["profile_admitted_to_fre"] is False
    }

    audit_pass = all(checks.values())

    artifact = {
        "artifact_id": "fre.openfhe.link_status_audit.001",
        "verdict": (
            "fail_closed_openfhe_link_target_verified_no_crypto"
            if audit_pass
            else "openfhe_link_target_audit_failed"
        ),
        "audit_pass": audit_pass,
        "backend_status": status,
        "dynamic_dependencies": dependencies,
        "test_count": 5,
        "profile_binding": {
            "artifact_id": profile["artifact_id"],
            "artifact_sha256": sha256(PROFILE),
            "profile_id":
                profile["selected_profile"]["profile_id"],
            "profile_admitted": False
        },
        "durable_prefix_binding": {
            "artifact_id": durable["artifact_id"],
            "artifact_sha256": sha256(DURABLE),
            "prefix": str(PREFIX),
            "copy_ready": durable["copy_ready"]
        },
        "source_hashes": {
            "cmake_sha256":
                sha256(ROOT / "CMakeLists.txt"),
            "status_header_sha256":
                sha256(
                    ROOT / "include/fre/openfhe_backend_status.hpp"
                ),
            "status_source_sha256":
                sha256(
                    ROOT
                    / "src/backends/openfhe/"
                    "openfhe_backend_status.cpp"
                ),
            "status_cli_sha256":
                sha256(ROOT / "src/cli/fre_openfhe_status.cpp")
        },
        "checks": checks,
        "boundary": {
            "link_target_only": True,
            "backend_available": True,
            "backend_linked": True,
            "profile_pinned": True,
            "profile_admitted": False,
            "crypto_allowed": False,
            "crypto_context_constructed": False,
            "key_generation_performed": False,
            "encryption_performed": False,
            "evaluation_performed": False,
            "decryption_performed": False,
            "fre_receipt_emitted": False,
            "receipt_congruence_established": False,
            "observational_closure": False,
            "production_security_claim": False,
            "physical_claim": False
        }
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    print(json.dumps({
        "artifact_id": artifact["artifact_id"],
        "audit_pass": audit_pass,
        "verdict": artifact["verdict"],
        "test_count": artifact["test_count"],
        "dynamic_dependencies": dependencies
    }, sort_keys=True))

    return 0 if audit_pass else 1

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "audit_pass": False,
            "error": f"{type(exc).__name__}: {exc}"
        }), file=sys.stderr)
        raise SystemExit(2)
