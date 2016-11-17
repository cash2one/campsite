from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
parents = Table('parents', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('g1fn', VARCHAR(length=64)),
    Column('g1ln', VARCHAR(length=64)),
    Column('g2fn', VARCHAR(length=64)),
    Column('g2ln', VARCHAR(length=64)),
    Column('g1street', VARCHAR(length=64)),
    Column('g1city', VARCHAR(length=64)),
    Column('g1state', VARCHAR(length=64)),
    Column('g1zipcode', VARCHAR(length=64)),
    Column('g1country', VARCHAR(length=64)),
    Column('g2street', VARCHAR(length=64)),
    Column('g2city', VARCHAR(length=64)),
    Column('g2state', VARCHAR(length=64)),
    Column('g2zipcode', VARCHAR(length=64)),
    Column('g2country', VARCHAR(length=64)),
    Column('g1phone', VARCHAR(length=64)),
    Column('g2phone', VARCHAR(length=64)),
    Column('g1email', VARCHAR(length=64)),
    Column('g2email', VARCHAR(length=64)),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['parents'].columns['g1email'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['parents'].columns['g1email'].create()
