from fastapi import FastAPI
from app.v1.auth.controller import router as routerAuth
from app.v1.pacientes.controller import router as routerPacientes

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()

app.include_router(routerAuth, prefix="/v1")
app.include_router(routerPacientes, prefix="/v1/pacientes")


@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"erro": "Não autenticado"}
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
