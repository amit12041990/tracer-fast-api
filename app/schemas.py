from pydantic import BaseModel , EmailStr,Field
from datetime import date,datetime
class Parent(BaseModel):
    username:str
    password:str
    email:EmailStr
    
class ParentLogin(BaseModel):
    email: EmailStr
    password: str

class Child(BaseModel):
    name:str
    gender:str
    dob:date
    parent_id: str = Field(..., alias="parent_id")

class ChildUpdate(BaseModel):
    name:str
    gender:str
    dob:datetime
    id:str
   
    
    
    