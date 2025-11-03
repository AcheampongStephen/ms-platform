from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.models import UserCreate, User, UserUpdate, Token
from app.database import get_database
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return payload

@router.post("/users/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    db = get_database()
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user
    user_dict = user.model_dump(exclude={"password"})
    user_dict["hashed_password"] = hashed_password
    
    from datetime import datetime
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    user_dict["is_active"] = True
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    logger.info(f"User registered: {user.email}")
    
    return User(
        id=str(created_user["_id"]),
        email=created_user["email"],
        name=created_user["name"],
        phone=created_user.get("phone"),
        created_at=created_user["created_at"],
        is_active=created_user["is_active"]
    )

@router.post("/users/login", response_model=Token)
async def login(email: str, password: str):
    db = get_database()
    
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    access_token = create_access_token(data={"sub": str(user["_id"])})
    logger.info(f"User logged in: {email}")
    
    return Token(access_token=access_token)

@router.get("/users/me", response_model=User)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = current_user["sub"]
    
    from bson import ObjectId
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        phone=user.get("phone"),
        created_at=user["created_at"],
        is_active=user["is_active"]
    )

@router.put("/users/me", response_model=User)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    user_id = current_user["sub"]
    
    from bson import ObjectId
    from datetime import datetime
    
    update_data = user_update.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    return User(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        phone=user.get("phone"),
        created_at=user["created_at"],
        is_active=user["is_active"]
    )