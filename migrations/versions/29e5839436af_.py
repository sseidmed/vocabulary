"""empty message

Revision ID: 29e5839436af
Revises: 15c68dd20043
Create Date: 2020-10-26 18:10:26.671448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29e5839436af'
down_revision = '15c68dd20043'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.drop_index('ix_word_name')
        batch_op.create_index(batch_op.f('ix_word_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_word_name'))
        batch_op.create_index('ix_word_name', ['name'], unique=False)

    # ### end Alembic commands ###
