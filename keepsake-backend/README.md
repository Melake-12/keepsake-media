# Keepsake API

FastAPI backend for the Keepsake couple's memory app. Tested end to end
(register → pair via invite code → upload a memory → shared visibility)
against SQLite; swap in Neon Postgres for real use.

## 1. Set up Neon

1. Create a free account at neon.tech, create a project.
2. Copy the connection string (looks like
   `postgresql://user:pass@ep-xxxx.neon.tech/dbname?sslmode=require`).
3. Change the prefix to `postgresql+psycopg2://` for SQLAlchemy.

## 2. Set up Cloudflare R2

1. Create a free Cloudflare account, enable R2 (needs a card on file, but
   you stay well within the free 10 GB tier for this app).
2. Create a bucket, e.g. `keepsake-media`.
3. Create an R2 API token (Account Home > R2 > Manage API tokens) with
   read/write access to the bucket. Note the Account ID, Access Key ID,
   and Secret Access Key.
4. (Optional, for later) connect a custom domain to the bucket so photos
   have a real public URL instead of the default R2 one.

## 3. Configure environment

Copy `.env.example` to `.env` and fill in your real values:

```bash
cp .env.example .env
```

## 4. Install and run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API docs.

## What's built

- `POST /auth/register`, `POST /auth/login` — email + password, returns
  a JWT valid for 7 days
- `POST /couples` — current user creates a couple workspace, gets an
  invite code back
- `POST /couples/join` — partner joins using that invite code (caps at
  two people per couple)
- `GET /memories/upload-url` — returns a presigned R2 URL; the app PUTs
  the photo/video directly to R2, file bytes never touch this server
- `POST /memories` — records the uploaded memory (caption, date, geo)
  once the R2 upload finishes
- `GET /memories` — lists the couple's shared gallery

Every memory, journal entry, and bucket-list item is scoped by
`couple_id`, so the same schema supports one couple today and many
couples later without a rewrite.

## Not built yet (next steps, in roadmap order)

- Journal entries and bucket list routers (same pattern as `memories.py`
  — copy it)
- Actual email delivery for invites (right now the invite code is
  returned in the API response; wire up a free tier like Resend to
  email it instead)
- Push notifications (Expo Notifications) for check-ins and countdowns
- Map view endpoint (memories already store latitude/longitude)

## A note on passwords

Pin `bcrypt==4.0.1` in requirements.txt — newer bcrypt releases break
passlib's version detection. Already handled in this requirements.txt.
