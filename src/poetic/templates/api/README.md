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

## app

```bash
uvicorn main:app --reload
```

## DB

SQLite: `db/db.db`

### alembic

```bash
$ alembic revision -m "comment"
$ alembic upgrade +1
$ alembic upgrade head
$ alembic downgrade -1
$ alembic downgrade base
```

`DB_URL` determined from `.env`

VSCode debug configuration included for `upgrade +1` and `downgrade -1`