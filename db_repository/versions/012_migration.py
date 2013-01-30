from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String),
    Column('title', String),
    Column('organization', String),
    Column('panel', String),
    Column('featured', Boolean),
    Column('org_logo', String),
    Column('img_path', String),
)

entity = Table('entity', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String),
    Column('img_url', String(length=140)),
    Column('entity_type', String(length=32), nullable=False),
)

speaker = Table('speaker', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('organization', String(length=140)),
    Column('panel', String(length=140)),
    Column('featured', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['entity'].create()
    post_meta.tables['speaker'].columns['organization'].create()
    post_meta.tables['speaker'].columns['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['entity'].drop()
    post_meta.tables['speaker'].columns['organization'].drop()
    post_meta.tables['speaker'].columns['title'].drop()
