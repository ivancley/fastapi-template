from fastapi import FastAPI
from app.auth.controller import router as routerAuth

app = FastAPI()

app.include_router(routerAuth)

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}
