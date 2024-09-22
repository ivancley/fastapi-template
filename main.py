from fastapi import FastAPI
from app.v1.auth.controller import router as routerAuth
from app.v1.pacientes.controller import router as routerPacientes

app = FastAPI()

app.include_router(routerAuth, prefix="/v1")
app.include_router(routerPacientes, prefix="/v1/pacientes")

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}
