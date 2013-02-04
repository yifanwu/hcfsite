from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
team = Table('team', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('bio', String, nullable=False),
)

speaker = Table('speaker', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String, nullable=False),
    Column('img_url', String),
    Column('title', String),
    Column('organization', String),
    Column('panel', String),
    Column('featured', Boolean),
)

speaker = Table('speaker', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String, nullable=False),
    Column('img_url', String(length=140)),
    Column('title', String(length=140)),
    Column('organization', String(length=140)),
    Column('featured', Boolean),
    Column('panel_id', Integer),
)

posts = Table('posts', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('panel', String),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=5000)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('panel_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['team'].create()
    pre_meta.tables['speaker'].columns['panel'].drop()
    post_meta.tables['speaker'].columns['panel_id'].create()
    pre_meta.tables['posts'].columns['panel'].drop()
    post_meta.tables['posts'].columns['panel_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['team'].drop()
    pre_meta.tables['speaker'].columns['panel'].create()
    post_meta.tables['speaker'].columns['panel_id'].drop()
    pre_meta.tables['posts'].columns['panel'].create()
    post_meta.tables['posts'].columns['panel_id'].drop()
