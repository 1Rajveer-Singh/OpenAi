from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.models.database import get_db
from app.models.schemas import User
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class UserCreate(BaseModel):
    username: str
    email: str
    phone: str
    password: str
    full_name: str
    business_name: str
    business_type: str
    preferred_language: str = "hi"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

def verify_password(plain_password, hashed_password):
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email) |
        (User.phone == user_data.phone)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username, email, or phone already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        business_name=user_data.business_name,
        business_type=user_data.business_type,
        preferred_language=user_data.preferred_language
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "business_name": new_user.business_name,
            "business_type": new_user.business_type,
            "preferred_language": new_user.preferred_language
        }
    }

@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    
    # Find user
    user = db.query(User).filter(User.username == user_credentials.username).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "business_name": user.business_name,
            "business_type": user.business_type,
            "preferred_language": user.preferred_language
        }
    }

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "full_name": current_user.full_name,
        "business_name": current_user.business_name,
        "business_type": current_user.business_type,
        "preferred_language": current_user.preferred_language,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }

@router.put("/profile")
async def update_profile(
    full_name: str = None,
    business_name: str = None,
    business_type: str = None,
    preferred_language: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    
    if full_name:
        current_user.full_name = full_name
    if business_name:
        current_user.business_name = business_name
    if business_type:
        current_user.business_type = business_type
    if preferred_language:
        current_user.preferred_language = preferred_language
    
    current_user.updated_at = datetime.now()
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Profile updated successfully",
        "user_info": {
            "id": current_user.id,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "business_name": current_user.business_name,
            "business_type": current_user.business_type,
            "preferred_language": current_user.preferred_language
        }
    }