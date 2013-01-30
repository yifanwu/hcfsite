from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
entity = Table('entity', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String),
    Column('title', String),
    Column('organization', String),
    Column('panel', String),
    Column('featured', Boolean),
    Column('org_logo', String),
    Column('category', String),
    Column('logo', String),
)

entity = Table('entity', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String),
    Column('img_path', String(length=140)),
    Column('title', String(length=140)),
    Column('organization', String(length=140)),
    Column('panel', String(length=140)),
    Column('featured', Boolean),
    Column('org_logo', String(length=128)),
    Column('category', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entity'].columns['logo'].drop()
    post_meta.tables['entity'].columns['img_path'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['entity'].columns['logo'].create()
    post_meta.tables['entity'].columns['img_path'].drop()
