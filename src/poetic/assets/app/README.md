## setup

```bash
source venv/bin/activate
poetry install --no-root
cp .env.template .env
```

## api

API docs: http://localhost:8000/docs

## docker

```bash
docker compose up --build
```

Only one service:
```bash
docker compose up --build  <service>

## app

```bash
uvicorn main:app --reload
```