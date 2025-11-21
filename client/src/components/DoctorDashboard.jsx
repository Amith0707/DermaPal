// ...existing code...
import React, { useEffect, useState } from "react";

export default function DoctorPage() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function fetchPatients() {
    setLoading(true);
    setError("");
    try {
      const resp = await fetch("http://localhost:5000/patients");
      if (!resp.ok) throw new Error(`Failed: ${resp.status}`);
      const data = await resp.json();
      setPatients(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError(err?.message || "Failed to fetch patients");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchPatients();
  }, []);

  function renderImage(image) {
    if (!image) return null;
    // If already a data URL
    if (typeof image === "string" && image.startsWith("data:")) return image;
    // If base64 without data: prefix, assume jpeg
    if (typeof image === "string" && /^[A-Za-z0-9+/=]+$/.test(image) && image.length > 100) {
      return `data:image/jpeg;base64,${image}`;
    }
    // Otherwise assume it's a URL
    return image;
  }

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: "16px auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Doctor Dashboard</h2>
        <div>
          <button onClick={fetchPatients} style={{
            padding: "8px 12px",
            borderRadius: 6,
            border: "1px solid #ccc",
            background: "#fff",
            cursor: "pointer"
          }}>
            Refresh
          </button>
        </div>
      </div>

      {loading && <div>Loading patients...</div>}
      {error && <div style={{ color: "crimson" }}>{error}</div>}

      <div style={{
        marginTop: 18,
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
        gap: 16
      }}>
        {patients.length === 0 && !loading && <div style={{ color: "#666" }}>No patients found.</div>}
        {patients.map((p, idx) => {
          // fields: name, age, symptoms, image, prediction, date (submission date)
          const imgSrc = renderImage(p.image);
          return (
            <div key={idx} style={{
              background: "#fff",
              padding: 12,
              borderRadius: 8,
              boxShadow: "0 6px 18px rgba(0,0,0,0.04)",
              display: "flex",
              flexDirection: "column",
              gap: 8
            }}>
              <div style={{ display: "flex", gap: 12 }}>
                {imgSrc ? (
                  <img src={imgSrc} alt={p.name || "patient"} style={{ width: 96, height: 96, objectFit: "cover", borderRadius: 6, border: "1px solid #eee" }} />
                ) : (
                  <div style={{ width: 96, height: 96, background: "#fafafa", borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center", color: "#999" }}>
                    No image
                  </div>
                )}

                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 600 }}>{p.name || "—"}</div>
                  <div style={{ color: "#555", fontSize: 14 }}>Age: {p.age ?? "—"}</div>
                  <div style={{ color: "#555", fontSize: 13, marginTop: 6 }}>{p.date ? new Date(p.date).toLocaleString() : ""}</div>
                </div>
              </div>

              <div style={{ fontSize: 14 }}>
                <strong>Symptoms:</strong>
                <div style={{ marginTop: 6, color: "#333" }}>{p.symptoms || "—"}</div>
              </div>

              <div style={{ fontSize: 14 }}>
                <strong>Prediction:</strong>
                <div style={{ marginTop: 6, color: "#2b6cb0" }}>{p.prediction || "Not available"}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}