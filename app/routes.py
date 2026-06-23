"""HTTP route handlers for the bookmarks service."""

from fastapi import APIRouter, Response

from app.models import Bookmark, BookmarkCreate
from app.repository import repository

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@router.post("/bookmarks", response_model=Bookmark)
def create_bookmark(data: BookmarkCreate) -> Bookmark:
    """Create a bookmark from the request body and return it with an id."""
    return repository.add(data)


@router.get("/bookmarks", response_model=list[Bookmark])
def list_bookmarks() -> list[Bookmark]:
    """Return all stored bookmarks."""
    return repository.list()


# BUG (planted problem 6): the search route is documented in the README
# (GET /bookmarks/search?tag=...) but is intentionally missing here.
# It must be added so that searching by tag works through the API.
#
# Note on ordering: when the search route is added it must be declared
# BEFORE the /bookmarks/{id} route below, otherwise FastAPI will try to
# parse "search" as an integer id.


@router.get("/bookmarks/{bookmark_id}", response_model=Bookmark)
def get_bookmark(bookmark_id: int) -> Bookmark | None:
    """Return a single bookmark by id."""
    # BUG (planted problem 2): when the id does not exist this returns None,
    # which FastAPI serializes as a 200 response with a null body.
    # It should instead raise an HTTPException(404).
    return repository.get(bookmark_id)


@router.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int) -> Response:
    """Delete a bookmark by id and return 204 No Content."""
    # TODO (planted problem 3): implement deletion.
    # This should remove the bookmark via repository.delete() and return a
    # 204 response, or raise a 404 if the bookmark does not exist.
    raise NotImplementedError("DELETE /bookmarks/{id} is not implemented yet")
