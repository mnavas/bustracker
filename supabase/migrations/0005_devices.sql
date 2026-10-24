-- 0005 — Paired devices + push tokens.
-- Driver devices are QR-paired and bound to a bus; guardian devices belong to a
-- GoTrue account (see docs/device-pairing.md). Tokens are stored hashed.

create table device (
  id            uuid primary key default gen_random_uuid(),
  kind          text not null check (kind in ('driver', 'guardian')),
  driver_id     uuid references driver(id) on delete cascade,
  guardian_id   uuid references guardian(id) on delete cascade,
  bus_id        uuid references bus(id) on delete set null,   -- for driver devices
  token_hash    text not null,
  paired_at     timestamptz not null default now(),
  last_seen_at  timestamptz,
  revoked       boolean not null default false,
  check (
    (kind = 'driver'   and driver_id   is not null) or
    (kind = 'guardian' and guardian_id is not null)
  )
);

-- FCM/APNs push tokens (one or more per device). Consumed by the push sender.
create table push_token (
  id          uuid primary key default gen_random_uuid(),
  device_id   uuid not null references device(id) on delete cascade,
  platform    text not null check (platform in ('fcm', 'apns')),
  token       text not null,
  active      boolean not null default true,
  updated_at  timestamptz not null default now(),
  unique (platform, token)
);
