# BusTracker

**Self-hosted school-bus tracking and attendance platform. One installation = one school-transport company.**

A school-transport company clones this repository, starts Docker, and immediately has its own server
to register its buses, routes, students and guardians, run the daily pickups and drop-offs, and give
every parent live visibility of the bus carrying their child. Drivers and parents use two dedicated
mobile apps that sync to *that company's* server.

> **Open server, free to self-host.** This server platform is MIT licensed — run it yourself at no
> cost. The companion driver and parent apps are not included in this repository.

---

## The three pieces

| Piece | What it is | Who runs it |
|---|---|---|
| **Server** | Docker Compose stack: web dashboard + database + realtime + push + API | The transport company (self-hosted) |
| **Driver app** | Mobile app — start/end a run, follow the ordered home-by-home route, auto-log boardings, report incidents | Each driver |
| **Parent app** | Mobile app — track the assigned bus live, get "bus approaching / child on board / child dropped off" alerts, report absences | Each parent/tutor |

A phone pairs to a company's server by scanning a **QR code** — no app-store account linking, no
central cloud. Each install is an island; each company owns its children's data.

---

## The model: door-to-door, driven by distance to home

BusTracker is built for **door-to-door** school transport — the bus visits each child's home in turn.
A child's **home is the stop**, and the bus's **distance to that home** is what drives everything:

- As the bus gets near a child's home, the parent is alerted that it is **approaching**.
- When the bus reaches the home, the child's **pickup** (morning) or **drop-off** (afternoon) is
  recorded automatically and the parent is notified.

No scanning, no badges, no manual roll-call.

---

## What the company gets

- **Live fleet monitoring** — every active run on a map, each bus's position and last-update time.
- **Parent peace of mind** — each parent can live-track the bus on *their* child's routes, with a
  live ETA to the child's stop on days they ride, plus push alerts on approach, boarding, and drop-off.
- **Automatic attendance** — who was picked up and dropped off, when and where, recorded per run.
- **Absence reporting** — parents flag "not riding today" in advance; the driver's list updates.
- **Accountability** — on-time performance, run history with the bus's route trail, incident log.

---

## Documentation

| Guide | For |
|---|---|
| [Installation & First-Time Setup](docs/install.md) | Standing up your server and configuring your company |
| [Daily Use](docs/daily-use.md) | Running the day: fleet map, live runs, attendance, incidents |
| [Routes, Students & Guardians](docs/routes-students-guardians.md) | Buses, drivers, students, homes, routes, QR pairing |
| [Administration & Maintenance](docs/admin.md) | Backups, updates, push/SMTP setup, troubleshooting, CLI |

---

## Status

Early development (v0.0.0): the self-hosted Docker stack, management CLI, database schema, and the
admin dashboard skeleton are the first milestone. Routes, the proximity engine, parent alerts, and
the two mobile apps follow in v0.1+.

---

## License

The server platform (this repository) is **MIT licensed** — see [LICENSE](LICENSE).

The driver and parent apps are not included in this repository.
