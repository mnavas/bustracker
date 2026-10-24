-- 0007 — Indexes (geo GiST + hot lookups + retention).

-- Geo (GiST) — distance-to-home, geofence eval, map + trail.
create index idx_student_home_geog   on student      using gist (home_geog);
create index idx_bus_position_geog   on bus_position using gist (geog);
create index idx_route_point_geog    on route_point  using gist (geog);
create index idx_run_stop_stop_geog  on run_stop     using gist (stop_geog);

-- Scheduling / assignment lookups.
create index idx_route_stop_route    on route_stop (route_id, leg, seq);
create index idx_route_stop_student  on route_stop (student_id);
create index idx_contract_student    on contract   (student_id) where status = 'active';

-- Run / attendance.
create index idx_run_route_date      on run        (route_id, service_date, leg);
create index idx_run_status          on run        (status);
create index idx_run_stop_run        on run_stop   (run_id, seq);
create index idx_run_stop_student    on run_stop   (student_id);
create index idx_route_point_run     on route_point (run_id, seq);

-- People / devices / notifications.
create index idx_student_guardian_g  on student_guardian (guardian_id);
create index idx_device_driver       on device     (driver_id);
create index idx_device_guardian     on device     (guardian_id);
create index idx_push_token_device   on push_token (device_id) where active;
create index idx_notification_g      on notification (guardian_id, created_at desc);
create index idx_absence_student     on absence    (student_id, service_date);

-- Retention purge of the GPS trail (delete route_point older than N days).
create index idx_route_point_at      on route_point (at);
