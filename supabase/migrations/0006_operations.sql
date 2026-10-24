-- 0006 — Operational: runs, live positions, trail, attendance, proximity events,
-- absences, incidents, notifications.

-- A scheduled execution of one route LEG on a date. A round route yields up to two
-- runs per date (to_school + from_school); an academy route yields a from_school run
-- on its (adjustable) days. 'boarding' = the all-aboard muster before 'active'.
create table run (
  id           uuid primary key default gen_random_uuid(),
  route_id     uuid not null references route(id) on delete restrict,
  bus_id       uuid references bus(id)     on delete set null,
  driver_id    uuid references driver(id)  on delete set null,
  monitor_id   uuid references monitor(id) on delete set null,
  service_date date not null,
  leg          text not null check (leg in ('to_school', 'from_school')),
  status       text not null default 'planned'
                 check (status in ('planned', 'boarding', 'active', 'completed', 'cancelled')),
  started_at   timestamptz,
  ended_at     timestamptz,
  created_at   timestamptz not null default now(),
  unique (route_id, service_date, leg)
);

-- Latest known position per bus (the live map + the proximity engine read this).
create table bus_position (
  bus_id      uuid primary key references bus(id) on delete cascade,
  geog        geography(Point, 4326) not null,
  heading     numeric,
  speed       numeric,                      -- km/h
  on_run      boolean not null default false,
  run_id      uuid references run(id) on delete set null,
  updated_at  timestamptz not null default now()
);

-- Ordered polyline of a run (append-only). Purged after company.trail_retention_days.
create table route_point (
  id       bigserial primary key,
  run_id   uuid not null references run(id) on delete cascade,
  seq      integer not null,
  geog     geography(Point, 4326) not null,
  speed    numeric,
  at       timestamptz not null default now()
);

-- Guardian-reported absence. Pre-marks the matching run_stop skipped/absent and
-- suppresses proximity evaluation + alerts for that student/day.
create table absence (
  id                        uuid primary key default gen_random_uuid(),
  student_id                uuid not null references student(id) on delete cascade,
  service_date              date not null,
  shift                     text not null check (shift in ('am', 'pm', 'both')),
  reason                    text check (reason in ('sick', 'travel', 'other')),
  note                      text,
  reported_by_guardian_id   uuid references guardian(id) on delete set null,
  created_at                timestamptz not null default now()
);

-- Per student per run — the attendance + progress record. Generated from the
-- route_stop memberships whose leg + days_of_week match the run. The distance engine
-- advances status; a from_school leg's single-origin muster sets 'onboard' up front.
create table run_stop (
  id                    uuid primary key default gen_random_uuid(),
  run_id                uuid not null references run(id) on delete cascade,
  student_id            uuid not null references student(id) on delete cascade,
  seq                   integer not null default 0,
  stop_geog             geography(Point, 4326),   -- resolved at generation (override or home)
  status                text not null default 'pending'
                          check (status in ('pending', 'approaching', 'onboard',
                                            'dropped', 'absent', 'no_show', 'skipped')),
  approach_notified_at  timestamptz,
  boarded_at            timestamptz,
  boarded_geog          geography(Point, 4326),
  dropped_at            timestamptz,
  dropped_geog          geography(Point, 4326),
  closest_distance_m    numeric,
  exception_id          uuid references absence(id) on delete set null,
  unique (run_id, student_id)
);

-- Idempotent proximity latch: one row per (run, student, kind) guarantees a
-- threshold crossing fires exactly once (see docs/geofencing.md §4).
create table geofence_event (
  id          bigserial primary key,
  run_id      uuid not null references run(id) on delete cascade,
  student_id  uuid not null references student(id) on delete cascade,
  kind        text not null check (kind in ('approach_enter', 'arrival_enter', 'arrival_exit')),
  geog        geography(Point, 4326),
  distance_m  numeric,
  at          timestamptz not null default now(),
  unique (run_id, student_id, kind)
);

-- Driver-reported incident on a run.
create table incident (
  id           uuid primary key default gen_random_uuid(),
  run_id       uuid references run(id) on delete set null,
  driver_id    uuid references driver(id) on delete set null,
  kind         text not null check (kind in ('breakdown', 'accident', 'traffic_delay',
                                             'road_closure', 'medical', 'other')),
  note         text,
  geog         geography(Point, 4326),
  created_at   timestamptz not null default now(),
  resolved_at  timestamptz
);

-- Outbound notification log (every alert, for audit + delivery debugging).
create table notification (
  id          uuid primary key default gen_random_uuid(),
  guardian_id uuid references guardian(id) on delete cascade,
  student_id  uuid references student(id) on delete set null,
  run_id      uuid references run(id) on delete set null,
  kind        text not null check (kind in ('bus_approaching', 'child_boarded', 'child_dropped',
                                            'run_started', 'run_delayed', 'run_cancelled',
                                            'absence_ack', 'incident', 'admin_broadcast')),
  channel     text not null check (channel in ('push', 'inapp', 'sms')),
  payload     jsonb,
  status      text not null default 'queued' check (status in ('queued', 'sent', 'failed')),
  sent_at     timestamptz,
  created_at  timestamptz not null default now()
);
