from sqlalchemy.orm import Session
from app.v1.pacientes.models import PacienteDB, PacienteCreateModel


class PacienteServices:

    def get_paciente_email(self, db: Session, email: str):
        return db.query(PacienteDB).filter(PacienteDB.email == email).first()

    def add(self, db: Session, paciente: PacienteCreateModel):
        novo_paciente = PacienteDB(
            nome=paciente.nome,
            email=paciente.email,
            telefone=paciente.telefone,
            disabled=False
        )
        db.add(novo_paciente)
        db.commit()
        db.refresh(novo_paciente)
        return novo_paciente

    def get_all(self, db: Session):
        return db.query(PacienteDB)\
            .filter(PacienteDB.disabled == False)\
            .order_by(PacienteDB.nome.asc())\
            .all()

    def get_by_id(self, db: Session, id: int):
        return db.query(PacienteDB).filter(PacienteDB.id == id).first()

    def update(self, db: Session, db_paciente: PacienteDB, paciente: PacienteCreateModel):
        db_paciente.nome = paciente.nome
        db_paciente.email = paciente.email
        db_paciente.telefone = paciente.telefone
        db.commit()
        db.refresh(db_paciente)
            
    def delete(self, db: Session, db_paciente: PacienteDB):
        db_paciente.disabled = True
        db.commit()
        db.refresh(db_paciente)
        return db_paciente


paciente_services = PacienteServices()