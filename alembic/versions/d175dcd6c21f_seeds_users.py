"""seeds users

Revision ID: d175dcd6c21f
Revises: 6387b4334e06
Create Date: 2024-09-28 18:49:48.867852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# revision identifiers, used by Alembic.
revision: str = 'd175dcd6c21f'
down_revision: Union[str, None] = '6387b4334e06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tabela_user = sa.table(
    "users",
    sa.column("id", sa.Integer),
    sa.column("email", sa.String),
    sa.column("hashed_password", sa.String),
    sa.column("nome", sa.String)
)

tabela_roles = sa.table(
    "user_roles",
    sa.column("user_id", sa.Integer),
    sa.column("role_id", sa.Integer),
)


def upgrade() -> None:
    op.bulk_insert(
        tabela_user,
        [
            {
                "email": "admin@gmail.com",
                "hashed_password": pwd_context.hash("12345678"),
                "nome": "admin"
            }
        ],
    )

    op.bulk_insert(
        tabela_user,
        [
            {
                "email": "usuario@gmail.com",
                "hashed_password": pwd_context.hash("12345678"),
                "nome": "usuario",
            }
        ],
    )

    conn = op.get_bind()

    admin_user_id = conn.execute(sa.text("SELECT id FROM users WHERE nome = 'admin'")).fetchone()[0]
    usuario_user_id = conn.execute(sa.text("SELECT id FROM users WHERE nome = 'usuario'")).fetchone()[0]

    superuser_role_id = conn.execute(sa.text("SELECT id FROM roles WHERE name = 'superuser'")).fetchone()[0]
    usuario_role_id = conn.execute(sa.text("SELECT id FROM roles WHERE name = 'user'")).fetchone()[0]

    op.bulk_insert(tabela_roles, [
        {'user_id': admin_user_id, 'role_id': superuser_role_id},
        {'user_id': usuario_user_id, 'role_id': usuario_role_id}
    ])


def downgrade() -> None:
    conn = op.get_bind()

    admin_user_id = conn.execute(sa.text("SELECT id FROM users WHERE username = 'admin'")).fetchone()[0]
    usuario_user_id = conn.execute(sa.text("SELECT id FROM users WHERE username = 'usuario'")).fetchone()[0]

    op.execute(f"DELETE FROM user_roles WHERE user_id IN ({admin_user_id}, {usuario_user_id})")
    op.execute(f"DELETE FROM users WHERE id IN ({admin_user_id}, {usuario_user_id})")
