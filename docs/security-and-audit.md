# Governance Security & Audit Notes

This document is written for auditors and reviewers. It states the security
properties Quantova governance provides, and gives a concrete, read-only checklist
for validating them against a live chain. The repository also ships a runnable
**security back-test check** (see [§3](#3-running-the-security-back-test-check))
that automates the structural and post-quantum checks below.

## 1. Security properties

| Property | Mechanism | Where to verify |
|---|---|---|
| No unilateral control | All privileged (`Root`) execution flows only through a bonded, token-weighted referendum; there is no unilateral execution path | Referenda `CancelOrigin`/`KillOrigin = EnsureRoot`; governance-only enactment |
| Post-quantum authorization | Every proposal and vote is a signed extrinsic verified with Dilithium / Falcon / SPHINCS+ | `Signature = QSignature`; `impl Verify for QSignature` ([post-quantum-signing.md](post-quantum-signing.md)) |
| Spam resistance | Refundable QTOV bonds, forfeited to treasury if a proposal fails to engage | Bond tables ([participation-and-fees.md](participation-and-fees.md)) |
| Impact-scaled thresholds | Higher-impact classes require larger bonds, locked stake, supermajorities, and quorums | Class parameters ([referendum-classes.md](referendum-classes.md)) |
| Time-locked enactment | Approved calls are scheduled after an enactment delay, leaving a public reaction window | Referenda → Scheduler wiring; per-class enactment period |
| Sustained commitment | High-impact proposers lock a large QTOV stake for the governance cycle | Documented lock-ups (mint/upgrade ~90d; freeze short) |
| Accountable emergency response | Freeze / recovery is a bonded supermajority referendum with on-chain evidence, reversible by the same process | Freeze class parameters ([referendum-classes.md](referendum-classes.md)) |
| Validator Sybil resistance | Validator minimum self-stake is a security parameter changeable only by critical referendum | §10.2 / §11.4 |

## 2. Validation checklist (against a live node)

All checks below are **read-only** — query state and metadata; submit nothing.

**Pallet presence & wiring**
- [ ] Runtime metadata exposes `Referenda`, `ConvictionVoting`, `Preimage`, and
  `Scheduler` pallets.
- [ ] `Referenda::SubmitOrigin` is signed; `CancelOrigin` and `KillOrigin` are
  `Root` (reachable only through governance).
- [ ] `ConvictionVoting::Polls` points at `Referenda`; a vote-locking period is set.
- [ ] Approved referenda enact via the `Scheduler` after the enactment delay.

**Post-quantum signing**
- [ ] The chain's signature type is `QSignature` (post-quantum), not an
  ECDSA / sr25519 type. Confirm via the signed-extrinsic signature type in metadata.
- [ ] A vote extrinsic signed with each scheme (Dilithium, Falcon, SPHINCS+)
  verifies, and a tampered signature is rejected.
- [ ] The voting account equals the account derived from the signing public key.

**Referendum classes & parameters**
- [ ] Enumerate referendum tracks and compare each track's decision deposit,
  prepare / decision / confirm / enactment periods, and approval / support curves
  against the documented classes in [referendum-classes.md](referendum-classes.md).
- [ ] Confirm the enactment delay matches the documented execution delay per class.

**Bonds & locks**
- [ ] Confirm submission / decision deposits match the documented bond table.
- [ ] Confirm lock durations (mint / upgrade ~90 days; freeze short) are enforced.

## 3. Running the security back-test check

The repository ships a read-only checker under [`check/`](../check) that automates
the structural and post-quantum items above. It connects to a Quantova node over
JSON-RPC, reads only public chain state and metadata, and reports `PASS` / `WARN` /
`FAIL`. It performs no signing, submits no transactions, and changes nothing.

```bash
cd check
pip install -r requirements.txt          # just: requests
python run_checks.py --rpc http://127.0.0.1:9944
python run_checks.py --rpc http://127.0.0.1:9944 --json   # machine-readable, for CI
```

What it verifies (all read-only):

- **Connectivity & finality** — node reachable; finalized head advancing.
- **Governance pallets present** — `Referenda`, `ConvictionVoting`, `Preimage`,
  `Scheduler`, with their expected storage items and dispatchables.
- **Post-quantum signing present** — the `QSignature` type and the Dilithium /
  Falcon / SPHINCS+ schemes are exposed in the runtime metadata.
- **Governance-gated origins** — confirms referendum cancel / kill are `Root`-only
  and submission is signed.

It ships with an offline self-test (`python tests/test_offline.py`) that runs the
full battery against a mock node in both a healthy and a deliberately broken
scenario, proving the failure-detection paths.

## 4. What this repository is and is not

- **Is:** a documentation and reference repository describing Quantova's governance
  structure, plus a read-only security back-test check auditors can run.
- **Is not:** a security audit, a formal verification, or a guarantee. It contains
  no private keys, no secrets, and no code that performs any on-chain action.
  Auditors should independently verify every property in §1 against a live runtime
  using the checklist in §2 and the checker in §3.

---

*Sources: Quantova governance specification (Ch. 8–11) for policy; Quantova protocol
runtime for implementation. © 2026 Quantova Inc, BUSL-1.1.*
