import React, { useState, useEffect } from 'react';

const AppointmentForm = () => {
  const [doctors, setDoctors] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [formData, setFormData] = useState({
    patient_name: '',
    doctor_id: '',
    appointment_date: '',
    time_slot: ''
  });

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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const fetchAvailableSlots = async (doctorId, date) => {
    if (!doctorId || !date) return;
    
    try {
      const response = await fetch(`http://localhost:8000/doctors/${doctorId}/available-slots/${date}`);
      const data = await response.json();
      if (response.ok) {
        setAvailableSlots(data.available_slots);
      } else {
        setError(data.detail || 'Failed to fetch available slots');
      }
    } catch (error) {
      console.error('Error fetching available slots:', error);
      setError('Failed to fetch available slots');
    }
  };

  useEffect(() => {
    if (formData.doctor_id && formData.appointment_date) {
      fetchAvailableSlots(formData.doctor_id, formData.appointment_date);
    } else {
      setAvailableSlots([]);
    }
  }, [formData.doctor_id, formData.appointment_date]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      if (!formData.patient_name.trim()) {
        setError('Please enter a valid patient name');
        return;
      }

      if (!formData.doctor_id || parseInt(formData.doctor_id) <= 0) {
        setError('Please enter a valid doctor ID');
        return;
      }

      const appointmentDateTime = new Date(formData.appointment_date + 'T' + formData.time_slot);
      if (appointmentDateTime < new Date()) {
        setError('Please select a future date and time');
        return;
      }

      const response = await fetch(`http://localhost:8000/doctors/${formData.doctor_id}/appointments/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_name: formData.patient_name.trim(),
          appointment_date: appointmentDateTime.toISOString(),
          time_slot: formData.time_slot
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSuccess(`Appointment booked successfully! Your appointment ID is: ${data.id}`);
        setFormData({
          patient_name: '',
          doctor_id: '',
          appointment_date: '',
          time_slot: ''
        });
      } else {
        setError(data.detail || 'Failed to book appointment. Please try again.');
      }
    } catch (error) {
      console.error('Error booking appointment:', error);
      setError('Failed to book appointment. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Book Appointment</h2>
      {success && <div className="success-message">{success}</div>}
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Patient Name:</label>
          <input
            type="text"
            value={formData.patient_name}
            onChange={(e) => setFormData({...formData, patient_name: e.target.value})}
            disabled={loading}
            required
          />
        </div>
        <div>
          <label>Select Doctor:</label>
          <select
            value={formData.doctor_id}
            onChange={(e) => setFormData({...formData, doctor_id: e.target.value})}
            disabled={loading}
            required
          >
            <option value="">Choose a doctor</option>
            {doctors.map(doctor => (
              <option key={doctor.id} value={doctor.id}>
                Dr. {doctor.name} - {doctor.specialty} ({doctor.slots_per_day} slots/day)
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Date:</label>
          <input
            type="date"
            value={formData.appointment_date}
            onChange={(e) => setFormData({...formData, appointment_date: e.target.value})}
            disabled={loading}
            min={new Date().toISOString().split('T')[0]}
            required
          />
        </div>
        <div>
          <label>Time:</label>
          <select
            value={formData.time_slot}
            onChange={(e) => setFormData({...formData, time_slot: e.target.value})}
            disabled={loading || availableSlots.length === 0}
            required
          >
            <option value="">Choose a time slot</option>
            {availableSlots.map(slot => (
              <option key={slot} value={slot}>
                {slot}
              </option>
            ))}
          </select>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Booking...' : 'Book Appointment'}
        </button>
      </form>
    </div>
  );
};

export default AppointmentForm;