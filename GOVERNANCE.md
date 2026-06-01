# Quantova Governance

How the Quantova network is governed: who can change it, through what process, at
what cost, and how every governance action is authorized by post-quantum
signatures.

This repository is a reference for token holders, validators, integrators, and
auditors. It explains the governance model in plain terms, documents the
participation bonds and lock-ups, and shows the on-chain code that implements it —
including the post-quantum signing path that secures every vote. It also ships a
read-only [security back-test check](docs/security-and-audit.md#3-running-the-security-back-test-check)
auditors can run against a live node.

## The model in one paragraph

Quantova is governed entirely on-chain. All privileged execution authority (the
`Root` origin) is reached only by passing a bonded, token-weighted **referendum** —
there is no unilateral path for any individual, including the founding team, to
change the network. Routine decisions (treasury spend, ecosystem grants) pass by
simple majority with a small bond; consequential decisions (minting QTOV,
upgrading the runtime, freezing stolen funds, changing security parameters) require
a large bonded and locked QTOV stake plus a supermajority. Voting power is
denominated in QTOV, and holders can lock QTOV for longer to gain a higher voting
multiplier. Every proposal and every vote is submitted as a signed transaction
whose signature is **post-quantum** (Dilithium, Falcon, or SPHINCS+).

## How governance works, step by step

1. **Author** — anyone may draft a proposal. Protocol-level changes (QIPs) are
   discussed openly and implemented in reference clients; on-chain decisions are
   prepared as a runtime call and stored as a **preimage**.
2. **Submit with a bond** — the proposer submits an on-chain referendum and posts a
   QTOV **bond**. The bond is returned if the proposal reaches the engagement
   threshold and **forfeited to the treasury** if it does not, so spam funds the
   network rather than costing nothing.
3. **Lock stake (for high-impact classes)** — minting, runtime upgrades, and freezes
   additionally require the proposer to **lock** a large QTOV stake for the
   governance cycle (the freeze path keeps the stake high but the lock short).
4. **Discuss** — a mandatory discussion period runs before voting, scaled to impact
   (longer for higher-impact classes).
5. **Vote** — QTOV holders vote. Voting power = QTOV × the holder's lock multiplier
   (see [participation-and-fees.md](docs/participation-and-fees.md)). Each vote is a
   post-quantum-signed extrinsic.
6. **Decide** — the referendum passes if it meets its **approval threshold** (simple
   majority for routine, 75–80% supermajority for consequential) and its **quorum**
   (4% routine, up to 40% for critical).
7. **Time-locked enactment** — a passed referendum does not execute immediately. An
   **execution delay** (48h for routine, up to 30 days for critical) elapses before
   the scheduler dispatches the call, leaving a public window to react.

## What governance controls

| Decision | Class | Authority |
|---|---|---|
| Treasury spend, ecosystem grants | Standard referendum | All QTOV holders, simple majority |
| Protocol parameter adjustments (QIPs) | Standard / QIP | Holders + validator consensus |
| Minting QTOV (lower emission / release treasury) | Critical referendum | High-stake holders, 80% supermajority |
| Runtime / protocol upgrades | Critical referendum | High-stake holders, 80% supermajority |
| Freeze / recover stolen or exploited funds | Freeze referendum | High-stake holders, 75% supermajority |
| Validator minimum self-stake, slashing rates | Critical referendum | High-stake holders, supermajority |

Full parameter tables are in
[docs/referendum-classes.md](docs/referendum-classes.md).

## Repository contents

| File | What it covers |
|---|---|
| [GOVERNANCE.md](GOVERNANCE.md) | This overview — the model and process |
| [docs/participation-and-fees.md](docs/participation-and-fees.md) | Bonds, lock-ups / vote-locking timelocks, conviction multipliers |
| [docs/referendum-classes.md](docs/referendum-classes.md) | Standard, critical (mint, upgrade), and freeze referendum parameters |
| [docs/post-quantum-signing.md](docs/post-quantum-signing.md) | How votes are post-quantum signed, with the real chain code |
| [docs/pallet-architecture.md](docs/pallet-architecture.md) | The OpenGov pallet stack that implements governance, with code |
| [docs/security-and-audit.md](docs/security-and-audit.md) | Security properties, a read-only validation checklist, and the security back-test check |

## Source

The parameter tables in this repository are the Quantova governance specification —
the bonds, lock-ups, and referendum classes that govern participation. The code
snippets are taken from the Quantova protocol runtime and show how the model is
implemented on-chain. The security back-test check in
[docs/security-and-audit.md](docs/security-and-audit.md) lets auditors verify the
structure against a live node.

## License

Licensed under the Business Source License 1.1 (BUSL-1.1), © 2026 Quantova Inc.
See [LICENSE](LICENSE) and [LICENSE-OVERVIEW.md](LICENSE-OVERVIEW.md).
