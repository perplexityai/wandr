from collections.abc import Collection, Mapping
from typing import Any

from relay.core import RelayError


def validate_request_mapping(
    value: Mapping[str, Any] | None,
    *,
    provider: str,
    allowed: Collection[str],
) -> dict[str, Any]:
    data = dict(value or {})
    unknown = sorted((key for key in data if key not in allowed), key=str)
    if unknown:
        noun = "option" if len(unknown) == 1 else "options"
        names = ", ".join(repr(key) for key in unknown)
        supported = ", ".join(sorted(allowed))
        raise RelayError(
            f"Unknown {provider} request {noun}: {names}. "
            f"Supported options: {supported}."
        )
    return data
