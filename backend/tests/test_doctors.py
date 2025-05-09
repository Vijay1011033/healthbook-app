from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app

client = TestClient(app)

def test_create_doctor():
    response = client.post(
        "/doctors/",
        json={"name": "Dr. Smith", "specialty": "Cardiology", "slots_per_day": 8}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Dr. Smith"

def test_get_doctors():
    response = client.get("/doctors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_appointment():
    # First create a doctor
    doctor_response = client.post(
        "/doctors/",
        json={"name": "Dr. Johnson", "specialty": "Pediatrics", "slots_per_day": 8}
    )
    doctor_id = doctor_response.json()["id"]

    # Then create an appointment
    appointment_data = {
        "patient_name": "John Doe",
        "appointment_date": datetime.now().isoformat(),
        "time_slot": "10:00"
    }
    response = client.post(
        f"/doctors/{doctor_id}/appointments/",
        json=appointment_data
    )
    assert response.status_code == 200
    assert response.json()["patient_name"] == "John Doe"

def test_cancel_appointment():
    # Create doctor and appointment first
    doctor_response = client.post(
        "/doctors/",
        json={"name": "Dr. Brown", "specialty": "Dentist", "slots_per_day": 8}
    )
    doctor_id = doctor_response.json()["id"]

    appointment_response = client.post(
        f"/doctors/{doctor_id}/appointments/",
        json={
            "patient_name": "Jane Doe",
            "appointment_date": datetime.now().isoformat(),
            "time_slot": "11:00"
        }
    )
    appointment_id = appointment_response.json()["id"]

    # Cancel the appointment
    response = client.delete(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Appointment cancelled successfully"