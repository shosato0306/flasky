"""empty message

Revision ID: cc401fea4b7d
Revises: 8f5b9110a8b5
Create Date: 2018-12-22 17:02:22.079001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc401fea4b7d'
down_revision = '8f5b9110a8b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_heml', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_heml')
    # ### end Alembic commands ###
