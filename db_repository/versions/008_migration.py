from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
people = Table('people', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('panel_id', Integer),
)

people = Table('people', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('panel', String(length=140)),
    Column('description', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['people'].columns['panel_id'].drop()
    post_meta.tables['people'].columns['description'].create()
    post_meta.tables['people'].columns['panel'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['people'].columns['panel_id'].create()
    post_meta.tables['people'].columns['description'].drop()
    post_meta.tables['people'].columns['panel'].drop()
