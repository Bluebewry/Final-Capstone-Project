"""empty message

Revision ID: 22b9bf9cda53
Revises: 14f87b200a09
Create Date: 2023-03-01 13:47:30.810872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b9bf9cda53'
down_revision = '14f87b200a09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('img_url', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('img_url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('caption', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_pkey')
    )
    op.drop_table('product')
    # ### end Alembic commands ###
