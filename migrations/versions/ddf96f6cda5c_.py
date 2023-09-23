"""empty message

Revision ID: ddf96f6cda5c
Revises: be2efef5d418
Create Date: 2023-04-12 00:54:53.228222

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ddf96f6cda5c'
down_revision = 'be2efef5d418'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resident', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('workplace', sa.String(length=100), nullable=False))
        batch_op.alter_column('phone_num',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=20),
               existing_nullable=False)

    with op.batch_alter_table('visitor', schema=None) as batch_op:
        batch_op.alter_column('phone_num',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visitor', schema=None) as batch_op:
        batch_op.alter_column('phone_num',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('resident', schema=None) as batch_op:
        batch_op.alter_column('phone_num',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('workplace')
        batch_op.drop_column('unit')

    # ### end Alembic commands ###