from app.schemas import User, UserRole
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
            language="ja",
            password=pwd_context.hash("pass123"),  # Hashed password
            role=UserRole.DOCTOR
        ),
        User(
            username="patient1",
            role=UserRole.PATIENT,  # Use UserRole.patient enum
            language="ru",
            password=pwd_context.hash("pass123")  # Hashed password
        ),
        User(
            username="patient2",
            language="ur",
            password=pwd_context.hash("pass123"),  # Hashed password
            role=UserRole.PATIENT
        )
    ]
}
