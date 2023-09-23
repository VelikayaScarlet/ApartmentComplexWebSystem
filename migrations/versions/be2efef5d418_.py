"""empty message

Revision ID: be2efef5d418
Revises: 5f5f467666ca
Create Date: 2023-04-07 21:57:12.225632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be2efef5d418'
down_revision = '5f5f467666ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('edu_bg', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('skill', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('sentence', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('salary', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('salary')
        batch_op.drop_column('sentence')
        batch_op.drop_column('title')
        batch_op.drop_column('skill')
        batch_op.drop_column('edu_bg')
        batch_op.drop_column('company')

    # ### end Alembic commands ###