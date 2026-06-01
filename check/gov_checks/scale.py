"""Minimal, dependency-free helpers for reading Quantova (Substrate) chain state.

Everything here is read-only: it derives the storage keys for public chain state
and decodes the SCALE-encoded values the node returns. It contains no signing,
no transaction construction, and no chain-mutating logic.

* ``twox128`` / ``storage_value_key`` — derive the key for a pallet StorageValue.
* ``decode_u64`` / ``decode_h160`` / ``decode_option`` — decode the common value
  shapes used by the bridge pallet's storage items.

The xxHash64 / twox-128 implementation matches Substrate's
``sp_core::twox_128`` (two 64-bit hashes, seeds 0 and 1, little-endian,
concatenated). It is validated against the canonical
``twox128("System") == 0x26aa394eea5630e07c48ae0c9558cef7`` vector in the tests.
"""

from typing import Optional

_MASK64 = (1 << 64) - 1
_P1 = 0x9E3779B185EBCA87
_P2 = 0xC2B2AE3D27D4EB4F
_P3 = 0x165667B19E3779F9
_P4 = 0x85EBCA77C2B2AE63
_P5 = 0x27D4EB2F165667C5


def _rotl(x: int, r: int) -> int:
    return ((x << r) | (x >> (64 - r))) & _MASK64


def _round(acc: int, inp: int) -> int:
    acc = (acc + (inp * _P2 & _MASK64)) & _MASK64
    acc = _rotl(acc, 31)
    acc = (acc * _P1) & _MASK64
    return acc


def _merge(acc: int, val: int) -> int:
    val = _round(0, val)
    acc ^= val
    acc = (acc * _P1 + _P4) & _MASK64
    return acc


def xxh64(data: bytes, seed: int = 0) -> int:
    """xxHash64 of ``data`` with ``seed`` (matches Substrate's usage)."""
    n = len(data)
    i = 0
    if n >= 32:
        v1 = (seed + _P1 + _P2) & _MASK64
        v2 = (seed + _P2) & _MASK64
        v3 = seed & _MASK64
        v4 = (seed - _P1) & _MASK64
        while i + 32 <= n:
            v1 = _round(v1, int.from_bytes(data[i:i + 8], "little")); i += 8
            v2 = _round(v2, int.from_bytes(data[i:i + 8], "little")); i += 8
            v3 = _round(v3, int.from_bytes(data[i:i + 8], "little")); i += 8
            v4 = _round(v4, int.from_bytes(data[i:i + 8], "little")); i += 8
        h = (_rotl(v1, 1) + _rotl(v2, 7) + _rotl(v3, 12) + _rotl(v4, 18)) & _MASK64
        h = _merge(h, v1)
        h = _merge(h, v2)
        h = _merge(h, v3)
        h = _merge(h, v4)
    else:
        h = (seed + _P5) & _MASK64
    h = (h + n) & _MASK64

    while i + 8 <= n:
        k1 = _round(0, int.from_bytes(data[i:i + 8], "little"))
        h ^= k1
        h = (_rotl(h, 27) * _P1 + _P4) & _MASK64
        i += 8
    if i + 4 <= n:
        h ^= (int.from_bytes(data[i:i + 4], "little") * _P1) & _MASK64
        h = (_rotl(h, 23) * _P2 + _P3) & _MASK64
        i += 4
    while i < n:
        h ^= (data[i] * _P5) & _MASK64
        h = (_rotl(h, 11) * _P1) & _MASK64
        i += 1

    h ^= h >> 33
    h = (h * _P2) & _MASK64
    h ^= h >> 29
    h = (h * _P3) & _MASK64
    h ^= h >> 32
    return h


def twox128(data: bytes) -> bytes:
    """Substrate twox-128: xxh64(seed=0) ++ xxh64(seed=1), each little-endian."""
    return xxh64(data, 0).to_bytes(8, "little") + xxh64(data, 1).to_bytes(8, "little")


def storage_value_key(pallet: str, item: str) -> str:
    """0x-hex storage key for a pallet StorageValue: twox128(pallet)++twox128(item)."""
    key = twox128(pallet.encode("ascii")) + twox128(item.encode("ascii"))
    return "0x" + key.hex()


# --- value decoders (SCALE) ------------------------------------------------

def _strip(h: str) -> bytes:
    s = h[2:] if h.startswith(("0x", "0X")) else h
    return bytes.fromhex(s)


def decode_u64(value_hex: Optional[str]) -> Optional[int]:
    """Decode a SCALE u64 (little-endian). None/empty -> 0 (ValueQuery default)."""
    if value_hex is None or value_hex in ("0x", ""):
        return 0
    b = _strip(value_hex)[:8]
    return int.from_bytes(b.ljust(8, b"\x00"), "little")


def decode_h160(value_hex: Optional[str]) -> Optional[str]:
    """Decode an OptionQuery<H160>. Returns 0x-hex address or None if unset."""
    if value_hex is None or value_hex in ("0x", ""):
        return None
    b = _strip(value_hex)
    # OptionQuery prefixes a 0x01 present-byte; tolerate both with/without.
    if len(b) == 21 and b[0] in (0, 1):
        b = b[1:]
    if len(b) < 20:
        return None
    return "0x" + b[:20].hex()


def is_present(value_hex: Optional[str]) -> bool:
    """True if an OptionQuery storage value is set (non-empty)."""
    return value_hex is not None and value_hex not in ("0x", "")


def decode_percent(value_hex: Optional[str]) -> Optional[int]:
    """Decode sp_runtime::Percent (single byte 0..100). None/empty -> 0."""
    if value_hex is None or value_hex in ("0x", ""):
        return 0
    b = _strip(value_hex)
    return b[0] if b else 0
