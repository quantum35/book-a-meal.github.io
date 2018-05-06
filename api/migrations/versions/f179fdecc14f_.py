"""empty message

Revision ID: f179fdecc14f
Revises: 2e87225e9513
Create Date: 2018-05-06 08:32:09.784398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f179fdecc14f'
down_revision = '2e87225e9513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'menus', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('orders_item_id_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'menus', ['item_id'], ['id'], ondelete='CASCADE')
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('users', 'admin')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_item_id_fkey', 'orders', 'menus', ['item_id'], ['id'])
    op.drop_constraint(None, 'menus', type_='foreignkey')
    op.drop_column('menus', 'user_id')
    # ### end Alembic commands ###
