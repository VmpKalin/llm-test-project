"""Pydantic models for the bookmarks service."""

from pydantic import BaseModel, Field, validator


class BookmarkCreate(BaseModel):
    """Input model used when creating a bookmark."""

    url: str = Field(..., description="The bookmarked URL.")
    title: str = Field(..., description="Human-readable title for the bookmark.")
    tags: list[str] = Field(default_factory=list, description="Optional list of tags.")

    @validator('url')
    def validate_url(cls, v):
        if not v:
            raise ValueError("URL cannot be empty")
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("URL must start with 'http://' or 'https://'")
        return v


class Bookmark(BookmarkCreate):
    """Stored bookmark, including its generated integer id."""

    id: int = Field(..., description="Server-generated unique identifier.")
