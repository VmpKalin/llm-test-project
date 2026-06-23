"""Unit tests for the in-memory BookmarkRepository.

Some tests target the deliberately planted problems and are expected to
FAIL on the fresh, unmodified project.
"""

from app.models import BookmarkCreate
from app.repository import BookmarkRepository


def make_data(url="https://example.com", title="Example", tags=None):
    """Helper to build a BookmarkCreate with sensible defaults."""
    return BookmarkCreate(url=url, title=title, tags=tags or [])


def test_add_and_get():
    """A stored bookmark can be retrieved by its id."""
    repo = BookmarkRepository()
    created = repo.add(make_data())
    fetched = repo.get(created.id)
    assert fetched is not None
    assert fetched.url == "https://example.com"


def test_list_returns_all():
    """list() returns every stored bookmark."""
    repo = BookmarkRepository()
    repo.add(make_data(title="One"))
    repo.add(make_data(title="Two"))
    assert len(repo.list()) == 2


def test_get_missing_returns_none():
    """get() returns None for an unknown id."""
    repo = BookmarkRepository()
    assert repo.get(999) is None


def test_delete_removes_bookmark():
    """delete() removes an existing bookmark and reports success."""
    repo = BookmarkRepository()
    created = repo.add(make_data())
    assert repo.delete(created.id) is True
    assert repo.get(created.id) is None


def test_delete_missing_returns_false():
    """delete() reports False when the id does not exist."""
    repo = BookmarkRepository()
    assert repo.delete(123) is False


def test_first_id_is_one():
    """Planted problem 4: ids should start at 1, not 0."""
    repo = BookmarkRepository()
    created = repo.add(make_data())
    assert created.id == 1  # currently fails: first id is 0


def test_search_is_case_insensitive():
    """Planted problem 1: tag search should ignore case."""
    repo = BookmarkRepository()
    repo.add(make_data(title="Py", tags=["Python"]))
    results = repo.search("python")
    assert len(results) == 1  # currently fails: search is case-sensitive
