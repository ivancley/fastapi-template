from fastapi import FastAPI
from app.v1.auth.controller import router as routerAuth

app = FastAPI()

app.include_router(routerAuth, prefix="/v1")

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}
