"""Quantova governance security & conformance checks (read-only).

A read-only back-test check that verifies the Quantova governance structure on a
live node: the OpenGov pallets are present and wired, authorization is
post-quantum, and referendum cancel/kill are governance-gated. It performs no
signing, submits no transactions, and changes nothing.
"""

from . import checks, client, report, scale, spec

__version__ = "1.0.0"
__all__ = ["checks", "client", "report", "scale", "spec", "__version__"]
