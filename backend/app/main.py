from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import doctors

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Appointment Booking System",
    description="API for managing doctor appointments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doctors.router, tags=["doctors"])