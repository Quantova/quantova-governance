# Quantova Licensing Overview

**Repository:** `quantova-governance` — Quantova Governance Reference

This repository contains software and documentation developed and maintained by Quantova Inc. This file serves as the authoritative licensing index for the contents of this repository and applies to all contents of this repository unless explicitly stated otherwise. It is published in alignment with the licensing standard of the wider Quantova technology stack.

## Copyright and Ownership

© 2026 Quantova Inc. All rights reserved.

Quantova Inc is a company registered in Singapore and is the legal owner and steward of:

- The Quantova protocol
- The QRC20 network standards
- The Quantova Virtual Machine (QVM)
- The Provenance and Quantization Registry (PQR)
- Associated research, specifications, client libraries, and reference implementations

This repository provides reference documentation for the Quantova on-chain governance structure and forms part of this stack.

## Primary License: Business Source License (BUSL-1.1)

Unless otherwise stated, all contents of this repository — including the SDK source code, reference implementations, examples, and documentation — are licensed under the Business Source License, version 1.1 (BUSL-1.1).

The full license text is included in this repository at:

```
/LICENSE-BUSL-1.1
```

The authoritative BUSL-1.1 license text may also be obtained from: https://mariadb.com/bsl11/

Key parameters for this repository:

- **Licensor:** Quantova Inc.
- **Licensed Work:** `quantova-governance` — Quantova Governance Reference, © 2026 Quantova Inc.
- **Change Date:** 2029-06-01 (or the fourth anniversary of the first public distribution of a given version, whichever comes first).
- **Change License:** Apache License, Version 2.0.

On the Change Date, each version of the Licensed Work converts automatically to the Change License.

## What This Repository Contains

This repository provides reference documentation for the Quantova on-chain governance structure: how decisions are made, the participation bonds and lock-ups, the referendum classes, the post-quantum signing path that secures every vote, and the governance pallet wiring. It contains documentation and excerpts of the protocol's own source code for reference. It does not contain private keys, secrets, deployment material, or any code that performs on-chain actions.

## Application and Integration Clarification

Reading, citing, and reviewing this documentation to understand, audit, or build on Quantova governance is explicitly permitted. The repository is reference material and does not itself perform any on-chain action.

## Validator and Node Operator Clarification

Running a validator node or full node on the canonical Quantova network, and using this SDK to support such operation, is explicitly permitted under the BUSL-1.1 license and does not constitute restricted "Production Use."

A formal clarification for validators, node operators, exchanges, custodians, and infrastructure providers is provided at:

```
/docs/validators/licensing.md
```

Participation in staking, consensus, block production, and transaction processing on the Quantova network does not create additional licensing obligations.

## Restricted Use Under BUSL-1.1

The BUSL-1.1 license restricts use of the Licensed Work, together with Quantova consensus, runtime, and QVM code, to launch, operate, or market a competing blockchain network or distributed ledger that is not the canonical Quantova network. It further restricts offering the Licensed Work to third parties as a hosted or managed service, or otherwise using the Licensed Work to provide a commercial product or service that competes with the products or services of the Licensor.

This restriction applies to, but is not limited to:

- Independent or derivative mainnets
- Forks marketed as separate networks
- Networks intended to replace or compete with Quantova
- SDK distributions repackaged or offered as a competing managed service

Forking, modifying, or analyzing the code for testing, auditing, research, or contribution purposes is permitted.

## Canonical Network Definition

For licensing and authorization purposes, the canonical Quantova network is defined by all of the following:

- Official signed source releases published by Quantova Inc
- A unique post-quantum genesis hash
- Signed runtime and protocol artifacts
- Post-quantum cryptographic signatures, including CRYSTALS-Dilithium and Falcon

Any network deployment that does not match these identifiers is not the Quantova network and is not authorized under the Quantova BUSL license.

## Documentation and Specifications

Documentation, research materials, and protocol specifications included in this repository are licensed under BUSL-1.1 unless explicitly stated otherwise within the relevant file or directory. Documentation is provided for informational and technical reference purposes and reflects protocol behavior enforced by code.

## Third-Party Software

This repository is documentation and does not bundle third-party software dependencies. Code excerpts shown for reference are part of the Quantova protocol and are governed by this same license. Any third-party notices that apply to the protocol itself are maintained in the protocol repository. Where applicable, third-party license notices are provided in:

```
/THIRD_PARTY_LICENSES.md
```

or within dependency manifests (for example, `pyproject.toml`).

## No Legal, Financial, or Regulatory Advice

Nothing in this repository, including documentation and specifications, constitutes legal, financial, or regulatory advice. Operators, validators, and users are responsible for ensuring compliance with applicable laws and regulations in their respective jurisdictions.

## Institutional and Licensing Inquiries

Licensing, institutional, and regulatory inquiries relating to the Quantova technology stack should be directed through official Quantova channels published by Quantova Inc.

Protocol identity and licensing intent are cryptographically anchored at genesis via an immutable on-chain commitment.

© 2026 Quantova Inc
