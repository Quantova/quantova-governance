# Participation, Bonds & Lock-Ups

This document collects everything it costs to participate in Quantova governance:
the QTOV bonds to raise a proposal, the lock-ups that back high-impact proposals,
the vote-locking timelocks that set voting weight, and where forfeited QTOV goes.

All figures are transcribed from the Quantova developer documentation (Chapters 8.5,
9.7, and 11) and form the Quantova governance participation specification.

## 1. There is no governance "fee" — only bonds

Governance carries **no transaction fee beyond the standard weight fee**. Instead,
raising a proposal requires a refundable **QTOV bond**:

- The bond is **returned** if the proposal reaches the engagement threshold.
- The bond is **forfeited to the Quantova treasury** if it does not.

This makes spam and frivolous proposals fund the treasury rather than cost
nothing, and it scales the price of participation with the impact of the action.

## 2. Vote-locking timelocks → voting multiplier

Voting power is denominated in QTOV. A holder can vote with liquid QTOV, or **lock**
QTOV for a chosen duration to receive a higher voting multiplier. Locking affects
voting weight only; the asset is always QTOV.

| Lock duration | Voting multiplier |
|---|---|
| Liquid QTOV (no lock) | 1.0× |
| 1-month lock | 1.0× |
| 12-month lock | 1.5× |
| 24-month lock | 2.5× |

Locked QTOV is also the basis for referendum quorums. Higher-impact referenda
require proposers to lock a larger QTOV stake for the governance cycle, so the
holders who can move the network are those committing the most stake.

## 3. Proposal bonds & locked stake by action

To raise an on-chain referendum a proposer bonds QTOV; high-impact classes also
require a locked stake held for the governance cycle. Forfeited QTOV is routed in
full to the Quantova treasury.

| Action | QTOV at stake to propose | Voter pool |
|---|---|---|
| Ecosystem grant proposal | 1,000 QTOV bond | QTOV holders |
| Parameter adjustment (QIP) | 10,000 QTOV bond | QTOV holders / validators |
| Treasury action (under $500K equiv.) | 5,000 QTOV bond | QTOV holders |
| Treasury action (over $500K equiv.) | 25,000 QTOV bond | QTOV holders |
| Mint QTOV (lower emission / release treasury) | 500,000 QTOV bond + 5,000,000 QTOV locked ~90 days | QTOV holders |
| Freeze / recover stolen assets | 250,000 QTOV bond + 2,500,000 QTOV locked (short) | High-stake QTOV holders |
| Emergency runtime upgrade (major change) | 1,000,000 QTOV bond + 10,000,000 QTOV locked ~90 days | High-stake QTOV holders |

## 4. How the locks differ

The lock-up profile is deliberately different across classes:

- **Mint and emergency-upgrade** paths lock the proposer's stake for the full
  governance cycle (**~90 days**), because these are deliberate, high-impact changes
  that should require sustained commitment.
- **Freeze / asset-recovery** keeps the stake **high but the lock short** — held only
  through the referendum and a brief execution window (**~14–21 days**), then
  released — so urgent asset recovery is costly to abuse yet does not tie up large
  stake for long.

## 5. Thresholds & quorums at a glance

| Referendum type | Approval threshold | Quorum (circulating QTOV) |
|---|---|---|
| Standard (treasury / ecosystem) | Simple majority (>50%) | 4% |
| Critical — Mint | 80% supermajority | 35% |
| Critical — Emergency runtime upgrade | 80% supermajority | 40% |
| Freeze / Asset recovery | 75% supermajority | 30% |

## 6. Where forfeited QTOV goes

Every privileged action puts QTOV at stake, and QTOV forfeited by spammers, failed
proposers, or slashed validators is routed **in full to the Quantova treasury**. The
network does not subsidize spam or bad actors — it bills them, and the proceeds
accrue to the treasury.

---

*Source: Quantova governance specification §8.5 (Governance Bonds), §9.7 (QTOV
Voting Weight & Locking), §11.3–§11.6 (Referenda, Bonds & Anti-Spam).*
