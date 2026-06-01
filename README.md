# Quantova Governance

Reference documentation for the Quantova on-chain governance structure — how
decisions are made, what they cost to participate in, and how every vote is secured
by post-quantum cryptography. Written for token holders, validators, integrators,
and auditors.

## Start here

- **[GOVERNANCE.md](GOVERNANCE.md)** — the model and the end-to-end process (read
  this first).

## Documents

| Document | What it covers |
|---|---|
| [GOVERNANCE.md](GOVERNANCE.md) | How governance works: the no-unilateral-control model, the three categories, and the full proposal → vote → time-locked enactment flow |
| [docs/participation-and-fees.md](docs/participation-and-fees.md) | Participation bonds, vote-locking timelocks, conviction multipliers, and where forfeited QTOV goes |
| [docs/referendum-classes.md](docs/referendum-classes.md) | Standard, critical (mint, emergency upgrade), and freeze / asset-recovery referendum parameters |
| [docs/post-quantum-signing.md](docs/post-quantum-signing.md) | How governance and votes are post-quantum signed (Dilithium / Falcon / SPHINCS+), with the real chain code |
| [docs/pallet-architecture.md](docs/pallet-architecture.md) | The OpenGov pallet stack (referenda, conviction-voting, preimage, scheduler) that implements governance, with runtime code |
| [docs/security-and-audit.md](docs/security-and-audit.md) | Security properties, a read-only validation checklist, and the runnable security back-test check |

## At a glance

- **No unilateral control.** All privileged (`Root`) authority is reached only
  through bonded, token-weighted referenda; cancel and kill are governance-only.
- **Post-quantum from the signature layer up.** The chain's signature type is
  `QSignature` (Dilithium / Falcon / SPHINCS+); there is no ECDSA path into
  governance.
- **Impact-scaled cost.** Routine votes need a small bond, a simple majority, and a
  4% quorum; consequential votes need large bonded + locked stake, a 75–80%
  supermajority, and a 30–40% quorum.
- **Vote-locking → weight.** Vote liquid for 1.0×, or lock QTOV up to 24 months for
  up to 2.5× voting power.
- **Time-locked enactment.** Approved proposals execute only after a delay (48h
  routine, up to 30 days critical).

## For auditors

[docs/security-and-audit.md](docs/security-and-audit.md) lists the security
properties, a read-only checklist to validate them against a live node, and a
runnable security back-test check (under [check/](check)) that automates the
structural and post-quantum verification.

This repository contains documentation and code excerpts only — no private keys, no
secrets, and nothing that performs any on-chain action.

## License

Licensed under the Business Source License 1.1 (BUSL-1.1), © 2026 Quantova Inc.
See [LICENSE](LICENSE) and [LICENSE-OVERVIEW.md](LICENSE-OVERVIEW.md).
