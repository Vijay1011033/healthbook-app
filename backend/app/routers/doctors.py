from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from .. import models, schemas

router = APIRouter()

@router.post("/doctors/", response_model=schemas.Doctor)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    if doctor.slots_per_day <= 0:
        raise HTTPException(status_code=400, detail="Slots per day must be positive")
    
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.get("/doctors/", response_model=List[schemas.Doctor])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

@router.get("/doctors/{doctor_id}", response_model=schemas.Doctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/doctors/{doctor_id}/appointments/", response_model=schemas.Appointment)
def create_appointment(
    doctor_id: int,
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Convert string to datetime if needed
    if isinstance(appointment.appointment_date, str):
        try:
            appointment_date = datetime.fromisoformat(appointment.appointment_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)")
    else:
        appointment_date = appointment.appointment_date

    # Parse time slot
    try:
        time_parts = appointment.time_slot.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        # Update appointment date with the correct time
        appointment_date = appointment_date.replace(hour=hour, minute=minute)
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid time slot format. Please use HH:MM format")

    # Validate appointment time (9 AM - 5 PM)
    if hour < 9 or hour >= 17:
        raise HTTPException(status_code=400, detail="Appointments only available between 9 AM and 5 PM")

    # Check if the specific time slot is already booked
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date == appointment_date,
        models.Appointment.time_slot == appointment.time_slot,
        models.Appointment.is_cancelled == False
    ).first()

    if existing_appointment:
        raise HTTPException(status_code=400, detail="This time slot is already booked")

    # Check if doctor has reached their daily appointment limit
    appointments_on_date = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date >= appointment_date.replace(hour=0, minute=0),
        models.Appointment.appointment_date < appointment_date.replace(hour=0, minute=0) + timedelta(days=1),
        models.Appointment.is_cancelled == False
    ).count()

    if appointments_on_date >= doctor.slots_per_day:
        raise HTTPException(status_code=400, detail="No available slots for this day")

    db_appointment = models.Appointment(
        **appointment.dict(),
        doctor_id=doctor_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/doctors/{doctor_id}/available-slots/{date}")
def get_available_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Get all booked appointments for the doctor on the selected date
    booked_slots = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date >= selected_date,
        models.Appointment.appointment_date < selected_date + timedelta(days=1),
        models.Appointment.is_cancelled == False
    ).all()

    # Create a list of all possible time slots (9 AM to 5 PM)
    all_slots = [f"{hour:02d}:00" for hour in range(9, 17)]
    booked_times = [appointment.time_slot for appointment in booked_slots]

    # Filter out booked slots
    available_slots = [slot for slot in all_slots if slot not in booked_times]

    # Limit available slots based on doctor's slots_per_day setting
    if len(available_slots) > (doctor.slots_per_day - len(booked_slots)):
        available_slots = available_slots[:doctor.slots_per_day - len(booked_slots)]

    return {
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": available_slots,
        "total_slots": doctor.slots_per_day,
        "booked_slots": len(booked_slots)
    }

@router.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.is_cancelled = True
    db.commit()
    return {"message": "Appointment cancelled successfully"}