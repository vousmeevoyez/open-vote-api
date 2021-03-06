"""added order_no

Revision ID: 8facdee76831
Revises: 036631130441
Create Date: 2019-03-20 20:51:56.479659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8facdee76831'
down_revision = '036631130441'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidate', sa.Column('order_no', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('candidate', 'order_no')
    # ### end Alembic commands ###
