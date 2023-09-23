"""empty message

Revision ID: 4fb0d6325190
Revises: f4f3d7a617fe
Create Date: 2023-05-20 13:39:13.053072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4fb0d6325190'
down_revision = 'f4f3d7a617fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mapmark', schema=None) as batch_op:
        batch_op.alter_column('long',
               existing_type=mysql.FLOAT(),
               type_=sa.Numeric(precision=9, scale=6),
               existing_nullable=False)
        batch_op.alter_column('lat',
               existing_type=mysql.FLOAT(),
               type_=sa.Numeric(precision=9, scale=6),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mapmark', schema=None) as batch_op:
        batch_op.alter_column('lat',
               existing_type=sa.Numeric(precision=9, scale=6),
               type_=mysql.FLOAT(),
               existing_nullable=False)
        batch_op.alter_column('long',
               existing_type=sa.Numeric(precision=9, scale=6),
               type_=mysql.FLOAT(),
               existing_nullable=False)

    # ### end Alembic commands ###
