"""unique car constraint

Revision ID: 2fea2975f47f
Revises: 41ee2563c507
Create Date: 2025-01-31 22:25:08.557687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fea2975f47f'
down_revision = '41ee2563c507'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_car', ['car_name', 'car_class'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.drop_constraint('unique_car', type_='unique')

    # ### end Alembic commands ###
