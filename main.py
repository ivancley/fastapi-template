from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
from app.v1.auth.controller import router as routerAuth
from app.v1.pacientes.controller import router as routerPacientes
import json


app = FastAPI()

app.include_router(routerAuth, prefix="/v1")
app.include_router(routerPacientes, prefix="/v1/pacientes")



@app.middleware("http")
async def custom_response_middleware(request: Request, call_next):
    response = await call_next(request)

    content = await response.text()  # Read response content as string

    new_response = {
        "version_system": "1.1",
        "status_code": response.status_code,
        "data": json.loads(content),  # Parse string as JSON
        "error": None
    }

    return response

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}
