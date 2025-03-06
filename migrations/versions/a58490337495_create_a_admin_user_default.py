"""Create a admin user default

Revision ID: a58490337495
Revises: 8a90405f986b
Create Date: 2025-03-03 16:32:44.542132

"""

from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# revision identifiers, used by Alembic.
revision = 'a58490337495'
down_revision = '8a90405f986b'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    admin_user = {
        'id': '188bfdca-c0f5-4424-a12c-ec4c5de8c9e3',
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password': bcrypt.generate_password_hash('Admin123@').decode('utf-8'),
        'role': 'admin',
        'photo': 'default-photo.svg',
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc)
    }

    conn.execute(
        sa.text("""
            INSERT INTO users (id, first_name, last_name, email, password, role, photo, created_at, updated_at)
            VALUES (:id, :first_name, :last_name, :email, :password, :role, :photo, :created_at, :updated_at)
            ON CONFLICT (email) DO NOTHING;
        """), admin_user
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM users WHERE email = 'admin@example.com'"))

