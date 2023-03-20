"""empty message

Revision ID: 2e2ff034cf56
Revises: 45ee8eb3795a
Create Date: 2023-03-17 14:00:05.363495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e2ff034cf56'
down_revision = '45ee8eb3795a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('course_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('form_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'students', ['student_id'], ['id'])
        batch_op.create_foreign_key(None, 'forms', ['form_id'], ['id'])
        batch_op.create_foreign_key(None, 'courses', ['course_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scores', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'forms', ['id'], ['id'])
        batch_op.drop_column('form_id')
        batch_op.drop_column('course_id')
        batch_op.drop_column('student_id')

    # ### end Alembic commands ###
