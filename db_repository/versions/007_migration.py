from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
medical_form = Table('medical_form', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('vaccine', VARCHAR(length=500)),
    Column('add', BOOLEAN),
    Column('asth', BOOLEAN),
    Column('bedw', BOOLEAN),
    Column('chestpain', BOOLEAN),
    Column('chro', BOOLEAN),
    Column('ckpox', DATE),
    Column('diab', BOOLEAN),
    Column('dizz', BOOLEAN),
    Column('dtap', DATE),
    Column('emodisorder', BOOLEAN),
    Column('explain', VARCHAR(length=1024)),
    Column('hib', DATE),
    Column('hosp', BOOLEAN),
    Column('insu', BOOLEAN),
    Column('insucomp', VARCHAR(length=128)),
    Column('insuphon', VARCHAR(length=128)),
    Column('insupoli', VARCHAR(length=128)),
    Column('insusubs', VARCHAR(length=128)),
    Column('meningitis', DATE),
    Column('mump', DATE),
    Column('other', BOOLEAN),
    Column('parents_id', INTEGER),
    Column('pcv', DATE),
    Column('polio', DATE),
    Column('recinj', BOOLEAN),
    Column('restrictions', VARCHAR(length=1024)),
    Column('seenprof', BOOLEAN),
    Column('seiz', BOOLEAN),
    Column('sign', BOOLEAN),
    Column('surg', BOOLEAN),
    Column('swim', BOOLEAN),
    Column('tb', DATE),
    Column('tbtest', BOOLEAN),
)

medical_form = Table('medical_form', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('allergies', String(length=1024)),
    Column('dtap', Date),
    Column('mump', Date),
    Column('polio', Date),
    Column('ckpox', Date),
    Column('meningitis', Date),
    Column('hib', Date),
    Column('pcv', Date),
    Column('tb', Date),
    Column('tbtest', Boolean),
    Column('hosp', Boolean),
    Column('surg', Boolean),
    Column('chro', Boolean),
    Column('bedw', Boolean),
    Column('recinj', Boolean),
    Column('asth', Boolean),
    Column('diab', Boolean),
    Column('seiz', Boolean),
    Column('dizz', Boolean),
    Column('chestpain', Boolean),
    Column('add', Boolean),
    Column('emodisorder', Boolean),
    Column('seenprof', Boolean),
    Column('other', Boolean),
    Column('explain', String(length=1024)),
    Column('swim', Boolean),
    Column('restrictions', String(length=1024)),
    Column('insu', Boolean),
    Column('insucomp', String(length=128)),
    Column('insupoli', String(length=128)),
    Column('insusubs', String(length=128)),
    Column('insuphon', String(length=128)),
    Column('sign', Boolean),
    Column('parents_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['medical_form'].columns['vaccine'].drop()
    post_meta.tables['medical_form'].columns['allergies'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['medical_form'].columns['vaccine'].create()
    post_meta.tables['medical_form'].columns['allergies'].drop()
