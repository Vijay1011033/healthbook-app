from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

# Initial doctor data
doctors_data = [
    {"name": "Dr. Arjun Krishnan", "specialty": "Cardiology", "slots_per_day": 8},
    {"name": "Dr. Priya Venkatesh", "specialty": "Pediatrics", "slots_per_day": 10},
    {"name": "Dr. Rajesh Subramaniam", "specialty": "Orthopedics", "slots_per_day": 6},
    {"name": "Dr. Lakshmi Ramachandran", "specialty": "Gynecology", "slots_per_day": 8},
    {"name": "Dr. Karthik Narayanan", "specialty": "Dermatology", "slots_per_day": 12},
    {"name": "Dr. Deepa Iyer", "specialty": "Neurology", "slots_per_day": 6}
]

def init_db():
    db = SessionLocal()
    try:
        # Check if we already have doctors
        existing_doctors = db.query(models.Doctor).all()
        if not existing_doctors:
            # Add doctors only if the table is empty
            for doctor_data in doctors_data:
                db_doctor = models.Doctor(**doctor_data)
                db.add(db_doctor)
            db.commit()
            print("Database initialized with doctor data")
        else:
            print("Doctors already exist in database")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()