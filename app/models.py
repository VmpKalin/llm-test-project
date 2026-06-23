"""Pydantic models for the bookmarks service."""

from pydantic import BaseModel, Field


class BookmarkCreate(BaseModel):
    """Input model used when creating a bookmark."""

    url: str = Field(..., description="The bookmarked URL.")
    title: str = Field(..., description="Human-readable title for the bookmark.")
    tags: list[str] = Field(default_factory=list, description="Optional list of tags.")

    # TODO (planted problem 5): the `url` field is not validated here.
    # It should reject empty strings and any value that does not start with
    # "http://" or "https://", returning a 422 response on invalid input.


class Bookmark(BookmarkCreate):
    """Stored bookmark, including its generated integer id."""

    id: int = Field(..., description="Server-generated unique identifier.")
