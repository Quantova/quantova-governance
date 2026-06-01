"""Offline self-test for the governance security back-test check.

Runs the full battery with no network using a mock JSON-RPC session, in two
scenarios:

* a HEALTHY runtime (all governance pallets + PQ signing present) -> expect no FAILs
* a BROKEN runtime (a governance pallet missing, PQ signature type absent,
   finality stalled) -> expect the checks to FAIL exactly those items

Run:  python3 tests/test_offline.py
"""

import sys
import time

from gov_checks import checks, spec
from gov_checks.client import RpcClient
from gov_checks.report import FAIL, PASS


class Resp:
    def __init__(self, data):
        self._d = data

    def json(self):
        return self._d


def make_metadata(healthy=True) -> str:
    """Fake metadata blob containing the ASCII names the scanner looks for."""
    names = list(spec.GOVERNANCE_PALLETS)
    for items in spec.EXPECTED_STORAGE.values():
        names += items
    for calls in spec.EXPECTED_CALLS.values():
        names += calls
    names += [spec.PQ_SIGNATURE_TYPE] + list(spec.PQ_SCHEME_NAMES)
    if not healthy:
        names.remove("ConvictionVoting")       # simulate a missing governance pallet
        names.remove(spec.PQ_SIGNATURE_TYPE)    # simulate PQ signature type absent
    blob = ("META" + "|".join(names) + "META").encode("ascii")
    return "0x" + blob.hex()


class MockNode:
    def __init__(self, healthy=True):
        self.healthy = healthy
        self.fin_number = 2000

    def rpc(self, method, params):
        if method == "chain_getFinalizedHead":
            return "0x" + "fe" * 32
        if method == "system_health":
            return {"peers": 8, "isSyncing": False}
        if method == "state_getMetadata":
            return make_metadata(self.healthy)
        if method == "chain_getHeader":
            if self.healthy:
                self.fin_number += 1           # advances -> PASS
            return {"number": hex(self.fin_number), "parentHash": "0x" + "00" * 32}
        if method == "state_getRuntimeVersion":
            return {"specName": "quantova", "specVersion": 1}
        raise AssertionError("unexpected rpc method: " + method)


class RpcSession:
    def __init__(self, node):
        self.node = node

    def post(self, url, json=None, headers=None, timeout=None):
        return Resp({"jsonrpc": "2.0", "id": json["id"],
                     "result": self.node.rpc(json["method"], json.get("params", []))})


def run_scenario(healthy: bool):
    rpc = RpcClient("http://node", session=RpcSession(MockNode(healthy=healthy)))
    return checks.run_all(rpc, interval=0.0, fast=False)


def main():
    _orig = time.sleep
    time.sleep = lambda *a, **k: None
    try:
        print("=" * 60)
        print("  Governance back-test check — OFFLINE self-test")
        print("=" * 60)

        healthy = run_scenario(True)
        c1 = healthy.counts()
        print("\nScenario 1: HEALTHY runtime")
        print(healthy.to_text())
        assert c1[FAIL] == 0, f"healthy should have 0 FAILs, got {c1[FAIL]}"
        assert c1[PASS] >= 8, f"expected many PASS, got {c1[PASS]}"

        broken = run_scenario(False)
        c2 = broken.counts()
        print("\n\nScenario 2: BROKEN runtime (missing pallet, no PQ type, stalled finality)")
        print(broken.to_text())
        fails = [r.check for r in broken.results if r.status == FAIL]
        assert c2[FAIL] >= 1, "broken should report FAILs"
        assert any("Governance pallets" in f for f in fails), "should detect missing pallet"
        assert any("Post-quantum signature type" in f for f in fails), "should detect missing PQ type"
        assert any("Finality advancing" in f for f in fails), "should detect stalled finality"

        print("\n" + "=" * 60)
        print(f"  SELF-TEST PASSED — healthy: {c1[PASS]} pass / 0 fail; "
              f"broken correctly flagged {c2[FAIL]} failures")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print("\nSELF-TEST FAILED:", e)
        return 1
    finally:
        time.sleep = _orig


if __name__ == "__main__":
    sys.exit(main())
