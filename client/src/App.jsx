import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home.jsx";
import PatientForm from "./components/PatientForm.jsx";
import DoctorDashboard from "./components/DoctorDashboard.jsx";

export default function App() {
  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb" }}>
      <nav>
        <Link to="/" style={{ fontWeight: 700, color: "#111" }}>DermaPal</Link>
        <Link to="/patient">Patient</Link>
        <Link to="/doctor">Doctor</Link>
      </nav>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/patient" element={<PatientForm />} />
          <Route path="/doctor" element={<DoctorDashboard />} />
        </Routes>
      </main>
    </div>
  );
}
