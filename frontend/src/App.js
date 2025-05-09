import React from 'react';
import './App.css';
import DoctorList from './components/DoctorList';
import AppointmentForm from './components/AppointmentForm';
import CancelAppointment from './components/CancelAppointment';

function App() {
  return (
    <div className="App">
      <h1>Healthcare Appointment Booking System</h1>
      <DoctorList />
      <AppointmentForm />
      <CancelAppointment />
    </div>
  );
}

export default App;