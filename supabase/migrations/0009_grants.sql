-- 0009 — Table privileges for the Supabase roles.
-- RLS governs row visibility, but PostgreSQL still requires base GRANTs. anon/authenticated
-- remain restricted by RLS (no policies for anon → denied; authenticated gets admin_all for
-- now), while service_role additionally bypasses RLS. Runs after all tables exist.

grant usage on schema public to anon, authenticated, service_role;

grant all privileges on all tables    in schema public to anon, authenticated, service_role;
grant all privileges on all sequences in schema public to anon, authenticated, service_role;
grant all privileges on all functions in schema public to anon, authenticated, service_role;

alter default privileges in schema public grant all on tables    to anon, authenticated, service_role;
alter default privileges in schema public grant all on sequences to anon, authenticated, service_role;
alter default privileges in schema public grant all on functions to anon, authenticated, service_role;
