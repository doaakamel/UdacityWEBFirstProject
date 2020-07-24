"""empty message

Revision ID: 4ab40dac1361
Revises: 1f8678e20a4a
Create Date: 2020-07-23 17:15:31.675862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ab40dac1361'
down_revision = '1f8678e20a4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Show_start_time'), 'Show', ['start_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Show_start_time'), table_name='Show')
    op.drop_table('Show')
    # ### end Alembic commands ###
