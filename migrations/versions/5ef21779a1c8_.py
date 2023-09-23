"""empty message

Revision ID: 5ef21779a1c8
Revises: c0ac92f5bada
Create Date: 2023-04-26 00:23:50.196379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ef21779a1c8'
down_revision = 'c0ac92f5bada'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parecord',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('person_type', sa.Integer(), nullable=False),
    sa.Column('le_type', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parecord')
    # ### end Alembic commands ###