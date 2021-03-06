"""empty message

Revision ID: 8ad4fea8861a
Revises: 
Create Date: 2021-10-20 19:17:09.464834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ad4fea8861a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Puntos',
    sa.Column('manzana', sa.String(), nullable=False),
    sa.Column('ciudad', sa.String(), nullable=True),
    sa.Column('personas', sa.String(), nullable=True),
    sa.Column('latitud', sa.Numeric(), nullable=True),
    sa.Column('longitud', sa.Numeric(), nullable=True),
    sa.Column('bajo', sa.Integer(), nullable=True),
    sa.Column('medio', sa.Integer(), nullable=True),
    sa.Column('alto', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('manzana')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Puntos')
    # ### end Alembic commands ###
