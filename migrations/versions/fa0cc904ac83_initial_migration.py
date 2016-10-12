"""Initial Migration

Revision ID: fa0cc904ac83
Revises: None
Create Date: 2016-09-29 17:59:57.929111

"""

# revision identifiers, used by Alembic.
revision = 'fa0cc904ac83'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agencies',
    sa.Column('ein', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=256), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('next_request_number', sa.Integer(), nullable=True),
    sa.Column('default_email', sa.String(length=254), nullable=True),
    sa.Column('appeals_email', sa.String(length=254), nullable=True),
    sa.PrimaryKeyConstraint('ein')
    )
    op.create_table('emails',
    sa.Column('metadata_id', sa.Integer(), nullable=False),
    sa.Column('to', sa.String(), nullable=True),
    sa.Column('cc', sa.String(), nullable=True),
    sa.Column('bcc', sa.String(), nullable=True),
    sa.Column('subject', sa.String(length=5000), nullable=True),
    sa.Column('email_content', sa.String(), nullable=True),
    sa.Column('attachments', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table('extensions',
    sa.Column('metadata_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table('files',
    sa.Column('metadata_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('mime_type', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table('instructions',
    sa.Column('metadata_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table('links',
    sa.Column('metadata_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table('notes',
    sa.Column('metadata_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=5000), nullable=True),
    sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('reasons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agency', sa.Integer(), nullable=True),
    sa.Column('deny_reason', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['agency'], ['agencies.ein'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.String(length=19), nullable=False),
    sa.Column('agency', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=90), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_submitted', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('submission', sa.String(length=30), nullable=True),
    sa.Column('current_status', sa.Enum('Open', 'In Progress', 'Due Soon', 'Overdue', 'Closed', 'Re-Opened', name='statuses'), nullable=True),
    sa.Column('visibility', postgresql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['agency'], ['agencies.ein'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('guid', sa.String(length=64), nullable=False),
    sa.Column('user_type', sa.String(length=64), nullable=False),
    sa.Column('agency', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('middle_initial', sa.String(length=1), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('email_validated', sa.Boolean(), nullable=False),
    sa.Column('terms_of_use_accepted', sa.String(length=16), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('organization', sa.String(length=128), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('fax_number', sa.String(length=15), nullable=True),
    sa.Column('mailing_address', postgresql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['agency'], ['agencies.ein'], ),
    sa.PrimaryKeyConstraint('guid', 'user_type'),
    sa.UniqueConstraint('guid')
    )
    op.create_table('responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.String(length=19), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('metadata_id', sa.Integer(), nullable=True),
    sa.Column('privacy', sa.Enum('private', 'release_private', 'release_public', name='privacy'), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_requests',
    sa.Column('user_guid', sa.String(length=64), nullable=False),
    sa.Column('user_type', sa.String(length=64), nullable=False),
    sa.Column('request_id', sa.String(length=19), nullable=False),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
    sa.ForeignKeyConstraint(['user_guid', 'user_type'], ['users.guid', 'users.user_type'], ),
    sa.PrimaryKeyConstraint('user_guid', 'user_type', 'request_id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.String(length=19), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.Column('user_type', sa.String(length=64), nullable=True),
    sa.Column('response_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('previous_response_value', sa.String(), nullable=True),
    sa.Column('new_response_value', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
    sa.ForeignKeyConstraint(['response_id'], ['responses.id'], ),
    sa.ForeignKeyConstraint(['user_id', 'user_type'], ['users.guid', 'users.user_type'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    op.drop_table('user_requests')
    op.drop_table('responses')
    op.drop_table('users')
    op.drop_table('requests')
    op.drop_table('reasons')
    op.drop_table('roles')
    op.drop_table('notes')
    op.drop_table('links')
    op.drop_table('instructions')
    op.drop_table('files')
    op.drop_table('extensions')
    op.drop_table('emails')
    op.drop_table('agencies')
    ### end Alembic commands ###
