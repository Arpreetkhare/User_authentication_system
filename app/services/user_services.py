import uuid
from fastapi.exceptions import HTTPException
from fastapi import Request, status
from datetime import datetime,timedelta

import redis
from app.dependencies.auth_dependency import create_access_token, logout_user , get_current_user , validate_token
from app.models.user_models import User
from app.crud.user_crud import get_user_by_username , create_user
from app.helper.user_helper import hash_password , verify_password , logger


redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

class UserService:
    @staticmethod
    async def register_user(request: User, db):
        try :

            existing_user = await get_user_by_username(db, request.username)
            if existing_user:
                logger.warning(f"Registration failed: User '{request.username}' already exists.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already exists"
                )

            hashed_password = hash_password(request.password)

            new_user = {
                "user_id": str(uuid.uuid4()),
                "username": request.username.strip(),
                "password": hashed_password,
                "created_at": datetime.utcnow().isoformat()
            }

            result = await create_user(db, new_user)
            logger.info(f"User '{request.username}' registered successfully.")
            return {"id": str(result.inserted_id), "username": request.username}
        
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )

    @staticmethod
    async def login_user(request:User,db) :
        try:
            user = await  get_user_by_username(db,request.username) 

            if not user or not verify_password(request.password , user["password"]) :
                logger.warning(f"Login failed for user '{request.username}': Invalid credentials.")
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            

            access_token = create_access_token(
            data = {
                "sub": str(user["user_id"]), 
                "username": str(user["username"])
                
            } , expire_delta=timedelta(hours=1) 
            )

            redis_client.set(str(user["user_id"]), access_token, ex=3600)  # Set expiry to 1 hour

            logger.info(f"User '{request.username}' logged in successfully.")
            return {"access_token": access_token, "token_type": "bearer"}
       
        
        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )
        
    @staticmethod
    async def logout_user(current_user):
        """
            Logs out the authenticated user by invalidating their token.
        """
        try:
            user_id = current_user
            if not user_id:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token: user_id is missing or invalid"
            )
            logout_user(user_id)  # Invalidate token
            logger.info(f"User '{current_user}' logging out")
            return {"message": "User logged out successfully."}
        except Exception as e:
            logger.error(f'Error during user logout : {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal error: {str(e)}"
            )



            