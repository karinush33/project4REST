from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from auth import create_access_token
import dal_users
from typing import List

"""
Router for User Management.
"""

router = APIRouter(tags=["Users"])

class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=100)

class LoginRequest(BaseModel):
    user_name: str
    password: str

@router.post("/users", status_code=201)
def register(user: UserCreate):
    """
    Registers a new user in the system.
    """
    success = dal_users.insert_user(user.user_name, user.email, user.password)
    if not success:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return {"message": "User created successfully"}

@router.post("/auth/login")
def login(login_data: LoginRequest):
    """
    Authenticates a user and returns a JWT token.
    """
    user = dal_users.get_user_by_username(login_data.user_name)
    if not user or not dal_users.verify_password(login_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user['user_name'])
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users")
def list_users():
    """
    Returns a list of all registered users (for Management Page).
    """
    return dal_users.get_all_users()

@router.put("/users/{user_id}")
def update_user(user_id: int, email: str):
    """
    Updates the email of an existing user.
    """
    dal_users.update_user_email(user_id, email)
    return {"message": "Updated"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Deletes a user from the system by ID.
    """
    dal_users.delete_user(user_id)
    return {"message": "Deleted"}