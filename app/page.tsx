"use client";

import { useState } from "react";
import Link from "next/link";

// Public landing page served at "/" on the company's own server.
// The admin dashboard lives at /dashboard (login-gated). All styles are scoped
// under `.lp` so nothing leaks into the dashboard.
export default function Home() {
  const [menu, setMenu] = useState(false);
  const close = () => setMenu(false);

  return (
    <div className="lp">
      <style>{CSS}</style>

      <nav>
        <div className="wrap nav-inner">
          <a className="nav-brand" href="#top">
            <span className="mark">BT</span>
            <strong>BusTracker</strong>
          </a>
          <div className="nav-links">
            <a href="#how">How it works</a>
            <a href="#features">Features</a>
            <a href="#parents">For parents</a>
            <a href="#support">Support</a>
            <Link className="btn btn-primary" href="/dashboard">
              Dashboard
            </Link>
          </div>
          <button
            className={`nav-hamburger${menu ? " open" : ""}`}
            aria-label="Menu"
            onClick={() => setMenu((m) => !m)}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
        <div className={`nav-mobile${menu ? " open" : ""}`}>
          <a href="#how" onClick={close}>How it works</a>
          <a href="#features" onClick={close}>Features</a>
          <a href="#parents" onClick={close}>For parents</a>
          <a href="#support" onClick={close}>Support</a>
          <Link href="/dashboard" onClick={close}>Dashboard →</Link>
        </div>
      </nav>

      <header className="hero" id="top">
        <div className="wrap">
          <span className="pill">Self-hosted · one install = one company</span>
          <h1>Know exactly where the school bus is — and when your child is on it.</h1>
          <p className="lede">
            BusTracker is a self-hosted, door-to-door school-bus tracking platform. Parents watch
            their own child&apos;s bus live and get alerts as it approaches, when their child boards,
            and when they&apos;re dropped off — all driven by the bus&apos;s distance to each home.
          </p>
          <div className="cta">
            <Link className="btn btn-primary" href="/dashboard">Open the dashboard</Link>
            <a className="btn btn-outline" href="https://github.com/mnavas/bustracker">View on GitHub</a>
          </div>
        </div>
      </header>

      <section id="pieces">
        <div className="wrap">
          <div className="sec-head">
            <h2>Three pieces, one company</h2>
            <p>The company runs its own server. Drivers and parents use two dedicated apps that sync only to that server.</p>
          </div>
          <div className="grid cols-3">
            <div className="card"><div className="ic">🖥️</div><h3>The server</h3><p>A one-command Docker install the transport company runs itself: the dashboard, database, live tracking and API. The company owns all of its data.</p></div>
            <div className="card"><div className="ic">🚍</div><h3>Driver app</h3><p>Start a run and drive. The ordered home-by-home list, live location, and boarding/drop-off recording happen automatically — minimal taps.</p></div>
            <div className="card"><div className="ic">📱</div><h3>Parent app</h3><p>Track your child&apos;s bus live, with a countdown to your home and push alerts on approach, boarding, and drop-off.</p></div>
          </div>
        </div>
      </section>

      <section id="how" className="alt">
        <div className="wrap">
          <div className="sec-head">
            <h2>Driven by distance to home</h2>
            <p>Door-to-door: each child&apos;s home is the stop, and the bus&apos;s distance to it drives everything. No scanning, no badges, no manual roll-call.</p>
          </div>
          <div className="steps">
            <div className="step"><div className="n">1</div><h3>Approaching</h3><p>As the bus nears a child&apos;s home, that child&apos;s parents get a heads-up alert so they can be ready.</p></div>
            <div className="step"><div className="n">2</div><h3>On board</h3><p>When the bus reaches the home, the pickup is recorded automatically and the parent is notified their child is aboard.</p></div>
            <div className="step"><div className="n">3</div><h3>Dropped off</h3><p>On the way home, reaching the door records the drop-off and alerts the parent — at home, or a different contracted destination.</p></div>
          </div>
        </div>
      </section>

      <section id="features">
        <div className="wrap">
          <div className="sec-head">
            <h2>What the company gets</h2>
            <p>Everything needed to run daily routes and give parents real visibility.</p>
          </div>
          <div className="grid cols-3">
            <div className="card"><div className="ic">🗺️</div><h3>Live fleet monitoring</h3><p>Every active run on a map, each bus&apos;s position and last-update time, and its progress along the route.</p></div>
            <div className="card"><div className="ic">✅</div><h3>Automatic attendance</h3><p>Who was picked up and dropped off, when and where — recorded per run, no roll-call.</p></div>
            <div className="card"><div className="ic">🔔</div><h3>Parent alerts</h3><p>Push notifications on approach, boarding and drop-off, plus run-started and delay notices.</p></div>
            <div className="card"><div className="ic">🛣️</div><h3>Flexible routes</h3><p>To-school, from-school, or round trips; per-day assignments; academy returns to a different destination.</p></div>
            <div className="card"><div className="ic">🙋</div><h3>Absence reporting</h3><p>Parents flag &quot;not riding today&quot; in advance; the driver&apos;s list updates and false alerts are suppressed.</p></div>
            <div className="card"><div className="ic">🔒</div><h3>Data ownership &amp; privacy</h3><p>Children&apos;s data stays on the company&apos;s own server. Parents see only their own child&apos;s bus — never other children or homes.</p></div>
          </div>
        </div>
      </section>

      <section id="parents" className="alt">
        <div className="wrap">
          <div className="sec-head">
            <h2>For parents</h2>
            <p>Peace of mind, scoped tightly to your own child.</p>
          </div>
          <div className="grid cols-2">
            <div className="card"><div className="ic">👀</div><h3>See your child&apos;s bus</h3><p>Follow the routes your child is on while they&apos;re running, with a live ETA to your home on the days they ride.</p></div>
            <div className="card"><div className="ic">🛡️</div><h3>Only your child</h3><p>You never see other children, other homes, or the wider fleet — just the bus carrying your own child.</p></div>
          </div>
          <p className="note">The parent and driver apps are provided by the company that operates your route — ask them for an invite. BusTracker does not run a shared cloud; each company hosts its own.</p>
        </div>
      </section>

      <section id="support">
        <div className="wrap">
          <div className="sec-head">
            <h2>Support</h2>
            <p>Documentation, source, and help standing up your own instance.</p>
          </div>
          <div className="support-grid">
            <div className="support-card">
              <h3>📚 Documentation</h3>
              <p>Step-by-step guides for installing, running day-to-day, and administering your server.</p>
              <a className="slink" href="https://github.com/mnavas/bustracker/blob/main/docs/install.md">Installation &amp; setup →</a>
              <a className="slink" href="https://github.com/mnavas/bustracker/blob/main/docs/daily-use.md">Daily use →</a>
              <a className="slink" href="https://github.com/mnavas/bustracker/blob/main/docs/routes-students-guardians.md">Routes, students &amp; guardians →</a>
              <a className="slink" href="https://github.com/mnavas/bustracker/blob/main/docs/admin.md">Administration &amp; maintenance →</a>
            </div>
            <div className="support-card">
              <h3>💻 Source &amp; issues</h3>
              <p>The server platform is free and open source (MIT). Browse the code, report a problem, or request a feature on GitHub.</p>
              <a className="slink" href="https://github.com/mnavas/bustracker">github.com/mnavas/bustracker →</a>
              <a className="slink" href="https://github.com/mnavas/bustracker/issues">Open an issue →</a>
            </div>
            <div className="support-card">
              <h3>🛠️ Help deploying</h3>
              <p>Prefer not to run a server yourself? Help is available to deploy, configure and keep your instance running — including custom-branded apps.</p>
              <a className="slink" href="mailto:warionv@gmail.com?subject=BusTracker%20setup%20help">warionv@gmail.com →</a>
            </div>
          </div>
        </div>
      </section>

      <footer>
        <div className="wrap f-inner">
          <div>
            <div className="brand"><span className="mark">BT</span> BusTracker</div>
            <small>
              Self-hosted school-bus tracking. Server is MIT-licensed open source.
              <br />
              The driver and parent apps are provided separately by the operating company.
            </small>
          </div>
          <div className="f-links">
            <a href="#how">How it works</a>
            <a href="#features">Features</a>
            <a href="#support">Support</a>
            <a href="https://github.com/mnavas/bustracker">GitHub</a>
            <a href="mailto:warionv@gmail.com?subject=BusTracker">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

const CSS = `
.lp { --bus:#f6b900; --bus-dark:#d99e00; --bus-pale:#fff4d1; --ink:#1a1403; --navy:#0f172a;
  --gray-100:#f1f5f9; --gray-200:#e2e8f0; --gray-600:#475569; --gray-800:#1e293b; --white:#fff;
  --radius:14px; --maxw:1080px;
  background:var(--white); color:var(--gray-800); line-height:1.6; min-height:100vh;
  font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; }
.lp *, .lp *::before, .lp *::after { box-sizing:border-box; margin:0; padding:0; }
.lp .wrap { max-width:var(--maxw); margin:0 auto; padding:0 1.25rem; }
.lp h1, .lp h2, .lp h3 { color:var(--navy); line-height:1.2; }
.lp a { color:inherit; }
.lp nav { position:sticky; top:0; z-index:100; background:rgba(255,255,255,.95); backdrop-filter:blur(8px); border-bottom:1px solid var(--gray-200); }
.lp .nav-inner { height:62px; display:flex; align-items:center; justify-content:space-between; }
.lp .nav-brand { display:flex; align-items:center; gap:10px; text-decoration:none; }
.lp .nav-brand .mark { width:30px; height:30px; border-radius:8px; background:var(--bus); color:var(--ink); font-weight:800; display:grid; place-items:center; font-size:.9rem; }
.lp .nav-brand strong { font-size:1.1rem; color:var(--navy); }
.lp .nav-links { display:flex; align-items:center; gap:1.75rem; }
.lp .nav-links a { text-decoration:none; font-size:.9rem; font-weight:500; color:var(--gray-600); transition:color .15s; }
.lp .nav-links a:hover { color:var(--navy); }
.lp .nav-hamburger { display:none; background:none; border:none; cursor:pointer; padding:6px; color:var(--gray-800); flex-direction:column; gap:5px; }
.lp .nav-hamburger span { display:block; width:22px; height:2px; background:currentColor; border-radius:2px; transition:transform .2s,opacity .2s; }
.lp .nav-hamburger.open span:nth-child(1) { transform:translateY(7px) rotate(45deg); }
.lp .nav-hamburger.open span:nth-child(2) { opacity:0; }
.lp .nav-hamburger.open span:nth-child(3) { transform:translateY(-7px) rotate(-45deg); }
.lp .nav-mobile { display:none; flex-direction:column; background:var(--white); border-top:1px solid var(--gray-200); padding:.5rem 1.25rem 1rem; }
.lp .nav-mobile.open { display:flex; }
.lp .nav-mobile a { text-decoration:none; font-size:.95rem; font-weight:500; color:var(--gray-600); padding:.7rem 0; border-bottom:1px solid var(--gray-100); }
.lp .nav-mobile a:last-child { border-bottom:none; }
.lp .btn { display:inline-flex; align-items:center; gap:6px; padding:.6rem 1.25rem; border-radius:9px; font-size:.9rem; font-weight:600; text-decoration:none; transition:all .15s; border:none; cursor:pointer; }
.lp .btn-primary { background:var(--bus); color:var(--ink); }
.lp .btn-primary:hover { background:var(--bus-dark); }
.lp .btn-outline { background:transparent; color:var(--navy); border:1.5px solid var(--gray-200); }
.lp .btn-outline:hover { border-color:var(--bus-dark); }
.lp .hero { background:linear-gradient(165deg,var(--bus-pale) 0%,var(--white) 62%); padding:5.5rem 0 4.5rem; text-align:center; }
.lp .hero h1 { font-size:clamp(2rem,5vw,3.1rem); font-weight:800; letter-spacing:-.02em; }
.lp .hero .lede { max-width:640px; margin:1.1rem auto 0; font-size:1.12rem; color:var(--gray-600); }
.lp .hero .cta { display:flex; gap:.8rem; justify-content:center; flex-wrap:wrap; margin-top:2rem; }
.lp .pill { display:inline-block; background:var(--white); border:1px solid var(--gray-200); color:var(--gray-600); font-size:.8rem; font-weight:600; padding:.3rem .85rem; border-radius:999px; margin-bottom:1.25rem; }
.lp section { padding:4.25rem 0; }
.lp section.alt { background:var(--gray-100); border-top:1px solid var(--gray-200); border-bottom:1px solid var(--gray-200); }
.lp .sec-head { text-align:center; max-width:640px; margin:0 auto 2.5rem; }
.lp .sec-head h2 { font-size:clamp(1.5rem,3.5vw,2rem); font-weight:800; }
.lp .sec-head p { color:var(--gray-600); margin-top:.6rem; }
.lp .grid { display:grid; gap:1.1rem; }
.lp .cols-3 { grid-template-columns:repeat(3,1fr); }
.lp .cols-2 { grid-template-columns:repeat(2,1fr); }
.lp .card { background:var(--white); border:1px solid var(--gray-200); border-radius:var(--radius); padding:1.5rem; }
.lp .card .ic { width:42px; height:42px; border-radius:10px; background:var(--bus-pale); color:var(--ink); display:grid; place-items:center; font-size:1.3rem; margin-bottom:.9rem; }
.lp .card h3 { font-size:1.05rem; }
.lp .card p { color:var(--gray-600); font-size:.94rem; margin-top:.4rem; }
.lp .steps { display:grid; grid-template-columns:repeat(3,1fr); gap:1.1rem; }
.lp .step { background:var(--white); border:1px solid var(--gray-200); border-radius:var(--radius); padding:1.5rem; }
.lp .step .n { width:32px; height:32px; border-radius:999px; background:var(--bus); color:var(--ink); font-weight:800; display:grid; place-items:center; margin-bottom:.8rem; }
.lp .step h3 { font-size:1.02rem; }
.lp .step p { color:var(--gray-600); font-size:.93rem; margin-top:.35rem; }
.lp .support-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.1rem; }
.lp .support-card { background:var(--white); border:1px solid var(--gray-200); border-radius:var(--radius); padding:1.6rem; }
.lp .support-card h3 { font-size:1.05rem; margin-bottom:.4rem; }
.lp .support-card p { color:var(--gray-600); font-size:.94rem; }
.lp .support-card a.slink { color:var(--bus-dark); font-weight:600; text-decoration:none; font-size:.92rem; display:block; margin-top:.6rem; }
.lp .support-card a.slink:hover { text-decoration:underline; }
.lp .note { margin:2rem auto 0; padding:1rem 1.25rem; background:var(--bus-pale); border:1px solid #f0dca0; border-radius:10px; color:#6b5600; font-size:.9rem; }
.lp footer { background:var(--navy); color:#cbd5e1; padding:2.5rem 0; font-size:.9rem; }
.lp footer .f-inner { display:flex; justify-content:space-between; flex-wrap:wrap; gap:1.5rem; }
.lp footer a { color:#cbd5e1; text-decoration:none; }
.lp footer a:hover { color:var(--bus); }
.lp footer .f-links { display:flex; gap:1.5rem; flex-wrap:wrap; }
.lp footer .brand { display:flex; align-items:center; gap:10px; color:var(--white); font-weight:700; }
.lp footer .mark { width:26px; height:26px; border-radius:7px; background:var(--bus); color:var(--ink); display:grid; place-items:center; font-weight:800; font-size:.8rem; }
.lp footer small { color:#64748b; }
@media (max-width:820px) {
  .lp .nav-links { display:none; }
  .lp .nav-hamburger { display:flex; }
  .lp .cols-3, .lp .cols-2, .lp .steps, .lp .support-grid { grid-template-columns:1fr; }
}
`;
