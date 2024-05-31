from fastapi import FastAPI,HTTPException,APIRouter,Request
from app.models import parent_collection
from app.schemas import Parent,ParentLogin
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt

router = APIRouter()

@router.post('/register/', response_model=dict)
async def register(parent: Parent):
    #print(parent.model_dump())
    hashed_password = bcrypt.hashpw(parent.password.encode('utf-8'), bcrypt.gensalt())
    
    parent_dict = parent.dict()
    parent_dict["password"] = hashed_password.decode('utf-8')
    parent_dict["_id"] = str(ObjectId())
    parent_dict["created_at"]=datetime.now()
    
    # Insert the user data into MongoDB
    result = await parent_collection.insert_one(parent_dict)
    if result.inserted_id:
        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    
    raise HTTPException(status_code=500, detail="User could not be created")


@router.post('/login',response_model=dict)
async def login(parent:ParentLogin):
    #fetch data
    user = await parent_collection.find_one({"email":parent.email})
    if not user:
        raise HTTPException(status_code=404,detail='Email Not Found')
    if not bcrypt.checkpw(parent.password.encode('utf-8'), user['password'].encode('utf-8')):
         raise HTTPException(status_code=404,detail='Incorrect Password')
    
    return {
        "message": "Login successful",
        "user": {
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
            "_id":str(user["_id"])
        }
    }

   
@router.get("/parent/{id}", response_model=dict)
async def provide_parent(id: str):

    parent = await parent_collection.find_one({"_id":id})
    
    if parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    parent.pop('password',None)
    return parent


@router.put('/parent/{id}/change-password', response_model=dict)
async def change_password(id: str, request: Request):
    request_data = await request.json()
    print(request_data)
    new_password = request_data.get("newPassword")
    old_password = request_data.get("oldPassword")
    
    if not ObjectId.is_valid(id):
        return {"error": "Invalid ID format"}
    
    parent_document = await parent_collection.find_one({"_id": str(id)})
    
    if parent_document is None:
        return {"error": "No user found"}
    
    hashed_password = parent_document.get('password')
    
    
    if len(new_password) < 4 or len(new_password) > 8:
        return {"error": "New password length must be between 4 and 8 characters"}
        
        
    if not bcrypt.checkpw(old_password.encode('utf-8'), hashed_password.encode('utf-8')):
        return {"error": "Old password is incorrect"}
    
    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    updated_document = await parent_collection.find_one_and_update(
        {"_id": str(id)},
        {"$set": {"password": hashed_new_password.decode('utf-8')}}
    )
    
    if updated_document is None:
        return {"error": "Could not process your request"}
    
    return {"message": "Password updated successfully"}


