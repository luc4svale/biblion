"""truncate name of file_path and cover_image_path columns on books table

Revision ID: c66d0c852fc1
Revises: a58490337495
Create Date: 2025-03-03 19:08:02.646804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66d0c852fc1'
down_revision = 'a58490337495'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file', sa.String(length=70), nullable=False))
        batch_op.add_column(sa.Column('cover', sa.String(length=70), server_default='default-cover.jpg', nullable=False))
        batch_op.drop_column('file_path')
        batch_op.drop_column('cover_image_path')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cover_image_path', sa.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('file_path', sa.VARCHAR(length=255), nullable=False))
        batch_op.drop_column('cover')
        batch_op.drop_column('file')

    # ### end Alembic commands ###
