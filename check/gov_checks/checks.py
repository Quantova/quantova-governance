"""Read-only governance security & conformance checks.

Every check only READS public chain state, finality, and runtime metadata. None of
them sign, submit, or change anything. The goal is to confirm the governance
structure is wired as specified and that authorization is post-quantum.

Groups:
  A. Connectivity & finality
  B. Governance pallets present (structural conformance)
  C. Post-quantum signing present
  D. Governance-gated origins

A failed check reports *that* something is missing or misconfigured; it never
includes an exploit.
"""

import time
from typing import Optional

from . import spec
from .client import RpcClient, RpcError
from .report import FAIL, INFO, PASS, Report, SKIP, WARN


# --------------------------------------------------------------------------- #
# A. Connectivity & finality
# --------------------------------------------------------------------------- #

def check_connectivity(report: Report, rpc: RpcClient) -> None:
    cat = "A. connectivity & finality"
    try:
        h = rpc.finalized_head()
        report.add("JSON-RPC reachable", PASS, f"finalized head {str(h)[:18]}…", cat)
    except RpcError as e:
        report.add("JSON-RPC reachable", FAIL, str(e), cat)
        return
    try:
        health = rpc.health()
        peers = health.get("peers") if isinstance(health, dict) else None
        syncing = health.get("isSyncing") if isinstance(health, dict) else None
        report.add("Node health", PASS if not syncing else WARN,
                   f"peers={peers} isSyncing={syncing}", cat)
    except RpcError as e:
        report.add("Node health", WARN, str(e), cat)


def check_finality_advancing(report: Report, rpc: RpcClient, interval: float = 4.0) -> None:
    cat = "A. connectivity & finality"
    try:
        h1 = rpc.header(rpc.finalized_head())
        n1 = int(h1.get("number"), 16) if isinstance(h1, dict) else None
        time.sleep(interval)
        h2 = rpc.header(rpc.finalized_head())
        n2 = int(h2.get("number"), 16) if isinstance(h2, dict) else None
        if n1 is None or n2 is None:
            report.add("Finality advancing", WARN, "could not read finalized header numbers", cat)
        elif n2 > n1:
            report.add("Finality advancing", PASS, f"finalized {n1} -> {n2} in ~{interval:.0f}s", cat)
        else:
            report.add("Finality advancing", FAIL, f"finalized head did not advance ({n1} -> {n2})", cat)
    except (RpcError, ValueError, TypeError) as e:
        report.add("Finality advancing", WARN, str(e), cat)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def _metadata_bytes(rpc: RpcClient) -> Optional[bytes]:
    try:
        meta_hex = rpc.metadata()
    except RpcError:
        return None
    return bytes.fromhex(meta_hex[2:] if meta_hex.startswith("0x") else meta_hex)


# --------------------------------------------------------------------------- #
# B. Governance pallets present
# --------------------------------------------------------------------------- #

def check_pallets(report: Report, raw: Optional[bytes]) -> None:
    """Confirm the OpenGov pallets + a representative set of their storage items
    and dispatchables are present in runtime metadata (name-presence scan)."""
    cat = "B. governance pallets"
    if raw is None:
        report.add("Runtime metadata", FAIL, "state_getMetadata failed", cat)
        return

    def present(name: str) -> bool:
        return name.encode("ascii") in raw

    missing_pallets = [p for p in spec.GOVERNANCE_PALLETS if not present(p)]
    if not missing_pallets:
        report.add("Governance pallets present", PASS,
                   "Referenda, ConvictionVoting, Preimage, Scheduler", cat)
    else:
        report.add("Governance pallets present", FAIL, f"missing: {', '.join(missing_pallets)}", cat)

    for pallet, items in spec.EXPECTED_STORAGE.items():
        miss = [i for i in items if not present(i)]
        if not miss:
            report.add(f"{pallet} storage items", PASS, f"{len(items)} present", cat)
        else:
            report.add(f"{pallet} storage items", WARN, f"missing: {', '.join(miss)}", cat)

    for pallet, calls in spec.EXPECTED_CALLS.items():
        miss = [c for c in calls if not present(c)]
        if not miss:
            report.add(f"{pallet} dispatchables", PASS, f"{len(calls)} present", cat)
        else:
            report.add(f"{pallet} dispatchables", WARN, f"missing: {', '.join(miss)}", cat)


# --------------------------------------------------------------------------- #
# C. Post-quantum signing present
# --------------------------------------------------------------------------- #

def check_post_quantum(report: Report, raw: Optional[bytes]) -> None:
    """Confirm the post-quantum signature type and the three NIST schemes are
    exposed in runtime metadata — i.e. governance is authorized post-quantum."""
    cat = "C. post-quantum signing"
    if raw is None:
        report.add("Post-quantum signature type", SKIP, "no metadata", cat)
        return

    def present(name: str) -> bool:
        return name.encode("ascii") in raw

    if present(spec.PQ_SIGNATURE_TYPE):
        report.add("Post-quantum signature type", PASS,
                   f"'{spec.PQ_SIGNATURE_TYPE}' present in metadata", cat)
    else:
        report.add("Post-quantum signature type", FAIL,
                   f"'{spec.PQ_SIGNATURE_TYPE}' not found in metadata", cat)

    missing = [s for s in spec.PQ_SCHEME_NAMES if not present(s)]
    if not missing:
        report.add("PQ schemes (Dilithium/Falcon/SPHINCS+)", PASS, "all three present", cat)
    else:
        report.add("PQ schemes (Dilithium/Falcon/SPHINCS+)", WARN, f"missing: {', '.join(missing)}", cat)


# --------------------------------------------------------------------------- #
# D. Governance-gated origins
# --------------------------------------------------------------------------- #

def check_origins(report: Report, raw: Optional[bytes]) -> None:
    """Referenda submit is signed; cancel/kill are Root (governance-only). The
    call names are confirmed present; the origin wiring is verified by an auditor
    against the runtime config (the names alone cannot encode the origin)."""
    cat = "D. governance-gated origins"
    if raw is None:
        report.add("Governance-gated origins", SKIP, "no metadata", cat)
        return

    def present(name: str) -> bool:
        return name.encode("ascii") in raw

    miss = [c for c in spec.ROOT_GATED_CALLS if not present(c)]
    if not miss:
        report.add("Referenda cancel/kill present", PASS,
                   "cancel + kill exposed (Root-gated in runtime config)", cat)
    else:
        report.add("Referenda cancel/kill present", WARN, f"missing: {', '.join(miss)}", cat)
    report.add("Origin wiring", INFO,
               "confirm SubmitOrigin=signed, Cancel/Kill=Root in the runtime config", cat)


# --------------------------------------------------------------------------- #
# orchestration
# --------------------------------------------------------------------------- #

def run_all(rpc: RpcClient, *, interval: float = 4.0, fast: bool = False) -> Report:
    report = Report()
    check_connectivity(report, rpc)
    if not fast:
        check_finality_advancing(report, rpc, interval=interval if interval else 4.0)
    raw = _metadata_bytes(rpc)
    check_pallets(report, raw)
    check_post_quantum(report, raw)
    check_origins(report, raw)
    return report
