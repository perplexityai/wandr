"""Validation for untrusted URLs before any verifier-side network access."""

from __future__ import annotations

import asyncio
import ipaddress
import socket
from urllib.parse import SplitResult, urlsplit


class UnsafeURLError(ValueError):
    """A URL is malformed or can address a non-public network."""


def parse_http_url(url: str) -> tuple[SplitResult, str, int]:
    """Return parsed URL, hostname, and port for a safe HTTP(S) URL shape."""
    if (
        not url
        or "\\" in url
        or any(char.isspace() or ord(char) < 32 or 127 <= ord(char) <= 159 for char in url)
    ):
        raise UnsafeURLError("URL contains whitespace, controls, or backslashes")

    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise UnsafeURLError("URL is malformed") from exc

    if parsed.scheme.lower() not in {"http", "https"}:
        raise UnsafeURLError("URL scheme must be http or https")
    if not parsed.hostname:
        raise UnsafeURLError("URL requires a hostname")
    if parsed.username is not None or parsed.password is not None:
        raise UnsafeURLError("URL must not contain credentials")

    hostname = parsed.hostname
    if "%" in hostname:
        raise UnsafeURLError("URL must not contain an IPv6 zone identifier")
    effective_port = port or (443 if parsed.scheme.lower() == "https" else 80)

    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        literal = None
    if literal is not None and not _is_global_address(literal):
        raise UnsafeURLError("URL resolves to a non-public address")

    return parsed, hostname, effective_port


def _is_global_address(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    return address.is_global and not (
        address.is_link_local
        or address.is_loopback
        or address.is_multicast
        or address.is_private
        or address.is_reserved
        or address.is_unspecified
    )


async def resolve_public_http_url(
    url: str,
    *,
    timeout: float,
) -> tuple[str, tuple[str, ...]]:
    """Resolve a URL and reject empty, mixed, or non-global address answers."""
    _, hostname, port = parse_http_url(url)
    loop = asyncio.get_running_loop()
    try:
        answers = await asyncio.wait_for(
            loop.getaddrinfo(hostname, port, type=socket.SOCK_STREAM),
            timeout=timeout,
        )
    except (OSError, TimeoutError) as exc:
        raise UnsafeURLError("URL hostname could not be resolved") from exc

    addresses: set[str] = set()
    for answer in answers:
        sockaddr = answer[4]
        if not sockaddr:
            continue
        raw_address = str(sockaddr[0]).split("%", 1)[0]
        try:
            address = ipaddress.ip_address(raw_address)
        except ValueError as exc:
            raise UnsafeURLError("URL resolver returned an invalid address") from exc
        if not _is_global_address(address):
            raise UnsafeURLError("URL resolves to a non-public address")
        addresses.add(address.compressed)

    if not addresses:
        raise UnsafeURLError("URL hostname returned no addresses")
    return hostname, tuple(sorted(addresses))
