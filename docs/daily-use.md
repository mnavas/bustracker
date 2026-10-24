# Daily Use Guide

How you run the day with BusTracker: monitoring runs, following attendance, handling absences and
incidents, and what parents see.

---

## The dashboard at a glance

After logging in you land on **Overview** — a snapshot of the day: buses on a run, students on
board, active runs, registered students. The left nav takes you to each area:

| Area | What it's for |
|---|---|
| **Live Map** | Every active run — each bus's position, heading, and when it last reported in |
| **Runs & Attendance** | Live per-run attendance, plus run history |
| **Fleet** | Schools, buses, drivers, monitors |
| **Students** | Students, their homes, and their guardians |
| **Routes** | Routes, legs, schedules, and service contracts |
| **Reports** | On-time performance, attendance, per-driver summaries |
| **Settings** | Company info, geofence thresholds, notifications, accounts, retention |

---

## Monitoring runs (Live Map)

Each active run shows on the map with:

- The bus's **current position** and heading,
- A **last-update time** so you can spot a phone that has dropped off the network,
- Its **progress** along the route (stops done / pending).

Positions update as the bus moves; a stale timestamp usually means the driver lost signal — run data
is not lost, it syncs when the phone reconnects.

---

## How a run works

1. The driver sees the day's assigned **runs** and **starts** one when setting off. The bus then
   streams its location, and the driver just drives.
2. For a **from-school** run (everyone boards at the school) the driver first confirms the expected
   students are aboard ("all aboard"), then starts the route.
3. As the bus reaches each child's home, BusTracker records the **pickup** (morning) or **drop-off**
   (afternoon) **automatically, from the bus's distance to the home** — no scanning, no roll-call.
4. If a child isn't there, the driver marks a **no-show**; if something goes wrong, they report an
   **incident** (breakdown, delay, …).
5. The driver **ends** the run when it's complete.

> Because attendance comes from distance (the driver is focused on driving, not tapping), alerts can
> occasionally be a little late — a known trade-off tuned by the approach/arrival settings.

---

## Attendance

**Runs & Attendance** shows each run's board live: every student moving through *pending →
approaching → on board → dropped off* (or *absent* / *no-show*). Run history keeps the bus's route
trail and the time + place of each pickup and drop-off, so "did my child get picked up?" is always
answerable from stored data.

---

## What parents see

- When a run starts, parents of children on it can **track that bus live**. A parent can follow **any
  route their child is assigned to while it is active** — e.g. the daily round trip every day (even
  when the child isn't aboard that day) and an academy return whenever it runs.
- On days the child actually rides, the parent also sees a **live ETA to their home/stop**.
- Parents get **push alerts** (when enabled): bus **approaching**, child **on board**, child
  **dropped off**, plus run-started and delay/incident notices.
- A parent only ever sees a **bus position** for their own child's assigned routes — never other
  children, other homes, or the wider fleet.

---

## Absences

A parent can report that their child **won't ride** — this morning, this afternoon, or all day. That
removes the child from the driver's list and from proximity evaluation for that run, so no false
"where's my child?" expectation and no unnecessary alerts. The parent gets an acknowledgement.

---

## Incidents & delays

When a driver reports an incident (breakdown, accident, traffic delay, road closure, medical), you're
alerted on the dashboard and can **broadcast** a short message (e.g. "running ~15 min late") to the
guardians of that run.

---

## Reports

Open **Reports** to see, for any date range:

- **On-time performance** — scheduled vs. actual pickup/drop-off,
- **Attendance** — per student and per route,
- **Run durations**, and
- **Per-driver** summaries.

---

## A normal day

1. Drivers **start** their morning runs; buses appear on your Live Map.
2. Pickups record automatically as each bus reaches each home; parents get their alerts.
3. You watch the map and the attendance board, and handle any absences or incidents.
4. Afternoon runs reverse the flow — drop-offs at home (or the contracted destination).
5. At day's end (or any range), you pull reports.

> **Availability (v0.0.0):** the stack, CLI, schema, and dashboard skeleton are in place. The live
> map, roster/route screens, the proximity engine, parent alerts, and the two mobile apps roll out
> across v0.1+. This guide describes the full workflow end to end.
