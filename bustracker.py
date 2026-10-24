#!/usr/bin/env python3
"""BusTracker CLI — install, start, stop, update, and manage your company server."""

import base64
import getpass
import hashlib
import hmac
import json
import os
import platform
import re
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path

# ── Platform ──────────────────────────────────────────────────────────────────

def _cmd():
    return "bustracker" if platform.system() == "Windows" else "./bustracker"

# ── Colors ────────────────────────────────────────────────────────────────────

def _supports_color():
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return sys.stdout.isatty()

_COLOR = _supports_color()

def _c(text, code): return f"\033[{code}m{text}\033[0m" if _COLOR else text
def green(t):  return _c(t, "32")
def yellow(t): return _c(t, "33")
def red(t):    return _c(t, "31")
def cyan(t):   return _c(t, "36")
def bold(t):   return _c(t, "1")
def dim(t):    return _c(t, "2")

def ok(msg):      print(green("✓ ") + msg)
def warn(msg):    print(yellow("⚠ ") + msg)
def err(msg):     print(red("✗ ") + msg)
def info(msg):    print(cyan("→ ") + msg)
def step(n, msg): print(f"\n{bold(str(n) + '.')} {msg}")

# ── Helpers ───────────────────────────────────────────────────────────────────

HERE = Path(__file__).parent.resolve()

def run(cmd, check=True):
    subprocess.run(cmd, shell=True, check=check, cwd=HERE)

def run_ok(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, cwd=HERE)
    return r.returncode == 0

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"  {prompt}{suffix}: ").strip()
    return val or default or ""

def ask_password(prompt="Password (min 6 chars)"):
    while True:
        pw = getpass.getpass(f"  {prompt}: ")
        if len(pw) < 6:
            print(f"  {red('Password must be at least 6 characters — try again.')}")
            continue
        pw2 = getpass.getpass(f"  Confirm password: ")
        if pw == pw2:
            return pw
        print(f"  {red('Passwords do not match — try again.')}")

def ask_email(prompt="Admin email"):
    while True:
        email = ask(prompt).strip()
        if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return email
        print(f"  {red('That does not look like a valid email — try again.')}")

def ask_yes(prompt, default=True):
    suffix = "[Y/n]" if default else "[y/N]"
    val = input(f"  {prompt} {suffix} ").strip().lower()
    return (val in ("y", "yes")) if val else default

def pick(prompt, options):
    print(f"\n  {prompt}")
    for i, label in enumerate(options):
        print(f"  {bold(str(i + 1) + '.')} {label}")
    print()
    while True:
        raw = input(f"  Enter number (1–{len(options)}): ").strip()
        try:
            n = int(raw)
            if 1 <= n <= len(options):
                return n - 1
        except ValueError:
            pass
        print(f"  Please enter a number between 1 and {len(options)}.")

# ── JWT generation (pure Python — no Node.js needed on host) ─────────────────

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _make_jwt(payload: dict, secret: str) -> str:
    header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body   = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header}.{body}"
    sig = _b64url(
        hmac.new(secret.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    )
    return f"{signing_input}.{sig}"

def generate_supabase_keys(jwt_secret: str):
    iat = int(time.time())
    exp = iat + 5 * 365 * 24 * 60 * 60
    anon_key    = _make_jwt({"role": "anon",         "iss": "supabase-demo", "iat": iat, "exp": exp}, jwt_secret)
    service_key = _make_jwt({"role": "service_role", "iss": "supabase-demo", "iat": iat, "exp": exp}, jwt_secret)
    return anon_key, service_key

# ── Docker ────────────────────────────────────────────────────────────────────

def ensure_docker():
    if not run_ok("docker --version"):
        err("Docker is not installed.")
        if platform.system() == "Linux":
            if ask_yes("Install Docker now?"):
                info("Running the official Docker install script…")
                run("curl -fsSL https://get.docker.com | sh")
                user = os.environ.get("USER", "")
                if user:
                    run(f"sudo usermod -aG docker {user}", check=False)
                ok("Docker installed.")
                print("  " + dim(f"You may need to log out and back in, then run: {_cmd()} install"))
                sys.exit(0)
        else:
            print(f"  Download Docker Desktop: {cyan('https://www.docker.com/products/docker-desktop/')}")
        sys.exit(1)

    if not run_ok("docker info"):
        err("Docker is installed but not running.")
        if platform.system() == "Linux":
            if ask_yes("Start Docker now?"):
                run("sudo systemctl start docker", check=False)
                time.sleep(2)
                if not run_ok("docker info"):
                    err("Could not start Docker. Try: sudo systemctl start docker")
                    sys.exit(1)
                ok("Docker started.")
                return
        else:
            print("  Please open Docker Desktop and wait for it to start, then try again.")
        sys.exit(1)

    if not run_ok("docker compose version"):
        err("Docker Compose plugin not found. Please update Docker Desktop.")
        sys.exit(1)

    ok("Docker is ready.")

# ── Git ───────────────────────────────────────────────────────────────────────

def ensure_git():
    if run_ok("git --version"):
        ok("Git is ready.")
        return
    err("Git is not installed.")
    print(f"  Install Git from: {cyan('https://git-scm.com/downloads')}")
    sys.exit(1)

# ── Network ───────────────────────────────────────────────────────────────────

def get_local_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("10.254.254.254", 1))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info_t in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ips.add(info_t[4][0])
    except Exception:
        pass
    ips.discard("127.0.0.1")
    return sorted(ips)

