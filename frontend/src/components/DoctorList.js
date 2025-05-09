import React, { useState, useEffect } from 'react';

const DoctorList = () => {
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    try {
      const response = await fetch('http://localhost:8000/doctors/');
      const data = await response.json();
      setDoctors(data);
    } catch (error) {
      console.error('Error fetching doctors:', error);
    }
  };

  return (
    <div>
      <h2>Available Doctors</h2>
      <div className="doctors-grid">
        {doctors.map(doctor => (
          <div key={doctor.id} className="doctor-card">
            <h3>Dr. {doctor.name}</h3>
            <p>Specialty: {doctor.specialty}</p>
            <p>Available Slots: {doctor.slots_per_day}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DoctorList;