"""Add photo column on users table

Revision ID: 088419cfb4f7
Revises: c165dd068c2e
Create Date: 2025-03-01 01:19:55.854702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '088419cfb4f7'
down_revision = 'c165dd068c2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo', sa.String(length=70), server_default='default-photo.svg', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('photo')

    # ### end Alembic commands ###
