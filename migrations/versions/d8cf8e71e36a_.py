"""empty message

Revision ID: d8cf8e71e36a
Revises: b685343826e3
Create Date: 2023-04-06 19:32:27.690432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8cf8e71e36a'
down_revision = 'b685343826e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visitor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('visit_time', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visitor', schema=None) as batch_op:
        batch_op.drop_column('visit_time')

    # ### end Alembic commands ###
