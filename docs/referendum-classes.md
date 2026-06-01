# Referendum Classes

Quantova gates decisions by impact. Routine decisions use a low-cost **standard
referendum**; supply, protocol, and security-critical decisions use **critical
referenda** with thresholds scaled to their impact; live theft or bridge
compromise is handled by a narrow **freeze / asset-recovery referendum**. There is
no admin shortcut around any of these paths.

All parameters below are the Quantova governance specification (Chapter 11).

## 1. Three categories of governance

| Category | Mechanism | Voter pool |
|---|---|---|
| Protocol improvements | QIP process with reference implementation | Open community / validator consensus |
| Treasury & ecosystem | On-chain referendum with QTOV-weighted voting | All QTOV holders |
| Critical network operations | High-bond on-chain referendum | High-stake QTOV holders |

Protocol improvements (QIPs) are drafted, discussed openly, implemented in
reference clients, and adopted through validator consensus — the social layer.
Token-weighted voting is reserved for specific on-chain decisions.

## 2. Standard referendum

For routine treasury and ecosystem decisions.

| Parameter | Value |
|---|---|
| Discussion period | 7 days minimum |
| Proposal submission | On-chain, requires a QTOV bond |
| Voting period | 7 days |
| Execution delay | 48 hours, time-locked |
| Passing threshold | Simple majority (>50%) |
| Quorum requirement | 4% of circulating QTOV |

## 3. Critical referenda

High-impact operations change the supply, the protocol itself, or a
security-critical parameter (minting QTOV, upgrading the runtime, or adjusting
safety parameters such as the validator minimum self-stake or slashing rates).
The native asset is bonded **and** locked for the governance cycle to raise the
referendum, and the larger the change, the larger the stake and supermajority
required.

### 3a. Minting referendum (new QTOV into circulation)

A moderate-cost referendum. It can only ever **lower** the hardcoded emission
schedule or release pre-allocated treasury QTOV; it cannot raise issuance above
the schedule.

| Parameter | Value |
|---|---|
| Proposal bond | 500,000 QTOV |
| Minimum proposer stake | 5,000,000 QTOV, locked for the governance cycle (~90 days) |
| Discussion period | 30 days minimum |
| Voting period | 14 days |
| Execution delay | 30 days |
| Passing threshold | 80% supermajority |
| Quorum requirement | 35% of circulating QTOV |

### 3b. Emergency protocol-upgrade referendum

The maximum-cost path, used to change the runtime itself — the only mechanism that
can alter consensus, slashing, or the cryptographic primitives. It carries the
highest bond and locked-stake requirement on the network.

| Parameter | Value |
|---|---|
| Proposal bond | 1,000,000 QTOV |
| Minimum proposer stake | 10,000,000 QTOV, locked for the governance cycle (~90 days) |
| Discussion period | 14 days (reducible to 48h for an actively exploited vulnerability) |
| Voting period | 14 days |
| Execution delay | 30 days (reducible under an active exploit) |
| Passing threshold | 80% supermajority |
| Quorum requirement | 40% of circulating QTOV |

## 4. Freeze & asset-recovery referendum

An active Layer-1 with cross-chain bridges needs a way to respond to live theft or
a bridge compromise without handing any party a unilateral capability. Quantova
provides this as a high-threshold referendum, not an operator power. The scope is
narrow and recorded on-chain: freeze assets that are demonstrably the proceeds of
theft or an exploit so they cannot be bridged out, return them through the same
process, and lift the freeze by a follow-up vote. **The chain keeps producing and
finalizing blocks throughout — a freeze targets specific assets, it does not stop
the network.**

| Parameter | Value |
|---|---|
| Proposal bond | 250,000 QTOV |
| Minimum proposer stake | 2,500,000 QTOV (high stake, short lock) |
| Stake lock | Held through the referendum + execution window only (~14–21 days), then released |
| Discussion period | Up to 21 days (reducible to 24h for an active, evidenced theft) |
| Voting period | 14 days (reducible to 24h under an active exploit) |
| Execution delay | 14 days (reducible to 0 for an evidenced, in-progress theft) |
| Passing threshold | 75% supermajority |
| Quorum requirement | 30% of circulating QTOV |

A freeze executes only through a bonded supermajority referendum with on-chain
evidence and a public record; no individual, validator, or Quantova Inc can invoke it alone. It applies to the narrowest set of assets that resolves the incident and
is reversible by the same process — an accountable safeguard, not a backdoor.

## 5. Security parameters are critical-class by design

Some parameters cannot be changed by a routine proposal because they are security
controls. The validator **minimum self-stake** ($50,000 USD-equivalent in QTOV) is a
Sybil-resistance measure; raising or lowering it requires a **critical referendum**
with a large bonded stake and a supermajority — the same class of vote used for
minting and runtime upgrades. This keeps a Sybil-resistance control from being
weakened cheaply or quietly.

---

*Source: Quantova governance specification §11.2–§11.5, §10.2 (validator minimum).*
