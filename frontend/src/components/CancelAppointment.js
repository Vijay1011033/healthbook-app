import React, { useState } from 'react';

const CancelAppointment = () => {
  const [appointmentId, setAppointmentId] = useState('');

  const handleCancel = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/appointments/${appointmentId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        alert('Appointment cancelled successfully!');
        setAppointmentId('');
      } else {
        const error = await response.json();
        alert(error.detail);
      }
    } catch (error) {
      console.error('Error cancelling appointment:', error);
      alert('Failed to cancel appointment');
    }
  };

  return (
    <div>
      <h2>Cancel Appointment</h2>
      <form onSubmit={handleCancel}>
        <div>
          <label>Appointment ID:</label>
          <input
            type="number"
            value={appointmentId}
            onChange={(e) => setAppointmentId(e.target.value)}
            required
          />
        </div>
        <button type="submit">Cancel Appointment</button>
      </form>
    </div>
  );
};

export default CancelAppointment;