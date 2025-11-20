export default function DoctorDashboard() {
  // temporary dummy data – later you will fetch from backend
  const patients = [
    {
      id: 1,
      name: "John Doe",
      age: 35,
      symptoms: "Red patch, itchy skin",
      diagnosis: "Eczema",
      image: "https://via.placeholder.com/120"
    },
    {
      id: 2,
      name: "Sarah Lee",
      age: 28,
      symptoms: "Dark circular patch",
      diagnosis: "Ringworm",
      image: "https://via.placeholder.com/120"
    }
  ];

  return (
    <div className="page">
      <h2>Doctor Dashboard</h2>

      {patients.map((p) => (
        <div className="card" key={p.id}>
          <img src={p.image} alt="skin lesion" />
          <h3>{p.name}</h3>
          <p><strong>Age:</strong> {p.age}</p>
          <p><strong>Symptoms:</strong> {p.symptoms}</p>
          <p><strong>Predicted Disease:</strong> {p.diagnosis}</p>
        </div>
      ))}
    </div>
  );
}
