from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
<<<<<<< HEAD
=======
category = Table('category', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
)

panel = Table('panel', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('category', String),
    Column('info', String),
)

panel = Table('panel', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('info', String(length=5000)),
    Column('category_id', Integer),
)

>>>>>>> 8d12a52d7ea7a5a98dffc7ec7b2b0b41111bddfc

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
=======
    post_meta.tables['category'].create()
    pre_meta.tables['panel'].columns['category'].drop()
    post_meta.tables['panel'].columns['category_id'].create()
>>>>>>> 8d12a52d7ea7a5a98dffc7ec7b2b0b41111bddfc


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
=======
    post_meta.tables['category'].drop()
    pre_meta.tables['panel'].columns['category'].create()
    post_meta.tables['panel'].columns['category_id'].drop()
>>>>>>> 8d12a52d7ea7a5a98dffc7ec7b2b0b41111bddfc
