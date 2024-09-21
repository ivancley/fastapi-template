from fastapi import FastAPI
from auth import auth

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}
