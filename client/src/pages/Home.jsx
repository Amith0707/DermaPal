import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={{ padding: "24px" }}>
      {/* MAIN CARD */}
      <div
        style={{
          maxWidth: "700px",
          margin: "0 auto",
          background: "#ffeef1",
          padding: "32px",
          borderRadius: "16px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.1)"
        }}
      >
        <h1 style={{ marginBottom: "8px" }}>Welcome to DermaPal</h1>
        <p style={{ color: "#444", marginBottom: "24px" }}>
          Your Smart Skin Disease Classifier
        </p>

        {/* BUTTONS */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <Link
            to="/patient"
            className="btn"
            style={{
              background: "#2563eb",
              textAlign: "center",
              borderRadius: "10px",
              padding: "12px",
              color: "white",
              fontSize: "18px",
              textDecoration: "none",
            }}
          >
            Patient
          </Link>

          <Link
            to="/doctor"
            className="btn"
            style={{
              background: "#10b981",
              textAlign: "center",
              borderRadius: "10px",
              padding: "12px",
              color: "white",
              fontSize: "18px",
              textDecoration: "none",
            }}
          >
            Doctor
          </Link>
        </div>
      </div>

      {/* DESCRIPTION OUTSIDE THE CARD */}
      <div
        style={{
          maxWidth: "700px",
          margin: "32px auto 0",
          padding: "0 8px",
          textAlign: "justify",
          lineHeight: "1.6",
          color: "#333",
        }}
      >
        <p>
          DermaPal is an AI-powered skin disease classifier that helps patients
          receive quick preliminary assessments. Upload your skin lesion image 
          along with your details, and our intelligent system analyzes the 
          condition and shares a summarized report with a doctor instantly.
        </p>
      </div>
    </div>
  );
}
