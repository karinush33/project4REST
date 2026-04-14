import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta, timezone
import dal_users

"""
Authentication module for managing JWT tokens and user validation.
"""

SECRET_KEY = "running-app-secret-key"
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()

def create_access_token(user_name: str) -> str:
    """ Generates a JWT access token for a successfully logged-in user. """
    payload = {
        "sub": user_name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """ Validates the provided JWT token and returns the corresponding user from the DB. """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("sub")
        if not user_name:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = dal_users.get_user_by_username(user_name)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")