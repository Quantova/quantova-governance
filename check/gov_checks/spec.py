"""Expected governance structure, derived from the Quantova protocol runtime.

This is the conformance baseline for the back-test check: the OpenGov pallets the
canonical runtime exposes, a representative set of their storage items and calls,
and the post-quantum signature identifiers that must be present. The structural
checks confirm a running node's metadata matches this baseline.

Sources (Quantova protocol runtime):
* construct_runtime: Preimage(27), Scheduler(28), Referenda(29), ConvictionVoting(30)
* signature type:    `Signature = quantova_account::QSignature` (Dilithium/Falcon/SPHINCS+)
"""

# Governance pallet names (runtime construct_runtime names) and their indices.
GOVERNANCE_PALLETS = {
    "Preimage": 27,
    "Scheduler": 28,
    "Referenda": 29,
    "ConvictionVoting": 30,
}

# Representative storage items per pallet (present in standard OpenGov runtimes).
EXPECTED_STORAGE = {
    "Referenda": ["ReferendumCount", "ReferendumInfoFor", "TrackQueue", "DecidingCount"],
    "ConvictionVoting": ["VotingFor", "ClassLocksFor"],
    "Preimage": ["StatusFor", "PreimageFor"],
    "Scheduler": ["Agenda", "Lookup"],
}

# Representative dispatchables per pallet.
EXPECTED_CALLS = {
    "Referenda": ["submit", "place_decision_deposit", "cancel", "kill", "nudge_referendum"],
    "ConvictionVoting": ["vote", "delegate", "undelegate", "unlock", "remove_vote"],
    "Preimage": ["note_preimage", "unnote_preimage", "request_preimage"],
    "Scheduler": ["schedule", "cancel", "schedule_named"],
}

# Post-quantum signing identifiers expected in runtime metadata.
# (QSignature enum + the three NIST scheme variants / primitive public-key types.)
PQ_SIGNATURE_TYPE = "QSignature"
PQ_SCHEME_NAMES = ["SPHINCS", "FALCON", "DILITHIUM"]

# Governance-gated origin expectations (verified structurally where possible).
# Referenda submit is signed; cancel/kill are Root (governance-only).
ROOT_GATED_CALLS = ["cancel", "kill"]
