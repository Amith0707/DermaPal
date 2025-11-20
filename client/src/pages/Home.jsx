import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="page">
      <h1>Welcome to DermaPal</h1>
      <p>Your Smart Skin Disease Classifier</p>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "20px" }}>
        <Link className="btn" to="/patient">I am a Patient</Link>
        <Link className="btn" to="/doctor" style={{ background: "#10b981" }}>
          I am a Doctor
        </Link>
      </div>
    </div>
  );
}
