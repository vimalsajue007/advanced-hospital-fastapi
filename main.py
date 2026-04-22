from fastapi import FastAPI
from database import Base, engine

from routers import doctor, patient, appointment, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)

@app.get("/")
def home():
    return {"message": "API Running"}