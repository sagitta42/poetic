## api

API docs: http://localhost:8000/docs

## docker

```bash
docker compose up --build
```

## app

```bash
source venv/bin/activate
poetry install --no-root
uvicorn main:app --reload
```