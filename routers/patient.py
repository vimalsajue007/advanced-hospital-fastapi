from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate
from utils.auth import verify_token

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    yield db

# create
@router.post("/")
def create_patient(data: PatientCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    patient = Patient(**data.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

# get all and search
@router.get("/")
def get_patients(
    search: str = Query(None),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    query = db.query(Patient)
    
    if search:
        query = query.filter(
            (Patient.name.ilike(f"%{search}%")) |
            (Patient.phone.ilike(f"%{search}%"))
        )
    
    return query.all()

# update
@router.put("/{id}")
def update_patient(id: int, data: PatientUpdate, db: Session = Depends(get_db), user=Depends(verify_token)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

# delete
@router.delete("/{id}")
def delete_patient(id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}