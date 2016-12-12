from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
camper_registration = Table('camper_registration', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('submission_timestamp', TIMESTAMP),
    Column('payment_received', TIMESTAMP),
    Column('registration_complete', Boolean),
    Column('accepted', Boolean),
    Column('camper_id', Integer),
    Column('camp_session_id', Integer),
    Column('gradeinfall', String(length=2)),
    Column('prevcamper', Boolean),
    Column('cabin_pal_name', String(length=64)),
    Column('shirtsize', String(length=4)),
    Column('emgname', String(length=255)),
    Column('emgrelation', String(length=64)),
    Column('emgemail', String(length=64)),
    Column('emgphone', String(length=32)),
    Column('accept', Boolean),
    Column('ppsrelease', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['camper_registration'].columns['emgphone'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['camper_registration'].columns['emgphone'].drop()
