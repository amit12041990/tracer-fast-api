from fastapi import FastAPI,HTTPException,APIRouter,Request,Form
from app.models import parent_collection,child_collection
from app.schemas import Child,ChildUpdate
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt
import random
import json
from ..apicalls.textAnalysis import analyze_text
router =APIRouter()

@router.post("/add_child/",response_model=dict)
async def add_child(child:Child):
    print(child.parent_id)
    try:
        
        parent = await parent_collection.find_one({"_id": str(child.parent_id)})
    except Exception as e:
        print(f"error : {e}")
    if not parent:
        raise HTTPException(status_code=404,detail='Parent Not Found')
    
    #generate service key for extension and android 
    while True:
        service_code = "{:08d}".format(random.randint(0, 99999999))
        existing_child = await child_collection.find_one({"service_code": service_code})
        if not existing_child:
            break
    dob_datetime = datetime.combine(child.dob, datetime.min.time())
    # Insert the child data into MongoDB
    child_dict = child.dict(by_alias=True)
    child_dict["_id"] = str(ObjectId())
    child_dict["created_at"] = datetime.now()
    child_dict["service_code"] = service_code  # Add the unique auth_code
    child_dict["dob"]=dob_datetime
    
    result = await child_collection.insert_one(child_dict)
    if result.inserted_id:
        return {"message": "Child added successfully", "child_id": str(result.inserted_id)}

    raise HTTPException(status_code=500, detail="Child could not be added")
    
@router.get("/parent/get-childs/{id}", response_model=dict)
async def getAllChild(id: str):
    try:
        # Find documents matching the parent_id
        id = id.strip()
        query = {'parent_id':id}
       
        childs_cursor = child_collection.find(query)
        
        # Fetch all documents into a list
        childs_document = await childs_cursor.to_list(length=None)
        
        # Check if the list is empty
        if not childs_document:
            return {'error': f"No child found"}
        
        return {'children': childs_document}

    except Exception as e:
        # Return a generic error message if something goes wrong
        return {'error': f"Child fetch failed: {str(e)}"}

    
@router.put("/update_child/", response_model=dict)
async def update_child(updated_child: ChildUpdate):
    # Convert child_id to ObjectId
    try:
        child_id =ObjectId(updated_child.id)
    except :
        raise HTTPException(status_code=400, detail="Invalid id format")

    # Check if the child exists
    existing_child = await child_collection.find_one({"_id": updated_child.id})
    if not existing_child:
        raise HTTPException(status_code=404, detail="Child not found")

    # Update the child data
    update_data = updated_child.dict(exclude={"id"}, exclude_unset=True)
    if update_data:
        await child_collection.update_one({"_id": updated_child.id}, {"$set": update_data})

    return {"message": "Child updated successfully"}

@router.get("/child/delete_child/{child_id}",response_model=dict)
async def delete_child(child_id:str):
    child_id = child_id.strip()
    try:
        IsDeleted = child_collection.find_one_and_delete({"_id":str(child_id)})
        if IsDeleted:
            return {'message':'child deleted successfully'}
    except Exception as e:
        return {'Error':f"{e}"}
    
#Extension Data 


from ..filters.extensionCommentDataFormate import serialiseTextIntoJson

@router.post('/comment',response_model=dict)
async def save_extension_comment(comment: str = Form(...)):
   
    
    data =await analyze_text(comment)
    #convert string response to json object
    comment_list = []
    jsonString = json.loads(data.strip("```json\n```"))
    comment_list.append(jsonString)
    
    #convertTextToJson = serialiseTextIntoJson({'message':data})
    #serialise and filter json object
    """  
    try:
        
        filterForDB = filter_data(convertTextToJson)
    except Exception as e:
        raise HTTPException(status_code=400,detail={'error':f'e'})
    """
    
    
    
     
    print(comment_list)
    return {'message':comment_list}

""" @router.post('/visit') """

    
    
    
    
    