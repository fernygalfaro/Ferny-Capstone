"""Initial migration

Revision ID: 12a0665e7170
Revises: 
Create Date: 2024-07-08 16:55:26.086885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12a0665e7170'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop constraints that depend on the 'users' table
    op.drop_constraint('user_preferences_user_id_fkey', 'user_preferences', type_='foreignkey')
    op.drop_constraint('user_likes_user_id_fkey', 'user_likes', type_='foreignkey')

    # Drop tables that depend on the 'users' table
    op.drop_table('user_preferences')
    op.drop_table('user_likes')

    # Now drop the 'users' table
    op.drop_table('users')

    # Create new tables
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password', sa.String(length=60), nullable=False),
        sa.Column('favorite_movie', sa.String(length=100), nullable=True),
        sa.Column('favorite_music', sa.String(length=100), nullable=True),
        sa.Column('image_file', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('preference', sa.String(length=100)),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'user_likes',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('like', sa.String(length=100)),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop new tables
    op.drop_table('user_likes')
    op.drop_table('user_preferences')
    op.drop_table('user')

    # Recreate old tables
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('is_creator', sa.Boolean, server_default=sa.text('false'), nullable=True),
        sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
        sa.UniqueConstraint('email', name='users_email_key'),
        sa.UniqueConstraint('username', name='users_username_key')
    )

    op.create_table(
        'user_preferences',
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('music_id', sa.Integer, nullable=False),
        sa.Column('movie_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_preferences_user_id_fkey'),
        sa.PrimaryKeyConstraint('user_id', 'music_id', 'movie_id', name='user_preferences_pkey')
    )

    op.create_table(
        'user_likes',
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('item_type', sa.String(length=10), nullable=False),
        sa.Column('item_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_likes_user_id_fkey'),
        sa.PrimaryKeyConstraint('user_id', 'item_type', 'item_id', name='user_likes_pkey')
    )

    # Recreate constraints
    op.create_foreign_key('user_preferences_user_id_fkey', 'user_preferences', 'users', ['user_id'], ['user_id'])
    op.create_foreign_key('user_likes_user_id_fkey', 'user_likes', 'users', ['user_id'], ['user_id'])
