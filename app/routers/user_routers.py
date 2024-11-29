from app.database.database import get_db
from fastapi import APIRouter,Depends, Request
from app.dependencies.auth_dependency import validate_token , get_current_user
from app.models.user_models import User
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.user_services import UserService


router=APIRouter()




@router.post("/register")
async def register_user_route(
    request:User , 
    db:AsyncIOMotorClient= Depends(get_db)):

    """
        user router to rgister user:

        params:
        - `request`: A paydantic model containing the user registration data
        - `db` : The MongoDB database client.


        return : 
        - The user details (excluding sensitive data like  password)

    """
    
    return await UserService.register_user(request,db)
    


@router.post("/login")
async def login_user(
    request:User,
    db:AsyncIOMotorClient=Depends(get_db)):

    """
        Logs in a user.

        This route authenticates the user based on their username and password and returns a JWT token 
        or an error if authentication fails.
        
    """


    
    return await UserService.login_user(request, db)
       
        
   



@router.post("/logout")
async def logout_user(
    current_user: str = Depends(get_current_user)
    ):

    """
        Logs out the authenticated user.

        This route remove the token from the temp storage (redis) to make user logout 
        
    """
    return await UserService.logout_user(current_user)
    

    
        