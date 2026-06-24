"""Tests for the JsonStorage class."""

import json
from pathlib import Path

import pytest

from app.models import Bookmark
from app.storage import JsonStorage


@pytest.fixture
def storage(tmp_path):
    """Fixture to provide a temporary JsonStorage instance."""
    filepath = tmp_path / "bookmarks.json"
    return JsonStorage(filepath)


def test_save_and_load(storage, tmp_path):
    """Test saving and loading bookmarks."""
    # Create some sample bookmarks
    bookmark1 = Bookmark(id=1, url="http://example.com", title="Example", tags=["test"])
    bookmark2 = Bookmark(id=2, url="http://example.org", title="Example Org", tags=["test"])

    # Save the bookmarks to the storage
    storage.save([bookmark1, bookmark2])

    # Load the bookmarks from the storage
    loaded_bookmarks = storage.load()

    # Check that the loaded bookmarks match the original ones
    assert len(loaded_bookmarks) == 2
    assert loaded_bookmarks[0].id == 1
    assert loaded_bookmarks[0].url == "http://example.com"
    assert loaded_bookmarks[0].title == "Example"
    assert loaded_bookmarks[0].tags == ["test"]
    assert loaded_bookmarks[1].id == 2
    assert loaded_bookmarks[1].url == "http://example.org"
    assert loaded_bookmarks[1].title == "Example Org"
    assert loaded_bookmarks[1].tags == ["test"]


def test_load_nonexistent_file(storage):
    """Test loading from a non-existent file."""
    # Load bookmarks from a non-existent file
    loaded_bookmarks = storage.load()

    # Check that the loaded bookmarks are empty
    assert len(loaded_bookmarks) == 0


def test_load_invalid_json(storage, tmp_path):
    """Test loading from a file with invalid JSON data."""
    # Create an invalid JSON file
    filepath = tmp_path / "bookmarks.json"
    with open(filepath, 'w') as f:
        f.write("invalid json")

    # Load bookmarks from the invalid JSON file
    with pytest.raises(ValueError):
        storage.load()
