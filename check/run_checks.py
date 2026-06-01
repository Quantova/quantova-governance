#!/usr/bin/env python3
"""Run the Quantova governance security back-test check (read-only).

Examples:
    python run_checks.py --rpc http://127.0.0.1:9944
    python run_checks.py --rpc http://127.0.0.1:9944 --json
    python run_checks.py --rpc http://127.0.0.1:9944 --fast

This tool is READ-ONLY: no signing, no transaction submission, no state changes.
It verifies the governance structure and that authorization is post-quantum.
"""

import argparse
import json
import sys

from gov_checks import checks
from gov_checks.client import RpcClient


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="governance-security-check",
        description="Read-only Quantova governance security & conformance check.",
    )
    p.add_argument("--rpc", required=True, help="Quantova JSON-RPC endpoint (http://host:9944)")
    p.add_argument("--interval", type=float, default=4.0,
                   help="seconds between finality samples (default: 4)")
    p.add_argument("--fast", action="store_true", help="skip timed finality sampling")
    p.add_argument("--json", action="store_true", help="emit JSON report")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    rpc = RpcClient(args.rpc)
    report = checks.run_all(rpc, interval=args.interval, fast=args.fast)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print("Quantova Governance Security & Conformance Check (read-only)")
        print(report.to_text())
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
