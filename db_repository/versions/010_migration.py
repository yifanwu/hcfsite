from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
organization = Table('organization', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('logo', String),
    Column('description', String),
)

panel = Table('panel', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('category', String),
    Column('description', String),
    Column('logo', String),
)

people = Table('people', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('description', String),
    Column('panel', String),
    Column('featured', Boolean),
)

entity = Table('entity', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String),
    Column('title', String(length=140)),
    Column('organization', String(length=140)),
    Column('panel', String(length=140)),
    Column('featured', Boolean),
    Column('org_logo', String(length=128)),
    Column('category', String(length=64)),
    Column('logo', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['organization'].drop()
    pre_meta.tables['panel'].drop()
    pre_meta.tables['people'].drop()
    post_meta.tables['entity'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['organization'].create()
    pre_meta.tables['panel'].create()
    pre_meta.tables['people'].create()
    post_meta.tables['entity'].drop()
