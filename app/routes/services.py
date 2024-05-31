from fastapi import FastAPI,HTTPException,APIRouter,Request
from app.models import parent_collection,child_collection,extension_data
from app.schemas import Parent,ParentLogin
from datetime import datetime,timezone
from bson.objectid import ObjectId
import bcrypt
import json

router = APIRouter()

#apps login 

@router.post('/services/login', response_model=dict)
async def services_login(request: Request):
    auth_data = await request.json()
    email = auth_data.get('email')
    pwd = auth_data.get('password')
    service_code = auth_data.get('service_code')
    
    # Find user document by email
    get_parent = await parent_collection.find_one({'email': email})
    
    if not get_parent:
        return {'error': 'Email not found'}
    
    # Check password
    hashed_password = get_parent.get('password')
    if not bcrypt.checkpw(pwd.encode('utf-8'), hashed_password.encode('utf-8')):
        return {'error': 'Incorrect Password'}
    
    # Authentication successful
    #now find out child using service code
    get_child = await child_collection.find_one({'service_code':service_code})
    
    if not get_child:
        return {'error': 'child not found ,check service code'}
   
    return {'message': get_child}

#Google Chrome EXTENSION 
from ..apicalls.keywordsFinder import get_keywords,filter_keywords
@router.post("/services/page-visit-extension",response_model=dict)
async def child_page_history(request:Request):
    history_visits = await request.json()
    child_id = history_visits[0]['child_id']
    if history_visits :
        
    
        unfilterData = history_visits[1:]
        
    
        filtered_data = [
            item for item in unfilterData
            if 'url' not in item or not (item['url'].startswith('chrome:') or item['url'].startswith('http:'))
        ]
        #scrape url for keyword and save this to keyword
        
        keywords = await  get_keywords(filtered_data,"")

        #save history_visit into mongodb
    
        for item in filtered_data:
            item['date']=datetime.now(timezone.utc)
        
        if len(keywords) is not None:
            try:
                saveThese = await extension_data.update_one(
                    {'child_id': child_id}, 
                    {'$push': 
                        {
                            'urls': {'$each': filtered_data},
                            'keywords':{'$each':keywords}
                            }
                    },
                    upsert=True)
              
                
                if saveThese.modified_count > 0 :
                    return {'message': 'Data is saved successfully.'}
                else:
                    return {'message': 'No data was saved.'}
            except Exception as e:
                print(f"Error in DB save: {e}")
                raise HTTPException(status_code=400,detail=f'error : {e}')
        
        
        
       
        
    
    raise HTTPException(status_code=400,detail='work on it')
from ..apicalls.textAnalysis import analyze_text
@router.post("/services/comment-made-extension",response_model=dict)
async def comment_made_extension(request:Request):
    data = await request.json()

    
    child_id = data[1]['child_Id']
    comment = data[0]['comment']
    url =data[0]['form_url']
    
   
    keyword_with_comment = await get_keywords([{"url":url,"sec":0}],str(comment))
    if len(keyword_with_comment) is not None:
            try:
                analyzed_text = await analyze_text(comment)
                jsonString = json.loads(analyzed_text.strip("```json\n```"))
                jsonString['date']=datetime.now(timezone.utc)
                
                saveThese = await extension_data.update_one(
                    {'child_id': child_id}, 
                    {'$push': 
                        {
                            
                            'keywords':{'$each':keyword_with_comment}
                        }
                    },
                    upsert=True)
              
                saveAnalyzed_text = await extension_data.update_one(
                    {'child_id':child_id},
                    {"$set":{
                            "analyzedText":jsonString
                            }
                    },upsert=True
                )
                if saveThese.modified_count > 0 and saveAnalyzed_text.modified_count>0:
                    return {'message': 'Data is saved successfully.'}
                else:
                    return {'message': 'No data was saved.'}
            except Exception as e:
                print(f"Error in DB save: {e}")
                raise HTTPException(status_code=400,detail=f'error : {e}')
    
    
    
    
    raise HTTPException(status_code=400,detail='work on it')




#Apk Webview