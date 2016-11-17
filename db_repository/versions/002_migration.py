from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
camper_registration = Table('camper_registration', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('camper_id', INTEGER),
    Column('camp_session_id', INTEGER),
    Column('medical_form_id', INTEGER),
    Column('submission_timestamp', DATETIME),
    Column('payment_received', DATETIME),
    Column('registration_complete', BOOLEAN),
    Column('accepted', BOOLEAN),
)

camper_registration = Table('camper_registration', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('submission_timestamp', DateTime),
    Column('payment_received', DateTime),
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
    Column('accept', Boolean),
    Column('ppsrelease', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['camper_registration'].columns['medical_form_id'].drop()
    post_meta.tables['camper_registration'].columns['accept'].create()
    post_meta.tables['camper_registration'].columns['cabin_pal_name'].create()
    post_meta.tables['camper_registration'].columns['emgemail'].create()
    post_meta.tables['camper_registration'].columns['emgname'].create()
    post_meta.tables['camper_registration'].columns['emgrelation'].create()
    post_meta.tables['camper_registration'].columns['gradeinfall'].create()
    post_meta.tables['camper_registration'].columns['ppsrelease'].create()
    post_meta.tables['camper_registration'].columns['prevcamper'].create()
    post_meta.tables['camper_registration'].columns['shirtsize'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['camper_registration'].columns['medical_form_id'].create()
    post_meta.tables['camper_registration'].columns['accept'].drop()
    post_meta.tables['camper_registration'].columns['cabin_pal_name'].drop()
    post_meta.tables['camper_registration'].columns['emgemail'].drop()
    post_meta.tables['camper_registration'].columns['emgname'].drop()
    post_meta.tables['camper_registration'].columns['emgrelation'].drop()
    post_meta.tables['camper_registration'].columns['gradeinfall'].drop()
    post_meta.tables['camper_registration'].columns['ppsrelease'].drop()
    post_meta.tables['camper_registration'].columns['prevcamper'].drop()
    post_meta.tables['camper_registration'].columns['shirtsize'].drop()
