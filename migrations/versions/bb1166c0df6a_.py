"""empty message

Revision ID: bb1166c0df6a
Revises: 468a1ebfb400
Create Date: 2021-03-28 03:30:19.965544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb1166c0df6a'
down_revision = '468a1ebfb400'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courier', sa.Column('earnings', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courier', 'earnings')
    # ### end Alembic commands ###
