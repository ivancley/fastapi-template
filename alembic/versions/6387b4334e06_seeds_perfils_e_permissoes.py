"""seeds perfils e permissoes

Revision ID: 6387b4334e06
Revises: 8d269a0c1b93
Create Date: 2024-09-28 18:45:16.264825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6387b4334e06'
down_revision: Union[str, None] = '8d269a0c1b93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'permissions',
            sa.column('name', sa.String),
            sa.column('description', sa.String)
        ),
        [
            {'name': 'permission_list', 'description': 'Listar permissões'},
            {'name': 'permission_create', 'description': 'Criar permissões'},
            {'name': 'permission_update', 'description': 'Atualizar a permissões'},
            {'name': 'permission_delete', 'description': 'Deletar a permissões'},
            {'name': 'read_me', 'description': 'Ler minhas informações'},
            {'name': 'paciente_list', 'description': 'Listar pacientes'},
            {'name': 'paciente_create', 'description': 'Criar pacientes'},
            {'name': 'paciente_read', 'description': 'Ler paciente'},
            {'name': 'paciente_update', 'description': 'Atualizar paciente'},
            {'name': 'paciente_delete', 'description': 'Deletar paciente'}
        ]
    )

    op.bulk_insert(
        sa.table(
            'roles',
            sa.column('name', sa.String),
            sa.column('description', sa.String)
        ),
        [
            {'name': 'superuser', 'description': 'Superuser usuário com acesso completo'},
            {'name': 'user', 'description': 'Usuário padrão do sistema'}
        ]
    )

    superuser_permissions = [
        'permission_list', 'permission_create', 'permission_update', 'permission_delete'
    ]
    for perm in superuser_permissions:
        op.execute(
            f"INSERT INTO role_permissions (role_id, permission_id) "
            f"SELECT roles.id, permissions.id FROM roles, permissions "
            f"WHERE roles.name = 'superuser' AND permissions.name = '{perm}'"
        )

    usuario_permissions = [
        'read_me', 'paciente_list', 'paciente_create', 'paciente_read', 'paciente_update', 'paciente_delete'
    ]
    for perm in usuario_permissions:
        op.execute(
            f"INSERT INTO role_permissions (role_id, permission_id) "
            f"SELECT roles.id, permissions.id FROM roles, permissions "
            f"WHERE roles.name = 'usuario' AND permissions.name = '{perm}'"
        )


def downgrade() -> None:
    op.execute("DELETE FROM role_permissions WHERE role_id IN (SELECT id FROM roles WHERE name IN ('superuser', 'usuario'))")
    op.execute("DELETE FROM roles WHERE name IN ('superuser', 'usuario')")
    op.execute("DELETE FROM permissions WHERE name IN ('permission_list', 'permission_create', 'permission_update', 'permission_delete', 'read_me', 'paciente_list', 'paciente_create', 'paciente_read', 'paciente_update', 'paciente_delete')")