# ── .env helpers ──────────────────────────────────────────────────────────────

def _env_file():
    return HERE / ".env"

def _set_env(content: str, key: str, value: str) -> str:
    """Set KEY=value in the .env text (replace in place, else append)."""
    pattern = re.compile(rf"^{re.escape(key)}=.*$", re.MULTILINE)
    if pattern.search(content):
        return pattern.sub(f"{key}={value}", content, count=1)
    sep = "" if content.endswith("\n") else "\n"
    return content + f"{sep}{key}={value}\n"

def _check_installed():
    if not _env_file().exists():
        err("BusTracker is not set up yet.")
        print("  Run " + bold(f"{_cmd()} install") + " first.")
        sys.exit(1)

def _print_urls(app_url=None):
    if app_url:
        base = app_url
        print("  Dashboard: " + bold(cyan(base + "/dashboard")))
        print("  Studio:    " + cyan(base.replace(":3000", ":3001")) + dim("  (admin only — keep private)"))
        return
    ips = get_local_ips()
    if ips:
        base = f"http://{ips[0]}:3000"
        print("  Dashboard: " + bold(cyan(base + "/dashboard")))
        print("  Studio:    " + cyan(f"http://{ips[0]}:3001"))

def _read_env_value(key: str) -> str:
    env = _env_file()
    if not env.exists():
        return ""
    # Last match wins, matching docker-compose's handling of duplicate keys.
    val = ""
    for line in env.read_text().splitlines():
        if line.startswith(f"{key}="):
            val = line[len(key) + 1:].strip()
    return val

def _sql_str(val: str) -> str:
    if not val:
        return "NULL"
    return "'" + val.replace("'", "''") + "'"

def _sql_bool(val: str, default=True) -> str:
    v = str(val).strip().lower()
    if v == "":
        return "true" if default else "false"
    return "true" if v in ("on", "true", "yes", "1") else "false"

def _sql_num(val: str, default: str) -> str:
    try:
        float(val)
        return val
    except (TypeError, ValueError):
        return default

# ── Commands ──────────────────────────────────────────────────────────────────

