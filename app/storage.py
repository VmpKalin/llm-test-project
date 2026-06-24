"""JSON storage for bookmarks."""

import json
from pathlib import Path

from app.models import Bookmark


class JsonStorage:
    """JSON storage for bookmarks with a configurable file path."""

    def __init__(self, filepath: str) -> None:
        self.filepath = Path(filepath)

    def save(self, bookmarks: list[Bookmark]) -> None:
        """Write a list of Bookmark objects to the JSON file."""
        try:
            with self.filepath.open('w') as f:
                json.dump([b.model_dump() for b in bookmarks], f)
        except Exception as e:
            raise IOError(f"Failed to save bookmarks: {e}")

    def load(self) -> list[Bookmark]:
        """Read the JSON file and return a list of Bookmark objects."""
        if not self.filepath.exists():
            return []

        try:
            with self.filepath.open('r') as f:
                data = json.load(f)
                return [Bookmark(**item) for item in data]
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON data: {e}")
