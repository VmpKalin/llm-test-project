# Bookmarks Service

A small in-memory REST API for saving bookmarks (a URL with a title and tags).
Built with FastAPI and Pydantic, backed by a simple dict-based repository with
no database, so the whole project is self-contained. It exists as a testbed for
an AI coding assistant: most of it works, but a handful of bugs and unfinished
endpoints are planted on purpose (see **Known issues**).

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
./run.sh                            # or: uvicorn app.main:app --reload

# 4. Run the tests
pytest
```

The server listens on http://localhost:8000. Interactive API docs are available
at http://localhost:8000/docs.

## Endpoints

| Method | Path                        | Description                                            |
|--------|-----------------------------|--------------------------------------------------------|
| GET    | `/health`                   | Liveness probe; returns `{"status": "ok"}`.            |
| POST   | `/bookmarks`                | Create a bookmark from a JSON body; returns it with a generated integer id. |
| GET    | `/bookmarks`                | List all bookmarks.                                    |
| GET    | `/bookmarks/{id}`           | Return one bookmark, or 404 if the id does not exist.  |
| GET    | `/bookmarks/search?tag=...` | List bookmarks carrying the given tag (case-insensitive). |
| DELETE | `/bookmarks/{id}`           | Delete a bookmark by id; returns 204 No Content.       |

## Known issues

These are planted on purpose. Each has a matching `# BUG:` or `# TODO:` comment
in the source.

1. `repository.search()` matches tags case-sensitively, so searching `python`
   misses a bookmark tagged `Python`. It should be case-insensitive.
2. `GET /bookmarks/{id}` returns `200` with a `null` body for an unknown id
   instead of a proper `404`.
3. `DELETE /bookmarks/{id}` is declared but its body just raises
   `NotImplementedError`; it must remove the bookmark and return `204`.
4. The id generator is off by one: the first bookmark gets id `0` instead of
   `1`. Ids should start at `1`.
5. `POST /bookmarks` does not validate the `url` field. It should reject empty
   values and anything not starting with `http://` or `https://`, returning
   `422` on invalid input.
6. `GET /bookmarks/search?tag=...` is documented above but the route is missing
   entirely from `routes.py` and needs to be added.
