"""Read-only JSON-RPC client for the Quantova governance back-test check.

This client only ever READS: state queries, finality, and runtime metadata. It
performs no signing, submits no transactions, and exposes no state-changing call —
so it cannot alter the chain, even by mistake. The HTTP transport is a
``requests``-style session and can be injected (the offline self-test does this to
run with no network).
"""

from typing import Any, List, Optional

try:
    import requests as _requests
except Exception:  # pragma: no cover
    _requests = None


class RpcError(Exception):
    pass


class RpcClient:
    """Minimal read-only JSON-RPC client."""

    def __init__(self, endpoint: str, session: Optional[Any] = None, timeout: int = 30):
        self.endpoint = endpoint
        self.timeout = timeout
        self._id = 1
        if session is not None:
            self.session = session
        elif _requests is not None:
            self.session = _requests.Session()
        else:
            raise RuntimeError("the 'requests' package is required (or inject a session)")

    def call(self, method: str, params: Optional[List[Any]] = None) -> Any:
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or []}
        self._id += 1
        try:
            resp = self.session.post(self.endpoint, json=payload,
                                     headers={"content-type": "application/json"},
                                     timeout=self.timeout)
            data = resp.json()
        except Exception as exc:
            raise RpcError(f"{method} transport error: {exc}") from exc
        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            raise RpcError(f"{method}: {err.get('message') if isinstance(err, dict) else err}")
        return data.get("result") if isinstance(data, dict) else data

    # read-only conveniences
    def metadata(self) -> str:
        return self.call("state_getMetadata", [])

    def finalized_head(self) -> str:
        return self.call("chain_getFinalizedHead", [])

    def header(self, block_hash: Optional[str] = None) -> dict:
        return self.call("chain_getHeader", [block_hash] if block_hash else [])

    def health(self) -> dict:
        return self.call("system_health", [])

    def runtime_version(self) -> dict:
        return self.call("state_getRuntimeVersion", [])

    def get_storage(self, key_hex: str, at: Optional[str] = None) -> Optional[str]:
        return self.call("state_getStorage", [key_hex] + ([at] if at else []))
