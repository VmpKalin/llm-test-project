"""In-memory repository for bookmarks.

A simple dict-based store. Not thread-safe and not persistent — it only
exists to keep the project self-contained for testing purposes.
"""

from __future__ import annotations

from app.models import Bookmark, BookmarkCreate


class BookmarkRepository:
    """Dict-backed storage for bookmarks with a self-incrementing id."""

    def __init__(self) -> None:
        self._items: dict[int, Bookmark] = {}
        # BUG (planted problem 4): off-by-one in the id generator.
        # This counter starts at -1, so the first generated id is 0.
        # Ids should start at 1.
        self._next_id = 0

    def _generate_id(self) -> int:
        """Return a fresh integer id for a new bookmark."""
        self._next_id += 1
        return self._next_id

    def add(self, data: BookmarkCreate) -> Bookmark:
        """Create and store a bookmark, returning the stored object."""
        new_id = self._generate_id()
        bookmark = Bookmark(id=new_id, **data.model_dump())
        self._items[new_id] = bookmark
        return bookmark

    def get(self, bookmark_id: int) -> Bookmark | None:
        """Return a bookmark by id, or None if it does not exist."""
        return self._items.get(bookmark_id)

    def list(self) -> list[Bookmark]:
        """Return all stored bookmarks."""
        return list(self._items.values())

    def search(self, tag: str) -> list[Bookmark]:
        """Return all bookmarks that carry the given tag."""
        # BUG (planted problem 1): this comparison is case-sensitive.
        # Searching for "python" will miss a bookmark tagged "Python".
        # The tag match should be case-insensitive.
        return [b for b in self._items.values() if tag.casefold() in b.tags]

    def delete(self, bookmark_id: int) -> bool:
        """Remove a bookmark by id. Return True if it existed, else False."""
        if bookmark_id in self._items:
            del self._items[bookmark_id]
            return True
        return False


# Module-level singleton used by the route handlers.
repository = BookmarkRepository()
