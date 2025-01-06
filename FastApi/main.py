from fastapi import FastAPI
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import auth_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)