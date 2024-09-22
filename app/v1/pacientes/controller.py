from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.v1.pacientes.models import PacienteCreateModel, PacienteViewModel
from app.v1.pacientes.services import paciente_services as service
from app.v1.utils.db_services import get_db 
from app.v1.auth.security import get_current_user, UsuarioDB 


router = APIRouter()

exception_paciente_ja_cadastrado = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
    detail="Paciente já cadastrado com este e-mail"
)
exception_paciente_nao_encontado = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, 
    detail="Paciente não encontrado"
)

@router.post("/", response_model=PacienteViewModel, status_code=status.HTTP_201_CREATED)
def create_paciente(
    paciente: PacienteCreateModel, 
    db: Session = Depends(get_db),
    current_user: UsuarioDB = Depends(get_current_user)
):
    db_paciente = service.get_paciente_email(db, paciente.email)
    if db_paciente:
        raise exception_paciente_ja_cadastrado
        
    novo_paciente = service.add(db, paciente)
    return novo_paciente


@router.get("/", response_model=List[PacienteViewModel])
def get_pacientes(
    db: Session = Depends(get_db),
    current_user: UsuarioDB = Depends(get_current_user)
):
    return service.get_all(db)


@router.get("/{paciente_id}", response_model=PacienteViewModel)
def get_pacientes_by_id(
    paciente_id: int, 
    db: Session = Depends(get_db),
    current_user: UsuarioDB = Depends(get_current_user)
):
    paciente = service.get_by_id(db, paciente_id)
    if not paciente:
        raise exception_paciente_nao_encontado
    
    return paciente


@router.put("/{paciente_id}", response_model=PacienteViewModel)
def update_pacientes(
    paciente_id: int, 
    updated_paciente: PacienteCreateModel, 
    db: Session = Depends(get_db),
    current_user: UsuarioDB = Depends(get_current_user)
):
    db_paciente = service.get_by_id(db, paciente_id)
    if not db_paciente:
        raise exception_paciente_nao_encontado
    
    service.update(db, db_paciente, updated_paciente)
    return db_paciente


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def del_delete_paciente(
    paciente_id: int, 
    db: Session = Depends(get_db),
    current_user: UsuarioDB = Depends(get_current_user)
):
    db_paciente = service.get_by_id(db, paciente_id)
    if not db_paciente:
        raise exception_paciente_nao_encontado
    
    service.delete(db, db_paciente)
    return db_paciente
