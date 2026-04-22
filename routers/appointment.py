from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient
from schemas.appointment import AppointmentCreate
from utils.auth import verify_token

router = APIRouter(prefix="/appointments", tags=["Appointments"])

def get_db():
    db = SessionLocal()
    yield db

# create appoinment
@router.post("/")
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    
    doctor = db.query(Doctor).filter(Doctor.id == data.doctor_id).first()
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appointment = Appointment(**data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

# getl all and filter
@router.get("/")
def get_appointments(
    doctor_id: int = Query(None),
    patient_id: int = Query(None),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    query = db.query(Appointment)

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)

    return query.all()

# cancel appoinment
@router.patch("/{id}/cancel")
def cancel_appointment(id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    appointment = db.query(Appointment).filter(Appointment.id == id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "Cancelled"
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment cancelled"}