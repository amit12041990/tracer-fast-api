from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

#applying connection
MONGO_CONNECTION_DETAIL = os.getenv('MONGO_DETAILS')

#DB Detail
client = AsyncIOMotorClient(MONGO_CONNECTION_DETAIL)
db=client.tracer_ai_db
parent_collection = db.parent
child_collection = db.child 

extension_data=db.extension_data


