```bash
$ alembic revision -m "comment"
$ alembic upgrade +1
$ alembic upgrade head
$ alembic downgrade -1
$ alembic downgrade base
```

`DB_URL` determined from `.env`

VSCode debug configuration included for `upgrade +1` and `downgrade -1`