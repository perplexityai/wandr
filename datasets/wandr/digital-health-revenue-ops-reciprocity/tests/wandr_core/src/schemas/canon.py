from pydantic import BaseModel, Field

CANONICAL_INVALID = "NOT_FOUND"


class CanonResult(BaseModel):
    """Result of canonifying a single key value."""

    canonical: str = Field(
        description=(
            "The canonical form of the input value. "
            f"Return {CANONICAL_INVALID} if no match."
        ),
    )
