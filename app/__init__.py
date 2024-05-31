from fastapi import FastAPI
from .routes import parent,child,services
from fastapi.middleware.cors import CORSMiddleware



app =FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(parent.router)
app.include_router(child.router)
app.include_router(services.router)
@app.get("/")
async def welcome():
    return ({'hello':'world'})