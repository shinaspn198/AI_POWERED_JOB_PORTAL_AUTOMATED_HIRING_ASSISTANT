from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from api.database import get_db
from api.models.user import User


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# JWT settings
SECRET_KEY = "zecpath-ai-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Create JWT access token
def create_access_token(user_id: int, role: str):
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# -------------------------
# SIGNUP
# -------------------------

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    password: str
    role: str


@router.post("/signup")
def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):

    # Validate role
    if user_data.role not in ["job_seeker", "recruiter"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be job_seeker or recruiter"
        )

    # Check existing email
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = pwd_context.hash(
        user_data.password
    )

    # Create user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed_password,
        role=user_data.role,
        profile_completed=False,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "profile_completed": new_user.profile_completed
    }


# -------------------------
# LOGIN
# -------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):

    # Find user by email
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not pwd_context.verify(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        user.id,
        user.role
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "profile_completed": user.profile_completed
    }