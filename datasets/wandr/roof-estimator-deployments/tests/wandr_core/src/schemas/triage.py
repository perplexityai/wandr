"""Shared schemas used by pipeline components."""

from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    """Quick check: is fetched page content usable for analysis?"""

    usable: bool = Field(
        description=(
            "True if the meat of the page content is delivered, even alongside nav/cookie/login garbage. "
            "False ONLY if: entirely a CAPTCHA/login wall with zero real text, obviously truncated behind "
            "a paywall, or completely garbled. When in doubt, True."
        ),
    )
    reason: str = Field(
        description="One sentence explaining the decision.",
    )
