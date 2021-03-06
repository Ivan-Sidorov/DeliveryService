"""empty message

Revision ID: 8a82c5355b3c
Revises: 
Create Date: 2021-03-22 19:28:20.941466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a82c5355b3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courier',
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('courier_id')
    )
    op.create_table('type',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('vol', sa.Integer(), nullable=True),
    sa.Column('coef', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('type_id')
    )
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('region', sa.Integer(), nullable=True),
    sa.Column('assign', sa.String(length=30), nullable=True),
    sa.Column('complete', sa.String(length=30), nullable=True),
    sa.Column('courier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['courier.courier_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('regions',
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.Column('region', sa.Integer(), nullable=True),
    sa.Column('courier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['courier.courier_id'], ),
    sa.PrimaryKeyConstraint('region_id')
    )
    op.create_table('working_hours',
    sa.Column('wh_id', sa.Integer(), nullable=False),
    sa.Column('hours', sa.String(length=15), nullable=True),
    sa.Column('courier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['courier.courier_id'], ),
    sa.PrimaryKeyConstraint('wh_id')
    )
    op.create_table('preferred_time',
    sa.Column('dt_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('hours', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('dt_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('preferred_time')
    op.drop_table('working_hours')
    op.drop_table('regions')
    op.drop_table('order')
    op.drop_table('type')
    op.drop_table('courier')
    # ### end Alembic commands ###
