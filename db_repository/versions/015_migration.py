from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
entity = Table('entity', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String, nullable=False),
    Column('img_url', String),
    Column('entity_type', String, nullable=False),
)

organization = Table('organization', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String, nullable=False),
    Column('img_url', String(length=140)),
)

panel = Table('panel', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('info', String(length=5000)),
    Column('category', String(length=64)),
)

speaker = Table('speaker', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String, nullable=False),
    Column('img_url', String(length=140)),
    Column('title', String(length=140)),
    Column('organization', String(length=140)),
    Column('panel', String(length=140)),
    Column('featured', Boolean),
)

advisor = Table('advisor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String, nullable=False),
    Column('img_url', String(length=140)),
    Column('title', String(length=140)),
    Column('organization', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entity'].drop()
    post_meta.tables['organization'].columns['description'].create()
    post_meta.tables['organization'].columns['img_url'].create()
    post_meta.tables['organization'].columns['name'].create()
    post_meta.tables['panel'].columns['info'].create()
    post_meta.tables['panel'].columns['name'].create()
    post_meta.tables['speaker'].columns['description'].create()
    post_meta.tables['speaker'].columns['img_url'].create()
    post_meta.tables['speaker'].columns['name'].create()
    post_meta.tables['advisor'].columns['description'].create()
    post_meta.tables['advisor'].columns['img_url'].create()
    post_meta.tables['advisor'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entity'].create()
    post_meta.tables['organization'].columns['description'].drop()
    post_meta.tables['organization'].columns['img_url'].drop()
    post_meta.tables['organization'].columns['name'].drop()
    post_meta.tables['panel'].columns['info'].drop()
    post_meta.tables['panel'].columns['name'].drop()
    post_meta.tables['speaker'].columns['description'].drop()
    post_meta.tables['speaker'].columns['img_url'].drop()
    post_meta.tables['speaker'].columns['name'].drop()
    post_meta.tables['advisor'].columns['description'].drop()
    post_meta.tables['advisor'].columns['img_url'].drop()
    post_meta.tables['advisor'].columns['name'].drop()
