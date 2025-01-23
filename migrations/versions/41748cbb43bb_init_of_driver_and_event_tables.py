"""init of driver and event tables

Revision ID: 41748cbb43bb
Revises: 
Create Date: 2025-01-22 22:03:14.158738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41748cbb43bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_name', sa.String(length=64), nullable=False),
    sa.Column('driver_car', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('driver', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_driver_driver_car'), ['driver_car'], unique=True)
        batch_op.create_index(batch_op.f('ix_driver_driver_name'), ['driver_name'], unique=True)

    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_event_name'), ['event_name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_event_name'))

    op.drop_table('event')
    with op.batch_alter_table('driver', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_driver_driver_name'))
        batch_op.drop_index(batch_op.f('ix_driver_driver_car'))

    op.drop_table('driver')
    # ### end Alembic commands ###
