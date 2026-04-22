from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate
from utils.auth import verify_token

router = APIRouter(prefix="/doctors", tags=["Doctors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create
@router.post("/")
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    doctor = Doctor(**data.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

# get all and filter
@router.get("/")
def get_doctors(
    specialization: str = Query(None),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    query = db.query(Doctor)
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    
    return query.all()

# update
@router.put("/{id}")
def update_doctor(id: int, data: DoctorUpdate, db: Session = Depends(get_db), user=Depends(verify_token)):
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(doctor, key, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor

# delete
@router.delete("/{id}")
def delete_doctor(id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted"}

# activate / deactivate
@router.patch("/{id}/status")
def toggle_doctor(id: int, is_active: bool, db: Session = Depends(get_db), user=Depends(verify_token)):
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doctor.is_active = is_active
    db.commit()
    db.refresh(doctor)
    return {"message": "Status updated", "is_active": doctor.is_active}