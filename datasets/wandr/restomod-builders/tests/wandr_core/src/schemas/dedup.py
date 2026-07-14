from pydantic import BaseModel, Field


class DedupResult(BaseModel):
    """Groups of duplicate item numbers from the numbered input list."""

    groups: list[list[int]] = Field(
        description=(
            "Groups of duplicate item numbers. Each group is a list of numbers that "
            "refer to the same entity. Singletons are omitted."
        ),
    )
