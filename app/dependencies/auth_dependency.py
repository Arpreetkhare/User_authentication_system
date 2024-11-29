from datetime import datetime, timedelta
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, Request, HTTPException, status
import jwt
import redis

# Redis connection setup
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)


# Load environment variables
load_dotenv()

# Retrieve values from environment variables (or use defaults)
SECRET_KEY = os.getenv("SECRET_KEY", "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Function to create an access token
def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # Use expire_delta if provided, else use the default expiration time
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    
    # Encode the JWT token with the specified algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    redis_client.set(to_encode["sub"], encoded_jwt, ex=3600)
    return encoded_jwt

# Function to validate the token from request header
def validate_token(request: Request) -> dict:
    auth_header = request.headers.get("Authorization") or request.headers.get("authentication")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]  # Extract token from the "Bearer <token>" format
        try:
            # Decode and verify the token
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Ensure the decoded token contains the user information
            if "sub" not in decoded:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing user information")
            
            stored_token = redis_client.get(decoded["sub"])
            if not stored_token or stored_token != token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid or has been logged out")
            
            # Attach the user information to the request state
            request.state.user = decoded["sub"]  # You can store other user info if needed
            return decoded["sub"]   # Return the user information if the token is valid

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing from header!")




def logout_user(user_id: str):
    # Remove token from Redis
    redis_client.delete(user_id)

# Dependency to get current user from token
def get_current_user(request: Request, user: dict = Depends(validate_token)) -> dict:
    return request.state.user  # Return the user attached to the request state
