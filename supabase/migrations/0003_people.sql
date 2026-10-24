-- 0003 — People: guardians (parents/tutors), students (children), and the link.
-- student.home_geog + care_notes are the most sensitive fields in the system
-- (see docs/privacy-and-safety.md). Access is tightly scoped by RLS (0008).

create table guardian (
  id                 uuid primary key default gen_random_uuid(),
  name               text not null,
  phone              text,
  email              text,
  email_verified_at  timestamptz,
  relationship       text check (relationship in ('mother', 'father', 'tutor', 'other')),
  auth_user_id       uuid,          -- GoTrue account (mandatory by default); no FK by design
  status             text not null default 'active' check (status in ('active', 'suspended')),
  created_at         timestamptz not null default now()
);

create table student (
  id             uuid primary key default gen_random_uuid(),
  name           text not null,
  photo_url      text,
  school_id      uuid references school(id) on delete set null,
  grade          text,
  classroom      text,
  home_geog      geography(Point, 4326),   -- SENSITIVE: the default stop / geofence centre
  home_address   text,                     -- SENSITIVE
  care_notes     text,                     -- SENSITIVE: allergies / medical / handling
  status         text not null default 'active' check (status in ('active', 'inactive')),
  enrolled_at    date,
  unenrolled_at  date,
  created_at     timestamptz not null default now()
);

-- Many-to-many: a child may have several guardians; a guardian several children.
create table student_guardian (
  student_id            uuid not null references student(id) on delete cascade,
  guardian_id           uuid not null references guardian(id) on delete cascade,
  relationship          text check (relationship in ('mother', 'father', 'tutor', 'other')),
  is_primary            boolean not null default false,
  can_authorize_pickup  boolean not null default false,
  notify                boolean not null default true,   -- receives alerts for this child
  primary key (student_id, guardian_id)
);
