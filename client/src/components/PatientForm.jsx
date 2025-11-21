import { useState } from "react";

export default function PatientForm() {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // for now just show a message – you can connect backend later
    setMessage("Patient data submitted successfully (mock).");
  };

  return (
    <div className="page">
      <h2>Patient Information</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Enter Age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
        />

        <textarea
          placeholder="Describe the symptoms"
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          rows="4"
          required
        ></textarea>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
          required
        />

        <button type="submit">Upload & Submit</button>
      </form>

      {message && <p style={{ marginTop: "12px", fontWeight: "bold" }}>{message}</p>}
    </div>
  );
}
