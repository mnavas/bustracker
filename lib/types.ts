// Shared TypeScript types aligned with supabase/migrations/. Conceptual — expand
// as the dashboard/apps are built (v0.1+). See docs/data-model.md.

export type Leg = "to_school" | "from_school";
export type RouteDirection = "to_school" | "from_school" | "round";
export type ContractType = "one_way_to" | "one_way_from" | "round_trip" | "academy";
export type RunStatus = "planned" | "boarding" | "active" | "completed" | "cancelled";
export type RunStopStatus =
  | "pending"
  | "approaching"
  | "onboard"
  | "dropped"
  | "absent"
  | "no_show"
  | "skipped";

export interface Company {
  id: string;
  name: string;
  timezone: string;
  contact: string | null;
  approach_radius_m: number;
  approach_eta_min: number;
  arrival_radius_m: number;
  arrival_dwell_s: number;
  position_stale_s: number;
  notify_on_approach: boolean;
  notify_on_board: boolean;
  notify_on_drop: boolean;
  notify_on_run_start: boolean;
  require_guardian_accounts: boolean;
  trail_retention_days: number;
}

export interface School {
  id: string;
  name: string;
  address: string | null;
}

export interface Bus {
  id: string;
  plate: string;
  make: string | null;
  model: string | null;
  color: string | null;
  capacity: number | null;
  status: "active" | "suspended";
  current_driver_id: string | null;
}

export interface Driver {
  id: string;
  name: string;
  licence_no: string | null;
  phone: string | null;
  status: "active" | "suspended";
}

export interface Student {
  id: string;
  name: string;
  school_id: string | null;
  grade: string | null;
  classroom: string | null;
  home_address: string | null;
  care_notes: string | null;
  status: "active" | "inactive";
}

export interface Guardian {
  id: string;
  name: string;
  phone: string | null;
  email: string | null;
  relationship: "mother" | "father" | "tutor" | "other" | null;
  status: "active" | "suspended";
}

export interface Route {
  id: string;
  name: string;
  school_id: string;
  direction: RouteDirection;
  is_academy: boolean;
  active: boolean;
}

export interface RouteStop {
  id: string;
  route_id: string;
  student_id: string;
  leg: Leg;
  seq: number;
  days_of_week: number[];
  active: boolean;
}

export interface Contract {
  id: string;
  student_id: string;
  route_id: string;
  type: ContractType;
  status: "active" | "suspended";
  start_date: string;
  end_date: string | null;
}

export interface Run {
  id: string;
  route_id: string;
  bus_id: string | null;
  driver_id: string | null;
  service_date: string;
  leg: Leg;
  status: RunStatus;
  started_at: string | null;
  ended_at: string | null;
}

export interface RunStop {
  id: string;
  run_id: string;
  student_id: string;
  seq: number;
  status: RunStopStatus;
  boarded_at: string | null;
  dropped_at: string | null;
}
