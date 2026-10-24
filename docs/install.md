# Installation & First-Time Setup

This guide walks you through installing BusTracker and getting your company server ready. No
programming knowledge required.

> **One install = one transport company.** Everything runs on your own server; there is no shared
> cloud, and the children's data never leaves your infrastructure.

---

## What you need

### The server

BusTracker runs in Docker on any machine that stays on 24/7. Because drivers and parents connect
over the internet, the server must be **reachable from outside your local network** — a small VPS
(cloud server) with a public address is the simplest option, or an on-premises machine with a fixed
public IP / port-forwarding.

| | Minimum | Recommended |
|---|---|---|
| RAM | 4 GB | 8 GB |
| Storage | 20 GB free | 40 GB free |
| System | Ubuntu 22, Debian 12, or any Docker host | A small cloud VPS |
| Network | A public address drivers/parents can reach | A domain name + HTTPS |

### Reachability

- Drivers pair their phones to your server by scanning a **QR code** that contains your server URL,
  so that URL must work from a phone on mobile data — not just your office WiFi.
- Parents sign in to their accounts in the parent app, which also needs to reach your server.
- A domain name (e.g. `bus.micolegio.com`) with HTTPS is strongly recommended for production.
- For a first test you can run everything on your laptop and reach it at `http://localhost:3000`.

> **Tip:** Give the server a fixed address (static IP or a domain) so pairing QR codes and parent
> sign-ins never stop working.

---

## Step 1 — Download BusTracker

Open a terminal on the server and run:

```bash
git clone https://github.com/mnavas/bustracker
cd bustracker
```

The server platform is free and open source (MIT). If you don't have Git, download the ZIP from
GitHub and extract it to a folder named `bustracker`.

---

## Step 2 — Run the install wizard

**Linux / Mac:**
```bash
./bustracker install
```

**Windows:**
```
bustracker install
```

The wizard asks a few questions, then does everything automatically:

**Question 1 — Server URL**
It shows a numbered list of your machine's addresses. Pick the one drivers and parents will reach
(for a cloud server, the public address or your domain). If unsure on a laptop test, pick
`http://localhost:3000`.

**Question 2 — Company name**
Shown in the dashboard and the apps. You can change it later in Settings.

**Question 3 — Admin email and password**
Your login for the BusTracker dashboard. Use a real email you own; the password must be at least 6
characters and is entered twice to confirm.

**Question 4 — Email verification (SMTP) — optional**
Parent accounts are email-verified. You can configure SMTP now or skip and add it later (see
[admin.md](admin.md)). You can skip this for a first test.

**Question 5 — Push notifications — optional**
Alerts to parents when their app is closed use FCM (Android) and APNs (iOS). You can record the
credentials now or add them later. Skip this for a first test — the live map and in-app updates work
without push.

After answering, the wizard:
- Installs Docker if needed (first time only),
- Builds and starts all services (a few minutes the first time),
- Creates the database, your company, and your admin account.

When it finishes you'll see something like:

```
✓ BusTracker is running!

  Dashboard: http://your-server:3000/dashboard
  Studio:    http://your-server:3001
```

Open the Dashboard link and log in.

---

## Step 3 — Configure your company

Go to **Settings** in the dashboard. Everything here is yours to control:

| Setting | What it does |
|---|---|
| **Company info** | Name, timezone, contact. |
| **Approach radius / ETA** | How near the bus must be to a child's home before parents get the "approaching" alert (default 800 m, or 5 minutes away). |
| **Arrival radius / dwell** | How close (and for how long) the bus must be to the home to record a pickup/drop-off (default 60 m, 15 s). |
| **Notifications** | Which events alert parents: approaching, on board, dropped off, run started. |
| **Require guardian accounts** | On by default — children's data is only reachable through a verified parent account. |
| **Trail retention** | How many days the per-run GPS trail is kept before it is purged (default 30). |

> Parent accounts are email-verified. Configure SMTP so verification emails can be sent — see
> [admin.md](admin.md).

---

## Step 4 — Register schools, buses and drivers

Go to **Fleet**:

- **Schools** — the schools you serve (name, address, location).
- **Buses** — plate, make/model, color, capacity, photo.
- **Drivers** — name, photo, licence, phone. (Optionally register **monitors/aides** who ride along.)

---

## Step 5 — Register students and guardians

Go to **Students**:

- **Students** — name, photo, school, grade, and their **home pinned on the map** (this home is the
  stop the bus drives to, and the point that drives alerts). Add any **care notes** the driver needs
  (e.g. an allergy).
- **Guardians** — each parent/tutor's name, phone, email, and relationship. Link guardians to their
  children (a child can have several guardians; a guardian several children), and send each an
  **invite** to the parent app.

See [routes-students-guardians.md](routes-students-guardians.md).

---

## Step 6 — Build routes, schedules and contracts

Go to **Routes**:

- Create a **route** serving one school, with a **direction**: *to school*, *from school*, or
  *round* (both).
- Assign students to the route **per leg**, in pickup order. Each student's home is their stop; you
  can set a **different drop-off destination** for a return leg, and limit a student to certain
  **days of the week**.
- Set the **schedule** (days + departure times) and mark holidays on the **service calendar**.
- Record each student's **service contract** (one-way, round-trip, or an academy return that follows
  the academy schedule).

See [routes-students-guardians.md](routes-students-guardians.md).

---

## Step 7 — Pair buses and invite parents

- Generate a **pairing QR** for each bus/driver. The driver scans it once in the driver app to link
  their phone to your server and their bus.
- Send each guardian their **parent-app invite**; they create/verify their account and immediately
  see their own child(ren).

---

## Step 8 — Test before going live

1. Open the Dashboard and confirm your schools, buses, drivers, students, routes and schedules look
   right.
2. Pair one driver phone, start a run, and confirm the bus appears on the **Live Map** with a recent
   update time.
3. From a parent account, confirm you can see that run's bus and (on a day the child rides) an ETA to
   the home.
4. Drive near a seeded home and confirm the approach/arrival events are recorded under
   **Runs & Attendance**.

---

## Auto-start on boot

All services use `restart: unless-stopped`, so BusTracker comes back automatically after a reboot or
power loss. Wait a couple of minutes after the machine starts, then check the Dashboard.

---

## Where to next

- Running the day-to-day → [daily-use.md](daily-use.md)
- Schools, buses, students, guardians, routes, contracts, pairing → [routes-students-guardians.md](routes-students-guardians.md)
- Backups, updates, SMTP, push, troubleshooting, CLI → [admin.md](admin.md)

> **Note on availability (v0.0.0):** the self-hosted stack, the management CLI, the full database
> schema, and the admin dashboard skeleton are in place. The roster/route screens, the proximity
> engine, parent alerts, and the two mobile apps roll out across v0.1+. This guide describes the full
> product so your setup is ready as each piece lands.
