from fastapi import FastAPI
from app.database.database import get_db
from fastapi.exceptions import HTTPException
from app.routers.user_routers import router



app=FastAPI()
db=get_db()



        

@app.on_event("startup")
async def startup_event():
    try:
        # Check if we can access the database collections (as MongoDB does not use SQL)
        db.list_collection_names()
        print("MongoDB connected")
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))
        raise HTTPException(status_code=500, detail="Database connection failed")

# Root endpoint to check API status
@app.get("/")
async def read_root():
    return {"message": "API is running"}
app.include_router(router, tags=["router"])

# app.include_router(,tags=['router'])












