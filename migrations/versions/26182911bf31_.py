"""empty message

Revision ID: 26182911bf31
Revises: 4ab40dac1361
Create Date: 2020-07-23 17:19:34.066118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26182911bf31'
down_revision = '4ab40dac1361'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('Upcomming', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'Upcomming')
    # ### end Alembic commands ###