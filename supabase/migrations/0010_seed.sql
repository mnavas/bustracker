-- 0010 — Seed example domain data so the dashboard shell has something to show and the
-- route/membership/contract/run layering is demonstrated end-to-end.
--
-- Encodes the real worked example (docs/v0.0.0/analysis.md §8): a child on a daily ROUND
-- route (to school Mon–Fri, home Mon/Wed/Fri) PLUS a Tue/Thu ACADEMY return to a different
-- destination. The `company` row itself is seeded from .env by `./bustracker install`.
-- Coordinates are near Guayaquil (lng, lat).

do $$
declare
  v_school   uuid;
  v_bus      uuid;
  v_driver   uuid;
  v_student  uuid;
  v_guardian uuid;
  v_round    uuid;   -- round route (to school + home)
  v_academy  uuid;   -- from_school-only academy return
begin
  insert into school (name, address, geog)
    values ('Colegio Demo', 'Av. Principal 100',
            ST_SetSRID(ST_MakePoint(-79.9000, -2.1700), 4326)::geography)
    returning id into v_school;

  insert into driver (name, licence_no, phone)
    values ('Carlos Ruiz', 'EC-123456', '+593990000001') returning id into v_driver;

  insert into bus (plate, make, model, color, capacity, current_driver_id)
    values ('GAB-1234', 'Toyota', 'Hiace', 'white', 18, v_driver) returning id into v_bus;

  insert into student (name, school_id, grade, home_geog, home_address, care_notes)
    values ('Ana Pérez', v_school, '4B',
            ST_SetSRID(ST_MakePoint(-79.9120, -2.1600), 4326)::geography,
            'Calle Los Ceibos 45', 'Peanut allergy')
    returning id into v_student;

  insert into guardian (name, phone, email, relationship)
    values ('María Pérez', '+593990000002', 'maria@example.com', 'mother')
    returning id into v_guardian;

  insert into student_guardian (student_id, guardian_id, relationship, is_primary,
                                can_authorize_pickup, notify)
    values (v_student, v_guardian, 'mother', true, true, true);

  -- Routes ------------------------------------------------------------------
  insert into route (name, school_id, direction, is_academy, default_bus_id, default_driver_id)
    values ('Ruta A', v_school, 'round', false, v_bus, v_driver) returning id into v_round;

  insert into route (name, school_id, direction, is_academy, default_bus_id, default_driver_id)
    values ('Academia PM', v_school, 'from_school', true, v_bus, v_driver)
    returning id into v_academy;

  -- Schedules: round runs Mon–Fri (am+pm); academy runs Tue/Thu (pm only) ----
  insert into route_schedule (route_id, days_of_week, am_departure_time, pm_departure_time)
    values (v_round, '{1,2,3,4,5}', '06:30', '13:30');
  insert into route_schedule (route_id, days_of_week, pm_departure_time)
    values (v_academy, '{2,4}', '17:30');

  -- Contracts (commercial layer): a round-trip + an academy service ----------
  insert into contract (student_id, route_id, type) values (v_student, v_round,   'round_trip');
  insert into contract (student_id, route_id, type) values (v_student, v_academy, 'academy');

  -- Memberships (operational layer) that FULFIL the contracts ----------------
  -- To school: every weekday on the round route.
  insert into route_stop (route_id, student_id, leg, seq, days_of_week)
    values (v_round, v_student, 'to_school', 1, '{1,2,3,4,5}');
  -- Home: on the round route ONLY Mon/Wed/Fri (Tue/Thu she takes the academy return).
  insert into route_stop (route_id, student_id, leg, seq, days_of_week)
    values (v_round, v_student, 'from_school', 1, '{1,3,5}');
  -- Academy return Tue/Thu, dropped at a DIFFERENT destination (grandparent's) via stop_geog.
  insert into route_stop (route_id, student_id, leg, seq, days_of_week, stop_geog)
    values (v_academy, v_student, 'from_school', 1, '{2,4}',
            ST_SetSRID(ST_MakePoint(-79.9050, -2.1555), 4326)::geography);
end $$;
