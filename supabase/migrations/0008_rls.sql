-- 0008 — Row-Level Security
--
-- v0.0.0 policy: enable RLS everywhere; grant the logged-in admin (role `authenticated`)
-- full access. `service_role` bypasses RLS (server-side use). `anon` has no table access.
--
-- The guardian/driver-scoped policies are the SAFETY-CRITICAL part of this product
-- (docs/privacy-and-safety.md §2–3) and are intentionally NOT enabled yet — they are
-- designed as the TODO below and must be prototyped/tested before the apps ship (v0.1,
-- risk R2). Until then only admins (authenticated) and the server (service_role) touch data.

do $$
declare t text;
begin
  foreach t in array array[
    'company','school','driver','monitor','bus',
    'guardian','student','student_guardian',
    'route','route_stop','contract','route_schedule','school_calendar',
    'device','push_token',
    'run','bus_position','route_point','run_stop','absence','geofence_event',
    'incident','notification'
  ]
  loop
    execute format('alter table %I enable row level security;', t);
    execute format(
      'create policy admin_all on %I for all to authenticated using (true) with check (true);', t);
  end loop;
end $$;

-- ────────────────────────────────────────────────────────────────────────────
-- TODO (v0.1) — device/account-scoped policies. Target behaviour:
--
--  GUARDIAN (GoTrue account, joined via guardian.auth_user_id -> student_guardian):
--    • read only their own children (student via student_guardian) and derived data
--      (run_stop/attendance, notifications addressed to them);
--    • read a bus_position ONLY for a route their child is ASSIGNED to (route_stop)
--      that currently has an `active` run — assignment-scoped, NOT gated on the child
--      riding that day (so the daily main round trip is visible even on academy days);
--    • NEVER read: student.home_geog/home_address/care_notes of any child, other
--      children, other routes' stops, or the wider fleet;
--    • alerts/personal ETA are additionally gated on the child's own run_stop for the day.
--
--  DRIVER (device token, joined via device -> bus):
--    • read only the run_stop/student rows of a run whose bus_id = the device's bus and
--      service_date = today and status in ('boarding','active') — current run only;
--    • read those students' home/stop/care_notes (needed to drive the run safely);
--    • write only its own bus's bus_position/route_point and its run's run_stop/geofence_event.
--
-- Prototype these against seed data (docs/v0.0.0/analysis.md R2) before enabling.
-- ────────────────────────────────────────────────────────────────────────────
