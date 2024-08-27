import time

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal

app = FastAPI()

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware
async def add_process_time_header(request: Request):
    print("in add_process_time_header middleware.") # dummy message
    api_key = request.headers.get("X-Api-Key")
    if api_key != "my_secret_api_key":
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get('/', dependencies=[Depends(add_process_time_header)])
async def app_root():
    return { 'message': 'Helloworld' }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8888)