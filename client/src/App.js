import { useState, useEffect } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  ScatterChart, Scatter, LineChart, Line, ReferenceLine, Legend
} from "recharts";

const API = "http://localhost:5000/api";

const theme = {
  bg: "#0a0a0f",
  surface: "#12121a",
  card: "#1a1a26",
  border: "#2a2a3e",
  accent: "#e63946",
  accentSoft: "#ff6b6b",
  gold: "#ffd60a",
  teal: "#06d6a0",
  blue: "#118ab2",
  text: "#f0f0f8",
  muted: "#8888aa",
};

const styles = {
  app: {
    minHeight: "100vh",
    background: theme.bg,
    color: theme.text,
    fontFamily: "'Courier New', monospace",
  },
  nav: {
    background: theme.surface,
    borderBottom: `1px solid ${theme.border}`,
    padding: "0 2rem",
    display: "flex",
    alignItems: "center",
    gap: "0",
    position: "sticky",
    top: 0,
    zIndex: 100,
  },
  logo: {
    fontFamily: "'Georgia', serif",
    fontSize: "1.1rem",
    fontWeight: "bold",
    color: theme.accent,
    padding: "1.2rem 1.5rem 1.2rem 0",
    borderRight: `1px solid ${theme.border}`,
    marginRight: "1rem",
    letterSpacing: "0.05em",
  },
  navBtn: (active) => ({
    background: "none",
    border: "none",
    color: active ? theme.accent : theme.muted,
    fontFamily: "'Courier New', monospace",
    fontSize: "0.78rem",
    padding: "1.2rem 1rem",
    cursor: "pointer",
    borderBottom: active ? `2px solid ${theme.accent}` : "2px solid transparent",
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    transition: "color 0.2s",
  }),
  page: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "3rem 2rem",
  },
  heading: {
    fontFamily: "'Georgia', serif",
    fontSize: "2.5rem",
    fontWeight: "normal",
    marginBottom: "0.5rem",
    color: theme.text,
    letterSpacing: "-0.02em",
  },
  subheading: {
    color: theme.muted,
    fontSize: "0.9rem",
    marginBottom: "2.5rem",
    letterSpacing: "0.05em",
    textTransform: "uppercase",
  },
  grid: (cols) => ({
    display: "grid",
    gridTemplateColumns: `repeat(${cols}, 1fr)`,
    gap: "1rem",
    marginBottom: "2rem",
  }),
  card: {
    background: theme.card,
    border: `1px solid ${theme.border}`,
    padding: "1.5rem",
    borderRadius: "2px",
  },
  statCard: (color) => ({
    background: theme.card,
    border: `1px solid ${color || theme.border}`,
    borderLeft: `3px solid ${color || theme.accent}`,
    padding: "1.5rem",
    borderRadius: "2px",
  }),
  label: {
    fontSize: "0.7rem",
    color: theme.muted,
    textTransform: "uppercase",
    letterSpacing: "0.1em",
    marginBottom: "0.4rem",
  },
  value: {
    fontSize: "2rem",
    fontWeight: "bold",
    fontFamily: "'Georgia', serif",
  },
  tag: (color) => ({
    display: "inline-block",
    background: color + "22",
    color: color,
    border: `1px solid ${color}44`,
    padding: "0.2rem 0.6rem",
    fontSize: "0.7rem",
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    borderRadius: "2px",
    marginBottom: "0.5rem",
  }),
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: "0.85rem",
  },
  th: {
    textAlign: "left",
    padding: "0.75rem 1rem",
    background: theme.surface,
    color: theme.muted,
    fontSize: "0.7rem",
    textTransform: "uppercase",
    letterSpacing: "0.1em",
    borderBottom: `1px solid ${theme.border}`,
  },
  td: {
    padding: "0.75rem 1rem",
    borderBottom: `1px solid ${theme.border}22`,
    color: theme.text,
  },
  input: {
    background: theme.surface,
    border: `1px solid ${theme.border}`,
    color: theme.text,
    padding: "0.5rem 0.75rem",
    fontFamily: "'Courier New', monospace",
    fontSize: "0.85rem",
    width: "100%",
    borderRadius: "2px",
    outline: "none",
  },
  btn: {
    background: theme.accent,
    color: "#fff",
    border: "none",
    padding: "0.75rem 2rem",
    fontFamily: "'Courier New', monospace",
    fontSize: "0.85rem",
    letterSpacing: "0.1em",
    textTransform: "uppercase",
    cursor: "pointer",
    borderRadius: "2px",
    marginTop: "1rem",
  },
  divider: {
    borderColor: theme.border,
    margin: "2rem 0",
  },
  loading: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "200px",
    color: theme.muted,
    fontSize: "0.85rem",
    letterSpacing: "0.1em",
  },
};

