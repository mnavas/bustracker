export default function Placeholder({
  title,
  version,
  children,
}: {
  title: string;
  version: string;
  children?: React.ReactNode;
}) {
  return (
    <section>
      <h1 style={{ fontSize: 24, margin: "0 0 4px" }}>{title}</h1>
      <p className="bt-muted" style={{ marginTop: 0 }}>
        {children ?? "This section is part of an upcoming milestone."}
      </p>
      <div className="bt-card" style={{ padding: 22, marginTop: 18 }}>
        <span
          style={{
            display: "inline-block",
            background: "var(--accent)",
            color: "var(--accent-ink)",
            fontWeight: 700,
            fontSize: 12,
            borderRadius: 999,
            padding: "3px 10px",
          }}
        >
          Coming in {version}
        </span>
        <p className="bt-muted" style={{ fontSize: 13, marginTop: 12, marginBottom: 0 }}>
          See <code>docs/roadmap.md</code> for the delivery plan.
        </p>
      </div>
    </section>
  );
}
