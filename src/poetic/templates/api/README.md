## api

API docs: http://localhost:8000/docs

## app

```bash
source venv/bin/activate
poetry install --no-root
uvicorn main:app --reload
```

## docker

```bash
docker compose up --build
```