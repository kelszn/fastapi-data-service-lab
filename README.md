# FastAPI CRUD Learning Lab

A small in-memory REST API built to practise FastAPI routing, Pydantic request validation and HTTP error handling.

This is a learning lab, not a production service. Data is stored in a Python list and resets whenever the application restarts.

## Implemented endpoints

| Method | Route | Behaviour |
|---|---|---|
| `GET` | `/` | Basic health-style response |
| `GET` | `/posts` | Return all in-memory posts |
| `GET` | `/posts/latest` | Return the latest post or a 404 |
| `GET` | `/posts/{id}` | Return one post by integer ID |
| `POST` | `/posts` | Validate and create a post |
| `PUT` | `/posts/{id}` | Replace a post while preserving its ID |
| `DELETE` | `/posts/{id}` | Remove a post or return a 404 |

## Data model

A new post accepts:

- `title: str`
- `content: str`
- `published: bool = True`
- `rating: int | None`

The server assigns an ID; clients do not supply it.

## Repository map

```text
.
├── app/
│   ├── __init__.py
│   └── main.py          # Model, in-memory store, helpers and routes
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- API root: <http://127.0.0.1:8000/>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{"title":"Delta tables","content":"Notes on append and merge behaviour","published":true,"rating":8}'
```

## Current boundaries

- no database or persistence;
- no authentication or authorisation;
- random IDs are not guaranteed to be collision-free;
- no automated tests;
- the delete handler should return an empty response body explicitly;
- the update response should be a structured JSON object rather than a formatted string.

## Next improvements

1. Add pytest/TestClient coverage for success and error paths.
2. Move models and routes into separate modules as the app grows.
3. Add SQL persistence and migrations.
4. Return consistent response models.
5. Add logging, configuration and containerised setup.

## Tools

Python · FastAPI · Pydantic · Uvicorn · REST · HTTP status handling
