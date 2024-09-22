## Projeto Base (Boilerplate) para desenvolvimento de aplicações REST utilizando os frameworks

Este é um projeto de API desenvolvido com **FastAPI**, utilizando **SQLAlchemy** como ORM e aplicando o conceito de versionamento de API para suportar diferentes versões (v1, v2, v3, etc.). A estrutura é granular para facilitar a manutenção, escalabilidade e organização do código.

## Funcionalidades
- Autenticação com **JWT** usando email e senha.
- Criação e gerenciamento de usuários.
- Suporte a múltiplas versões da API (`v1`, `v2`, etc.).
- Integração com banco de dados usando **SQLAlchemy**.
- Migrações de banco de dados com **Alembic**.

## Requisitos

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **Uvicorn** (para rodar o servidor)
- **PostgreSQL** (ou outro banco de dados compatível)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/ivancley/fastapi-template.git
cd fastapi-template
```

2. Crie e ative o ambiente virtual:
```bash
python - venv .venv 
source .venv/bin/active 
pip install -r requirements.txt 
```

3. Configure as variáveis de ambiente no arquivo .env:
```bash
SECRET_KEY="sua_chave_secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL="postgresql://usuario:senha@localhost:5432/seu_banco"
```

4. Execute a migração do Banco:
```bash
alembic upgrade head
```

5. Execute o projeto:
```bash
fastapi dev main.py 
```

### Endpoints Principais
#### Autenticação
**POST** /v1/login: Autentica o usuário utilizando email e senha e retorna um token JWT.
#### Usuários
**POST** /v1/usuarios/novo/: Cria um novo usuário.
**GET** /v1/usuarios/eu/: Retorna as informações do usuário autenticado.

### Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.