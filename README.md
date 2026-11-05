# Flask Task Manager — PostgreSQL edition

A small Flask CRUD app using PostgreSQL. This version is intended for Docker/containerization practice.

## Features
- Create tasks with title and description
- Mark tasks complete or active
- Delete tasks
- PostgreSQL persistence
- `/health` endpoint checks database connectivity

## Project structure
```text
flask-task-manager-postgres/
├── app.py
├── requirements.txt
├── templates/
├── static/
├── .gitignore
└── README.md
```

## PostgreSQL connection

The app reads its connection string from `DATABASE_URL`.

Example:
```text
postgresql://taskuser:taskpass@db:5432/taskmanager
```

When using Docker Compose, `db` should be the PostgreSQL service name. Do not use `localhost` from inside the Flask container to reach the database container.

## Run locally

You need a PostgreSQL server available and a database/user created. Set `DATABASE_URL`, then:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://taskuser:taskpass@localhost:5432/taskmanager"
python app.py
```

Open http://localhost:5000

## Containerization challenge

This project intentionally does not include a Dockerfile or Compose file. Build them yourself.

Suggested milestones:
1. Create a Dockerfile and install `requirements.txt`.
2. Run the Flask app with Gunicorn (example command: `gunicorn --bind 0.0.0.0:5000 app:app`).
3. Create a PostgreSQL container using the official `postgres` image.
4. Set `DATABASE_URL` on the Flask container, using the database service name as the hostname.
5. Add a named volume mounted at `/var/lib/postgresql/data` for PostgreSQL persistence.
6. Add a PostgreSQL health check and make the app wait for the database to become healthy.
7. Test create/list/complete/delete tasks and `/health`.

## Environment variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL |
| `SECRET_KEY` | Flask session signing key |
| `PORT` | App port; defaults to 5000 |

Use strong secrets outside local practice. Do not commit real credentials to Git.
