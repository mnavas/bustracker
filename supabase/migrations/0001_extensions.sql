-- 0001 — Extensions
-- PostGIS powers all geo work (distance-to-home, geofence crossings, ETA, map queries).
create extension if not exists postgis;
create extension if not exists pgcrypto;
