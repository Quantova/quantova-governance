# Post-Quantum Signing of Governance & Votes

Every governance action on Quantova — submitting a referendum, placing a vote,
delegating, or removing a vote — is an ordinary signed transaction. What makes it
post-quantum is the **signature type the runtime accepts**: Quantova does not use
ECDSA/secp256k1 anywhere. The chain's signature type is a NIST post-quantum
signature, so the authority to govern is gated end-to-end by post-quantum
cryptography.

This document shows exactly where and how that happens, using the real code from
the Quantova protocol runtime.

## 1. The chain's signature type is post-quantum

The runtime defines its transaction signature type as `QSignature`, and derives the
account id from the signer of that signature. Governance pallets inherit this
automatically — they never define their own signature scheme.

```rust
// runtime/src/lib.rs

/// Alias to a hash when used in the context of a transaction signature on the chain.
pub type Signature = quantova_account::QSignature;

/// Some way of identifying an account on the chain. We intentionally make it
/// equivalent to the public key of our transaction signing scheme.
pub type AccountId = <<Signature as Verify>::Signer as IdentifyAccount>::AccountId;

/// The hashing algorithm used by the chain.
pub type Hashing = sha3_substrate_hashing::Sha3Hashing;
```

Because `Signature = QSignature`, the signed extrinsic that carries a
`ConvictionVoting::vote` or `Referenda::submit` call is verified with a
post-quantum signature before the call is ever dispatched. There is no separate
governance credential — your governance identity is simply your post-quantum
account.

## 2. The three post-quantum schemes

`QSignature` is an enum over the three NIST post-quantum signature schemes Quantova
supports. All three share one address space.

```rust
// primitives/account/src/lib.rs

pub type SphincsSignatureBytes   = BoundedVec<u8, ConstU32<7856>>;
pub type FalconSignatureBytes    = BoundedVec<u8, ConstU32<754>>;
pub type DilithiumSignatureBytes = BoundedVec<u8, ConstU32<2420>>;

pub enum QSignature {
    /// SLH-DSA (aka SPHINCS+) signature scheme
    /// Based on https://csrc.nist.gov/pubs/fips/205/final
    SPHINCS   { signature: SphincsSignatureBytes,   public_key: sphincsp::Public },
    /// Falcon-512 signature scheme
    FALCON    { signature: FalconSignatureBytes,    public_key: falcon::Public },
    /// Dilithium2 signature scheme
    DILITHIUM { signature: DilithiumSignatureBytes, public_key: dilithium::Public },
}
```

| Scheme | Standard | Signature size |
|---|---|---|
| SPHINCS+ (SLH-DSA) | NIST FIPS 205 | up to 7856 bytes |
| Falcon-512 | NIST PQC (FN-DSA) | up to 754 bytes |
| Dilithium2 | NIST (ML-DSA) | up to 2420 bytes |

## 3. How a governance vote is verified

When a vote extrinsic arrives, the runtime calls `QSignature::verify`. For each
scheme it (1) verifies the post-quantum signature over the signed payload, and then
(2) derives the account id **from the public key** and checks it matches the claimed
signer. Both must hold or the extrinsic is rejected — so a vote can only be cast by
the holder of the corresponding post-quantum private key.

```rust
// primitives/account/src/lib.rs  (abridged: one of three identical-shaped arms)

impl Verify for QSignature {
    type Signer = QSigner;

    fn verify<L: Lazy<[u8]>>(&self, mut msg: L, signer: &AccountId32) -> bool {
        match self {
            QSignature::DILITHIUM { signature, public_key } => {
                let detached = match TryInto::<[u8; dilithium::DETACHED_SIGNATURE_SERIALIZED_SIZE]>
                    ::try_into(signature.as_slice())
                {
                    Ok(sig) => sig,
                    Err(_)  => return false,
                };
                let signature = dilithium::Signature::from_components(*public_key, detached);

                // (1) post-quantum signature must verify over the payload
                if !signature.verify(msg.get(), public_key) {
                    return false;
                }
                // (2) the account id derived from the public key must match the signer
                let derived_account_id = QSigner::from(*public_key).into_account();
                derived_account_id == *signer
            },
            // QSignature::FALCON { .. }  => { /* same shape, Falcon verify */ },
            // QSignature::SPHINCS { .. } => { /* same shape, SPHINCS+ verify */ },
            # _ => false,
        }
    }
}
```

## 4. Post-quantum account derivation

The account that votes is derived deterministically from the post-quantum public
key: SHA3-256 of the public key, truncated to 20 bytes, with the leading byte set
to `0x40` (the Base64 "Q" branding). This is the `QSigner` → account id mapping the
verifier checks against.

```rust
// primitives/account/src/lib.rs

impl From<sphincsp::Public> for QSigner {
    fn from(pk: sphincsp::Public) -> Self {
        let digest = sha3_substrate_hashing::Sha3Hashing::hash(pk.as_ref()).0;
        let mut address = [0u8; 20];
        address.copy_from_slice(&digest[..20]);
        address[0] = 0x40; // Append branding Q in base64
        QSigner::from(address)
    }
}

impl sp_runtime::traits::IdentifyAccount for QSigner {
    type AccountId = AccountId32;
    fn into_account(self) -> Self::AccountId { AccountId32::new(self.0) }
}
```

## 5. End-to-end: what secures a vote

1. A holder builds a `ConvictionVoting::vote { poll_index, vote }` (or
   `Referenda::submit`) call.
2. The call is wrapped in an extrinsic and **signed with the holder's post-quantum
   key** (Dilithium, Falcon, or SPHINCS+).
3. On import, the runtime checks the signature via `QSignature::verify`: the
   post-quantum signature must verify over the payload **and** the account derived
   from the public key must equal the signer.
4. Only then is the vote dispatched and tallied by `pallet-referenda` /
   `pallet-conviction-voting`.

The same post-quantum gate applies to proposal submission, delegation, and vote
removal — there is no classical-cryptography path into Quantova governance.

---

*Code is reproduced from the Quantova protocol runtime (`runtime/src/lib.rs`,
`primitives/account/src/lib.rs`), © 2026 Quantova Inc, BUSL-1.1. The `verify`
function above is abridged to one of three equally-shaped match arms for
readability; the Falcon and SPHINCS+ arms perform the analogous scheme-specific
verification.*
