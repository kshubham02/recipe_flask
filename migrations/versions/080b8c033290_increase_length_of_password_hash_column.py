"""Increase length of password_hash column

Revision ID: 080b8c033290
Revises: 7e3ce6652f6f
Create Date: 2024-06-12 14:13:26.874526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '080b8c033290'
down_revision = '7e3ce6652f6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=1128),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=1128),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###