def _wait_for_supabase(max_wait=120):
    import urllib.request
    app_url = _read_env_value("NEXT_PUBLIC_SUPABASE_URL") or "http://localhost:8000"
    health_url = f"{app_url}/auth/v1/health"
    info("Waiting for Supabase to be ready…")
    for _ in range(max_wait // 3):
        try:
            urllib.request.urlopen(health_url, timeout=2)
            ok("Supabase is ready.")
            return
        except Exception:
            time.sleep(3)
    warn("Supabase did not become ready in time. You may need to run seed/add-admin manually.")


def _company_seed_sql() -> str:
    """INSERT the single company row from .env (idempotent)."""
    name     = _read_env_value("COMPANY_NAME") or "My Transport Company"
    tz       = _read_env_value("COMPANY_TIMEZONE") or "America/Guayaquil"
    contact  = _read_env_value("COMPANY_CONTACT")
    appr_r   = _sql_num(_read_env_value("APPROACH_RADIUS_M"), "800")
    appr_eta = _sql_num(_read_env_value("APPROACH_ETA_MIN"), "5")
    arr_r    = _sql_num(_read_env_value("ARRIVAL_RADIUS_M"), "60")
    arr_dw   = _sql_num(_read_env_value("ARRIVAL_DWELL_S"), "15")
    stale    = _sql_num(_read_env_value("POSITION_STALE_S"), "120")
    n_appr   = _sql_bool(_read_env_value("NOTIFY_ON_APPROACH"))
    n_board  = _sql_bool(_read_env_value("NOTIFY_ON_BOARD"))
    n_drop   = _sql_bool(_read_env_value("NOTIFY_ON_DROP"))
    n_start  = _sql_bool(_read_env_value("NOTIFY_ON_RUN_START"))
    req_acct = _sql_bool(_read_env_value("REQUIRE_GUARDIAN_ACCOUNTS"))
    retain   = _sql_num(_read_env_value("TRAIL_RETENTION_DAYS"), "30")
    return (
        "INSERT INTO company ("
        "  name, timezone, contact,"
        "  approach_radius_m, approach_eta_min, arrival_radius_m, arrival_dwell_s, position_stale_s,"
        "  notify_on_approach, notify_on_board, notify_on_drop, notify_on_run_start,"
        "  require_guardian_accounts, trail_retention_days"
        ") VALUES ("
        f"  {_sql_str(name)}, {_sql_str(tz)}, {_sql_str(contact)},"
        f"  {appr_r}, {appr_eta}, {arr_r}, {arr_dw}, {stale},"
        f"  {n_appr}, {n_board}, {n_drop}, {n_start},"
        f"  {req_acct}, {retain}"
        ") ON CONFLICT (only_one) DO NOTHING;"
    )


def _psql(sql: str, check=True):
    subprocess.run(
        "docker compose exec -T db bash -c 'PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -d postgres'",
        input=sql.encode(), shell=True, check=check, cwd=HERE,
    )


def cmd_seed():
    _check_installed()
    name = _read_env_value("COMPANY_NAME")
    if not name:
        warn("COMPANY_NAME not set in .env — seeding with a default name.")
    _psql(_company_seed_sql())
    ok(f"Company row seeded: {bold(name or 'My Transport Company')}")


# Storage needs post-boot setup: its tables are created by the storage service on
# first start (after initdb), so the bucket, grants, and policies can't live in a
# migration. The role memberships are in 0000_roles.sh; the rest is applied here.
_STORAGE_SQL = """
grant anon, authenticated, service_role to supabase_storage_admin;
grant usage on schema storage to anon, authenticated, service_role;
grant all on all tables in schema storage to anon, authenticated, service_role;
grant all on all sequences in schema storage to anon, authenticated, service_role;
insert into storage.buckets (id, name, public) values ('media','media',true) on conflict (id) do nothing;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='storage' and tablename='objects' and policyname='bt_media_read') then
    create policy bt_media_read on storage.objects for select using (bucket_id='media');
  end if;
  if not exists (select 1 from pg_policies where schemaname='storage' and tablename='objects' and policyname='bt_media_write') then
    create policy bt_media_write on storage.objects for all to authenticated, service_role using (bucket_id='media') with check (bucket_id='media');
  end if;
end $$;
"""


def _storage_setup(check_fail=True):
    try:
        _psql(_STORAGE_SQL)
        ok("Storage configured (media bucket + policies).")
    except Exception as e:
        (warn if not check_fail else err)(f"Storage setup failed: {e}")
        if check_fail:
            sys.exit(1)


def cmd_storage_setup():
    _check_installed()
    _storage_setup()


def _create_admin(email, password, service_key, supa_url):
    import urllib.request, urllib.error
    api_url = f"{supa_url}/auth/v1/admin/users"
    payload = json.dumps({"email": email, "password": password, "email_confirm": True}).encode()
    req = urllib.request.Request(
        api_url, data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {service_key}",
                 "apikey": service_key},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def cmd_add_admin():
    _check_installed()
    print()
    print(bold("Add a dashboard admin account"))
    print()
    email    = ask_email()
    password = ask_password()
    service_key = _read_env_value("SERVICE_ROLE_KEY") or _read_env_value("SUPABASE_SERVICE_ROLE_KEY")
    supa_url    = _read_env_value("NEXT_PUBLIC_SUPABASE_URL") or "http://localhost:8000"
    try:
        data = _create_admin(email, password, service_key, supa_url)
        ok(f"Admin account created: {bold(email)}  (id: {data.get('id', '?')})")
    except Exception as e:
        err(f"Could not create admin account: {e}")
        sys.exit(1)


def cmd_install():
    print(f"\n{bold('BusTracker — Installation')}\n")

    env_file = _env_file()
    if env_file.exists():
        ok("BusTracker is already installed.")
        print("  Run " + bold(f"{_cmd()} start") + "   to start the server.")
        print("  Run " + bold(f"{_cmd()} status") + "  to check containers.")
        return

    step(1, "Checking Docker…")
    ensure_docker()

    env_example = HERE / ".env.example"
    if not env_example.exists():
        err(".env.example not found. Make sure you're in the BusTracker folder.")
        sys.exit(1)

    step(2, "Server URL")
    print(f"  {dim('The address drivers and parents reach this server on.')}")
    ips = get_local_ips()
    url_options = [f"http://{ip}:3000" for ip in ips] + ["http://localhost:3000", "Enter manually"]
    idx = pick("Select the server URL:", url_options)
    if url_options[idx] == "Enter manually":
        app_url = ask("Server URL").rstrip("/")
    else:
        app_url = url_options[idx]
        ok(f"Using: {cyan(app_url)}")

    print()
    step(3, "Company name")
    company_name = ask("Transport company name", default="My Transport Company")

    print()
    step(4, "Admin account")
    print(f"  {dim('The login for the BusTracker dashboard.')}")
    print()
    admin_email    = ask_email()
    admin_password = ask_password()

    # Optional: SMTP for guardian email verification.
    smtp = {}
    print()
    step(5, "Parent email verification (SMTP) — optional")
    print(f"  {dim('Guardian accounts are email-verified. Configure SMTP now, or skip and add later.')}")
    if ask_yes("Configure SMTP now?", default=False):
        smtp["SMTP_HOST"] = ask("SMTP host")
        smtp["SMTP_PORT"] = ask("SMTP port", default="587")
        smtp["SMTP_USER"] = ask("SMTP username")
        smtp["SMTP_PASS"] = getpass.getpass("  SMTP password: ").strip()
        smtp["SMTP_ADMIN_EMAIL"] = admin_email

    # Optional: push credentials (sender lands in v0.3 — paths are recorded now).
    push = {}
    print()
    step(6, "Push notifications — optional")
    print(f"  {dim('Parent alerts when the app is closed (FCM/APNs). Paths are recorded; the')}")
    print(f"  {dim('sender ships in v0.3. Keep credential files under secrets/ (gitignored).')}")
    if ask_yes("Record push credentials now?", default=False):
        push["PUSH_FCM_CREDENTIALS_FILE"] = ask("FCM service-account JSON path", default="secrets/fcm-service-account.json")
        push["PUSH_APNS_KEY_FILE"] = ask("APNs .p8 key path", default="secrets/apns-key.p8")
        push["PUSH_APNS_KEY_ID"] = ask("APNs key ID")
        push["PUSH_APNS_TEAM_ID"] = ask("APNs team ID")
        push["PUSH_APNS_BUNDLE_ID"] = ask("App bundle ID")

    print()
    step(7, "Generating secrets…")
    postgres_password = secrets.token_urlsafe(20)
    jwt_secret        = secrets.token_hex(32)
    internal_secret   = secrets.token_urlsafe(20)
    anon_key, service_key = generate_supabase_keys(jwt_secret)
    ok("Secrets generated (Postgres password, JWT secret, Supabase keys).")

    env_content = (
        env_example.read_text()
        .replace("change-me-strong-password", postgres_password)
        .replace("change-me-at-least-32-chars-random-string", jwt_secret)
        .replace("change-me-random-string", internal_secret)
        .replace("${ANON_KEY}",         anon_key)
        .replace("${SERVICE_ROLE_KEY}", service_key)
        .replace("\nANON_KEY=",         f"\nANON_KEY={anon_key}")
        .replace("\nSERVICE_ROLE_KEY=", f"\nSERVICE_ROLE_KEY={service_key}")
        .replace("http://localhost:3000", app_url)
        .replace("http://localhost:8000", app_url.replace(":3000", ":8000"))
        # Fill the empty placeholders in-place (don't append duplicate keys).
        .replace("\nCOMPANY_NAME=\n", f"\nCOMPANY_NAME={company_name}\n")
        .replace("\nADMIN_EMAIL=\n", f"\nADMIN_EMAIL={admin_email}\n")
    )
    # Optional SMTP → also disable GoTrue autoconfirm so emails are really verified.
    if smtp.get("SMTP_HOST"):
        for k, v in smtp.items():
            env_content = _set_env(env_content, k, v)
        env_content = _set_env(env_content, "GOTRUE_AUTOCONFIRM", "false")
    for k, v in push.items():
        env_content = _set_env(env_content, k, v)

    env_file.write_text(env_content)
    ok(".env saved.")

    kong_template = HERE / "docker" / "kong.yml.template"
    kong_out      = HERE / "docker" / "kong.yml"
    if kong_template.exists():
        kong_out.write_text(
            kong_template.read_text()
            .replace("${SUPABASE_ANON_KEY}",   anon_key)
            .replace("${SUPABASE_SERVICE_KEY}", service_key)
        )
        ok("docker/kong.yml written.")

    step(8, "Building and starting BusTracker…")
    print(f"  {dim('First run downloads images and builds the app — a few minutes.')}")
    run("docker compose up -d --build")

    step(9, "Initializing database…")
    _wait_for_supabase()
    db_ok = True
    try:
        _psql(_company_seed_sql())
        ok("Database initialized (company row seeded).")
    except Exception as e:
        db_ok = False
        warn(f"DB init failed: {e}. Run {bold(_cmd() + ' seed')} later.")

    # Storage setup (bucket + policies live outside migrations — see _storage_setup).
    _storage_setup(check_fail=False)

    step(10, "Creating admin account…")
    admin_ok = True
    try:
        supa_url = app_url.replace(":3000", ":8000") if ":3000" in app_url else "http://localhost:8000"
        _create_admin(admin_email, admin_password, service_key, supa_url)
        ok(f"Admin account created: {bold(admin_email)}")
    except Exception as e:
        admin_ok = False
        warn(f"Could not create admin account: {e}")

    print()
    print("─" * 56)
    ok(bold("BusTracker is running!"))
    print()
    _print_urls(app_url)
    print()
    if not admin_ok:
        warn(bold("The admin account was NOT created."))
        print(f"  Run {bold(_cmd() + ' add-admin')} to create it, then log in.")
        print()
    if not db_ok:
        warn(bold("The database was NOT initialized."))
        print(f"  Run {bold(_cmd() + ' seed')} to initialize it.")
        print()
    print(f"  Run {bold(_cmd() + ' help')} to see all available commands.")
    print()


def cmd_start():
    _check_installed()
    info("Starting BusTracker…")
    run("docker compose up -d")
    print()
    ok(bold("BusTracker started."))
    print()
    _print_urls(_read_env_value("NEXT_PUBLIC_APP_URL"))
    print()


def cmd_stop():
    info("Stopping BusTracker…")
    run("docker compose down")
    ok("BusTracker stopped.")


def cmd_restart():
    _check_installed()
    info("Restarting BusTracker…")
    run("docker compose restart")
    ok(bold("BusTracker restarted."))
    _print_urls(_read_env_value("NEXT_PUBLIC_APP_URL"))


def cmd_logs():
    svc = sys.argv[2] if len(sys.argv) > 2 else ""
    run(f"docker compose logs -f {svc}".strip(), check=False)


def cmd_status():
    run("docker compose ps")


def cmd_update():
    print(f"\n{bold('BusTracker — Update')}\n")
    step(1, "Checking Git…")
    ensure_git()
    step(2, "Pulling latest version…")
    run("git pull origin main")
    step(3, "Rebuilding app image…")
    run("docker compose build bustracker")
    step(4, "Restarting…")
    run("docker compose up -d")
    print()
    ok(bold("BusTracker updated and restarted."))
    _print_urls(_read_env_value("NEXT_PUBLIC_APP_URL"))


def cmd_hostname():
    ips = get_local_ips()
    print()
    if not ips:
        warn("No network addresses detected.")
        return
    print(bold("BusTracker is reachable at:"))
    print()
    for ip in ips:
        print("  Dashboard: " + cyan(f"http://{ip}:3000/dashboard"))
        print("  Studio:    " + cyan(f"http://{ip}:3001"))
        print()
    print(dim("  Studio is for administrators only — don't expose it publicly."))
    print()


def cmd_backup():
    _check_installed()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_dir = HERE / "backups"
    backup_dir.mkdir(exist_ok=True)
    out_file = backup_dir / f"bustracker_db_{timestamp}.sql"
    info(f"Backing up database to {dim(str(out_file))}…")
    run(
        f'docker compose exec -T db bash -c "PGPASSWORD=$POSTGRES_PASSWORD pg_dump -U postgres -d postgres" > "{out_file}"',
        check=False,
    )
    if out_file.exists() and out_file.stat().st_size > 0:
        ok(f"Backup saved: {bold(out_file.name)}")
    else:
        err("Backup failed or produced an empty file.")
        if out_file.exists():
            out_file.unlink()
        sys.exit(1)


def cmd_restore():
    if len(sys.argv) < 3:
        err("Usage: bustracker restore <backup-file.sql>")
        sys.exit(1)
    backup_path = Path(sys.argv[2])
    if not backup_path.exists():
        err(f"File not found: {backup_path}")
        sys.exit(1)
    _check_installed()
    warn(f"This will OVERWRITE the current database with: {bold(backup_path.name)}")
    if not ask_yes("Are you sure?", default=False):
        info("Restore cancelled.")
        return
    info("Restoring database…")
    run(f'docker compose exec -T db bash -c "PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -d postgres" < "{backup_path}"')
    ok("Database restored. Restart BusTracker to apply.")
    print("  " + bold(f"{_cmd()} restart"))


def cmd_keys():
    _check_installed()
    print()
    print(bold("BusTracker — current secrets"))
    print()
    for key in ("POSTGRES_PASSWORD", "JWT_SECRET", "INTERNAL_SECRET",
                "ANON_KEY", "SERVICE_ROLE_KEY"):
        val = _read_env_value(key)
        display = val[:24] + "…" if len(val) > 28 else val
        print(f"  {key:<30} {dim(display)}")
    print()
    print(dim("  Full values are in .env — keep that file private."))
    print()


def cmd_help():
    print(f"""
{bold('BusTracker')} — self-hosted school-bus tracking, attendance & parent alerts

{bold('USAGE')}
  ./bustracker <command>       (Linux / Mac)
  bustracker <command>         (Windows)

{bold('COMMANDS')}
  {green('install')}      First-time setup: server URL, company name, admin account,
                 optional SMTP + push, then builds and starts everything.
  {green('start')}        Start all containers
  {green('stop')}         Stop all containers
  {green('restart')}      Restart all containers
  {green('update')}       Pull the latest version, rebuild the app, and restart
  {green('logs')}         View live logs  (Ctrl+C to stop)
                 Optional: {dim('./bustracker logs bustracker')}  — app only
  {green('status')}       Show container status
  {green('seed')}         Insert/update the company row from .env values
  {green('storage-setup')} Configure the media storage bucket + policies (idempotent)
  {green('add-admin')}    Create a dashboard admin account (email + password)
  {green('backup')}       Dump the database to backups/bustracker_db_<timestamp>.sql
  {green('restore')}      Restore a database backup: {dim('./bustracker restore backups/file.sql')}
  {green('hostname')}     List all URLs where BusTracker is reachable
  {green('keys')}         Show the generated secrets (truncated)
  {green('help')}         Show this message

{bold('PORTS')}
  3000  BusTracker dashboard
  3001  Supabase Studio (admin DB UI — keep private)
  8000  Supabase API (used by the apps)
""")


# ── Entry point ───────────────────────────────────────────────────────────────

COMMANDS = {
    "install":   cmd_install,
    "start":     cmd_start,
    "stop":      cmd_stop,
    "restart":   cmd_restart,
    "logs":      cmd_logs,
    "status":    cmd_status,
    "update":    cmd_update,
    "seed":      cmd_seed,
    "storage-setup": cmd_storage_setup,
    "add-admin": cmd_add_admin,
    "hostname":  cmd_hostname,
    "backup":    cmd_backup,
    "restore":   cmd_restore,
    "keys":      cmd_keys,
    "help":      cmd_help,
    "-h":        cmd_help,
    "--help":    cmd_help,
}

def main():
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)
    cmd = sys.argv[1].lower()
    if cmd not in COMMANDS:
        err(f"Unknown command: {cmd}")
        print("  Run " + bold(f"{_cmd()} help") + " for available commands.")
        sys.exit(1)
    COMMANDS[cmd]()

if __name__ == "__main__":
    main()
