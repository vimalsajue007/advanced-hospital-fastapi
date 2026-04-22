from fastapi import APIRouter
from schemas.auth import Login
from utils.auth import create_token

router = APIRouter()

@router.post("/login")
def login(data: Login):
    if data.username == "admin" and data.password == "admin":
        return {"token": create_token({"user": data.username})}
    return {"error": "Invalid credentials"}