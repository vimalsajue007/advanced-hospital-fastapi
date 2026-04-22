from pydantic import BaseModel, Field

class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str

class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    phone: str | None = None