function Loader() {
  return <div style={styles.loading}>[ LOADING DATA... ]</div>;
}

// ─── HOME PAGE ───────────────────────────────────────────────────────────────
function HomePage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get(`${API}/overview`).then(r => setData(r.data));
  }, []);

  if (!data) return <Loader />;

  return (
    <div style={styles.page}>
      <div style={{ marginBottom: "3rem" }}>
        <div style={styles.tag(theme.accent)}>Spring 2026 — Probability &amp; Statistics</div>
        <h1 style={{ ...styles.heading, fontSize: "3rem" }}>
          Global Organized<br />Crime Analysis
        </h1>
        <p style={styles.subheading}>2023 Global OC Index · 193 Countries · Standard Deviants</p>
        <p style={{ color: theme.muted, maxWidth: "600px", lineHeight: "1.8", fontSize: "0.9rem" }}>
          A statistical deep-dive into international organized crime patterns.
          Using descriptive statistics, probability distributions, confidence intervals,
          and regression modeling to understand and predict global criminality.
        </p>
      </div>

      <div style={styles.grid(4)}>
        {[
          { label: "Countries Analyzed", value: data.total_countries, color: theme.teal },
          { label: "Global Crime Mean", value: data.global_mean_criminality, color: theme.accent },
          { label: "Global Resilience Mean", value: data.global_mean_resilience, color: theme.blue },
          { label: "Variables Studied", value: "5", color: theme.gold },
        ].map((s, i) => (
          <div key={i} style={styles.statCard(s.color)}>
            <div style={styles.label}>{s.label}</div>
            <div style={{ ...styles.value, color: s.color }}>{s.value}</div>
          </div>
        ))}
      </div>

      <div style={styles.grid(2)}>
        <div style={styles.card}>
          <div style={styles.label}>🔴 Highest Crime Countries</div>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Country</th>
                <th style={styles.th}>Score</th>
              </tr>
            </thead>
            <tbody>
              {data.top5_highest.map((c, i) => (
                <tr key={i}>
                  <td style={styles.td}>{c.Country}</td>
                  <td style={{ ...styles.td, color: theme.accent, fontWeight: "bold" }}>
                    {c.Criminality.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={styles.card}>
          <div style={styles.label}>🟢 Lowest Crime Countries</div>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Country</th>
                <th style={styles.th}>Score</th>
              </tr>
            </thead>
            <tbody>
              {data.top5_lowest.map((c, i) => (
                <tr key={i}>
                  <td style={styles.td}>{c.Country}</td>
                  <td style={{ ...styles.td, color: theme.teal, fontWeight: "bold" }}>
                    {c.Criminality.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={styles.card}>
        <div style={styles.label}>Dataset Variables</div>
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", marginTop: "0.5rem" }}>
          {["Criminality", "Resilience", "Human Trafficking", "Cyber-dependent Crimes", "State-embedded Actors", "Country"].map(v => (
            <span key={v} style={styles.tag(theme.blue)}>{v}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── DATA EXPLORER ───────────────────────────────────────────────────────────
function DataPage() {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios.get(`${API}/data`).then(r => setData(r.data.data));
  }, []);

  const filtered = data.filter(d =>
    d.Country.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={styles.page}>
      <div style={styles.tag(theme.blue)}>Raw Data</div>
      <h1 style={styles.heading}>Data Explorer</h1>
      <p style={styles.subheading}>193 Countries · Global OC Index 2023</p>

      <input
        style={{ ...styles.input, maxWidth: "400px", marginBottom: "1.5rem" }}
        placeholder="Search country..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <div style={{ color: theme.muted, fontSize: "0.8rem", marginBottom: "1rem" }}>
        Showing {filtered.length} of {data.length} countries
      </div>

      <div style={{ overflowX: "auto" }}>
        <table style={styles.table}>
          <thead>
            <tr>
              {["Country", "Criminality", "Resilience", "Human Trafficking", "Cyber Crimes", "State Actors"].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((row, i) => (
              <tr key={i} style={{ background: i % 2 === 0 ? "transparent" : theme.surface + "44" }}>
                <td style={{ ...styles.td, fontWeight: "bold" }}>{row.Country}</td>
                <td style={{ ...styles.td, color: row.Criminality >= 7 ? theme.accent : row.Criminality >= 5 ? theme.gold : theme.teal }}>
                  {row.Criminality?.toFixed(2)}
                </td>
                <td style={styles.td}>{row.Resilience?.toFixed(2)}</td>
                <td style={styles.td}>{row["Human trafficking"]?.toFixed(2)}</td>
                <td style={styles.td}>{row["Cyber-dependent crimes"]?.toFixed(2)}</td>
                <td style={styles.td}>{row["State-embedded actors"]?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─── DESCRIPTIVE STATS ────────────────────────────────────────────────────────
function StatsPage() {
  const [stats, setStats] = useState(null);
  const [ci, setCi] = useState(null);

  useEffect(() => {
    axios.get(`${API}/stats`).then(r => setStats(r.data.statistics));
    axios.get(`${API}/confidence`).then(r => setCi(r.data));
  }, []);

  if (!stats || !ci) return <Loader />;

  const vars = Object.keys(stats);
  const measures = ["mean", "median", "std", "variance", "min", "max", "skewness"];

  return (
    <div style={styles.page}>
      <div style={styles.tag(theme.gold)}>Descriptive Analysis</div>
      <h1 style={styles.heading}>Statistical Summary</h1>
      <p style={styles.subheading}>Mean · Median · Std Dev · Variance · Skewness</p>

      <div style={{ overflowX: "auto", marginBottom: "3rem" }}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Variable</th>
              {measures.map(m => <th key={m} style={styles.th}>{m}</th>)}
            </tr>
          </thead>
          <tbody>
            {vars.map((v, i) => (
              <tr key={i} style={{ background: i % 2 === 0 ? "transparent" : theme.surface + "44" }}>
                <td style={{ ...styles.td, color: theme.gold, fontWeight: "bold" }}>{v}</td>
                {measures.map(m => (
                  <td key={m} style={styles.td}>{stats[v][m]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <hr style={styles.divider} />

      <div style={styles.tag(theme.teal)}>Inferential Statistics</div>
      <h2 style={{ ...styles.heading, fontSize: "1.8rem", marginTop: "1rem" }}>
        95% Confidence Intervals
      </h2>

      <div style={styles.grid(3)}>
        {[
          { label: "Sample Mean", value: ci.overall.mean, color: theme.text },
          { label: "CI Lower Bound", value: ci.overall.ci_lower, color: theme.teal },
          { label: "CI Upper Bound", value: ci.overall.ci_upper, color: theme.accent },
        ].map((s, i) => (
          <div key={i} style={styles.statCard(s.color)}>
            <div style={styles.label}>{s.label}</div>
            <div style={{ ...styles.value, color: s.color, fontSize: "1.8rem" }}>{s.value}</div>
          </div>
        ))}
      </div>

      <div style={styles.card}>
        <div style={styles.label}>CI by Resilience Group</div>
        <table style={{ ...styles.table, marginTop: "1rem" }}>
          <thead>
            <tr>
              {["Group", "Countries (n)", "Mean Criminality", "CI Lower", "CI Upper"].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {ci.by_group.map((g, i) => (
              <tr key={i}>
                <td style={{ ...styles.td, fontWeight: "bold" }}>{g.group}</td>
                <td style={styles.td}>{g.n}</td>
                <td style={{ ...styles.td, color: theme.gold }}>{g.mean}</td>
                <td style={{ ...styles.td, color: theme.teal }}>{g.ci_lower}</td>
                <td style={{ ...styles.td, color: theme.accent }}>{g.ci_upper}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─── PROBABILITY DISTRIBUTION ─────────────────────────────────────────────────
function DistributionPage() {
  const [dist, setDist] = useState(null);
  const [variable, setVariable] = useState("Criminality");

  const variables = ["Criminality", "Resilience", "Human trafficking", "Cyber-dependent crimes", "State-embedded actors"];

  useEffect(() => {
    axios.get(`${API}/distribution?variable=${encodeURIComponent(variable)}`)
      .then(r => setDist(r.data));
  }, [variable]);

  return (
    <div style={styles.page}>
      <div style={styles.tag(theme.teal)}>Probability</div>
      <h1 style={styles.heading}>Distribution Analysis</h1>
      <p style={styles.subheading}>Normal Distribution Fit · Shapiro-Wilk Test</p>

      <select
        style={{ ...styles.input, maxWidth: "300px", marginBottom: "2rem" }}
        value={variable}
        onChange={e => { setVariable(e.target.value); setDist(null); }}
      >
        {variables.map(v => <option key={v} value={v}>{v}</option>)}
      </select>

      {!dist ? <Loader /> : (
        <>
          <div style={styles.grid(4)}>
            {[
              { label: "Mean (μ)", value: dist.mu, color: theme.blue },
              { label: "Std Dev (σ)", value: dist.sigma, color: theme.gold },
              { label: "Shapiro-Wilk p", value: dist.shapiro_p, color: dist.is_normal ? theme.teal : theme.accent },
              { label: "Normality", value: dist.is_normal ? "Normal ✓" : "Non-normal ✗", color: dist.is_normal ? theme.teal : theme.accent },
            ].map((s, i) => (
              <div key={i} style={styles.statCard(s.color)}>
                <div style={styles.label}>{s.label}</div>
                <div style={{ ...styles.value, color: s.color, fontSize: "1.5rem" }}>{s.value}</div>
              </div>
            ))}
          </div>

          <div style={styles.card}>
            <div style={styles.label}>Frequency Distribution — {variable}</div>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={dist.histogram} margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
                <XAxis dataKey="label" tick={{ fontSize: 10, fill: theme.muted }} angle={-30} textAnchor="end" height={60} />
                <YAxis tick={{ fontSize: 11, fill: theme.muted }} />
                <Tooltip
                  contentStyle={{ background: theme.card, border: `1px solid ${theme.border}`, borderRadius: "2px" }}
                  labelStyle={{ color: theme.muted }}
                />
                <Bar dataKey="count" fill={theme.blue} opacity={0.8} radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div style={{ ...styles.card, marginTop: "1rem" }}>
            <div style={styles.label}>Normal Curve Overlay</div>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={dist.normal_curve} margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
                <XAxis dataKey="x" tick={{ fontSize: 11, fill: theme.muted }} tickFormatter={v => v.toFixed(1)} />
                <YAxis tick={{ fontSize: 11, fill: theme.muted }} />
                <Tooltip
                  contentStyle={{ background: theme.card, border: `1px solid ${theme.border}` }}
                  formatter={(v) => [v.toFixed(5), "Density"]}
                />
                <ReferenceLine x={dist.mu} stroke={theme.accent} strokeDasharray="4 4" label={{ value: `μ=${dist.mu}`, fill: theme.accent, fontSize: 11 }} />
                <Line type="monotone" dataKey="y" stroke={theme.teal} strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  );
}

// ─── REGRESSION PAGE ──────────────────────────────────────────────────────────
function RegressionPage() {
  const [reg, setReg] = useState(null);
  const [inputs, setInputs] = useState({ Resilience: 5, "Human trafficking": 5, "Cyber-dependent crimes": 5, "State-embedded actors": 5 });
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    axios.get(`${API}/regression`).then(r => setReg(r.data));
  }, []);

  const handlePredict = () => {
    axios.post(`${API}/predict`, inputs).then(r => setPrediction(r.data));
  };

  if (!reg) return <Loader />;

  return (
    <div style={styles.page}>
      <div style={styles.tag(theme.accentSoft)}>Machine Learning</div>
      <h1 style={styles.heading}>Regression Analysis</h1>
      <p style={styles.subheading}>Multiple Linear Regression · Criminality Prediction</p>

      <div style={styles.grid(3)}>
        {[
          { label: "R² Score", value: reg.r2, color: reg.r2 > 0.7 ? theme.teal : theme.gold },
          { label: "RMSE", value: reg.rmse, color: theme.blue },
          { label: "Intercept", value: reg.intercept, color: theme.muted },
        ].map((s, i) => (
          <div key={i} style={styles.statCard(s.color)}>
            <div style={styles.label}>{s.label}</div>
            <div style={{ ...styles.value, color: s.color, fontSize: "1.8rem" }}>{s.value}</div>
          </div>
        ))}
      </div>

      <div style={styles.grid(2)}>
        <div style={styles.card}>
          <div style={styles.label}>Model Coefficients</div>
          <table style={{ ...styles.table, marginTop: "1rem" }}>
            <thead>
              <tr>
                <th style={styles.th}>Feature</th>
                <th style={styles.th}>Coefficient</th>
              </tr>
            </thead>
            <tbody>
              {reg.coefficients.map((c, i) => (
                <tr key={i}>
                  <td style={styles.td}>{c.feature}</td>
                  <td style={{ ...styles.td, color: c.coefficient > 0 ? theme.accent : theme.teal, fontWeight: "bold" }}>
                    {c.coefficient > 0 ? "+" : ""}{c.coefficient}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={styles.card}>
          <div style={styles.label}>🔮 Live Prediction</div>
          {reg.features_used.map(feat => (
            <div key={feat} style={{ marginBottom: "1rem", marginTop: "0.75rem" }}>
              <div style={{ ...styles.label, marginBottom: "0.3rem" }}>{feat}: {inputs[feat]}</div>
              <input
                type="range" min="0" max="10" step="0.5"
                value={inputs[feat] || 5}
                onChange={e => setInputs({ ...inputs, [feat]: parseFloat(e.target.value) })}
                style={{ width: "100%", accentColor: theme.accent }}
              />
            </div>
          ))}
          <button style={styles.btn} onClick={handlePredict}>Predict →</button>
          {prediction && (
            <div style={{
              marginTop: "1.5rem",
              padding: "1rem",
              border: `1px solid ${prediction.color === "red" ? theme.accent : prediction.color === "orange" ? theme.gold : theme.teal}`,
              borderRadius: "2px",
              textAlign: "center"
            }}>
              <div style={styles.label}>Predicted Criminality</div>
              <div style={{
                fontSize: "2.5rem",
                fontFamily: "'Georgia', serif",
                color: prediction.color === "red" ? theme.accent : prediction.color === "orange" ? theme.gold : theme.teal
              }}>
                {prediction.predicted_criminality}
              </div>
              <div style={{ color: theme.muted, fontSize: "0.8rem", marginTop: "0.25rem" }}>
                {prediction.level} Criminality Level
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={styles.card}>
        <div style={styles.label}>Actual vs Predicted Criminality</div>
        <ResponsiveContainer width="100%" height={340}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
            <XAxis dataKey="actual" name="Actual" tick={{ fontSize: 11, fill: theme.muted }} label={{ value: "Actual", position: "bottom", fill: theme.muted, fontSize: 11 }} />
            <YAxis dataKey="predicted" name="Predicted" tick={{ fontSize: 11, fill: theme.muted }} label={{ value: "Predicted", angle: -90, position: "insideLeft", fill: theme.muted, fontSize: 11 }} />
            <Tooltip
              cursor={{ strokeDasharray: "3 3" }}
              contentStyle={{ background: theme.card, border: `1px solid ${theme.border}` }}
              formatter={(val, name, props) => [val, props.dataKey === "actual" ? "Actual" : "Predicted"]}
            />
            <Scatter data={reg.scatter_data} fill={theme.accent} opacity={0.7} />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
const pages = ["Home", "Data", "Statistics", "Distribution", "Regression"];

export default function App() {
  const [page, setPage] = useState("Home");

  return (
    <div style={styles.app}>
      <nav style={styles.nav}>
        <div style={styles.logo}>STANDARD DEVIANTS</div>
        {pages.map(p => (
          <button key={p} style={styles.navBtn(page === p)} onClick={() => setPage(p)}>
            {p}
          </button>
        ))}
      </nav>

      {page === "Home" && <HomePage />}
      {page === "Data" && <DataPage />}
      {page === "Statistics" && <StatsPage />}
      {page === "Distribution" && <DistributionPage />}
      {page === "Regression" && <RegressionPage />}
    </div>
  );
}