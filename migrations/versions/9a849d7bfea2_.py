"""empty message

Revision ID: 9a849d7bfea2
Revises: e1c5ddf6b6e3
Create Date: 2023-02-20 20:22:02.393010

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9a849d7bfea2'
down_revision = 'e1c5ddf6b6e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email', schema=None) as batch_op:
        batch_op.drop_column('sender')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sender', mysql.VARCHAR(length=100), nullable=False))

    # ### end Alembic commands ###
