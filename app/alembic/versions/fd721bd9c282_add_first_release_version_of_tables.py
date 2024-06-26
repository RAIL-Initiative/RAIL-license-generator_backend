"""Add first release version of tables

Revision ID: fd721bd9c282
Revises: d4867f3a4c0a
Create Date: 2024-02-28 20:17:26.883159

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'fd721bd9c282'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('license',
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('license', sa.String(), nullable=False),
    sa.Column('application', sa.Boolean(), nullable=False),
    sa.Column('model', sa.Boolean(), nullable=False),
    sa.Column('sourcecode', sa.Boolean(), nullable=False),
    sa.Column('data', sa.Boolean(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('git_commit_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_license_id'), 'license', ['id'], unique=False)
    op.create_table('licensedomain',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('licensesource',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('license_licensedomain_link',
    sa.Column('license_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['licensedomain.id'], ),
    sa.ForeignKeyConstraint(['license_id'], ['license.id'], ),
    sa.PrimaryKeyConstraint('license_id', 'domain_id')
    )
    op.create_table('licenserestriction',
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['licensedomain.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['licensesource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('license_licenserestriction_link',
    sa.Column('license_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['license_id'], ['license.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['licenserestriction.id'], ),
    sa.PrimaryKeyConstraint('license_id', 'source_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('license_licenserestriction_link')
    op.drop_table('licenserestriction')
    op.drop_table('license_licensedomain_link')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('licensesource')
    op.drop_table('licensedomain')
    op.drop_index(op.f('ix_license_id'), table_name='license')
    op.drop_table('license')
    # ### end Alembic commands ###
