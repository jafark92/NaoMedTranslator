from pydantic import BaseModel
from enum import Enum
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(BaseModel):
    username: str
    role: UserRole
    language: str
    password: str  # Store hashed password


# Mock database (replace with real DB in production)
fake_db = {
    "users": [
        User(
            username="doctor1",
            role=UserRole.DOCTOR,  # Use UserRole.DOCTOR enum
            language="en",
            password=pwd_context.hash("pass123")  # Hashed password
        ),
        User(
            username="doctor2",
            language="es",
            password=pwd_context.hash("pass123"),  # Hashed password
            role=UserRole.DOCTOR
        ),
        User(
            username="patient1",
            role=UserRole.PATIENT,  # Use UserRole.patient enum
            language="fr",
            password=pwd_context.hash("pass123")  # Hashed password
        ),
        User(
            username="patient2",
            language="hi",
            password=pwd_context.hash("pass123"),  # Hashed password
            role=UserRole.PATIENT
        )
    ]
}
