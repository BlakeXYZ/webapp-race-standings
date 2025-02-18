"""initial migration

Revision ID: 3c9def68d87e
Revises: 8751366afa5e
Create Date: 2025-02-17 21:35:59.275412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c9def68d87e'
down_revision = '8751366afa5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_name', sa.String(length=64), nullable=False),
    sa.Column('car_class', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('car_name', 'car_class', name='unique_car')
    )
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_car_car_class'), ['car_class'], unique=False)
        batch_op.create_index(batch_op.f('ix_car_car_name'), ['car_name'], unique=False)

    op.create_table('driver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('driver', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_driver_driver_name'), ['driver_name'], unique=True)

    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=64), nullable=False),
    sa.Column('event_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_event_date'), ['event_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_event_event_name'), ['event_name'], unique=True)

    op.create_table('driver_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['driver.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('driver_id', 'event_id', 'car_id', name='unique_driver_event')
    )
    with op.batch_alter_table('driver_event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_driver_event_car_id'), ['car_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_driver_event_driver_id'), ['driver_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_driver_event_event_id'), ['event_id'], unique=False)

    op.create_table('driver_event_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_event_id', sa.Integer(), nullable=False),
    sa.Column('fastest_lap', sa.Interval(), nullable=True),
    sa.Column('average_lap', sa.Interval(), nullable=True),
    sa.Column('total_laps', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['driver_event_id'], ['driver_event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('driver_event_stats', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_driver_event_stats_driver_event_id'), ['driver_event_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_driver_event_stats_total_laps'), ['total_laps'], unique=False)

    op.create_table('laptime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_event_id', sa.Integer(), nullable=False),
    sa.Column('laptime', sa.Interval(), nullable=False),
    sa.Column('run_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['driver_event_id'], ['driver_event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('laptime', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_laptime_run_number'), ['run_number'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('laptime', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_laptime_run_number'))

    op.drop_table('laptime')
    with op.batch_alter_table('driver_event_stats', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_driver_event_stats_total_laps'))
        batch_op.drop_index(batch_op.f('ix_driver_event_stats_driver_event_id'))

    op.drop_table('driver_event_stats')
    with op.batch_alter_table('driver_event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_driver_event_event_id'))
        batch_op.drop_index(batch_op.f('ix_driver_event_driver_id'))
        batch_op.drop_index(batch_op.f('ix_driver_event_car_id'))

    op.drop_table('driver_event')
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_event_name'))
        batch_op.drop_index(batch_op.f('ix_event_event_date'))

    op.drop_table('event')
    with op.batch_alter_table('driver', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_driver_driver_name'))

    op.drop_table('driver')
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_car_car_name'))
        batch_op.drop_index(batch_op.f('ix_car_car_class'))

    op.drop_table('car')
    # ### end Alembic commands ###
