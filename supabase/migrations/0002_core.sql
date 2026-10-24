-- 0002 — Core entities: company (single row), school, driver, monitor, bus.
-- Single-tenant: the whole database is one company.

create table company (
  id                         uuid primary key default gen_random_uuid(),
  only_one                   boolean not null default true unique check (only_one),
  name                       text not null,
  logo_url                   text,
  timezone                   text not null default 'America/Guayaquil',
  contact                    text,
  pairing_secret             text not null default encode(gen_random_bytes(16), 'hex'),
  -- Geofencing (the distance-to-home engine; see docs/geofencing.md)
  approach_radius_m          integer not null default 800,
  approach_eta_min           integer not null default 5,
  arrival_radius_m           integer not null default 60,
  arrival_dwell_s            integer not null default 15,
  position_stale_s           integer not null default 120,
  -- Notifications (see docs/notifications.md)
  notify_on_approach         boolean not null default true,
  notify_on_board            boolean not null default true,
  notify_on_drop             boolean not null default true,
  notify_on_run_start        boolean not null default true,
  quiet_hours_start          time,
  quiet_hours_end            time,
  -- Accounts: guardian accounts are mandatory by default (children's data).
  require_guardian_accounts  boolean not null default true,
  -- Retention: GPS trail (route_point) is purged after this many days.
  trail_retention_days       integer not null default 30,
  created_at                 timestamptz not null default now()
);

create table school (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  address     text,
  geog        geography(Point, 4326),   -- school location (destination/origin anchor)
  contact     text,
  created_at  timestamptz not null default now()
);

create table driver (
  id            uuid primary key default gen_random_uuid(),
  name          text not null,
  photo_url     text,
  licence_no    text,
  phone         text,
  status        text not null default 'active' check (status in ('active', 'suspended')),
  auth_user_id  uuid,              -- optional GoTrue login; no FK by design
  created_at    timestamptz not null default now()
);

create table monitor (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  phone       text,
  photo_url   text,
  status      text not null default 'active' check (status in ('active', 'suspended')),
  created_at  timestamptz not null default now()
);

create table bus (
  id                 uuid primary key default gen_random_uuid(),
  plate              text not null,
  make               text,
  model              text,
  color              text,
  capacity           integer,
  photo_url          text,
  status             text not null default 'active' check (status in ('active', 'suspended')),
  current_driver_id  uuid references driver(id) on delete set null,
  created_at         timestamptz not null default now()
);
