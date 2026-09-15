# Mini CRM

A minimal CRM for sales managers to capture and track leads. Prospects submit
their details through a Telegram bot; managers work the leads through a REST API.

Two independent processes share one PostgreSQL database and communicate **only
over HTTP** (bot → API):

- **API** (`src/app`) — FastAPI service: authentication, leads, users.
- **Bot** (`src/tg_bot`) — aiogram Telegram bot that walks a prospect through a
  lead form and posts the result to the API.

## How it works

1. A manager registers and logs in (JWT auth).
2. `GET /users/invite-link` returns a personal `t.me/<bot>?start=<token>` link.
3. A prospect opens the link; the bot collects **name → phone → email**.
4. The bot posts the lead to `POST /bot/leads/` (authenticated with a shared
   secret header); the API creates it **assigned to that manager**.
5. The manager lists their leads and moves each through the status flow
   `new → in_progress → closed`.

Leads are scoped per manager — a manager only ever sees and mutates their own.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy 2.0 (async) + asyncpg, PostgreSQL
- Alembic (migrations)
- Pydantic v2 / pydantic-settings
- python-jose (JWT, HS256) + bcrypt
- aiogram 3 (bot) + httpx
- uv (dependencies) · pytest (tests)
- Docker / Docker Compose

## Architecture

Each resource follows `router → service → repository → model`:

```
src/app/
  api/            # routers (HTTP layer), dependencies, exception handlers
  services/       # business logic (incl. lead status state machine)
  repositories/   # database access
  core/
    db/           # engine, session, models, DB config
    schemas/      # Pydantic request/response models
    security.py   # JWT + password hashing
src/tg_bot/       # Telegram bot (separate process)
```

## Running with Docker

Requirements: Docker + Docker Compose, and a Telegram bot token from
[@BotFather](https://t.me/BotFather).

1. Create your env file:
   ```bash
   cp .env.example .env
   ```
2. Fill in `.env`:
   - `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB`
   - `SECRET_KEY` and `BOT_SECRET_KEY` — generate strong values:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
   - `TELEGRAM_BOT_TOKEN` and `BOT_USERNAME` from BotFather.
3. Start everything:
   ```bash
   docker compose up --build
   ```

On startup the API applies database migrations (`alembic upgrade head`)
automatically, then serves on **http://localhost:8000**.
Interactive API docs (Swagger): **http://localhost:8000/docs**.

## Local development

Requires a running Postgres and a `DATABASE_URL` in `.env`.

```bash
uv run uvicorn src.app.main:app --reload    # API
uv run python -m src.tg_bot.main            # bot (separate process)
```

Migrations:

```bash
uv run alembic revision --autogenerate -m "message"
uv run alembic upgrade head
```

## Tests

```bash
uv run pytest tests/ -v
```

Tests run against an in-memory SQLite database and require neither Docker nor
Postgres.
