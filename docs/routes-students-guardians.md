# Routes, Students & Guardians

Everything about the pieces you manage as the company: schools, buses, drivers, students and their
homes, guardians, routes and their legs, schedules, service contracts, and pairing phones.

---

## Schools, buses, drivers, monitors (Fleet)

In **Fleet** you register the basics:

| Entity | Fields |
|---|---|
| **School** | Name, address, location. A route serves one school. |
| **Bus** | Plate, make/model, color, capacity, photo. Suspend to retire without deleting history. |
| **Driver** | Name, photo, licence, phone. Suspend to block from driving without deleting runs. |
| **Monitor** (optional) | An adult aide who rides along; assignable to a route/run for your records. |

---

## Students and their homes (Students)

Each **student** has:

| Field | Notes |
|---|---|
| Name, photo | Shown to the assigned driver during a run |
| School, grade/classroom | Your records |
| **Home** | Pinned on the map — this is the **stop** the bus drives to, and the point that drives alerts. Get it right: a wrong pin causes late or missed alerts. |
| **Care notes** | Sensitive info the driver needs (e.g. allergy, medical). Keep it minimal. |

A student's home and care notes are the most protected data in the system — shown only to admins and
to the assigned driver during a run, never to any parent.

---

## Guardians (Students → Guardians)

A **guardian** (parent/tutor) has a name, phone, email, and relationship. Link guardians to students:

- A child may have **several guardians**; a guardian may have **several children**.
- Mark who is **primary** and who **may authorise pickup**, and whether each guardian **receives
  alerts** for that child.

Send each guardian an **invite** to the parent app. They create and verify an account (parent
accounts are mandatory by default, so a child's data is never reachable anonymously) and immediately
see their own child(ren) — and nothing else.

---

## Routes and legs (Routes)

A **route** serves one school and has a **direction**:

- **to school** — morning, door-to-door pickups ending at the school,
- **from school** — afternoon, from the school out to each home/destination,
- **round** — both legs (the usual case).

Assign students to a route **per leg**, in a **sequence** (the order the bus visits them):

- The stop defaults to the student's **home**. For a return leg you can set a **different drop-off
  destination** (an academy, a grandparent's, a second home).
- You can scope a membership to certain **days of the week** — e.g. a child rides the round route to
  school every weekday but home only on Mon/Wed/Fri.

> A student can belong to **several routes**. For example: the daily round route, plus a separate
> **return-only** route home on Tue/Thu for the days they attend an academy.

---

## Schedules and the service calendar

- **Schedule** — per route, the days of the week it runs and a departure time per leg. A round route
  usually has both a morning and an afternoon time; a return-only route just the afternoon one.
- **Service calendar** — mark holidays / no-service days so runs aren't generated then.

From the schedule, BusTracker generates the daily **runs** (one per leg, per day the route runs).

---

## Service contracts

A **contract** records what a family hired for a student:

| Type | Meaning |
|---|---|
| **One-way** | To school *or* from school only |
| **Round-trip** | Both legs |
| **Academy** | A return that follows the academy's schedule |

The **academy service follows the academy calendar** — you can cancel or retime an academy run for a
given date (the academy cancelled the session or runs a different activity) **without affecting the
regular route**, which always runs on its own schedule. A child on the academy return that day simply
isn't expected on the regular return and is never flagged as a no-show.

---

## Pairing a bus (QR)

Phones join your server by scanning a QR — no app-store account linking, no central cloud.

1. In **Fleet**, open the bus/driver and generate a **pairing QR**.
2. The driver scans it once in the driver app.
3. The app receives a scoped token and learns which bus it's bound to.

A pairing code is single-use and short-lived; the device token it issues is long-lived but
**revocable** — if a phone is lost, revoke it from the dashboard and re-pair a new one. A driver's
app only ever shows the students on its **current run**, for the **current day**.

---

## Geofence settings

How near is "approaching", and how close counts as "arrived", is set in **Settings**:

| Setting | Default | What it does |
|---|---|---|
| Approach radius | 800 m | Within this distance of a home, parents get the "approaching" alert… |
| Approach ETA | 5 min | …or within this many minutes away, whichever comes first. |
| Arrival radius | 60 m | Within this distance, a pickup/drop-off is recorded… |
| Arrival dwell | 15 s | …once the bus has stayed that close this long (guards against GPS jitter). |

Tune these to your streets — tighter in dense neighbourhoods, looser on fast roads.

> **Availability (v0.0.0):** roster/route/contract screens and QR pairing are being built across
> v0.1; the proximity engine and the mobile apps follow in v0.2–v0.3. This guide describes the full
> product so your setup is ready as each piece lands.
