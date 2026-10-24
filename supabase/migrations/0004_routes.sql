-- 0004 — Routes, per-student memberships, service contracts, schedules, calendar.
-- This is the scheduling/assignment layering (see docs/data-model.md, docs/v0.0.0/analysis.md §8):
--   route          — a path serving one school, with a direction (to/from/round)
--   route_stop      — OPERATIONAL: a student's membership in a route, per leg, day-scoped
--   contract        — COMMERCIAL: what the family hired (one-way / round-trip / academy)
--   route_schedule  — default departure times + the days the route runs
--   school_calendar — no-service days

create table route (
  id                  uuid primary key default gen_random_uuid(),
  name                text not null,
  school_id           uuid not null references school(id) on delete restrict,
  direction           text not null check (direction in ('to_school', 'from_school', 'round')),
  -- Academy routes follow the academy's schedule: their runs can be cancelled/retimed per date
  -- without affecting any regular route (the independence rule, docs/requirements.md FR-A4c).
  is_academy          boolean not null default false,
  default_bus_id      uuid references bus(id)     on delete set null,
  default_driver_id   uuid references driver(id)  on delete set null,
  default_monitor_id  uuid references monitor(id) on delete set null,
  active              boolean not null default true,
  created_at          timestamptz not null default now()
);

-- A student's membership in a route, PER LEG. One row per (route, student, leg).
-- The geofenced point defaults to student.home_geog; stop_geog overrides it (e.g. a
-- different drop-off destination on a from_school leg, or a safer pickup corner).
-- days_of_week lets a student ride a leg only on some of the days the route runs
-- (e.g. ride the round route's from_school leg only Mon/Wed/Fri).
create table route_stop (
  id            uuid primary key default gen_random_uuid(),
  route_id      uuid not null references route(id) on delete cascade,
  student_id    uuid not null references student(id) on delete cascade,
  leg           text not null check (leg in ('to_school', 'from_school')),
  seq           integer not null default 0,              -- order within the leg
  days_of_week  integer[] not null default '{1,2,3,4,5}', -- 0=Sun..6=Sat (subset of route's days)
  stop_geog     geography(Point, 4326),                   -- override; default is student.home_geog
  active        boolean not null default true,
  unique (route_id, student_id, leg)
);

-- Enforce that a leg is compatible with the route's direction:
-- a 'round' route carries both legs; a single-direction route only its own leg.
create or replace function route_stop_leg_ok() returns trigger language plpgsql as $$
declare d text;
begin
  select direction into d from route where id = new.route_id;
  if d is null then
    raise exception 'route % not found', new.route_id;
  end if;
  if d <> 'round' and new.leg <> d then
    raise exception 'leg "%" not allowed on a "%" route', new.leg, d;
  end if;
  return new;
end $$;

create trigger trg_route_stop_leg
  before insert or update on route_stop
  for each row execute function route_stop_leg_ok();

-- What the family hired (commercial layer). One contract -> one or more route_stop
-- memberships that fulfil it. The regular and academy contracts coexist.
create table contract (
  id          uuid primary key default gen_random_uuid(),
  student_id  uuid not null references student(id) on delete cascade,
  route_id    uuid not null references route(id) on delete restrict,
  type        text not null check (type in ('one_way_to', 'one_way_from', 'round_trip', 'academy')),
  status      text not null default 'active' check (status in ('active', 'suspended')),
  start_date  date not null default current_date,
  end_date    date,
  notes       text,
  created_at  timestamptz not null default now()
);

-- Default schedule per route. A round route typically sets both times; a return-only
-- route sets only pm. days_of_week is the days the route runs at all (e.g. academy Tue/Thu).
create table route_schedule (
  id                 uuid primary key default gen_random_uuid(),
  route_id           uuid not null references route(id) on delete cascade,
  days_of_week       integer[] not null default '{1,2,3,4,5}',
  am_departure_time  time,
  pm_departure_time  time,
  active             boolean not null default true
);

-- No-service days (holidays). school_id null = company-wide. Suppresses run generation.
create table school_calendar (
  id            uuid primary key default gen_random_uuid(),
  school_id     uuid references school(id) on delete cascade,
  service_date  date not null,
  is_service    boolean not null default false,   -- false = no service that day
  reason        text,
  unique (school_id, service_date)
);
