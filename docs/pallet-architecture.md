# Pallet Architecture

Quantova governance is **a set of runtime pallets, not a separate layer**. It uses
the standard Substrate OpenGov stack — referenda, conviction voting, preimages, and
the scheduler — wired together in the runtime. This document shows the pallet
wiring so auditors can map the documented policy to the code that enforces it.

## 1. The governance pallet stack

From the runtime's `construct_runtime!` (pallet indices shown):

| Pallet | Index | Role |
|---|---|---|
| `pallet_preimage` | 27 | Stores the call bytes a referendum will execute (the proposal preimage) |
| `pallet_scheduler` | 28 | Dispatches an approved call after its time-locked enactment delay |
| `pallet_referenda` | 29 | The referendum lifecycle: submission, decision, approval / support tallying |
| `pallet_conviction_voting` | 30 | Token-weighted voting with lock-based conviction multipliers |

These four compose the governance flow: a **preimage** holds the call, **referenda**
runs the decision, **conviction-voting** tallies token-weighted votes, and the
**scheduler** enacts the result after the delay.

## 2. Conviction voting (token-weighted votes + lock multipliers)

`pallet-conviction-voting` is where votes are recorded and where lock-based
multipliers apply. Note the vote-locking period and the `Polls = Referenda` wiring.

```rust
// runtime/src/lib.rs

parameter_types! {
    pub const VoteLockingPeriod: BlockNumber = 30 * DAYS;
}

impl pallet_conviction_voting::Config for Runtime {
    type WeightInfo        = pallet_conviction_voting::weights::SubstrateWeight<Self>;
    type RuntimeEvent      = RuntimeEvent;
    type Currency          = Balances;
    type VoteLockingPeriod = VoteLockingPeriod;
    type MaxVotes          = ConstU32<512>;
    type MaxTurnout        = frame_support::traits::TotalIssuanceOf<Balances, Self::AccountId>;
    type Polls             = Referenda;     // votes are cast on Referenda polls
    type BlockNumberProvider = System;
    type VotingHooks       = ();
}
```

The lock-duration → multiplier mapping (1.0× / 1.5× / 2.5×) is documented in
[participation-and-fees.md](participation-and-fees.md).

## 3. Referenda (the referendum lifecycle)

`pallet-referenda` runs submission → decision → confirmation. The origins are the
principal security surface: **any signed account may submit** a referendum, while
**cancel and kill are `Root`-only** — i.e. reachable only through governance itself,
never by an individual.

```rust
// runtime/src/lib.rs

impl pallet_referenda::Config for Runtime {
    type WeightInfo       = pallet_referenda::weights::SubstrateWeight<Self>;
    type RuntimeCall      = RuntimeCall;
    type RuntimeEvent     = RuntimeEvent;
    type Scheduler        = Scheduler;                  // time-locked enactment
    type Currency         = pallet_balances::Pallet<Self>;
    type SubmitOrigin     = EnsureSigned<AccountId>;    // any signed account may submit
    type CancelOrigin     = EnsureRoot<AccountId>;      // cancel only via governance
    type KillOrigin       = EnsureRoot<AccountId>;      // kill only via governance
    type Slash            = ();
    type Votes            = pallet_conviction_voting::VotesOf<Runtime>;
    type Tally            = pallet_conviction_voting::TallyOf<Runtime>;
    type SubmissionDeposit = SubmissionDeposit;
    type MaxQueued        = ConstU32<100>;
    type UndecidingTimeout = UndecidingTimeout;
    type AlarmInterval    = AlarmInterval;
    type Tracks           = TracksInfo;                 // per-class parameters (see §4)
    type Preimages        = Preimage;                   // call bytes stored as preimage
    type BlockNumberProvider = System;
}
```

## 4. Tracks (per-class parameters)

Referendum classes are expressed as **tracks**. Each track sets the decision
deposit, the prepare / decision / confirm / enactment periods, and the approval and
support curves. The standard, mint, emergency-upgrade, and freeze classes described
in [referendum-classes.md](referendum-classes.md) map onto tracks, where:

- the **decision deposit** corresponds to the class's proposal bond,
- the **decision / confirm periods** correspond to the class's voting period,
- the **enactment period** corresponds to the class's execution delay,
- the **approval curve** encodes the passing threshold (simple majority or 75–80%
  supermajority), and
- the **support curve** encodes the quorum (4–40% of circulating QTOV).

Auditors validating the chain should enumerate the live tracks and confirm each
class's deposit, periods, and curves match the parameters in
[referendum-classes.md](referendum-classes.md). The automated checker in
[`check/`](../check) confirms the governance pallets and their structure; the exact
per-class numeric parameters are validated against the class spec.

## 5. Time-locked enactment (scheduler + preimage)

A passed referendum does not execute inline. `pallet-referenda` schedules the
preimage's call through `pallet-scheduler` after the track's enactment period —
this is the on-chain mechanism behind the "execution delay" in the referendum
tables. `pallet-preimage` holds the call bytes (with a storage deposit) until then.

## 6. Post-quantum signature wiring

Every governance extrinsic is authorized by the chain's post-quantum signature
type. The runtime sets:

```rust
// runtime/src/lib.rs
pub type Signature = quantova_account::QSignature;
pub type Hashing   = sha3_substrate_hashing::Sha3Hashing;
```

so a `ConvictionVoting::vote` or `Referenda::submit` extrinsic is verified with a
Dilithium / Falcon / SPHINCS+ signature before dispatch. See
[post-quantum-signing.md](post-quantum-signing.md) for the verification code.

---

*Code is reproduced from the Quantova protocol runtime (`runtime/src/lib.rs`),
© 2026 Quantova Inc, BUSL-1.1.*
