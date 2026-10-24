# Administration & Maintenance

Backups, updates, email (SMTP), push credentials, troubleshooting, and the full CLI reference.

---

## The `./bustracker` CLI

All management runs through one command (`bustracker` on Windows):

```
./bustracker install       First-time setup (server URL, company, admin, optional SMTP/push)
./bustracker start         Start all containers
./bustracker stop          Stop all containers
./bustracker restart       Restart all containers
./bustracker update        Pull the latest version, rebuild, and restart
./bustracker logs          Live logs (Ctrl+C to stop) — e.g. ./bustracker logs bustracker
./bustracker status        Show container status
./bustracker seed          Insert/update the company row from .env
./bustracker storage-setup Configure the media storage bucket + policies (idempotent)
./bustracker add-admin     Create a dashboard admin (email + password)
./bustracker backup        Dump the database to backups/
./bustracker restore       Restore a backup: ./bustracker restore backups/file.sql
./bustracker hostname      List the URLs the server is reachable at
./bustracker keys          Show the generated secrets (truncated)
./bustracker help          Show all commands
```

---

## Ports

| Port | Service | Access |
|---|---|---|
| 3000 | BusTracker dashboard | Admin (and the apps hit the API) |
| 3001 | Supabase Studio | Database admin UI — keep private |
| 8000 | Supabase API (Kong) | Used by the dashboard and the apps |

Expose 3000 (and your API) to the internet for the apps to reach; keep 3001 private.

> **Running alongside another stack:** BusTracker uses the same ports as some sibling projects (e.g.
> Taximeter). Run only one such stack at a time, or change the published ports before starting.

---

## Backups

```bash
./bustracker backup
```

Writes a timestamped SQL dump to `backups/bustracker_db_<timestamp>.sql`. Copy these somewhere safe
(another disk, object storage). Back up before every update.

Restore:

```bash
./bustracker restore backups/bustracker_db_20260101_120000.sql
./bustracker restart
```

Restore **overwrites** the current database — you'll be asked to confirm.

---

## Updating

```bash
./bustracker update
```

This pulls the latest version (`git pull origin main`), rebuilds the app image, and restarts.
**Back up first.** Database schema changes apply automatically on a fresh database; for existing
installs, review release notes before updating.

---

## Admin accounts

Create another dashboard admin:

```bash
./bustracker add-admin
```

Admin logins are managed by the auth service (GoTrue).

---

## Email (SMTP) — for parent accounts

Parent accounts are **email-verified**, so GoTrue needs an SMTP sender to send verification emails.
Set these in `.env` and restart:

```
SMTP_HOST=smtp.yourprovider.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASS=...
SMTP_SENDER_NAME=YourCompany
SMTP_ADMIN_EMAIL=you@yourcompany.com
```

If SMTP is left blank, GoTrue auto-confirms accounts (fine for a dev/admin-only test, but configure
SMTP before inviting real parents).

---

## Push notifications (FCM / APNs)

Alerts to parents when their app is closed are delivered through Google's and Apple's push gateways,
which need per-app credentials. Keep the credential files under `secrets/` (git-ignored) and point
`.env` at them:

```
PUSH_FCM_CREDENTIALS_FILE=secrets/fcm-service-account.json   # Android (Firebase service account)
PUSH_APNS_KEY_FILE=secrets/apns-key.p8                       # iOS (APNs auth key)
PUSH_APNS_KEY_ID=...
PUSH_APNS_TEAM_ID=...
PUSH_APNS_BUNDLE_ID=...
```

Without push, the live map and in-app updates still work; only closed-app alerts are unavailable.

---

## Data retention & privacy

- The per-run **GPS trail** (`route_point`) is purged after `TRAIL_RETENTION_DAYS` (default 30);
  attendance records (times + places) persist for accountability.
- Student **home locations** and **care notes** are the most sensitive data in the system. They are
  shown only to admins and to the assigned driver during a run, never to any parent.
- See the privacy model for the full access rules (internal docs).

---

## Security

- All secrets (`POSTGRES_PASSWORD`, `JWT_SECRET`, Supabase keys) are generated at install into
  `.env`. **Keep `.env` private** and never commit it — it's git-ignored.
- `docker/kong.yml` is generated from the template with your real keys and is also git-ignored.
- Push credentials under `secrets/` are git-ignored.
- Put the server behind HTTPS (a reverse proxy such as Caddy or Nginx with a certificate) for
  production; phones should pair and sign in over `https://`.
- Keep Supabase Studio (port 3001) off the public internet.

---

## Troubleshooting

**A service keeps restarting.** Check its logs:
```bash
./bustracker logs auth
./bustracker logs rest
./bustracker logs db
```

**`port is already allocated` on 3000/3001/8000/8443.** Another stack (or app) is using those ports.
Stop the other stack first, or change the published ports. BusTracker shares ports with some sibling
projects — run one at a time.

**`password authentication failed` for `supabase_auth_admin` / `authenticator`.** The service roles
weren't created — the database was initialised before the role bootstrap ran. On a fresh install
this is handled automatically; if you hit it, you have stale data: back up anything you need, then
reset the database volume and reinstall:
```bash
docker compose down -v
./bustracker install
```
⚠️ `down -v` **erases the database** — only do this on an install with no data you need.

**`realtime` keeps restarting on `ulimit`.** The container needs a higher open-file limit; this is
set in `docker-compose.yml` (`ulimits: nofile`). Ensure your Docker daemon allows it.

**The build fails on `COPY /app/public`.** Ensure the `public/` folder exists in the repo (it is
committed); a corrupted checkout can drop it.

**Studio shows "unhealthy".** Cosmetic — Studio's healthcheck expects a `pg-meta` service that isn't
part of this stack. Studio still works.

**Can't reach the dashboard from a phone.** The server URL in the pairing QR / parent invite must be
reachable from mobile data, not just your LAN. Use a public address or domain, and open the port /
set up your reverse proxy.

**Check everything is up:**
```bash
./bustracker status
```

---

## Where things live

| Path | What |
|---|---|
| `.env` | All configuration and secrets (git-ignored) |
| `docker/kong.yml` | Generated gateway config (git-ignored) |
| `secrets/` | Push credential files (git-ignored) |
| `supabase/migrations/` | Database schema, run in order on a fresh DB |
| `backups/` | Your database dumps |
