const STATS = [
  { label: "Buses on a run", value: "—" },
  { label: "Students on board", value: "—" },
  { label: "Active runs", value: "—" },
  { label: "Registered students", value: "—" },
];

export default function DashboardOverview() {
  return (
    <section>
      <h1 style={{ fontSize: 24, margin: "0 0 4px" }}>Overview</h1>
      <p className="bt-muted" style={{ marginTop: 0 }}>
        Your fleet at a glance. Live numbers appear once the driver app comes online (v0.2) and the
        proximity engine lands (v0.3).
      </p>

      <div
        style={{
          display: "grid",
          gap: 14,
          gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          marginTop: 18,
        }}
      >
        {STATS.map((s) => (
          <div key={s.label} className="bt-card" style={{ padding: 18 }}>
            <div style={{ fontSize: 30, fontWeight: 700 }}>{s.value}</div>
            <div className="bt-muted" style={{ fontSize: 13, marginTop: 4 }}>
              {s.label}
            </div>
          </div>
        ))}
      </div>

      <div className="bt-card" style={{ padding: 22, marginTop: 18 }}>
        <h2 style={{ fontSize: 16, margin: "0 0 8px" }}>Getting started</h2>
        <ol
          className="bt-muted"
          style={{ margin: 0, paddingLeft: 18, lineHeight: 1.7, fontSize: 14 }}
        >
          <li>
            Add your <strong>schools</strong>, <strong>buses</strong> and <strong>drivers</strong> in{" "}
            <strong>Fleet</strong>.
          </li>
          <li>
            Register <strong>students</strong> (with their home on the map) and their{" "}
            <strong>guardians</strong>.
          </li>
          <li>
            Build <strong>routes</strong>, assign students per leg, and pair each bus by QR. Watch the{" "}
            <strong>Live Map</strong> as runs begin.
          </li>
        </ol>
        <p className="bt-muted" style={{ fontSize: 13, marginTop: 14 }}>
          These flows are being built across v0.1–v0.4 — see <code>docs/roadmap.md</code>.
        </p>
      </div>
    </section>
  );
}
